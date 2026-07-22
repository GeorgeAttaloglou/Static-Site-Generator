def markdown_to_blocks(markdown_text: str) -> list[str]:
    raw_blocks = markdown_text.split('\n\n')

    blocks = []
    for block in raw_blocks:
        stripped_block = block.strip()
        if stripped_block != '':
            blocks.append(stripped_block)

    return blocks