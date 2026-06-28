from __future__ import annotations
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from parsemarkdown import markdown_to_blocks, text_to_textnodes
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block: str) -> BlockType:

    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("-"):
        return BlockType.UNORDERED_LIST
    elif block.startswith("1."):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    

def markdown_to_html_node(markdown: str) -> HTMLNode:
    html: HTMLNode = ParentNode("div", [])

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        blocktype = block_to_block_type(block)
        
        child_node: HTMLNode
        if blocktype == BlockType.PARAGRAPH:
            block = block.replace("\n", " ") #remove new lines for para blocks
            block = block.replace("  ", " ") #replace double spaces with one
            html.children.append(make_parent_or_leaf("p", block))
        elif blocktype == BlockType.CODE:
            code_node= LeafNode("code", block.split("```")[1].lstrip())
            pre_node = ParentNode("pre", [code_node])
            html.children.append(pre_node)
        elif blocktype == BlockType.QUOTE:
            text = block.split(">")[1].lstrip()
            html.children.append(make_parent_or_leaf("blockquote", text))
        elif blocktype == BlockType.ORDERED_LIST:
            list_node = ParentNode("ol", [])
            lines = block.split("\n")
            for line in lines:
                dot_index = line.index(".")
                text = line[dot_index + 2:]
                list_node.children.append(make_parent_or_leaf("li", text))
            html.children.append(list_node)
        elif blocktype == BlockType.UNORDERED_LIST:
            list_node = ParentNode("ul", [])
            lines = block.split("\n")
            for line in lines:
                text = line[2:]
                list_node.children.append(make_parent_or_leaf("li", text))
            html.children.append(list_node)
        elif blocktype == BlockType.HEADING:
            header_node = header_block_to_node(block)
            html.children.append(header_node)

    return html

def make_parent_or_leaf(tag: str, text: str)->HTMLNode:
    children: list[HTMLNode] = text_to_children(text)
    if len(children) > 0:
        return ParentNode(tag, children)
    else:
        return LeafNode(tag, text)
        

def text_to_children(text: str)-> list[HTMLNode]:
    html_nodes: list[HTMLNode] = []
    text_nodes: list[TextNode] = text_to_textnodes(text)

    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    
    return html_nodes

def header_block_to_node(markdown: str) -> LeafNode:
    count = markdown.count("#")
    if count >= 1 and count <= 6:
        text = markdown.replace("#", "").strip()
        if len(text) > 0:
            return LeafNode("h" + str(count), text)
    raise ValueError(f"Invalid header: {markdown}")

        

