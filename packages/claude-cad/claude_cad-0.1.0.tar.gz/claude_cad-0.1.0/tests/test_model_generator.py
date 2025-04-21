"""
Tests for the model_generator module.
"""

import unittest
import cadquery as cq

# Add parent directory to the Python path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.claude_cad.model_generator import create_primitive, execute_script


class TestModelGenerator(unittest.TestCase):
    """Test cases for the model_generator module."""
    
    def test_create_primitive_box(self):
        """Test creating a box primitive."""
        # Create a box
        box = create_primitive("box", {
            "length": 10.0,
            "width": 20.0,
            "height": 30.0
        })
        
        # Verify the box was created
        self.assertIsInstance(box, cq.Workplane)
        
        # Verify the dimensions
        bb = box.val().BoundingBox()
        self.assertAlmostEqual(bb.xlen, 10.0)
        self.assertAlmostEqual(bb.ylen, 20.0)
        self.assertAlmostEqual(bb.zlen, 30.0)
    
    def test_create_primitive_sphere(self):
        """Test creating a sphere primitive."""
        # Create a sphere
        sphere = create_primitive("sphere", {
            "radius": 15.0
        })
        
        # Verify the sphere was created
        self.assertIsInstance(sphere, cq.Workplane)
        
        # Verify the dimensions
        bb = sphere.val().BoundingBox()
        self.assertAlmostEqual(bb.xlen, 30.0, delta=0.1)
        self.assertAlmostEqual(bb.ylen, 30.0, delta=0.1)
        self.assertAlmostEqual(bb.zlen, 30.0, delta=0.1)
    
    def test_create_primitive_cylinder(self):
        """Test creating a cylinder primitive."""
        # Create a cylinder
        cylinder = create_primitive("cylinder", {
            "radius": 5.0,
            "height": 25.0
        })
        
        # Verify the cylinder was created
        self.assertIsInstance(cylinder, cq.Workplane)
        
        # Verify the dimensions
        bb = cylinder.val().BoundingBox()
        self.assertAlmostEqual(bb.xlen, 10.0, delta=0.1)
        self.assertAlmostEqual(bb.ylen, 10.0, delta=0.1)
        self.assertAlmostEqual(bb.zlen, 25.0, delta=0.1)
    
    def test_create_primitive_cone(self):
        """Test creating a cone primitive."""
        # Create a cone
        cone = create_primitive("cone", {
            "radius1": 10.0,
            "radius2": 5.0,
            "height": 20.0
        })
        
        # Verify the cone was created
        self.assertIsInstance(cone, cq.Workplane)
        
        # Verify the dimensions
        bb = cone.val().BoundingBox()
        self.assertAlmostEqual(bb.xlen, 20.0, delta=0.1)
        self.assertAlmostEqual(bb.ylen, 20.0, delta=0.1)
        self.assertAlmostEqual(bb.zlen, 20.0, delta=0.1)
    
    def test_execute_script(self):
        """Test executing a CadQuery script."""
        # Simple script to create a box
        script = """
        import cadquery as cq
        
        result = cq.Workplane("XY").box(10, 10, 10)
        """
        
        # Execute the script
        model = execute_script(script)
        
        # Verify the model was created
        self.assertIsInstance(model, cq.Workplane)
        
        # Verify the dimensions
        bb = model.val().BoundingBox()
        self.assertAlmostEqual(bb.xlen, 10.0)
        self.assertAlmostEqual(bb.ylen, 10.0)
        self.assertAlmostEqual(bb.zlen, 10.0)


if __name__ == "__main__":
    unittest.main()
