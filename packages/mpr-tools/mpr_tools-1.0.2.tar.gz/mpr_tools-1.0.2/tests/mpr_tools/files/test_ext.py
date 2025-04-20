"""Tests for mpr_tools.files.ext"""

from pathlib import Path

from src.mpr_tools.files.ext import get_extension


def test_get_extension_str():
    """Test for get_extension() when passing str"""
    path1 = "home/foo/file"
    path2 = "home/foo/file.tar"
    path3 = "home/foo/file.tar.gz"
    path4 = "home/foo/file.tar.gz.abc.cd"

    assert get_extension(path1) == ""
    assert get_extension(path2) == "tar"
    assert get_extension(path3) == "tar.gz"
    assert get_extension(path4) == "tar.gz.abc.cd"


def test_get_extension_path():
    """Test for get_extension() when passing Path()"""
    path1 = Path("home/foo/file")
    path2 = Path("home/foo/file.tar")
    path3 = Path("home/foo/file.tar.gz")
    path4 = Path("home/foo/file.tar.gz.abc.cd")

    assert get_extension(path1) == ""
    assert get_extension(path2) == "tar"
    assert get_extension(path3) == "tar.gz"
    assert get_extension(path4) == "tar.gz.abc.cd"
