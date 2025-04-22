import bisect
from dataclasses import dataclass
from enum import Enum
from xml.etree.ElementTree import Element, SubElement

class Easing(Enum):
    LINEAR = "linear"
    EASE_IN = "ease-in"
    EASE_OUT = "ease-out"
    EASE_IN_OUT = "ease-in-out"
    
    @staticmethod
    def cubic_bezier(x1: float, y1: float, x2: float, y2: float) -> str:
        return f"cubic-bezier({x1},{y1},{x2},{y2})"

@dataclass
class Keyframe:
    time: float  # 0-1 for CSS, seconds for SMIL
    value: str
    easing: str = Easing.LINEAR.value

class Animation:
    def __init__(self, element, attribute, duration=1, delay=0, 
                repeat="indefinite", timeline=None):
        self.element = element
        self.attribute = attribute
        self.duration = duration
        self.delay = delay
        self.repeat = repeat
        self.keyframes = []
        self.timeline = timeline

    def add_keyframe(self, time: float, value: str, easing=Easing.LINEAR):
        key = Keyframe(time, value, easing.value)
        bisect.insort(self.keyframes, key, key=lambda k: k.time)
        return self

    def to_smil(self):
        """Generate SMIL animation elements"""
        animate = Element('animate', attrib={
            'attributeName': self.attribute,
            'dur': f"{self.duration}s",
            'begin': f"{self.delay}s",
            'repeatCount': str(self.repeat),
            'calcMode': 'spline',
            'keyTimes': ';'.join(str(k.time/self.duration) for k in self.keyframes),
            'keySplines': ';'.join(k.easing for k in self.keyframes),
            'values': ';'.join(k.value for k in self.keyframes)
        })
        return [animate]

    def to_css(self):
        """Generate CSS animation styles"""
        anim_name = f"anim_{id(self)}"
        keyframes = [
            f"{k.time*100}% {{ {self.attribute}: {k.value}; "
            f"animation-timing-function: {k.easing}; }}"
            for k in self.keyframes
        ]
        return f"""
        @keyframes {anim_name} {{
            {''.join(keyframes)}
        }}
        #{self.element.attrib['id']} {{
            animation: {anim_name} {self.duration}s {self.delay}s {self.repeat};
        }}
        """

class Timeline:
    def __init__(self):
        self.animations = []
        self.current_time = 0

    def add_animation(self, animation: Animation, offset=0):
        animation.delay = self.current_time + offset
        self.animations.append(animation)
        return self

    def create_sequence(self):
        """Chain animations in sequence"""
        self.current_time = max(a.delay + a.duration for a in self.animations)
        return self

    def apply(self, method='smil'):
        """Apply animations to elements using specified method"""
        results = []
        for anim in self.animations:
            if method == 'smil':
                results.extend(anim.to_smil())
            elif method == 'css':
                results.append(anim.to_css())
        return results

# Usage Example
svg_root = Element('svg', xmlns="http://www.w3.org/2000/svg", 
                  viewBox="0 0 400 400", width="400", height="400")

# Create animated circle
circle = SubElement(svg_root, 'circle', 
                   id="circle1", cx="50", cy="50", r="40", fill="blue")

# Create timeline
tl = Timeline()

# Position animation
pos_anim = Animation(circle, 'cx', duration=3)
pos_anim.add_keyframe(0, '50', Easing.EASE_IN_OUT)
pos_anim.add_keyframe(1, '350', Easing.cubic_bezier(0.68, -0.55, 0.27, 1.55))
tl.add_animation(pos_anim)

# Color animation
color_anim = Animation(circle, 'fill', duration=3)
color_anim.add_keyframe(0, 'blue')
color_anim.add_keyframe(1, 'red')
tl.add_animation(color_anim, offset=0.5)

# Apply SMIL animations
for anim_element in tl.apply('smil'):
    circle.extend(anim_element)

# Apply CSS animations (alternative method)
style = SubElement(svg_root, 'style')
style.text = '\n'.join(tl.apply('css'))

# Output the SVG
from xml.dom import minidom
rough_xml = Element.tostring(svg_root, 'utf-8')
pretty_xml = minidom.parseString(rough_xml).toprettyxml(indent="  ")
print(pretty_xml)
