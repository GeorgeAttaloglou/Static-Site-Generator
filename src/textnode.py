from enum import Enum

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE_TEXT = 'code'
    LINK = 'link'
    IMAGE = 'image'


class TextNode:
    def __init__(self, text:str, text_type:TextType, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other:TextNode) -> bool:

        # if all values are equal return True
        return self.text == other.text and self.text_type == self.text_type and self.url == other.url
    
    def __repr__(self) -> str:
        
        # TextNode(TEXT, TEXT_TYPE, URL)
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"