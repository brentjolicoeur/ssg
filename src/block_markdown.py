

def markdown_to_blocks(markdown):
    lines = markdown.split('\n')
    blank_lines_indices = []
    line_blocks = []

    for i in range(len(lines)):
        if not lines[i]:
            blank_lines_indices.append(i)

    current_line_index = 0
    for index in blank_lines_indices:
        if current_line_index == index:
            current_line_index += 1
            continue
        block = "\n".join(lines[current_line_index:index])
        block = block.strip()
        line_blocks.append(block)
        current_line_index = index + 1
    
    if current_line_index != len(lines) - 1:
        last_block = "\n".join(lines[current_line_index:])
        last_block = last_block.strip()
        line_blocks.append(last_block)

    return line_blocks