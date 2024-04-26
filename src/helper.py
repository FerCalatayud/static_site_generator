from htmlnode import LeafNode
from enum import Enum

class TextNodeType(Enum):
    TEXT = "txt"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextNodeType.TEXT:
        return LeafNode(text_node.text)
    elif text_node.text_type == TextNodeType.BOLD:
        return LeafNode(text_node.text, tag="b")
    elif text_node.text_type == TextNodeType.ITALIC:
        return LeafNode(text_node.text, tag="i")
    elif text_node.text_type == TextNodeType.CODE:
        return LeafNode(text_node.text, tag="code")
    elif text_node.text_type == TextNodeType.LINK:
        return LeafNode(text_node.text, tag="a", props={"href": text_node.url})
    elif text_node.text_type == TextNodeType.IMAGE:
        return LeafNode("", tag="img", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Text Node has no type")