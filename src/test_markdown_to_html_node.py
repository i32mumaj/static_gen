import unittest

from block import markdown_to_html_node
from parentnode import ParentNode


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_returns_div_parent_node(self):
        node = markdown_to_html_node("Just a paragraph")
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "div")

    def test_empty_markdown(self):
        node = markdown_to_html_node("")
        self.assertEqual(node.to_html(), "<div></div>")

    def test_single_paragraph(self):
        md = "This is a simple paragraph."
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>This is a simple paragraph.</p></div>",
        )

    def test_paragraphs_with_inline_markdown(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_multiple_paragraphs(self):
        md = "First paragraph\n\nSecond paragraph\n\nThird paragraph"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>First paragraph</p><p>Second paragraph</p><p>Third paragraph</p></div>",
        )

    def test_headings_all_levels(self):
        md = """# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3>"
            "<h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )

    def test_heading_with_inline_markdown(self):
        md = "### This is a **bold** heading"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h3>This is a <b>bold</b> heading</h3></div>",
        )

    def test_code_block_no_inline_parsing(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>This is text that _should_ remain\n"
            "the **same** even with inline stuff\n</code></pre></div>",
        )

    def test_code_block_with_language_fence(self):
        md = "```python\nprint('hi')\n```"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>print('hi')\n</code></pre></div>",
        )

    def test_quote_block(self):
        md = "> This is a quote\n> with two lines"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote with two lines</blockquote></div>",
        )

    def test_quote_block_with_inline_markdown(self):
        md = "> a quote with **bold** and _italic_"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>a quote with <b>bold</b> and <i>italic</i></blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- item one\n- item two\n- item three"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>item one</li><li>item two</li><li>item three</li></ul></div>",
        )

    def test_unordered_list_with_inline_markdown(self):
        md = "- **bold** item\n- item with `code`"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li><b>bold</b> item</li><li>item with <code>code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_ordered_list_double_digits(self):
        md = "\n".join(f"{i}. item {i}" for i in range(1, 12))
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol>"
            + "".join(f"<li>item {i}</li>" for i in range(1, 12))
            + "</ol></div>",
        )

    def test_ordered_list_with_inline_markdown(self):
        md = "1. a [link](https://boot.dev)\n2. plain"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><ol><li>a <a href="https://boot.dev">link</a></li><li>plain</li></ol></div>',
        )

    def test_mixed_document(self):
        md = """# Title

This is an intro paragraph with **bold** text.

- first bullet
- second bullet

> a wise quote

```
code stays raw _here_
```

1. step one
2. step two"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<h1>Title</h1>"
            "<p>This is an intro paragraph with <b>bold</b> text.</p>"
            "<ul><li>first bullet</li><li>second bullet</li></ul>"
            "<blockquote>a wise quote</blockquote>"
            "<pre><code>code stays raw _here_\n</code></pre>"
            "<ol><li>step one</li><li>step two</li></ol>"
            "</div>",
        )

    def test_image_in_paragraph(self):
        md = "text with an ![alt](https://i.imgur.com/x.png) image"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><p>text with an <img src="https://i.imgur.com/x.png" alt="alt"></img> image</p></div>',
        )


if __name__ == "__main__":
    unittest.main()
