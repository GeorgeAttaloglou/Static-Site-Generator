from blocktype import BlockType
import re

def block_to_blocktype(block: str) -> BlockType:
    lines = block.strip('\n')

    if len(lines) > 1:
        # if there are more than one lines we are dealing with a list
        pass

    if re.search(r"(#{1,6} )\w*", block):
        return BlockType.HEADING
    elif re.search(r"", block)
