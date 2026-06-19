# 安装 BIRD.skills

共有三种安装方式，请根据你使用的 Agent 平台选择：

| 安装方式        | 适用平台                                                                                          | 说明                                                    |
| --------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| **Plugin 安装** | 支持插件的平台（Claude Code、Codex CLI、Antigravity、Gemini CLI、Pi、Factory Droid、Copilot CLI） | 推荐首选；可安装整个 bundle，也可以只启用需要的 skill。 |
| **Skills 安装** | 任何支持 `skills.sh` 的平台                                                                       | 一行命令快速安装全部 skills。                           |
| **手动安装**    | 不支持插件或 skills 的平台（Cursor、Kimi Code、OpenCode 等）                                      | 手动复制或软链 skill 目录。                             |

> **建议：** 优先尝试 **Plugin 安装**，控制权最大；如果你的平台不支持插件，退回到 **Skills 安装**；两者都不行时再使用 **手动安装**。

### Plugin 安装

Plugin 是首选安装方式。它可以安装整个 bundle，然后只启用你需要的 skill。如果同时使用多个 Agent 平台，请分别在每个平台中安装。

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

Antigravity 会在会话启动时运行插件钩子，因此 skills 从第一条消息起即可用。使用相同命令重新安装即可更新。

#### Codex App

Codex App 与 Codex CLI 共享插件配置。先通过 CLI 侧载，App 中即可使用这些 skills：

```bash
codex plugin marketplace add bird-chinese-community/BIRD.skills
# 然后在 Codex 内使用 /plugins 安装单个 skill
```

#### Codex CLI

```bash
codex plugin marketplace add bird-chinese-community/BIRD.skills
# 然后在 Codex 内使用 /plugins 安装单个 skill
```

#### Factory Droid

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

#### Gemini CLI

安装扩展：

```bash
gemini extensions install https://github.com/bird-chinese-community/BIRD.skills
```

后续更新：

```bash
gemini extensions update BIRD.skills
```

#### GitHub Copilot CLI

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

#### Pi

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
npx skills add bird-chinese-community/BIRD.skills
```

你仍然可以在 Agent 设置中单独禁用不需要的 skill。

### 手动安装

如果 plugin 和 `skills.sh` 都不适用（例如 Cursor、Kimi Code 或 OpenCode），请克隆本仓库，然后将需要的 skill 目录复制或软链到 Agent 的 skills 目录（例如 `~/.claude/skills/`、`~/.codex/skills/`、`.agents/skills/`）。

---

> 后续更新时，重新运行对应平台的安装命令即可。手动安装则 `git pull` 后重新复制或软链 skill 目录。
