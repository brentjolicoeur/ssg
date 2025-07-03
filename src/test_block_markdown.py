import unittest

from helpers import markdown_to_blocks


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