import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_is_htmlnode_subclass(self):
        node = ParentNode("div", [LeafNode("span", "child")])
        self.assertIsInstance(node, HTMLNode)

    def test_value_always_none(self):
        node = ParentNode("div", [LeafNode("span", "child")])
        self.assertIsNone(node.value)

    def test_constructor_sets_fields(self):
        children = [LeafNode("span", "child")]
        node = ParentNode("div", children, {"class": "greeting"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, {"class": "greeting"})

    def test_props_default_none(self):
        node = ParentNode("div", [LeafNode("span", "child")])
        self.assertIsNone(node.props)

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

    def test_to_html_three_levels_deep(self):
        leaf = LeafNode("i", "deep text")
        level3 = ParentNode("b", [leaf])
        level2 = ParentNode("span", [level3])
        level1 = ParentNode("div", [level2])
        self.assertEqual(
            level1.to_html(),
            "<div><span><b><i>deep text</i></b></span></div>",
        )

    def test_to_html_multiple_children(self):
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

    def test_to_html_preserves_children_order(self):
        node = ParentNode(
            "ul",
            [
                LeafNode("li", "first"),
                LeafNode("li", "second"),
                LeafNode("li", "third"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<ul><li>first</li><li>second</li><li>third</li></ul>",
        )

    def test_to_html_mixed_leaf_and_parent_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("span", "leaf sibling"),
                ParentNode("p", [LeafNode("b", "nested")]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><span>leaf sibling</span><p><b>nested</b></p></div>",
        )

    def test_to_html_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_none_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_grandchild_missing_children_raises(self):
        broken_child = ParentNode("span", None)
        parent_node = ParentNode("div", [broken_child])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_grandchild_missing_tag_raises(self):
        broken_child = ParentNode(None, [LeafNode("b", "text")])
        parent_node = ParentNode("div", [broken_child])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_leaf_child_no_value_raises(self):
        node = ParentNode("div", [LeafNode("span", None)])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_single_prop(self):
        node = ParentNode(
            "div", [LeafNode("span", "child")], {"class": "greeting"}
        )
        self.assertEqual(
            node.to_html(), '<div class="greeting"><span>child</span></div>'
        )

    def test_to_html_multiple_props(self):
        node = ParentNode(
            "a",
            [LeafNode(None, "click me")],
            {"href": "https://boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://boot.dev" target="_blank">click me</a>',
        )

    def test_to_html_empty_props_dict(self):
        node = ParentNode("div", [LeafNode("span", "child")], {})
        self.assertEqual(node.to_html(), "<div><span>child</span></div>")

    def test_to_html_nested_props_at_multiple_levels(self):
        child = ParentNode(
            "span", [LeafNode(None, "text")], {"id": "inner"}
        )
        parent = ParentNode("div", [child], {"class": "outer"})
        self.assertEqual(
            parent.to_html(),
            '<div class="outer"><span id="inner">text</span></div>',
        )

    def test_two_nodes_with_same_values_produce_same_html(self):
        node1 = ParentNode("div", [LeafNode("span", "child")])
        node2 = ParentNode("div", [LeafNode("span", "child")])
        self.assertEqual(node1.to_html(), node2.to_html())

    def test_to_html_special_characters_in_child_value(self):
        node = ParentNode("p", [LeafNode(None, "1 < 2 & 3 > 2")])
        self.assertEqual(node.to_html(), "<p>1 < 2 & 3 > 2</p>")

    def test_repr_contains_tag_and_props(self):
        node = ParentNode(
            "div", [LeafNode("span", "child")], {"class": "greeting"}
        )
        node_repr = repr(node)
        self.assertIn("div", node_repr)
        self.assertIn("greeting", node_repr)

    def test_repr_contains_children(self):
        child = LeafNode("span", "child")
        node = ParentNode("div", [child])
        node_repr = repr(node)
        self.assertIn("children", node_repr)


if __name__ == "__main__":
    unittest.main()
