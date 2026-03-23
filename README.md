# Holo Nano Banana 🍌

Generate or edit images using Nano Banana Pro (Gemini 3 Pro) via OpenRouter, optimized for OpenClaw agents.

## 🚀 描述

这是一个 OpenClaw Skill，用于通过 OpenRouter API 调用 Google 的 Nano Banana Pro (Gemini 3 Pro Image) 模型。支持文生图（Text-to-Image）和图生图（Image-to-Image / Editing）。

**近期重大更新：** 引入了系统级防抖约束与渐进式加载（Progressive Loading）的风格库。它不再仅仅是一个命令执行器，更是一个自带审美与最佳实践的自动化配图助理。

遵循 **OpenClaw 最佳实践**：
- 使用 `uv` 进行依赖管理，部署时将依赖安装到 OpenClaw 全局环境。
- 使用 **Progressive Loading**：在 `SKILL.md` 内置索引，外置细粒度 Prompt，极大地节省 Agent 上下文，同时保证神级长咒语被精准利用。

## 🧠 改进的 Agent 工作流

1. **System Prompt 防呆**：内置 `prompts/system.md` 约束（杜绝写实人脸恐怖谷、防文字崩坏、统一构图高留白）。
2. **渐进式加载风格库 (Style Library)**：内置了预调好的画风（科技、极简、水彩插画、二次元等）。Agent 会根据需要 `read` 具体的提示词特征然后进行拼接拼装，无需人类提供冗长细碎的光影提示词。

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
./openclaw_deploy_skill.sh ~/.agents/skills/holo-nano-banana
```

### 部署后的结构

```
holo-nano-banana/
├── SKILL.md
├── prompts/                     # ◀️ 新增体系
│   ├── system.md                # 统一图形生成最高优先级约束
│   └── styles/                  # 局部加载风格库
│       ├── anime.md
│       ├── minimal.md
│       ├── tech.md
│       └── watercolor.md
└── scripts/
    ├── banana.sh                # Agent 调用的入口
    └── generate.py              # 核心逻辑
```

## 🤖 使用方法 (Agent)

当接到画图任务，Agent 将：

1. **理解与匹配**：选择对应的风格。
2. **加载语料**：读取 `prompts/system.md` 与选定的 `prompts/styles/*.md`。
3. **融合拼接**：将人类的核心需求（如：算力中心）和长串光影提示词完美融合。
4. **触发生成**：

```bash
# 执行融合后的 Prompt 生成图片
bash {baseDir}/scripts/banana.sh --prompt "Assembled long prompt here..." --output "/path/to/save.png"
```

## ⚙️ 配置

需要确保 OpenClaw 的运行环境中包含以下环境变量：

- `OPENROUTER_API_KEY`: 你的 OpenRouter API Key
