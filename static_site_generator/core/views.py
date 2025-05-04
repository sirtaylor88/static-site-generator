"""Define views to serve."""

import os
from pathlib import Path

from static_site_generator.business.blocks import markdown_to_html_node


def extract_title(markdown: str) -> str:
    """Extract the title."""

    for line in markdown.split("\n\n"):
        if line.startswith("# "):
            return line.replace("# ", "", 1).strip()
        if line.startswith("#\t"):
            return line.replace("#\t", "", 1).strip()
    raise ValueError("No title found.")


def generate_page(
    from_path: Path, template_path: Path, dest_path: Path, base_path: Path
) -> None:
    """Generate page."""

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, encoding="utf-8") as sf:
        markdown = sf.read()

    with open(template_path, encoding="utf-8") as tf:
        template = tf.read()

    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()

    title = extract_title(markdown)
    html_content = (
        template.replace("{{ Content }}", content)
        .replace("{{ Title }}", title)
        .replace('href="/', f'href="{base_path}/')
        .replace('src="/', f'src="{base_path}/')
    )
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as df:
        df.write(html_content)


def generate_pages_recursive(
    dir_path_content: Path, template_path: Path, dest_dir_path: Path, base_path: Path
) -> None:
    """Generate page recursively."""
    for item in os.scandir(dir_path_content):
        source_path = Path(item.path)
        if os.path.isfile(item):
            generate_page(
                source_path, template_path, dest_dir_path / "index.html", base_path
            )
        else:
            generate_pages_recursive(
                source_path, template_path, dest_dir_path / item.name, base_path
            )
