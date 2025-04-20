from pathlib import Path

from src.get_nodes import get_classes

_here = Path(__file__).parent


def test_select_all_classes_in_a_file():
    _assert_get_classes_from_path_yields(
        path=Path("test_data/selecting_class/all_the_classes_of_the_file"),
        search="",
        expected_names=["A", "B"],
    )


def test_selecting_a_class_that_doesnt_exist():
    _assert_get_classes_from_path_yields(
        path=Path("test_data/selecting_class/a_class_that_doesnt_exist/"),
        search="A",
        expected_names=[],
    )


def test_selecting_a_class_among_two():
    _assert_get_classes_from_path_yields(
        path=Path("test_data/selecting_class/a_class_among_two"),
        search="A",
        expected_names=["A"],
    )


def test_selecting_in_a_sub_directory():
    path = Path("test_data/selecting_class/a_class_in_a_sub_directory")
    classes = list(get_classes([_here / path], ""))
    assert classes[0].name == "A"


def test_selecting_when_exist_in_two_files():
    _assert_get_classes_from_path_yields(
        path=Path("test_data/selecting_class/same_name_in_two_files"),
        search="A",
        expected_names=["A", "A"],
    )


def test_selecting_a_nested_class():
    _assert_get_classes_from_path_yields(
        path=Path("test_data/selecting_class/a_nested_class"),
        search="Inner",
        expected_names=["Inner"],
    )


def _assert_get_classes_from_path_yields(*, path: Path, search: str, expected_names: list[str]):
    classes = list(get_classes([_here / path], search))
    assert [c.name for c in classes] == expected_names
