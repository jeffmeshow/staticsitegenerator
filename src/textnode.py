from __future__ import annotations
from leafnode import LeafNode
from enum import Enum

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    LINK = "link"
    IMAGE = "image"
    CODE = "code"

class TextNode:

    def __init__(self, text:str, text_type:TextType, url:str = None)->None:
        self.text = text
        self.text_type = text_type
        self.url = url

        if text_type in {TextType.TEXT, TextType.BOLD, TextType.ITALIC} and text == "":
            raise ValueError("Text required for TEXT, BOLD, and ITALIC types")

        if text_type in {TextType.LINK, TextType.IMAGE} and url is None:
            raise ValueError("URL required for LINK or IMAGE")
        
    def __eq__(self, other):
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    t = text_node.text_type
    if t == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif t == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif t == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif t == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif t == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif t == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Invalid Text Type")