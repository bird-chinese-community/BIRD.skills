# BIRD Agent Skills

本仓库托管用于 BIRD（BIRD1/2/3）路由配置、编辑器设置以及 CI/CD 工作流的 Agent Skills。

## Skills

- [`bird-agent`](./bird-agent) — 编写、验证、格式化并调试 BIRD（BIRD1/2/3）路由守护进程配置文件。
- [`birdcc-installer`](./birdcc-installer) — 安装 BIRD 编辑器支持与 `birdcc` 命令行工具集。
- [`birdcc-cicd`](./birdcc-cicd) — 将 `setup-birdcc` GitHub Action 添加到 CI/CD 工作流中。

## 使用方式

这些 skills 遵循 [Agent Skills](https://agentskills.io/) 约定。大部分 skill 包含：

- `SKILL.md` — Skill 清单与使用说明
- `agents/openai.yaml` — OpenAI agent 调用元数据
- `scripts/` — 仅使用 Python 标准库、可通过 `uv run` 运行的辅助脚本
- `references/` — 聚焦的参考指南

`birdcc-cicd` 没有 `scripts/` 目录，只提供 `SKILL.md`、`agents/openai.yaml`
和 `references/`。

## 安装

### Claude Code

先添加 marketplace，再安装需要的 skill：

```bash
/plugin marketplace add bird-chinese-community/BIRD.skills
/plugin install bird-agent@bird-skills
/plugin install birdcc-installer@bird-skills
/plugin install birdcc-cicd@bird-skills
```

### OpenAI Codex CLI

```bash
codex plugin marketplace add bird-chinese-community/BIRD.skills
# 在 Codex 内使用 /plugins 安装 bird-agent、birdcc-installer 或 birdcc-cicd
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

克隆仓库后，将需要的 skill 目录复制或软链到 agent 的 skills 目录（例如
`~/.claude/skills/`、`~/.codex/skills/` 或 `.agents/skills/`）。

## 许可

[MIT](./LICENSE)
