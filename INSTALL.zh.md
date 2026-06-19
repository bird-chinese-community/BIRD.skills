# 安装 BIRD.skills

共有三种安装方式，请根据你使用的 Agent 平台选择：

| 安装方式        | 适用平台                                                                                                     | 说明                                                    |
| --------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| **Plugin 安装** | 支持插件的平台（Claude Code、Codex CLI、Antigravity、Gemini CLI、Kimi Code、Pi、Factory Droid、Copilot CLI） | 针对单个 Agent 的原生安装；可选择需要的 skill。        |
| **Skills 安装** | `skills.sh` 支持的任意 Agent（通用 `.agents/skills` 及 17+ 个 Agent，包括 Cursor、OpenCode、Kimi Code CLI 等） | 一行命令安装，然后选择要部署到哪些 Agent。            |
| **手动安装**    | 不被 plugin 或 `skills.sh` 覆盖的极少数平台                                                                  | 手动复制或软链 skill 目录。                             |

> **建议：**
> - 如果你跨多个 Agent 使用，优先用 **Skills 安装**——安装一次即可选择分发到哪些 Agent。
> - 如果你只在一个 Agent 中使用且想要原生 plugin 体验，用 **Plugin 安装**。
> - 两者都不支持时，才使用 **手动安装**。

## Plugin 安装

Plugin 针对特定 Agent 提供原生安装。它可以安装整个 bundle，然后只启用你需要的 skill。如果同时使用多个 Agent 平台，请分别在每个平台中安装。

### Claude Code

```bash
/plugin marketplace add bird-chinese-community/BIRD.skills
/plugin install bird-agent@bird-skills
/plugin install birdcc-installer@bird-skills
/plugin install birdcc-cicd@bird-skills
```

### Antigravity

```bash
agy plugin install https://github.com/bird-chinese-community/BIRD.skills
```

Antigravity 会在会话启动时运行插件钩子，因此 skills 从第一条消息起即可用。使用相同命令重新安装即可更新。

### Codex App

Codex App 与 Codex CLI 共享插件配置。先通过 CLI 侧载，App 中即可使用这些 skills：

```bash
codex plugin marketplace add bird-chinese-community/BIRD.skills
# 然后在 Codex 内使用 /plugins 安装单个 skill
```

### Codex CLI

```bash
codex plugin marketplace add bird-chinese-community/BIRD.skills
# 然后在 Codex 内使用 /plugins 安装单个 skill
```

### Factory Droid

注册插件市场：

```bash
droid plugin marketplace add https://github.com/bird-chinese-community/BIRD.skills
```

安装 skills：

```bash
droid plugin install bird-agent@BIRD.skills
droid plugin install birdcc-installer@BIRD.skills
droid plugin install birdcc-cicd@BIRD.skills
```

### Gemini CLI

安装扩展：

```bash
gemini extensions install https://github.com/bird-chinese-community/BIRD.skills
```

后续更新：

```bash
gemini extensions update BIRD.skills
```

### GitHub Copilot CLI

注册插件市场：

```bash
copilot plugin marketplace add bird-chinese-community/BIRD.skills
```

安装 skills：

```bash
copilot plugin install bird-agent@bird-chinese-community/BIRD.skills
copilot plugin install birdcc-installer@bird-chinese-community/BIRD.skills
copilot plugin install birdcc-cicd@bird-chinese-community/BIRD.skills
```

### Kimi Code

在 Kimi Code 中使用 `/plugins` 打开插件管理器，然后直接从本仓库安装：

```bash
/plugins install https://github.com/bird-chinese-community/BIRD.skills
```

### Pi

```bash
pi install git:github.com/bird-chinese-community/BIRD.skills
```

本地开发时，可以将本仓库作为临时包加载运行 Pi：

```bash
pi -e /path/to/BIRD.skills
```

### Skills 安装

如果你的平台不支持 plugin，可以使用 `skills.sh` 作为快速降级方案。该命令会一次性安装全部三个 skills：

```bash
npx skills@latest add bird-chinese-community/BIRD.skills
```

你仍然可以在 Agent 设置中单独禁用不需要的 skill。

### 手动安装

如果 plugin 和 `skills.sh` 都不适用（例如 Cursor 或 OpenCode），请克隆本仓库，然后将需要的 skill 目录复制或软链到 Agent 的 skills 目录（例如 `~/.claude/skills/`、`~/.codex/skills/`、`.agents/skills/`）。

---

> Tips: 后续更新时，重新运行对应平台的安装命令即可。手动安装则 `git pull` 后重新复制或软链 skill 目录。
