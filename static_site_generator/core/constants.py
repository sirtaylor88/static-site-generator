"""Module defining constants."""

import re
from enum import Enum


class TextType(Enum):
    """Define text types."""

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class BlockType(Enum):
    """Define block types."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class PATTERN(Enum):
    """Define regex patterns."""

    HEADING = re.compile(r"^(#{1,6})[^\S\r\n]+([\S ]+)")
    CODE = re.compile(r"^`{3}([\s\S]+)(`{3})$", re.MULTILINE)
