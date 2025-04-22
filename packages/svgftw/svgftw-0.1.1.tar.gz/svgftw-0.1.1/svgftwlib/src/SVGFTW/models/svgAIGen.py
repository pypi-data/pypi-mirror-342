from typing import Dict, Any, Optional
import os
from pathlib import Path
import numpy as np
try:
    import onnxruntime as ort
    import torch
    import torch.nn.functional as F
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

class AIStyleTransfer:
    """
    Handles AI-powered SVG style transfer and generation operations.
    """
    
    def __init__(self):
        """Initialize AI style transfer system."""
        self.session = None
        self.current_model = None
        self.cuda_enabled = False
        self.device = "cpu"
        self._check_requirements()
        
    def _check_requirements(self) -> None:
        """Verify AI/ML requirements are met."""
        if not ML_AVAILABLE:
            raise ImportError(
                "AI features require onnxruntime and torch. "
                "Install with: pip install onnxruntime torch"
            )
            
    def load_model(self, model_name: str) -> None:
        """
        Load an ONNX style transfer model.
        
        Args:
            model_name: Name of the style model to load
        """
        model_path = self._get_model_path(model_name)
        providers = ['CPUExecutionProvider']
        
        if self.cuda_enabled:
            providers.insert(0, 'CUDAExecutionProvider')
            
        self.session = ort.InferenceSession(
            model_path, 
            providers=providers
        )
        self.current_model = model_name
        
    def _get_model_path(self, model_name: str) -> str:
        """Get the path to a style model file."""
        models_dir = Path(__file__).parent / "models"
        model_file = f"{model_name}.onnx"
        model_path = models_dir / model_file
        
        if not model_path.exists():
            raise FileNotFoundError(
                f"Style model '{model_name}' not found at {model_path}"
            )
            
        return str(model_path)
        
    def apply_style(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply AI style transfer to SVG attributes.
        
        Args:
            attrs: Original SVG attributes
            
        Returns:
            Processed attributes with AI style transfer applied
        """
        processed_attrs = attrs.copy()
        
        if 'ai-style-model' in attrs:
            model_name = attrs['ai-style-model']
            if self.current_model != model_name:
                self.load_model(model_name)
                
            if 'style' in attrs:
                processed_style = self._transform_style(attrs['style'])
                processed_attrs['style'] = processed_style
                
            if 'd' in attrs:  # Transform path data for artistic effect
                processed_path = self._transform_path(attrs['d'])
                processed_attrs['d'] = processed_path
                
        return processed_attrs
        
    def _transform_style(self, style: str) -> str:
        """
        Transform CSS style string using AI model.
        
        Args:
            style: Original CSS style string
            
        Returns:
            Transformed style string
        """
        if not self.session:
            return style
            
        # Parse style string into features
        style_dict = self._parse_style(style)
        
        # Convert style parameters to model input format
        input_features = self._prepare_style_features(style_dict)
        
        # Run style transfer
        outputs = self.session.run(
            None, 
            {'input': input_features}
        )
        
        # Convert model output back to style string
        transformed_style = self._output_to_style(
            outputs[0], 
            style_dict
        )
        
        return transformed_style
        
    def _transform_path(self, path_data: str) -> str:
        """
        Transform SVG path data using AI model.
        
        Args:
            path_data: Original path data
            
        Returns:
            Artistically transformed path data
        """
        if not self.session:
            return path_data
            
        # Convert path commands to features
        path_features = self._path_to_features(path_data)
        
        # Apply style transfer
        transformed_features = self.session.run(
            None, 
            {'input': path_features}
        )[0]
        
        # Convert back to path data
        return self._features_to_path(transformed_features)
        
    def _parse_style(self, style: str) -> Dict[str, str]:
        """Parse CSS style string into dictionary."""
        if not style:
            return {}
            
        styles = {}
        for item in style.split(';'):
            if ':' in item:
                key, value = item.split(':', 1)
                styles[key.strip()] = value.strip()
        return styles
        
    def _prepare_style_features(
        self, 
        style_dict: Dict[str, str]
    ) -> np.ndarray:
        """Convert style parameters to model input features."""
        # Example feature extraction - actual implementation would be
        # more sophisticated based on the specific model architecture
        features = []
        
        # Color handling
        for key in ['fill', 'stroke']:
            if key in style_dict:
                color = self._parse_color(style_dict[key])
                features.extend(color)
            else:
                features.extend([0, 0, 0])  # Default black
                
        # Numeric properties
        numeric_props = ['stroke-width', 'opacity']
        for prop in numeric_props:
            if prop in style_dict:
                try:
                    value = float(style_dict[prop])
                    features.append(value)
                except ValueError:
                    features.append(1.0)  # Default value
            else:
                features.append(1.0)  # Default value
                
        return np.array(features, dtype=np.float32).reshape(1, -1)
        
    def _parse_color(self, color_str: str) -> list:
        """Parse color string to RGB values."""
        if color_str.startswith('#'):
            # Hex color
            color = color_str.lstrip('#')
            return [
                int(color[i:i+2], 16) / 255 
                for i in (0, 2, 4)
            ]
        return [0, 0, 0]  # Default black
        
    def _output_to_style(
        self, 
        output: np.ndarray, 
        original_style: Dict[str, str]
    ) -> str:
        """Convert model output back to CSS style string."""
        # This is a simplified example - real implementation would be
        # more sophisticated based on model output format
        style_parts = []
        
        # Handle colors
        if output.size >= 6:
            rgb = output[:3] * 255
            style_parts.append(
                f"fill:rgb({','.join(map(str, rgb.astype(int)))})"
            )
            
            rgb = output[3:6] * 255
            style_parts.append(
                f"stroke:rgb({','.join(map(str, rgb.astype(int)))})"
            )
            
        # Handle numeric properties
        if output.size >= 8:
            style_parts.append(f"stroke-width:{output[6]:.2f}")
            style_parts.append(f"opacity:{output[7]:.2f}")
            
        # Preserve any original properties not handled by the model
        for key, value in original_style.items():
            if not any(part.startswith(key + ':') for part in style_parts):
                style_parts.append(f"{key}:{value}")
                
        return ';'.join(style_parts)
        
    def enable_cuda(self) -> None:
        """Enable CUDA acceleration for AI operations."""
        try:
            import torch
            if torch.cuda.is_available():
                self.cuda_enabled = True
                self.device = "cuda"
                # Reload model with CUDA if one is loaded
                if self.current_model:
                    self.load_model(self.current_model)
        except ImportError:
            raise RuntimeError("CUDA acceleration requires PyTorch")
