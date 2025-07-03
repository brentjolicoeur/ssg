from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError('tag is missing')
        if children is None or children == []:
            raise ValueError('Children nodes are required for parent nodes')
        super().__init__(tag, None, props, children)

    def to_html(self):
        if self.tag is None:
            raise ValueError('tag is missing')
        if self.children is None or not self.children:
            raise ValueError('Children nodes are required for parent nodes')
        
        html_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"

        return html_string