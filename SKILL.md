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
bash {baseDir}/scripts/banana.sh --prompt "A futuristic city" --output "/mnt/usb/data/images/2026/city.png"
```

### Edit/Transform Image (Experimental)

```bash
bash {baseDir}/scripts/banana.sh --prompt "Turn it into a painting" --input-image "/path/to/source.jpg" --output "/path/to/result.png"
```

## Configuration

The skill relies on `OPENROUTER_API_KEY` environment variable being set in the agent's context.
