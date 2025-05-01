"""Main program."""

from static_site_generator.business.textnode import TextNode


def main():
    """Main app."""
    text_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(text_node)
