from calculator import Calculator
import pytest

calculator = Calculator()

def test_sum_positive_numbers():
    assert calculator.sum(4, 5) == 9

def test_sum_negative_numbers():
    assert calculator.sum(-6, -10) == -16

def test_sum_mixed_numbers():
    assert calculator.sum(-6, 6) == 0

def test_sum_floats():
    res = calculator.sum(5.6, 4.3)
    assert round(res, 1) == 9.9

def test_sum_with_zero():
    assert calculator.sum(10, 0) == 10

def test_div_normal():
    assert calculator.div(10, 2) == 5

def test_div_by_zero():
    with pytest.raises(ArithmeticError, match="На ноль делить нельзя"):
        calculator.div(10, 0)