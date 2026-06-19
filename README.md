# BIRD Agent Skills

This repository hosts agent skills for BIRD routing configuration, editor setup, and CI/CD workflows.

## Skills

- [`bird-agent`](./bird-agent) — Write, validate, format, and debug BIRD (BIRD1/2/3) routing
  daemon configuration files.
- [`birdcc-installer`](./birdcc-installer) — Install BIRD editor support and the `birdcc`
  command-line toolkit.
- [`birdcc-cicd`](./birdcc-cicd) — Add the `setup-birdcc` GitHub Action to CI/CD workflows.

## Usage

These skills follow the [Agent Skills](https://agentskills.io/)
convention. Most skills include:

- `SKILL.md` — Skill manifest and usage instructions
- `agents/openai.yaml` — OpenAI agent invocation metadata
- `scripts/` — PEP 723 stdlib-only helper scripts runnable with `uv run`
- `references/` — Focused reference guides

`birdcc-cicd` has no `scripts/` directory; it only provides `SKILL.md`,
`agents/openai.yaml`, and `references/`.

## Installation

### Claude Code

Add the marketplace once, then install the skills you need:

```bash
/plugin marketplace add bird-chinese-community/BIRD.skills
/plugin install bird-agent@bird-skills
/plugin install birdcc-installer@bird-skills
/plugin install birdcc-cicd@bird-skills
```

### OpenAI Codex CLI

```bash
codex plugin marketplace add bird-chinese-community/BIRD.skills
# Then inside Codex, use /plugins to install bird-agent, birdcc-installer, or birdcc-cicd
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

Clone the repo and copy or symlink the skill folders into your agent's skills
directory (e.g. `~/.claude/skills/`, `~/.codex/skills/`, or `.agents/skills/`).

## License

[MIT](./LICENSE)
