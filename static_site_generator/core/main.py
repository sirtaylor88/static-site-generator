"""Main program."""

from pathlib import Path

from static_site_generator.core.utils import copy_static
from static_site_generator.core.views import generate_page


def main():
    """Main app."""

    core_dir = Path(__file__).parent.parent
    root_dir = core_dir.parent

    copy_static(
        core_dir / "static",
        root_dir / "public",
    )

    generate_page(
        root_dir / "content" / "index.md",
        core_dir / "templates" / "template.html",
        root_dir / "public" / "index.html",
    )


main()
