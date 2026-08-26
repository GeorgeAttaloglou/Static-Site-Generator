import os
import shutil
import sys

from generate_page import generate_page

SOURCE_DIR = "static"
DESTINATION_DIR = "docs"
CONTENT_DIR = "content"
TEMPLATE_PATH = "template.html"


def copy_static_to_public() -> None:
    """Wipe the public directory and replace it with a fresh copy of static."""
    if not os.path.exists(SOURCE_DIR):
        raise Exception("Error: Invalid source directory")

    if os.path.exists(DESTINATION_DIR):
        shutil.rmtree(DESTINATION_DIR)

    shutil.copytree(SOURCE_DIR, DESTINATION_DIR)


def generate_pages_recursive(
    basepath: str,
    source_dir_path: str = CONTENT_DIR,
    dest_dir_path: str = DESTINATION_DIR,
) -> None:
    
    """Mirror the content directory structure into public, generating an
    .html page (via the template) for every markdown file found."""
    for entry in os.listdir(source_dir_path):
        source_path = os.path.join(source_dir_path, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(source_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(source_path, dest_path)
        else:
            dest_path = dest_path.replace(".md", ".html")
            generate_page(source_path, TEMPLATE_PATH, dest_path, basepath)


def main(basepath: str="/") -> None:
    basepath = sys.argv[1]
    copy_static_to_public()
    generate_pages_recursive(basepath)


if __name__ == "__main__":
    main()