from IPython.display import display, clear_output
import drawsvg as draw
from drawsvg.widgets import DrawingWidget, AsyncAnimation
import ipywidgets as widgets
import time

class LiveCodingSVG:
    def __init__(self, width=600, height=400):
        self.dwg = draw.Drawing(width, height)
        self.widget = DrawingWidget(width, height)
        self.params = {}
        self.animation = None
        
    def _redraw(self):
        """Force redraw of the SVG canvas"""
        self.widget.set_drawing(self.dwg)
        
    def add_element(self, element_type, **kwargs):
        """Add elements dynamically using method chaining"""
        elem = getattr(draw, element_type)(**kwargs)
        self.dwg.append(elem)
        self._redraw()
        return self
        
    def live_animation(self, fps=30):
        """Create frame-based animation that updates in real-time"""
        self.animation = AsyncAnimation(fps=fps)
        display(self.animation)
        return self.animation
        
    def interactive_session(self):
        """Start interactive session with parameter controls"""
        param_box = widgets.HBox([])
        display(widgets.VBox([self.widget, param_box]))
        
        def update_param(name, value):
            self.params[name] = value
            self._redraw()
            
        return update_param
    
    def code_cell_demo(self):
        """Demo live coding workflow between cells"""
        output = widgets.Output()
        display(output)
        
        with output:
            self._redraw()
            display(self.widget)
            
        return output

# Usage Example 1: Basic interactive session
live_svg = LiveCodingSVG()
live_svg.add_element('Circle', cx=100, cy=100, r=50, fill='red')
live_svg.interactive_session()

# In subsequent cells, modify elements dynamically:
# live_svg.add_element('Rectangle', x=200, y=200, width=100, height=50, fill='blue')
# live_svg.dwg.elements[0].fill = 'green'  # Modify existing element
# live_svg._redraw()

# Usage Example 2: Parameter-driven animation
anim = LiveCodingSVG().live_animation(fps=60)

@anim.set_draw_frame
def draw_frame(t):
    dwg = draw.Drawing(600, 400)
    dwg.append(draw.Circle(300 + 100*t, 200, 50, fill='hsl(%.0f,80%%,50%%)' % (t*360)))
    return dwg

# Usage Example 3: Physics simulation
physics_svg = LiveCodingSVG()
update_params = physics_svg.interactive_session()

class Ball:
    def __init__(self):
        self.x = 300
        self.y = 50
        self.vy = 0
        
ball = Ball()

def physics_step():
    ball.vy += 0.5  # Gravity
    ball.y += ball.vy
    if ball.y > 350:
        ball.y = 350
        ball.vy *= -0.8  # Bounce
        
    physics_svg.dwg.elements = []  # Clear previous frame
    physics_svg.add_element('Circle', cx=ball.x, cy=ball.y, r=20, fill='purple')
    physics_svg.add_element('Rectangle', x=0, y=360, width=600, height=40, fill='gray')
    
# Run in a cell to animate:
# from IPython.display import display, clear_output
# while True:
#     physics_step()
#     physics_svg._redraw()
#     time.sleep(0.016)
