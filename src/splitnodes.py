import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT or not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
        text_blocks = find_sub_blocks(node.text, delimiter)
        if not text_blocks:
            raise Exception("Delimiter not found in TextNode")
        for block in text_blocks:
            if block.startswith(delimiter):
                new_nodes.append(TextNode(block.strip(delimiter), text_type))
            else:
                new_nodes.append(TextNode(block, TextType.TEXT))

    return new_nodes

def find_sub_blocks(text, delimiter):
    delimited_locations = get_indices_of_delimited_blocks(text, delimiter)
    text_blocks = split_into_text_blocks(text, delimited_locations, delimiter)
    return text_blocks

def get_indices_of_delimited_blocks(text, delimiter):
    words = text.split()
    start_indices = []
    end_indices = []

    for i in range(len(words)):
        if words[i].startswith(delimiter):
            start_indices.append(i)
        if words[i].endswith(delimiter):
            end_indices.append(i)

    if len(start_indices) != len(end_indices):
        raise Exception("Invalid Markdwon syntax--closing delimiter not found")
    
    sub_block_indices = tuple(zip(start_indices, end_indices, strict=True))

    return sub_block_indices

def split_into_text_blocks(text, delimited_locations, delimiter):
    words = text.split()
    text_lists, text_blocks = [], []
    current_index = 0
    # this for loop creates lists of words split into sections based upon the occurence of the delimiter
    for i in range(len(delimited_locations)):
        if delimited_locations[i][0] == current_index:
            text_lists.append(words[:delimited_locations[i][1] + 1])
            current_index = delimited_locations[i][1] + 1
        else:
            text_lists.append(words[current_index : delimited_locations[i][0]])
            text_lists.append(words[delimited_locations[i][0] : delimited_locations[i][1] + 1])
            current_index = delimited_locations[i][1] + 1
        if i == len(delimited_locations) - 1:
            if words[current_index:] == []:
                continue
            text_lists.append(words[current_index:])
    # this for loop converts the lists of words into a list of multi-word strings
    for item in text_lists:
        if not text_blocks:
            if len(item) == 1:
                text_blocks.append(item[0])
            else:
                string = ''
                for word in item:
                    string += (word + ' ')
                if string.startswith(delimiter):
                    text_blocks.append(string.rstrip())
                else:
                    text_blocks.append(string)
        else:
            if len(item) == 1:
                if item[0].startswith(delimiter):
                    text_blocks.append(item[0])
                else:
                    text_blocks.append(' ' + item[0])
            else:
                string = ''
                for word in item:
                    string += (word + ' ')
                if string.startswith(delimiter):
                    text_blocks.append(string.rstrip())
                else:
                    text_blocks.append(' ' + string)
    
    text_blocks[-1] = text_blocks[-1].rstrip()
    return text_blocks

def extract_markdown_images(text):
    img_regex_pattern = r"\!(.*?)\)"
    alt_pattern = r"\[(.*?)]"
    url_pattern = r"\((.*)"
    matches = re.findall(img_regex_pattern, text)
    alt_texts, urls = [], []

    for match in matches:
        alt_texts.append(re.findall(alt_pattern, match))
        urls.append(re.findall(url_pattern, match))

    image_info = []

    for i in range(len(alt_texts)):
        new_image = (alt_texts[i][0], urls[i][0])
        image_info.append(new_image)

    return image_info

def extract_markdown_links(text):
    anchor_pattern = r"\[(.*?)]"
    url_pattern = r"\((.*?)\)"

    anchors = re.findall(anchor_pattern, text)
    urls = re.findall(url_pattern, text)

    links_info =[]
    for i in range(len(anchors)):
        new_image = (anchors[i], urls[i])
        links_info.append(new_image)

    return links_info

def split_nodes_image(old_nodes):
    pass

def split_nodes_link(old_nodes):
    pass