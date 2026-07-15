import unittest
from htmlnode import HTMLNode, LeafNode

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