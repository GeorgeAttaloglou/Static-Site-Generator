from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            blocks = node.text.split(delimiter)

            if len(blocks) % 2 == 0:
                raise Exception('Delimiter never closed')

            for i in range(len(blocks)):
                if blocks[i] == '':
                    continue

                if i % 2 == 0:
                    new_nodes.append(TextNode(blocks[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(blocks[i], text_type))

    return new_nodes
