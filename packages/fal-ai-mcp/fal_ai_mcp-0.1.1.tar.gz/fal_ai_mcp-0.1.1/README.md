# FAL AI Image Generator MCP

A Model Context Protocol (MCP) server for generating images using the FAL.ai platform and HiDream-ai/HiDream-I1-Full model.

## Installation

```bash
# Using pip (recommended)
pip install fal-ai-mcp

# Using uv
uv pip install fal-ai-mcp
```

Or install directly from the source:

```bash
# Using pip
pip install git+https://github.com/OKitchen/fal-ai-mcp.git

# Using uv
uv pip install git+https://github.com/OKitchen/fal-ai-mcp.git
```

## Usage

### Run as a standalone server

First, set your FAL.ai API key as an environment variable:

```bash
export FAL_KEY="your-fal-api-key"
# or
export FAL_API_KEY="your-fal-api-key"
```

Then run the server:

```bash
# If installed via pip
python -m fal_ai_mcp

# Or using the installed entry point
fal-ai-mcp
```

### Use with MCP Inspector

```bash
# Using Python module
export FAL_KEY="your-fal-api-key" && npx @modelcontextprotocol/inspector -- python -m fal_ai_mcp

# Using uvx (alternative method)
export FAL_KEY="your-fal-api-key" && npx @modelcontextprotocol/inspector uvx fal-ai-mcp
```

### Configure in Claude Desktop, Cursor or Windsurf

Add one of these configurations to your MCP config file:

#### Method 1: Using uvx (Recommended for Cursor)

This method works well in Cursor and other environments:

```json
{
  "mcpServers": {
    "fal-ai-image-generator": {
      "command": "uvx",
      "args": [
        "fal-ai-mcp"
      ],
      "env": {
        "FAL_KEY": "your-fal-api-key"
      }
    }
  }
}
```

#### Method 2: Using Python module

Standard approach using the Python module directly:

```json
{
  "mcpServers": {
    "fal-ai-image-generator": {
      "command": "python",
      "args": [
        "-m",
        "fal_ai_mcp"
      ],
      "env": {
        "FAL_KEY": "your-fal-api-key"
      }
    }
  }
}
```

## Features

This MCP server provides a single tool for generating high-quality images from text prompts using FAL.ai platform and HiDream-ai/HiDream-I1-Full model:

- Text-to-image generation using the `text_to_image_fal` tool
- Returns complete metadata including image URL or base64 image data, dimensions, and other information
- Easy integration with MCP-compatible applications

### Example Tool Usage

```python
result = text_to_image_fal(prompt="A professional tech illustration showing MCP architecture connecting multiple AI services")
image_url = result["images"][0]["url"]
```

## API Reference

### `text_to_image_fal`

Generates an image from a text prompt using the FAL.ai API and HiDream-I1-Full model.

**Parameters:**
- `prompt` (string): The text description of the image you want to generate

**Returns:**
- A dictionary containing the generated image data, including:
  - `images`: Array of generated images with URLs, dimensions, and content type
  - `timings`: Performance metrics
  - `seed`: The random seed used for generation
  - `has_nsfw_concepts`: Safety check results
  - `prompt`: The original prompt

### Response Format Details

The response from `text_to_image_fal` is a JSON object containing:

```json
{
  "images": [
    {
      "url": "data:image/jpeg;base64,/9j/...",
      "width": 1024,
      "height": 1024,
      "content_type": "image/jpeg"
    }
  ],
  "timings": {
    "inference": 23.09505701251328
  },
  "seed": 12345,
  "has_nsfw_concepts": [
    false
  ],
  "prompt": "A beautiful mountain landscape with a lake and sunset"
}
```

The `url` field contains base64 encoded image data that can be displayed directly in browsers or decoded to save as a file.

## Troubleshooting

### Python Version Requirements

This package requires Python 3.10 or higher. If you encounter an error like:

```
ERROR: Could not find a version that satisfies the requirement fal-ai-mcp
ERROR: No matching distribution found for fal-ai-mcp
```

Make sure you're using Python 3.10 or higher:

```bash
python --version
```

### Module Not Found

If you encounter an error like:

```
No module named fal_ai_mcp
```

Make sure the package is properly installed:

```bash
pip list | grep fal-ai-mcp
```

If it's not listed, try reinstalling:

```bash
pip install --force-reinstall fal-ai-mcp
```

### FAL API Key Not Set

If you see an error about missing FAL API keys:

```
ValueError: Neither FAL_API_KEY nor FAL_KEY environment variables are set
```

Make sure to set your FAL.ai API key before running the server:

```bash
export FAL_KEY="your-fal-api-key"
```

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/OKitchen/fal-ai-mcp.git
cd fal-ai-mcp

# Set up a virtual environment
uv init
uv add -e .

# Run the server locally with your FAL.ai API key
export FAL_KEY="your-fal-api-key" && uv run -m fal_ai_mcp
```

## License

MIT

## Acknowledgements

- [FAL.ai](https://www.fal.ai) for providing the image generation API
- [Model Context Protocol (MCP)](https://modelcontextprotocol.github.io/) for the protocol specification
- The open-source community for inspiration and support