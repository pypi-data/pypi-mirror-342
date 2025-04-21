#!/usr/bin/env python3
"""
Mock MCP Server for Claude CAD

This file provides a simplified version of the MCP server that doesn't rely on 
the actual MCP package. It allows for testing the core functionality without 
dealing with MCP-specific implementation details.
"""

import os
import json
import tempfile
import uuid
import shutil
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable

import cadquery as cq

from . import model_generator
from . import utils


class MockMcpError(Exception):
    """Mock implementation of McpError."""
    
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"MCP Error {code}: {message}")


class MockServer:
    """A simplified mock implementation of the MCP Server."""
    
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.handlers = {}
        self.onerror = None
    
    def setRequestHandler(self, schema: str, handler: Callable) -> None:
        """Register a request handler."""
        self.handlers[schema] = handler
    
    async def connect(self, transport: Any) -> None:
        """Mock connection to a transport."""
        print(f"Mock server {self.name} v{self.version} connected")
    
    async def close(self) -> None:
        """Mock close the server connection."""
        print(f"Mock server {self.name} closed")


class MockStdioTransport:
    """A mock implementation of the stdio transport."""
    
    def __init__(self):
        pass


class MockRequest:
    """A mock request object."""
    
    def __init__(self, params: Any):
        self.params = params


# Mock schema constants
ListResourcesRequestSchema = "resources/list"
ReadResourceRequestSchema = "resources/read"
ListToolsRequestSchema = "tools/list"
CallToolRequestSchema = "tools/call"


# Mock error codes
class MockErrorCode:
    """Mock error codes."""
    InvalidRequest = 400
    MethodNotFound = 404
    InternalError = 500
    InvalidParams = 422


