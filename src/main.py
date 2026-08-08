from textnode import TextNode,TextType
import os
import shutil

def copy_dir_to_public() -> None:
    source_dir = 'static'
    destination_dir = 'public'
    if not os.path.exists(source_dir):
        raise Exception('Error: Invalid source directory')
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    # copy contents of source into destination
    shutil.copytree(source_dir, destination_dir)