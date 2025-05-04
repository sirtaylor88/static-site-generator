"""Main program."""

import sys
from pathlib import Path

from static_site_generator.core.utils import copy_static
from static_site_generator.core.views import generate_pages_recursive


def main():
    """Main app."""

    args = sys.argv
    base_path = "/"
    if len(args) > 1:
        base_path = sys.argv[1]

    core_dir = Path(__file__).parent.parent
    root_dir = core_dir.parent

    copy_static(
        core_dir / "static",
        root_dir / "docs",
    )

    generate_pages_recursive(
        root_dir / "content",
        core_dir / "templates" / "template.html",
        root_dir / "docs",
        Path(base_path),
    )


main()
