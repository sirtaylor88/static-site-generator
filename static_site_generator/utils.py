"""Useful methods."""

import re

from static_site_generator.business.html_node import HTMLNode, LeafNode
from static_site_generator.business.text_node import TextNode, text_node_to_html_node
from static_site_generator.constants import PATTERN, BlockType, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """Split nodes based on delimiter.

    Args:
        old_nodes: A list of TextNode instances.
        delimiter: The delimiter string.
        text_type: The type of the text.

    Returns:
        A new list of TextNode instances.

    Raises:
        TypeError: if text type is not valid.
    """
    result = []
    if text_type not in [
        TextType.TEXT,
        TextType.BOLD,
        TextType.CODE,
        TextType.ITALIC,
    ]:
        raise TypeError("Invalid text type.")

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        if delimiter in node.text_content and node.text_content.count(delimiter) == 1:
            result.append(node)
            continue

        substrings = node.text_content.split(delimiter, 2)
        if len(substrings) < 3:
            result.append(node)
            continue
        if substrings[0]:
            result.append(TextNode(substrings[0], TextType.TEXT))
        result.append(TextNode(substrings[1], text_type))
        if substrings[2]:
            result.extend(
                split_nodes_delimiter(
                    [TextNode(substrings[2], TextType.TEXT)], delimiter, text_type
                )
            )

    return result


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Extract images from markdown text.

    Args:
        text: A string.

    Returns:
        A list of tuple of `src` and `alt` attributes for each image.
    """
    pattern = r"!\[(.*?)\]\((.*?)\)"
    re.findall(pattern, text)
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Extract images from markdown link.

    Args:
        text: A string.

    Returns:
        A list of tuple of anchor text and URL for each link.
    """
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    re.findall(pattern, text)
    return re.findall(pattern, text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split nodes having images.

    Args:
        old_nodes: A list of TextNode instances.

    Returns:
        A new list of TextNode instances.
    """
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        image_data_list = extract_markdown_images(node.text_content)

        if not image_data_list:
            result.append(node)
            continue

        alt, src = image_data_list[0]
        substrings = node.text_content.split(f"![{alt}]({src})", 1)
        if substrings[0]:
            result.append(TextNode(substrings[0], TextType.TEXT))
        result.append(TextNode(alt, TextType.IMAGE, src))
        if substrings[1]:
            result.extend(split_nodes_image([TextNode(substrings[1], TextType.TEXT)]))

    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split nodes having links.

    Args:
        old_nodes: A list of TextNode instances.

    Returns:
        A new list of TextNode instances.
    """
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        link_data_list = extract_markdown_links(node.text_content)

        if not link_data_list:
            result.append(node)
            continue

        text, href = link_data_list[0]
        substrings = node.text_content.split(f"[{text}]({href})", 1)
        if substrings[0]:
            result.append(TextNode(substrings[0], TextType.TEXT))
        result.append(TextNode(text, TextType.LINK, href))
        if substrings[1]:
            result.extend(split_nodes_link([TextNode(substrings[1], TextType.TEXT)]))

    return result


def text_to_textnodes(text: str) -> list[TextNode]:
    """Convert text to a list of TextNode.

    Args:
        text: A string.

    Returns:
        A list of TextNode instances.
    """
    node_list = split_nodes_image([TextNode(text, TextType.TEXT)])
    node_list = split_nodes_link(node_list)
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "*", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    return node_list


def markdowns_to_blocks(markdown: str) -> list[str]:
    """Convert a markdown text to blocks."""
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    return list(filter(None, blocks))


def block_to_block_type(markdown: str) -> BlockType:
    """Get block type."""

    if PATTERN.HEADING.value.match(markdown):
        return BlockType.HEADING
    if PATTERN.CODE.value.match(markdown):
        return BlockType.CODE
    lines = markdown.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{idx}. ") for idx, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def parse_paragraph(markdown: str) -> tuple[str, str]:
    """Get paragraph text and tag."""
    html_nodes = text_to_children(markdown.replace("\n", " "))
    text = "".join(node.to_html() for node in html_nodes)
    return text, "p"


def parse_heading(markdown: str) -> tuple[str, str]:
    """Get heading text and tag.

    Raises:
        ValueError if getting error.
    """
    m = PATTERN.HEADING.value.match(markdown)
    if not m:
        raise ValueError("Error parsing heading.")
    level = len(m.group(1))
    return m.group(2), f"h{level}"


def parse_quote(markdown) -> tuple[str, str]:
    """Get quote text and tag."""
    text = ""
    for line in markdown.split("\n"):
        line_text = line[1:].strip()
        html_nodes = text_to_children(line_text)
        line_text = "".join(node.to_html() for node in html_nodes)
        if not line_text:
            continue
        text += f"<p>{line_text}</p>"
    return text, "blockquote"


def parse_list(markdown: str, ordered: bool = False) -> tuple[str, str]:
    """Get list text and tag."""
    text = ""
    slice_index = 2
    tag = "ul"
    if ordered:
        slice_index = 3
        tag = "ol"

    for line in markdown.split("\n"):
        line_text = line[slice_index:].strip()
        if not line_text:
            continue
        text += f"<li>{line_text}</li>"
    return text, tag


def parse_code_block(markdown: str) -> tuple[str, str]:
    """Get code text and tag.

    Raises:
        ValueError if getting error.
    """
    m = PATTERN.CODE.value.match(markdown)
    if not m:
        raise ValueError("Error parsing code block.")
    return f"<code>{m.group(1).lstrip()}</code>", "pre"


def block_to_html_node(markdown: str, block_type: BlockType) -> HTMLNode:
    """Convert a text block to HTML node."""
    if block_type not in BlockType:
        raise ValueError

    match block_type:
        case BlockType.HEADING:
            text, tag = parse_heading(markdown)
        case BlockType.QUOTE:
            text, tag = parse_quote(markdown)
        case BlockType.UNORDERED_LIST:
            text, tag = parse_list(markdown)
        case BlockType.ORDERED_LIST:
            text, tag = parse_list(markdown, ordered=True)
        case BlockType.CODE:
            text, tag = parse_code_block(markdown)
        case _:
            text, tag = parse_paragraph(markdown)

    return LeafNode(text, tag=tag)


def text_to_children(text: str) -> list[HTMLNode]:
    """Convert a text to a list of HTMLNode."""
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """Convert markdown text to a HTML node."""
    blocks = markdowns_to_blocks(markdown)
    html_content = ""
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        html_content += html_node.to_html()

    return LeafNode(html_content, tag="div")