class ClaudeCADServer:
    """Mock MCP Server implementation for 3D modeling with CadQuery."""
    
    def __init__(self):
        """Initialize the CAD MCP server."""
        self.server = MockServer("claude_cad", "0.1.0")
        
        # Create a temp directory for storing generated models
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Dictionary to store created models
        self.models: Dict[str, Dict[str, Any]] = {}
        
        # Set up request handlers
        self.setup_handlers()
        self.setup_error_handling()

    def setup_error_handling(self) -> None:
        """Configure error handling for the server."""
        self.server.onerror = lambda error: print(f"[MCP Error] {error}", flush=True)
        
    def setup_handlers(self) -> None:
        """Register all request handlers for the server."""
        self.setup_resource_handlers()
        self.setup_tool_handlers()
        
    def setup_resource_handlers(self) -> None:
        """Set up handlers for resource-related requests."""
        
        # Handler for listing available models as resources
        self.server.setRequestHandler(
            ListResourcesRequestSchema,
            self.handle_list_resources
        )
        
        # Handler for reading model content
        self.server.setRequestHandler(
            ReadResourceRequestSchema,
            self.handle_read_resource
        )
        
    def setup_tool_handlers(self) -> None:
        """Set up handlers for tool-related requests."""
        
        # Handler for listing available CAD tools
        self.server.setRequestHandler(
            ListToolsRequestSchema,
            self.handle_list_tools
        )
        
        # Handler for calling CAD tools
        self.server.setRequestHandler(
            CallToolRequestSchema,
            self.handle_call_tool
        )
        
    async def handle_list_resources(self, request: Any) -> Dict[str, List[Dict[str, str]]]:
        """Handle the resources/list request to provide available 3D models.
        
        Returns:
            A dictionary containing the list of available models as resources.
        """
        return {
            "resources": [
                {
                    "uri": f"model://{model_id}",
                    "name": model_info.get("name", f"Model {model_id}"),
                    "mimeType": "model/step",
                    "description": model_info.get("description", "A 3D model created with CadQuery")
                }
                for model_id, model_info in self.models.items()
            ]
        }
        
    async def handle_read_resource(self, request: Any) -> Dict[str, List[Dict[str, str]]]:
        """Handle the resources/read request to provide model data.
        
        Args:
            request: The MCP request object containing the resource URI.
            
        Returns:
            A dictionary containing the model data.
            
        Raises:
            McpError: If the requested model is not found.
        """
        url = utils.parse_resource_uri(request.params.uri)
        model_id = url.path.lstrip('/')
        
        if model_id not in self.models:
            raise MockMcpError(
                MockErrorCode.InvalidRequest,
                f"Model {model_id} not found"
            )
            
        model_info = self.models[model_id]
        
        # Return metadata about the model
        return {
            "contents": [
                {
                    "uri": request.params.uri,
                    "mimeType": "application/json",
                    "text": json.dumps(model_info, indent=2)
                }
            ]
        }
        
    async def handle_list_tools(self, request: Any) -> Dict[str, List[Dict[str, Any]]]:
        """Handle the tools/list request to provide available CAD tools.
        
        Returns:
            A dictionary containing the list of available CAD tools.
        """
        return {
            "tools": [
                {
                    "name": "create_primitive",
                    "description": "Create a primitive 3D shape",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "shape_type": {
                                "type": "string",
                                "description": "Type of primitive shape (box, sphere, cylinder, cone)",
                                "enum": ["box", "sphere", "cylinder", "cone"]
                            },
                            "parameters": {
                                "type": "object",
                                "description": "Parameters for the primitive shape"
                            },
                            "name": {
                                "type": "string",
                                "description": "Name of the model"
                            },
                            "description": {
                                "type": "string",
                                "description": "Description of the model"
                            }
                        },
                        "required": ["shape_type", "parameters"]
                    }
                },
                {
                    "name": "create_model_from_text",
                    "description": "Create a 3D model from a text description using CadQuery",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "description": {
                                "type": "string",
                                "description": "Natural language description of the 3D model to create"
                            },
                            "name": {
                                "type": "string",
                                "description": "Name of the model"
                            },
                            "format": {
                                "type": "string",
                                "description": "Export format (step, stl)",
                                "enum": ["step", "stl"],
                                "default": "step"
                            }
                        },
                        "required": ["description"]
                    }
                },
                {
                    "name": "execute_cadquery_script",
                    "description": "Execute custom CadQuery Python code to create a 3D model",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Python code using CadQuery to create a model"
                            },
                            "name": {
                                "type": "string",
                                "description": "Name of the model"
                            },
                            "description": {
                                "type": "string",
                                "description": "Description of the model"
                            },
                            "format": {
                                "type": "string",
                                "description": "Export format (step, stl)",
                                "enum": ["step", "stl"],
                                "default": "step"
                            }
                        },
                        "required": ["code"]
                    }
                }
            ]
        }
        
    async def handle_call_tool(self, request: Any) -> Dict[str, List[Dict[str, str]]]:
        """Handle the tools/call request to execute a CAD tool.
        
        Args:
            request: The MCP request object containing the tool name and arguments.
            
        Returns:
            A dictionary containing the result of the tool execution.
            
        Raises:
            McpError: If the requested tool is not found or if there's an error executing it.
        """
        tool_name = request.params.name
        args = request.params.arguments or {}
        
        try:
            if tool_name == "create_primitive":
                return await self._handle_create_primitive(args)
            elif tool_name == "create_model_from_text":
                return await self._handle_create_model_from_text(args)
            elif tool_name == "execute_cadquery_script":
                return await self._handle_execute_cadquery_script(args)
            else:
                raise MockMcpError(
                    MockErrorCode.MethodNotFound,
                    f"Unknown tool: {tool_name}"
                )
        except Exception as e:
            if isinstance(e, MockMcpError):
                raise
            raise MockMcpError(
                MockErrorCode.InternalError,
                f"Error executing {tool_name}: {str(e)}"
            )
    
    async def _handle_create_primitive(self, args: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
        """Handle the create_primitive tool request.
        
        Args:
            args: The tool arguments containing the primitive shape details.
            
        Returns:
            A dictionary containing the result of the primitive creation.
        """
        shape_type = args.get("shape_type")
        parameters = args.get("parameters", {})
        name = args.get("name", f"Primitive {shape_type.capitalize()}")
        description = args.get("description", f"A {shape_type} created with CadQuery")
        
        # Generate the model using CadQuery
        try:
            model = model_generator.create_primitive(shape_type, parameters)
            
            # Save the model and store metadata
            model_id = self._save_model(model, name, description)
            
            # Return success message with model information
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Created {shape_type} model with ID: {model_id}\n"
                               f"You can access this model as a resource with URI: model://{model_id}"
                    }
                ]
            }
        except Exception as e:
            raise MockMcpError(
                MockErrorCode.InternalError,
                f"Error creating primitive: {str(e)}"
            )
    
    async def _handle_create_model_from_text(self, args: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
        """Handle the create_model_from_text tool request.
        
        Args:
            args: The tool arguments containing the text description of the model.
            
        Returns:
            A dictionary containing the result of the model creation.
        """
        description = args.get("description")
        name = args.get("name", "Text-generated Model")
        format_type = args.get("format", "step")
        
        if not description:
            raise MockMcpError(
                MockErrorCode.InvalidParams,
                "Model description is required"
            )
        
        try:
            # Generate model from text description
            model, code = model_generator.create_from_text(description)
            
            # Save the model
            model_id = self._save_model(model, name, description, code, format_type)
            
            # Return success message with model information and generated code
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Created model from description with ID: {model_id}\n"
                               f"You can access this model as a resource with URI: model://{model_id}\n\n"
                               f"Generated CadQuery code:\n```python\n{code}\n```"
                    }
                ]
            }
        except Exception as e:
            raise MockMcpError(
                MockErrorCode.InternalError,
                f"Error creating model from text: {str(e)}"
            )
    
    async def _handle_execute_cadquery_script(self, args: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
        """Handle the execute_cadquery_script tool request.
        
        Args:
            args: The tool arguments containing the CadQuery Python code.
            
        Returns:
            A dictionary containing the result of the script execution.
        """
        code = args.get("code")
        name = args.get("name", "Custom CadQuery Model")
        description = args.get("description", "A model created with custom CadQuery code")
        format_type = args.get("format", "step")
        
        if not code:
            raise MockMcpError(
                MockErrorCode.InvalidParams,
                "CadQuery code is required"
            )
        
        try:
            # Execute the CadQuery script
            model = model_generator.execute_script(code)
            
            # Save the model
            model_id = self._save_model(model, name, description, code, format_type)
            
            # Return success message with model information
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Successfully executed CadQuery code and created model with ID: {model_id}\n"
                               f"You can access this model as a resource with URI: model://{model_id}"
                    }
                ]
            }
        except Exception as e:
            raise MockMcpError(
                MockErrorCode.InternalError,
                f"Error executing CadQuery script: {str(e)}"
            )
    
    def _save_model(self, 
                   model: cq.Workplane, 
                   name: str, 
                   description: str, 
                   code: Optional[str] = None,
                   format_type: str = "step") -> str:
        """Save a CadQuery model to disk and store its metadata.
        
        Args:
            model: The CadQuery Workplane object.
            name: The name of the model.
            description: The description of the model.
            code: The CadQuery code used to generate the model (optional).
            format_type: The export format (step, stl).
            
        Returns:
            The generated model ID.
        """
        model_id = str(uuid.uuid4())
        model_dir = self.temp_dir / model_id
        model_dir.mkdir(exist_ok=True)
        
        # Export the model in the requested format
        if format_type.lower() == "stl":
            file_path = model_dir / f"{model_id}.stl"
            model.export(str(file_path))
            mime_type = "model/stl"
        else:  # Default to STEP
            file_path = model_dir / f"{model_id}.step"
            model.export(str(file_path))
            mime_type = "model/step"
        
        # Store model metadata
        self.models[model_id] = {
            "id": model_id,
            "name": name,
            "description": description,
            "file_path": str(file_path),
            "mime_type": mime_type,
            "format": format_type,
            "code": code
        }
        
        return model_id
    
    async def run(self) -> None:
        """Start the CAD MCP server."""
        # Use MockStdioTransport instead of the real transport
        transport = MockStdioTransport()
        await self.server.connect(transport)
        print("Mock Claude CAD server running", flush=True)
    
    async def cleanup(self) -> None:
        """Clean up resources used by the server."""
        try:
            # Remove temporary directory
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except Exception as e:
            print(f"Error during cleanup: {e}", flush=True)
        
        # Close the server connection
        await self.server.close()


def main() -> None:
    """Entry point for the Claude CAD mock server."""
    import asyncio
    import signal
    import sys
    
    # Create and run the server
    server = ClaudeCADServer()
    
    # Set up signal handlers
    loop = asyncio.get_event_loop()
    
    for sig in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(server, loop)))
    
    try:
        loop.run_until_complete(server.run())
        loop.run_forever()
    except Exception as e:
        print(f"Server error: {e}", flush=True)
        sys.exit(1)


async def shutdown(server: ClaudeCADServer, loop: asyncio.AbstractEventLoop) -> None:
    """Gracefully shut down the server."""
    print("Shutting down server...", flush=True)
    await server.cleanup()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    
    for task in tasks:
        task.cancel()
    
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


if __name__ == "__main__":
    main()
