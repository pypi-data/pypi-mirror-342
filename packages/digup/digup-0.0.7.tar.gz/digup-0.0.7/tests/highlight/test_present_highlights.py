from textwrap import dedent

from src.highlight import present_highlights, IdentifierToHighlight


def test_present_highlights():
    source = """
    def f():
        a = 1
        b = 0
        return a + b
    """
    result = present_highlights(
        {
            2: [IdentifierToHighlight(name="f", column=4, color=196)],
            3: [IdentifierToHighlight(name="a", column=4, color=46)],
            4: [IdentifierToHighlight(name="b", column=4, color=21)],
            5: [IdentifierToHighlight(name="a", column=4, color=46)],
        },
        source,
    )

    assert result == dedent(
        """
    def \x1b[38;5;196mf\x1b[0m():
        \x1b[38;5;46ma\x1b[0m = 1
        \x1b[38;5;21mb\x1b[0m = 0
        \x1b[38;5;46ma\x1b[0meturn a + b
    """
    )
