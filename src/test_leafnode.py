import unittest

from htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_leaf(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual('<a href="https://www.google.com">Click me!</a>', LeafNode.to_html(node))

    def test_tag_no_prop(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual('<p>This is a paragraph of text.</p>', LeafNode.to_html(node))


    def test_no_tag(self):
        node = LeafNode(None, "This leaf node has no tag")
        self.assertEqual("This leaf node has no tag", LeafNode.to_html(node))

    def test_no_tag_with_prop(self):
        node = LeafNode(None, "This leaf node has no tag but has prop", {"href": "https://www.google.com"})
        self.assertEqual("This leaf node has no tag but has prop", LeafNode.to_html(node))


    def test_leaf_value_none(self):
        with self.assertRaises(ValueError):
            node = LeafNode("a", None, {"href": "https://www.google.com"})





if __name__ == "__main__":
    unittest.main()