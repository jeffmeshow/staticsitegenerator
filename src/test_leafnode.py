import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_create_node(self):
        node = LeafNode(tag="p", value="This is a paragraph", props={"style": "color='red'"})
        assert node.tag == "p"
        assert node.value == "This is a paragraph"
        assert node.children == None
        assert node.props["style"] == "color='red'"


    def test_create_no_children(self):
        leaf_node = LeafNode(tag="p", value="This is leaf p node", props=None)
        assert leaf_node.children is None

    def test_a_tag(self):
        node = LeafNode(tag="a", value="This is a cool training site", props={"href": "http://boot.dev"})
        expected = '<a href="http://boot.dev">This is a cool training site</a>'
        assert node.to_html() == expected

    def test_no_tag(self):
        node = LeafNode(tag=None, value="This is just raw text.")
        #print (node.to_html())
        assert node.to_html() == 'This is just raw text.'

    def test_no_value(self):
        with self.assertRaises(ValueError) as context:
           node = LeafNode(tag="p", value=None)
           html = node.to_html()
       

    
