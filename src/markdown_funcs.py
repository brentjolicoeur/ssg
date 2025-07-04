from textnode_helpers import block_to_block_type, BlockType, text_to_textnodes
from parentnode import ParentNode
from textnode import TextNode, TextType

def markdown_to_blocks(markdown):
    blocks = []
    splits = markdown.split('\n\n')
    for split in splits:
        if split.strip() != '':
            blocks.append(split.strip())
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        type = block_to_block_type(block)

        match type:
            case BlockType.PARAGRAPH:
                normalized_text = block.replace('\n', ' ')
                children = text_to_children(normalized_text)
                p_node = ParentNode('p', children)
                block_nodes.append(p_node)
            case BlockType.HEADING:
                heading, text = strip_and_determine_heading(block)
                children = text_to_children(text)
                h_node = ParentNode(f"h{heading}", children)
                block_nodes.append(h_node)
            case BlockType.CODE:
                text = block[3: -3]
                if text.startswith('\n'):
                    text = text[1:]
                node = TextNode(text, TextType.CODE)
                code_node = node.text_node_to_html_node()
                code_parent = ParentNode("pre", [code_node])
                block_nodes.append(code_parent)
            case BlockType.QUOTE:
                stripped_block = strip_quote_block(block)
                children = text_to_children(stripped_block)
                q_node = ParentNode('blockquote', children)
                block_nodes.append(q_node)
            case BlockType.UNORDERED_LIST:
                list_items = process_list_items(block)
                ul_node = ParentNode('ul', list_items)
                block_nodes.append(ul_node)
            case BlockType.ORDERED_LIST:
                list_items = process_list_items(block, ordered=True)
                ol_node = ParentNode('ol', list_items)
                block_nodes.append(ol_node)
    return ParentNode('div', block_nodes)
            
def text_to_children(block):
    child_html_nodes = []
    text_nodes = text_to_textnodes(block)
    for node in text_nodes:
        html_node = node.text_node_to_html_node()
        child_html_nodes.append(html_node)
    return child_html_nodes

def strip_and_determine_heading(block):
    split_header = block.split(maxsplit=1)
    heading = len(split_header[0])
    text = split_header[1] if len(split_header) > 1 else ""
    return heading, text

def strip_quote_block(block):
    lines = block.splitlines()
    stripped_lines = []
    for line in lines:
        if line.startswith("> "):
            stripped_lines.append(line[2:])
        else:
            stripped_lines.append(line[1:])
    return ' '.join(stripped_lines)

def process_list_items(block, ordered=False):
    list_items = []
    lines = block.splitlines()
    for line in lines:
        if ordered:
            split_line = line.split('. ', maxsplit=1)
            text = split_line[1]
        else:
            text = line[2:]
        line_nodes = text_to_children(text)
        list_items.append(ParentNode('li', line_nodes))
    return list_items
        
