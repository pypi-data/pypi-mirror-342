"""
Example script for creating a 3D model from a text description using the Claude CAD MCP plugin.

This example demonstrates how to use the text-to-model feature to generate models from natural language.
"""

import json
import asyncio
from pathlib import Path
import sys
import os

# Add the parent directory to the Python path to import the claude_cad package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.claude_cad.mock_server import ClaudeCADServer, MockRequest


async def main():
    # Initialize the CAD MCP server
    server = ClaudeCADServer()
    
    # Example descriptions to test
    descriptions = [
        "Create a gear with 20 teeth and a 50mm diameter",
        "Make a simple box that is 30mm long, 20mm wide, and 15mm high with rounded corners",
        "Create a cylinder with a 25mm diameter and 40mm height with a 10mm hole through the center"
    ]
    
    # Process each description
    for description in descriptions:
        print(f"\n\n--- Processing description: '{description}' ---")
        
        # Create a request parameter for the text-to-model tool
        tool_request = {
            "params": {
                "name": "create_model_from_text",
                "arguments": {
                    "description": description,
                    "name": "Text Generated Model",
                    "format": "step"
                }
            }
        }
        
        # Call the tool to create the model
        response = await server._handle_create_model_from_text(tool_request["params"]["arguments"])
        
        # Print the response (truncating the code part for clarity)
        content = response["content"][0]["text"]
        code_start = content.find("```python")
        if code_start > 0:
            short_content = content[:code_start + 100] + "...\n```"
            print("\nResponse from MCP server (truncated):")
            print(short_content)
        else:
            print("\nResponse from MCP server:")
            print(content)
    
    # Clean up server resources
    await server.cleanup()
    
    print("\nText-to-model examples completed.")


if __name__ == "__main__":
    asyncio.run(main())
