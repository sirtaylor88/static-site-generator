"""Define text node."""

import typing as tp

from htmlnode import LeafNode


class TextNode:
    """Text node."""

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

    def __init__(self, text: str, text_type: str, url: tp.Optional[str] = None) -> None:
        """Inits TextNode."""
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """Check if 2 instances are equals."""
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        """String representantion of a TextNode instance."""
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


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
        case TextNode.TEXT:
            return LeafNode(text_node.text)
        case TextNode.BOLD:
            return LeafNode(text_node.text, tag="b")
        case TextNode.ITALIC:
            return LeafNode(text_node.text, tag="i")
        case TextNode.CODE:
            return LeafNode(text_node.text, tag="code")
        case TextNode.LINK:
            return LeafNode(text_node.text, tag="a", props={"href": text_node.url})
        case TextNode.IMAGE:
            return LeafNode(
                "", tag="img", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise TypeError("Text type is not valid.")
