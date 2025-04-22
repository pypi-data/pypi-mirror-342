from dataclasses import dataclass
from xml.etree.ElementTree import Element, SubElement

@dataclass
class PedalboardEffect:
    name: str
    params: dict
    input: str = "SourceGraphic"
    result: str = None

class SVGPedalboard:
    def __init__(self, filter_id):
        self.filter_id = filter_id
        self.effects = []
        self._last_result = "SourceGraphic"
        
    def add_effect(self, effect_type, **params):
        """Add a filter effect to the chain"""
        effect = PedalboardEffect(
            name=effect_type,
            params=params,
            input=self._last_result,
            result=f"{effect_type}_{len(self.effects)}"
        )
        self.effects.append(effect)
        self._last_result = effect.result
        return self  # Enable method chaining
    
    def add_custom_glsl(self, code):
        """Add custom GLSL shader effect (where supported)"""
        return self.add_effect(
            "feCustom",
            shader=code,
            type="fragment",
            result="customShader"
        )
    
    def to_svg(self):
        """Generate SVG filter element with effect chain"""
        filter_elem = Element('filter', id=self.filter_id)
        
        for idx, effect in enumerate(self.effects):
            elem = SubElement(filter_elem, effect.name)
            elem.attrib['in'] = effect.input
            elem.attrib['result'] = effect.result
            
            # Handle special cases
            if effect.name == 'feConvolveMatrix':
                elem.attrib['kernelMatrix'] = ' '.join(map(str, effect.params['matrix']))
            elif effect.name == 'feColorMatrix':
                self._handle_color_matrix(elem, effect.params)
            else:
                elem.attrib.update({k: str(v) for k, v in effect.params.items()})
                
        # Final merge if needed
        if len(self.effects) > 1:
            merge = SubElement(filter_elem, 'feMerge')
            SubElement(merge, 'feMergeNode', **{'in': self._last_result})
            SubElement(merge, 'feMergeNode', **{'in': "SourceGraphic"})
            
        return filter_elem
    
    def _handle_color_matrix(self, elem, params):
        matrix = params.get('values')
        if matrix and len(matrix) == 20:
            elem.attrib['values'] = ' '.join(map(str, matrix))
        elif params.get('type') in ['hueRotate', 'saturate']:
            elem.attrib['values'] = str(params['value'])
            
    @staticmethod
    def create_chain(*effects):
        """Create complex chains from predefined effects"""
        pb = SVGPedalboard("effect-chain")
        for effect in effects:
            pb.add_effect(**effect)
        return pb

# Example usage
chain = (SVGPedalboard("pedalboard-1")
         .add_effect('feGaussianBlur', stdDeviation=2)
         .add_effect('feColorMatrix', 
                    type='matrix',
                    values=[0.33, 0.33, 0.33, 0, 0,
                            0.33, 0.33, 0.33, 0, 0,
                            0.33, 0.33, 0.33, 0, 0,
                            0, 0, 0, 1, 0])
         .add_effect('feConvolveMatrix', 
                    matrix=[0, 1, 0, 
                            1, -4, 1, 
                            0, 1, 0],
                    order=3)
         .add_custom_glsl("""
             void main(void) {
                 vec4 color = texture2D(in, coord);
                 color.rgb = 1.0 - color.rgb;
                 gl_FragColor = color;
             }
         """))

# Generate SVG output
svg_filter = chain.to_svg()
