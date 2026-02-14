# Holo Nano Banana 🍌

Generate or edit images using Nano Banana Pro (Gemini 3 Pro) via OpenRouter, optimized for OpenClaw agents.

## 🚀 描述

这是一个 OpenClaw Skill，用于通过 OpenRouter API 调用 Google 的 Nano Banana Pro (Gemini 3 Pro Image) 模型。支持文生图（Text-to-Image）和图生图（Image-to-Image / Editing）。

它遵循 **OpenClaw 最佳实践**：
- 使用 `uv` 进行依赖管理。
- 部署时将依赖安装到 OpenClaw 的全局 `.venv` 环境。
- 运行时直接调用全局环境的 Python 解释器。

## 🛠️ 开发

### 依赖安装

项目使用 `uv` 管理依赖。在开发目录下：

```bash
# 安装依赖到本地 .venv (用于开发调试)
uv sync
```

### 本地运行测试

```bash
# 需要设置 OPENROUTER_API_KEY
export OPENROUTER_API_KEY="sk-or-..."

# 生成图片
uv run scripts/generate.py --prompt "A cool banana wearing sunglasses" --output "test.png"
```

## 📦 部署

使用提供的部署脚本将 Skill 安装到 OpenClaw 的 Skills 目录。

```bash
# 部署 (会自动安装依赖到全局 ~/.openclaw/.venv)
./openclaw_deploy_skill.sh <skills-directory>

# 示例
./openclaw_deploy_skill.sh /mnt/usb/holobot/.openclaw/skills/holo-nano-banana
```

### 部署后的结构

```
holo-nano-banana/
├── SKILL.md
└── scripts/
    ├── banana.sh    # Agent 调用的入口
    └── generate.py  # 核心逻辑
```

*注意：`pyproject.toml` 不会被部署，但在部署过程中会被读取以安装依赖。*

## 🤖 使用方法 (Agent)

Agent 可以通过 `exec` 工具调用 `banana.sh`：

```bash
# 生成图片
bash {baseDir}/scripts/banana.sh --prompt "prompt here" --output "/path/to/save.png"

# 编辑/变换图片
bash {baseDir}/scripts/banana.sh --prompt "make it cyberpunk style" --input-image "source.jpg" --output "result.png"
```

## ⚙️ 配置

需要确保 OpenClaw 的运行环境中包含以下环境变量：

- `OPENROUTER_API_KEY`: 你的 OpenRouter API Key

## 🏗️ 架构说明

为了节省空间和避免重复安装，本 Skill **不维护独立的 venv**。
- `openclaw_deploy_skill.sh` 读取 `pyproject.toml` 中的依赖列表。
- 使用 `uv pip install` 将这些依赖 (`requests`, `pillow`) 安装到 `~/.openclaw/.venv` (全局环境)。
- `scripts/banana.sh` 硬编码指向 `~/.openclaw/.venv/bin/python3` 来执行 Python 脚本。
