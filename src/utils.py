"""Useful methods."""

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
