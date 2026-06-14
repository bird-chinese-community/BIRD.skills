# BIRD Agent Skills

本仓库托管用于 BIRD（BIRD1/2/3）路由配置、编辑器设置以及 CI/CD 工作流的 Agent Skills。

## Skills

- [`bird-agent`](./bird-agent) — 编写、验证、格式化并调试 BIRD（BIRD1/2/3）路由守护进程配置文件。
- [`birdcc-installer`](./birdcc-installer) — 安装 BIRD 编辑器支持与 `birdcc` 命令行工具集。
- [`birdcc-cicd`](./birdcc-cicd) — 将 `setup-birdcc` GitHub Action 添加到 CI/CD 工作流中。

## 使用方式

这些 skills 遵循 [Agent Skills](https://agentskills.io/) 约定。每个 skill 包含：

- `SKILL.md` — Skill 清单与使用说明
- `agents/openai.yaml` — OpenAI agent 调用元数据
- `scripts/` — 仅使用 Python 标准库、可通过 `uv run` 运行的辅助脚本
- `references/` — 聚焦的参考指南

## 许可

与 BIRD-LSP 项目采用相同的许可证（GNU GPL v3）。
