import pytest


class TestSetMethods:

    def test_set_intersection(self):
        assert {3, 2, 1, 4} & {4, 3, 5, 6} == {3, 4}

    def test_set_union(self):
        assert {3, 2, 1, 4} | {4, 3, 5, 6} == {1, 2, 3, 4, 5, 6}


def test_set_only_unique():
    assert {1, 2, 3, 2, 1} == {3, 3, 3, 1, 1, 2, 1, 1, 3}


def test_set_only_hashable_elements():
    s = set()
    with pytest.raises(TypeError):
        assert s.add(['a', 'b', 'c'])


@pytest.mark.parametrize('symbol', 'abcdef1234%!^')
def test_set_add_in(symbol):
    s = set()
    s.add(symbol)
    assert symbol in s
