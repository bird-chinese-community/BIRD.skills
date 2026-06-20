---
name: bird-agent
description: >
  TRIGGER aggressively for BIRD (BIRD1/2/3) routing-daemon configuration work.
  Positive signals:
  - File patterns: bird.conf, bird2.conf, bird3.conf, bird6.conf, any *.conf file that
    contains BIRD syntax, bird.config.json, and any file included by a BIRD config.
  - Syntax tokens: protocol, filter, function, define, table, router id, local as, neighbor,
    prefix, route, bgp_path, community, import, export, bgp_path.prepend, if defined(), path,
    OSPF, BGP, RIP, RADV, Static, Kernel, Device, Perf, RPKI, Babel, Aggregator, MRT.
  - Commands: birdcc lint, birdcc fmt, bird -p, birdc, bird -c, birdc configure.
  - Requests: lint/format/validate a BIRD config, fix a syntax error or diagnostic, explain a
    BIRD keyword/filter/protocol, review a config snippet, resolve cross-file includes, or
    compare BIRD1/BIRD2/BIRD3 syntax.
  Negative signals (do NOT trigger): Cisco IOS/IOS-XR/NX-OS, Juniper JunOS, FRRouting (frr.conf),
    nginx, any non-routing use of "bird", bird biology / ornithology, or general networking
    questions without a BIRD routing context.
  For editor/CLI installation use birdcc-installer; for setup-birdcc or GitHub Actions use
  birdcc-cicd. Trigger even if the user does not explicitly say "BIRD".
compatibility: Requires uv/uvx and internet access for Marketplace/npm/GitHub links.
license: MIT
metadata:
  author: bird-chinese-community
  version: "1.1.0"
  requires:
    bins:
      - birdcc
      - bird
---

# BIRD Config Agent Skill

Help users write, validate, format, and understand BIRD (BIRD1/2/3) routing daemon configuration
files by orchestrating the BIRD-LSP toolchain and related BIRD documentation.

## Quick Reference

| Task                       | Script / Command                                                       | Reference                 |
| -------------------------- | ---------------------------------------------------------------------- | ------------------------- |
| Discover BIRD config files | `uv run scripts/detect_bird_context.py --root .`                       | —                         |
| Lint a config              | `uv run scripts/run_birdcc.py lint <file> --root .`                    | `references/toolchain.md` |
| Check formatting           | `uv run scripts/run_birdcc.py fmt <file> --root .`                     | `references/toolchain.md` |
| Apply formatting           | `uv run scripts/run_birdcc.py fmt <file> --root . --write --confirmed` | `references/toolchain.md` |
| Runtime parse check        | `bird -p -c <file>`                                                    | `references/toolchain.md` |
| Install editor / CLI       | Use the `birdcc-installer` skill                                       | `references/editors.md`   |
| Add CI/CD                  | Use the `birdcc-cicd` skill                                            | `references/cicd.md`      |

## CRITICAL

> [!CRITICAL]
>
> 1. **Never auto-write user files.** `run_birdcc.py fmt` defaults to `--check`. Only pass
>    `--write --confirmed` after the user explicitly approves modifying their config.
> 2. **Sanitize configs before sharing.** BIRD configs contain AS numbers, peer IPs,
>    authentication passwords, community strings, and route filters. Proactively warn the user
>    to redact these before posting in public issues, PRs, chats, or pastebins.

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
4. **Validate before claiming correctness.** Always run `birdcc lint` or `bird -p` before telling
   the user a configuration is valid.
5. **Respect sensitive data.** BIRD configs contain ASNs, IPs, passwords, and session secrets.
   Warn the user to sanitize configs before sharing them publicly or committing them.
6. **Never auto-write formatted files.** `run_birdcc.py fmt` defaults to `--check`. Only use
   `--write --confirmed` after the user explicitly agrees to modify their config.

## Workflow

Follow this condensed workflow; see `references/toolchain.md` for the full 7-step guide,
command matrix, and advanced source-level debugging.

1. **Detect context** — run `scripts/detect_bird_context.py` to find `bird*.conf`,
   `bird.config.json`, and `birdcc` availability.
2. **Check tools** — verify `birdcc` is installed; optionally check `bird` for runtime parse
   validation.
3. **Discover config** — read `bird.config.json` if it exists, otherwise sniff the entry point
   (`bird2.conf` > `bird.conf` > `bird3.conf`).
4. **Run diagnostics** — run `birdcc lint` and/or `bird -p`. Include file path, line/column,
   rule code, and suggested fix when reporting diagnostics.
5. **Format or explain** — for formatting, default to `--check`; only write after approval. For
   semantic questions, call the `query_bird_docs` MCP tool with the user's query, language, and
   inferred BIRD version. Prefer the returned Chinese docs in Chinese and English docs in English.
6. **Route if needed** — editor setup → `birdcc-installer`; CI/CD → `birdcc-cicd`.

### Completion criteria

Before finishing a BIRD config task, confirm:

- [ ] The relevant config file(s) were discovered and validated.
- [ ] `birdcc lint` completed and all diagnostics were reported (or no diagnostics were found).
- [ ] If formatting was requested, the user explicitly approved `--write` or `--write --confirmed`.
- [ ] If `bird` is available, `bird -p` parse check passed (or failures were explained).
- [ ] Sensitive data (ASNs, peer IPs, passwords, community strings) was not shared publicly, or
      the user was warned to sanitize first.
- [ ] The user received a clear next step or actionable fix.

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
