import unittest
from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_single_paragraph(self):
        md = "This is a simple paragraph."
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(), "<div><p>This is a simple paragraph.</p></div>"
        )

    def test_multi_line_paragraph_joins_with_space(self):
        # Lines within one block are joined with a space, not a newline.
        md = "This is line one.\nThis is line two."
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>This is line one. This is line two.</p></div>",
        )

    def test_paragraph_with_all_inline_markdown_types(self):
        md = (
            "Text with **bold**, _italic_, `code`, a [link](https://a.com), "
            "and an ![img](https://a.com/i.png)."
        )
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><p>Text with <b>bold</b>, <i>italic</i>, <code>code</code>, '
            'a <a href="https://a.com">link</a>, and an '
            '<img src="https://a.com/i.png" alt="img"></img>.</p></div>',
        )

    def test_heading_h1(self):
        node = markdown_to_html_node("# H1")
        self.assertEqual(node.to_html(), "<div><h1>H1</h1></div>")

    def test_heading_h6(self):
        node = markdown_to_html_node("###### Deepest heading")
        self.assertEqual(node.to_html(), "<div><h6>Deepest heading</h6></div>")

    def test_heading_does_not_have_leading_space(self):
        # Regression test: block[j:] used to include the space right
        # after the "#" markers, producing "<h2> Heading</h2>".
        node = markdown_to_html_node("## This is a heading")
        self.assertEqual(
            node.to_html(), "<div><h2>This is a heading</h2></div>"
        )

    def test_heading_with_inline_bold(self):
        node = markdown_to_html_node("## Heading with **bold** word")
        self.assertEqual(
            node.to_html(),
            "<div><h2>Heading with <b>bold</b> word</h2></div>",
        )

    def test_code_block_strips_fence_newlines(self):
        # Regression test: the newline immediately after the opening
        # fence and immediately before the closing fence used to be left
        # in the code content ("\nprint('hi')\n" instead of "print('hi')").
        md = "```\nprint('hi')\n```"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(), "<div><pre><code>print('hi')</code></pre></div>"
        )

    def test_code_block_does_not_process_inline_markdown(self):
        # Underscores/asterisks inside a code block must stay literal.
        md = "```\nthis _should_ stay **literal**\n```"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>this _should_ stay **literal**</code></pre></div>",
        )

    def test_quote_single_line(self):
        node = markdown_to_html_node("> a quote")
        self.assertEqual(
            node.to_html(), "<div><blockquote>a quote</blockquote></div>"
        )

    def test_quote_multi_line_strips_prefix_on_every_line(self):
        # Regression test: the literal "> " prefix used to be left in the
        # rendered text on every line of a multi-line quote.
        md = "> line one\n> line two"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>line one line two</blockquote></div>",
        )

    def test_quote_with_inline_bold(self):
        node = markdown_to_html_node("> A quote with **bold** text")
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>A quote with <b>bold</b> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- item one\n- item two"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>item one</li><li>item two</li></ul></div>",
        )

    def test_unordered_list_with_inline_formatting(self):
        md = "- item with **bold**\n- item with _italic_"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>item with <b>bold</b></li>"
            "<li>item with <i>italic</i></li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_ordered_list_with_inline_link(self):
        md = "1. see [here](https://a.com)\n2. second item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><ol><li>see <a href="https://a.com">here</a></li>'
            "<li>second item</li></ol></div>",
        )

    def test_full_document_with_every_block_type(self):
        md = """# Heading

This is a paragraph with **bold** and _italic_ text.

> A quote block

- item one
- item two

1. first
2. second

```
code block here
```"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<h1>Heading</h1>"
            "<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>"
            "<blockquote>A quote block</blockquote>"
            "<ul><li>item one</li><li>item two</li></ul>"
            "<ol><li>first</li><li>second</li></ol>"
            "<pre><code>code block here</code></pre>"
            "</div>",
        )

    def test_result_is_a_single_top_level_div(self):
        node = markdown_to_html_node("Some text")
        self.assertEqual(node.tag, "div")
