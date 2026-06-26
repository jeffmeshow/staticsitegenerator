import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_create_node(self):
        node = HTMLNode(tag="p", value="This is a paragraph", children=None, props={"style": "color='red'"})
        
        assert node.tag == "p"
        assert node.value == "This is a paragraph"
        assert node.children == None
        assert node.props["style"] == "color='red'"

    def test_cprops(self):
        node = HTMLNode(tag="p", value="This is a paragraph", children=None, props={"style": "color='red'", "font-size": "16px"})
        
        assert len(node.props.keys()) == 2
        assert node.props["font-size"] == "16px"
        assert node.props["style"] == "color='red'"

    def test_create_children(self):

        child1 = HTMLNode(tag="p", value="This is a child p1", children=None, props=None)
        child2 = HTMLNode(tag="p", value="This is a child p2", children=None, props=None)
        node = HTMLNode(tag="div", value="This is parent div", children=[child1,child2], props=None)

        assert node.tag == "div"
        assert len(node.children) == 2
        assert node.children[0].tag == "p"
        assert "Children: p[This is a child p1]" in node.children_to_string()