from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from block_markdown import block_to_block_type, markdown_to_blocks
from inline_markdown import text_to_textnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block) 
        if block_type == 'paragraph':
            block_nodes.append(paragraph_to_html_node(block))
        elif block_type == 'heading':
            block_nodes.append(heading_to_html_node(block))
        elif block_type == 'quote':
            block_nodes.append(quote_to_html_node(block))
        elif block_type == 'unordered_list':
            block_nodes.append(unordered_list_to_html_node(block))
        elif block_type == 'ordered list':
            block_nodes.append(ordered_list_to_html_node(block))
        else:
            raise Exception("Block type not recognized.")

    final_html_node = ParentNode('div', block_nodes)
    return final_html_node

def paragraph_to_html_node(block):
    child_nodes = text_to_children(block)
    paragraph_block = ParentNode('p', child_nodes)
    return paragraph_block

def heading_to_html_node(block):
    heading_split = block.split(maxsplit=1)
    heading_level = heading_split[0].count('#')
    child_nodes = text_to_children(heading_split[1])
    heading_block = ParentNode(f'h{heading_level}', child_nodes)
    return heading_block

def quote_to_html_node(block):
    quote_leafs = []
    lines = block.splitlines()
    for line in lines:
        text = line.lstrip('>')
        child_nodes = text_to_children(text)
        quote_leafs.extend(child_nodes)
    quote_block = ParentNode('blockquote', quote_leafs)
    return quote_block

def unordered_list_to_html_node(block):
    lines = block.splitlines()
    line_nodes = [get_list_line_nodes(line) for line in lines]
    unordered_list_block = ParentNode('ul', line_nodes)
    return unordered_list_block

def ordered_list_to_html_node(block):
    lines = block.splitlines()
    line_nodes = [get_list_line_nodes(line) for line in lines]
    ordered_list_block = ParentNode('ol', line_nodes)
    return ordered_list_block

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes
    
def get_list_line_nodes(line):
    separator = line.split(maxsplit=1)
    child_nodes = text_to_children(separator[1])
    node = ParentNode('li', child_nodes)
    return node

