import unittest

from textnode import TextNode, TextType

class TestTextnodeToHtmlnode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_plaintext(self):
        node = TextNode("testing plaintext", TextType.TEXT)
        self.assertEqual("testing plaintext", node.text_node_to_html_node().to_html())

    def test_bold(self):
        node = TextNode("testing bold", TextType.BOLD)
        self.assertEqual("<b>testing bold</b>", node.text_node_to_html_node().to_html())

    def test_italic(self):
        node = TextNode("testing italic", TextType.ITALIC)
        self.assertEqual("<i>testing italic</i>", node.text_node_to_html_node().to_html())

    def test_code(self):
        node = TextNode("testing code", TextType.CODE)
        self.assertEqual("<code>testing code</code>", node.text_node_to_html_node().to_html())

    def test_link(self):
        node = TextNode("testing link", TextType.LINK, url="espn.com")
        self.assertEqual('<a href="espn.com">testing link</a>', node.text_node_to_html_node().to_html())
    
    def test_image(self):
        node = TextNode("testing image", TextType.IMAGE, url="espn.com")
        self.assertEqual('<img src="espn.com" alt="testing image"></img>', node.text_node_to_html_node().to_html())

    def test_invalid_text_type1(self):
        with self.assertRaises(AttributeError):
            node = TextNode("testing strikethrough", TextType.STRIKETHROUGH)

    def test_invalid_text_type2(self):
        with self.assertRaises(ValueError):
            node = TextNode("testing strikethrough", "highlight")

    def test_empty_text(self):
        with self.assertRaises(ValueError):
            node = TextNode("", TextType.TEXT)
            node.text_node_to_html_node().to_html()

    def test_empty_url_link(self):
        with self.assertRaises(ValueError):
            node = TextNode("testing link missing url", TextType.LINK)
            node.text_node_to_html_node().to_html()

    def test_empty_url_image(self):
        with self.assertRaises(ValueError):
            node = TextNode("testing image without source url", TextType.IMAGE)
            node.text_node_to_html_node().to_html()

if __name__ == "__main__":
    unittest.main()