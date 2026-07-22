import unittest
from extract_images_and_links import extract_markdown_images, extract_markdown_links

class TestExtractImagesAndLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "![one](https://a.com/1.png) and ![two](https://a.com/2.png)"
        )
        self.assertListEqual(
            [("one", "https://a.com/1.png"), ("two", "https://a.com/2.png")],
            matches,
        )

    def test_extract_no_images_returns_empty_list(self):
        matches = extract_markdown_images("just plain text with no images")
        self.assertListEqual([], matches)

    def test_extract_image_with_empty_alt_text(self):
        matches = extract_markdown_images("![](https://a.com/i.png)")
        self.assertListEqual([("", "https://a.com/i.png")], matches)

    def test_extract_image_with_empty_url(self):
        matches = extract_markdown_images("![alt]()")
        self.assertListEqual([("alt", "")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "[one](https://a.com/1) and [two](https://a.com/2)"
        )
        self.assertListEqual(
            [("one", "https://a.com/1"), ("two", "https://a.com/2")],
            matches,
        )

    def test_extract_no_links_returns_empty_list(self):
        matches = extract_markdown_links("just plain text with no links")
        self.assertListEqual([], matches)

    def test_extract_link_with_empty_text(self):
        matches = extract_markdown_links("[](https://a.com/l)")
        self.assertListEqual([("", "https://a.com/l")], matches)

    def test_extract_link_at_start_of_string(self):
        matches = extract_markdown_links("[start link](https://a.com) rest of text")
        self.assertListEqual([("start link", "https://a.com")], matches)

    def test_extract_link_with_query_params(self):
        matches = extract_markdown_links(
            "[search](https://a.com/search?q=test&x=1)"
        )
        self.assertListEqual(
            [("search", "https://a.com/search?q=test&x=1")], matches
        )

    def test_images_function_ignores_links(self):
        text = "Here is ![img](https://a.com/i.png) and [link](https://a.com/l)"
        self.assertListEqual(
            [("img", "https://a.com/i.png")], extract_markdown_images(text)
        )

    def test_links_function_ignores_images(self):
        text = "Here is ![img](https://a.com/i.png) and [link](https://a.com/l)"
        self.assertListEqual(
            [("link", "https://a.com/l")], extract_markdown_links(text)
        )

    def test_image_immediately_followed_by_link_no_space(self):
        text = "![img](https://a.com/i.png)[link](https://a.com/l)"
        self.assertListEqual(
            [("img", "https://a.com/i.png")], extract_markdown_images(text)
        )
        self.assertListEqual(
            [("link", "https://a.com/l")], extract_markdown_links(text)
        )

    def test_malformed_markdown_no_closing_bracket_does_not_match(self):
        # Missing "]" means neither pattern should match at all.
        text = "[not a link(https://a.com)"
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

    def test_malformed_markdown_missing_paren_does_not_match(self):
        text = "[text](https://a.com"
        self.assertListEqual([], extract_markdown_links(text))

    def test_exclamation_with_space_is_treated_as_link_not_image(self):
        # A "!" that isn't immediately followed by "[" doesn't form an
        # image marker, so this should be picked up by the links
        # extractor instead of the images one.
        text = "! [not an image](https://a.com)"
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual(
            [("not an image", "https://a.com")], extract_markdown_links(text)
        )