import re
from enum import Enum

from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    lines = markdown.splitlines()
    blocks = []
    current_block = []
    for line in lines:
        if line.strip() == "":
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        else:
            current_block.append(line)
    if current_block:
        blocks.append("\n".join(current_block))
    return blocks

def block_to_blocktype(block: str) -> BlockType:
    lines = block.split("\n")

    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING

    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text: str) -> list:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def paragraph_to_html_node(block: str) -> ParentNode:
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block: str) -> ParentNode:
    level = len(block.split(" ")[0])
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    inner = "\n".join(lines[1:-1])
    if inner:
        inner += "\n"
    code = text_node_to_html_node(TextNode(inner, TextType.TEXT))
    return ParentNode("pre", [ParentNode("code", [code])])


def quote_to_html_node(block: str) -> ParentNode:
    stripped = []
    for line in block.split("\n"):
        stripped.append(line.lstrip(">").strip())
    text = " ".join(stripped)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block: str) -> ParentNode:
    items = []
    for line in block.split("\n"):
        text = line[2:]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


def ordered_list_to_html_node(block: str) -> ParentNode:
    items = []
    for line in block.split("\n"):
        text = line.split(". ", 1)[1]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_blocktype(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)

