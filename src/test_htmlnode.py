import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_default_values(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_values_set(self):
        node = HTMLNode(
            tag="p",
            value="Hello, world!",
            children=[],
            props={"class": "greeting"},
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "greeting"})

    def test_children_hold_htmlnodes(self):
        child = HTMLNode(tag="span", value="child")
        parent = HTMLNode(tag="div", children=[child])
        self.assertEqual(len(parent.children), 1)
        self.assertIs(parent.children[0], child)

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), 'href="https://boot.dev"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), 'href="https://boot.dev" target="_blank"'
        )

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        node = HTMLNode(tag="p", value="Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_repr_contains_fields(self):
        node = HTMLNode(
            tag="a",
            value="click me",
            children=None,
            props={"href": "https://boot.dev"},
        )
        node_repr = repr(node)
        self.assertIn("a", node_repr)
        self.assertIn("click me", node_repr)
        self.assertIn("https://boot.dev", node_repr)


if __name__ == "__main__":
    unittest.main()