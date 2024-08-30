"""Test Text nodes."""

import pytest

from textnode import TextNode, text_node_to_html_node


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


@pytest.mark.parametrize(
    "text, node_type, url, expected",
    [
        ("", "text", None, ""),
        ("Renault", "bold", None, "<b>Renault</b>"),
        ("Alain", "italic", None, "<i>Alain</i>"),
        ("python3 -V", "code", None, "<code>python3 -V</code>"),
        (
            "Search",
            "link",
            "https://google.fr",
            '<a href="https://google.fr">Search</a>',
        ),
        (
            "Mona Lisa",
            "image",
            (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/"
                "Mona_Lisa.jpg/594px-Mona_Lisa.jpg"
            ),
            (
                '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/'
                '6/6a/Mona_Lisa.jpg/594px-Mona_Lisa.jpg" alt="Mona Lisa"></img>'
            ),
        ),
    ],
)
def test_convert_to_html_node(text, node_type, url, expected):
    """Test `text_node_to_html_node` method."""
    node = TextNode(text=text, text_type=node_type, url=url)
    assert text_node_to_html_node(node).to_html() == expected

    with pytest.raises(TypeError) as excinfo:
        text_node_to_html_node(TextNode("", "abc"))
    assert "Text type is not valid." in str(excinfo)
