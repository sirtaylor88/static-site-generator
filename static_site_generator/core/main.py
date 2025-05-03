"""Main program."""

from pathlib import Path

from static_site_generator.core.utils import copy_static


def main():
    """Main app."""
    copy_static(
        Path(__file__).parent.parent / "static",
        Path(__file__).parent.parent.parent / "public",
    )


main()
