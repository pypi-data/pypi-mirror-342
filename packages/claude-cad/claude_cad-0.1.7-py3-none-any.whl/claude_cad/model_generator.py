"""
Model generator functions for Claude CAD.

This module contains functions to generate CadQuery models from various inputs
such as primitive parameters, text descriptions, and custom code.
"""

import re
from typing import Dict, Any, Tuple, Union, List, Optional

import cadquery as cq

from . import utils


def create_primitive(shape_type: str, parameters: Dict[str, Any]) -> cq.Workplane:
    """Create a primitive 3D shape based on the given parameters.
    
    Args:
        shape_type: The type of shape to create (box, sphere, cylinder, cone).
        parameters: A dictionary of parameters for the shape.
        
    Returns:
        A CadQuery Workplane object representing the shape.
        
    Raises:
        ValueError: If the shape type is invalid or required parameters are missing.
    """
    # Start with a base workplane
    result = cq.Workplane("XY")
    
    if shape_type == "box":
        # Required parameters for a box
        length = float(parameters.get("length", 10.0))
        width = float(parameters.get("width", 10.0))
        height = float(parameters.get("height", 10.0))
        centered = bool(parameters.get("centered", True))
        
        # Create the box
        result = result.box(length, width, height, centered=centered)
        
    elif shape_type == "sphere":
        # Required parameters for a sphere
        radius = float(parameters.get("radius", 5.0))
        
        # Create the sphere
        result = result.sphere(radius)
        
    elif shape_type == "cylinder":
        # Required parameters for a cylinder
        radius = float(parameters.get("radius", 5.0))
        height = float(parameters.get("height", 10.0))
        centered = bool(parameters.get("centered", True))
        
        # Create the cylinder
        result = result.cylinder(height, radius, centered=centered)
        
    elif shape_type == "cone":
        # Required parameters for a cone
        radius1 = float(parameters.get("radius1", 5.0))
        radius2 = float(parameters.get("radius2", 0.0))
        height = float(parameters.get("height", 10.0))
        centered = bool(parameters.get("centered", True))
        
        # Create the cone
        result = result.cone(height, radius1, radius2, centered=centered)
        
    else:
        raise ValueError(f"Invalid shape type: {shape_type}")
    
    return result


def create_from_text(description: str) -> Tuple[cq.Workplane, str]:
    """Create a 3D model from a text description.
    
    This function interprets a natural language description and generates
    a corresponding CadQuery model.
    
    Args:
        description: A natural language description of the 3D model to create.
        
    Returns:
        A tuple containing:
        - The generated CadQuery Workplane object
        - The Python code used to generate the model
    """
    # Parse the description to extract model type and parameters
    model_type, parameters = _parse_description(description)
    
    # Generate CadQuery code based on the parsed description
    code = _generate_cadquery_code(model_type, parameters, description)
    
    # Execute the generated code to create the model
    model = execute_script(code)
    
    return model, code


def execute_script(code: str) -> cq.Workplane:
    """Execute CadQuery Python code to create a 3D model.
    
    Args:
        code: Python code using CadQuery to create a model.
        
    Returns:
        A CadQuery Workplane object representing the model.
        
    Raises:
        Exception: If there's an error executing the code or if it doesn't produce a valid model.
    """
    # Define a namespace for execution
    namespace = {
        "cq": cq,
        "cadquery": cq,
        "result": None
    }
    
    # Execute the code
    try:
        exec(code, namespace)
    except Exception as e:
        raise Exception(f"Error executing CadQuery code: {str(e)}")
    
    # Retrieve the result variable
    result = namespace.get("result")
    
    # If no result variable, try to find a variable that looks like a CadQuery object
    if result is None:
        for name, value in namespace.items():
            if isinstance(value, cq.Workplane):
                result = value
                break
    
    # Ensure we have a valid model
    if not isinstance(result, cq.Workplane):
        raise Exception("CadQuery code did not produce a valid model. Make sure to assign your model to a variable named 'result'.")
    
    return result


