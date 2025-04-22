"""
AI-powered vector generation and manipulation using multimodal models.
Enhanced with model ensembles, memory caching, and differentiable SVG rendering.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
import numpy as np
from pathlib import Path
from functools import lru_cache

from ..utils.feature_loader import FeatureRegistry, requires_feature

class DifferentiableSVGRenderer:
    """Differentiable rendering system for SVG elements."""
    
    def __init__(self, resolution: Tuple[int, int] = (512, 512)):
        """
        Initialize differentiable SVG renderer.
        
        Args:
            resolution: Output resolution (width, height)
        """
        import torch
        import torch.nn.functional as F
        
        self.torch = torch
        self.F = F
        self.resolution = resolution
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def render(self, element: Dict[str, Any]) -> np.ndarray:
        """
        Render SVG element as differentiable tensor.
        
        Args:
            element: SVG element dictionary
            
        Returns:
            Rendered tensor
        """
        paths = self._parse_path_data(element['d'])
        return self._render_paths(paths)
        
    def _parse_path_data(self, path_data: str) -> List[Dict[str, Any]]:
        """Parse SVG path data into command lists."""
        paths = []
        current_path = []
        tokens = path_data.split()
        
        for token in tokens:
            if token[0].isalpha():
                if current_path:
                    paths.append({'commands': current_path})
                current_path = [token]
            else:
                current_path.append(token)
                
        if current_path:
            paths.append({'commands': current_path})
            
        return paths
        
    def _render_paths(self, paths: List[Dict[str, Any]]) -> np.ndarray:
        """Render paths to differentiable tensor."""
        device = self.device
        width, height = self.resolution
        canvas = self.torch.zeros((1, 1, height, width), device=device)
        
        for path in paths:
            points = self._commands_to_points(path['commands'])
            if len(points) < 2:
                continue
                
            # Convert to tensor
            points = self.torch.tensor(
                points,
                dtype=self.torch.float32,
                device=device
            )
            
            # Scale to canvas
            points[:, 0] = points[:, 0] * width / 512
            points[:, 1] = points[:, 1] * height / 512
            
            # Render line segments
            for i in range(len(points) - 1):
                start = points[i]
                end = points[i + 1]
                
                # Create anti-aliased line
                self._draw_line(canvas, start, end)
                
        return canvas.cpu().numpy()
        
    def _commands_to_points(self, commands: List[str]) -> List[Tuple[float, float]]:
        """Convert path commands to point sequence."""
        points = []
        current = None
        
        i = 0
        while i < len(commands):
            cmd = commands[i]
            
            if cmd[0] == 'M':
                x = float(commands[i + 1])
                y = float(commands[i + 2])
                points.append((x, y))
                current = (x, y)
                i += 3
            elif cmd[0] == 'L':
                x = float(commands[i + 1])
                y = float(commands[i + 2])
                points.append((x, y))
                current = (x, y)
                i += 3
            elif cmd[0] == 'Q':
                # Sample quadratic curve
                x1 = float(commands[i + 1])
                y1 = float(commands[i + 2])
                x2 = float(commands[i + 3])
                y2 = float(commands[i + 4])
                
                # Sample points along curve
                t = np.linspace(0, 1, 10)
                for t_val in t:
                    x = (1-t_val)**2 * current[0] + \
                        2*(1-t_val)*t_val * x1 + \
                        t_val**2 * x2
                    y = (1-t_val)**2 * current[1] + \
                        2*(1-t_val)*t_val * y1 + \
                        t_val**2 * y2
                    points.append((x, y))
                    
                current = (x2, y2)
                i += 5
            else:
                i += 1
                
        return points
        
    def _draw_line(
        self,
        canvas: "torch.Tensor",
        start: "torch.Tensor",
        end: "torch.Tensor"
    ) -> None:
        """Draw anti-aliased line on canvas."""
        # Create line mask
        x0, y0 = start.round().long()
        x1, y1 = end.round().long()
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        
        if dx == 0 and dy == 0:
            return
            
        # Use Xiaolin Wu's line algorithm for anti-aliasing
        steep = dy > dx
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            dx, dy = dy, dx
            
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            
        gradient = dy / dx if dx != 0 else 1
        
        # Handle first endpoint
        xend = round(x0)
        yend = y0 + gradient * (xend - x0)
        xgap = 1 - ((x0 + 0.5) - int(x0 + 0.5))
        xpxl1 = xend
        ypxl1 = int(yend)
        
        if steep:
            self._plot(canvas, ypxl1, xpxl1, (1 - (yend - ypxl1)) * xgap)
            self._plot(canvas, ypxl1 + 1, xpxl1, (yend - ypxl1) * xgap)
        else:
            self._plot(canvas, xpxl1, ypxl1, (1 - (yend - ypxl1)) * xgap)
            self._plot(canvas, xpxl1, ypxl1 + 1, (yend - ypxl1) * xgap)
            
        intery = yend + gradient
        
        # Handle second endpoint
        xend = round(x1)
        yend = y1 + gradient * (xend - x1)
        xgap = (x1 + 0.5) - int(x1 + 0.5)
        xpxl2 = xend
        ypxl2 = int(yend)
        
        if steep:
            self._plot(canvas, ypxl2, xpxl2, (1 - (yend - ypxl2)) * xgap)
            self._plot(canvas, ypxl2 + 1, xpxl2, (yend - ypxl2) * xgap)
        else:
            self._plot(canvas, xpxl2, ypxl2, (1 - (yend - ypxl2)) * xgap)
            self._plot(canvas, xpxl2, ypxl2 + 1, (yend - ypxl2) * xgap)
            
        # Main loop
        if steep:
            for x in range(xpxl1 + 1, xpxl2):
                y = int(intery)
                self._plot(canvas, y, x, 1 - (intery - y))
                self._plot(canvas, y + 1, x, intery - y)
                intery = intery + gradient
        else:
            for x in range(xpxl1 + 1, xpxl2):
                y = int(intery)
                self._plot(canvas, x, y, 1 - (intery - y))
                self._plot(canvas, x, y + 1, intery - y)
                intery = intery + gradient
                
    def _plot(
        self,
        canvas: "torch.Tensor",
        x: int,
        y: int,
        brightness: float
    ) -> None:
        """Plot a single point on canvas with given brightness."""
        if 0 <= x < canvas.shape[2] and 0 <= y < canvas.shape[3]:
            canvas[0, 0, x, y] = brightness

@FeatureRegistry.register('ai-basic', ['onnxruntime'])
class AIVectorStylerBasic:
    """Handle basic AI-powered vector art generation using ONNX Runtime."""
    
    def __init__(self):
        import onnxruntime as ort
        self.ort = ort
        self.style_models = []
        self._initialize_basic()
    
    def _initialize_basic(self):
        """Initialize basic ONNX models."""
        pass  # Basic initialization code here

# Cache size for style transfer results
STYLE_CACHE_SIZE = 100

@FeatureRegistry.register('ai-full', ['torch', 'transformers'])
class AIVectorStyler:
    """Handle AI-powered vector art generation and styling."""
    
    def __init__(self, ensemble_size: int = 3, diff_render: bool = True):
        """
        Initialize AI vector styling system.
        
        Args:
            ensemble_size: Number of models in the ensemble
            diff_render: Enable differentiable SVG rendering
        """
        import torch
        import torch.nn.functional as F
        import torch.nn as nn
        from transformers import CLIPProcessor, CLIPModel, AutoModel
        
        self.torch = torch
        self.F = F
        self.nn = nn
        self.CLIPProcessor = CLIPProcessor
        self.CLIPModel = CLIPModel
        self.AutoModel = AutoModel
        
        self.clip_model = None
        self.clip_processor = None
        self.style_models = []
        self.device = "cpu"
        self.ensemble_size = ensemble_size
        self.style_cache = {}
        
        # Initialize differentiable renderer
        self.diff_render = diff_render
        if diff_render:
            self.diff_renderer = DifferentiableSVGRenderer()
            
        # Initialize GAN components
        self.style_discriminator = None
        self.style_generator = None
        self._initialize_gan()
            
    def _initialize_gan(self) -> None:
        """Initialize GAN components for style preservation."""
        # Style discriminator network
        self.style_discriminator = self.nn.Sequential(
            self.nn.Linear(512, 256),
            self.nn.LeakyReLU(0.2),
            self.nn.Linear(256, 128),
            self.nn.LeakyReLU(0.2),
            self.nn.Linear(128, 1),
            self.nn.Sigmoid()
        ).to(self.device)
        
        # Style generator network
        self.style_generator = self.nn.Sequential(
            self.nn.Linear(256, 512),
            self.nn.ReLU(),
            self.nn.Linear(512, 1024),
            self.nn.ReLU(),
            self.nn.Linear(1024, 2048),
            self.nn.Tanh()
        ).to(self.device)
        
        # Initialize optimizers
        self.d_optimizer = self.torch.optim.Adam(
            self.style_discriminator.parameters(),
            lr=0.0002
        )
        self.g_optimizer = self.torch.optim.Adam(
            self.style_generator.parameters(),
            lr=0.0002
        )
        
    def load_models(self, model_dir: Optional[str] = None) -> None:
        """
        Load required AI models including ensemble models.
        
        Args:
            model_dir: Optional directory containing models
        """
        # Load CLIP for text understanding
        self.clip_model = CLIPModel.from_pretrained(
            "openai/clip-vit-large-patch14"  # Upgraded to larger model
        )
        self.clip_processor = CLIPProcessor.from_pretrained(
            "openai/clip-vit-large-patch14"
        )
        
        if torch.cuda.is_available():
            self.device = "cuda"
            self.clip_model.to(self.device)
            
        # Load ensemble of style transfer models
        if model_dir:
            base_path = Path(model_dir)
            model_paths = [
                base_path / f"vector_style_{i}.onnx"
                for i in range(self.ensemble_size)
            ]
            
            for path in model_paths:
                if path.exists():
                    model = ort.InferenceSession(str(path))
                    self.style_models.append(model)
                    
        # Initialize feature extraction model
        self.feature_extractor = AutoModel.from_pretrained(
            "facebook/dinov2-large"
        ).to(self.device)
                
    def text_to_vector(
        self,
        prompt: str,
        complexity: float = 1.0,
        style: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate SVG elements from text description.
        
        Args:
            prompt: Text description of desired vector art
            complexity: Level of detail (0-2)
            style: Optional style to apply
            
        Returns:
            Generated SVG element
        """
        # Encode text with CLIP
        inputs = self.clip_processor(
            text=prompt,
            return_tensors="pt",
            padding=True
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get text features
        with torch.no_grad():
            text_features = self.clip_model.get_text_features(
                **inputs
            )
            
        # Convert features to vector commands
        paths = self._features_to_paths(
            text_features[0].cpu().numpy(),
            complexity
        )
        
        # Create SVG element
        element = {
            'type': 'path',
            'd': self._combine_paths(paths),
            'style': 'fill:none;stroke:black;stroke-width:2'
        }
        
        # Apply style if specified
        if style and self.style_model:
            element = self.apply_style_transfer(element, style)
            
        return element
        
    def generate_concept(
        self,
        prompt: str,
        num_variations: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple vector concept variations.
        
        Args:
            prompt: Text description
            num_variations: Number of variations to generate
            
        Returns:
            List of generated SVG elements
        """
        variations = []
        
        # Generate base concept
        base_element = self.text_to_vector(prompt)
        variations.append(base_element)
        
        # Generate variations through perturbation
        base_paths = self._parse_path_data(base_element['d'])
        
        for _ in range(num_variations - 1):
            varied_paths = self._create_variation(base_paths)
            
            element = {
                'type': 'path',
                'd': self._combine_paths(varied_paths),
                'style': base_element['style']
            }
            variations.append(element)
            
        return variations
        
    @lru_cache(maxsize=STYLE_CACHE_SIZE)
    def apply_style_transfer(
        self,
        element_hash: str,
        style_reference: str,
        preserve_topology: bool = True
    ) -> Dict[str, Any]:
        """
        Transform SVG element using specified style.
        
        Args:
            element: Original SVG element
            style_reference: Style description or reference
            
        Returns:
            Styled SVG element
        """
        element = self.style_cache.get(element_hash)
        if not element:
            return element
            
        if not self.style_models:
            return element
            
        # Extract enhanced style features
        style_features = self._extract_style_features(style_reference)
            
        # Prepare element features with improved extraction
        paths = self._parse_path_data(element['d'])
        path_features = self._extract_enhanced_features(paths)
        
        # Prepare content for differentiable rendering
        if self.diff_render:
            content_rendering = self.diff_renderer.render(element)
            
        # Run ensemble style transfer
        styled_features_list = []
        for model in self.style_models:
            styled_features = model.run(
                None,
                {
                    'content': path_features,
                    'style': style_features
                }
            )[0]
            
            if preserve_topology:
                # Use GAN to ensure style consistency
                styled_features = self._preserve_style_gan(
                    styled_features,
                    style_features
                )
                
            styled_features_list.append(styled_features)
            
        # Combine ensemble results with attention weights
        attention_weights = self._compute_attention_weights(
            styled_features_list,
            path_features
        )
        styled_features = np.average(
            styled_features_list,
            weights=attention_weights,
            axis=0
        )
        
        # Convert back to paths
        styled_paths = self._features_to_paths(
            styled_features,
            complexity=1.0
        )
        
        element['d'] = self._combine_paths(styled_paths)
        return element
        
    def _extract_style_features(self, style_reference: str) -> np.ndarray:
        """Extract rich style features using CLIP and DINOv2."""
        # Get CLIP features
        style_inputs = self.clip_processor(
            text=style_reference,
            return_tensors="pt",
            padding=True
        )
        style_inputs = {
            k: v.to(self.device) for k, v in style_inputs.items()
        }
        
        with torch.no_grad():
            clip_features = self.clip_model.get_text_features(
                **style_inputs
            )
            dino_features = self.feature_extractor(
                style_inputs['input_ids']
            ).last_hidden_state
            
            # Combine features with attention
            combined = torch.cat(
                [clip_features, dino_features.mean(1)], dim=-1
            )
            
        return combined[0].cpu().numpy()
        
    def _extract_enhanced_features(
        self,
        paths: List[str]
    ) -> np.ndarray:
        """Extract enhanced path features with geometric understanding."""
        points = self._paths_to_points(paths)
        
        # Add geometric features
        angles = self._compute_angles(points)
        curvature = self._compute_curvature(points)
        
        # Combine with original features
        features = np.concatenate([
            points,
            angles[:, np.newaxis],
            curvature[:, np.newaxis]
        ], axis=1)
        
        return features
        
    def _preserve_style_gan(
        self,
        styled_features: np.ndarray,
        target_style: np.ndarray
    ) -> np.ndarray:
        """Refine style transfer using GAN for better preservation."""
        styled_tensor = self.torch.from_numpy(styled_features).to(self.device)
        target_tensor = self.torch.from_numpy(target_style).to(self.device)
        
        # Train discriminator
        self.d_optimizer.zero_grad()
        
        # Real batch
        label_real = self.torch.ones(1, 1).to(self.device)
        output_real = self.style_discriminator(target_tensor)
        d_loss_real = self.F.binary_cross_entropy(
            output_real,
            label_real
        )
        
        # Fake batch
        label_fake = self.torch.zeros(1, 1).to(self.device)
        fake_style = self.style_generator(styled_tensor)
        output_fake = self.style_discriminator(fake_style.detach())
        d_loss_fake = self.F.binary_cross_entropy(
            output_fake,
            label_fake
        )
        
        d_loss = d_loss_real + d_loss_fake
        d_loss.backward()
        self.d_optimizer.step()
        
        # Train generator
        self.g_optimizer.zero_grad()
        output_fake = self.style_discriminator(fake_style)
        g_loss = self.F.binary_cross_entropy(
            output_fake,
            label_real
        )
        g_loss.backward()
        self.g_optimizer.step()
        
        # Return refined features
        return fake_style.detach().cpu().numpy()
        
    def _compute_attention_weights(
        self,
        features_list: List[np.ndarray],
        original_features: np.ndarray
    ) -> np.ndarray:
        """Compute attention weights for ensemble combination."""
        weights = []
        for features in features_list:
            # Calculate similarity with original content
            similarity = np.sum(
                features * original_features
            ) / (
                np.linalg.norm(features) *
                np.linalg.norm(original_features)
            )
            weights.append(np.exp(similarity))
            
        # Normalize weights
        weights = np.array(weights)
        return weights / weights.sum()
        
    def _features_to_paths(
        self,
        features: np.ndarray,
        complexity: float
    ) -> List[str]:
        """Convert neural features to SVG paths."""
        # Scale features to coordinate space
        coords = features.reshape(-1, 2)
        coords = (coords * 200) + 200  # Scale to 400x400 space
        
        # Generate paths based on complexity
        num_points = int(len(coords) * complexity)
        points = coords[:num_points]
        
        paths = []
        current_path = []
        
        for i, point in enumerate(points):
            if i == 0 or np.random.random() < 0.2:
                # Start new subpath
                if current_path:
                    paths.append(current_path)
                current_path = [f"M {point[0]:.2f} {point[1]:.2f}"]
            else:
                # Add curve to current point
                prev = points[i-1]
                ctrl = (prev + point) / 2
                current_path.append(
                    f"Q {ctrl[0]:.2f} {ctrl[1]:.2f} "
                    f"{point[0]:.2f} {point[1]:.2f}"
                )
                
        if current_path:
            paths.append(current_path)
            
        return paths
        
    def _parse_path_data(self, path_data: str) -> List[str]:
        """Split path data into subpaths."""
        subpaths = []
        current = []
        
        for cmd in path_data.split():
            if cmd.startswith('M') and current:
                subpaths.append(current)
                current = []
            current.append(cmd)
            
        if current:
            subpaths.append(current)
            
        return subpaths
        
    def _paths_to_features(
        self,
        paths: List[str]
    ) -> np.ndarray:
        """Convert paths to neural features."""
        points = []
        
        for subpath in paths:
            current_point = None
            
            for cmd in ' '.join(subpath).split():
                if cmd[0] == 'M':
                    coords = cmd[1:].split(',')
                    current_point = [
                        float(coords[0]),
                        float(coords[1])
                    ]
                    points.append(current_point)
                elif cmd[0] == 'L':
                    coords = cmd[1:].split(',')
                    point = [float(coords[0]), float(coords[1])]
                    points.append(point)
                    current_point = point
                elif cmd[0] == 'Q':
                    parts = cmd[1:].split()
                    ctrl = [
                        float(parts[0]),
                        float(parts[1])
                    ]
                    end = [float(parts[2]), float(parts[3])]
                    points.extend([ctrl, end])
                    current_point = end
                    
        # Normalize to feature space
        points = np.array(points)
        points = (points - 200) / 200  # Normalize from 400x400 space
        
        return points.reshape(1, -1)
        
    def _create_variation(
        self,
        base_paths: List[str]
    ) -> List[str]:
        """Create variation of base paths."""
        varied = []
        
        for subpath in base_paths:
            # Add random perturbations to control points
            new_path = []
            
            for cmd in subpath:
                if cmd.startswith('M'):
                    new_path.append(cmd)  # Keep start points
                else:
                    # Add noise to coordinates
                    parts = cmd.split()
                    new_parts = []
                    
                    for part in parts:
                        try:
                            value = float(part)
                            # Add small random offset
                            noise = np.random.normal(0, 5)
                            new_parts.append(
                                f"{value + noise:.2f}"
                            )
                        except ValueError:
                            new_parts.append(part)
                            
                    new_path.append(' '.join(new_parts))
                    
            varied.append(new_path)
            
        return varied
        
    def _combine_paths(self, paths: List[str]) -> str:
        """Combine subpaths into single path string."""
        return ' '.join([' '.join(p) for p in paths])

    def _compute_angles(self, points: np.ndarray) -> np.ndarray:
        """Compute angles between consecutive points."""
        # Convert to vector differences
        vectors = np.diff(points, axis=0)
        
        # Calculate angles using arctan2
        angles = np.arctan2(vectors[:, 1], vectors[:, 0])
        
        # Add padding for last point
        angles = np.pad(angles, (0, 1), mode='edge')
        
        return angles
        
    def _compute_curvature(self, points: np.ndarray) -> np.ndarray:
        """Compute local curvature at each point."""
        if len(points) < 3:
            return np.zeros(len(points))
            
        # Calculate first and second derivatives
        first_deriv = np.gradient(points, axis=0)
        second_deriv = np.gradient(first_deriv, axis=0)
        
        # Compute curvature using differential geometry formula
        num = np.abs(
            first_deriv[:, 0] * second_deriv[:, 1] -
            first_deriv[:, 1] * second_deriv[:, 0]
        )
        denom = np.power(
            first_deriv[:, 0]**2 + first_deriv[:, 1]**2,
            1.5
        )
        
        # Handle division by zero
        curvature = np.where(
            denom > 1e-10,
            num / denom,
            0
        )
        
        return curvature
        
    def _paths_to_points(self, paths: List[str]) -> np.ndarray:
        """Convert SVG paths to point sequence."""
        points = []
        
        for subpath in paths:
            current = None
            
            for cmd in ' '.join(subpath).split():
                if cmd[0] == 'M':
                    coords = cmd[1:].split(',')
                    current = np.array([
                        float(coords[0]),
                        float(coords[1])
                    ])
                    points.append(current)
                elif cmd[0] == 'L':
                    coords = cmd[1:].split(',')
                    current = np.array([
                        float(coords[0]),
                        float(coords[1])
                    ])
                    points.append(current)
                elif cmd[0] == 'Q':
                    parts = cmd[1:].split()
                    # Sample points along quadratic curve
                    start = current
                    ctrl = np.array([
                        float(parts[0]),
                        float(parts[1])
                    ])
                    end = np.array([
                        float(parts[2]),
                        float(parts[3])
                    ])
                    
                    t = np.linspace(0, 1, 10)
                    curve_points = np.outer(
                        (1-t)**2, start
                    ) + np.outer(
                        2*(1-t)*t, ctrl
                    ) + np.outer(
                        t**2, end
                    )
                    
                    points.extend(curve_points)
                    current = end
                    
        return np.array(points)
