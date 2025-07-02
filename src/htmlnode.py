class HTMLNode():
    def __init__(self, tag=None, value=None, props=None, children=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError('method not implemented by child class')
    
    def props_to_html(self):
        if not self.props:
            return ''
        attributes = []
        for key in self.props:
            attributes.append(f'{key}="{self.props[key]}"')
        return " " + ' '.join(attributes)
    
    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"
    
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
        