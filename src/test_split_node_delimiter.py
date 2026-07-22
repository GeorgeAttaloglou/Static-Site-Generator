import unittest
from split_node_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType

class SplitDelimiterTest(unittest.TestCase):
    
    def test_default(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.TEXT),
            ])
    
    def test_multiple(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE_TEXT)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.TEXT)
            ])
    
    def test_italic(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.TEXT),
            ])

    def test_bold_delimiter(self):
        node = TextNode("a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ])

    def test_no_delimiter_present(self):
        # A plain node with no delimiter in it at all should pass through
        # unchanged as a single TEXT node, not raise an error.
        node = TextNode("plain text, nothing special", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("plain text, nothing special", TextType.TEXT),
            ])

    def test_delimiter_at_start(self):
        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" at the start", TextType.TEXT),
            ])

    def test_delimiter_at_end(self):
        node = TextNode("ends with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("ends with ", TextType.TEXT),
            TextNode("code", TextType.CODE_TEXT),
            ])

    def test_multiple_delimited_sections_in_one_node(self):
        node = TextNode("a `one` b `two` c", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.TEXT),
            TextNode("one", TextType.CODE_TEXT),
            TextNode(" b ", TextType.TEXT),
            TextNode("two", TextType.CODE_TEXT),
            TextNode(" c", TextType.TEXT),
            ])

    def test_entire_text_is_delimited(self):
        node = TextNode("`all code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [TextNode("all code", TextType.CODE_TEXT)])

    def test_unclosed_delimiter_raises(self):
        node = TextNode("this has an `unclosed code block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

    def test_three_delimiters_raises(self):
        # Three occurrences of the delimiter means the last one never
        # gets closed, so this should also raise.
        node = TextNode("`one` `two", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

    def test_empty_string_node_returns_nothing(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [])

    def test_empty_old_nodes_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE_TEXT), [])

    def test_non_text_node_passes_through_unchanged(self):
        # Nodes that aren't plain TEXT (already BOLD, ITALIC, etc.) should
        # be left alone even if their text happens to contain the delimiter.
        node = TextNode("already `bold`", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [TextNode("already `bold`", TextType.BOLD)])

    def test_mixed_batch_of_text_and_non_text_nodes(self):
        text_node = TextNode("a `code` here", TextType.TEXT)
        bold_node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([text_node, bold_node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" here", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            ])