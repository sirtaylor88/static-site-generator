"""Define text node."""

import re
import typing as tp

from static_site_generator.business.html_node import LeafNode
from static_site_generator.core.constants import TextType


class TextNode:
    """Text node."""

    def __init__(
        self, text: str, text_type: TextType, url: tp.Optional[str] = None
    ) -> None:
        """Inits TextNode."""
        self.text_content = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """Check if 2 instances are equals."""
        return (
            self.text_content == other.text_content
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        """String representantion of a TextNode instance."""
        return f"TextNode({self.text_content}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Convert TextNode to HTML Node.

    Args:
        text_node: A TextNode instance.

    Raises:
        TypeError if text type is not valid

    Returns:
        A HTMLNode instance.
    """

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(text_node.text_content)
        case TextType.BOLD:
            return LeafNode(text_node.text_content, tag="b")
        case TextType.ITALIC:
            return LeafNode(text_node.text_content, tag="i")
        case TextType.CODE:
            return LeafNode(text_node.text_content, tag="code")
        case TextType.LINK:
            return LeafNode(
                text_node.text_content,
                tag="a",
                props={
                    "href": text_node.url,
                },
            )
        case TextType.IMAGE:
            return LeafNode(
                "",
                tag="img",
                props={
                    "src": text_node.url,
                    "alt": text_node.text_content,
                },
            )
        case _:
            raise TypeError("Text type is not valid.")


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
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Extract images from markdown link.

    Args:
        text: A string.

    Returns:
        A list of tuple of anchor text and URL for each link.
    """
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
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
