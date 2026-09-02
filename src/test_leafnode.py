import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_is_htmlnode_subclass(self):
        node = LeafNode("p", "Hello, world!")
        self.assertIsInstance(node, HTMLNode)

    def test_children_always_none(self):
        node = LeafNode("p", "Hello, world!", {"class": "greeting"})
        self.assertIsNone(node.children)

    def test_values_set(self):
        node = LeafNode("p", "Hello, world!", {"class": "greeting"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.props, {"class": "greeting"})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode(
            "a", "Click me!", {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_no_tag_with_props(self):
        node = LeafNode(None, "Just text", {"class": "ignored"})
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_empty_props(self):
        node = LeafNode("p", "Hello, world!", {})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Some text")
        self.assertEqual(node.to_html(), "<span>Some text</span>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Italic text")
        self.assertEqual(node.to_html(), "<i>Italic text</i>")

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src": "image.png", "alt": "An image"})
        self.assertEqual(
            node.to_html(), '<img src="image.png" alt="An image"></img>'
        )

    def test_leaf_to_html_single_prop(self):
        node = LeafNode("a", "boot.dev", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">boot.dev</a>')

    def test_repr_contains_fields(self):
        node = LeafNode("a", "click me", {"href": "https://boot.dev"})
        node_repr = repr(node)
        self.assertIn("a", node_repr)
        self.assertIn("click me", node_repr)
        self.assertIn("https://boot.dev", node_repr)

    def test_repr_no_children_field(self):
        node = LeafNode("p", "Hello, world!")
        node_repr = repr(node)
        self.assertNotIn("children", node_repr)

    def test_two_nodes_with_same_values(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), node2.to_html())

    def test_leaf_to_html_special_characters(self):
        node = LeafNode("p", "1 < 2 & 3 > 2")
        self.assertEqual(node.to_html(), "<p>1 < 2 & 3 > 2</p>")


if __name__ == "__main__":
    unittest.main()
