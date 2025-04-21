# Claude CAD

A Model Context Protocol (MCP) plugin for creating 3D models with Claude AI using CadQuery.

## Overview

Claude CAD is an MCP plugin that allows Claude AI to create 3D models based on text prompts. It leverages the powerful parametric modeling capabilities of CadQuery, a Python-based CAD scripting library, to generate complex 3D models that can be exported in various formats (STEP, STL, etc.).

## Features

- Generate 3D models from natural language descriptions
- Parametric modeling using CadQuery's Python API
- Support for primitives, boolean operations, extrusions, and more
- Export models in various formats (STEP, STL, etc.)
- Full integration with Claude AI via MCP

## Installation

### Prerequisites

- Python 3.9+
- CadQuery
- Model Context Protocol SDK
- uv (Modern Python package installer)

### Install using uv

```bash
# Install uv if not already installed
pip install uv

# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install from PyPI
uv pip install claude-cad

# Or install from source
git clone https://github.com/bronson/claude_cad.git
cd claude_cad
uv pip install -e .
```

For detailed installation instructions, see [INSTALL.md](INSTALL.md).

## Configuration

To use Claude CAD with Claude, you need to update your Claude configuration file:

```json
{
  "mcpServers": {
    "claude_cad": {
      "command": "python",
      "args": ["-m", "claude_cad.server"],
      "env": {}
    }
  }
}
```

## Usage

Once installed and configured, you can ask Claude to create 3D models using natural language:

```
Please create a 3D model of a small gear with 10 teeth and a 20mm diameter.
```

Claude will use the Claude CAD MCP plugin to generate the model and provide a download link or preview.

## Examples

See the `examples` directory for sample models and prompts:

- `simple_box.py`: Creates a basic box primitive
- `lego_brick.py`: Creates a LEGO-compatible brick
- `text_to_model.py`: Demonstrates text-to-3D-model generation

## Development

To set up a development environment:

```bash
# Clone the repository
git clone https://github.com/bronson/claude_cad.git
cd claude_cad

# Create a virtual environment
uv venv

# Install dependencies
uv pip install -r requirements.txt

# Install in development mode
uv pip install -e .

# Run tests
python -m unittest discover tests
```

## License

Apache 2.0

## Credits

- CadQuery: https://github.com/CadQuery/cadquery
- Model Context Protocol: Anthropic's Claude integration API
- uv: https://github.com/astral-sh/uv
