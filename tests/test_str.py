import pytest
from random import randint


class TestStrMethods:

    def test_str_concat_multiply(self):
        assert 'a' * 3 + 'b' * 2 == 'aaabb'

    def test_str_slicing(self):
        string = 'abcdefghijklmnop'
        assert string[2:8:2] == 'ceg'

    def test_str_reverse(self):
        string = 'abcdefgh'
        assert string[::-1] == 'hgfedcba'


def test_str_immutable():
    string = 'qwerty'
    with pytest.raises(TypeError):
        string[0] = 'a'


# как в параметрах декоратора вызвать фикстуру ?
@pytest.mark.parametrize('left_spaces,right_spaces',
                         [(randint(1, 15), randint(1, 15)) for _ in range(10)])
def test_str_strip(left_spaces, right_spaces):
    base_string = 'qwerty'
    new_string = ' ' * left_spaces + base_string + ' ' * right_spaces
    assert base_string == new_string.strip()
