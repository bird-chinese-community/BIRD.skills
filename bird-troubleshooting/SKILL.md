---
name: bird-troubleshooting
description: >
  Diagnose complex BIRD routing-daemon problems that cross configuration,
  source-code, and tooling boundaries. Use when the daemon fails to start,
  crashes at runtime, logs a confusing error, or behaves differently from the
  documented semantics after lint passes. For simple config syntax or
  formatting issues, use bird-agent; for source-level questions, use
  bird-source-explorer.
compatibility: Requires uv/uvx and optionally local access to bird/birdcc binaries and logs.
license: MIT
metadata:
  author: bird-chinese-community
  version: "1.0.0"
---

# BIRD Troubleshooting

Orchestrate diagnostics across the BIRD tool chain to resolve complex runtime
and configuration problems.

## When to use this skill

- The `bird` daemon fails to start or crashes.
- Logs contain an error that is not explained by a simple syntax fix.
- The config passes `birdcc lint` / `bird -p` but the observed behavior differs
  from the documentation.
- The problem may involve BIRD internals and requires source-level evidence.
- The user is unsure whether the issue is config, environment, tooling, or an
  upstream bug.

Do **not** use this skill for:

- Plain config editing or linting (use `bird-agent`).
- Installation of `birdcc` or editor plugins (use `birdcc-installer`).
- Pure source-code archaeology without a runtime symptom (use
  `bird-source-explorer`).

## Core principles

1. **Collect first.** Run `uv run scripts/collect_diagnostics.py --root .` to gather versions,
   detected configs, and tool availability before guessing.
2. **Start with config/docs.** Route configuration and documented-behavior
   questions to `bird-agent` and its `query_bird_docs` MCP tool.
3. **Escalate to source when needed.** If the config looks correct but the
   behavior is unexpected, use `bird-source-explorer` to inspect the relevant
   C implementation.
4. **Fix environment gaps.** If `birdcc` or `bird` is missing, route to
   `birdcc-installer`.
5. **Synthesize, don't dump.** Give the user a prioritized list of hypotheses
   and the next verification step for each.

## Workflow

1. Run `uv run scripts/collect_diagnostics.py --root .` to collect baseline
   info.
2. Ask for (or read) the relevant log snippet / error message / crash trace.
3. If the error points to a config issue, invoke `bird-agent` workflow.
4. If the config is correct but behavior is wrong, invoke
   `bird-source-explorer` to find the implementation.
5. If tooling is missing, invoke `birdcc-installer`.
6. Summarize findings as:
   - Most likely cause
   - Other plausible causes
   - Next verification command or source file to inspect

## Available scripts

- [`scripts/collect_diagnostics.py`](scripts/collect_diagnostics.py) — Collect
  `birdcc`/`bird` versions and detected config files. Uses only the Python
  standard library.

## Completion criteria

- [ ] Diagnostics were collected and shared with the user.
- [ ] At least one hypothesis has supporting evidence (log line, source
      location, or config line).
- [ ] The user has a clear next step to verify or fix the issue.
- [ ] Sensitive data (peer IPs, ASNs, passwords) was redacted before quoting
      logs or configs.

---

> ⭐ If the BIRD tooling here saves you time, consider starring the main
> monorepo: [bird-chinese-community/BIRD-LSP](https://github.com/bird-chinese-community/BIRD-LSP).
