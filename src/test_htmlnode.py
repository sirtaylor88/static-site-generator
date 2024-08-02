"""Test HTML nodes."""

import pytest

from htmlnode import HTMLNode, LeafNode


@pytest.mark.parametrize(
    "props, expected",
    [
        (
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
            'href="https://www.google.com" target="_blank"',
        ),
        ({}, ""),
    ],
)
def test_props_to_html(props, expected):
    """Test __eq__ method."""
    node = HTMLNode(props=props)
    assert node.props_to_html() == expected


@pytest.mark.parametrize(
    "n, expected",
    [
        ([], "HTMLNode(None, None, None, None)"),
        (["h1", None, None, None], "HTMLNode(h1, None, None, None)"),
        (
            ["p", "Hello world", None, None],
            "HTMLNode(p, Hello world, None, None)",
        ),
        (
            ["p", "Hello world", None, {"class": "text-center"}],
            "HTMLNode(p, Hello world, None, {'class': 'text-center'})",
        ),
    ],
)
def test_repr(n, expected):
    """Test __repr__ method."""
    node = HTMLNode(*n)
    assert str(node) == expected


def test_init_leaf_node():
    """Test __init__ method for LeafNode"""
    with pytest.raises(TypeError) as excinfo:
        LeafNode()
    assert "missing 1 required positional argument: 'value'" in str(excinfo)

    lnode = LeafNode("I am a Leaf Node")
    assert str(lnode) == "HTMLNode(None, I am a Leaf Node, None, None)"
    assert lnode.children is None


@pytest.mark.parametrize(
    "n, expected",
    [
        (["I am a Leaf Node"], "I am a Leaf Node"),
        (["I am a Leaf Node", "p"], "<p>I am a Leaf Node</p>"),
        (
            ["I am a Leaf Node", "p", {"class": "text-center"}],
            '<p class="text-center">I am a Leaf Node</p>',
        ),
    ],
)
def test_leaf_node_to_html(n, expected):
    """Test `to_html` method from LeafNode."""
    lnode = LeafNode(*n)
    assert lnode.to_html() == expected

    with pytest.raises(ValueError) as excinfo:
        LeafNode("").to_html()
    assert "Leaf node must have a value." in str(excinfo)
