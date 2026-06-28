import re
from textnode import TextNode, TextType

def extract_markdown_images(text: str) -> list[tuple[str,str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[(str,str)]:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result: list[TextNode]  = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            if not node.text.count(delimiter) % 2 == 0:
                raise ValueError("Not valid markdown, missing closing delimiter.")
            in_type = False
            current_node = ""
            i: int = 0
            while i < len(node.text):
                
                if node.text[i:].startswith(delimiter):
                    if in_type:
                        if len(current_node) > 0:
                            new_type_node = TextNode(current_node, text_type)
                            result.append(new_type_node)
                        in_type = False
                    else:
                        if len(current_node) > 0:
                            new_text_node = TextNode(current_node, TextType.TEXT)
                            result.append(new_text_node)
                        in_type = True
                    current_node = ""
                    i+= (len(delimiter))
                else:
                    current_node += node.text[i]
                    i += 1
            if len(current_node) > 0 and not in_type:
                new_text_node = TextNode(current_node, TextType.TEXT)
                result.append(new_text_node)

    return result
   
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    result: list[TextNode] = []
    start_node = TextNode(text, TextType.TEXT)
    result.append(start_node)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_image(result)
    result = split_nodes_link(result)

    return result

def markdown_to_blocks(markdown: str) -> list[str]:
    result: list[str] = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if len(block) > 0:
            result.append(block)
    return result

def parse_title_text(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            text = line.replace("#", "").strip()
            if len(text) > 0:
                return text
    raise ValueError("No title found in markdown")

    
