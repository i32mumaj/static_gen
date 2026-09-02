import unittest
from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("Test node", TextType.LINK)
        self.assertEqual(node.url, None)

    def test_not_eq_diff_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Click me", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Click me", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic")

    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("A description", TextType.IMAGE, "https://boot.dev/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://boot.dev/img.png", "alt": "A description"},
        )

    def test_invalid_text_type_raises(self):
        node = TextNode("Broken", TextType.BOLD)
        node.text_type = "not_a_text_type"
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block_in_middle(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic_delimiter(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_multiple_delimited_sections(self):
        node = TextNode("**a** and **b**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("a", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
            ],
        )

    def test_delimiter_at_start(self):
        node = TextNode("**bold** at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" at the start", TextType.TEXT),
            ],
        )

    def test_delimiter_at_end(self):
        node = TextNode("at the end **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("at the end ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_no_delimiter_present(self):
        node = TextNode("Plain text, nothing special", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("Plain text, nothing special", TextType.TEXT)])

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])

    def test_only_delimiters_no_content(self):
        node = TextNode("****", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This has `one unmatched delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_text_nodes_pass_through_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    def test_mixed_text_and_non_text_nodes(self):
        nodes = [
            TextNode("start `code` end", TextType.TEXT),
            TextNode("already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("start ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" end", TextType.TEXT),
                TextNode("already italic", TextType.ITALIC),
            ],
        )

    def test_multiple_old_nodes_all_text(self):
        nodes = [
            TextNode("`a`", TextType.TEXT),
            TextNode("`b`", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [TextNode("a", TextType.CODE), TextNode("b", TextType.CODE)],
        )

    def test_empty_old_nodes_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])

class TestSplitNodesImage(unittest.TestCase):

    def test_single_image(self):
        node = TextNode("Here is an image: ![alt text](image_url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is an image: ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "image_url"),
            ],
        )

    def test_no_images(self):
        node = TextNode("No images here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](image_url) and another ![second image](second_url)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "image_url"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "second_url"),
            ],
        )

    def test_image_at_start(self):
        node = TextNode("![alt](image_url) at the start", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("alt", TextType.IMAGE, "image_url"),
                TextNode(" at the start", TextType.TEXT),
            ],
        )

    def test_image_at_end(self):
        node = TextNode("at the end ![alt](image_url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("at the end ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "image_url"),
            ],
        )

    def test_adjacent_images_no_text_between(self):
        node = TextNode("![img1](url1)![img2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode("img2", TextType.IMAGE, "url2"),
            ],
        )

    def test_non_text_nodes_pass_through_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    def test_mixed_text_and_non_text_nodes(self):
        nodes = [
            TextNode("start ![alt](image_url) end", TextType.TEXT),
            TextNode("already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("start ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "image_url"),
                TextNode(" end", TextType.TEXT),
                TextNode("already italic", TextType.ITALIC),
            ],
        )

    def test_multiple_old_nodes_all_text(self):
        nodes = [
            TextNode("![a](url_a)", TextType.TEXT),
            TextNode("![b](url_b)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("a", TextType.IMAGE, "url_a"),
                TextNode("b", TextType.IMAGE, "url_b"),
            ],
        )

    def test_empty_old_nodes_list(self):
        self.assertEqual(split_nodes_image([]), [])

    def test_ignores_links_mixed_with_images(self):
        node = TextNode(
            "Start ![img](img_url) middle [link](link_url) end", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "img_url"),
                TextNode(" middle [link](link_url) end", TextType.TEXT),
            ],
        )

    def test_empty_alt_text(self):
        node = TextNode("An image: ![](image_url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("An image: ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "image_url"),
            ],
        )

    def test_duplicate_images(self):
        node = TextNode(
            "![dup](same_url) and again ![dup](same_url)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("dup", TextType.IMAGE, "same_url"),
                TextNode(" and again ", TextType.TEXT),
                TextNode("dup", TextType.IMAGE, "same_url"),
            ],
        )

class TestSplitNodesLink(unittest.TestCase):

    def test_single_link(self):
        node = TextNode("Here is a link: [link text](link_url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is a link: ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "link_url"),
            ],
        )

    def test_no_links(self):
        node = TextNode("No links here.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_link_at_start(self):
        node = TextNode("[link text](link_url) at the start", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("link text", TextType.LINK, "link_url"),
                TextNode(" at the start", TextType.TEXT),
            ],
        )

    def test_link_at_end(self):
        node = TextNode("at the end [link text](link_url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("at the end ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "link_url"),
            ],
        )

    def test_adjacent_links_no_text_between(self):
        node = TextNode("[link1](url1)[link2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("link2", TextType.LINK, "url2"),
            ],
        )

    def test_non_text_nodes_pass_through_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    def test_mixed_text_and_non_text_nodes(self):
        nodes = [
            TextNode("start [link text](link_url) end", TextType.TEXT),
            TextNode("already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("start ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "link_url"),
                TextNode(" end", TextType.TEXT),
                TextNode("already italic", TextType.ITALIC),
            ],
        )

    def test_multiple_old_nodes_all_text(self):
        nodes = [
            TextNode("[a](url_a)", TextType.TEXT),
            TextNode("[b](url_b)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("a", TextType.LINK, "url_a"),
                TextNode("b", TextType.LINK, "url_b"),
            ],
        )

    def test_empty_old_nodes_list(self):
        self.assertEqual(split_nodes_link([]), [])

    def test_ignores_images_mixed_with_links(self):
        node = TextNode(
            "Start ![img](img_url) middle [link](link_url) end", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Start ![img](img_url) middle ", TextType.TEXT),
                TextNode("link", TextType.LINK, "link_url"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_empty_link_text(self):
        node = TextNode("A link: [](link_url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("A link: ", TextType.TEXT),
                TextNode("", TextType.LINK, "link_url"),
            ],
        )

    def test_duplicate_links(self):
        node = TextNode(
            "[dup](same_url) and again [dup](same_url)", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("dup", TextType.LINK, "same_url"),
                TextNode(" and again ", TextType.TEXT),
                TextNode("dup", TextType.LINK, "same_url"),
            ],
        )

class TestTextToTextnodes(unittest.TestCase):

    def test_all_node_types_together(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_plain_text_only(self):
        self.assertEqual(
            text_to_textnodes("Just a plain sentence."),
            [TextNode("Just a plain sentence.", TextType.TEXT)],
        )

    def test_empty_string_yields_no_nodes(self):
        # An empty section is dropped by split_nodes_delimiter, so nothing remains.
        self.assertEqual(text_to_textnodes(""), [])

    def test_whitespace_only_text_is_preserved(self):
        self.assertEqual(
            text_to_textnodes("   "),
            [TextNode("   ", TextType.TEXT)],
        )

    def test_newlines_preserved_in_text(self):
        self.assertEqual(
            text_to_textnodes("line one\nline two"),
            [TextNode("line one\nline two", TextType.TEXT)],
        )

    def test_entire_string_is_bold(self):
        self.assertEqual(
            text_to_textnodes("**everything bold**"),
            [TextNode("everything bold", TextType.BOLD)],
        )

    def test_entire_string_is_a_link(self):
        self.assertEqual(
            text_to_textnodes("[only a link](https://boot.dev)"),
            [TextNode("only a link", TextType.LINK, "https://boot.dev")],
        )

    def test_entire_string_is_an_image(self):
        self.assertEqual(
            text_to_textnodes("![only an image](https://boot.dev/x.png)"),
            [TextNode("only an image", TextType.IMAGE, "https://boot.dev/x.png")],
        )

    def test_bold_at_start_and_end(self):
        self.assertEqual(
            text_to_textnodes("**a** middle **b**"),
            [
                TextNode("a", TextType.BOLD),
                TextNode(" middle ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
            ],
        )

    def test_multiple_of_each_inline_type(self):
        self.assertEqual(
            text_to_textnodes("**b1** _i1_ `c1` **b2** _i2_ `c2`"),
            [
                TextNode("b1", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("i1", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("c1", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("b2", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("i2", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("c2", TextType.CODE),
            ],
        )

    def test_bold_processed_before_italic(self):
        # "**" is consumed by the bold pass, so the inner text is not re-split.
        self.assertEqual(
            text_to_textnodes("**bold** and _italic_"),
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
        )

    def test_italic_inside_a_word(self):
        self.assertEqual(
            text_to_textnodes("a_b_c"),
            [
                TextNode("a", TextType.TEXT),
                TextNode("b", TextType.ITALIC),
                TextNode("c", TextType.TEXT),
            ],
        )

    def test_adjacent_image_and_link(self):
        self.assertEqual(
            text_to_textnodes("![img](i-url)[link](l-url)"),
            [
                TextNode("img", TextType.IMAGE, "i-url"),
                TextNode("link", TextType.LINK, "l-url"),
            ],
        )

    def test_link_and_image_with_same_text_and_url(self):
        self.assertEqual(
            text_to_textnodes("![x](u) then [x](u)"),
            [
                TextNode("x", TextType.IMAGE, "u"),
                TextNode(" then ", TextType.TEXT),
                TextNode("x", TextType.LINK, "u"),
            ],
        )

    def test_bold_immediately_followed_by_image(self):
        self.assertEqual(
            text_to_textnodes("**bold** ![img](url)"),
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url"),
            ],
        )

    def test_empty_alt_text_image(self):
        self.assertEqual(
            text_to_textnodes("see ![](url) here"),
            [
                TextNode("see ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "url"),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_empty_link_text(self):
        self.assertEqual(
            text_to_textnodes("see [](url) here"),
            [
                TextNode("see ", TextType.TEXT),
                TextNode("", TextType.LINK, "url"),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_unclosed_bold_delimiter_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("this is **unclosed bold")

    def test_unclosed_code_delimiter_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("this is `unclosed code")

    def test_lone_single_underscore_raises(self):
        # A stray "_" is treated as an unbalanced italic delimiter.
        with self.assertRaises(ValueError):
            text_to_textnodes("2 _ 3 = 6")

    def test_bold_inside_code_span_breaks_parsing(self):
        # Bold is split before code, so "`x = **y**`" leaves stray backticks
        # that then fail to balance during the code pass.
        with self.assertRaises(ValueError):
            text_to_textnodes("`x = **y**`")

    def test_formatting_inside_link_text_is_not_nested(self):
        # The bold pass runs first and eats the "**", so the "[...](...)"
        # pattern is broken up and never recognized as a link.
        self.assertEqual(
            text_to_textnodes("[**bold link**](https://boot.dev)"),
            [
                TextNode("[", TextType.TEXT),
                TextNode("bold link", TextType.BOLD),
                TextNode("](https://boot.dev)", TextType.TEXT),
            ],
        )

    def test_image_is_not_treated_as_link(self):
        self.assertEqual(
            text_to_textnodes("![pic](p-url) and [go](g-url)"),
            [
                TextNode("pic", TextType.IMAGE, "p-url"),
                TextNode(" and ", TextType.TEXT),
                TextNode("go", TextType.LINK, "g-url"),
            ],
        )

    def test_result_nodes_have_none_url_for_non_link_types(self):
        nodes = text_to_textnodes("plain **bold** `code` *italic*")
        for node in nodes:
            self.assertIsNone(node.url)

    def test_idempotent_on_already_plain_text(self):
        once = text_to_textnodes("nothing special here")
        twice = text_to_textnodes(once[0].text)
        self.assertEqual(once, twice)

    def test_text_between_two_images(self):
        self.assertEqual(
            text_to_textnodes("![a](ua) and ![b](ub)"),
            [
                TextNode("a", TextType.IMAGE, "ua"),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "ub"),
            ],
        )

    def test_code_span_containing_special_markdown_chars(self):
        self.assertEqual(
            text_to_textnodes("run `pip install -e .` now"),
            [
                TextNode("run ", TextType.TEXT),
                TextNode("pip install -e .", TextType.CODE),
                TextNode(" now", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()