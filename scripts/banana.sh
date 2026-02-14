#!/bin/bash
#
# Holo Nano Banana - Image Generation
# Usage: bash banana.sh --prompt "description" --output "path/to/image.png"
#

# Standard OpenClaw Venv Path
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
VENV_PYTHON="$OPENCLAW_HOME/.venv/bin/python3"

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Error: OpenClaw runtime environment not found at $VENV_PYTHON"
    echo "Please ensure the base environment is set up correctly."
    exit 1
fi

# Get script dir
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Execute python script using key from environment (OPENROUTER_API_KEY)
# Pass all arguments to the python script
"$VENV_PYTHON" "$SCRIPT_DIR/generate.py" "$@"