def _parse_description(description: str) -> Tuple[str, Dict[str, Any]]:
    """Parse a natural language description to extract model type and parameters.
    
    Args:
        description: A natural language description of the 3D model.
        
    Returns:
        A tuple containing the model type and a dictionary of parameters.
    """
    # Default to a simple box if we can't parse anything specific
    model_type = "custom"
    parameters = {}
    
    # Look for common shape types
    if re.search(r'\b(box|cube|block|rectangular)\b', description, re.IGNORECASE):
        model_type = "box"
        
        # Try to extract dimensions
        length_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:length|long)', description, re.IGNORECASE)
        width_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:width|wide)', description, re.IGNORECASE)
        height_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:height|tall|high)', description, re.IGNORECASE)
        
        if length_match:
            parameters["length"] = float(length_match.group(1))
        if width_match:
            parameters["width"] = float(width_match.group(1))
        if height_match:
            parameters["height"] = float(height_match.group(1))
    
    elif re.search(r'\b(sphere|ball|round)\b', description, re.IGNORECASE):
        model_type = "sphere"
        
        # Try to extract radius
        radius_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:radius)', description, re.IGNORECASE)
        diameter_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:diameter)', description, re.IGNORECASE)
        
        if radius_match:
            parameters["radius"] = float(radius_match.group(1))
        elif diameter_match:
            parameters["radius"] = float(diameter_match.group(1)) / 2.0
    
    elif re.search(r'\b(cylinder|tube|pipe)\b', description, re.IGNORECASE):
        model_type = "cylinder"
        
        # Try to extract dimensions
        radius_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:radius)', description, re.IGNORECASE)
        diameter_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:diameter)', description, re.IGNORECASE)
        height_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:height|tall|high)', description, re.IGNORECASE)
        
        if radius_match:
            parameters["radius"] = float(radius_match.group(1))
        elif diameter_match:
            parameters["radius"] = float(diameter_match.group(1)) / 2.0
        
        if height_match:
            parameters["height"] = float(height_match.group(1))
    
    elif re.search(r'\b(cone|conical|pyramid)\b', description, re.IGNORECASE):
        model_type = "cone"
        
        # Try to extract dimensions
        radius1_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:base radius|bottom radius)', description, re.IGNORECASE)
        radius2_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:top radius)', description, re.IGNORECASE)
        height_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:height|tall|high)', description, re.IGNORECASE)
        
        if radius1_match:
            parameters["radius1"] = float(radius1_match.group(1))
        
        if radius2_match:
            parameters["radius2"] = float(radius2_match.group(1))
        elif "cone" in description.lower():
            # Default to a pointed cone if not specified
            parameters["radius2"] = 0.0
        
        if height_match:
            parameters["height"] = float(height_match.group(1))
    
    # If it's a gear or complex shape, use a custom model
    elif re.search(r'\b(gear|cog|wheel|teeth)\b', description, re.IGNORECASE):
        model_type = "gear"
        
        # Extract gear parameters
        num_teeth_match = re.search(r'(\d+)\s*(?:teeth|tooth)', description, re.IGNORECASE)
        pitch_diameter_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:pitch diameter|diameter)', description, re.IGNORECASE)
        pressure_angle_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:degree|deg)?\s*(?:pressure angle)', description, re.IGNORECASE)
        
        if num_teeth_match:
            parameters["num_teeth"] = int(num_teeth_match.group(1))
        else:
            parameters["num_teeth"] = 20  # Default
        
        if pitch_diameter_match:
            parameters["pitch_diameter"] = float(pitch_diameter_match.group(1))
        else:
            parameters["pitch_diameter"] = 50.0  # Default
        
        if pressure_angle_match:
            parameters["pressure_angle"] = float(pressure_angle_match.group(1))
        else:
            parameters["pressure_angle"] = 20.0  # Default
    
    elif re.search(r'\b(screw|bolt|thread|nut)\b', description, re.IGNORECASE):
        model_type = "screw"
        
        # Extract thread parameters
        diameter_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:diameter)', description, re.IGNORECASE)
        length_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:length|long)', description, re.IGNORECASE)
        
        if diameter_match:
            parameters["diameter"] = float(diameter_match.group(1))
        else:
            parameters["diameter"] = 5.0  # Default
        
        if length_match:
            parameters["length"] = float(length_match.group(1))
        else:
            parameters["length"] = 20.0  # Default
    
    # Extract common operations
    if re.search(r'\b(holes?|bore|drill)\b', description, re.IGNORECASE):
        parameters["has_holes"] = True
        
        # Try to extract hole dimensions
        hole_diameter_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:diameter|dia)\s*(?:hole|bore)', description, re.IGNORECASE)
        if hole_diameter_match:
            parameters["hole_diameter"] = float(hole_diameter_match.group(1))
        else:
            parameters["hole_diameter"] = 5.0  # Default
    
    if re.search(r'\b(fillet|round|radius)\b', description, re.IGNORECASE):
        parameters["has_fillets"] = True
        
        # Try to extract fillet radius
        fillet_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:fillet|round|radius)', description, re.IGNORECASE)
        if fillet_match:
            parameters["fillet_radius"] = float(fillet_match.group(1))
        else:
            parameters["fillet_radius"] = 1.0  # Default
    
    if re.search(r'\b(chamfer|bevel)\b', description, re.IGNORECASE):
        parameters["has_chamfers"] = True
        
        # Try to extract chamfer distance
        chamfer_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:chamfer|bevel)', description, re.IGNORECASE)
        if chamfer_match:
            parameters["chamfer_distance"] = float(chamfer_match.group(1))
        else:
            parameters["chamfer_distance"] = 1.0  # Default
    
    if re.search(r'\b(shell|hollow|thin)\b', description, re.IGNORECASE):
        parameters["is_shelled"] = True
        
        # Try to extract shell thickness
        shell_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m)?\s*(?:shell|wall|thick)', description, re.IGNORECASE)
        if shell_match:
            parameters["shell_thickness"] = float(shell_match.group(1))
        else:
            parameters["shell_thickness"] = 1.0  # Default
    
    return model_type, parameters


