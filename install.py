#!/usr/bin/env python3
"""Install only the portable personal reliability policy; preserve other settings."""
import argparse
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parent
BEGIN = '<!-- BEGIN PERSONAL RELIABILITY POLICY v1 -->'
END = '<!-- END PERSONAL RELIABILITY POLICY v1 -->'


def policy_merge(old, policy):
    if BEGIN in old or END in old:
        if old.count(BEGIN) != 1 or old.count(END) != 1:
            raise ValueError('Ambiguous policy markers; refusing to overwrite')
        start, finish = old.index(BEGIN), old.index(END) + len(END)
        if finish < start:
            raise ValueError('Invalid policy marker order')
        return old[:start] + policy.strip() + old[finish:]
    return old.rstrip() + ('\n\n' if old.strip() else '') + policy.strip() + '\n'


def set_table(text, table, settings):
    if text and not text.endswith('\n'):
        text += '\n'
    lines = text.splitlines(keepends=True)
    headers = [i for i, line in enumerate(lines) if re.match(r'^\s*\[', line)]
    if table is None:
        start, end = 0, headers[0] if headers else len(lines)
    else:
        matches = [i for i in headers if re.match(r'^\s*\[' + re.escape(table) + r'\]\s*(?:#.*)?$', lines[i])]
        if not matches:
            return text.rstrip() + '\n\n[' + table + ']\n' + ''.join(k + ' = ' + json.dumps(v) + '\n' for k, v in settings.items())
        start = matches[0] + 1
        end = next((i for i in headers if i >= start), len(lines))
    body = lines[start:end]
    for key, value in settings.items():
        pattern = re.compile(r'^\s*' + re.escape(key) + r'\s*=')
        hits = [i for i, line in enumerate(body) if pattern.match(line)]
        replacement = key + ' = ' + json.dumps(value) + '\n'
        if hits:
            body[hits[0]] = replacement
        else:
            body.append(replacement)
    return ''.join(lines[:start] + body + lines[end:])


def desired(target):
    changes = {}
    policy = (ROOT / 'POLICY.md').read_text()
    for name in ['AGENTS.md', 'AGENTS.override.md']:
        path = target / name
        if name == 'AGENTS.md' or path.exists():
            changes[path] = policy_merge(path.read_text() if path.exists() else '', policy)
    config = target / 'config.toml'
    old = config.read_text() if config.exists() else ''
    before = tomllib.loads(old)
    # Do not alter sandbox, approval, provider, authentication, MCP, or plugins.
    new = set_table(old, None, {'model': 'gpt-6.1-sol', 'model_reasoning_effort': 'medium'})
    new = set_table(new, 'agents', {'enabled': True, 'max_concurrent_threads_per_session': 3,
                                 'default_subagent_model': 'gpt-6.1-sol',
                                 'default_subagent_reasoning_effort': 'medium'})
    # The textual editor must never silently modify TOML string contents or
    # unrelated settings. Compare the entire parsed document to the exact
    # authorized semantic change, before creating backups or writing files.
    expected = copy.deepcopy(before)
    expected.update(model='gpt-6.1-sol', model_reasoning_effort='medium')
    expected.setdefault('agents', {}).update(
        enabled=True, max_concurrent_threads_per_session=3,
        default_subagent_model='gpt-6.1-sol',
        default_subagent_reasoning_effort='medium')
    if tomllib.loads(new) != expected:
        raise ValueError('Unsupported TOML layout: semantic preservation check failed; no files changed. Use a TOML-aware editor for this host.')
    changes[config] = new
    changes[target / 'reliability/WORKFLOW.md'] = (ROOT / 'WORKFLOW.md').read_text()
    for agent in sorted((ROOT / 'agents').glob('*.toml')):
        content = agent.read_text()
        parsed = tomllib.loads(content)
        assert all(k in parsed for k in ('name', 'description', 'developer_instructions', 'model', 'model_reasoning_effort'))
        changes[target / 'agents' / agent.name] = content
    return {p: s for p, s in changes.items() if not p.exists() or p.read_text() != s}


def atomic_write(path, content, mode=0o600):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.reliability-', dir=path.parent)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def install(target, dry_run=False):
    target = target.expanduser().resolve()
    changes = desired(target)
    for path in changes:
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != target.parent):
            raise ValueError('Refusing symlinked destination: ' + str(path))
    if dry_run or not changes:
        return {'changed': [str(p.relative_to(target)) for p in changes], 'dry_run': dry_run}
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup = target / 'reliability/backups' / stamp
    backup.mkdir(parents=True, mode=0o700)
    originals = {}
    for path in changes:
        originals[path] = (path.read_bytes(), path.stat().st_mode & 0o777) if path.exists() else None
        if path.exists():
            saved = backup / path.relative_to(target)
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, saved)
            saved.chmod(0o600)
    written = []
    try:
        for path, content in changes.items():
            mode = originals[path][1] if originals[path] else 0o600
            atomic_write(path, content, mode)
            written.append(path)
    except Exception:
        for path in reversed(written):
            if originals[path] is None:
                path.unlink()
            else:
                atomic_write(path, originals[path][0].decode(), originals[path][1])
        raise
    manifest = {'version': 1, 'target': str(target), 'backup': str(backup),
                'files': {str(p.relative_to(target)): {'existed': originals[p] is not None,
                         'sha256': hashlib.sha256(s.encode()).hexdigest()} for p, s in changes.items()}}
    atomic_write(backup / 'manifest.json', json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))))
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    print(json.dumps(install(args.target, args.dry_run), indent=2))
