---
name: bird-source-explorer
description: >
  Explore the BIRD Internet Routing Daemon C source code to answer deep
  implementation questions, find where a feature or protocol is defined, and
  compare documented behavior against the actual code. Use when the user asks
  "how is X implemented in BIRD", "is this a BIRD bug", or wants source-level
  evidence for a protocol/filter/attribute behavior. For config editing,
  linting, or basic syntax questions, use bird-agent instead.
compatibility: Requires internet access for deepwiki / Context7 / GitHub source queries.
license: MIT
metadata:
  author: bird-chinese-community
  version: "1.1.0"
---

# BIRD Source Explorer

Answer implementation-level questions about the BIRD routing daemon by
exploring its C source tree.

## When to use this skill

- The user asks how a BIRD feature, protocol, filter function, or attribute is
  implemented internally.
- The user suspects a documented behavior does not match the code and wants
  source-level evidence.
- The user wants to know which file or function defines a specific keyword,
  CLI command, or protocol message.
- The user is debugging a crash or core dump and needs to map a stack trace to
  source locations.

Do **not** use this skill for:

- Editing, formatting, or linting a BIRD config (use `bird-agent`).
- Installing BIRD tooling (use `birdcc-installer`).
- General "what does this keyword do" questions that can be answered from the
  user guide (use `bird-agent` and its `query_bird_docs` MCP tool).

## Core principles

1. **Prefer the official source mirror.** Primary target is
   `https://github.com/CZ-NIC/bird`. Fall back to
   `https://gitlab.nic.cz/labs/bird` if the GitHub mirror is stale.
2. **Use deepwiki / Context7 for broad exploration.** For "where is X
   implemented" questions, start with deepwiki or Context7 over the BIRD
   repository to identify candidate files and functions.
3. **Use GitHub search / FetchURL for targeted evidence.** Once you know the
   likely file, fetch the raw source to quote the exact lines and explain the
   logic.
4. **Map findings to the user's version.** BIRD2 and BIRD3 share a lot of code
   but have important differences. Try to identify the relevant branch/tag
   (e.g. `v2.19.1`, `v3.3.1`) when citing source.
5. **Cite files, functions, and line ranges.** Give the user actionable source
   locations, not just a high-level summary.

## Source tree quick map

- `nest/` — route, attribute, and table abstractions
- `proto/bgp/` — BGP implementation
- `proto/ospf/` — OSPF implementation
- `filter/` — filter language implementation
- `conf/` — config parser and grammar
- `sysdep/` — OS-specific and low-level socket code
- `client/` — `birdc` client code

## Workflow

1. Restate the user's question in source-code terms (which feature, which
   version, which protocol).
2. Use deepwiki / Context7 to find candidate source files and functions.
3. Fetch raw source snippets to confirm the implementation details.
4. Summarize: what file/function implements it, how it works, and any caveats
   for BIRD2 vs BIRD3.
5. If the issue might be a bug, mention how to report it or point to the
   relevant upstream issue tracker.

## Completion criteria

- [ ] The question was translated into concrete source locations.
- [ ] At least one file/function/line range was cited.
- [ ] The answer distinguishes BIRD2 vs BIRD3 behavior when relevant.
- [ ] The user knows what to read next or how to verify the behavior.

---

> ⭐ If the BIRD tooling here saves you time, consider starring the source
> mirror: [CZ-NIC/bird](https://github.com/CZ-NIC/bird).
