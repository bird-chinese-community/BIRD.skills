# Agent Guide for BIRD Agent Skills

This document is written for AI coding agents that need to understand and work on the
`BIRD-skills` repository. The repository contains [Agent Skills](https://agentskills.io/)
for BIRD (BIRD1/2/3) routing-daemon configuration work, editor setup, and CI/CD workflows.

## Project overview

This repository hosts three agent skills:

- **`bird-agent`** — Helps users write, validate, format, and understand BIRD (BIRD1/2/3)
  routing-daemon configuration files. It orchestrates the `@birdcc/cli` (`birdcc`) toolchain
  and community documentation.
- **`birdcc-installer`** — Guides users through installing BIRD editor support and the
  `@birdcc/cli` (`birdcc`) command-line toolkit.
- **`birdcc-cicd`** — Helps users add the `setup-birdcc` GitHub Action to CI/CD workflows.

There is no application server or runtime service in this repository. The deliverables are
skill manifests, reference documentation, helper scripts (where applicable), evaluation
fixtures, and agent invocation metadata.

## Repository structure

```text
.
├── README.md                          # Human-facing project description
├── .gitignore                         # Standard Python/Node/IDE ignores; also ignores docs/superpowers/
├── bird-agent/                        # BIRD config agent skill
│   ├── SKILL.md                       # Skill manifest (description, when to use, principles)
│   ├── agents/openai.yaml             # OpenAI agent interface metadata
│   ├── scripts/                       # PEP 723 stdlib-only helper scripts
│   │   ├── detect_bird_context.py
│   │   └── run_birdcc.py
│   ├── references/                    # Focused reference guides
│   │   ├── birdcc-ecosystem.md
│   │   ├── toolchain.md
│   │   ├── cicd.md
│   │   ├── editors.md
│   │   ├── safety.md
│   │   └── examples.md
│   └── evals/                         # Evaluation prompts, assertions, and fixtures
│       ├── evals.json
│       └── fixtures/
├── birdcc-installer/                  # BIRD tooling installer agent skill
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── scripts/
│   │   ├── detect_editor.py
│   │   ├── detect_ide.py
│   │   └── check_cli.py
│   ├── references/
│   │   ├── editors.md
│   │   ├── cli.md
│   │   └── offline.md
│   └── evals/
│       └── evals.json
└── birdcc-cicd/                       # BIRD CI/CD agent skill
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/
    │   └── setup-birdcc.md
    └── evals/
        └── evals.json
```

## Technology stack

- **Language**: Python 3.10+ (helper scripts only)
- **Script packaging**: PEP 723 inline script metadata; no `pyproject.toml`, `package.json`,
  `Cargo.toml`, or other package manifest in this repository.
- **Runtime runner**: `uv run` / `uvx` is the expected way to execute scripts.
- **External tools consumed at runtime**:
  - `@birdcc/cli` (`birdcc`) — the BIRD linter/formatter/LSP CLI (Node.js/npm/pnpm/yarn/bun).
  - `bird` — the BIRD daemon binary, used for `bird -p` validation.
  - `code` — the VSCode CLI, used to detect installed BIRD extensions.
- **Documentation**: Markdown.
- **Agent metadata**: YAML (`agents/openai.yaml`).
- **Evaluations**: JSON (`evals/evals.json`) with `transcript.md`/`workflow.md` assertion checks.

## Build and runtime architecture

There is **no build step**. The repository is a collection of static skill assets and standalone
scripts.

### Running helper scripts

Each script is self-contained and uses only the Python standard library. Run them from the skill
root with `uv run`:

```bash
# bird-agent
uv run bird-agent/scripts/detect_bird_context.py --root .
uv run bird-agent/scripts/run_birdcc.py lint bird-agent/evals/fixtures/bird.conf --root .
uv run bird-agent/scripts/run_birdcc.py fmt bird-agent/evals/fixtures/bird-unformatted.conf --root .

# birdcc-installer
uv run birdcc-installer/scripts/detect_editor.py --root .
uv run birdcc-installer/scripts/detect_ide.py
uv run birdcc-installer/scripts/check_cli.py
```

`run_birdcc.py` requires `birdcc` to be on `PATH`. It defaults `fmt` to `--check` and only allows
`--write` when the user also passes `--confirmed`.

### Runtime data flow

1. The agent reads the skill manifest (`SKILL.md`) and relevant reference files.
2. For context-aware tasks, the agent invokes `scripts/detect_bird_context.py`,
   `scripts/detect_editor.py`, or `scripts/detect_ide.py` and parses the JSON output.
3. For lint/format/validate tasks, the agent invokes `scripts/run_birdcc.py`, which shells out to
   `birdcc` and returns structured JSON.
4. For installation tasks, the agent reads `references/editors.md`, `references/cli.md`, or
   `references/offline.md` and provides exact commands/IDs.
5. For CI/CD tasks, the agent reads `birdcc-cicd/references/setup-birdcc.md` and produces a workflow
   snippet.

## Code organization and module divisions

### Skill directories

All skills share the same internal layout, except `birdcc-cicd` does not include
`scripts/`:

- `SKILL.md` — Front-matter metadata plus usage instructions. This is the single source of truth
  for when the skill should be invoked, core principles, available scripts, and output style.
- `agents/openai.yaml` — Display name, short description, brand color, invocation policy, and
  tool dependencies.
- `scripts/` — Small, focused Python utilities that produce JSON on stdout.
  (`birdcc-cicd` has no scripts.)
- `references/` — Markdown references the agent reads before handling a specific task.
- `evals/` — Evaluation definitions and fixture files.

### Scripts

- `bird-agent/scripts/detect_bird_context.py`
  - Scans the workspace for `bird*.conf` files, `bird.config.json`, and checks whether `birdcc` is
    available.
  - Uses filename heuristics to infer BIRD version (`bird.conf`, `bird2.conf`, `bird3.conf`,
    `bird6.conf`).
  - Rejects symlink escapes and large files.

- `bird-agent/scripts/run_birdcc.py`
  - Validates the supplied config path is inside `--root` and is a regular file.
  - Rejects paths starting with `-` to avoid flag injection.
  - Builds and executes `birdcc lint` or `birdcc fmt`.
  - Parses JSON diagnostics from `birdcc lint --format json`.

- `birdcc-installer/scripts/detect_editor.py`
  - Detects editor signals in the workspace (`.vscode/`, `.idea/`, `.cursorrules`, Neovim/Vim
    configs, etc.) and optionally in the user's home directory.
  - Returns detected editors and a confidence level.

- `birdcc-installer/scripts/detect_ide.py`
  - Detects installed IDEs/editors, their extension/plugin state, and marketplace availability.
  - Can optionally install extensions when passed `--install` and confirmed by the user.

- `birdcc-installer/scripts/check_cli.py`
  - Checks whether `birdcc` is installed and reports its version.

### References

- `bird-agent/references/toolchain.md` — Standard 7-step workflow (detect, check tools, discover
  config, run diagnostics, format, answer semantic questions, source-level debugging).
- `bird-agent/references/birdcc-ecosystem.md` — Map of community-maintained BIRD tooling
  repositories.
- `bird-agent/references/cicd.md` — `setup-birdcc` GitHub Action usage (routing reference).
- `bird-agent/references/editors.md` — Editor setup routing reference.
- `bird-agent/references/safety.md` — Handling sensitive data in BIRD configs.
- `bird-agent/references/examples.md` — Worked examples for common user scenarios.
- `birdcc-installer/references/editors.md` — Editor setup for VSCode, VSCodium, Cursor, Windsurf,
  Trae, Kiro, Antigravity, Neovim, Vim, and JetBrains IDEA.
- `birdcc-installer/references/cli.md` — Installing and verifying `@birdcc/cli`.
- `birdcc-installer/references/offline.md` — Offline / air-gapped / mirror install guidance.
- `birdcc-cicd/references/setup-birdcc.md` — Adding `setup-birdcc` to GitHub Actions.

## Development conventions

- **Python scripts must use only the standard library** and declare PEP 723 metadata:
  ```python
  # /// script
  # requires-python = ">=3.10"
  # dependencies = []
  # ///
  ```
- **Output JSON on stdout** with `ensure_ascii=False` and an indentation of 2 spaces.
- **No third-party dependencies** in this repository; rely on externally installed `birdcc`,
  `bird`, and `code` CLIs.
- **Security-first path handling**: scripts resolve paths, enforce `--root` containment, and reject
  arguments that start with `-`.
- **Do not auto-write user files**: `run_birdcc.py fmt` defaults to `--check`; `--write` requires
  `--confirmed` and explicit user approval.
- **Match the user's language** (Chinese or English) in agent responses.
- **Version awareness**: distinguish BIRD1, BIRD2, and BIRD3 syntax/semantics.
- **Star callouts**: when a user benefits from a related BIRD project, invite them to star the
  relevant repository once per interaction.

## Testing instructions

There is no automated test runner checked into this repository. Evaluation is defined in
`evals/evals.json` files:

- Each entry has an `id`, `name`, `prompt`, `expected_output`, optional `files`, and a list of
  `assertions`.
- Assertions are checked against generated `transcript.md` or `workflow.md` files (the evaluation
  harness is external).
- Fixtures live in `bird-agent/evals/fixtures/`:
  - `bird.conf` — missing semicolon after `router id`.
  - `bird-unformatted.conf` — inconsistent indentation for formatter testing.
  - `cross-file/main.conf` and `cross-file/peers.conf` — cross-file include diagnostic testing.

### Validating scripts locally

You can verify that the helper scripts are syntactically correct and executable:

```bash
# Syntax check all Python scripts
python3 -m py_compile \
  bird-agent/scripts/detect_bird_context.py \
  bird-agent/scripts/run_birdcc.py \
  birdcc-installer/scripts/detect_editor.py \
  birdcc-installer/scripts/detect_ide.py \
  birdcc-installer/scripts/check_cli.py

# Run with uv
uv run bird-agent/scripts/detect_bird_context.py --root .
uv run birdcc-installer/scripts/detect_editor.py --root .
uv run birdcc-installer/scripts/check_cli.py
```

If `birdcc` is installed, you can also exercise the lint path:

```bash
uv run bird-agent/scripts/run_birdcc.py lint bird-agent/evals/fixtures/bird.conf --root .
```

## Deployment and distribution

- Skills are consumed by an OpenAI Codex-compatible agent skill loader using the metadata in
  `agents/openai.yaml` and the manifest in `SKILL.md`.
- The repository references externally published artifacts (npm `@birdcc/cli`, VSCode/OpenVSX
  extensions, GitHub Action `bird-chinese-community/setup-birdcc`) but does not publish its own
  package.
- There is no CI/CD configuration inside this repository itself.

## Security considerations

- BIRD configurations frequently contain sensitive data: AS numbers, peer IPs, BGP passwords,
  community strings, and route filters. The skill explicitly warns users to sanitize configs before
  sharing them publicly.
- `run_birdcc.py` does not write files unless the user passes both `--write` and `--confirmed`.
- `run_birdcc.py` validates that config paths resolve to regular files inside `--root` and rejects
  paths beginning with `-`.
- When validating configs, prefer the read-only parse check `bird -p` over starting the BIRD daemon.
- Do not commit production secrets to this repository or suggest that users commit them.

## License

MIT (see `LICENSE`).
