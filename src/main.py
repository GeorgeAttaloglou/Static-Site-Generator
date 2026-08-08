import os
import shutil
from generate_page import generate_page

def copy_static_to_public() -> None:
    source_dir = 'static'
    destination_dir = 'public'
    if not os.path.exists(source_dir):
        raise Exception('Error: Invalid source directory')
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    # copy contents of source into destination
    shutil.copytree(source_dir, destination_dir)

def main():
    copy_static_to_public()

    generate_page("content/index.md", "template.html", "public/index.html")

main()
