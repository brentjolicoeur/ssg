import unittest

from splitnodes import  split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):

    def test_single_node_bold(self):
        bold_node = TextNode("This is a **string with bold** markdown text.", TextType.TEXT)
        correct = [TextNode("This is a ", TextType.TEXT), TextNode("string with bold", TextType.BOLD), TextNode(" markdown text.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_delimiter([bold_node], '**', TextType.BOLD))

    def test_single_node_italic(self):
        italic_node = TextNode("This is a *string with italic* markdown text.", TextType.TEXT)
        correct = [TextNode("This is a ", TextType.TEXT), TextNode("string with italic", TextType.ITALIC), TextNode(" markdown text.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_delimiter([italic_node], '*', TextType.ITALIC))

    def test_single_node_code(self):
        code_node = TextNode("This is a `string with code block` markdown text.", TextType.TEXT)
        correct = [TextNode("This is a ", TextType.TEXT), TextNode("string with code block", TextType.CODE), TextNode(" markdown text.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_delimiter([code_node], '`', TextType.CODE))

    def test_multi_occurence(self):
        markdown = "*This* is a string that *has markdown text* in it. Now it *has multiple markdown* occurences."
        multi_italic_node = TextNode(markdown, TextType.TEXT)
        correct = [TextNode("This", TextType.ITALIC), TextNode(" is a string that ", TextType.TEXT), TextNode("has markdown text", TextType.ITALIC),
                   TextNode(" in it. Now it ", TextType.TEXT), TextNode("has multiple markdown", TextType.ITALIC), TextNode(" occurences.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_delimiter([multi_italic_node], '*', TextType.ITALIC))
    
    def test_single_word_markdown_at_end(self):
        test_node = TextNode("This is markdown text with a markdown at the **end.**", TextType.TEXT)
        correct = [TextNode("This is markdown text with a markdown at the ", TextType.TEXT), TextNode("end.", TextType.BOLD)]
        self.assertEqual(correct, split_nodes_delimiter([test_node], '**', TextType.BOLD))

    def test_single_word_markdown_at_begin(self):
        test_node = TextNode("**This** is markdown text with a markdown at the beginning.", TextType.TEXT)
        correct = [TextNode("This", TextType.BOLD), TextNode(" is markdown text with a markdown at the beginning.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_delimiter([test_node], '**', TextType.BOLD))

    def test_unpaired_markdown(self):
        italic_node = TextNode("This is a *string with italic markdown text.", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([italic_node], '*', TextType.ITALIC)

class ExtractImaagesAndLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        correct = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(correct, extract_markdown_images(text))

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        correct = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(correct, extract_markdown_links(text))

if __name__ == "__main__":
    unittest.main()