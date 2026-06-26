import unittest
from parsemarkdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from parsemarkdown import split_nodes_image, split_nodes_link, text_to_textnodes
from parsemarkdown import markdown_to_blocks
from textnode import TextNode, TextType

class TestParseMarkDown(unittest.TestCase):
    def test_simple(self):
        nodes = [
                TextNode("Bold text", TextType.BOLD),
                TextNode("Normal text with **bold** text", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert len(result) == 5
        assert result[2].text_type == TextType.BOLD
        assert result[2].text == "bold"

    def test_delimiteratstart(self):
        nodes = [
                TextNode("Bold text", TextType.BOLD),
                TextNode("**bold** text", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert len(result) == 4
        assert result[1].text_type == TextType.BOLD
        assert result[1].text == "bold"

    def test_delimiteratdouble(self):
        nodes = [
                TextNode("Bold text", TextType.BOLD),
                TextNode("_italic__italic_ text", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                ]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        assert len(result) == 5
        assert result[1].text_type == TextType.ITALIC
        assert result[1].text == "italic"
        assert result[2].text_type == TextType.ITALIC
        assert result[2].text == "italic"

    def test_extract_image_basic(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        assert len(result) == 2
        assert result[0][0] == "rick roll"
        assert result[1][1] == "https://i.imgur.com/fJRm4Vk.jpeg"

    def test_extract_link_basic(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        assert len(result) == 2

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://wikipedia.org"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_text_totextnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()  