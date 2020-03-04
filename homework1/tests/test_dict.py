import pytest


class TestDictRestrictions:

    def test_dict_get_not_existing(self):
        dictionary = {'alice': 10}
        with pytest.raises(KeyError):
            print(dictionary['bob'])

    def test_dict_only_hashable_keys(self):
        dictionary = {}
        with pytest.raises(TypeError):
            dictionary[[1, 2, 3]] = 'something'

    def test_dict_overwriting(self, random_int):
        dictionary = {}
        for i in range(random_int):
            dictionary['key'] = i
        assert dictionary == {'key': random_int-1}


def test_dict_comprehension():
    assert {i: i ** 2 for i in range(5)} == {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}


@pytest.mark.parametrize('dict1,dict2',
                         [({'a': 10, 'b': 20}, {'c': 30, 'd': 40}),
                          ({'a': 10, 'b': 20, 'c': 30}, {'d': 40}),
                          ({'a': 10, 'b': 20, 'c': 30, 'd': 40}, {})])
def test_dict_get_summarize(dict1, dict2):
    assert {**dict1, **dict2} == {'a': 10, 'b': 20, 'c': 30, 'd': 40}
