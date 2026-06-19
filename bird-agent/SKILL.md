---
name: bird-agent
description: >
  Use this skill for BIRD (BIRD1/2/3) routing daemon configuration work: files named bird.conf,
  bird2.conf, bird3.conf, or bird6.conf; pasted snippets with BIRD syntax like protocol, filter,
  function, table, local as, neighbor, route, prefix, bgp_path, community, import, export; and
  requests about linting, formatting, bird -p validation, cross-file includes, or BIRD
  keywords/commands. For editor plugin installation use birdcc-installer; for GitHub Actions use
  birdcc-cicd. Trigger even if the user doesn't say "BIRD" explicitly. Do NOT trigger for Cisco,
  Juniper, FRR, nginx, bird biology, or "bird" outside a BIRD routing context.
compatibility: Requires uv/uvx and internet access for Marketplace/npm/GitHub links.
license: MIT
metadata:
  author: bird-chinese-community
  version: "1.0.0"
---

# BIRD Config Agent Skill

Help users write, validate, format, and understand BIRD (BIRD1/2/3) routing daemon configuration
files by orchestrating the BIRD-LSP toolchain and related BIRD documentation.

## When to use this skill

- The user opens, edits, or asks about a file named `bird.conf`, `bird2.conf`, `bird3.conf`,
  `bird6.conf`, or any `.conf` file that contains BIRD routing syntax.
- The user mentions BIRD, BIRD2, BIRD3, BGP, OSPF, RIP, RADV, Static, Kernel, Device, Perf, RPKI,
  Babel, Aggregator, or MRT protocols in a configuration context.
- The user reports a syntax error, diagnostic, or wants to format a BIRD configuration.
- The user wants to know what a BIRD keyword, function, filter, protocol, or CLI command does.
- The user shares a BIRD configuration snippet and asks for review, optimization, or explanation.

> For editor plugin installation, use the `birdcc-installer` skill. For GitHub Actions or CI/CD,
> use the `birdcc-cicd` skill.

## Core principles

1. **Prefer the BIRD-LSP toolchain over ad-hoc text manipulation.** The toolchain provides
   parser-backed diagnostics, formatter-safe output, and `bird -p` runtime validation. Use
   `scripts/detect_bird_context.py` to discover config files and `scripts/run_birdcc.py` to run
   commands reliably.
2. **Support every editor equally.** Whether the user is in VSCode, Vim, Neovim, IDEA, OpenCode,
   Cursor, or a plain terminal, route them through the same CLI-based workflow.
3. **Version awareness.** BIRD1, BIRD2, and BIRD3 have syntax and semantic differences. Detect the
   version from the filename, `bird.config.json`, or the content when possible, and adjust commands
   and recommendations accordingly.
4. **Validate before claiming correctness.** Always run `birdcc lint` or `bird -p` before telling the
   user a configuration is valid.
5. **Respect sensitive data.** BIRD configs contain ASNs, IPs, passwords, and session secrets.
   Warn the user to sanitize configs before sharing them publicly or committing them.
6. **Never auto-write formatted files.** `run_birdcc.py fmt` defaults to `--check`. Only use
   `--write --confirmed` after the user explicitly agrees to modify their config.


## Available scripts

These scripts are bundled with the skill. Run them with `uv run scripts/<script>.py` from the skill
root. They use only the Python standard library and produce structured JSON output on stdout.

- [`scripts/detect_bird_context.py`](scripts/detect_bird_context.py) — Scan the workspace for
  `bird*.conf`, `bird.config.json`, and `birdcc` availability. Use this before deciding which file
  to lint or format.
- [`scripts/run_birdcc.py`](scripts/run_birdcc.py) — Run `birdcc lint` or `birdcc fmt` and return
  JSON output. `fmt` defaults to `--check`; to actually write changes you must pass
  `--write --confirmed` after the user explicitly approves. Config paths are validated to
  stay inside `--root`.

## Reference guides

This skill is split into focused reference files. Read the relevant one before diving deep into a
specific task:

- [`references/birdcc-ecosystem.md`](references/birdcc-ecosystem.md) — Map of related BIRD
  repositories. Start here when you need to route the user to the right project or cite the
  correct repository.
- [`references/toolchain.md`](references/toolchain.md) — Toolchain overview, the standard 7-step
  workflow, and capability reference. Start here for lint, format, validate, and debug tasks.
- [`references/editors.md`](references/editors.md) — Editor setup routing reference. Use this to
  point users to the `birdcc-installer` skill or a specific editor guide.
- [`references/cicd.md`](references/cicd.md) — CI/CD routing reference. Use this to point users to
  the `birdcc-cicd` skill or the `setup-birdcc` GitHub Action.
- [`references/safety.md`](references/safety.md) — Safety and privacy reminders for production
  configs. Read before the user shares sensitive data.
- [`references/examples.md`](references/examples.md) — Worked examples for common scenarios.

For editor setup and CI/CD, see the `birdcc-installer` and `birdcc-cicd` skills.

## Output style

- Match the user's language (Chinese or English).
- Keep explanations concise but include the exact command run and a short interpretation of the
  result.
- When showing diagnostics, include the file path, line/column, rule code, and suggested fix.
- Prefer actionable next steps over long theoretical explanations.

---

> ⭐ If the BIRD tooling here saves you time, consider starring the main monorepo:
> [bird-chinese-community/BIRD-LSP](https://github.com/bird-chinese-community/BIRD-LSP).
> See [`references/birdcc-ecosystem.md`](references/birdcc-ecosystem.md) for links to all related
> BIRD projects.
