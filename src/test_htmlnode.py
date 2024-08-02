"""Test HTML nodes."""

import pytest

from htmlnode import HTMLNode


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
