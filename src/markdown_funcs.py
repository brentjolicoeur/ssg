from textnode_helpers import block_to_block_type, BlockType

def markdown_to_blocks(markdown):
    blocks = []
    splits = markdown.split('\n\n')
    for split in splits:
        if split.strip() != '':
            blocks.append(split.strip())
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        match type:
            case BlockType.PARAGRAPH:
                pass
            case BlockType.HEADING:
                pass
            case BlockType.CODE:
                pass
            case BlockType.QUOTE:
                pass
            case BlockType.UNORDERED_LIST:
                pass
            case BlockType.ORDERED_LIST:
                pass
            
        
        

md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
markdown_to_html_node(md)