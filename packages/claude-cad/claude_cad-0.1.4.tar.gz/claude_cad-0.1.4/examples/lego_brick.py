"""
Example script for creating a LEGO-like brick using the Claude CAD MCP plugin.

This example demonstrates how to use custom CadQuery code through the MCP plugin.
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

# CadQuery code for creating a LEGO-like brick
LEGO_CODE = '''
import cadquery as cq

# Lego Brick Parameters
lbumps = 2  # number of bumps long
wbumps = 4  # number of bumps wide
thin = True  # True for thin, False for thick

# Lego Brick Constants
pitch = 8.0
clearance = 0.1
bumpDiam = 4.8
bumpHeight = 1.8

if thin:
    height = 3.2
else:
    height = 9.6

t = (pitch - (2 * clearance) - bumpDiam) / 2.0
postDiam = pitch - t  # works out to 6.5

total_length = lbumps * pitch - 2.0 * clearance
total_width = wbumps * pitch - 2.0 * clearance

# Make the base
result = cq.Workplane("XY").box(total_length, total_width, height)

# Shell inwards not outwards
result = result.faces("<Z").shell(-1.0 * t)

# Make the bumps on the top
result = (
    result.faces(">Z")
    .workplane()
    .rarray(pitch, pitch, lbumps, wbumps, True)
    .circle(bumpDiam / 2.0)
    .extrude(bumpHeight)
)

# Add posts on the bottom. Posts are different diameter depending on geometry
# solid studs for 1 bump, tubes for multiple, none for 1x1
tmp = result.faces("<Z").workplane(invert=True)

if lbumps > 1 and wbumps > 1:
    tmp = (
        tmp.rarray(pitch, pitch, lbumps - 1, wbumps - 1, center=True)
        .circle(postDiam / 2.0)
        .circle(bumpDiam / 2.0)
        .extrude(height - t)
    )
elif lbumps > 1:
    tmp = (
        tmp.rarray(pitch, pitch, lbumps - 1, 1, center=True)
        .circle(t)
        .extrude(height - t)
    )
elif wbumps > 1:
    tmp = (
        tmp.rarray(pitch, pitch, 1, wbumps - 1, center=True)
        .circle(t)
        .extrude(height - t)
    )
else:
    tmp = result

result = tmp
'''


async def main():
    """Run the example to create a LEGO brick."""
    # Initialize the CAD MCP server
    server = ClaudeCADServer()
    
    # Create parameters for executing the LEGO brick code
    parameters = {
        "code": LEGO_CODE,
        "name": "LEGO Brick (2x4)",
        "description": "A LEGO-compatible brick with 2x4 studs",
        "format": "step"
    }
    
    # Call the tool to create the model
    print("Creating LEGO brick model...")
    response = await server._handle_execute_cadquery_script(parameters)
    
    # Print the response
    print("\nResponse from MCP server:")
    print(json.dumps(response, indent=2))
    
    # Clean up server resources
    await server.cleanup()
    
    print("\nModel creation example completed.")


if __name__ == "__main__":
    asyncio.run(main())
