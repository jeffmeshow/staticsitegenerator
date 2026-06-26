from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self,
                  tag:str, 
                  value:str, 
                  props: dict[str, str] = None)->None:
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self) -> str:
        if not self.value or self.value == "":
            raise ValueError("All leaf nodes must have a value.")
        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return self.value
    
    def __repr__(self):
        print(f"tag: {self.tag} value: {self.value} props: {self.props_to_html()}")