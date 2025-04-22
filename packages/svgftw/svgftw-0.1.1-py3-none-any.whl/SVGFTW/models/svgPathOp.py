from svgpathtools import Path, Line, CubicBezier, parse_path
from beziers.path import BezierPath
from beziers.point import Point as BezierPoint
from booleanOperations import BooleanOperationManager
from bezier_interpolation import interpolate
import numpy as np

class SVGOptimizedPath:
    def __init__(self, path_data=None):
        self.segments = []
        if path_data:
            self.load(path_data)
            
    def load(self, path_data):
        """Load SVG path string"""
        svg_path = parse_path(path_data)
        self._convert_from_svgpathtools(svg_path)
        
    def _convert_from_svgpathtools(self, svg_path):
        """Convert svgpathtools Path to internal representation"""
        self.segments = []
        for segment in svg_path:
            if isinstance(segment, CubicBezier):
                self.segments.append({
                    'type': 'CUBIC',
                    'points': [
                        (segment.start.real, segment.start.imag),
                        (segment.control1.real, segment.control1.imag),
                        (segment.control2.real, segment.control2.imag),
                        (segment.end.real, segment.end.imag)
                    ]
                })
            elif isinstance(segment, Line):
                self.segments.append({
                    'type': 'LINE',
                    'points': [
                        (segment.start.real, segment.start.imag),
                        (segment.end.real, segment.end.imag)
                    ]
                })

    def to_bezier_path(self):
        """Convert to beziers.py BezierPath"""
        bpath = BezierPath()
        for seg in self.segments:
            if seg['type'] == 'CUBIC':
                points = [BezierPoint(*p) for p in seg['points']]
                bpath.appendSegment(points)
            elif seg['type'] == 'LINE':
                points = [BezierPoint(*p) for p in seg['points']]
                bpath.appendSegment(points)
        return bpath

    def boolean_operation(self, other, operation='union'):
        """Perform boolean operations using booleanOperations"""
        manager = BooleanOperationManager()
        # Convert to booleanOperations compatible format
        contours = self._to_boolean_contours()
        other_contours = other._to_boolean_contours()
        
        result = []
        def _pen(point, segment_type=None):
            result.append((point[0], point[1]))
            
        if operation == 'union':
            manager.union(contours, _pen)
        elif operation == 'difference':
            manager.difference(contours, other_contours, _pen)
        elif operation == 'intersection':
            manager.intersection(contours, other_contours, _pen)
        elif operation == 'xor':
            manager.xor(contours, other_contours, _pen)
            
        return self._reconstruct_from_points(result)

    def simplify(self, tolerance=0.1):
        """Simplify path using Ramer-Douglas-Peucker algorithm"""
        points = self.get_points()
        if len(points) < 3:
            return self
            
        mask = self._rd_mask(points, tolerance)
        simplified = [points[i] for i in range(len(points)) if mask[i]]
        return self._reconstruct_from_points(simplified)

    def smooth(self, iterations=3):
        """Smooth path using bezier-interpolation"""
        points = self.get_points()
        if len(points) < 4:
            return self
            
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        t = np.linspace(0, 1, len(x))
        
        # Use cubic Bézier interpolation
        interp_points = interpolate(x, y, t, kind='cubic')
        return self._reconstruct_from_points(interp_points)

    def offset(self, distance):
        """Offset path using beziers.py"""
        bpath = self.to_bezier_path()
        bpath.offset(distance)
        return self._convert_from_beziers(bpath)

    def _convert_from_beziers(self, bpath):
        """Convert from beziers.py BezierPath"""
        self.segments = []
        for segment in bpath.asSegments():
            points = [(p.x, p.y) for p in segment]
            if len(points) == 4:
                self.segments.append({'type': 'CUBIC', 'points': points})
            elif len(points) == 2:
                self.segments.append({'type': 'LINE', 'points': points})
        return self

    def _reconstruct_from_points(self, points):
        """Reconstruct path from point list"""
        # Implement smart segment reconstruction logic
        # (This would use bezier-interpolation for smooth reconstruction)
        pass

    def get_points(self, num=100):
        """Sample points along path"""
        # Implementation using svgpathtools
        pass

    def _rd_mask(self, points, epsilon):
        """Ramer-Douglas-Peucker algorithm implementation"""
        # Recursive simplification logic
        pass

    def _to_boolean_contours(self):
        """Convert to booleanOperations compatible contours"""
        # Implementation details for contour conversion
        pass

    def d(self):
        """Export as SVG path string"""
        path = Path()
        for seg in self.segments:
            if seg['type'] == 'CUBIC':
                start = complex(*seg['points'][0])
                c1 = complex(*seg['points'][1])
                c2 = complex(*seg['points'][2])
                end = complex(*seg['points'][3])
                path.append(CubicBezier(start, c1, c2, end))
            elif seg['type'] == 'LINE':
                start = complex(*seg['points'][0])
                end = complex(*seg['points'][1])
                path.append(Line(start, end))
        return path.d()
