from __future__ import annotations

from digup.aggregation import Aggregation
from digup.count_words import Word, WordCount


def test_sum_a_single_wordcounts():
    assert Aggregation.of([WordCount([Word("x", 1, 1)], 2)]) == Aggregation({"x": 1})


def test_sum_of_distinct_identifiers():
    assert Aggregation.of([WordCount([Word("x", 1, 1)], 2), WordCount([Word("y", 1, 1)], 2)]) == Aggregation(
        {"x": 1, "y": 1}
    )


def test_sum_of_same_identifier():
    assert Aggregation.of([WordCount([Word("x", 1, 1)], 2), WordCount([Word("x", 1, 1)], 2)]) == Aggregation({"x": 2})
