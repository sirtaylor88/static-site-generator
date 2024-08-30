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
        A list of TextNode instances.
    """
    result = []
    for node in old_nodes:
        if node.text_type != TextNode.TEXT:
            result.append(node)
            continue

        if delimiter in node.text and node.text.count(delimiter) % 2 == 1:
            raise ValueError("Invalid markdown syntax.")

        texts = node.text.split(delimiter)
        for i, text in enumerate(texts):
            result.append(TextNode(text, TextNode.TEXT if i % 2 == 0 else text_type))

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
