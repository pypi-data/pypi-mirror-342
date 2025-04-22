import textwrap
from dataclasses import dataclass
from typing import Union

class TextEngine:
    """SVG text engine with multi-line, path, and HTML support"""
    
    @dataclass
    class FontWrapper:
        family: str = "Arial"
        size: int = 12
        weight: str = "normal"
        style: str = "normal"
        
        @property
        def css(self) -> str:
            return f"font-family: {self.family}; font-size: {self.size}px; " \
                   f"font-weight: {self.weight}; font-style: {self.style}"

    def __init__(self, svg_root):
        self.svg = svg_root
        self._current_font = self.FontWrapper()

    def create_text(self, x: float, y: float, content: str, 
                   max_width: float = None, **attrs) -> etree.Element:
        """Create multi-line text element with optional wrapping"""
        text_elem = etree.SubElement(self.svg, 'text', 
                                   {'x': str(x), 'y': str(y), **attrs})
        text_elem.set('style', self._current_font.css)
        
        if max_width:
            lines = self._wrap_text(content, max_width)
            for dy, line in enumerate(lines):
                tspan = etree.SubElement(text_elem, 'tspan',
                                       {'x': str(x), 'dy': f"{1.2 * self._current_font.size}px"})
                tspan.text = line
        else:
            text_elem.text = content
            
        return text_elem

    def create_text_path(self, path_id: str, content: str, 
                        start_offset: float = 0, **attrs) -> etree.Element:
        """Create text following a path"""
        text_elem = etree.SubElement(self.svg, 'text')
        text_path = etree.SubElement(text_elem, 'textPath',
                                   {'href': f"#{path_id}",
                                    'startOffset': str(start_offset),
                                    **attrs})
        text_path.text = content
        return text_elem

    def create_foreign_object(self, x: float, y: float, 
                             width: float, height: float,
                             html_content: str) -> etree.Element:
        """Embed HTML content using foreignObject"""
        nsmap = {None: "http://www.w3.org/2000/svg",
                'xhtml': "http://www.w3.org/1999/xhtml"}
        
        foreign = etree.SubElement(self.svg, 'foreignObject',
                                 {'x': str(x), 'y': str(y),
                                  'width': str(width), 'height': str(height)})
        
        # Add XHTML content with proper namespace
        div = etree.SubElement(foreign, '{http://www.w3.org/1999/xhtml}div')
        div.append(etree.XML(html_content))
        return foreign

    def _wrap_text(self, text: str, max_width: float) -> list:
        """Wrap text based on font metrics"""
        avg_char_width = self._current_font.size * 0.6
        max_chars = int(max_width / avg_char_width)
        
        return textwrap.wrap(text, width=max_chars, 
                            break_long_words=True, 
                            replace_whitespace=False)

    @property
    def font(self) -> FontWrapper:
        return self._current_font
    
    @font.setter
    def font(self, font: FontWrapper):
        self._current_font = font

# Usage Example
svg_root = etree.Element('svg', xmlns="http://www.w3.org/2000/svg", 
                        viewBox="0 0 800 600")

engine = TextEngine(svg_root)

# 1. Multi-line wrapped text
engine.font = TextEngine.FontWrapper(size=14, family="Verdana")
engine.create_text(20, 40, "This is a long text that needs wrapping in SVG", 
                  max_width=200)

# 2. Text on path
path = etree.SubElement(svg_root, 'path', 
                       id="curve", 
                       d="M 100 200 Q 300 50 500 200",
                       fill="none", stroke="black")
engine.create_text_path("curve", "Text flowing along a path", start_offset=50)

# 3. ForeignObject with HTML
html_content = '''
<div xmlns="http://www.w3.org/1999/xhtml" 
     style="background: #f0f0f0; padding: 20px;">
    <h1>HTML in SVG</h1>
    <p>Embedded content with <em>styling</em> and <a href="#">links</a></p>
</div>
'''
engine.create_foreign_object(300, 100, 400, 200, html_content)

# Output SVG
print(etree.tostring(svg_root, pretty_print=True).decode())
