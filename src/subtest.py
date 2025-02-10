from htmlnode import *


no_subparent_node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)



test_node = ParentNode("p",
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

def to_html(self):
    parent_nodes = f"<{self.tag}>"
    for node in self.children:
        if isinstance(node, LeafNode):
            parent_nodes += node.to_html()
        else:
            nested_nodes = node.to_html()
            parent_nodes += nested_nodes
    parent_nodes += f"</{self.tag}>"
    return parent_nodes


print(no_subparent_node.to_html())
