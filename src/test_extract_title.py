import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        self.assertEqual(extract_title("# Hello World"), "Hello World")

    def test_title_is_first_line_of_larger_document(self):
        md = "# My Title\n\nSome paragraph text here."
        self.assertEqual(extract_title(md), "My Title")

    def test_title_found_after_other_content(self):
        md = "Some intro text\n\n# The Real Title\n\nmore text"
        self.assertEqual(extract_title(md), "The Real Title")

    def test_returns_first_h1_when_multiple_present(self):
        md = "# First Title\n\nSome text\n\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")

    def test_h2_is_not_mistaken_for_h1(self):
        md = "## Not a title\n# Actual Title"
        self.assertEqual(extract_title(md), "Actual Title")

    def test_hash_without_space_is_not_a_heading(self):
        with self.assertRaises(Exception):
            extract_title("#NoSpaceHere")

    def test_no_h1_raises(self):
        md = "Just a paragraph.\n## A subheading\nMore text."
        with self.assertRaises(Exception):
            extract_title(md)

    def test_empty_string_raises(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_trailing_whitespace_is_stripped(self):
        self.assertEqual(
            extract_title("# Title with trailing spaces   "),
            "Title with trailing spaces",
        )

    def test_leading_extra_hash_in_title_is_preserved(self):
        # Regression test: line.strip("# ") used to strip a *set* of
        # characters, not a literal prefix, so any leading '#' inside the
        # title itself (after the required "# ") got eaten too.
        self.assertEqual(
            extract_title("# ## Nested-looking title"),
            "## Nested-looking title",
        )

    def test_trailing_hash_in_title_is_preserved(self):
        # Regression test: the same strip() bug also ate a trailing '#'
        # that was part of the actual title content.
        self.assertEqual(extract_title("# Rating: A#"), "Rating: A#")

    def test_title_with_inline_markdown_is_returned_raw(self):
        # extract_title just returns the raw heading text; it doesn't
        # process inline markdown like bold/italic.
        self.assertEqual(
            extract_title("# Title with **bold** word"),
            "Title with **bold** word",
        )


if __name__ == "__main__":
    unittest.main()