def _generate_cadquery_code(model_type: str, parameters: Dict[str, Any], description: str) -> str:
    """Generate CadQuery Python code based on the model type and parameters.
    
    Args:
        model_type: The type of model to generate.
        parameters: A dictionary of parameters for the model.
        description: The original text description.
        
    Returns:
        Python code that uses CadQuery to create the model.
    """
    code_lines = [
        "import cadquery as cq",
        "",
        f"# Model generated from description: {description}",
        ""
    ]
    
    if model_type == "box":
        length = parameters.get("length", 10.0)
        width = parameters.get("width", 10.0)
        height = parameters.get("height", 10.0)
        
        code_lines.extend([
            f"# Create a box with dimensions: {length} x {width} x {height}",
            "result = cq.Workplane(\"XY\")",
            f"result = result.box({length}, {width}, {height}, centered=True)"
        ])
        
    elif model_type == "sphere":
        radius = parameters.get("radius", 5.0)
        
        code_lines.extend([
            f"# Create a sphere with radius: {radius}",
            "result = cq.Workplane(\"XY\")",
            f"result = result.sphere({radius})"
        ])
        
    elif model_type == "cylinder":
        radius = parameters.get("radius", 5.0)
        height = parameters.get("height", 10.0)
        
        code_lines.extend([
            f"# Create a cylinder with radius: {radius} and height: {height}",
            "result = cq.Workplane(\"XY\")",
            f"result = result.cylinder({height}, {radius}, centered=True)"
        ])
        
    elif model_type == "cone":
        radius1 = parameters.get("radius1", 5.0)
        radius2 = parameters.get("radius2", 0.0)
        height = parameters.get("height", 10.0)
        
        code_lines.extend([
            f"# Create a cone with base radius: {radius1}, top radius: {radius2}, and height: {height}",
            "result = cq.Workplane(\"XY\")",
            f"result = result.cone({height}, {radius1}, {radius2}, centered=True)"
        ])
        
    elif model_type == "gear":
        num_teeth = parameters.get("num_teeth", 20)
        pitch_diameter = parameters.get("pitch_diameter", 50.0)
        pressure_angle = parameters.get("pressure_angle", 20.0)
        thickness = parameters.get("height", 5.0)
        
        code_lines.extend([
            f"# Create a gear with {num_teeth} teeth, pitch diameter: {pitch_diameter}, and pressure angle: {pressure_angle}",
            "import math",
            "",
            f"num_teeth = {num_teeth}",
            f"pitch_diameter = {pitch_diameter}",
            f"pressure_angle = {pressure_angle}",
            f"thickness = {thickness}",
            "",
            "# Calculate gear parameters",
            "module_val = pitch_diameter / num_teeth",
            "addendum = module_val",
            "dedendum = 1.25 * module_val",
            "outer_diameter = pitch_diameter + 2 * addendum",
            "root_diameter = pitch_diameter - 2 * dedendum",
            "base_diameter = pitch_diameter * math.cos(math.radians(pressure_angle))",
            "tooth_angle = 360 / num_teeth",
            "",
            "# Create the gear",
            "result = cq.Workplane(\"XY\")",
            "",
            "# Create the base cylinder",
            f"result = result.circle(pitch_diameter / 2).extrude({thickness})",
            "",
            "# Add hub/mounting hole (optional)",
            "hub_diameter = pitch_diameter * 0.3",
            "result = result.faces(\">Z\").workplane().circle(hub_diameter / 2).extrude(thickness * 0.5)",
            "",
            "# Create a mounting hole",
            "hole_diameter = pitch_diameter * 0.2",
            "result = result.faces(\">Z\").workplane().circle(hole_diameter / 2).cutThruAll()"
        ])
        
    elif model_type == "screw":
        diameter = parameters.get("diameter", 5.0)
        length = parameters.get("length", 20.0)
        head_diameter = diameter * 1.8
        head_height = diameter * 0.6
        
        code_lines.extend([
            f"# Create a screw with diameter: {diameter} and length: {length}",
            f"shaft_diameter = {diameter}",
            f"shaft_length = {length}",
            f"head_diameter = {head_diameter}",
            f"head_height = {head_height}",
            "",
            "# Create the shaft",
            "result = cq.Workplane(\"XY\")",
            "result = result.circle(shaft_diameter / 2).extrude(shaft_length)",
            "",
            "# Create the head",
            "result = result.faces(\">Z\").workplane().circle(head_diameter / 2).extrude(head_height)",
            "",
            "# Add a slot to the head",
            "slot_width = head_diameter * 0.2",
            "slot_depth = head_height * 0.5",
            "result = result.faces(\">Z\").workplane()",
            "result = result.slot2D(slot_width, head_diameter - 1, 0).cutBlind(-slot_depth)"
        ])
        
    else:
        # Default to a simple box if model type is not recognized
        code_lines.extend([
            "# Create a default box",
            "result = cq.Workplane(\"XY\")",
            "result = result.box(10, 10, 10, centered=True)"
        ])
    
    # Add optional features based on parameters
    if parameters.get("has_holes", False):
        hole_diameter = parameters.get("hole_diameter", 5.0)
        code_lines.extend([
            "",
            f"# Add a through hole with diameter: {hole_diameter}",
            f"result = result.faces(\">Z\").workplane().circle({hole_diameter / 2}).cutThruAll()"
        ])
    
    if parameters.get("has_fillets", False):
        fillet_radius = parameters.get("fillet_radius", 1.0)
        code_lines.extend([
            "",
            f"# Add fillets with radius: {fillet_radius}",
            f"result = result.edges().fillet({fillet_radius})"
        ])
    
    if parameters.get("has_chamfers", False):
        chamfer_distance = parameters.get("chamfer_distance", 1.0)
        code_lines.extend([
            "",
            f"# Add chamfers with distance: {chamfer_distance}",
            f"result = result.edges().chamfer({chamfer_distance})"
        ])
    
    if parameters.get("is_shelled", False):
        shell_thickness = parameters.get("shell_thickness", 1.0)
        code_lines.extend([
            "",
            f"# Create a shell with thickness: {shell_thickness}",
            f"result = result.shell(-{shell_thickness})"
        ])
    
    # Return the generated code
    return "\n".join(code_lines)
