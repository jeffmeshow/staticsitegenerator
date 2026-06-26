import unittest
from leafnode import LeafNode
from textnode import TextNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_create_node(self):
        node = ParentNode("p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                            ],  
                            props={"style": "color='red'"})
        assert node.tag == "p"
        assert node.value is None
        assert len(node.children) == 4
        assert node.children[2].tag == "i"
        assert node.children[2].value == "italic text"
        assert node.props["style"] == "color='red'"

    def test_to_html_basic(self):
        node = ParentNode("p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                            ],  
                            props={"size": "12px"})
        result = node.to_html()
        assert result == '<p size="12px"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'

    def test_to_html_nested(self):
        node = ParentNode("div",
                            [
                                ParentNode("p", 
                                            [
                                            LeafNode(None, "Normal text"),
                                            LeafNode("i", "italic text"),
                                            LeafNode(None, "Normal text"),
                                            ]),
                                LeafNode("p", "Another paragraph")
                            ])
        result = node.to_html()
        assert result == '<div><p>Normal text<i>italic text</i>Normal text</p><p>Another paragraph</p></div>'

    def test_no_children(self):
        with self.assertRaises(ValueError) as context:
           node = ParentNode(tag="p", children=None)
           html = node.to_html()

    def test_no_tag(self):
        with self.assertRaises(ValueError) as context:
           node = ParentNode(tag=None, 
                             children = [
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                                ])
           html = node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )