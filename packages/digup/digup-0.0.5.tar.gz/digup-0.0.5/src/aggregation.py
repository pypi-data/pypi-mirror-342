from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from src.count_words import WordCount


@dataclass(frozen=True)
class Aggregation:
    _counts: dict[str, int]

    @classmethod
    def of(cls, statement_word_counts: list[WordCount]) -> Aggregation:
        total: dict[str, int] = defaultdict(lambda: 0)
        for word_counts in statement_word_counts:
            for word_count in word_counts.words:
                total[word_count.word] += word_count.occurences
        return Aggregation(total)

    def counts(self) -> Iterable[tuple[str, int]]:
        return sorted(self._counts.items(), key=lambda item: -item[1])
