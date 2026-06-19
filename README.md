# BIRD.skills (Agent Skills)

> Agent skills for writing, validating, formatting, and shipping BIRD (BIRD1/2/3) routing daemon configurations.

## Which skill do I need?

| If your pain point is...                                                          | Use this skill                           |
| --------------------------------------------------------------------------------- | ---------------------------------------- |
| "I need to write or fix `bird.conf`, `bird2.conf`, `bird3.conf`, or `bird6.conf`" | [`bird-agent`](./bird-agent)             |
| "I need editor support or the `birdcc` CLI installed"                             | [`birdcc-installer`](./birdcc-installer) |
| "I want BIRD linting or formatting in GitHub Actions"                             | [`birdcc-cicd`](./birdcc-cicd)           |

### Skill descriptions

- **[`bird-agent`](./bird-agent)** — Write, validate, format, and debug BIRD (BIRD1/2/3) routing daemon configs. Use when the user mentions `bird.conf`, `bird2.conf`, `bird3.conf`, `bird6.conf`, `bird.config.json`, `birdcc lint/fmt`, `bird -p` validation, BIRD filter syntax, or BGP/routing configuration questions.
- **[`birdcc-installer`](./birdcc-installer)** — Install BIRD editor support and the `birdcc` CLI. Use when the user asks about VSCode/VSCodium/Cursor/Windsurf/Trae/Kiro/Antigravity/Neovim/Vim/JetBrains BIRD plugins, or installing the `birdcc` command-line toolkit.
- **[`birdcc-cicd`](./birdcc-cicd)** — Add the `setup-birdcc` GitHub Action to CI/CD workflows. Use when the user wants to lint, format, or validate BIRD configs in GitHub Actions.

## What are Agent Skills?

[Agent Skills](https://agentskills.io/) are reusable, agent-readable capability bundles. Each skill contains a `SKILL.md` manifest, `agents/openai.yaml` metadata, optional PEP 723 stdlib-only helper scripts, and focused reference guides.

## Quick start for AI agents

After installing the skills, point an agent at a workspace with BIRD files and ask naturally:

```text
"Check this bird2.conf for errors and format it"
"Install BIRD support for my editor"
"Add BIRD validation to our GitHub Actions workflow"
```

The agent will use the right skill, run `birdcc lint` / `fmt`, validate with `bird -p`, or generate CI snippets as needed.

## Installation

### Claude Code

```bash
/plugin marketplace add bird-chinese-community/BIRD.skills
/plugin install bird-agent@bird-skills
/plugin install birdcc-installer@bird-skills
/plugin install birdcc-cicd@bird-skills
```

### Codex CLI

```bash
codex plugin marketplace add bird-chinese-community/BIRD.skills
# Then inside Codex, use /plugins to install individual skills
```

### skills.sh

```bash
npx skills add bird-chinese-community/BIRD.skills
```

### agentskill.sh

```bash
npx @agentskill.sh/cli setup
# Then in any agent session:
/learn @bird-chinese-community/BIRD.skills
```

### Manual install

Clone the repo and copy or symlink skill folders into your agent's skills directory (e.g. `~/.claude/skills/`, `~/.codex/skills/`, `.agents/skills/`).

## Security

BIRD configs may contain sensitive AS numbers, peer IPs, BGP passwords, and BGP community. DO NOT commit production secrets or share unsanitized configs publicly.

## Contributing

See [`AGENTS.md`](./AGENTS.md) for development conventions. To add a skill, create a new folder matching the existing layout with `SKILL.md`, `agents/openai.yaml`, and references/scripts as appropriate.

## License

[MIT](./LICENSE)
