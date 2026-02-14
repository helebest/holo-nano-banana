import argparse
import os
import sys
import json
import base64
import requests
from io import BytesIO
from PIL import Image

def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("OPENROUTER_API_KEY")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def main():
    parser = argparse.ArgumentParser(
        description="Generate/Edit images using Nano Banana Pro via OpenRouter"
    )
    parser.add_argument("--prompt", "-p", required=True, help="Image description/prompt")
    parser.add_argument("--output", "-o", required=True, help="Output filename")
    parser.add_argument("--input-image", "-i", help="Input image for editing (optional)")
    parser.add_argument("--api-key", "-k", help="OpenRouter API Key")
    parser.add_argument("--model", default="google/gemini-3-pro-image-preview", help="Model ID")
    
    args = parser.parse_args()
    
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found.", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.ai",
        "X-Title": "OpenClaw Holo Nano Banana",
    }

    # Build messages
    messages = []
    
    if args.input_image:
        if not os.path.exists(args.input_image):
            print(f"Error: Input image {args.input_image} not found.", file=sys.stderr)
            sys.exit(1)
            
        base64_image = encode_image(args.input_image)
        # OpenAI Vision format
        content = [
            {"type": "text", "text": args.prompt},
            {
                "type": "image_url", 
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
        messages.append({"role": "user", "content": content})
        print(f"Mode: Editing/Transformation (Input: {args.input_image})")
    else:
        messages.append({"role": "user", "content": args.prompt})
        print(f"Mode: Text-to-Image Generation")

    payload = {
        "model": args.model,
        "messages": messages,
        # Hints for OpenRouter/Gemini
        "temperature": 1.0, 
    }

    print(f"Sending request to OpenRouter ({args.model})...")
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"API Error ({response.status_code}):", file=sys.stderr)
            print(response.text, file=sys.stderr)
            sys.exit(1)
            
        result = response.json()
        
        # Parse response for images
        # OpenRouter/Gemini usually returns images in choices[0].message.images (custom field)
        # or sometimes as markdown links in content.
        
        images_data = []
        
        # Check custom images field (OpenRouter specific for some models)
        try:
            if 'choices' in result and len(result['choices']) > 0:
                message = result['choices'][0].get('message', {})
                if 'images' in message and message['images']:
                     for img_item in message['images']:
                        if isinstance(img_item, dict) and 'image_url' in img_item:
                             url = img_item['image_url'].get('url', '')
                             if url.startswith('data:image'):
                                 images_data.append(url)
        except Exception:
            pass

        # Fallback: Parse markdown from content if no custom field
        if not images_data and 'choices' in result:
             content_text = result['choices'][0]['message'].get('content', '')
             if content_text and "data:image" in content_text:
                 # Simple extraction logic for markdown images
                 import re
                 # Look for data URIs in parens or quotes
                 urls = re.findall(r'(data:image/[^;]+;base64,[^"\)\s]+)', content_text)
                 if urls:
                     images_data.extend(urls)

        if not images_data:
            print("No images found in response.", file=sys.stderr)
            print("Full response:", json.dumps(result, indent=2), file=sys.stderr)
            sys.exit(1)

        print(f"Received {len(images_data)} image(s).")
        
        # Save first image to output path
        # Handle data URI
        header, b64_str = images_data[0].split(',', 1)
        img_bytes = base64.b64decode(b64_str)
        
        # Save
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        with open(args.output, "wb") as f:
            f.write(img_bytes)
            
        print(f"Image saved to: {args.output}")
        print(f"MEDIA: {args.output}")
        
    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
