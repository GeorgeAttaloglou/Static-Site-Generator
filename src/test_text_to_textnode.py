import unittest
from text_to_textnode import text_to_textnode
from textnode import TextNode, TextType


class TestTextToTextnode(unittest.TestCase):
    def test_all_types_combined(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![image](https://i.imgur.com/fake.png) and a [link](https://boot.dev)"
        )
        new_nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/fake.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_plain_text_no_markdown(self):
        new_nodes = text_to_textnode("just plain text, nothing special")
        self.assertListEqual(
            [TextNode("just plain text, nothing special", TextType.TEXT)],
            new_nodes,
        )

    def test_bold_only(self):
        new_nodes = text_to_textnode("This is **bold** text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_italic_only(self):
        new_nodes = text_to_textnode("This is _italic_ text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_code_only(self):
        new_nodes = text_to_textnode("This is `code` text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE_TEXT),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_only(self):
        new_nodes = text_to_textnode("This is ![img](https://a.com/i.png) text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://a.com/i.png"),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_only(self):
        new_nodes = text_to_textnode("This is [link](https://a.com/l) text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://a.com/l"),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_bold_sections(self):
        new_nodes = text_to_textnode("**one** and **two**")
        self.assertListEqual(
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_empty_string_returns_empty_list(self):
        self.assertListEqual([], text_to_textnode(""))

    def test_underscore_inside_image_url_does_not_break_parsing(self):
        # Regression test: underscores are very common in real URLs
        # (e.g. filenames). If italic-delimiter splitting ran before
        # image/link extraction, a lone "_" inside a URL would be
        # mistaken for an unclosed italic delimiter and raise.
        new_nodes = text_to_textnode(
            "Check this ![img](https://a.com/some_page.png) out"
        )
        self.assertListEqual(
            [
                TextNode("Check this ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://a.com/some_page.png"),
                TextNode(" out", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_underscore_inside_link_url_does_not_break_parsing(self):
        new_nodes = text_to_textnode(
            "Check this [link](https://a.com/some_page) out"
        )
        self.assertListEqual(
            [
                TextNode("Check this ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://a.com/some_page"),
                TextNode(" out", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_underscore_inside_bold_text_is_not_re_split(self):
        # Once "bold_word" becomes a single BOLD node, the later italic
        # ("_") pass must not reach back into it and split it further,
        # since split_nodes_delimiter skips non-TEXT nodes entirely.
        new_nodes = text_to_textnode("This is **bold_word** here")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold_word", TextType.BOLD),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_unclosed_bold_delimiter_raises(self):
        with self.assertRaises(Exception):
            text_to_textnode("This has **unclosed bold")

    def test_unclosed_italic_delimiter_raises(self):
        with self.assertRaises(Exception):
            text_to_textnode("This has _unclosed italic")

    def test_unclosed_code_delimiter_raises(self):
        with self.assertRaises(Exception):
            text_to_textnode("This has `unclosed code")

    def test_image_and_link_adjacent_with_no_space(self):
        new_nodes = text_to_textnode(
            "![img](https://a.com/i.png)[link](https://a.com/l)"
        )
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "https://a.com/i.png"),
                TextNode("link", TextType.LINK, "https://a.com/l"),
            ],
            new_nodes,
        )

    def test_bold_and_italic_adjacent_with_no_space(self):
        new_nodes = text_to_textnode("**bold**_italic_")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()