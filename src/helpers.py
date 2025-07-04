import re

from textnode import TextType, TextNode
from enum import Enum

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # only splitting "text" type objects
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splits = node.text.split(delimiter)
        if len(splits) % 2 == 0:
            raise Exception("unmatched delimiter found")
        while len(splits) > 1: # while loop in case multiple examples of delimited text in node
            plain_text = splits.pop(0) # first item in split will be plain text
            delimited_text = splits.pop(0) # second item (first after previous pop) is the delimited text
            if plain_text: # handles edge case where delimiter is first character in node's text
                plain_node = TextNode(plain_text, TextType.TEXT)
                new_nodes.append(plain_node)
            if delimited_text: # handles edge case where delimiters surround no text
                delimited_node = TextNode(delimited_text, text_type)
                new_nodes.append(delimited_node)
        # Last item in splt will be plain text
        if splits[0] != '':  # handles edge case where delimiter is last character in node's text
            new_nodes.append(TextNode(splits[0], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    images_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(images_regex, text)
    return matches

def extract_markdown_links(text):
    links_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(links_regex, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # only splitting "text" type objects
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        working_text = node.text # get text to separate
        for i in range(len(images)): #handles potential multiple images
            alt_text, url = images[i][0], images[i][1]
            split = working_text.split(f"![{alt_text}]({url})", 1) # split around image block
            before = split.pop(0) # get text before image block
            if before: # handles case where image block is at the start of node
                before_node = TextNode(before, TextType.TEXT)
                new_nodes.append(before_node)
            image_node = TextNode(alt_text, TextType.IMAGE, url) # creates the image node
            new_nodes.append(image_node)
            working_text = split[0] # sets the text after the image block to continue working with if necessary
        if working_text: # will not trigger if image block is at the end of the node's text
            new_nodes.append(TextNode(working_text, TextType.TEXT)) # any remaining text gets appended as a text node
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # only splitting "text" type objects
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        working_text = node.text # get text to separate
        for i in range(len(links)): #handles potential multiple images
            anchor_text, url = links[i][0], links[i][1]
            split = working_text.split(f"[{anchor_text}]({url})", 1) # split around image block
            before = split.pop(0) # get text before image block
            if before: # handles case where image block is at the start of node
                before_node = TextNode(before, TextType.TEXT)
                new_nodes.append(before_node)
            link_node = TextNode(anchor_text, TextType.LINK, url) # creates the image node
            new_nodes.append(link_node)
            working_text = split[0] # sets the text after the image block to continue working with if necessary
        if working_text: # will not trigger if image block is at the end of the node's text
            new_nodes.append(TextNode(working_text, TextType.TEXT)) # any remaining text gets appended as a text node

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    bold_nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    bold_italic_nodes = split_nodes_delimiter(bold_nodes, '_', TextType.ITALIC)
    delimited_nodes = split_nodes_delimiter(bold_italic_nodes, '`', TextType.CODE)
    delimited_images_nodes = split_nodes_image(delimited_nodes)
    final_nodes = split_nodes_link(delimited_images_nodes)
    return final_nodes

def markdown_to_blocks(markdown):
    blocks = []
    splits = markdown.split('\n\n')
    for split in splits:
        if split.strip() != '':
            blocks.append(split.strip())
    return blocks

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(block):
    if block.startswith('#'):
        HEADERS = ('#', '##', '###', '####', '#####', '######')
        header = block.split(maxsplit=1)
        if header[0] in HEADERS:
            return BlockType.HEADING
        else:
            return BlockType.PARAGRAPH
    if block.startswith('```'):
        code = block.split('```')
        if len(code) == 3 and block.endswith('```'):
            return BlockType.CODE
        return BlockType.PARAGRAPH
    lines = block.splitlines()
    if block.startswith('>'):
        for line in lines:
            if not line.startswith('>'):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith('- '):
        for line in lines:
            if not line.startswith('- '):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith('1. '):
        for index, line in enumerate(lines):
            if not line.startswith(f"{index + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH