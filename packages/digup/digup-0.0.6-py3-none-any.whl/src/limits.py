import abc
from collections import Counter
from typing import Iterable


class Limit(abc.ABC):
    @abc.abstractmethod
    def limit(self, collection: Iterable[str]) -> list[str]:
        raise NotImplementedError


class NoLimit(Limit):

    def limit(self, collection: Iterable[str]) -> list[str]:
        return list(collection)


class FirstN(Limit):
    def __init__(self, n: int):
        self._limit = n

    def limit(self, collection: Iterable[str]) -> list[str]:
        return list(collection)[: self._limit]


class LastN(Limit):
    def __init__(self, n: int):
        self._n = n

    def limit(self, collection: Iterable[str]) -> list[str]:
        return list(collection)[self._n - 1 :]


class MostN(Limit):
    def __init__(self, n: int):
        self._n = n

    def limit(self, collection: Iterable[str]) -> list[str]:
        return [v for v, _ in Counter(collection).most_common(self._n)]


class LeastN(Limit):
    def __init__(self, n: int):
        self._n = n

    def limit(self, collection: Iterable[str]) -> list[str]:
        c: Counter[str] = Counter()
        c.subtract(collection)
        return [v for v, _ in c.most_common(self._n)]
