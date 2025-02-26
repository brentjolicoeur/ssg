def markdown_to_blocks(markdown):
    lines = markdown.split('\n')
    blank_lines_indices = []
    line_blocks = []

    for i in range(len(lines)):
        if not lines[i].strip():
            blank_lines_indices.append(i)

    current_line_index = 0
    for index in blank_lines_indices:
        if current_line_index == index:
            current_line_index += 1
            continue
        block = "\n".join(lines[current_line_index:index])
        block = block.strip()
        if block:
            line_blocks.append(block)
        current_line_index = index + 1
    
    if current_line_index < len(lines):
        last_block = "\n".join(lines[current_line_index:])
        last_block = last_block.strip()
        if last_block:
            line_blocks.append(last_block)

    return line_blocks

def block_to_block_type(block):
    if block.startswith("```") and block.endswith("```"):
        return "code"
    elif block.startswith("#"):
        HEADINGS = ('#', '##', '###', '####', '#####', '######')
        header = block.split(maxsplit=1)
        if header[0] not in HEADINGS:
            return "paragraph"
        return "heading"
    elif block.startswith(">"):
        quote_lines = block.splitlines()
        for line in quote_lines:
            if not line.startswith('>'):
                return "paragraph"
        return "quote"
    elif block.startswith("* ") or block.startswith("- "):
        bullet = block[0]
        unorderd_lines = block.splitlines()
        for line in unorderd_lines:
            if not line.startswith(f"{bullet} "):
                return "paragraph"
        return "unordered_list"
    elif block.startswith("1. "):
        ordered_lines = block.splitlines()
        for index, line in enumerate(ordered_lines):
            if not line.startswith(f"{index + 1}. "):
                return "paragraph"
        return "ordered list"
    return "paragraph"