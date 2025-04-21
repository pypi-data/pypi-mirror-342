"""
Example script for creating a simple box using the Claude CAD MCP plugin.

This example demonstrates how to call the MCP plugin tools directly to create a model.
Uses the mock server implementation to avoid dependency issues.
"""

import json
import asyncio
from pathlib import Path
import sys
import os

# Add the parent directory to the Python path to import the claude_cad package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the mock server instead of the real server
from src.claude_cad.mock_server import ClaudeCADServer, MockRequest
from src.claude_cad.model_generator import create_primitive


async def main():
    """Run the example to create a simple box."""
    # Initialize the CAD MCP server
    server = ClaudeCADServer()
    
    # Create parameters for a simple box
    parameters = {
        "shape_type": "box",
        "parameters": {
            "length": 20.0,
            "width": 15.0,
            "height": 10.0
        },
        "name": "Simple Box",
        "description": "A simple box created using the Claude CAD MCP plugin"
    }
    
    # Call the tool to create the model
    response = await server._handle_create_primitive(parameters)
    
    # Print the response
    print("Response from MCP server:")
    print(json.dumps(response, indent=2))
    
    # Clean up server resources
    await server.cleanup()
    
    # Access the created model directly
    model = create_primitive("box", {
        "length": 20.0,
        "width": 15.0,
        "height": 10.0
    })
    
    # Export the model to a STEP file in the current directory
    output_path = Path.cwd() / "simple_box.step"
    model.export(str(output_path))
    
    print(f"\nModel exported to: {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
