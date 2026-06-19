# Installing BIRD.skills

There are three ways to install these skills. Pick the one that matches your agent harness:

| Method             | Best for                                                                                                                           | What you get                                                   |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Plugin install** | Harnesses that support plugins (Claude Code, GitHub Copilot CLI, Codex CLI, Antigravity, Gemini CLI, Kimi Code, Pi, Factory Droid) | Native install for a single harness; pick the skills you want. |
| **Skills install** | Any harness supported by `skills.sh` (universal `.agents/skills` plus 60+ agents including Cursor, OpenCode, Kimi Code CLI, etc.)  | One command, then choose which agents receive the skills.      |
| **Manual install** | Platforms not covered by plugin or `skills.sh`                                                                                     | Copy or symlink the skill folders yourself.                    |

> **Recommendation:**
>
> - Please use **plugin install** whenever possible for the best experience and update support.
> - When a plugin install is not available, use **skills install** as a quick fallback. This is especially useful if you use multiple agent platforms.
> - Use **manual install** only when neither of the above covers your harness.

## 1. Prerequisites

- Make sure you know whether your current agent platform supports plugins. You can check via WebSearch or the platform's documentation.

## 2. Plugin install

Plugins give you a native install for a specific harness. They let you install the whole bundle and then enable only the skills you want. If you use multiple harnesses, install the plugin in each one separately.

### Claude Code

```bash
/plugin marketplace add bird-chinese-community/BIRD.skills
/plugin install bird-agent@bird-skills
/plugin install birdcc-installer@bird-skills
/plugin install birdcc-cicd@bird-skills
```

### GitHub Copilot CLI

Add this repository as a plugin marketplace, then install the skills you want:

```bash
copilot plugin marketplace add bird-chinese-community/BIRD.skills
copilot plugin install bird-agent@bird-skills
copilot plugin install birdcc-installer@bird-skills
copilot plugin install birdcc-cicd@bird-skills
```

In an interactive Copilot session you can also use:

```text
/plugin marketplace add bird-chinese-community/BIRD.skills
/plugin install bird-agent@bird-skills
/plugin install birdcc-installer@bird-skills
/plugin install birdcc-cicd@bird-skills
```

### Antigravity

```bash
agy plugin install https://github.com/bird-chinese-community/BIRD.skills
```

Antigravity runs the plugin's session-start hook, so the skills are active from the first message. Reinstall with the same command to update.

### Codex App

Codex App shares plugin configuration with Codex CLI. Side-load via the CLI first, then the skills are available inside the App:

```bash
codex plugin marketplace add bird-chinese-community/BIRD.skills
# Then inside Codex, use /plugins to install individual skills
```

### Codex CLI

```bash
codex plugin marketplace add bird-chinese-community/BIRD.skills
# Then inside Codex, use /plugins to install individual skills
```

### Factory Droid

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

### Gemini CLI

Install the extension:

```bash
gemini extensions install https://github.com/bird-chinese-community/BIRD.skills
```

Update later:

```bash
gemini extensions update BIRD.skills
```

> Note: Google is sunsetting Gemini CLI in favor of Antigravity CLI. New users should consider installing via Antigravity instead.

### Kimi Code

Open Kimi Code's plugin manager with `/plugins`, then install directly from this repository:

```bash
/plugins install https://github.com/bird-chinese-community/BIRD.skills
```

### Pi

```bash
pi install git:github.com/bird-chinese-community/BIRD.skills
```

For local development, run Pi with this checkout loaded as a temporary package:

```bash
pi -e /path/to/BIRD.skills
```

### 3. Skills install

If your harness does not support plugins, use `skills.sh` as a quick fallback. This installs all three skills at once:

```bash
npx -y skills@latest add bird-chinese-community/BIRD.skills --skill bird-agent --skill birdcc-cicd --skill birdcc-installer -a <AGENT_NAME> -y
```

> Replace `<AGENT_NAME>` with any agent listed in the [Skills.sh README (Supported Agents)](https://raw.githubusercontent.com/vercel-labs/skills/refs/heads/main/README.md) (please read this first), such as `claude-code`, `codex`, `github-copilot`, `antigravity`, etc.
>
> You can also use `-g` to install skills globally (recommended). If you have multiple agents, pass multiple `-a` arguments to specify which agents receive the skills.
>
> Note: You must ask the user for consent before choosing whether to install "only under the current project" or "globally" (global is recommended).

After installation, you can still disable individual skills in your harness settings if you only need some of them.

### 4. Manual install

If neither plugins nor `skills.sh` work for your harness (for example, Cursor or OpenCode):

1. Clone this repository locally:

   ```bash
   git clone https://github.com/bird-chinese-community/BIRD.skills
   ```

2. Symlink the skill folders you need into your agent's skills directory (e.g. `~/.claude/skills/`, `~/.codex/skills/`, `~/.agents/skills/`, `~/.cursor/skills/`).

3. Restart the agent. Some agents also need their skill cache cleared — check your agent's docs for the cache path (often `~/.<agent>/cache` or similar).

---

> Tips: To update later, re-run the install command for your harness. For manual installs, `git pull` and re-copy or re-symlink the skill folders.
