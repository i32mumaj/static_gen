import unittest
from block import markdown_to_blocks, block_to_blocktype, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("   \n\t\n   "), [])

    def test_single_block_no_blank_lines(self):
        md = "Just a single paragraph of text"
        self.assertEqual(markdown_to_blocks(md), ["Just a single paragraph of text"])

    def test_leading_and_trailing_blank_lines(self):
        md = "\n\n\nHello world\n\n\n"
        self.assertEqual(markdown_to_blocks(md), ["Hello world"])

    def test_multiple_consecutive_blank_lines_between_blocks(self):
        md = "First block\n\n\n\nSecond block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block"],
        )

    def test_blank_line_with_spaces_is_a_separator(self):
        md = "First block\n   \nSecond block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block"],
        )

    def test_multiline_block_preserved(self):
        md = "line one\nline two\nline three"
        self.assertEqual(
            markdown_to_blocks(md),
            ["line one\nline two\nline three"],
        )

    def test_inner_line_whitespace_is_not_stripped(self):
        md = "  indented line  \n\nnext block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["  indented line  ", "next block"],
        )

    def test_heading_list_and_code_blocks(self):
        md = """# Heading

- item 1
- item 2

```
code here
```"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# Heading",
                "- item 1\n- item 2",
                "```\ncode here\n```",
            ],
        )

    def test_no_trailing_newline(self):
        md = "block one\n\nblock two"
        self.assertEqual(
            markdown_to_blocks(md),
            ["block one", "block two"],
        )


class TestBlockToBlockType(unittest.TestCase):
    # --- headings ---
    def test_heading_h1(self):
        self.assertEqual(block_to_blocktype("# Heading"), BlockType.HEADING)

    def test_heading_all_levels(self):
        for i in range(1, 7):
            block = "#" * i + " Heading"
            self.assertEqual(block_to_blocktype(block), BlockType.HEADING)

    def test_heading_seven_hashes_is_paragraph(self):
        self.assertEqual(block_to_blocktype("####### Too deep"), BlockType.PARAGRAPH)

    def test_heading_no_space_is_paragraph(self):
        self.assertEqual(block_to_blocktype("#Heading"), BlockType.PARAGRAPH)

    def test_heading_hash_only_is_paragraph(self):
        self.assertEqual(block_to_blocktype("#"), BlockType.PARAGRAPH)

    def test_heading_with_trailing_text_and_markup(self):
        self.assertEqual(
            block_to_blocktype("### This is a **bold** heading"), BlockType.HEADING
        )

    # --- code ---
    def test_code_block(self):
        self.assertEqual(
            block_to_blocktype("```\ncode here\n```"), BlockType.CODE
        )

    def test_code_block_with_language(self):
        self.assertEqual(
            block_to_blocktype("```python\nprint('hi')\n```"), BlockType.CODE
        )

    def test_code_block_multiple_lines(self):
        block = "```\nline one\nline two\nline three\n```"
        self.assertEqual(block_to_blocktype(block), BlockType.CODE)

    def test_code_block_single_line_backticks_is_paragraph(self):
        self.assertEqual(block_to_blocktype("```"), BlockType.PARAGRAPH)

    def test_code_block_only_opening_fence_is_paragraph(self):
        self.assertEqual(
            block_to_blocktype("```\nunclosed code"), BlockType.PARAGRAPH
        )

    def test_inline_code_is_not_code_block(self):
        self.assertEqual(
            block_to_blocktype("This has `inline code` in it"), BlockType.PARAGRAPH
        )

    # --- quote ---
    def test_quote_single_line(self):
        self.assertEqual(block_to_blocktype("> a quote"), BlockType.QUOTE)

    def test_quote_multi_line(self):
        self.assertEqual(
            block_to_blocktype("> line one\n> line two\n> line three"), BlockType.QUOTE
        )

    def test_quote_no_space_after_gt(self):
        self.assertEqual(block_to_blocktype(">no space\n>still a quote"), BlockType.QUOTE)

    def test_quote_one_line_missing_gt_is_paragraph(self):
        self.assertEqual(
            block_to_blocktype("> line one\nline two\n> line three"), BlockType.PARAGRAPH
        )

    # --- unordered list ---
    def test_unordered_list_single_item(self):
        self.assertEqual(block_to_blocktype("- item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple_items(self):
        self.assertEqual(
            block_to_blocktype("- one\n- two\n- three"), BlockType.UNORDERED_LIST
        )

    def test_unordered_list_dash_no_space_is_paragraph(self):
        self.assertEqual(block_to_blocktype("-one\n-two"), BlockType.PARAGRAPH)

    def test_unordered_list_one_bad_line_is_paragraph(self):
        self.assertEqual(
            block_to_blocktype("- one\ntwo\n- three"), BlockType.PARAGRAPH
        )

    def test_unordered_list_asterisk_is_paragraph(self):
        self.assertEqual(block_to_blocktype("* one\n* two"), BlockType.PARAGRAPH)

    # --- ordered list ---
    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_blocktype("1. item"), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple_items(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_blocktype(block), BlockType.ORDERED_LIST)

    def test_ordered_list_not_starting_at_one_is_paragraph(self):
        self.assertEqual(
            block_to_blocktype("2. one\n3. two"), BlockType.PARAGRAPH
        )

    def test_ordered_list_not_incrementing_is_paragraph(self):
        self.assertEqual(
            block_to_blocktype("1. one\n3. two\n4. three"), BlockType.PARAGRAPH
        )

    def test_ordered_list_wrong_order_is_paragraph(self):
        self.assertEqual(
            block_to_blocktype("1. one\n3. two\n2. three"), BlockType.PARAGRAPH
        )

    def test_ordered_list_no_space_after_dot_is_paragraph(self):
        self.assertEqual(block_to_blocktype("1.one\n2.two"), BlockType.PARAGRAPH)

    def test_ordered_list_long(self):
        block = "\n".join(f"{i}. item {i}" for i in range(1, 12))
        self.assertEqual(block_to_blocktype(block), BlockType.ORDERED_LIST)

    # --- paragraph ---
    def test_plain_paragraph(self):
        self.assertEqual(
            block_to_blocktype("Just a normal sentence."), BlockType.PARAGRAPH
        )

    def test_multiline_paragraph(self):
        self.assertEqual(
            block_to_blocktype("first line\nsecond line"), BlockType.PARAGRAPH
        )

    def test_empty_block_is_paragraph(self):
        self.assertEqual(block_to_blocktype(""), BlockType.PARAGRAPH)

    def test_paragraph_with_mixed_markers(self):
        self.assertEqual(
            block_to_blocktype("- a bullet\n> a quote\n1. a number"),
            BlockType.PARAGRAPH,
        )