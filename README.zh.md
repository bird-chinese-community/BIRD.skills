# BIRD.skills（Agent Skills）

> 为 BIRD（BIRD1/2/3）路由守护进程提供编写、验证、格式化与 CI/CD 一站式支持的 Agent Skills。

## 按场景选择 Skill

| 使用场景                                                               | 推荐 Skill                               |
| ---------------------------------------------------------------------- | ---------------------------------------- |
| 需要编写或修复 `bird.conf`、`bird2.conf`、`bird3.conf` 或 `bird6.conf` | [`bird-agent`](./bird-agent)             |
| 需要安装编辑器支持或 `birdcc` 命令行工具                               | [`birdcc-installer`](./birdcc-installer) |
| 想在 GitHub Actions 中校验或格式化 BIRD 配置                           | [`birdcc-cicd`](./birdcc-cicd)           |

### Skill 简介

- **[`bird-agent`](./bird-agent)** — 编写、验证、格式化和调试 BIRD（BIRD1/2/3）路由守护进程配置。当用户提到 `bird.conf`、`bird2.conf`、`bird3.conf`、`bird6.conf`、`bird.config.json`、`birdcc lint/fmt`、`bird -p` 验证、BIRD filter 语法或 BGP/路由配置问题时使用。
- **[`birdcc-installer`](./birdcc-installer)** — 安装 BIRD 编辑器支持与 `birdcc` CLI。当用户询问 VSCode/VSCodium/Cursor/Windsurf/Trae/Kiro/Antigravity/Neovim/Vim/JetBrains 的 BIRD 插件，或安装 `birdcc` 命令行工具集时使用。
- **[`birdcc-cicd`](./birdcc-cicd)** — 将 `setup-birdcc` GitHub Action 添加到 CI/CD 工作流。当用户希望在 GitHub Actions 中 lint、format 或验证 BIRD 配置时使用。

## 什么是 Agent Skills？

[Agent Skills](https://agentskills.io/) 是可复用、可被 Agent 读取的能力包。每个 skill 包含 `SKILL.md` 清单、`agents/openai.yaml` 元数据、可选的仅使用 Python 标准库的 PEP 723 辅助脚本，以及聚焦的参考指南。

## 给 AI Agent 的快速上手

安装 skills 后，将 Agent 放入包含 BIRD 配置文件的工作区，并用自然语言提问：

```text
"检查并格式化这个 bird2.conf"
"为我的编辑器安装 BIRD 支持"
"给 GitHub Actions 工作流加上 BIRD 校验"
```

Agent 会自动匹配对应 Skill，按需运行 `birdcc lint` / `fmt`、通过 `bird -p` 验证，或生成 CI 配置片段。

## 安装方式

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
# 然后在 Codex 内使用 /plugins 安装单个 skill
```

### skills.sh

```bash
npx skills add bird-chinese-community/BIRD.skills
```

### agentskill.sh

```bash
npx @agentskill.sh/cli setup
# 然后在任意 agent 会话中：
/learn @bird-chinese-community/BIRD.skills
```

### 手动安装

克隆仓库后，将需要的 skill 目录复制或软链到 Agent 的 skills 目录（例如 `~/.claude/skills/`、`~/.codex/skills/`、`.agents/skills/`）。

## 安全提示

BIRD 配置通常包含敏感的 AS 号、对端 IP 等信息。请勿将生产环境机密提交到仓库，或在未脱敏的情况下公开分享配置。

## 贡献

开发约定请参阅 [`AGENTS.md`](./AGENTS.md)。新增 skill 时，请按现有结构创建文件夹，包含 `SKILL.md`、`agents/openai.yaml` 以及必要的 references/scripts。

## 开源协议

本项目以 [MIT](./LICENSE) 协议开源。
