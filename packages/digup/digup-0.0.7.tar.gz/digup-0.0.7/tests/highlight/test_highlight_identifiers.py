from textwrap import dedent

from src.highlight import highlight_identifiers, IdentifierToHighlight
from src.limits import FirstN


def test_highlighting_identifiers_simple():
    code = dedent(
        """
    def f():
        a
        b
        a
    """
    )

    colored = highlight_identifiers(code, colors=[1, 2, 3])
    assert colored == {
        2: [IdentifierToHighlight(name="f", column=4, color=1)],
        3: [IdentifierToHighlight(name="a", column=4, color=2)],
        4: [IdentifierToHighlight(name="b", column=4, color=3)],
        5: [IdentifierToHighlight(name="a", column=4, color=2)],
    }


def test_highlighting_only_some_identifiers():
    code = """
    def f():
        a
        b
        c
    """

    colored = highlight_identifiers(code, only={"a", "b"}, colors=[1, 2])

    assert (
        colored
        == colored
        == {
            3: [IdentifierToHighlight(name="a", column=4, color=1)],
            4: [IdentifierToHighlight(name="b", column=4, color=2)],
        }
    )


def test_highlighting_params_only():
    code = """
    def f(a, b):
        a
        b
        c = lambda x: x + 1
    """

    colored = highlight_identifiers(code, params_only=True, colors=[1, 2, 3])

    assert colored == {
        2: [IdentifierToHighlight(name="a", column=6, color=1), IdentifierToHighlight(name="b", column=9, color=2)],
        3: [IdentifierToHighlight(name="a", column=4, color=1)],
        4: [IdentifierToHighlight(name="b", column=4, color=2)],
        5: [
            IdentifierToHighlight(name="x", column=15, color=3),
            IdentifierToHighlight(name="x", column=18, color=3),
        ],
    }


def test_highlight_first_n():
    code = "def f(a, b, c, d): ..."

    colored = highlight_identifiers(code, limit=FirstN(2), colors=[1, 2])

    assert colored == {
        1: [IdentifierToHighlight(name="f", column=4, color=1), IdentifierToHighlight(name="a", column=6, color=2)]
    }


def test_highlighting_classes():
    code = """
    class A:
        class B: ...
    """

    colored = highlight_identifiers(code, colors=[1, 2])

    assert colored == {
        2: [IdentifierToHighlight(name="A", column=6, color=1)],
        3: [IdentifierToHighlight(name="B", column=10, color=2)],
    }


def test_highlighting_a_module():
    code = """
    x = 0
    
    class A: ...
    """

    colored = highlight_identifiers(code, colors=[1, 2])

    assert colored == {
        2: [IdentifierToHighlight(name="x", column=0, color=1)],
        4: [IdentifierToHighlight(name="A", column=6, color=2)],
    }
