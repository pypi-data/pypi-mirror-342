import requests
from lxml import etree
from tinycss2 import parse_stylesheet
from functools import lru_cache
from urllib.parse import urljoin

class StyleEngine:
    """Handles CSS loading, parsing, and application"""
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.stylesheets = []
        self.cached_styles = {}
        self.specificity_cache = {}

    def add_stylesheet(self, css_source, is_external=False):
        """Load CSS from string, file, or URL"""
        if is_external:
            css_text = self._fetch_external_css(css_source)
        else:
            css_text = css_source
            
        rules = parse_stylesheet(css_text)
        self.stylesheets.extend(rules)

    @lru_cache(maxsize=32)
    def _fetch_external_css(self, url):
        """Fetch and cache external stylesheets"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return ''

    def _match_selector(self, element, selector):
        """Check if element matches CSS selector"""
        # Basic selector matching (expand for complex selectors)
        if selector.startswith('#'):
            return element.attrib.get('id') == selector[1:]
        if selector.startswith('.'):
            return selector[1:] in element.attrib.get('class', '').split()
        return element.tag == selector

    def _calculate_specificity(self, selector):
        """Calculate selector specificity (basic implementation)"""
        if selector in self.specificity_cache:
            return self.specificity_cache[selector]
            
        specificity = [0, 0, 0]
        if '#' in selector: specificity[0] += 1
        if '.' in selector: specificity[1] += 1
        if not selector.startswith(('#', '.')): specificity[2] += 1
        self.specificity_cache[selector] = specificity
        return specificity

    def apply_styles(self, svg_root):
        """Apply all styles to SVG elements"""
        # Process embedded styles
        for style in svg_root.findall('.//{http://www.w3.org/2000/svg}style'):
            self.add_stylesheet(style.text)

        # Process external stylesheets
        for pi in svg_root.xpath('//processing-instruction("xml-stylesheet")'):
            href = pi.text.split('href="')[1].split('"')[0]
            full_url = urljoin(self.base_url, href)
            self.add_stylesheet(full_url, is_external=True)

        # Apply styles in specificity order
        sorted_rules = sorted(
            (rule for rule in self.stylesheets if rule.type == 'qualified-rule'),
            key=lambda r: self._calculate_specificity(r.selector)
        )

        for element in svg_root.iter():
            inline_style = self.parse_inline_style(element)
            styles = inline_style.copy()

            for rule in sorted_rules:
                if self._match_selector(element, rule.selector):
                    for decl in parse_declarations(rule.content):
                        styles[decl.name] = decl.value

            self.apply_style_dict(element, styles)

    @staticmethod
    def parse_inline_style(element):
        """Parse inline style attribute to dictionary"""
        style = element.attrib.get('style', '')
        return dict(
            map(str.strip, decl.split(':', 1))
            for decl in style.split(';') 
            if decl.strip()
        )

    @staticmethod
    def apply_style_dict(element, style_dict):
        """Apply style dictionary to element"""
        style_str = ';'.join(f'{k}:{v}' for k, v in style_dict.items())
        if style_str:
            element.attrib['style'] = style_str
        elif 'style' in element.attrib:
            del element.attrib['style']

def parse_declarations(declarations):
    """Parse CSS declarations from rule content"""
    for token in declarations:
        if token.type == 'declaration':
            yield token

# Usage Example
svg = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <style>
        .shape { fill: blue; }
        #special { stroke-width: 2; }
    </style>
    <circle class="shape" id="special" cx="50" cy="50" r="40"/>
</svg>
'''

engine = StyleEngine()
root = etree.fromstring(svg)
engine.apply_styles(root)

# Resulting SVG will have inline styles combined from CSS and element attributes
print(etree.tostring(root, pretty_print=True).decode())
