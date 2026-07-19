from textnode import TextType, TextNode
from extract_images_and_links import extract_markdown_images, extract_markdown_links

def split_node_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(node)
            continue
            
        for image in images:

            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)

            if len(sections) % 2 != 0:
                raise ValueError("invalid markdown, image section not closed")
            
            if sections[0] != '':
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]),)

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_node_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(node)
            continue
            
        for link in links:

            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)

            if len(sections) % 2 != 0:
                raise ValueError("invalid markdown, link section not closed")
            
            if sections[0] != '':
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]),)

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes