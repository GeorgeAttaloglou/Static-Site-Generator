from textnode import TextNode, TextType
from split_node_delimiter import split_nodes_delimiter
from split_node_images_and_links import split_node_images, split_node_links

def text_to_textnode(text: str):
    node = TextNode(text, TextType.TEXT)
    new_nodes = [node]

    new_nodes = split_node_images(new_nodes)
    new_nodes = split_node_links(new_nodes)

    delimiters = ['**', '_', '`',]

    for delimiter in delimiters:
        match delimiter:
            case '**':
                new_nodes = split_nodes_delimiter(new_nodes, delimiter, TextType.BOLD)
            case '_':
                new_nodes = split_nodes_delimiter(new_nodes, delimiter, TextType.ITALIC)
            case '`':
                new_nodes = split_nodes_delimiter(new_nodes, delimiter, TextType.CODE_TEXT)

    return new_nodes