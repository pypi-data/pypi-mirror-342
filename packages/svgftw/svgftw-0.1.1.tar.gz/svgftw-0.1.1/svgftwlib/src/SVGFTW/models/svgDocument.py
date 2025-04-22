from typing import Optional, Union, List, Dict, Any, Tuple
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

from .svgElements import SVGElement, Gradient, Group
from .svgFactory import SVGFactory

class SVGDocument:
    """
    Main SVG document class that manages the root SVG element, definitions,
    and provides methods to add and manage elements within the SVG structure.
    """
    def __init__(self, width: Union[int, float] = 100, height: Union[int, float] = 100, 
                 viewBox: Optional[str] = None):
        """
        Initialize a new SVG document.
        
        Args:
            width: The width of the SVG document
            height: The height of the SVG document
            viewBox: Optional viewBox specification (minX, minY, width, height)
        """
        attrs = {
            "xmlns": "http://www.w3.org/2000/svg",
            "width": width,
            "height": height
        }
        
        # Add viewBox if specified
        if viewBox:
            attrs["viewBox"] = viewBox
        else:
            attrs["viewBox"] = f"0 0 {width} {height}"
            
        self.root = SVGElement('svg', **attrs)
        self.defs = SVGElement('defs')
        self.root.children.append(self.defs)
        
        # Keep a reference to the main group for easier access
        self.main_group: Optional[Group] = None

    def add_element(self, element: SVGElement, parent: Optional[SVGElement] = None) -> SVGElement:
        """
        Add an SVG element to the document structure.
        
        Args:
            element: The SVG element to add
            parent: The parent element (defaults to root if not specified)
            
        Returns:
            The added element
        """
        (parent or self.root).children.append(element)
        return element
    
    def add_gradient(self, grad: Gradient) -> str:
        """
        Add a gradient definition to the document.
        
        Args:
            grad: The gradient element to add
            
        Returns:
            The gradient's ID for reference in fill attributes
        """
        self.defs.children.append(grad)
        return grad.id  # Returns reference ID for usage
    
    def create_group(self, **attrs) -> Group:
        """
        Create and add a new group element to the document.
        
        Args:
            **attrs: Attributes for the group element
            
        Returns:
            The newly created group
        """
        group = SVGFactory.group(**attrs)
        return self.add_element(group)
    
    def set_main_group(self, **attrs) -> Group:
        """
        Set up a main group as the primary container for content.
        Useful for applying global transforms or styles.
        
        Args:
            **attrs: Attributes for the main group
            
        Returns:
            The main group
        """
        self.main_group = self.create_group(**attrs)
        return self.main_group
    
    def add_shape(self, shape_type: str, **attrs) -> SVGElement:
        """
        Create and add a shape using the SVGFactory.
        
        Args:
            shape_type: The type of shape (rect, circle, etc.)
            **attrs: Attributes for the shape
            
        Returns:
            The newly created shape element
        """
        shape = SVGFactory.create(shape_type, **attrs)
        return self.add_element(shape, self.main_group)
        
    def rect(self, x: float, y: float, width: float, height: float, **kwargs) -> SVGElement:
        """Convenience method to create and add a rectangle"""
        rect = SVGFactory.rect(x, y, width, height, **kwargs)
        return self.add_element(rect, self.main_group)
    
    def circle(self, cx: float, cy: float, r: float, **kwargs) -> SVGElement:
        """Convenience method to create and add a circle"""
        circle = SVGFactory.circle(cx, cy, r, **kwargs)
        return self.add_element(circle, self.main_group)
    
    def path(self, d: str, **kwargs) -> SVGElement:
        """Convenience method to create and add a path"""
        path = SVGFactory.path(d, **kwargs)
        return self.add_element(path, self.main_group)
    
    def to_string(self, pretty: bool = True) -> str:
        """
        Render the SVG document to a string.
        
        Args:
            pretty: Whether to format the output with nice indentation
            
        Returns:
            The SVG document as a string
        """
        xml_str = ET.tostring(self.root.to_xml(), encoding='unicode')
        
        if pretty:
            parsed = minidom.parseString(xml_str)
            return parsed.toprettyxml(indent="  ")
        return xml_str
    
    def save(self, filename: str, pretty: bool = True) -> None:
        """
        Save the SVG document to a file.
        
        Args:
            filename: The path to save the SVG file to
            pretty: Whether to format the output with nice indentation
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.to_string(pretty))
