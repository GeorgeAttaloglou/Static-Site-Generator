import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_init(self):
        HTMLNode1 = HTMLNode('h1','This is a heading')
        self.assertEqual(str(HTMLNode1), 'HTMLNode(h1, This is a heading, None, None)')

    def test_prop_to_html(self):
        HTMLNode1 = HTMLNode('h1','This is a heading',[HTMLNode()],{
            "href": "https://www.google.com",
            "target": "_blank",
            })

        self.assertEqual(HTMLNode1.prop_to_html(),  'href="https://www.google.com" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

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