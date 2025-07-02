from textnode import TextNode, TextType

def main():
    node1 = TextNode('this is some plain text', TextType.PLAIN)
    node2 = TextNode('this is bold text', TextType.BOLD)
    node3 = TextNode('this is a link', TextType.LINK, 'www.google.com')

    print(node1)
    print(node2)
    print(node3)

if __name__ == "__main__":
    main()