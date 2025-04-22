import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLParser
import re

class CommentedTreeBuilder(XMLParser):
    """XML parser that preserves comments and processing instructions"""
    def __init__(self, target=None):
        super().__init__(target=target)
        self._parser.CommentHandler = self.handle_comment
        self._parser.ProcessingInstructionHandler = self.handle_pi
        self._comments = []
        self._processing_instructions = []

    def handle_comment(self, data):
        self._comments.append(ET.Comment(data))
        
    def handle_pi(self, target, data):
        self._processing_instructions.append(ET.ProcessingInstruction(target, data))

    def close(self):
        super().close()
        return self._comments, self._processing_instructions

def parse_svg(filename):
    """Parse SVG with comments and processing instructions"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract XML declaration and DOCTYPE
    xml_decl = re.search(r'^<\?xml.*?\?>', content)
    doctype = re.search(r'<!DOCTYPE.*?>', content)
    
    # Create parser and parse content
    parser = CommentedTreeBuilder()
    root = ET.fromstring(content, parser=parser)
    comments, processing_instructions = parser.close()
    
    # Store metadata in element tree
    tree = ET.ElementTree(root)
    tree._comments = comments
    tree._processing_instructions = processing_instructions
    tree._xml_declaration = xml_decl.group(0) if xml_decl else None
    tree._doctype = doctype.group(0) if doctype else None
    
    # Register namespaces from root element
    namespaces = {k:v for k, v in root.attrib.items() if k.startswith('xmlns')}
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix.split(':')[-1] if ':' in prefix else '', uri)
    
    return tree

def save_svg(tree, filename):
    """Save SVG with preserved comments and namespaces"""
    root = tree.getroot()
    
    # Write to string
    root_str = ET.tostring(root, encoding='utf-8', xml_declaration=False).decode()
    
    # Reconstruct original structure
    parts = []
    if tree._xml_declaration:
        parts.append(tree._xml_declaration + "\n")
    if tree._doctype:
        parts.append(tree._doctype + "\n")
    
    # Add processing instructions
    for pi in tree._processing_instructions:
        parts.append(f"<?{pi.target} {pi.text}?>\n")
    
    # Add comments
    for comment in tree._comments:
        parts.append(f"<!--{comment.text}-->\n")
    
    # Add root element
    parts.append(root_str)
    
    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(''.join(parts))
