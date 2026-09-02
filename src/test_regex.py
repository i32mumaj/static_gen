from regex import extract_markdown_images, extract_markdown_links
import unittest

class TestMarkdownRegex(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "Here is an image: ![alt text](image_url)"
        expected = [("alt text", "image_url")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "Here is a link: [link text](link_url)"
        expected = [("link text", "link_url")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_multiple_images(self):
        text = "![img1](url1) and ![img2](url2)"
        expected = [("img1", "url1"), ("img2", "url2")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_multiple_links(self):
        text = "[link1](url1) and [link2](url2)"
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_matches(self):
        text = "No images or links here."
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])

    def test_empty_string(self):
        self.assertEqual(extract_markdown_images(""), [])
        self.assertEqual(extract_markdown_links(""), [])

    def test_images_and_links_together(self):
        text = "This is text with a ![image](img_url) and a [link](link_url)"
        self.assertEqual(extract_markdown_images(text), [("image", "img_url")])
        self.assertEqual(extract_markdown_links(text), [("link", "link_url")])

    def test_links_do_not_capture_images(self):
        text = "![only an image](img_url)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_images_do_not_capture_links(self):
        text = "[only a link](link_url)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_adjacent_images_no_separator(self):
        text = "![img1](url1)![img2](url2)"
        expected = [("img1", "url1"), ("img2", "url2")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_adjacent_links_no_separator(self):
        text = "[link1](url1)[link2](url2)"
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_adjacent_image_then_link_no_separator(self):
        text = "![img](img_url)[link](link_url)"
        self.assertEqual(extract_markdown_images(text), [("img", "img_url")])
        self.assertEqual(extract_markdown_links(text), [("link", "link_url")])

    def test_exclamation_with_space_before_link_still_matches(self):
        text = "Wow! [link](url) that is exciting"
        self.assertEqual(extract_markdown_links(text), [("link", "url")])

    def test_empty_alt_text(self):
        text = "![](image_url)"
        self.assertEqual(extract_markdown_images(text), [("", "image_url")])

    def test_empty_link_text(self):
        text = "[](link_url)"
        self.assertEqual(extract_markdown_links(text), [("", "link_url")])

    def test_empty_url_image(self):
        text = "![alt text]()"
        self.assertEqual(extract_markdown_images(text), [("alt text", "")])

    def test_empty_url_link(self):
        text = "[link text]()"
        self.assertEqual(extract_markdown_links(text), [("link text", "")])

    def test_both_empty_image(self):
        text = "![]()"
        self.assertEqual(extract_markdown_images(text), [("", "")])

    def test_both_empty_link(self):
        text = "[]()"
        self.assertEqual(extract_markdown_links(text), [("", "")])

    def test_nested_brackets_do_not_match_image(self):
        text = "![[nested]](url)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_nested_brackets_do_not_match_link(self):
        text = "[[nested]](url)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_url_with_query_string(self):
        text = "![alt](https://example.com/img.png?w=100&h=200)"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt", "https://example.com/img.png?w=100&h=200")],
        )

    def test_alt_text_with_punctuation_and_numbers(self):
        text = "![Photo #1: a cat, sitting.](url)"
        self.assertEqual(
            extract_markdown_images(text),
            [("Photo #1: a cat, sitting.", "url")],
        )

    def test_bracket_without_parens_not_a_link(self):
        text = "This is [not a link] on its own."
        self.assertEqual(extract_markdown_links(text), [])
        self.assertEqual(extract_markdown_images(text), [])

    def test_parens_without_brackets_not_a_link(self):
        text = "This is (not a link) on its own."
        self.assertEqual(extract_markdown_links(text), [])
        self.assertEqual(extract_markdown_images(text), [])

    def test_image_at_start_of_string(self):
        text = "![alt](url) starts here"
        self.assertEqual(extract_markdown_images(text), [("alt", "url")])

    def test_link_at_start_of_string(self):
        text = "[text](url) starts here"
        self.assertEqual(extract_markdown_links(text), [("text", "url")])

    def test_multiple_images_and_links_interleaved(self):
        text = "[l1](u1) ![i1](u2) [l2](u3) ![i2](u4)"
        self.assertEqual(
            extract_markdown_links(text), [("l1", "u1"), ("l2", "u3")]
        )
        self.assertEqual(
            extract_markdown_images(text), [("i1", "u2"), ("i2", "u4")]
        )

if __name__ == "__main__":
    unittest.main()
