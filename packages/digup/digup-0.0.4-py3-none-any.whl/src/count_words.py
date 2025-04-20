from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable


@dataclass(frozen=True)
class Word:
    word: str
    occurences: int
    span: int


@dataclass(frozen=True)
class WordCount:
    words: list[Word]
    length: int

    def sorted_by_occurences(self) -> WordCount:
        return WordCount(sorted(self.words, key=lambda wc: wc.occurences, reverse=True), self.length)


class IdentifierKind(StrEnum):
    ARG = "arg"
    NAME = "name"
    FUNCTION = "function"
    CLASS = "class"


@dataclass(frozen=True)
class Identifier:
    name: str
    lineno: int
    column: int
    kind: IdentifierKind


def get_identifiers(node: ast.AST) -> Iterable[Identifier]:
    for child in ast.walk(node):
        if isinstance(child, ast.arg):
            yield Identifier(child.arg, child.lineno, child.col_offset, IdentifierKind.ARG)
        elif isinstance(child, ast.Name):
            yield Identifier(child.id, child.lineno, child.col_offset, IdentifierKind.NAME)
        elif isinstance(child, ast.FunctionDef):
            yield Identifier(child.name, child.lineno, child.col_offset + len("def "), IdentifierKind.FUNCTION)
        elif isinstance(child, ast.ClassDef):
            yield Identifier(child.name, child.lineno, child.col_offset + len("class "), IdentifierKind.CLASS)
        # else:
        #     print(f"ignored: {child}")


def word_count(node: ast.AST, length: int) -> WordCount:

    occurences = {}
    line_start = {}
    line_end = {}

    for identifier in sorted(get_identifiers(node), key=lambda idf: (idf.lineno, idf.column)):
        name_encountered_for_the_first_time = identifier.name not in occurences
        if name_encountered_for_the_first_time:
            occurences[identifier.name] = 1
            line_start[identifier.name] = identifier.lineno
            line_end[identifier.name] = identifier.lineno
        else:
            occurences[identifier.name] += 1
            line_end[identifier.name] = identifier.lineno

    return WordCount(
        [
            Word(
                w,
                occurences[w],
                line_end[w] - line_start[w] + 1,
            )
            for w in occurences.keys()
        ],
        length=length,
    )
