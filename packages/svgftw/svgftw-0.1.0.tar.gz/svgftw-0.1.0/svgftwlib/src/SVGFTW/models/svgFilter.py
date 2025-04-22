from xml.etree.ElementTree import Element, SubElement

class SVGFilter:
    def __init__(self, filter_id, x="0", y="0", width="100%", height="100%", 
                filter_units="userSpaceOnUse"):
        self.element = Element('filter', id=filter_id)
        self.element.set('x', x)
        self.element.set('y', y)
        self.element.set('width', width)
        self.element.set('height', height)
        self.element.set('filterUnits', filter_units)
        self._last_result = "SourceGraphic"

    def add_primitive(self, tag, **attrs):
        """Add a raw filter primitive"""
        primitive = SubElement(self.element, tag, **attrs)
        if 'result' in attrs:
            self._last_result = attrs['result']
        return primitive

    def add_blur(self, std_deviation=5, result=None):
        """Add Gaussian blur effect"""
        return self.add_primitive(
            'feGaussianBlur',
            in_=self._last_result,
            stdDeviation=str(std_deviation),
            result=result or f"blur_{std_deviation}"
        )

    def add_drop_shadow(self, dx=5, dy=5, std_deviation=3, 
                       color="black", opacity=0.5, result=None):
        """Add drop shadow using feDropShadow (simpler method)"""
        return self.add_primitive(
            'feDropShadow',
            dx=str(dx),
            dy=str(dy),
            stdDeviation=str(std_deviation),
            flood_color=color,
            flood_opacity=str(opacity),
            result=result or "dropshadow"
        )

    def add_color_matrix(self, matrix_type="matrix", values=None, result=None):
        """Add color matrix transformation"""
        if matrix_type == "matrix" and not values:
            values = [
                1, 0, 0, 0, 0,
                0, 1, 0, 0, 0,
                0, 0, 1, 0, 0,
                0, 0, 0, 1, 0
            ]
        return self.add_primitive(
            'feColorMatrix',
            type=matrix_type,
            values=" ".join(map(str, values)) if values else "",
            in_=self._last_result,
            result=result or "colormatrix"
        )

    def add_offset(self, dx=10, dy=10, result=None):
        """Add positional offset"""
        return self.add_primitive(
            'feOffset',
            dx=str(dx),
            dy=str(dy),
            in_=self._last_result,
            result=result or "offset"
        )

    def add_merge(self, inputs):
        """Merge multiple inputs"""
        merge = self.add_primitive('feMerge')
        for input_name in inputs:
            SubElement(merge, 'feMergeNode', in_=input_name)
        return merge

    def add_legacy_drop_shadow(self):
        """Create drop shadow using multiple primitives (compatibility method)"""
        self.add_offset(dx=5, dy=5, result="offset")
        self.add_blur(std_deviation=3, result="blur")
        self.add_color_matrix(
            values=[
                1, 0, 0, 0, 0,
                0, 1, 0, 0, 0,
                0, 0, 1, 0, 0,
                0, 0, 0, 0.5, 0
            ],
            result="shadow"
        )
        self.add_merge(["shadow", "SourceGraphic"])

# Usage examples
def create_filters():
    # Simple drop shadow filter
    simple_shadow = SVGFilter("simple-shadow")
    simple_shadow.add_drop_shadow()

    # Complex filter chain
    complex_filter = SVGFilter("complex-effect")
    complex_filter.add_blur(2, result="blur1")
    complex_filter.add_offset(10, 10, result="offset1")
    complex_filter.add_color_matrix(
        matrix_type="saturate",
        values=0.5,
        result="desat"
    )
    complex_filter.add_merge(["blur1", "offset1", "desat"])

    # Legacy drop shadow
    legacy_filter = SVGFilter("legacy-shadow")
    legacy_filter.add_legacy_drop_shadow()

    return [simple_shadow.element, complex_filter.element, legacy_filter.element]

# Example SVG document with filters
svg_root = Element('svg', xmlns="http://www.w3.org/2000/svg", viewBox="0 0 400 400")
defs = SubElement(svg_root, 'defs')
for filter_element in create_filters():
    defs.append(filter_element)

# Add sample shape with filter
SubElement(svg_root, 'rect', 
          x="50", y="50", 
          width="100", height="100",
          fill="blue",
          filter="url(#simple-shadow)")

# Output the SVG
from xml.dom import minidom
rough_xml = Element.tostring(svg_root, 'utf-8')
pretty_xml = minidom.parseString(rough_xml).toprettyxml(indent="  ")
print(pretty_xml)
