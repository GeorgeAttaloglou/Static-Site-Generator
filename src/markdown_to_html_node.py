from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from markdown_to_blocks import markdown_to_blocks
from block_to_blocktype import block_to_block_type, BlockType
from text_to_textnode import text_to_textnode

def text_to_children(text) -> list[HTMLNode]:
    text = text.replace('\n', ' ')
    text_nodes = text_to_textnode(text)
    html_nodes = []

    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for i in range(len(blocks)):
        block = blocks[i]
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                new_html_node = ParentNode('p', text_to_children(block), None)
                html_nodes.append(new_html_node)
            case BlockType.HEADING:
                j = 0
                num_of_hashtags = 0
                while block[j] == '#':
                    num_of_hashtags += 1
                    j += 1
                new_html_node = ParentNode(f"h{num_of_hashtags}", text_to_children(block[j + 1:]), None)
                html_nodes.append(new_html_node)
            case BlockType.CODE:
                code_text = block.removeprefix("```").removesuffix('```')
                code_text = code_text.removeprefix('\n').removesuffix('\n')
                text = TextNode(code_text, TextType.CODE_TEXT, None)
                new_html_node = ParentNode('pre', [text_node_to_html_node(text)], None)
                html_nodes.append(new_html_node)
            case BlockType.QUOTE:
                quote_lines = block.split('\n')
                stripped_lines = [line.removeprefix('>').lstrip() for line in quote_lines]
                quote_text = '\n'.join(stripped_lines)
                new_html_node = ParentNode('blockquote', text_to_children(quote_text), None)
                html_nodes.append(new_html_node)
            case BlockType.UNORDERED_LIST:
                list_items = block.split('\n')
                li_nodes = []
                for item in list_items:
                    if not item:
                        continue
                    item = item.removeprefix('- ')
                    li_nodes.append(ParentNode('li', text_to_children(item), None))
                new_html_node = ParentNode('ul', li_nodes, None)
                html_nodes.append(new_html_node)
            case BlockType.ORDERED_LIST:
                list_items = block.split('\n')
                li_nodes = []
                for j, item in enumerate(list_items, 1):
                    if not item:
                        continue
                    item = item.removeprefix(f'{str(j)}. ')
                    li_nodes.append(ParentNode('li', text_to_children(item), None))
                new_html_node = ParentNode('ol', li_nodes, None)
                html_nodes.append(new_html_node)

    return ParentNode('div', html_nodes, None)