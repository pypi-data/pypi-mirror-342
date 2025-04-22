# filepath: c:\Users\paule\Documents\Github\SideProjects\SVGFTW\svgftw_lib_1\svgftwlib\src\SVGFTW\models\svgFactory.py
from typing import Dict, Any, Set, Tuple, Optional, List, Union
from .svgElements import SVGElement, Shape, Path

class SVGFactory:
    """
    Element factory with spec validation
    
    Creates SVG elements with attribute validation according to the SVG specification.
    Distinguishes between required and optional attributes for each element type.
    """
    # Required and optional attributes for each SVG element
    # Format: 'element': ({'required'}, {'optional'})
    _element_specs = {
        'rect': ({'x', 'y', 'width', 'height'}, 
                {'rx', 'ry', 'pathLength'}),
        'circle': ({'cx', 'cy', 'r'}, 
                  {'pathLength'}),
        'ellipse': ({'cx', 'cy', 'rx', 'ry'}, 
                   {'pathLength'}),
        'line': ({'x1', 'y1', 'x2', 'y2'}, 
                {'pathLength'}),
        'polyline': ({'points'}, 
                    {'pathLength'}),
        'polygon': ({'points'}, 
                   {'pathLength'}),
        'path': ({'d'}, 
                {'pathLength'}),
        'text': (set(), 
               {'x', 'y', 'dx', 'dy', 'rotate', 'textLength', 'lengthAdjust'}),
        'g': (set(), set()),  # No required attributes
        'use': ({'href', 'x', 'y'}, 
               {'width', 'height'}),
        'image': ({'href', 'x', 'y', 'width', 'height'}, 
                 {'preserveAspectRatio'}),
        'linearGradient': ({'id'}, 
                         {'x1', 'y1', 'x2', 'y2', 'gradientUnits', 'gradientTransform', 'spreadMethod'}),
        'radialGradient': ({'id'}, 
                         {'cx', 'cy', 'r', 'fx', 'fy', 'fr', 'gradientUnits', 'gradientTransform', 'spreadMethod'}),
        'stop': (set(), 
                {'offset', 'stop-color', 'stop-opacity'})
    }
    
    # Common presentation attributes applicable to many SVG elements
    _presentation_attrs = {
        'fill', 'fill-opacity', 'fill-rule', 
        'stroke', 'stroke-dasharray', 'stroke-dashoffset', 
        'stroke-linecap', 'stroke-linejoin', 'stroke-miterlimit', 
        'stroke-opacity', 'stroke-width',
        'opacity', 'color', 'display', 'visibility',
        'transform'
    }
    
    # Types for attribute validation
    _attr_types = {
        'x': (float, int),
        'y': (float, int),
        'width': (float, int),
        'height': (float, int),
        'cx': (float, int),
        'cy': (float, int),
        'r': (float, int),
        'rx': (float, int),
        'ry': (float, int),
        'opacity': (float, int),
        'fill-opacity': (float, int),
        'stroke-opacity': (float, int),
        'points': str,
        'd': str,
    }
    
    @classmethod
    def create(cls, tag: str, **attrs) -> SVGElement:
        """
        Create an SVG element with attribute validation.
        
        Args:
            tag: The SVG element tag name
            **attrs: Attributes to set on the element
            
        Returns:
            A new SVGElement instance
            
        Raises:
            ValueError: If the tag is invalid or required attributes are missing
        """
        # Check if this is a valid SVG element
        if tag not in cls._element_specs:
            similar_tags = [t for t in cls._element_specs.keys() if tag in t]
            suggestion = f" Did you mean {', '.join(similar_tags)}?" if similar_tags else ""
            raise ValueError(f"Invalid SVG element: '{tag}'.{suggestion}")
        
        # Get required and optional attribute sets
        required_attrs, optional_attrs = cls._element_specs[tag]
        
        # Check for missing required attributes
        missing = required_attrs - attrs.keys()
        if missing:
            raise ValueError(f"Missing required attributes for {tag}: {missing}")
        
        # Check for unknown attributes (excluding presentation attributes which are always allowed)
        unknown = attrs.keys() - required_attrs - optional_attrs - cls._presentation_attrs - {'class', 'id', 'style'}
        if unknown:
            print(f"Warning: Unknown attributes for {tag}: {unknown}")
        
        # Validate attribute types if defined
        for attr, value in attrs.items():
            if attr in cls._attr_types:
                expected_type = cls._attr_types[attr]
                if not isinstance(expected_type, tuple):
                    expected_type = (expected_type,)
                
                if not any(isinstance(value, t) for t in expected_type):
                    actual_type = type(value).__name__
                    expected_names = [t.__name__ for t in expected_type]
                    raise TypeError(f"Attribute '{attr}' expects {' or '.join(expected_names)}, got {actual_type}")
        
        # Select appropriate class based on element type
        if tag in ('rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon'):
            return Shape(tag, **attrs)
        elif tag == 'path':
            return Path(tag, **attrs)
        else:
            return SVGElement(tag, **attrs)
            
    @classmethod
    def rect(cls, x: float, y: float, width: float, height: float, **kwargs) -> Shape:
        """Convenience method to create a rectangle"""
        return cls.create('rect', x=x, y=y, width=width, height=height, **kwargs)
    
    @classmethod
    def circle(cls, cx: float, cy: float, r: float, **kwargs) -> Shape:
        """Convenience method to create a circle"""
        return cls.create('circle', cx=cx, cy=cy, r=r, **kwargs)
        
    @classmethod
    def ellipse(cls, cx: float, cy: float, rx: float, ry: float, **kwargs) -> Shape:
        """Convenience method to create an ellipse"""
        return cls.create('ellipse', cx=cx, cy=cy, rx=rx, ry=ry, **kwargs)
        
    @classmethod
    def line(cls, x1: float, y1: float, x2: float, y2: float, **kwargs) -> Shape:
        """Convenience method to create a line"""
        return cls.create('line', x1=x1, y1=y1, x2=x2, y2=y2, **kwargs)
        
    @classmethod
    def path(cls, d: str, **kwargs) -> Path:
        """Convenience method to create a path"""
        return cls.create('path', d=d, **kwargs)
        
    @classmethod
    def group(cls, **kwargs) -> SVGElement:
        """Convenience method to create a group"""
        return cls.create('g', **kwargs)
