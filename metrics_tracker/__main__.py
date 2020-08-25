import argparse
import pickle
import sys
from pathlib import Path


def print_data(data, padding=4):
    first_column_width = len(max(data, key=len)) + padding
    second_column_width = len(str(max(data.values()))) + padding

    header = f"┌{'─' * first_column_width}┬{'─' * second_column_width}┐"
    middle = f"\n├{'─' * first_column_width}┼{'─' * second_column_width}┤\n"
    footer = f"└{'─' * first_column_width}┴{'─' * second_column_width}┘"

    rows = [
        f"│{key.center(first_column_width)}│{str(value).center(second_column_width)}│"
        for key, value in data.items()
    ]
    printable_data = middle.join(rows)

    print(header)
    print(printable_data)
    print(footer)


def main():
    data_file = Path("data.pickle")

    if not data_file.is_file():
        with open(data_file, "wb") as data:
            pickle.dump(dict(), data)

    with open(data_file, "rb") as data:
        metrics = pickle.load(data)

    parser = argparse.ArgumentParser(prog="Metrics Tracker")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    parser.add_argument("--create", nargs=1, metavar="metric")
    parser.add_argument("--add", nargs=2, metavar=("metric", "amount"))
    parser.add_argument("--update", nargs=2, metavar=("old_name", "new_name"))
    parser.add_argument("--reset", nargs=1, metavar="metric")
    parser.add_argument("--remove", nargs=1, metavar="metric")
    parser.add_argument("--delete", action="store_true")
    parser.add_argument("--list", action="store_true")

    args = parser.parse_args()

    if args.create:
        metric = args.create[0]
        metrics[metric] = 0

    if args.add:
        metric, to_add = args.add
        metrics[metric] = metrics[metric] + int(to_add)

    if args.update:
        old_key, new_key = args.update
        metrics[new_key] = metrics[old_key]
        del metrics[old_key]

    if args.reset:
        metric = args.reset[0]
        metrics[metric] = 0

    if args.remove:
        metric = args.remove[0]
        del metrics[metric]

    if args.delete:
        metrics = dict()

    if args.list:
        print_data(metrics)

    with open(data_file, "wb") as data:
        pickle.dump(metrics, data)


main()
