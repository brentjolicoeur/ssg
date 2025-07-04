import unittest

from markdown_funcs import markdown_to_blocks, markdown_to_html_node
from textnode_helpers import block_to_block_type, BlockType


class BlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n  \t\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_block(self):
        md = "This is a single block.\nIt has no blank lines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single block.\nIt has no blank lines."])

    def test_markdown_to_blocks_leading_trailing_newlines(self):
        md = """

# Heading One

Paragraph one.

Paragraph two.

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading One",
                "Paragraph one.",
                "Paragraph two.",
            ],
        )
    
    def test_markdown_to_blocks_excessive_newlines(self):
        md = """Block A


Block B



Block C"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block A",
                "Block B",
                "Block C",
            ],
        )

class BlockToBlockType(unittest.TestCase):
    def test_paragraph_block(self):
        block = "This is a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_block(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_code_block(self):
        block = '''```python
print("Hello, world!")
```'''
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = '''> This is a quote.
> It spans multiple lines.'''
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = '''- Item one
- Item two'''
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = '''1. First item
2. Second item'''
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_mixed_content_paragraph(self):
        # This block looks like a list or heading but isn't
        block = "This is not a list - because it doesn't start with a dash space."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "Not a heading# because no space after hash."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_block(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

class BlockToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
    
    def test_headings(self):
        md = """
# This is an h1 with **bold** text

## This is an h2 with _italic_ text

### This is an h3 with `code` text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><h1>This is an h1 with <b>bold</b> text</h1><h2>This is an h2 with <i>italic</i> text</h2><h3>This is an h3 with <code>code</code> text</h3></div>",
    )

    def test_blockquote(self):
        md = """
> This is a quote with **bold** text
> and multiple lines with _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><blockquote>This is a quote with <b>bold</b> text and multiple lines with <i>italic</i> text</blockquote></div>",
    )

    def test_unordered_list(self):
        md = """
- First item with **bold** text
- Second item with _italic_ text
- Third item with `code` text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><ul><li>First item with <b>bold</b> text</li><li>Second item with <i>italic</i> text</li><li>Third item with <code>code</code> text</li></ul></div>",
    )

    def test_ordered_list(self):
        md = """
1. First numbered item
2. Second numbered item with **bold**
3. Third numbered item with _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><ol><li>First numbered item</li><li>Second numbered item with <b>bold</b></li><li>Third numbered item with <i>italic</i></li></ol></div>",
    )


if __name__ == '__main__':
    unittest.main()