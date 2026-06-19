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

There are three ways to install these skills. Pick the one that matches your agent harness:

| Method             | Best for                                                                                                         | What you get                                                        |
| ------------------ | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Plugin install** | Harnesses that support plugins (Claude Code, Codex CLI, Antigravity, Gemini CLI, Pi, Factory Droid, Copilot CLI) | The full bundle; install all skills or pick only the ones you need. |
| **Skills install** | Any harness that supports `skills.sh`                                                                            | A quick one-line install of all skills.                             |
| **Manual install** | Harnesses without plugin or skills support (Cursor, Kimi Code, OpenCode, etc.)                                   | Copy or symlink the skill folders yourself.                         |

> **Recommendation:** Try the **plugin install** first. It gives you the most control. If your harness does not support plugins, fall back to **skills install**. Use **manual install** only when neither of the above works.

### Plugin install

Plugins are the preferred way to install. They let you install the whole bundle and then enable only the skills you want. If you use multiple harnesses, install the plugin in each one separately.

#### Claude Code

```bash
/plugin marketplace add bird-chinese-community/BIRD.skills
/plugin install bird-agent@bird-skills
/plugin install birdcc-installer@bird-skills
/plugin install birdcc-cicd@bird-skills
```

#### Antigravity

```bash
agy plugin install https://github.com/bird-chinese-community/BIRD.skills
```

Antigravity runs the plugin's session-start hook, so the skills are active from the first message. Reinstall with the same command to update.

#### Codex App

Codex App shares plugin configuration with Codex CLI. Side-load via the CLI first, then the skills are available inside the App:

```bash
codex plugin marketplace add bird-chinese-community/BIRD.skills
# Then inside Codex, use /plugins to install individual skills
```

#### Codex CLI

```bash
codex plugin marketplace add bird-chinese-community/BIRD.skills
# Then inside Codex, use /plugins to install individual skills
```

#### Factory Droid

Register the marketplace:

```bash
droid plugin marketplace add https://github.com/bird-chinese-community/BIRD.skills
```

Install the skills:

```bash
droid plugin install bird-agent@BIRD.skills
droid plugin install birdcc-installer@BIRD.skills
droid plugin install birdcc-cicd@BIRD.skills
```

#### Gemini CLI

Install the extension:

```bash
gemini extensions install https://github.com/bird-chinese-community/BIRD.skills
```

Update later:

```bash
gemini extensions update BIRD.skills
```

#### GitHub Copilot CLI

Register the marketplace:

```bash
copilot plugin marketplace add bird-chinese-community/BIRD.skills
```

Install the skills:

```bash
copilot plugin install bird-agent@bird-chinese-community/BIRD.skills
copilot plugin install birdcc-installer@bird-chinese-community/BIRD.skills
copilot plugin install birdcc-cicd@bird-chinese-community/BIRD.skills
```

#### Pi

```bash
pi install git:github.com/bird-chinese-community/BIRD.skills
```

For local development, run Pi with this checkout loaded as a temporary package:

```bash
pi -e /path/to/BIRD.skills
```

### Skills install

If your harness does not support plugins, use `skills.sh` as a quick fallback. This installs all three skills at once:

```bash
npx skills add bird-chinese-community/BIRD.skills
```

You can still disable individual skills in your harness settings if you only need some of them.

### Manual install

If neither plugins nor `skills.sh` work for your harness (for example, Cursor, Kimi Code, or OpenCode), clone the repo and copy or symlink the skill folders into your agent's skills directory (e.g. `~/.claude/skills/`, `~/.codex/skills/`, `.agents/skills/`).

## Security

BIRD configs may contain sensitive AS numbers, peer IPs, BGP passwords, and BGP community. DO NOT commit production secrets or share unsanitized configs publicly.

## Contributing

See [`AGENTS.md`](./AGENTS.md) for development conventions. To add a skill, create a new folder matching the existing layout with `SKILL.md`, `agents/openai.yaml`, and references/scripts as appropriate.

## License

[MIT](./LICENSE)
