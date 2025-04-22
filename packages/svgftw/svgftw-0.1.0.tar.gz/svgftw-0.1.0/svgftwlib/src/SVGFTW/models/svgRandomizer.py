import drawsvg as draw
import random
import math
import colorsys
import argparse
from datetime import datetime

class SVGRandomizer:
    """
    A class to generate random SVG shapes with customizable properties.
    """
    
    def __init__(self, width=800, height=600, background_color=None):
        """
        Initialize the SVG randomizer.
        
        Args:
            width (int): Width of the SVG canvas in pixels
            height (int): Height of the SVG canvas in pixels
            background_color (str): Background color of the SVG
        """
        self.width = width
        self.height = height
        self.background_color = background_color
        self.drawing = draw.Drawing(width, height, origin=(0, 0))
        
        # Add background if specified
        if background_color:
            self.drawing.append(draw.Rectangle(0, 0, width, height, fill=background_color))
    
    def random_color(self, opacity=1.0, pastel=False):
        """
        Generate a random color.
        
        Args:
            opacity (float): Opacity value between 0 and 1
            pastel (bool): If True, generates pastel colors
            
        Returns:
            str: Color in rgb format
        """
        if pastel:
            h = random.random()
            s = random.uniform(0.3, 0.7)
            l = random.uniform(0.7, 0.9)
            r, g, b = [int(255 * c) for c in colorsys.hls_to_rgb(h, l, s)]
        else:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
        
        return f"rgb({r},{g},{b},{opacity})"
    
    def add_random_circle(self, min_radius=10, max_radius=100, fill=True, stroke=True, opacity=None):
        """
        Add a random circle to the drawing.
        """
        cx = random.uniform(0, self.width)
        cy = random.uniform(0, self.height)
        radius = random.uniform(min_radius, max_radius)
        
        fill_color = self.random_color(opacity if opacity else random.uniform(0.3, 1.0)) if fill else 'none'
        stroke_color = self.random_color() if stroke else 'none'
        stroke_width = random.uniform(1, 5) if stroke else 0
        
        circle = draw.Circle(cx, cy, radius, 
                          fill=fill_color, 
                          stroke=stroke_color, 
                          stroke_width=stroke_width)
        self.drawing.append(circle)
        return circle
    
    def add_random_rectangle(self, min_size=10, max_size=100, fill=True, stroke=True, opacity=None):
        """
        Add a random rectangle to the drawing.
        """
        x = random.uniform(0, self.width - max_size)
        y = random.uniform(0, self.height - max_size)
        width = random.uniform(min_size, max_size)
        height = random.uniform(min_size, max_size)
        
        fill_color = self.random_color(opacity if opacity else random.uniform(0.3, 1.0)) if fill else 'none'
        stroke_color = self.random_color() if stroke else 'none'
        stroke_width = random.uniform(1, 5) if stroke else 0
        
        # Randomly decide if we want rounded corners
        rx = random.uniform(0, 20) if random.random() > 0.5 else 0
        
        rect = draw.Rectangle(x, y, width, height, 
                           fill=fill_color, 
                           stroke=stroke_color,
                           stroke_width=stroke_width,
                           rx=rx, ry=rx)
        self.drawing.append(rect)
        return rect
    
    def add_random_ellipse(self, min_radius=10, max_radius=100, fill=True, stroke=True, opacity=None):
        """
        Add a random ellipse to the drawing.
        """
        cx = random.uniform(0, self.width)
        cy = random.uniform(0, self.height)
        rx = random.uniform(min_radius, max_radius)
        ry = random.uniform(min_radius, max_radius)
        
        fill_color = self.random_color(opacity if opacity else random.uniform(0.3, 1.0)) if fill else 'none'
        stroke_color = self.random_color() if stroke else 'none'
        stroke_width = random.uniform(1, 5) if stroke else 0
        
        ellipse = draw.Ellipse(cx, cy, rx, ry, 
                            fill=fill_color, 
                            stroke=stroke_color, 
                            stroke_width=stroke_width)
        self.drawing.append(ellipse)
        return ellipse
    
    def add_random_polygon(self, vertices=None, min_vertices=3, max_vertices=8, 
                         min_radius=50, max_radius=150, fill=True, stroke=True, opacity=None):
        """
        Add a random polygon to the drawing.
        """
        if vertices is None:
            vertices = random.randint(min_vertices, max_vertices)
        
        # Generate polygon centered in the canvas with random rotation
        cx = random.uniform(max_radius, self.width - max_radius)
        cy = random.uniform(max_radius, self.height - max_radius)
        
        points = []
        for i in range(vertices):
            angle = 2 * math.pi * i / vertices
            radius = random.uniform(min_radius, max_radius)
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append((x, y))
        
        fill_color = self.random_color(opacity if opacity else random.uniform(0.3, 1.0)) if fill else 'none'
        stroke_color = self.random_color() if stroke else 'none'
        stroke_width = random.uniform(1, 5) if stroke else 0
        
        polygon = draw.Lines(*[coord for point in points for coord in point], 
                           close=True,
                           fill=fill_color, 
                           stroke=stroke_color, 
                           stroke_width=stroke_width)
        self.drawing.append(polygon)
        return polygon
    
    def add_random_line(self, min_length=50, max_length=200, curved=False):
        """
        Add a random line to the drawing.
        """
        x1 = random.uniform(0, self.width)
        y1 = random.uniform(0, self.height)
        
        if curved:
            # Create a curved line with random control points
            points = [(x1, y1)]
            for _ in range(random.randint(1, 3)):
                x2 = min(max(0, x1 + random.uniform(-max_length, max_length)), self.width)
                y2 = min(max(0, y1 + random.uniform(-max_length, max_length)), self.height)
                points.append((x2, y2))
                x1, y1 = x2, y2
            
            stroke_color = self.random_color()
            stroke_width = random.uniform(1, 8)
            
            line = draw.Lines(*[coord for point in points for coord in point],
                           close=False,
                           fill='none',
                           stroke=stroke_color,
                           stroke_width=stroke_width)
        else:
            # Create a straight line
            length = random.uniform(min_length, max_length)
            angle = random.uniform(0, 2 * math.pi)
            x2 = min(max(0, x1 + length * math.cos(angle)), self.width)
            y2 = min(max(0, y1 + length * math.sin(angle)), self.height)
            
            stroke_color = self.random_color()
            stroke_width = random.uniform(1, 8)
            
            line = draw.Line(x1, y1, x2, y2,
                          stroke=stroke_color,
                          stroke_width=stroke_width)
        
        self.drawing.append(line)
        return line
    
    def generate_random_shapes(self, num_shapes=10):
        """
        Generate a specified number of random shapes.
        
        Args:
            num_shapes (int): Number of shapes to generate
        """
        shape_functions = [
            self.add_random_circle,
            self.add_random_rectangle,
            self.add_random_ellipse,
            self.add_random_polygon,
            self.add_random_line
        ]
        
        for _ in range(num_shapes):
            # Choose a random shape function and execute it
            func = random.choice(shape_functions)
            func()
    
    def save(self, filename=None):
        """
        Save the SVG to a file.
        
        Args:
            filename (str): Filename to save to. If None, a timestamp is used.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"random_svg_{timestamp}.svg"
        
        self.drawing.save_svg(filename)
        return filename


def main():
    """Main function to run the SVG randomizer from command line."""
    parser = argparse.ArgumentParser(description="Generate random SVG shapes")
    parser.add_argument("--width", type=int, default=800, help="Width of the SVG canvas")
    parser.add_argument("--height", type=int, default=600, help="Height of the SVG canvas")
    parser.add_argument("--bg", type=str, default=None, help="Background color")
    parser.add_argument("--shapes", type=int, default=10, help="Number of shapes to generate")
    parser.add_argument("--output", type=str, default=None, help="Output filename")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    
    args = parser.parse_args()
    
    # Set random seed if specified
    if args.seed is not None:
        random.seed(args.seed)
    
    # Create and use the randomizer
    randomizer = SVGRandomizer(width=args.width, height=args.height, background_color=args.bg)
    randomizer.generate_random_shapes(num_shapes=args.shapes)
    filename = randomizer.save(args.output)
    
    print(f"SVG saved to {filename}")


if __name__ == "__main__":
    main()
