# Codex Reliability Workflow

[中文说明](README.zh-CN.md)

A portable, risk-adaptive personal workflow for complex, multi-step Codex tasks. It combines reviewed plans, human approval, checkpoint verification and independent acceptance reviews. The goal is fewer consequential errors at reasonable total cost; no achieved numeric error rate is claimed.

## Workflow

1. The main agent evaluates complexity, impact, uncertainty and verifiability. Simple, reversible tasks proceed directly. For complex tasks it recommends standard or enhanced workflow; the user chooses.
2. A plan defines scope, dependencies, model assignments, resource expectations and acceptance criteria. A frontier reviewer checks the plan and its verification methods before human approval of a specific version.
3. Workers execute approved subtasks with evidence. High-impact intermediate outputs are checked before dependent work. Independent tasks can run in parallel; dependent or conflicting writes stay sequential.
4. Acceptance uses approved methods and thresholds, with evidence for every critical requirement. Reviewers independently check whether those methods adequately cover the original request.
5. Standard mode uses one fresh frontier acceptance reviewer. Enhanced mode uses three initially isolated reviewers: requirements coverage, independent reproduction, and counterexamples. Findings are resolved by evidence, not majority vote.
6. Repairs trigger rechecks; material changes trigger renewed review or plan approval. Missing critical evidence remains UNVERIFIED, never PASS.

## Install

Requires Python 3.11+ and a local Codex client supporting the documented custom-agent schema. Inspect the package before installing.

```sh
git clone https://github.com/aPuzzledCodingBear/codex-reliability-workflow.git
cd codex-reliability-workflow
python3 install.py --dry-run
python3 install.py
```

`--target PATH` selects a Codex home. Otherwise the installer uses `CODEX_HOME`, falling back to `~/.codex`. Start a new session or restart the client afterward; existing sessions can retain old instructions.

The installer merges a marked block into global `AGENTS.md` and an existing `AGENTS.override.md`, installs nine custom roles and `reliability/WORKFLOW.md`, enables up to three child threads, and sets main/default child model to `gpt-6.2-sol` with medium reasoning. It preserves unrelated instructions and settings, including permissions, authentication, provider, MCP and plugins. Replaced files are backed up. Repeated installation is idempotent.

The complete parsed TOML is checked against exactly the intended changes. Unsupported layouts fail before writes rather than silently changing unrelated content.

## Models

| Role | Requested model | Reasoning |
| --- | --- | --- |
| Main orchestrator / worker | `gpt-6.2-sol` | medium |
| Difficult planner | `gpt-6.2-sol` | high |
| Plan / acceptance / enhanced reviewers | `gpt-6.2-astra` | high |
| Narrow low-risk worker | `gpt-6-luna` | medium |
| Visual / computer-use specialist | `gpt-6.1-terra` | medium |

These are requested settings, not proof of model access. If a model is unavailable, explicitly choose an available replacement and update `POLICY.md` and the role TOML files before reinstalling. If changing the main/default child model, also update its settings and semantic-preservation expectations in `install.py`. Do not silently downgrade reviews. Names and supported settings may change between client releases.

## Multiple devices

Install on **each execution host**. Remote clients controlling a configured host use that host's configuration. This package does not automatically synchronize devices or configure remote access. Pull updates and rerun the installer on each host.

Hosted ChatGPT Work/web does not read local Codex files. Managed rules, project instructions and explicit overrides may affect behavior.

## Evidence, privacy and restoration

`WORKFLOW.md` defines task-local evidence: requirement → criterion → method → threshold → evidence → PASS/FAIL/UNVERIFIED. Keep runtime records private unless sharing is authorized.

Backups under `<Codex home>/reliability/backups/<timestamp>/` can contain private existing configuration: **never commit or upload them**. Raw prompt diagnostics, local verification reports, caches and task evidence are excluded. Publication review checked published sources for credentials, private paths, contact details and host-specific records; this bounded inspection is not a guarantee against every possible secret.

```sh
python3 -m unittest discover -s tests -v
python3 install.py --dry-run
```

Where supported, `codex debug prompt-input` verifies instruction discovery. Its output may contain private context; do not publish it. Some diagnostic subcommands reject `--strict-config`.

For rollback, consult the backup's `manifest.json`, restore backed-up existing files and remove only newly created files listed there. Preserve unrelated changes made since installation rather than blindly restoring old configuration.

## Reliability limits

These are behavioral instructions, not hard CI enforcement, a separate read-only sandbox or a statistical certificate. Three agreeing reviewers do not establish a small error probability. Numeric reliability requires trusted outcome labels, held-out full-workflow evaluation for a defined task class, uncertainty bounds and distribution-drift checks. Track completion and abstention alongside escaped errors.

## References

- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Global AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Settings and environment boundaries](https://learn.chatgpt.com/docs/developer-settings)
- [Conformal Risk Control](https://arxiv.org/abs/2208.02814)
- [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296)

No license has been selected for this initial publication; public availability alone does not grant an open-source license.

Model selection and dated pricing evidence: [English / 中文](MODEL-SELECTION.md).
