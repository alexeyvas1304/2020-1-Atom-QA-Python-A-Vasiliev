import pytest


class TestListMethods:
    def test_list_append(self, random_int):
        lst = [1, 2, 3]
        lst.append([random_int])
        assert lst == [1, 2, 3, [random_int]]

    def test_list_extend(self, random_int):
        lst = [1, 2, 3]
        lst.extend([random_int])
        assert lst == [1, 2, 3, random_int]


def test_list_mutable(random_int):
    a = [1, 2, 3, 4]
    b = a
    b[1] = random_int
    assert a[1] == random_int


def test_list_mutable_tricky():
    lst = [[1] * 3] * 3
    lst[0][0] = 2
    assert lst[0][0] == lst[1][0] == lst[2][0] == 2


# немного высосал из пальца
@pytest.mark.parametrize('lst, sorted_lst, reverse',
                         [([2, 5, 1, 3, 4], [1, 2, 3, 4, 5], False),
                          ([2, 5, 1, 3, 4], [5, 4, 3, 2, 1], True)])
def test_list_sort(lst, sorted_lst, reverse):
    assert sorted(lst, reverse=reverse) == sorted_lst
