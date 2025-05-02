"""Unit tests for useful methods."""

import pytest

from static_site_generator.business.text_node import TextNode
from static_site_generator.constants import BlockType, TextType
from static_site_generator.utils import (
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_html_node,
    markdowns_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


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


def test_markdowns_to_blocks():
    """Test that `markdowns_to_blocks` works correctly."""

    markdown_text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

    markdowns_to_blocks(markdown_text)

    assert markdowns_to_blocks(markdown_text) == [
        "This is **bolded** paragraph",
        (
            "This is another paragraph with _italic_ text and `code` here\n"
            "This is the same paragraph on a new line"
        ),
        "- This is a list\n- with items",
    ]


@pytest.mark.parametrize(
    "markdown_text, expected",
    [
        ("# h1", BlockType.HEADING),
        ("# h1 test", BlockType.HEADING),
        ("#\th1", BlockType.HEADING),
        ("#     \th1", BlockType.HEADING),
        ("## h2", BlockType.HEADING),
        ("### h3", BlockType.HEADING),
        ("#### h4", BlockType.HEADING),
        ("##### h5", BlockType.HEADING),
        ("###### h6", BlockType.HEADING),
        ("```pytest . ```", BlockType.CODE),
        ("```\npytest .\n```", BlockType.CODE),
        (">Hello", BlockType.QUOTE),
        ("> Hello\n> World", BlockType.QUOTE),
        ("- Hello", BlockType.UNORDERED_LIST),
        ("- Hello\n- World", BlockType.UNORDERED_LIST),
        ("1. Hello", BlockType.ORDERED_LIST),
        ("1. Hello\n2. World", BlockType.ORDERED_LIST),
        ("#", BlockType.PARAGRAPH),
        ("#h1", BlockType.PARAGRAPH),
        ("#\nh1", BlockType.PARAGRAPH),
        ("``pytest . ``", BlockType.PARAGRAPH),
        ("``````", BlockType.PARAGRAPH),
        ("> Hello\n World", BlockType.PARAGRAPH),
        ("- Hello\nWorld", BlockType.PARAGRAPH),
        ("2. Hello\n1. World", BlockType.PARAGRAPH),
    ],
)
def test_block_to_block_type(markdown_text, expected):
    """Test that `block_to_block_type` works correctly."""

    assert block_to_block_type(markdown_text) == expected


def test_paragraphs():
    """Test that `markdown_to_html_node` works correctly with paragraphs."""

    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    assert node.to_html() == (
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
        "<p>This is another paragraph with <i>italic</i> text and "
        "<code>code</code> here</p></div>"
    )


@pytest.mark.parametrize(
    "text, expected",
    [
        ("#    Hello world", "<div><h1>Hello world</h1></div>"),
        ("##    Hello world", "<div><h2>Hello world</h2></div>"),
        ("###    Hello world", "<div><h3>Hello world</h3></div>"),
        ("####    Hello world", "<div><h4>Hello world</h4></div>"),
        ("#####    Hello world", "<div><h5>Hello world</h5></div>"),
        ("######    Hello world", "<div><h6>Hello world</h6></div>"),
        ("#######    Hello world", "<div><p>#######    Hello world</p></div>"),
    ],
)
def test_heading(text, expected):
    """Test that `markdown_to_html_node` works correctly with heading."""

    node = markdown_to_html_node(text)
    assert node.to_html() == expected


def test_quotes():
    """Test that `markdown_to_html_node` works correctly with quote."""

    md = """
> hello world **_4 > 3**
>
>_6 > 5__
"""

    node = markdown_to_html_node(md)
    assert node.to_html() == (
        "<div><blockquote><p>hello world <b>_4 > 3</b></p><p><i>6 > 5</i>_</p>"
        "</blockquote></div>"
    )


def test_unordered_list():
    """Test that `markdown_to_html_node` works correctly with unordered list."""

    md = """
- bread
- salad
- fruits
"""

    node = markdown_to_html_node(md)
    assert node.to_html() == (
        "<div><ul><li>bread</li><li>salad</li><li>fruits</li></ul></div>"
    )


def test_ordered_list():
    """Test that `markdown_to_html_node` works correctly with ordered list."""

    md = """
1. bread
2. salad
3. fruits
"""

    node = markdown_to_html_node(md)
    assert node.to_html() == (
        "<div><ol><li>bread</li><li>salad</li><li>fruits</li></ol></div>"
    )


def test_codeblock():
    """Test that `markdown_to_html_node` works correctly with code block."""
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    assert node.to_html() == (
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with "
        "inline stuff\n</code></pre></div>"
    )
