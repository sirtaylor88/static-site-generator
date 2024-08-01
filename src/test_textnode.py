"""Test Text nodes."""

import pytest

from textnode import TextNode


@pytest.mark.parametrize(
    "n1, n2",
    [
        (["This is a text node", "bold"], ["This is a text node", "bold"]),
        (
            ["This is a text node", "bold", "https://google.com"],
            ["This is a text node", "bold", "https://google.com"],
        ),
    ],
)
def test_eq(n1, n2):
    """Test `__eq__` method."""
    node_1 = TextNode(*n1)
    node_2 = TextNode(*n2)
    assert node_1 == node_2


@pytest.mark.parametrize(
    "n1, n2",
    [
        (["This is a text node", "bold"], ["This is a text node", "italic"]),
        (
            ["This is a text node", "bold"],
            ["This is a text node", "bold", "https://google.com"],
        ),
        (
            ["This is a text node", "bold", "https://google.com"],
            ["This is a text node", "bold", "https://google.fr"],
        ),
    ],
)
def test_not_eq(n1, n2):
    """Test `__eq__` method."""
    node_1 = TextNode(*n1)
    node_2 = TextNode(*n2)
    assert node_1 != node_2


@pytest.mark.parametrize(
    "n, expected",
    [
        (["This is a text node", "bold"], "TextNode(This is a text node, bold, None)"),
        (
            ["This is a text node", "bold", "https://google.com"],
            "TextNode(This is a text node, bold, https://google.com)",
        ),
    ],
)
def test_repr(n, expected):
    """Test `__repr__` method."""
    node = TextNode(*n)
    assert str(node) == expected
