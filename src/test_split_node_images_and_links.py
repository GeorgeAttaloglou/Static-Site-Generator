import unittest
from extract_images_and_links import extract_markdown_images, extract_markdown_links
from split_node_images_and_links import split_node_images, split_node_links
from textnode import TextNode, TextType


class TestSplitNodeImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_node_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images_passthrough(self):
        node = TextNode("just plain text, no images here", TextType.TEXT)
        self.assertListEqual([node], split_node_images([node]))

    def test_split_images_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        self.assertListEqual([node], split_node_images([node]))

    def test_split_images_leading_image(self):
        # Regression test: an image at the very start of the text (no
        # leading text before it) used to be silently dropped entirely.
        node = TextNode("![img](https://a.com/i.png) trailing text", TextType.TEXT)
        new_nodes = split_node_images([node])
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "https://a.com/i.png"),
                TextNode(" trailing text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_trailing_image_only(self):
        node = TextNode("leading text ![img](https://a.com/i.png)", TextType.TEXT)
        new_nodes = split_node_images([node])
        self.assertListEqual(
            [
                TextNode("leading text ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://a.com/i.png"),
            ],
            new_nodes,
        )

    def test_split_images_entire_text_is_image(self):
        # Regression test: with no text before or after the image, the
        # image node itself used to be dropped, returning [] instead.
        node = TextNode("![img](https://a.com/i.png)", TextType.TEXT)
        new_nodes = split_node_images([node])
        self.assertListEqual(
            [TextNode("img", TextType.IMAGE, "https://a.com/i.png")], new_nodes
        )

    def test_split_images_ignores_links_in_mixed_text(self):
        node = TextNode(
            "Here is ![img](https://a.com/i.png) and [link](https://a.com/l)",
            TextType.TEXT,
        )
        new_nodes = split_node_images([node])
        self.assertListEqual(
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://a.com/i.png"),
                TextNode(" and [link](https://a.com/l)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_empty_list(self):
        self.assertListEqual([], split_node_images([]))

    def test_split_images_mixed_batch_of_nodes(self):
        batch = [
            TextNode("no image here", TextType.TEXT),
            TextNode("![img](https://a.com/i.png)", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        new_nodes = split_node_images(batch)
        self.assertListEqual(
            [
                TextNode("no image here", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://a.com/i.png"),
                TextNode("already bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_images_duplicate_images(self):
        node = TextNode(
            "![dup](https://a.com/d.png) and ![dup](https://a.com/d.png)",
            TextType.TEXT,
        )
        new_nodes = split_node_images([node])
        self.assertListEqual(
            [
                TextNode("dup", TextType.IMAGE, "https://a.com/d.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("dup", TextType.IMAGE, "https://a.com/d.png"),
            ],
            new_nodes,
        )

    def test_split_images_empty_string_node_passthrough(self):
        node = TextNode("", TextType.TEXT)
        self.assertListEqual([node], split_node_images([node]))

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and another [second link](https://blog.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_node_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://blog.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_no_links_passthrough(self):
        node = TextNode("just plain text, no links here", TextType.TEXT)
        self.assertListEqual([node], split_node_links([node]))

    def test_split_links_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        self.assertListEqual([node], split_node_links([node]))

    def test_split_links_leading_link(self):
        # Regression test: same "dropped when at the very start" bug as
        # images, plus the delimiter used to be built with a stray "!"
        # (image syntax), which meant it could never be found in real
        # link text and every call raised ValueError.
        node = TextNode("[link](https://a.com) trailing text", TextType.TEXT)
        new_nodes = split_node_links([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://a.com"),
                TextNode(" trailing text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_trailing_link_only(self):
        node = TextNode("leading text [link](https://a.com)", TextType.TEXT)
        new_nodes = split_node_links([node])
        self.assertListEqual(
            [
                TextNode("leading text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://a.com"),
            ],
            new_nodes,
        )

    def test_split_links_entire_text_is_link(self):
        node = TextNode("[link](https://a.com)", TextType.TEXT)
        new_nodes = split_node_links([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://a.com")], new_nodes
        )

    def test_split_links_ignores_images_in_mixed_text(self):
        node = TextNode(
            "Here is ![img](https://a.com/i.png) and [link](https://a.com/l)",
            TextType.TEXT,
        )
        new_nodes = split_node_links([node])
        self.assertListEqual(
            [
                TextNode(
                    "Here is ![img](https://a.com/i.png) and ", TextType.TEXT
                ),
                TextNode("link", TextType.LINK, "https://a.com/l"),
            ],
            new_nodes,
        )

    def test_split_links_empty_list(self):
        self.assertListEqual([], split_node_links([]))

    def test_split_links_mixed_batch_of_nodes(self):
        batch = [
            TextNode("no link here", TextType.TEXT),
            TextNode("[link](https://a.com/l)", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        new_nodes = split_node_links(batch)
        self.assertListEqual(
            [
                TextNode("no link here", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://a.com/l"),
                TextNode("already bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_links_empty_string_node_passthrough(self):
        node = TextNode("", TextType.TEXT)
        self.assertListEqual([node], split_node_links([node]))