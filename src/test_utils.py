"""Unit tests for useful methods."""

import pytest

from textnode import TextNode
from utils import split_nodes_delimiter


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
    """test that `split_nodes_delimiter` method works correctly."""
    assert split_nodes_delimiter(data, "**", TextNode.BOLD) == expected
