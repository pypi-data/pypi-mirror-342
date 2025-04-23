import ast
from collections import defaultdict
from dataclasses import dataclass
from textwrap import dedent
from typing import Optional

from digup.colorize import hue_gradient, colorize
from digup.count_words import get_identifiers, IdentifierKind
from digup.limits import Limit, NoLimit


@dataclass(frozen=True)
class IdentifierToHighlight:
    name: str
    column: int
    color: int


def highlight_identifiers(
    code: str,
    *,
    colors: Optional[list[int]] = None,
    only: Optional[set[str]] = None,
    params_only: bool = False,
    limit: Limit = NoLimit(),
) -> dict[int, list[IdentifierToHighlight]]:
    # TODO : je parse le code plusieurs fois ici, c'est un peu bête
    source = dedent(code)
    tree = ast.parse(source)

    sorted_identifiers = sorted(get_identifiers(tree), key=lambda idtf: (idtf.lineno, idtf.column))

    if params_only:
        for identifier in sorted_identifiers:
            if identifier.kind == IdentifierKind.ARG:
                if only is None:
                    only = set()
                only.add(identifier.name)

    if only is None:
        filtered_identifiers = sorted_identifiers
    else:
        filtered_identifiers = []
        for identifier in sorted_identifiers:
            if identifier.name in only:
                filtered_identifiers.append(identifier)

    ordered_names = {n: n for n in limit.limit(i.name for i in filtered_identifiers)}.keys()

    filtered_identifiers = [i for i in filtered_identifiers if i.name in ordered_names]

    if colors is None:
        colors = hue_gradient(len(ordered_names))

    colors_by_name = {name: color for name, color in zip(ordered_names, colors)}

    identifiers_by_line: dict[int, list[IdentifierToHighlight]] = defaultdict(list)
    for identifier in filtered_identifiers:
        identifiers_by_line[identifier.lineno].append(
            IdentifierToHighlight(identifier.name, identifier.column, colors_by_name[identifier.name])
        )

    return dict(identifiers_by_line)


def present_highlights(identifiers_by_line: dict[int, list[IdentifierToHighlight]], source: str) -> str:
    source = dedent(source)
    output_lines = []
    for lineno, line in enumerate(source.splitlines(), start=1):
        if lineno not in identifiers_by_line:
            output_lines.append(line)
            continue

        output_line = line
        for identifier in reversed(identifiers_by_line[lineno]):
            highlighted_identifier = colorize(identifier.name, foreground=identifier.color)
            output_line = (
                output_line[: identifier.column]
                + highlighted_identifier
                + output_line[identifier.column + len(identifier.name) :]
            )
        output_lines.append(output_line)
    return "\n".join(output_lines) + "\n"
