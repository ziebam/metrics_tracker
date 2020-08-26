import argparse
import pickle
import sys
import os
from pathlib import Path


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


def decision_confirmed():
    decision = input("Are you sure (y/n)?: ").lower()

    return bool(decision in ["y", "ye", "yes"])


def main():
    data_file = Path("data.pickle")

    if not data_file.is_file():
        with open(data_file, "wb") as data:
            pickle.dump([], data)

    with open(data_file, "rb") as data:
        metrics = pickle.load(data)

    parser = argparse.ArgumentParser(prog="Metrics Tracker")

    if len(sys.argv) == 1:
        sys.exit(parser.print_help())

    parser.add_argument("--create", nargs=1, metavar="metric")
    parser.add_argument("--add", nargs=2, type=int, metavar=("metric", "amount"))
    parser.add_argument("--update", nargs=2, metavar=("index", "new_name"))
    parser.add_argument("--reset", nargs=1, type=int, metavar="metric")
    parser.add_argument("--remove", nargs=1, type=int, metavar="metric")
    parser.add_argument("--delete", action="store_true")
    parser.add_argument("--list", action="store_true")

    args = parser.parse_args()

    if args.create:
        metric_id = len(metrics) + 1
        metric = args.create[0]
        metrics.append([metric_id, metric, 0])

        clear_screen()
        print(f'Created metric "{metric}" succesfully.')
        print_data(metrics)

    if args.add:
        metric_id, to_add = args.add
        metrics[metric_id - 1][2] += to_add

        clear_screen()
        print(
            f'Added {to_add} to the metric "{metrics[metric_id - 1][1]}" succesfully.'
        )
        print_data(metrics)

    if args.update:
        index, new_name = args.update
        index = int(index)
        old_name = metrics[index - 1][1]

        metrics[index - 1][1] = new_name

        clear_screen()
        print(f'Updated name of metric "{old_name}" to "{new_name}" succesfully.')
        print_data(metrics)

    if args.reset:
        if decision_confirmed():
            index = args.reset[0]
            metrics[index - 1][2] = 0

            clear_screen()
            print(f'Reset metric "{metrics[index - 1][1]}" to 0 succesfully.')
            print_data(metrics)
        else:
            sys.exit("Operation cancelled. Aborting.")

    if args.remove:
        if decision_confirmed():
            index = args.remove[0]
            name = metrics[index - 1][1]

            for idx, _ in enumerate(metrics[index:]):
                metrics[idx][0] -= 1

            del metrics[index - 1]

            clear_screen()
            print(f'Removed metric "{name}" succesfully.')
            print_data(metrics)
        else:
            sys.exit("Operation cancelled. Aborting.")

    if args.delete:
        if decision_confirmed():
            metrics = []
            clear_screen()
            print("Deleted the data succesfully.\n")
        else:
            sys.exit("Operation cancelled. Aborting.")

    if args.list:
        if metrics:
            print_data(metrics)
        else:
            sys.exit("There isn't any data to list. Aborting.")

    with open(data_file, "wb") as data:
        pickle.dump(metrics, data)


main()
