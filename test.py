#!/usr/bin/env python2

"""
Name: Joshua Brockschmidt
UW NetID: 1629722
Section: AA
CSE 160
Final Project

Tests that the datastructures in main.py are working as intended.
"""

import main

BASIC_DATES = ("2017-12-19", "2017-12-20", "2017-12-24", "2017-12-25", "2017-12-26",
               "2017-12-28", "2017-12-29", "2017-12-30", "2018-01-01", "2018-01-02")
BASIC_RATES = (1445.930054, 1485.550049, 1516.760010, 1507.770020, 1545.290039,
               1554.449951, 1664.469971, 1697.500000, 1752.310059, 1819.290039)
EPSILON = 0.000001

def assert_list_equals(list1, list2):
    """
    Asserts that two lists are equal in length and contents

    Args:
        list1: The first list.
        list2: The second list.
    """
    assert len(list1) == len(list2)
    for i in range(len(list1)):
        assert list1[i] == list2[i]

def assert_number_list_equals(list1, list2, epsilon):
    """
    Asserts that two lists of numbers are equal in length and contents within an allowable margin
    of error

    Args:
        list1: The first list of numbers.
        list2: The second list of numbers.
        epsilon: A positive number representing the allowable error.
    """
    assert len(list1) == len(list2)
    for i in range(len(list1)):
        assert abs(list1[i] - list2[i]) < epsilon

def create_basic_rates():
    """
    Creates a basic Rates object.
    """
    return main.Rates(rates=BASIC_RATES, dates=BASIC_DATES)

def test_basic_rates():
    """
    Checks that a basic Rates object stores rates and dates properly.
    """
    test_rates = create_basic_rates()
    assert_list_equals(test_rates.dates, BASIC_DATES)
    assert_number_list_equals(test_rates.rates, BASIC_RATES, EPSILON)

def test_load_csv():
    """
    Tests that Rates.load_csv(...) loads data in the right order.
    """
    expected_dates = BASIC_DATES
    expected_rates = BASIC_RATES
    test_rates = main.Rates(
        fn="data/test-small.csv",
        date_col="Date", rate_col="Adj Close", date_format="%Y-%m-%d",
        label="S&P 500"
    )
    assert_list_equals(test_rates.dates, expected_dates)
    assert_number_list_equals(test_rates.rates, expected_rates, EPSILON)

def test_normalize():
    """
    Tests that Rates.normalize(...) normalizes rates properly.
    """
    denom = max(BASIC_RATES)
    expected_rates = [n / denom for n in BASIC_RATES]
    test_rates = create_basic_rates().normalize()
    assert_number_list_equals(test_rates.rates, expected_rates, EPSILON)

def test_calc_derivatives():
    """
    Tests that Rates.calc_derivatives(...) calculates derivatives properly.
    """
    expected_derivs = (39.619995, 7.80249025, -8.98999, 37.520019, 4.579956,
                       110.02002, 33.030029, 27.4050295, 66.97998)
    test_rates = create_basic_rates().calc_derivatives()
    assert_number_list_equals(test_rates.rates, expected_derivs, EPSILON)

def test_correlate():
    """
    Tests that Rates.correlate(...) returns the proper Pearson correlation coefficient.
    This is somewhat trivial, as SciPy--which is ued to calculate the Pearson correlation
    coefficient--is a well-tested library on it's own.
    """
    test_rates1 = create_basic_rates()
    dates2 = ("2017-12-19", "2017-12-20", "2017-12-24", "2017-12-25", "2017-12-26",
              "2017-12-28", "2017-12-31", "2018-01-01", "2018-01-02")
    rates2 = (4235.921054, 8456.758047, 7578.730050, 6553.770020, 7545.280026,
              8125.168976, 8111.126785, 7145.156780, 6721.146802)
    test_rates2 = main.Rates(rates=rates2, dates=dates2)
    p, _ = test_rates1.correlate(test_rates2)
    assert abs(p - 0.11447171558830507) < EPSILON

if __name__ == "__main__":
    print "Running tests..."
    test_basic_rates()
    test_load_csv()
    test_normalize()
    test_calc_derivatives()
    test_correlate()
    print "All tests passed"
