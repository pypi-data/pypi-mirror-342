from scotils.finance.gambling.arbitrage import (
    decimal_to_implied_probability,
    american_to_decimal,
    calc_margin,
    calc_margin_american,
    find_arbitrage,
)


def test_decimal_to_implied_probability():
    assert decimal_to_implied_probability(2) == 50.0


def test_american_to_decimal():
    assert american_to_decimal(100) == 2.0
    assert american_to_decimal(-100) == 2.0


def test_calc_margin():
    assert calc_margin(2, 5) == 70.0
    assert calc_margin_american(100, 400) == 70.0


def test_find_arbitrage():
    assert find_arbitrage(100, 400) == (
        {0: 71.42857142857143, 1: 28.571428571428573},
        42.85714285714286,
    )
    assert find_arbitrage(100, 100) is None
