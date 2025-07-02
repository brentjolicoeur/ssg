import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(tag="h1", value="This is a heading")
        self.assertEqual("HTMLNode(tag: h1, value: This is a heading, children: None, props: None)", repr(node))

    def test_props_to_html(self):
        test = {"href": "https://www.google.com","target": "_blank",}
        node = HTMLNode(tag="h1", value="This is a heading",props=test)
        self.assertEqual(' href="https://www.google.com" target="_blank"', HTMLNode.props_to_html(node))

    def test_props_to_html_children(self):
        test = {"size": "800x1200","color": "blue",}
        node1 = HTMLNode(tag="h1", value="This is a heading")
        node2 = node = HTMLNode(tag="h1", value="This is a heading",props=test)
        node = HTMLNode(tag="h1", children=[node1, node2],props=test)
        self.assertEqual(' size="800x1200" color="blue"', HTMLNode.props_to_html(node))


if __name__ == "__main__":
    unittest.main()