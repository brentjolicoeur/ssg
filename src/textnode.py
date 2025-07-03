from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode():
    def __init__(self, text, text_type, url=None):
        if not text:
            raise ValueError("text is required")
        self.text = text
        if isinstance(text_type, TextType):
            self.text_type = text_type
        else:
            raise ValueError("text_type must be an instance of the TextType enum")
        self.url = url

    def __eq__(self, value):
        if not isinstance(value, TextNode):
            return False
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url

    def __repr__(self):
        if not self.url:
            return f"TextNode({self.text}, {self.text_type.value})"
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def text_node_to_html_node(self):
        if self.text_type == TextType.TEXT:
            node = LeafNode(None, self.text)
            return node
        elif self.text_type == TextType.BOLD:
            node = LeafNode("b", self.text)
            return node
        elif self.text_type == TextType.ITALIC:
            node = LeafNode("i", self.text)
            return node
        elif self.text_type == TextType.CODE:
            node = LeafNode("code", self.text)
            return node
        elif self.text_type == TextType.LINK:
            if not self.url:
                raise ValueError("missing url for link")
            node = LeafNode("a", self.text, {"href":self.url})
            return node
        elif self.text_type == TextType.IMAGE:
            if not self.url:
                raise ValueError("missing url for image")
            node = LeafNode("img", "", {"src":self.url, "alt":self.text})
            return node
        else:
            raise ValueError(f"Unsupported text type: {self.text_type}")