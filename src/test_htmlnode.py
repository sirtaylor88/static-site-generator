"""Test HTML nodes."""

import pytest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        # pylint: disable=no-value-for-parameter
        LeafNode()
        # pylint: enable=no-value-for-parameter
    assert "missing 1 required positional argument: 'value'" in str(excinfo)

    lnode = LeafNode("I am a Leaf Node")
    assert str(lnode) == "LeafNode(None, value: I am a Leaf Node, None)"
    assert lnode.children is None


@pytest.mark.parametrize(
    "n, expected",
    [
        (["I am a Leaf Node"], "I am a Leaf Node"),
        (["", "p"], "<p></p>"),
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
        LeafNode(None).to_html()
    assert "Leaf node must have a value." in str(excinfo)


def test_init_parent_node():
    """Test __init__ method for ParentNode"""
    with pytest.raises(TypeError) as excinfo:
        # pylint: disable=no-value-for-parameter
        ParentNode()
        # pylint: enable=no-value-for-parameter
    assert "missing 1 required positional argument: 'children'" in str(excinfo)

    lnode = LeafNode("Hello world")
    pnode = ParentNode([lnode], tag="h1")
    assert str(pnode) == (
        "ParentNode(h1, children: [LeafNode(None, value: Hello world, None)], None)"
    )


def test_parent_node_to_html():
    """Test `to_html` method from LeafNode."""

    child1 = LeafNode("Robert", tag="li")
    child2 = LeafNode("Alain", tag="li")

    pnode = ParentNode([child1, child2], tag="ul", props={"class": "text-center"})
    assert pnode.to_html() == (
        '<ul class="text-center"><li>Robert</li><li>Alain</li></ul>'
    )

    with pytest.raises(ValueError) as excinfo:
        ParentNode([], tag="p").to_html()
    assert "Parent node must have at least one child node." in str(excinfo)

    with pytest.raises(ValueError) as excinfo:
        ParentNode([child1]).to_html()
    assert "Parent node must have a tag." in str(excinfo)

    gnode = ParentNode([pnode], tag="div")
    assert gnode.to_html() == (
        '<div><ul class="text-center"><li>Robert</li><li>Alain</li></ul></div>'
    )
