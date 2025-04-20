"""Tests for mpr_tools.files.loaders"""

from src.mpr_tools.files.loaders import load_dict_from_file
from tests.constants import FIXTURES_FOLDER


def test_load_dict_from_file_yaml():
    """Test for load_dict_from_file() when passing .yaml"""

    sample_file = FIXTURES_FOLDER / "sample.yaml"

    data = load_dict_from_file(sample_file)

    assert data["test_yaml"]["level1_a"]["level2_a"] == "hello"
    assert data["test_yaml"]["level1_b"]["level2_b"] == "bye"


def test_load_dict_from_file_yml():
    """Test for load_dict_from_file() when passing .yml"""

    sample_file = FIXTURES_FOLDER / "sample.yml"

    data = load_dict_from_file(sample_file)

    assert data["test_yaml"]["level1_a"]["level2_a"] == "hello"
    assert data["test_yaml"]["level1_b"]["level2_b"] == "bye"


def test_load_dict_from_file_json():
    """Test for load_dict_from_file() when passing .json"""

    sample_file = FIXTURES_FOLDER / "sample.json"

    data = load_dict_from_file(sample_file)

    assert data["test_yaml"]["level1_a"]["level2_a"] == "hello"
    assert data["test_yaml"]["level1_b"]["level2_b"] == "bye"
