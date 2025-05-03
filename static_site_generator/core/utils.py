"""Define useful methods."""

import os
import shutil
from pathlib import Path


def copy_static(source: Path, destination: Path) -> None:
    """Copy static files."""
    print(source)
    print(destination)
    if os.path.exists(destination):
        for item in os.scandir(destination):
            if os.path.isfile(item):
                os.remove(item)
            else:
                shutil.rmtree(item)
    else:
        os.mkdir(destination)

    if os.path.exists(source):
        shutil.copytree(source, destination, dirs_exist_ok=True)
    else:
        raise ValueError()
