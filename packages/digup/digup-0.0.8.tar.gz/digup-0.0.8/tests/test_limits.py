from digup.limits import NoLimit, FirstN, LastN, MostN, LeastN


def test_no_limit():
    assert NoLimit().limit(["a", "b", "c"]) == ["a", "b", "c"]


def test_limit_to_first_n():
    assert FirstN(2).limit(["a", "b", "c"]) == ["a", "b"]


def test_limit_to_last_n():
    assert LastN(2).limit(["a", "b", "c"]) == ["b", "c"]


def test_limit_to_most_common_n():
    assert MostN(2).limit(["a", "b", "b", "c", "c"]) == ["b", "c"]


def test_limit_to_least_n():
    assert LeastN(2).limit(["a", "a", "b", "c"]) == ["b", "c"]
