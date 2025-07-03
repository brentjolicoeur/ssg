import unittest

from helpers import  split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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

class TestExtractImaagesAndLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        correct = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(correct, extract_markdown_images(text))

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        correct = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(correct, extract_markdown_links(text))

class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode("This is a ![text with](http://espn.com) single image", TextType.TEXT,)
        correct = [TextNode("This is a ", TextType.TEXT), TextNode("text with", TextType.IMAGE, "http://espn.com"), TextNode(" single image", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_image([node]))

    def test_beginning_single_image(self):
        node = TextNode("![This is a](http://espn.com) text with a beginning image.", TextType.TEXT)
        correct = [TextNode("This is a", TextType.IMAGE, "http://espn.com"), TextNode(" text with a beginning image.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_image([node]))

    def test_ending_single_image(self):
        node = TextNode("This is a text node with a ![image at the end](http://espn.com)", TextType.TEXT)
        correct = [TextNode("This is a text node with a ", TextType.TEXT), TextNode("image at the end", TextType.IMAGE, "http://espn.com")]
        self.assertEqual(correct, split_nodes_image([node]))

    def test_no_images(self):
        node = TextNode("This is a text node with no images.", TextType.TEXT)
        correct = [TextNode("This is a text node with no images.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_image([node]))

    def test_multiple_links(self):
        node = TextNode(
    "This is text with a image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,)
        correct = [
            TextNode("This is text with a image ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(correct, split_nodes_image([node]))

class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode("This is a [text with](http://espn.com) single link", TextType.TEXT,)
        correct = [TextNode("This is a ", TextType.TEXT), TextNode("text with", TextType.LINK, "http://espn.com"), TextNode(" single link", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_link([node]))

    def test_beginning_single_link(self):
        node = TextNode("[This is a](http://espn.com) text with a beginning link.", TextType.TEXT)
        correct = [TextNode("This is a", TextType.LINK, "http://espn.com"), TextNode(" text with a beginning link.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_link([node]))

    def test_ending_single_link(self):
        node = TextNode("This is a text node with a [link at the end](http://espn.com)", TextType.TEXT)
        correct = [TextNode("This is a text node with a ", TextType.TEXT), TextNode("link at the end", TextType.LINK, "http://espn.com")]
        self.assertEqual(correct, split_nodes_link([node]))

    def test_no_links(self):
        node = TextNode("This is a node without any links.", TextType.TEXT)
        correct = [TextNode("This is a node without any links.", TextType.TEXT)]
        self.assertEqual(correct, split_nodes_link([node]))

    def test_only_link_single(self):
        node = TextNode("[This node is only a link](http://espn.com)", TextType.TEXT)
        correct = [TextNode("This node is only a link", TextType.LINK, "http://espn.com")]
        self.assertEqual(correct, split_nodes_link([node]))

    def test_only_link_multi(self):
        node = TextNode("[This node has](http://espn.com) [only two links](http://google.com)", TextType.TEXT)
        correct = [TextNode("This node has", TextType.LINK, "http://espn.com"), TextNode(" ", TextType.TEXT), TextNode("only two links", TextType.LINK, "http://google.com")]
        self.assertEqual(correct, split_nodes_link([node]))

    def test_multiple_links(self):
        node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,)
        correct = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(correct, split_nodes_link([node]))