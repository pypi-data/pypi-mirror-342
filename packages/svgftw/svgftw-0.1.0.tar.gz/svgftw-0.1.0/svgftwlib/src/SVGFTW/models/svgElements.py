from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class SVGElement:
    """
    Represents an SVG element with support for extended attributes.
    """
    type: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate and process attributes after initialization."""
        self._validate_attributes()
        self._process_special_attributes()
    
    def _validate_attributes(self) -> None:
        """Validate SVG element attributes."""
        # Basic SVG element types
        valid_types = {
            'path', 'rect', 'circle', 'ellipse', 'line',
            'polyline', 'polygon', 'text', 'g', 'use',
            'image', 'clipPath', 'mask', 'pattern',
            'ai-generated', 'quantum-path', 'bio-pattern'
        }
        
        if self.type not in valid_types:
            raise ValueError(f"Invalid SVG element type: {self.type}")
            
        # Ensure required attributes are present for specific types
        if self.type == 'path' and 'd' not in self.attributes:
            raise ValueError("Path element requires 'd' attribute")
            
    def _process_special_attributes(self) -> None:
        """Process and validate special attributes for extended features."""
        if 'quantum-entanglement' in self.attributes:
            value = float(self.attributes['quantum-entanglement'])
            if not 0 <= value <= 1:
                raise ValueError("quantum-entanglement must be between 0 and 1")
                
        if 'holographic-depth' in self.attributes:
            value = int(self.attributes['holographic-depth'])
            if not 0 <= value <= 10:
                raise ValueError("holographic-depth must be between 0 and 10")
                
    def update_attribute(self, key: str, value: Any) -> None:
        """
        Update an attribute with validation.
        
        Args:
            key: Attribute name
            value: New attribute value
        """
        self.attributes[key] = value
        self._validate_attributes()
        
    def get_attribute(self, key: str, default: Any = None) -> Any:
        """
        Get an attribute value safely.
        
        Args:
            key: Attribute name
            default: Default value if attribute doesn't exist
            
        Returns:
            Attribute value or default
        """
        return self.attributes.get(key, default)
        
    def has_quantum_attributes(self) -> bool:
        """Check if element has quantum-related attributes."""
        return any(k.startswith('quantum-') for k in self.attributes)
        
    def has_ai_attributes(self) -> bool:
        """Check if element has AI-related attributes."""
        return any(k.startswith('ai-') for k in self.attributes)
        
    def has_bio_attributes(self) -> bool:
        """Check if element has bio-algorithm attributes."""
        return any(k.startswith('bio-') for k in self.attributes)
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert element to dictionary representation.
        
        Returns:
            Dictionary containing element type and attributes
        """
        return {
            'type': self.type,
            'attributes': self.attributes.copy()
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SVGElement':
        """
        Create element from dictionary representation.
        
        Args:
            data: Dictionary containing element data
            
        Returns:
            New SVGElement instance
        """
        return cls(
            type=data['type'],
            attributes=data['attributes'].copy()
        )
