"""
Utility functions for Claude CAD.

This module contains helper functions used throughout the Claude CAD package.
"""

import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Union
from urllib.parse import urlparse


def parse_resource_uri(uri: str) -> Any:
    """Parse a resource URI into its components.
    
    Args:
        uri: The resource URI to parse (e.g., 'model://123456').
        
    Returns:
        A parsed URL object.
    """
    return urlparse(uri)


def get_temp_file_path(suffix: str = '') -> Path:
    """Create a temporary file path with the given suffix.
    
    Args:
        suffix: File extension with dot (e.g., '.step').
        
    Returns:
        Path object representing a temporary file path.
    """
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    return Path(path)


def ensure_directory_exists(directory_path: Union[str, Path]) -> Path:
    """Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory_path: Path to the directory to create.
        
    Returns:
        Path object representing the directory.
    """
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def supported_export_formats() -> Dict[str, Dict[str, Any]]:
    """Get a dictionary of supported export formats.
    
    Returns:
        A dictionary mapping format names to their properties.
    """
    return {
        "step": {
            "extension": ".step",
            "mime_type": "model/step",
            "description": "STEP File Format (ISO 10303)",
        },
        "stl": {
            "extension": ".stl",
            "mime_type": "model/stl",
            "description": "STL File Format (Standard Triangle Language)",
        },
        "dxf": {
            "extension": ".dxf",
            "mime_type": "application/dxf",
            "description": "DXF File Format (Drawing Exchange Format)",
        },
        "svg": {
            "extension": ".svg",
            "mime_type": "image/svg+xml",
            "description": "SVG File Format (Scalable Vector Graphics)",
        },
        "gltf": {
            "extension": ".gltf",
            "mime_type": "model/gltf+json",
            "description": "glTF File Format (GL Transmission Format)",
        },
    }
