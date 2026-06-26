import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_create_node(self):
        node = TextNode("Great website", TextType.LINK, "http://boot.dev")
        
        assert node.text == "Great website"
        assert node.text_type == TextType.LINK
        assert node.url == "http://boot.dev"

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_for_link_or_image(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("This is a link", TextType.LINK, None)

        with self.assertRaises(Exception) as context:
            node = TextNode("This is an image", TextType.IMAGE, None)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_empty(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("", TextType.BOLD)
    
        with self.assertRaises(Exception) as context:
            node = TextNode("", TextType.ITALIC)

        with self.assertRaises(Exception) as context:
            node = TextNode("", TextType.PLAIN)

    def test_converttohtml_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_converttohml_image(self):
        node = TextNode("This is an image", TextType.IMAGE, url="images/car.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "images/car.jpg")

    def test_converttohtml_invalid_type(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("This is an image", TextType.VIDEO, url="videos/movie.mov")
            html_node = text_node_to_html_node(node)
    

if __name__ == "__main__":
    unittest.main()