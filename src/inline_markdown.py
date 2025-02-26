import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise Exception("Invalid Markdwon syntax--closing delimiter not found")
        
        for i in range(len(sections)):
            if not sections[i]:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
        
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue
        for image in images:
            image_alt, image_url = image[0], image[1]
            section = text.split(f"![{image_alt}]({image_url})", 1)
            if section[0]:
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, url=image_url))
            text = section[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(node)
            continue
        for link in links:
            link_text, link_url = link[0], link[1]
            section = text.split(f"[{link_text}]({link_url})", 1)
            if section[0]:
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url=link_url))
            text = section[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    start = [TextNode(text, TextType.TEXT)]

    delimited_bold = split_nodes_delimiter(start, "**", TextType.BOLD)
    delimited_bold_italic = split_nodes_delimiter(delimited_bold, "_", TextType.ITALIC)
    delimited_all = split_nodes_delimiter(delimited_bold_italic, "`", TextType.CODE)
    delimited_all_images = split_nodes_image(delimited_all)
    delimited_all_images_links = split_nodes_link(delimited_all_images)

    return delimited_all_images_links