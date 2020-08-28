"""Test functions for the pprinting_utils.py module."""

import pytest

from metrics_tracker.pprinting_utils import decision_confirmed, print_data

BASE_TEST_DATA = [["1", "test metric", "0"]]


def test_decision_confirmed(monkeypatch):
    with monkeypatch.context():
        monkeypatch.setattr("builtins.input", lambda _: "y")
        assert decision_confirmed()

        monkeypatch.setattr("builtins.input", lambda _: "ye")
        assert decision_confirmed()

        monkeypatch.setattr("builtins.input", lambda _: "yes")
        assert decision_confirmed()

        monkeypatch.setattr("builtins.input", lambda _: "Y")
        assert decision_confirmed()

        monkeypatch.setattr("builtins.input", lambda _: "YE")
        assert decision_confirmed()

        monkeypatch.setattr("builtins.input", lambda _: "YES")
        assert decision_confirmed()

        monkeypatch.setattr("builtins.input", lambda _: "")
        assert not decision_confirmed()

        monkeypatch.setattr("builtins.input", lambda _: "n")
        assert not decision_confirmed()

        monkeypatch.setattr("builtins.input", lambda _: "no")
        assert not decision_confirmed()

        monkeypatch.setattr("builtins.input", lambda _: "N")
        assert not decision_confirmed()

        monkeypatch.setattr("builtins.input", lambda _: "NO")
        assert not decision_confirmed()


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
