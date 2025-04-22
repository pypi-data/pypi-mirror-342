from typing import Dict, Any, List, Tuple
import numpy as np
from pathlib import Path

class HolographicRenderer:
    """
    Handles holographic/3D-like rendering effects for SVG elements.
    """
    
    def __init__(self):
        """Initialize holographic rendering system."""
        self.depth = 0
        self.cuda_enabled = False
        self.shadow_offset = 2
        self.layer_opacity_step = 0.2
        
    def set_depth(self, depth: int) -> None:
        """
        Set the holographic depth level.
        
        Args:
            depth: Number of depth layers (0-10)
        """
        if not 0 <= depth <= 10:
            raise ValueError("Depth must be between 0 and 10")
        self.depth = depth
        
    def apply_holographic_effect(
        self, 
        element_type: str,
        attrs: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Create layered elements for holographic effect.
        
        Args:
            element_type: Type of SVG element
            attrs: Original attributes
            
        Returns:
            List of attribute dictionaries for layered elements
        """
        if self.depth == 0:
            return [attrs]
            
        layers = []
        base_attrs = attrs.copy()
        
        # Add base element
        layers.append(base_attrs)
        
        if 'd' in attrs:  # Path-based element
            layers.extend(
                self._create_path_layers(attrs)
            )
        else:  # Basic shape
            layers.extend(
                self._create_shape_layers(element_type, attrs)
            )
            
        return layers
        
    def _create_path_layers(
        self, 
        attrs: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Create depth layers for path elements."""
        layers = []
        base_path = attrs['d']
        base_style = attrs.get('style', '')
        
        for i in range(1, self.depth + 1):
            layer = attrs.copy()
            
            # Calculate offset for this layer
            offset = self._calculate_layer_offset(i)
            
            # Transform path for depth effect
            layer['d'] = self._offset_path(base_path, offset)
            
            # Adjust style for depth effect
            layer['style'] = self._adjust_layer_style(
                base_style, 
                i
            )
            
            # Add specific holographic attributes
            layer['data-holo-layer'] = str(i)
            layer['data-holo-depth'] = str(self.depth)
            
            layers.append(layer)
            
        return layers
        
    def _create_shape_layers(
        self, 
        element_type: str,
        attrs: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Create depth layers for basic shape elements."""
        layers = []
        
        for i in range(1, self.depth + 1):
            layer = attrs.copy()
            
            # Calculate offset for this layer
            offset = self._calculate_layer_offset(i)
            
            # Transform shape attributes
            layer = self._offset_shape_attrs(
                element_type,
                layer,
                offset
            )
            
            # Adjust style for depth effect
            if 'style' in layer:
                layer['style'] = self._adjust_layer_style(
                    layer['style'],
                    i
                )
                
            # Add specific holographic attributes
            layer['data-holo-layer'] = str(i)
            layer['data-holo-depth'] = str(self.depth)
            
            layers.append(layer)
            
        return layers
        
    def _calculate_layer_offset(self, layer_index: int) -> Tuple[float, float]:
        """Calculate offset for a specific layer."""
        base_offset = self.shadow_offset * layer_index
        
        # Add some variation to make it more interesting
        angle = np.pi * 0.25  # 45 degrees
        x_offset = base_offset * np.cos(angle)
        y_offset = base_offset * np.sin(angle)
        
        return (x_offset, y_offset)
        
    def _offset_path(
        self, 
        path_data: str,
        offset: Tuple[float, float]
    ) -> str:
        """Offset path data for depth effect."""
        commands = path_data.split()
        new_commands = []
        
        x_offset, y_offset = offset
        
        for cmd in commands:
            if cmd[0].isalpha():
                new_commands.append(cmd)
            else:
                try:
                    coord = float(cmd)
                    # Alternate between x and y coordinates
                    if len(new_commands) % 2 == 1:
                        coord += x_offset
                    else:
                        coord += y_offset
                    new_commands.append(f"{coord:.2f}")
                except ValueError:
                    new_commands.append(cmd)
                    
        return ' '.join(new_commands)
        
    def _offset_shape_attrs(
        self,
        element_type: str,
        attrs: Dict[str, Any],
        offset: Tuple[float, float]
    ) -> Dict[str, Any]:
        """Offset shape attributes for depth effect."""
        x_offset, y_offset = offset
        new_attrs = attrs.copy()
        
        # Handle different shape types
        if element_type in {'rect', 'circle', 'ellipse'}:
            if 'x' in attrs:
                new_attrs['x'] = str(float(attrs['x']) + x_offset)
            if 'y' in attrs:
                new_attrs['y'] = str(float(attrs['y']) + y_offset)
            if 'cx' in attrs:
                new_attrs['cx'] = str(float(attrs['cx']) + x_offset)
            if 'cy' in attrs:
                new_attrs['cy'] = str(float(attrs['cy']) + y_offset)
                
        elif element_type == 'line':
            if 'x1' in attrs:
                new_attrs['x1'] = str(float(attrs['x1']) + x_offset)
                new_attrs['y1'] = str(float(attrs['y1']) + y_offset)
                new_attrs['x2'] = str(float(attrs['x2']) + x_offset)
                new_attrs['y2'] = str(float(attrs['y2']) + y_offset)
                
        return new_attrs
        
    def _adjust_layer_style(self, style: str, layer_index: int) -> str:
        """Adjust style attributes for depth effect."""
        style_dict = self._parse_style(style)
        
        # Calculate opacity for this layer
        base_opacity = float(
            style_dict.get('opacity', '1')
        )
        layer_opacity = base_opacity * (
            1 - layer_index * self.layer_opacity_step
        )
        style_dict['opacity'] = f"{max(0.1, layer_opacity):.2f}"
        
        # Add blur effect for depth
        blur_amount = layer_index * 0.5
        filter_effect = f"blur({blur_amount}px)"
        style_dict['filter'] = filter_effect
        
        return self._dict_to_style(style_dict)
        
    def _parse_style(self, style: str) -> Dict[str, str]:
        """Parse CSS style string into dictionary."""
        if not style:
            return {}
            
        style_dict = {}
        for item in style.split(';'):
            if ':' in item:
                key, value = item.split(':', 1)
                style_dict[key.strip()] = value.strip()
                
        return style_dict
        
    def _dict_to_style(self, style_dict: Dict[str, str]) -> str:
        """Convert style dictionary to CSS string."""
        return ';'.join(
            f"{k}:{v}" 
            for k, v in style_dict.items()
        )
        
    def enable_cuda(self) -> None:
        """Enable CUDA acceleration for complex effects."""
        try:
            import numba.cuda
            self.cuda_enabled = True
        except ImportError:
            raise RuntimeError("CUDA acceleration requires numba")
