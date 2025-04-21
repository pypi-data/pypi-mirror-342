# FAL AI Image Generator MCP

A Model Context Protocol (MCP) server for generating images using the FAL.ai platform and HiDream-ai/HiDream-I1-Full model.

## Quick Start

1. **Get a FAL.ai API Key**
   - Sign up at [FAL.ai](https://www.fal.ai) and obtain your API key

2. **Install the package**
```bash
# Using pip
pip install fal-ai-mcp

# Using uv
uv pip install fal-ai-mcp
```

3. **Run the server**
   ```bash
   export FAL_KEY="your-fal-api-key"
   fal-ai-mcp
   ```

4. **Test with MCP Inspector**
   ```bash
   npx @modelcontextprotocol/inspector -- python -m fal_ai_mcp
   ```

## Configure in Claude Desktop, Cursor or Windsurf

Add this configuration to your MCP config file:

```json
{
  "mcpServers": {
    "fal-ai-image-generator": {
      "command": "python",
      "args": ["-m", "fal_ai_mcp"],
      "env": {
        "FAL_KEY": "your-fal-api-key"
      }
    }
  }
}
```

## Features

This MCP server provides a tool for generating high-quality images from text prompts using FAL.ai platform:

- Text-to-image generation using the `text_to_image_fal` tool
- Returns complete metadata including image URL or base64 image data, dimensions, and other information
- Easy integration with MCP-compatible applications

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

## Installation Options

### Global Installation

To install the package globally or in your current environment:

```bash
# Using pip (recommended)
pip install fal-ai-mcp

# Using uv
uv pip install fal-ai-mcp
```

If you encounter any issues with the installation, try using the `--force-reinstall` flag:

```bash
pip install fal-ai-mcp --force-reinstall
```

### Installing from Source

```bash
# Using pip
pip install git+https://github.com/OKitchen/fal-ai-mcp.git

# Using uv
uv pip install git+https://github.com/OKitchen/fal-ai-mcp.git
```

### Adding as a Project Dependency

To add the package as a dependency to your Python project (requires a `pyproject.toml` file):

```bash
# Navigate to your project directory that has a pyproject.toml
cd your-project-directory

# Add as a dependency using uv
uv add fal-ai-mcp
```

Note: The `uv add` command will only work in a Python project that has a `pyproject.toml` file and is not named `fal-ai-mcp` (to avoid circular dependencies).

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
uv pip install -e .

# Run the server locally with your FAL.ai API key
export FAL_KEY="your-fal-api-key" && uv run -m fal_ai_mcp