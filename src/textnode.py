from enum import Enum
from htmlnode import LeafNode

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
        self.url = url
        if isinstance(text_type, TextType):
            self.text_type = text_type
        else:
            raise ValueError("text_type must be an instance of the TextType enum")

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.url == other.url and self.text_type == other.text_type

    def __repr__(self):
        if not self.url:
            return f'TextNode("{self.text}", {self.text_type})'
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'

    def to_html(self):
        # Handle different node types appropriately
        if self.text_type == TextType.TEXT:
            return self.text  # Basic text, e.g., <br> or plain content
        elif self.text_type == TextType.BOLD:
            return f"<b>{self.text}</b>"
        elif self.text_type == TextType.ITALIC:
            return f"<i>{self.text}</i>"
        elif self.text_type == TextType.CODE:
            return f"<code>{self.text}</code>"
        elif self.text_type == TextType.LINK:
            if not self.url:
                raise ValueError("URL is required for text type LINK")
            return f'<a href="{self.url}">{self.text}</a>'
        elif self.text_type == TextType.IMAGE:
            if not self.url:
                raise ValueError("URL is required for text type IMAGE")
            return f'<img src="{self.url}" alt="{self.text}" />'
        else:
            raise ValueError(f"Unsupported text type: {self.text_type}")

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        if text_node.url is None or text_node.url == "":
            raise ValueError("url required")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url is None or text_node.url == "":
            raise ValueError("url required")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("not a valid text type")
    