"""Tools for file extensions"""

from pathlib import Path


SUFFIX_OVERRIDE = {"yaml": "yml"}


def get_extension(filename: Path | str) -> str:
    """returns the file extension"""

    if isinstance(filename, str):
        filename = Path(filename)

    suffixes = filename.suffixes
    if suffixes:
        suffixes[0] = suffixes[0].replace(".", "")

    full_suffix = "".join(suffixes)

    return SUFFIX_OVERRIDE.get(full_suffix, full_suffix)
