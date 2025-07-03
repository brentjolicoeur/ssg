from textnode import TextType, TextNode

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