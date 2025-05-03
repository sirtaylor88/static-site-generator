"""Test Text nodes."""

import pytest

from static_site_generator.business.text_node import (
    TextNode,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)
from static_site_generator.constants import TextType


@pytest.mark.parametrize(
    "n1, n2",
    [
        (
            ["This is a text node", TextType.BOLD],
            ["This is a text node", TextType.BOLD],
        ),
        (
            ["This is a text node", TextType.BOLD, "https://google.com"],
            ["This is a text node", TextType.BOLD, "https://google.com"],
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
        ("", TextType.TEXT, None, ""),
        ("Renault", TextType.BOLD, None, "<b>Renault</b>"),
        ("Alain", TextType.ITALIC, None, "<i>Alain</i>"),
        ("python3 -V", TextType.CODE, None, "<code>python3 -V</code>"),
        (
            "Search",
            TextType.LINK,
            "https://google.fr",
            '<a href="https://google.fr">Search</a>',
        ),
        (
            "Mona Lisa",
            TextType.IMAGE,
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


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            [TextNode("Hello Tai, I'm here.", TextType.TEXT)],
            [TextNode("Hello Tai, I'm here.", TextType.TEXT)],
        ),
        (
            [TextNode("Hello **Tai**, I'm here.", TextType.TEXT)],
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("Tai", TextType.BOLD),
                TextNode(", I'm here.", TextType.TEXT),
            ],
        ),
        (
            [TextNode("Hello Tai, I'm **here.**", TextType.TEXT)],
            [
                TextNode("Hello Tai, I'm ", TextType.TEXT),
                TextNode("here.", TextType.BOLD),
            ],
        ),
    ],
)
def test_split_nodes_delimiter(data, expected):
    """Test that `split_nodes_delimiter` method works correctly."""
    assert split_nodes_delimiter(data, "**", TextType.BOLD) == expected

    with pytest.raises(TypeError) as excinfo:
        split_nodes_delimiter(data, "**", TextType.IMAGE)
    assert "Invalid text type." in str(excinfo)


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
        TextType.TEXT,
    )
    assert split_nodes_image([node]) == [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
        TextNode(" and ", TextType.TEXT),
        TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(".", TextType.TEXT),
    ]


def test_split_nodes_link():
    """Test that `split_nodes_link` method works correctly."""
    node = TextNode(
        (
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)."
        ),
        TextType.TEXT,
    )
    assert split_nodes_link([node]) == [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        TextNode(".", TextType.TEXT),
    ]


def test_text_to_textnodes():
    """Test that `text_to_textnodes` method works correctly."""
    text = (
        "This is **text** with an *italic* word and a `code block` "
        "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
        "and a [link](https://boot.dev)"
    )
    assert text_to_textnodes(text) == [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
    ]
