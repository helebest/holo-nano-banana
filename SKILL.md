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

## Workflow: How to Generate an Image (Agent Protocol)
Instead of asking the user to provide a long, detailed prompt, you (the agent) act as the prompt engineer. Follow this workflow:

1. **Understand Intent**: What does the user want to draw?
2. **Select Style**: Choose from the built-in Style Library (see below). If unsure, ask or pick the most appropriate one.
3. **Progressive Load**: Use the `read` tool to load the specific style file (e.g. `read {baseDir}/prompts/styles/tech.md`) AND the `read {baseDir}/prompts/system.md`.
4. **Assemble Prompt**: Combine the User's core subject + System constraints + Style keywords into a single, cohesive, rich English prompt.
5. **Execute**: Run `banana.sh` with the assembled prompt.

## Style Library Index
Do not read all of these. Read ONLY the one you need for the current task:
- `tech` - IT, Hacker, corporate, futuristic (`prompts/styles/tech.md`)
- `watercolor` - Fresh, elegant, traditional, nature (`prompts/styles/watercolor.md`)
- `minimal` - UI/UX, vector, flat, clean (`prompts/styles/minimal.md`)
- `anime` - Japanese animation, cinematic, vibrant (`prompts/styles/anime.md`)

## Usage

### Generate Image (After Assembling Prompt)


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
