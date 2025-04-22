"""
SVG path morphing utilities.
Enhanced with path interpolation and bezier curve optimization.
"""

from typing import List, Tuple
import numpy as np
from ..utils.feature_loader import FeatureRegistry, requires_feature

@FeatureRegistry.register('morphing', ['numpy'])
class PathMorpher:
    """Handle SVG path morphing operations."""
    
    def __init__(self, smoothing: float = 0.5):
        """
        Initialize path morpher.
        
        Args:
            smoothing: Smoothing factor for interpolation (0-1)
        """
        self.smoothing = max(0.0, min(1.0, smoothing))
        
    def normalize_points(self, path: str, num_points: int = 100) -> List[Tuple[float, float]]:
        """
        Convert SVG path to normalized point sequence.
        
        Args:
            path: SVG path data
            num_points: Number of points to sample
            
        Returns:
            List of (x, y) coordinates
        """
        # Extract raw points from path
        points = self._extract_path_points(path)
        
        # Calculate total path length
        total_length = 0
        segments = []
        for i in range(len(points) - 1):
            dx = points[i+1][0] - points[i][0]
            dy = points[i+1][1] - points[i][1]
            length = np.sqrt(dx*dx + dy*dy)
            total_length += length
            segments.append(length)
            
        # Normalize segments
        if total_length > 0:
            segments = [s/total_length for s in segments]
            
        # Sample points evenly along path
        normalized = []
        curr_point = points[0]
        curr_segment = 0
        remaining_segment = segments[0]
        
        for i in range(num_points):
            t = i / (num_points - 1)
            
            while t > remaining_segment and curr_segment < len(segments) - 1:
                t -= remaining_segment
                curr_segment += 1
                remaining_segment = segments[curr_segment]
                curr_point = points[curr_segment]
                
            # Interpolate within segment
            if remaining_segment > 0:
                next_point = points[curr_segment + 1]
                factor = t / remaining_segment
                x = curr_point[0] + (next_point[0] - curr_point[0]) * factor
                y = curr_point[1] + (next_point[1] - curr_point[1]) * factor
                normalized.append((x, y))
            else:
                normalized.append(curr_point)
                
        return normalized
        
    def create_morph_sequence(
        self,
        start_path: str,
        end_path: str,
        steps: int = 60
    ) -> List[str]:
        """
        Create sequence of paths morphing from start to end.
        
        Args:
            start_path: Starting SVG path
            end_path: Ending SVG path
            steps: Number of intermediate steps
            
        Returns:
            List of SVG path strings
        """
        normalized_start = self.normalize_points(start_path, 100)
        normalized_end = self.normalize_points(end_path, 100)
        
        morphed_paths = []
        for i in range(steps):
            t = self._smooth_interpolation(i / (steps - 1))
            new_points = []
            
            for p1, p2 in zip(normalized_start, normalized_end):
                x = p1[0] + (p2[0] - p1[0]) * t
                y = p1[1] + (p2[1] - p1[1]) * t
                new_points.append((x, y))
                
            morphed_paths.append(self._points_to_path(new_points))
            
        return morphed_paths
    
    def _smooth_interpolation(self, t: float) -> float:
        """Apply smoothing to interpolation parameter."""
        # Use cubic ease function
        if self.smoothing > 0:
            t = t * (1.0 - self.smoothing) + \
                (3 * t**2 - 2 * t**3) * self.smoothing
        return t
        
    def _extract_path_points(self, path: str) -> List[Tuple[float, float]]:
        """Extract point coordinates from SVG path."""
        points = []
        tokens = path.split()
        i = 0
        
        current_x = 0
        current_y = 0
        
        def parse_float(value: str) -> float:
            """Safely parse float values."""
            try:
                f = float(value)
                if not (isinstance(f, float) and -float('inf') < f < float('inf')):
                    return None
                return f
            except ValueError:
                return None
        
        while i < len(tokens):
            try:
                token = tokens[i]
                command = token.upper()
                is_relative = token != command
                
                if command == 'M':
                    # Move to
                    if i + 2 < len(tokens):
                        x = parse_float(tokens[i+1])
                        y = parse_float(tokens[i+2])
                        if x is None or y is None:
                            i += 1
                            continue
                        if is_relative and points:
                            x += current_x
                            y += current_y
                        points.append((x, y))
                        current_x = x
                        current_y = y
                        i += 3
                    else:
                        i += 1
                elif command == 'L':
                    # Line to
                    if i + 2 < len(tokens):
                        x = parse_float(tokens[i+1])
                        y = parse_float(tokens[i+2])
                        if x is None or y is None:
                            i += 1
                            continue
                        if is_relative:
                            x += current_x
                            y += current_y
                        points.append((x, y))
                        current_x = x
                        current_y = y
                        i += 3
                    else:
                        i += 1
                elif command == 'H':
                    # Horizontal line
                    if i + 1 < len(tokens):
                        x = parse_float(tokens[i+1])
                        if x is None:
                            i += 1
                            continue
                        if is_relative:
                            x += current_x
                        points.append((x, current_y))
                        current_x = x
                        i += 2
                    else:
                        i += 1
                elif command == 'V':
                    # Vertical line
                    if i + 1 < len(tokens):
                        y = parse_float(tokens[i+1])
                        if y is None:
                            i += 1
                            continue
                        if is_relative:
                            y += current_y
                        points.append((current_x, y))
                        current_y = y
                        i += 2
                    else:
                        i += 1
                elif token.upper() in 'CS':
                    # Cubic/smooth cubic bezier - sample points
                    if i + 6 < len(tokens) and token.upper() == 'C':
                        x1 = parse_float(tokens[i+1])
                        y1 = parse_float(tokens[i+2])
                        x2 = parse_float(tokens[i+3])
                        y2 = parse_float(tokens[i+4])
                        x = parse_float(tokens[i+5])
                        y = parse_float(tokens[i+6])
                        
                        if any(v is None for v in [x1, y1, x2, y2, x, y]):
                            i += 1
                            continue
                        
                        # Sample bezier curve
                        for t in np.linspace(0, 1, 10):
                            bx = self._cubic_bezier(
                                current_x, x1, x2, x,
                                t
                            )
                            by = self._cubic_bezier(
                                current_y, y1, y2, y,
                                t
                            )
                            points.append((bx, by))
                            
                        current_x = x
                        current_y = y
                        i += 7
                    else:
                        i += 1
                elif token.upper() == 'Q':
                    # Quadratic bezier
                    if i + 4 < len(tokens):
                        x1 = parse_float(tokens[i+1])
                        y1 = parse_float(tokens[i+2])
                        x = parse_float(tokens[i+3])
                        y = parse_float(tokens[i+4])
                        
                        if any(v is None for v in [x1, y1, x, y]):
                            i += 1
                            continue
                            
                        # Sample bezier curve
                        for t in np.linspace(0, 1, 8):
                            bx = self._quadratic_bezier(
                                current_x, x1, x,
                                t
                            )
                            by = self._quadratic_bezier(
                                current_y, y1, y,
                                t
                            )
                            points.append((bx, by))
                            
                        current_x = x
                        current_y = y
                        i += 5
                    else:
                        i += 1
                elif token.upper() == 'A':
                    # Elliptical arc - simplified to line
                    if i + 7 < len(tokens):
                        x = parse_float(tokens[i+6])
                        y = parse_float(tokens[i+7])
                        if x is None or y is None:
                            i += 1
                            continue
                        points.append((x, y))
                        current_x = x
                        current_y = y
                        i += 8
                    else:
                        i += 1
                elif token.upper() == 'Z':
                    # Close path - connect to first point
                    if points:
                        points.append(points[0])
                    i += 1
                else:
                    i += 1
            except (ValueError, IndexError):
                i += 1
                
        return points
        
    def _points_to_path(self, points: List[Tuple[float, float]]) -> str:
        """Convert point sequence to SVG path data."""
        if not points:
            return ""
            
        path_parts = [f"M {points[0][0]:.3f} {points[0][1]:.3f}"]
        
        for i in range(1, len(points)):
            x, y = points[i]
            path_parts.append(f"L {x:.3f} {y:.3f}")
            
        if points[-1] == points[0]:
            path_parts.append("Z")
            
        return " ".join(path_parts)
        
    def _cubic_bezier(
        self,
        p0: float,
        p1: float,
        p2: float,
        p3: float,
        t: float
    ) -> float:
        """Evaluate cubic bezier curve at parameter t."""
        return ((1-t)**3 * p0 +
                3*(1-t)**2 * t * p1 +
                3*(1-t) * t**2 * p2 +
                t**3 * p3)
                
    def _quadratic_bezier(
        self,
        p0: float,
        p1: float,
        p2: float,
        t: float
    ) -> float:
        """Evaluate quadratic bezier curve at parameter t."""
        return ((1-t)**2 * p0 +
                2*(1-t) * t * p1 +
                t**2 * p2)

# Provide convenience function for simple morphing
def calculate_morph_path(
    start_path: str,
    end_path: str,
    steps: int = 100
) -> List[str]:
    """
    Convenience function to create path morph sequence.
    
    Args:
        start_path: Starting SVG path
        end_path: Ending SVG path
        steps: Number of intermediate steps
        
    Returns:
        List of SVG path strings
    """
    morpher = PathMorpher()
    return morpher.create_morph_sequence(start_path, end_path, steps)
