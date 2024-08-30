"""Useful methods."""

import re

from textnode import TextNode


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: str
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
        ValueError: if there is a missing closing delimiter.
    """
    result = []
    if text_type not in [TextNode.TEXT, TextNode.BOLD, TextNode.CODE, TextNode.ITALIC]:
        raise TypeError("Invalid text type.")

    for node in old_nodes:
        if node.text_type != TextNode.TEXT:
            result.append(node)
            continue
        if delimiter in node.text and node.text.count(delimiter) == 1:
            raise ValueError("Invalid markdown syntax.")

        substrings = node.text.split(delimiter, 2)
        if len(substrings) < 3:
            result.append(node)
            continue
        if substrings[0]:
            result.append(TextNode(substrings[0], TextNode.TEXT))
        result.append(TextNode(substrings[1], text_type))
        if substrings[2]:
            result.extend(
                split_nodes_delimiter(
                    [TextNode(substrings[2], TextNode.TEXT)], delimiter, text_type
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
        if node.text_type != TextNode.TEXT:
            result.append(node)
            continue

        image_data_list = extract_markdown_images(node.text)

        if not image_data_list:
            result.append(node)
            continue

        alt, src = image_data_list[0]
        substrings = node.text.split(f"![{alt}]({src})", 1)
        if substrings[0]:
            result.append(TextNode(substrings[0], TextNode.TEXT))
        result.append(TextNode(alt, TextNode.IMAGE, src))
        if substrings[1]:
            result.extend(split_nodes_image([TextNode(substrings[1], TextNode.TEXT)]))

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
        if node.text_type != TextNode.TEXT:
            result.append(node)
            continue

        link_data_list = extract_markdown_links(node.text)

        if not link_data_list:
            result.append(node)
            continue

        text, href = link_data_list[0]
        substrings = node.text.split(f"[{text}]({href})", 1)
        if substrings[0]:
            result.append(TextNode(substrings[0], TextNode.TEXT))
        result.append(TextNode(text, TextNode.LINK, href))
        if substrings[1]:
            result.extend(split_nodes_link([TextNode(substrings[1], TextNode.TEXT)]))

    return result


def text_to_textnodes(text: str) -> list[TextNode]:
    """Convert text to a list of TextNode.

    Args:
        text: A string.

    Returns:
        A list of TextNode instances.
    """
    node_list = split_nodes_image([TextNode(text, TextNode.TEXT)])
    node_list = split_nodes_link(node_list)
    node_list = split_nodes_delimiter(node_list, "**", TextNode.BOLD)
    node_list = split_nodes_delimiter(node_list, "*", TextNode.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextNode.CODE)
    return node_list
