"""Define text node."""

import typing as tp


class TextNode:
    """Text node."""

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
