import os
from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path:str, template_path:str, dest_path:str) -> None:
    if not os.path.exists(from_path):
        raise FileNotFoundError("Error: from_path not found")

    if not os.path.exists(template_path):
        raise FileNotFoundError("Error: template_path not found")

    if not os.path.exists(dest_path):
        os.mknod(dest_path)

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # reads the markdown file
    with open(from_path, "r") as f:
        markdown_content = f.read()

    # reads the html template file
    with open(template_path, "r") as f:
        template_contents = f.read()

    # convert the markdown to html
    html_from_markdown = markdown_to_html_node(markdown_content).to_html()

    title_of_page = extract_title(markdown_content)

    template_contents = template_contents.replace("{{ Title }}", title_of_page)
    template_contents = template_contents.replace("{{ Content }}", html_from_markdown)

    with open(dest_path, "w") as file:
        file.write(template_contents)