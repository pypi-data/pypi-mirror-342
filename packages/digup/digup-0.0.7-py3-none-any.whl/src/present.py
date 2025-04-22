from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar, Iterable, Callable

from src.aggregation import Aggregation
from src.count_words import WordCount
from src.get_nodes import Node

TableItem = TypeVar("TableItem")


@dataclass(frozen=True)
class Table:
    columns: list[_Column]
    table_width: int

    @classmethod
    def of(cls, columns: list[_Column]) -> Table:
        table_width = sum(c.width for c in columns)
        return Table(columns, table_width)

    def present(self, items: Iterable[TableItem], item_to_tuple: Callable[[TableItem], Iterable]) -> str:
        res = ""
        res += self._separator()
        res += self._header()
        res += self._separator()
        res += self._body(items, item_to_tuple)
        return res

    def _header(self) -> str:
        return "".join(c.present_header() for c in self.columns) + "\n"

    def _separator(self) -> str:
        return "-" * self.table_width + "\n"

    def _body(self, items: Iterable[TableItem], item_to_tuple: Callable[[TableItem], Iterable]):
        res = ""
        for word in items:
            line = "".join([c.present_value(v) for c, v in zip(self.columns, item_to_tuple(word))])
            res += line + "\n"
        return res


def present_word_count(word_count: WordCount) -> str:
    return Table.of(
        [
            _Column("word", 40, "<"),
            _Column("#", 10, ">"),
            _Column("span", 10, ">"),
            _Column("proportion", 12, ">", precision=".0", type="%"),
        ]
    ).present(
        word_count.words,
        lambda word: (word.word, word.occurences, word.span, word.span / word_count.length),
    )


def present_aggregation(aggregation: Aggregation, limit_to: int):
    return Table.of(
        [
            _Column("word", 40, "<"),
            _Column("occurences", 10, ">"),
        ]
    ).present(
        list(aggregation.counts())[:limit_to],
        lambda a: a,
    )


@dataclass(frozen=True)
class LsItem:
    name: str
    length: int

    @classmethod
    def from_node(cls, node: Node, from_path: Path) -> LsItem:
        return LsItem(node.location_from(from_path), node.length)


def present_nodes(ls_items: list[LsItem], kind: str):
    return Table.of(
        [
            _Column(kind, 110, "<"),
            _Column("length", 10, ">"),
        ]
    ).present(
        ls_items,
        lambda ls_item: (ls_item.name, ls_item.length),
    )


@dataclass(frozen=True)
class _Column:
    name: str
    width: int
    align: str
    precision: str = ""
    type: str = ""

    def present_header(self) -> str:
        return f"{self.name: {self.align}{self.width}}"

    def present_value(self, value: object):
        return f"{value: {self.align}{self.width}{self.precision}{self.type}}"
