from enum import Enum
from src.htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"           # Normal text
    BOLD = "bold"           # **Bold text**
    ITALIC = "italic"       # _Italic text_
    CODE = "code"           # `Code text`
    LINK = "link"           # [anchor text](url)
    IMAGE = "image"         # ![alt text](url)
    
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        # First check if other is an instance of TextNode
        if not isinstance(other, TextNode):
            return False
        
        # Then check if all properties are equal
        return (
            self.text == other.text and 
            self.text_type == other.text_type and 
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text)
        elif text_node.text_type == TextType.LINK:
            # For links, we need the href prop
            return LeafNode("a", text_node.text, {"href": text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            # For images, we need src and alt props
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        else:
            raise Exception(f"Invalid text type: {text_node.text_type}")
