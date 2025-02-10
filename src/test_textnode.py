import unittest

from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_three_properties(self):
        node = TextNode("This is a txt node", TextType.BOLD, "espn.com")
        node2 = TextNode("This is a txt node", TextType.BOLD, "espn.com")
        self.assertEqual(node, node2)

    def test_eq_diff_text(self):
        node = TextNode("This is a txt node", TextType.BOLD, "espn.com")
        node2 = TextNode("This is not a txt node", TextType.BOLD, "espn.com")
        self.assertNotEqual(node, node2)

    def test_eq_diff_text_type(self):
        node = TextNode("This is a txt node", TextType.CODE, "espn.com")
        node2 = TextNode("This is not a txt node", TextType.BOLD, "espn.com")
        self.assertNotEqual(node, node2)

    def test_eq_one_url(self):
        node = TextNode("This is a txt node", TextType.BOLD)
        node2 = TextNode("This is not a txt node", TextType.BOLD, "espn.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHtmlConversion(unittest.TestCase):
    def test_plaintext(self):
        node = TextNode("testing plaintext", TextType.TEXT)
        self.assertEqual("testing plaintext", text_node_to_html_node(node).to_html())

    def test_bold(self):
        node = TextNode("testing bold", TextType.BOLD)
        self.assertEqual("<b>testing bold</b>", text_node_to_html_node(node).to_html())

    def test_italic(self):
        node = TextNode("testing italic", TextType.ITALIC)
        self.assertEqual("<i>testing italic</i>", text_node_to_html_node(node).to_html())

    def test_code(self):
        node = TextNode("testing code", TextType.CODE)
        self.assertEqual("<code>testing code</code>", text_node_to_html_node(node).to_html())

    def test_link(self):
        node = TextNode("testing link", TextType.LINK, url="espn.com")
        self.assertEqual('<a href="espn.com">testing link</a>', text_node_to_html_node(node).to_html())
    
    def test_image(self):
        node = TextNode("testing image", TextType.IMAGE, url="espn.com")
        self.assertEqual('<img src="espn.com" alt="testing image"></img>', text_node_to_html_node(node).to_html())

    def test_invalid_text_type1(self):
        with self.assertRaises(AttributeError):
            node = TextNode("testing strikethrough", TextType.STRIKETHROUGH)

    def test_invalid_text_type2(self):
        with self.assertRaises(ValueError):
            node = TextNode("testing strikethrough", "highlight")

    def test_empty_text(self):
        with self.assertRaises(ValueError):
            node = TextNode("", TextType.TEXT)

    def test_empty_url_link(self):
        with self.assertRaises(ValueError):
            node = TextNode("testing link missing url", TextType.LINK)
            text_node_to_html_node(node).to_html()

    def test_empty_url_image(self):
        with self.assertRaises(ValueError):
            node = TextNode("testing image without source url", TextType.IMAGE)
            text_node_to_html_node(node).to_html()

if __name__ == "__main__":
    unittest.main()