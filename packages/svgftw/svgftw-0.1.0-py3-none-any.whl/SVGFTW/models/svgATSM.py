import math
import re

class Matrix:
    """2D transformation matrix compliant with SVG specifications"""
    def __init__(self, a=1.0, b=0.0, c=0.0, d=1.0, e=0.0, f=0.0):
        self.components = (float(a), float(b), float(c), 
                          float(d), float(e), float(f))
    
    @property
    def a(self): return self.components[0]
    @property
    def b(self): return self.components[1]
    @property
    def c(self): return self.components[2]
    @property
    def d(self): return self.components[3]
    @property
    def e(self): return self.components[4]
    @property
    def f(self): return self.components[5]

    def __mul__(self, other):
        """Matrix multiplication (concatenation of transformations)"""
        a = self.a * other.a + self.c * other.b
        b = self.b * other.a + self.d * other.b
        c = self.a * other.c + self.c * other.d
        d = self.b * other.c + self.d * other.d
        e = self.a * other.e + self.c * other.f + self.e
        f = self.b * other.e + self.d * other.f + self.f
        return Matrix(a, b, c, d, e, f)

    def transform_point(self, x, y):
        """Apply matrix to a point"""
        return (
            self.a * x + self.c * y + self.e,
            self.b * x + self.d * y + self.f
        )

    @classmethod
    def identity(cls):
        return cls()

    @classmethod
    def translation(cls, tx, ty):
        return cls(1, 0, 0, 1, tx, ty)

    @classmethod
    def scaling(cls, sx, sy=None):
        sy = sx if sy is None else sy
        return cls(sx, 0, 0, sy, 0, 0)

    @classmethod
    def rotation(cls, degrees, cx=0, cy=0):
        θ = math.radians(degrees)
        cosθ = math.cos(θ)
        sinθ = math.sin(θ)
        return cls(
            cosθ, sinθ,
            -sinθ, cosθ,
            -cx * cosθ + cy * sinθ + cx,
            -cx * sinθ - cy * cosθ + cy
        )

    @classmethod
    def skew_x(cls, degrees):
        return cls(1, 0, math.tan(math.radians(degrees)), 1, 0, 0)

    @classmethod
    def skew_y(cls, degrees):
        return cls(1, math.tan(math.radians(degrees)), 0, 1, 0, 0)

    def __str__(self):
        return f"matrix({','.join(map(str, self.components))})"

class Transformable:
    """Mixin class for transformable SVG elements"""
    def __init__(self):
        self.transform = Matrix.identity()
        
    def apply_transform(self, matrix):
        """Apply new transformation matrix"""
        self.transform = matrix * self.transform  # Matrix multiplication order
    
    def translate(self, tx, ty):
        self.apply_transform(Matrix.translation(tx, ty))
    
    def scale(self, sx, sy=None):
        self.apply_transform(Matrix.scaling(sx, sy))
    
    def rotate(self, degrees, cx=0, cy=0):
        self.apply_transform(Matrix.rotation(degrees, cx, cy))
    
    def skew_x(self, degrees):
        self.apply_transform(Matrix.skew_x(degrees))
    
    def skew_y(self, degrees):
        self.apply_transform(Matrix.skew_y(degrees))
    
    def parse_transform(self, transform_str):
        """Parse SVG transform string into matrix"""
        if not transform_str:
            return
        matrix = Matrix.identity()
        for match in re.finditer(r'(\w+)\(([^)]*)\)', transform_str):
            name, args = match.groups()
            values = list(map(float, re.split(r'[\s,]+', args.strip())))
            if name == 'matrix' and len(values) == 6:
                matrix = Matrix(*values) * matrix
            elif name == 'translate':
                tx = values[0]
                ty = values[1] if len(values) > 1 else 0
                matrix = Matrix.translation(tx, ty) * matrix
            elif name == 'scale':
                sx = values[0]
                sy = values[1] if len(values) > 1 else sx
                matrix = Matrix.scaling(sx, sy) * matrix
            elif name == 'rotate':
                angle = values[0]
                cx = values[1] if len(values) > 1 else 0
                cy = values[2] if len(values) > 2 else 0
                matrix = Matrix.rotation(angle, cx, cy) * matrix
            elif name == 'skewX':
                matrix = Matrix.skew_x(values[0]) * matrix
            elif name == 'skewY':
                matrix = Matrix.skew_y(values[0]) * matrix
        self.transform = matrix

class SVGElement(Transformable):
    """Base SVG element with transformation support"""
    def __init__(self, tag, **attrs):
        super().__init__()
        self.tag = tag
        self.attrs = attrs
        if 'transform' in self.attrs:
            self.parse_transform(self.attrs['transform'])
            del self.attrs['transform']
    
    def serialize_transform(self):
        if self.transform.components != (1,0,0,1,0,0):
            return {'transform': str(self.transform)}
        return {}
