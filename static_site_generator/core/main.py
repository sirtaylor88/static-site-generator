"""Main program."""

from static_site_generator.business.text_node import TextNode
from static_site_generator.core.constants import TextType


def main():
    """Main app."""
    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(text_node)
