class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("was not implemented by child class")

    def props_to_html(self):
        if self.props is None:
            return ""
        attributes = ''
        for key, value in self.props.items():
            attributes += f' {key}="{value}"'

        return attributes

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value == None:
            raise ValueError("value required for LeafNode")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value required for LeafNode")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag == None:
            raise ValueError("ParentNode requires tag")
        if children == None or children == []:
            raise ValueError("Children nodes are required")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires tag")
        if not self.children:
            raise ValueError("Children nodes are required")
        parent_nodes = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            if isinstance(node, LeafNode):
                parent_nodes += node.to_html()
            else:
                nested_nodes = node.to_html()
                parent_nodes += nested_nodes
        parent_nodes += f"</{self.tag}>"
        return parent_nodes


    def __repr__(self):
        return f"HTMLNode({self.tag}, children: {self.children}, {self.props})"