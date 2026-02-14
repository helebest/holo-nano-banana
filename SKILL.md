---
name: holo-nano-banana
description: Generate or edit images using Nano Banana Pro (Gemini 3 Pro) via OpenRouter.
homepage: https://github.com/helebest/holo-nano-banana
---

# Holo Nano Banana

Generate images using Google's Nano Banana Pro (Gemini 3 Pro Image) API via OpenRouter.

## Prerequisites

1. OpenRouter API Key (in `OPENROUTER_API_KEY` env)
2. Python dependencies (`requests`, `pillow`) installed in OpenClaw global venv

## Usage

### Generate Image

```bash
bash {baseDir}/scripts/banana.sh --prompt "A futuristic city" --output "$HOME/data/images/2026/city.png"
```

### Edit/Transform Image

```bash
bash {baseDir}/scripts/banana.sh --prompt "Turn it into a painting" --input-image "/path/to/source.jpg" --output "/path/to/result.png"
```

## Delivering the Image (Feishu only)

When the current conversation is on **Feishu**, the `MEDIA:` marker does NOT auto-deliver images.
After generating the image, you MUST send it manually:

```bash
openclaw message send --channel feishu --target <target> --media "<output_path>" --message "<description>"
```

- `<target>`: the current Feishu chat ID (e.g. `oc_xxx`)
- `<description>`: a brief description of the generated image
- For other channels (Telegram, etc.), `MEDIA:` works normally — no extra step needed.

## Configuration

The skill relies on `OPENROUTER_API_KEY` environment variable being set in the agent's context.
