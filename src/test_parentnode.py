import unittest

from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_recursion(self):
        answer = "<p><b>Text1</b><h1><i>Text2</i><h2><c>Text3</c><d>Text4</d></h2><e>Text5</e></h1><a>Text6</a></p>"
        node = ParentNode("p",
                          [
                            LeafNode("b", "Text1"),
                            ParentNode("h1", [
                                                LeafNode("i", "Text2"),
                                                ParentNode("h2", [
                                                                    LeafNode("c", "Text3"),
                                                                    LeafNode("d", "Text4")]),
                                                LeafNode("e", "Text5")
                                                    ]),
                            LeafNode("a", "Text6")
                              ])
        
        self.assertEqual(answer, node.to_html())

    def test_base_case(self):
        parent = ParentNode(
    "div",
    [
        LeafNode("span", "Hello"),
        LeafNode("span", "World"),
    ]
)
        answer = f"<div><span>Hello</span><span>World</span></div>"


        self.assertEqual(answer, parent.to_html())

    def test_nested_nodes(self):
        parent = ParentNode(
            "div",
            [
                LeafNode("span", "Hello"),
                ParentNode(
                    "section",
                    [
                        LeafNode(None, "Nested Text"),
                        LeafNode("i", "Italic"),
                    ],
                ),
            ],
        )

        expected_html = "<div><span>Hello</span><section>Nested Text<i>Italic</i></section></div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_nested_with_empty_children(self):
        with self.assertRaises(ValueError):
            deeply_nested = ParentNode("div", [
                ParentNode("section", [
                ParentNode("article", [])
                ])
            ])

    def test_node_with_props(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        LeafNode("p", "Paragraph 1"),
                        LeafNode("p", "Paragraph 2", {"class": "highlight"}),
                    ],
                    {"id": "main-section"},
                ),
                LeafNode("footer", "Footer text", {"style": "color: gray;"}),
            ],
            {"class": "container", "role": "main"},
        )

        expected_html = (
            '<div class="container" role="main">'
            '<section id="main-section">'
            '<p>Paragraph 1</p>'
            '<p class="highlight">Paragraph 2</p>'
            '</section>'
            '<footer style="color: gray;">Footer text</footer>'
            '</div>'
        )

        self.assertEqual(node.to_html(), expected_html)
    
    def test_empty_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

        with self.assertRaises(ValueError):
            ParentNode("div", [])

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()