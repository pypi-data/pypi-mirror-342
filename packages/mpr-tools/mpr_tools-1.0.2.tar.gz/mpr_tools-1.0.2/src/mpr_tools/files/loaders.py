"""Tools for loading files"""

from pathlib import Path
import json

import yaml

from .ext import get_extension


LOADERS = {"yml": yaml.safe_load, "yaml": yaml.safe_load, "json": json.load}


def load_dict_from_file(filename: Path | str) -> dict:
    """Returns the dict loaded from a file"""

    ext = get_extension(filename)

    loader = LOADERS[ext]

    with open(filename, "r", encoding="utf-8") as content:
        return loader(content)
