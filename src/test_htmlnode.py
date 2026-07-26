import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_init(self):
        HTMLNode1 = HTMLNode('h1','This is a heading')
        self.assertEqual(str(HTMLNode1), 'HTMLNode(h1, This is a heading, None, None)')

    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_prop_to_html(self):
        HTMLNode1 = HTMLNode('h1','This is a heading',[HTMLNode()],{
            "href": "https://www.google.com",
            "target": "_blank",
            })

        self.assertEqual(HTMLNode1.prop_to_html(),  'href="https://www.google.com" target="_blank"')

    def test_prop_to_html_no_props(self):
        node = HTMLNode('p', 'text')
        self.assertEqual(node.prop_to_html(), '')

    def test_prop_to_html_empty_dict(self):
        node = HTMLNode('p', 'text', props={})
        self.assertEqual(node.prop_to_html(), '')

    def test_prop_to_html_single_prop(self):
        node = HTMLNode('a', 'link', props={'href': 'https://boot.dev'})
        self.assertEqual(node.prop_to_html(), 'href="https://boot.dev"')

    def test_to_html_not_implemented(self):
        node = HTMLNode('p', 'text')
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_with_children_and_props(self):
        child = HTMLNode('span', 'inner')
        node = HTMLNode('div', None, [child], {'class': 'container'})
        self.assertEqual(
            repr(node),
            f"HTMLNode(div, None, {[child]}, {{'class': 'container'}})",
        )

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag_returns_raw_value(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Click me!</a>',
        )

    def test_leaf_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_empty_string_value_is_valid(self):
        # Regression test: empty string is a legitimate value (e.g. an
        # <img> tag's content is always empty), so it must NOT raise.
        # Only a genuinely missing (None) value should raise.
        node = LeafNode("img", "", {"src": "https://a.com/i.png"})
        self.assertEqual(node.to_html(), '<img src="https://a.com/i.png"></img>')

    def test_leaf_children_is_always_none(self):
        node = LeafNode("p", "text")
        self.assertIsNone(node.children)

    def test_leaf_repr(self):
        node = LeafNode("p", "text", {"class": "greeting"})
        self.assertEqual(repr(node), "LeafNode(p, text, {'class': 'greeting'})")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_children_list_raises(self):
        # An empty list is falsy, so this hits the same "must have
        # children" check as passing None.
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_deeply_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [LeafNode("b", "bold"), LeafNode(None, " plain")],
                ),
                LeafNode("span", "sibling"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p><b>bold</b> plain</p><span>sibling</span></div>",
        )

    def test_repr(self):
        child = LeafNode("span", "child")
        node = ParentNode("div", [child], {"class": "wrapper"})
        self.assertEqual(
            repr(node),
            f"HTMLNode(div, None, {[child]}, {{'class': 'wrapper'}})",
        )

    def test_to_html_currently_ignores_own_props(self):
        # KNOWN QUIRK: ParentNode.to_html() never calls prop_to_html(), so
        # any props passed to a ParentNode are silently dropped from the
        # rendered output. This test documents that *current* behavior.
        # If props support gets added to ParentNode later, this test
        # should be updated (and will start failing) as a signal.
        node = ParentNode("div", [LeafNode("span", "child")], {"class": "wrapper"})
        self.assertEqual(node.to_html(), "<div><span>child</span></div>")