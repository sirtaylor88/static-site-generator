"""Unit tests for useful methods."""

import pytest

from textnode import TextNode
from utils import extract_markdown_images, extract_markdown_links, split_nodes_delimiter


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            [TextNode("Hello Tai, I'm here.", TextNode.TEXT)],
            [TextNode("Hello Tai, I'm here.", TextNode.TEXT)],
        ),
        (
            [TextNode("Hello **Tai**, I'm here.", TextNode.TEXT)],
            [
                TextNode("Hello ", TextNode.TEXT),
                TextNode("Tai", TextNode.BOLD),
                TextNode(", I'm here.", TextNode.TEXT),
            ],
        ),
    ],
)
def test_split_nodes_delimiter(data, expected):
    """Test that `split_nodes_delimiter` method works correctly."""
    assert split_nodes_delimiter(data, "**", TextNode.BOLD) == expected


def test_extract_markdown_images():
    """Test that `extract_markdown_images` method works correctly."""
    text = (
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
        "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    )
    assert extract_markdown_images(text) == [
        ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
        ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
    ]


def test_extract_markdown_links():
    """Test that `extract_markdown_links` method works correctly."""
    text = (
        "This is text with a link [to boot dev](https://www.boot.dev) and "
        "[to youtube](https://www.youtube.com/@bootdotdev)"
    )
    assert extract_markdown_links(text) == [
        ("to boot dev", "https://www.boot.dev"),
        ("to youtube", "https://www.youtube.com/@bootdotdev"),
    ]
