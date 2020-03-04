import pytest


class TestIntMathMethods:

    def test_int_integer_division(self):
        assert 1488 // 228 == 6

    @pytest.mark.parametrize('a,n,result',
                             [(2, 3, 8), (-2, 3, -8), (5, 0, 1), (0, 0, 1)])
    def test_int_pow(self, a, n, result):
        assert a ** n == result

    def test_int_simple_operations(self):
        assert 1 + 2 * 3 - (9 / 3 + 4) == 0

    def test_int_bitwise_operations(self):
        assert 1024 >> 4 == 64


def test_int_bin():
    assert bin(33) == '0b100001'
