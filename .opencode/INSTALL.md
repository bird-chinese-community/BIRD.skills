# Installing BIRD.skills for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed

## Installation

Add `bird-skills` to the `plugin` array in your `opencode.json` (global or project-level):

```json
{
  "plugin": ["bird-skills@git+https://github.com/bird-chinese-community/BIRD.skills.git"]
}
```

Restart OpenCode. The plugin installs through OpenCode's plugin manager and registers
three skills:

- `bird-agent` - write, validate, format, and debug BIRD routing-daemon configs
- `birdcc-installer` - install BIRD editor support and the `birdcc` CLI
- `birdcc-cicd` - add `setup-birdcc` to GitHub Actions workflows

Verify by asking: "List my BIRD skills" or "Load bird-agent".

OpenCode uses its own plugin install. If you also use Claude Code, Codex, Cursor, or
another harness, install BIRD.skills separately for each one.

## Updating

OpenCode installs BIRD.skills through a git-backed package spec. Some OpenCode and
Bun versions pin that resolved git dependency in a lockfile or cache, so a restart may
not pick up the newest commit. If updates do not appear, clear OpenCode's package cache
or reinstall the plugin.

To pin a specific version, use a branch or tag:

```json
{
  "plugin": ["bird-skills@git+https://github.com/bird-chinese-community/BIRD.skills.git#v1.0.0"]
}
```

## Troubleshooting

### Plugin not loading

1. Check logs: `opencode run --print-logs "hello" 2>&1 | grep -i bird`
2. Verify the plugin line in your `opencode.json`
3. Make sure you're running a recent version of OpenCode

### Skills not found

1. Use OpenCode's native `skill` tool to list available skills
2. Check that the plugin is loading (see above)
3. Each skill needs a `SKILL.md` file with valid YAML frontmatter

### Windows install issues

Some Windows OpenCode builds have upstream installer issues with git-backed plugin
specs. If OpenCode cannot install the plugin, try installing with system npm and
pointing OpenCode at the local package:

```powershell
npm install bird-skills@git+https://github.com/bird-chinese-community/BIRD.skills.git --prefix "$HOME\.config\opencode"
```

Then use the installed package path in `opencode.json`:

```json
{
  "plugin": ["~/.config/opencode/node_modules/bird-skills"]
}
```

## Getting Help

- Report issues: https://github.com/bird-chinese-community/BIRD.skills/issues
- Main documentation: https://github.com/bird-chinese-community/BIRD.skills/blob/main/README.md
