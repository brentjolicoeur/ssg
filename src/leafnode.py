from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("value is required for leaf nodes")
        super().__init__(tag, value, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value is required for leaf nodes")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
