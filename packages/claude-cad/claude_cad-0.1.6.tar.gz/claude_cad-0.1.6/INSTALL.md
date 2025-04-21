# Claude CAD Installation Guide

This guide will help you install and set up Claude CAD, an MCP plugin for creating 3D models with Claude AI using CadQuery.

## Prerequisites

Before installing Claude CAD, you need to have the following prerequisites:

1. **Python 3.9 or higher**
   - Download and install from [python.org](https://www.python.org/downloads/)
   - Make sure Python is added to your PATH

2. **CadQuery**
   - CadQuery is a powerful parametric modeling system for Python
   - It's recommended to install CadQuery via conda for best compatibility

3. **Claude Desktop Application**
   - This plugin works with the Claude desktop application
   - The application must support the Model Context Protocol (MCP)

4. **uv**
   - A modern Python package installer and resolver
   - Install with: `pip install uv`
   - Learn more: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

## Installation Options

### Option 1: Install from PyPI (Recommended)

```bash
# Create a virtual environment using uv
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Claude CAD using uv
uv pip install claude-cad
```

### Option 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/bronson/claude_cad.git
cd claude_cad

# Create a virtual environment using uv
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies using uv
uv pip install -r requirements.txt

# Install in development mode
uv pip install -e .
```

## Configure Claude Desktop

To use Claude CAD with Claude Desktop, you need to update your Claude configuration file:

1. Locate your Claude Desktop configuration file
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. Choose one of these configuration options:

   ### Option 1: Using Python directly

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

   ### Option 2: Using uvx (Recommended)

   For improved dependency management and reliability, use `uvx` (part of the uv toolkit):

   ```json
   {
     "mcpServers": {
       "claude_cad": {
         "command": "uvx", 
         "args": ["-m", "claude_cad.server"],
         "env": {}
       }
     }
   }
   ```

3. Restart Claude Desktop to apply the changes

## Verify Installation

To verify that Claude CAD is installed correctly:

1. Run one of the example scripts:

```bash
python examples/simple_box.py
```

2. This should create a simple box model and export it as a STEP file.

3. Open Claude Desktop and try using it with a prompt like:
   "Create a 3D model of a gear with 10 teeth"

## Troubleshooting

If you encounter issues:

1. Check that Python and CadQuery are installed correctly
2. Verify that the Claude configuration file has been updated
3. Look for error messages in the Claude Desktop logs
4. Try running the example scripts to isolate the issue

## Need Help?

If you need assistance, please:
- Check the documentation
- Open an issue on the GitHub repository
- Contact the project maintainers
