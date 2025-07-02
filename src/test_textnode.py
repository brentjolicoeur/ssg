import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_three_properties(self):
        node = TextNode("This is a txt node", TextType.TEXT, "espn.com")
        node2 = TextNode("This is a txt node", TextType.TEXT, "espn.com")
        self.assertEqual(node, node2)

    def test_eq_diff_text(self):
        node = TextNode("This is a txt node", TextType.BOLD, "espn.com")
        node2 = TextNode("This is not a txt node", TextType.BOLD, "espn.com")
        self.assertNotEqual(node, node2)

    def test_eq_diff_text_type(self):
        node = TextNode("This is a txt node", TextType.CODE, "espn.com")
        node2 = TextNode("This is a txt node", TextType.BOLD, "espn.com")
        self.assertNotEqual(node, node2)

    def test_eq_one_url(self):
        node = TextNode("This is a txt node", TextType.BOLD)
        node2 = TextNode("This is a txt node", TextType.BOLD, "espn.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

if __name__ == "__main__":
    unittest.main()
