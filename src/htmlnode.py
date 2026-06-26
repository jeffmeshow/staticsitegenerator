from __future__ import annotations

class HTMLNode:

    def __init__(self, tag:str = None, value:str = None, children: list[HTMLNode] | None = None, props: dict[str, str] = None)->None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parent nodes must have a tag.")
    
        if not self.children:
            raise ValueError("All parent nodes must have at least one child tag.  Otherwise this should be a leaf node.")
        
        result = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children: 
            result += node.to_html()
        result += f"</{self.tag}>"
    
    def props_to_html(self) -> str:
        result = ""
        if not self.props:
            return result
        for key in self.props:
            result += f' {key}="{self.props[key]}"'
        return result
    
    def children_to_string(self):
        result = "Children:"
        for child in self.children:
            result += f" {child.tag}[{child.value}]"
        return result

    def __repr__(self):
        print(f"tag: {self.tag} value: {self.value} props: {self.props_to_html()} children: {self.children_to_string()}")