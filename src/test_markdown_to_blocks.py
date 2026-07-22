import unittest
from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_multiple_block_types(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        self.assertListEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
        )

    def test_single_block_no_blank_lines(self):
        self.assertListEqual(
            markdown_to_blocks("Just one block of text"),
            ["Just one block of text"],
        )

    def test_empty_string_returns_empty_list(self):
        self.assertListEqual(markdown_to_blocks(""), [])

    def test_whitespace_only_string_returns_empty_list(self):
        self.assertListEqual(markdown_to_blocks("   \n  "), [])

    def test_strips_leading_and_trailing_whitespace_from_each_block(self):
        # Regression test: block.strip (missing parentheses) never
        # actually called the method, and reassigning the loop variable
        # never mutated the original list anyway, so whitespace used to
        # survive untouched.
        md = "  # Heading with spaces  \n\nSome text.  "
        self.assertListEqual(
            markdown_to_blocks(md),
            ["# Heading with spaces", "Some text."],
        )

    def test_extra_blank_lines_between_blocks_collapse(self):
        # Regression test: three blank lines (more than one "\n\n" pair)
        # used to leave a stray '' block behind, because .remove('') only
        # removes a single occurrence.
        md = "Block one\n\n\n\nBlock two"
        self.assertListEqual(markdown_to_blocks(md), ["Block one", "Block two"])

    def test_many_consecutive_blank_lines_all_collapse(self):
        md = "Block one\n\n\n\n\n\nBlock two"
        self.assertListEqual(markdown_to_blocks(md), ["Block one", "Block two"])

    def test_whitespace_only_block_between_real_blocks_is_dropped(self):
        # Regression test: a block containing only spaces (not an exact
        # empty string) used to slip past the '' in blocks check.
        md = "Block one\n\n   \n\nBlock two"
        self.assertListEqual(markdown_to_blocks(md), ["Block one", "Block two"])

    def test_leading_blank_lines_at_start_of_document(self):
        md = "\n\nBlock one\n\nBlock two"
        self.assertListEqual(markdown_to_blocks(md), ["Block one", "Block two"])

    def test_trailing_blank_lines_at_end_of_document(self):
        md = "Block one\n\nBlock two\n\n"
        self.assertListEqual(markdown_to_blocks(md), ["Block one", "Block two"])

    def test_single_newlines_within_a_block_are_preserved(self):
        # Only a blank line (double newline) separates blocks; a single
        # newline is just a line break within the same block and must
        # not be split on.
        md = "line one\nline two\nline three"
        self.assertListEqual(markdown_to_blocks(md), ["line one\nline two\nline three"])

    def test_heading_and_paragraph_two_blocks(self):
        md = "# Heading\n\nA paragraph of text."
        self.assertListEqual(
            markdown_to_blocks(md), ["# Heading", "A paragraph of text."]
        )

    def test_returns_new_list_not_mutating_caller_expectations(self):
        # Sanity check that the return value is a plain list of strings
        # in document order, independent of any internal implementation
        # detail.
        md = "one\n\ntwo\n\nthree"
        result = markdown_to_blocks(md)
        self.assertEqual(result, ["one", "two", "three"])
        self.assertIsInstance(result, list)
        for block in result:
            self.assertIsInstance(block, str)
