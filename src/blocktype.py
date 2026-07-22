from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 'Paragraph'
    HEADING = 'Heading'
    CODE = 'Code'
    QUOTE = 'Quote'
    UNORDERED_LIST = 'Unordered List'
    ORDERED_LIST = 'Ordered List'
