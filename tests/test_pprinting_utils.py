"""Test functions for the pprinting_utils.py module."""

import pytest

from metrics_tracker.pprinting_utils import print_data

BASE_TEST_DATA = [["1", "test metric", "0"]]


def test_print_data_with_default_padding(capfd):
    expected_stdout = (
        "┌───┬─────────────┬───┐\n│ 1 │ test metric │ 0 │\n└───┴─────────────┴───┘\n\n"
    )
    print_data(BASE_TEST_DATA)
    captured = capfd.readouterr()

    assert captured.out == expected_stdout


def test_print_data_with_custom_padding(capfd):
    expected_stdout = "┌─────┬───────────────┬─────┐\n│  1  │  test metric  │  0  │\n└─────┴───────────────┴─────┘\n\n"

    print_data(BASE_TEST_DATA, padding=2)
    captured = capfd.readouterr()

    assert captured.out == expected_stdout


def test_print_data_with_invalid_data():
    invalid_test_data = [["row", "of length", "3"], ["row", "of", "length", "4"]]

    with pytest.raises(SystemExit):
        print_data(invalid_test_data)
