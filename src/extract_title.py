def extract_title(markdown:str) -> str:
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("Error: no h1 header found")