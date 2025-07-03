import unittest

from helpers import  split_nodes_delimiter #extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):

    def test_single_node_bold(self):
        bold_node = TextNode("This is a **string with bold** markdown text.", TextType.TEXT)
        correct = [TextNode("This is a ", TextType.TEXT), TextNode("string with bold", TextType.BOLD), TextNode(" markdown text.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_delimiter([bold_node], '**', TextType.BOLD))

    def test_single_node_italic(self):
        italic_node = TextNode("This is a _string with italic_ markdown text.", TextType.TEXT)
        correct = [TextNode("This is a ", TextType.TEXT), TextNode("string with italic", TextType.ITALIC), TextNode(" markdown text.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_delimiter([italic_node], '_', TextType.ITALIC))

    def test_single_node_code(self):
        code_node = TextNode("This is a `string with code block` markdown text.", TextType.TEXT)
        correct = [TextNode("This is a ", TextType.TEXT), TextNode("string with code block", TextType.CODE), TextNode(" markdown text.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_delimiter([code_node], '`', TextType.CODE))

    def test_multi_occurence(self):
        markdown = "_This_ is a string that _has markdown text_ in it. Now it _has multiple markdown_ occurences."
        multi_italic_node = TextNode(markdown, TextType.TEXT)
        correct = [TextNode("This", TextType.ITALIC), TextNode(" is a string that ", TextType.TEXT), TextNode("has markdown text", TextType.ITALIC),
                   TextNode(" in it. Now it ", TextType.TEXT), TextNode("has multiple markdown", TextType.ITALIC), TextNode(" occurences.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_delimiter([multi_italic_node], '_', TextType.ITALIC))
    
    def test_single_word_markdown_at_end(self):
        test_node = TextNode("This is markdown text with a markdown at the **end.**", TextType.TEXT)
        correct = [TextNode("This is markdown text with a markdown at the ", TextType.TEXT), TextNode("end.", TextType.BOLD)]
        self.assertEqual(correct, split_nodes_delimiter([test_node], '**', TextType.BOLD))

    def test_single_word_markdown_at_begin(self):
        test_node = TextNode("**This** is markdown text with a markdown at the beginning.", TextType.TEXT)
        correct = [TextNode("This", TextType.BOLD), TextNode(" is markdown text with a markdown at the beginning.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_delimiter([test_node], '**', TextType.BOLD))

    def test_unpaired_markdown(self):
        italic_node = TextNode("This is a _string with italic markdown text.", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([italic_node], '_', TextType.ITALIC)