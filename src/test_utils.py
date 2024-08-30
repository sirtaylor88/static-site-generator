"""Unit tests for useful methods."""

import pytest

from textnode import TextNode
from utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


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
        (
            [TextNode("Hello Tai, I'm **here.**", TextNode.TEXT)],
            [
                TextNode("Hello Tai, I'm ", TextNode.TEXT),
                TextNode("here.", TextNode.BOLD),
            ],
        ),
    ],
)
def test_split_nodes_delimiter(data, expected):
    """Test that `split_nodes_delimiter` method works correctly."""
    assert split_nodes_delimiter(data, "**", TextNode.BOLD) == expected

    with pytest.raises(TypeError) as excinfo:
        split_nodes_delimiter(data, "**", TextNode.IMAGE)
    assert "Invalid text type." in str(excinfo)

    with pytest.raises(ValueError) as excinfo:
        split_nodes_delimiter(
            [TextNode("Hello Tai, **I'm here.", TextNode.TEXT)], "**", TextNode.BOLD
        )
    assert "Invalid markdown syntax." in str(excinfo)


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


def test_split_nodes_image():
    """Test that `split_nodes_image` method works correctly."""
    node = TextNode(
        (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)."
        ),
        TextNode.TEXT,
    )
    assert split_nodes_image([node]) == [
        TextNode("This is text with a ", TextNode.TEXT),
        TextNode("rick roll", TextNode.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
        TextNode(" and ", TextNode.TEXT),
        TextNode("obi wan", TextNode.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(".", TextNode.TEXT),
    ]


def test_split_nodes_link():
    """Test that `split_nodes_link` method works correctly."""
    node = TextNode(
        (
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)."
        ),
        TextNode.TEXT,
    )
    assert split_nodes_link([node]) == [
        TextNode("This is text with a link ", TextNode.TEXT),
        TextNode("to boot dev", TextNode.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextNode.TEXT),
        TextNode("to youtube", TextNode.LINK, "https://www.youtube.com/@bootdotdev"),
        TextNode(".", TextNode.TEXT),
    ]
