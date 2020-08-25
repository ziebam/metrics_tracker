import argparse
import pickle
import sys
from pathlib import Path


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
    footer = f"└{'┴'.join(border)}┘"

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

    if decision in ["y", "ye", "yes"]:
        return True
    else:
        return False


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

    if args.add:
        metric_id, to_add = args.add
        metrics[metric_id - 1][2] += to_add

    if args.update:
        index, new_name = args.update
        index = int(index)

        metrics[index - 1][1] = new_name

    if args.reset:
        if decision_confirmed():
            index = args.reset[0]
            metrics[index - 1][2] = 0
        else:
            sys.exit("Operation cancelled. Aborting.")

    if args.remove:
        index = args.remove[0]

        [[1, 2, 3], [2, 2, 3], [3, 2, 3]]

        for idx, _ in enumerate(metrics[index - 1 :]):
            metrics[idx][0] -= 1

        del metrics[index - 1]

        print(metrics)

    if args.delete:
        if decision_confirmed():
            metrics = []
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
