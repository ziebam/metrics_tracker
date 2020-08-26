import os
import sys


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_data(data, padding=2):
    num_of_columns = len(data[0])

    if not all(len(row) == num_of_columns for row in data):
        sys.exit("Invalid data. Aborting.")

    column_widths = []
    for i in range(num_of_columns):
        column_items = [str(row[i]) for row in data]
        column_width = len(max(column_items, key=len)) + padding

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
