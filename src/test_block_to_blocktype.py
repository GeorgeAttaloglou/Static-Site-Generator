import unittest
from block_to_blocktype import block_to_block_type
from blocktype import BlockType


class TestBlockToBlockType(unittest.TestCase):
    # --- headings ---
    def test_h1_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_h6_heading(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_h2_through_h5_headings(self):
        for hashes in ("##", "###", "####", "#####"):
            with self.subTest(hashes=hashes):
                self.assertEqual(
                    block_to_block_type(f"{hashes} Heading"), BlockType.HEADING
                )

    def test_seven_hashes_is_not_a_heading(self):
        # Markdown only supports h1-h6; 7 "#" characters isn't valid.
        self.assertEqual(
            block_to_block_type("####### Heading"), BlockType.PARAGRAPH
        )

    def test_hash_without_space_is_not_a_heading(self):
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    # --- code blocks ---
    def test_fenced_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_fenced_code_block_with_language_tag(self):
        block = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_single_line_triple_backticks_is_not_code(self):
        # Requires more than one line, so a lone "```" on its own line
        # doesn't count as a fenced block.
        self.assertEqual(block_to_block_type("```"), BlockType.PARAGRAPH)

    def test_unclosed_code_fence_is_not_code(self):
        block = "```\nprint('hello')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- quotes ---
    def test_single_line_quote(self):
        self.assertEqual(block_to_block_type("> a quote"), BlockType.QUOTE)

    def test_multi_line_quote(self):
        block = "> line one\n> line two\n> line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_with_one_non_quote_line_is_paragraph(self):
        block = "> line one\nline two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- unordered lists ---
    def test_unordered_list_single_item(self):
        self.assertEqual(block_to_block_type("- one item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple_items(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_with_one_bad_line_is_paragraph(self):
        block = "- item one\nitem two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_dash_without_space_is_not_unordered_list(self):
        self.assertEqual(block_to_block_type("-item"), BlockType.PARAGRAPH)

    # --- ordered lists ---
    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. only item"), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple_items(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_double_digit_numbering(self):
        block = "\n".join(f"{i}. item{i}" for i in range(1, 12))
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_not_starting_at_one_is_paragraph(self):
        block = "0. first\n1. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_skipped_number_is_paragraph(self):
        block = "1. first\n2. second\n4. fourth"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_out_of_order_is_paragraph(self):
        block = "1. first\n3. second\n2. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- plain paragraphs ---
    def test_plain_paragraph(self):
        block = "Just a normal paragraph of text with nothing special."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_multi_line_paragraph(self):
        block = "This is line one.\nThis is line two.\nThis is line three."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_string_is_paragraph(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
