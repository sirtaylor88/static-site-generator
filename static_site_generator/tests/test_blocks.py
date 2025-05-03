"""Unit tests for useful methods."""

import pytest

from static_site_generator.business.blocks import (
    block_to_block_type,
    markdown_to_html_node,
    markdowns_to_blocks,
)
from static_site_generator.constants import BlockType


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
