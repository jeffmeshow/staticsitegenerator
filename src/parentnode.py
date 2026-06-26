from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self,
                  tag:str, 
                  children: list[HTMLNode], 
                  props: dict[str, str] = None)->None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag.")
    
        if not self.children:
            raise ValueError("All parent nodes must have at least one child tag.  Otherwise this should be a leaf node.")
        
        result = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children: 
            result += node.to_html()
        result += f"</{self.tag}>"
        
        return result
    