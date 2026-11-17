import importlib.util
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def test_preservation_backup_and_idempotence(self):
        original = 'model="previous"\n[agents] # comment\nenabled=false\n[features]\njs_repl=false\n'
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            (target / 'config.toml').write_text(original)
            (target / 'AGENTS.md').write_text('Keep personal instruction.\n')
            (target / 'AGENTS.override.md').write_text('Keep override.\n')
            result = installer.install(target)
            config = tomllib.loads((target / 'config.toml').read_text())
            self.assertFalse(config['features']['js_repl'])
            self.assertTrue(config['agents']['enabled'])
            self.assertTrue((target / 'AGENTS.md').read_text().startswith('Keep personal instruction.'))
            self.assertTrue((target / 'AGENTS.override.md').read_text().startswith('Keep override.'))
            self.assertEqual((Path(result['backup']) / 'config.toml').read_text(), original)
            self.assertEqual(installer.install(target)['changed'], [])

    def test_multiline_ambiguity_fails_before_writes(self):
        original = 'developer_instructions = """\nmodel_reasoning_effort = "literal content"\n"""\n'
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            (target / 'config.toml').write_text(original)
            with self.assertRaisesRegex(ValueError, 'semantic preservation'):
                installer.install(target)
            self.assertEqual((target / 'config.toml').read_text(), original)
            self.assertEqual(sorted(p.name for p in target.iterdir()), ['config.toml'])

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / 'new-home'
            self.assertTrue(installer.install(target, dry_run=True)['changed'])
            self.assertFalse(target.exists())

    def test_write_failure_rolls_back(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            (target / 'config.toml').write_text('model="previous"\n')
            write = installer.atomic_write
            failed = False

            def fail_once(path, content, mode=0o600):
                nonlocal failed
                if path.name == 'config.toml' and not failed:
                    failed = True
                    raise OSError('Injected failure')
                return write(path, content, mode)

            with patch.object(installer, 'atomic_write', side_effect=fail_once):
                with self.assertRaises(OSError):
                    installer.install(target)
            self.assertFalse((target / 'AGENTS.md').exists())
            self.assertEqual((target / 'config.toml').read_text(), 'model="previous"\n')


if __name__ == '__main__':
    unittest.main()
