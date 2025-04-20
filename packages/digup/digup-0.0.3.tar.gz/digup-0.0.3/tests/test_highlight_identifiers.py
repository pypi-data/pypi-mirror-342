from textwrap import dedent

from src.colors import DISTINCT_COLORS
from src.highlight_identifiers import highlight_identifiers


def test_highlighting_identifiers():
    code = dedent(
        """
    def f():
        a
        b
        a
    """
    )

    colored = highlight_identifiers(code, colors=DISTINCT_COLORS)

    assert colored == dedent(
        """
    def \x1b[38;2;0;130;200mf\x1b[0m():
        \x1b[38;2;60;180;75ma\x1b[0m
        \x1b[38;2;230;25;75mb\x1b[0m
        \x1b[38;2;60;180;75ma\x1b[0m
    """
    )


def test_highlighting_only_some_identifiers():
    code = """
    def f():
        a
        b
        c
    """

    colored = highlight_identifiers(code, colors=DISTINCT_COLORS, only={"a", "b"})

    assert colored == dedent(
        """
    def f():
        \x1b[38;2;0;130;200ma\x1b[0m
        \x1b[38;2;60;180;75mb\x1b[0m
        c
    """
    )


def test_highlighting_params_only():
    code = """
    def f(a, b):
        a
        b
        c = lambda x: x + 1
    """

    colored = highlight_identifiers(code, colors=DISTINCT_COLORS, params_only=True)

    assert colored == dedent(
        """
    def f(\x1b[38;2;0;130;200ma\x1b[0m, \x1b[38;2;60;180;75mb\x1b[0m):
        \x1b[38;2;0;130;200ma\x1b[0m
        \x1b[38;2;60;180;75mb\x1b[0m
        c = lambda \x1b[38;2;230;25;75mx\x1b[0m: \x1b[38;2;230;25;75mx\x1b[0m + 1
    """
    )


def test_highlighting_classes():
    code = """
    class A:
        class B: ...
    """

    colored = highlight_identifiers(code, colors=DISTINCT_COLORS)

    assert colored == dedent(
        """
        class \x1b[38;2;0;130;200mA\x1b[0m:
            class \x1b[38;2;60;180;75mB\x1b[0m: ...
    """
    )


def test_highlighting_a_module():
    code = """
    x = 0
    
    class A: ...
    """

    colored = highlight_identifiers(code, colors=DISTINCT_COLORS)

    assert colored == dedent(
        """
        \x1b[38;2;0;130;200mx\x1b[0m = 0
        
        class \x1b[38;2;60;180;75mA\x1b[0m: ...
    """
    )
