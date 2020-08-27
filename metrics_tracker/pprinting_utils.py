"""Pprinting utilities for the `metrics_tracker` module."""

import os
import sys


def clear_screen():
    """Clears the console screen (cross-platform)."""

    os.system("cls" if os.name == "nt" else "clear")


def print_data(data, padding=1):
    """Pretty-prints the data to the terminal.

    Args:
        data: A list of lists. It can have a variable number of columns, given
          that their amount stays consistent throughout the rows.
        padding: Optional; The amount of whitespace between the value and the
          table border.
    """

    num_of_columns = len(data[0])

    if not all(len(row) == num_of_columns for row in data):
        sys.exit("Invalid data. Aborting.")

    column_widths = []
    for i in range(num_of_columns):
        column_items = [str(row[i]) for row in data]
        column_width = len(max(column_items, key=len)) + padding * 2

        column_widths.append(column_width)

    border = ["─" * width for width in column_widths]

    header = f"┌{'┬'.join(border)}┐"
    middle = f"\n├{'┼'.join(border)}┤\n"
    footer = f"└{'┴'.join(border)}┘\n"

    rows = []

    for row in data:
        rows.append(
            f"│{'│'.join([str(value).center(width) for value, width in zip(row, column_widths)])}│"
        )

    printable_data = middle.join(rows)

    print(header)
    print(printable_data)
    print(footer)
