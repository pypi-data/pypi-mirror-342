from xml.etree.ElementTree import Element, SubElement

class SVGClipPath:
    def __init__(self, clip_id, clip_path_units='userSpaceOnUse'):
        self.element = Element('clipPath', id=clip_id)
        self.element.set('clipPathUnits', clip_path_units)
        self.shapes = []
    
    def add_shape(self, shape_element):
        """Add a shape to the clipping path"""
        self.shapes.append(shape_element)
        self.element.append(shape_element)
    
    def set_transform(self, transform):
        """Apply transformation to the entire clipPath"""
        self.element.set('transform', transform)
    
    def to_element(self):
        return self.element

class SVGMask:
    def __init__(self, mask_id, 
                x='-10%', y='-10%', width='120%', height='120%',
                mask_units='objectBoundingBox',
                mask_content_units='userSpaceOnUse'):
        self.element = Element('mask', id=mask_id)
        self.element.set('x', x)
        self.element.set('y', y)
        self.element.set('width', width)
        self.element.set('height', height)
        self.element.set('maskUnits', mask_units)
        self.element.set('maskContentUnits', mask_content_units)
        self.content = []
    
    def add_content(self, element):
        """Add elements to define the mask's alpha channel"""
        self.content.append(element)
        self.element.append(element)
    
    def set_gradient_mask(self, gradient_id):
        """Create gradient-based mask (white=opaque, black=transparent)"""
        gradient_rect = Element('rect', 
                               x='0', y='0', 
                               width='100%', height='100%',
                               fill=f"url(#{gradient_id})")
        self.add_content(gradient_rect)
    
    def to_element(self):
        return self.element

class SVGPattern:
    def __init__(self, pattern_id, width, height,
                pattern_units='userSpaceOnUse',
                pattern_content_units='userSpaceOnUse',
                pattern_transform=None):
        self.element = Element('pattern', id=pattern_id)
        self.element.set('width', str(width))
        self.element.set('height', str(height))
        self.element.set('patternUnits', pattern_units)
        self.element.set('patternContentUnits', pattern_content_units)
        
        if pattern_transform:
            self.element.set('patternTransform', pattern_transform)
        
        self.tiles = []
    
    def add_tile(self, tile_element):
        """Add elements to the pattern tile"""
        self.tiles.append(tile_element)
        self.element.append(tile_element)
    
    def create_checkerboard(self, size, color1='#fff', color2='#000'):
        """Generate a checkerboard pattern"""
        self.add_tile(Element('rect', 
                            x='0', y='0', 
                            width=str(size), height=str(size), 
                            fill=color1))
        self.add_tile(Element('rect', 
                            x=str(size), y=str(size), 
                            width=str(size), height=str(size), 
                            fill=color1))
        self.add_tile(Element('rect', 
                            x=str(size), y='0', 
                            width=str(size), height=str(size), 
                            fill=color2))
        self.add_tile(Element('rect', 
                            x='0', y=str(size), 
                            width=str(size), height=str(size), 
                            fill=color2))
        return self
    
    def to_element(self):
        return self.element

# Usage Example
def create_complex_svg():
    # Create SVG root
    svg_root = Element('svg', 
                      xmlns='http://www.w3.org/2000/svg',
                      viewBox='0 0 400 400',
                      width='400',
                      height='400')
    
    # Define section
    defs = SubElement(svg_root, 'defs')
    
    # Create and add clip path
    clip = SVGClipPath('circle-clip')
    clip.add_shape(Element('circle', cx='200', cy='200', r='150'))
    defs.append(clip.to_element())
    
    # Create and add gradient mask
    mask = SVGMask('gradient-mask')
    linear_gradient = Element('linearGradient', id='mask-gradient')
    linear_gradient.append(Element('stop', offset='0%', stop_color='white'))
    linear_gradient.append(Element('stop', offset='100%', stop_color='black'))
    defs.append(linear_gradient)
    mask.set_gradient_mask('mask-gradient')
    defs.append(mask.to_element())
    
    # Create and add pattern
    pattern = SVGPattern('checker', 20, 20)
    pattern.create_checkerboard(10)
    defs.append(pattern.to_element())
    
    # Apply effects
    # Clipped rectangle
    SubElement(svg_root, 'rect',
              x='0', y='0',
              width='400', height='400',
              fill='blue',
              clip_path='url(#circle-clip)')
    
    # Masked image
    image = SubElement(svg_root, 'image',
                      href='example.jpg',
                      x='0', y='0',
                      width='400', height='400',
                      mask='url(#gradient-mask)')
    
    # Pattern-filled shape
    SubElement(svg_root, 'circle',
              cx='200', cy='200',
              r='100',
              fill='url(#checker)')
    
    return svg_root

# Generate SVG XML
import xml.dom.minidom
svg_element = create_complex_svg()
rough_xml = Element.tostring(svg_element, 'utf-8')
pretty_xml = xml.dom.minidom.parseString(rough_xml).toprettyxml(indent="  ")
print(pretty_xml)
