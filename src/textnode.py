from enum import Enum

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode():
    def __init__(self, text, text_type, url=None):
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