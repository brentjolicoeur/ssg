from textnode import TextNode, TextType

def main():
    node = TextNode("This is my test node.", TextType.ITALIC, "http://espn.com")
    print(node)


if __name__ == "__main__":
    main()