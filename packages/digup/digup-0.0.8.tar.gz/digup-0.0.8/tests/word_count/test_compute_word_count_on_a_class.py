import ast
from textwrap import dedent
from typing import cast

from digup.count_words import WordCount, Word, word_count
from digup.get_nodes import node_length


def test_empty_class():
    code = """\
    class A: ...
    """

    assert _wc(code) == WordCount([Word("A", 1, 1)], length=1)


def test_with_base_class():
    code = """\
    class A(B): ...
    """

    assert _wc(code) == WordCount([Word("A", 1, 1), Word("B", 1, 1)], length=1)


def test_a_class_with_members():
    code = """\
    class A:
        a: int
        b: int
    """

    assert _wc(code) == WordCount(
        [
            Word("A", 1, 1),
            Word("a", 1, 1),
            Word("int", 2, 2),
            Word("b", 1, 1),
        ],
        length=3,
    )


def test_a_class_with_methods():
    code = """\
    class A:
        def f(self, a: int) -> int:
            return a + 10
    """

    assert _wc(code) == WordCount(
        [
            Word("A", 1, 1),
            Word(word="f", occurences=1, span=1),
            Word(word="self", occurences=1, span=1),
            Word(word="a", occurences=2, span=2),
            Word(word="int", occurences=2, span=1),
        ],
        length=3,
    )


def _wc(code: str) -> WordCount:
    tree = ast.parse(dedent(code))
    class_node = cast(ast.ClassDef, tree.body[0])
    return word_count(class_node, node_length(class_node.lineno, class_node.end_lineno))
