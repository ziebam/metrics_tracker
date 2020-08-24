import argparse
import pickle
import sys
from pathlib import Path


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
        metrics[metric] = str(int(metrics[metric]) + int(to_add))

    if args.reset:
        metric = args.reset[0]
        metrics[metric] = 0

    if args.remove:
        metric = args.remove[0]
        del metrics[metric]

    if args.delete:
        metrics = dict()

    if args.list:
        longest_metric = len(max(metrics, key=len))
        longest_value = len(str(max([value for value in metrics.values()])))

        counter = 0

        print("┌" + "─" * (longest_metric + 6) + "┬" + "─" * (longest_value + 4) + "┐")
        for metric, value in metrics.items():
            counter += 1
            print(
                "│"
                + metric.center(longest_metric + 6)
                + "│"
                + str(value).center(longest_value + 4)
                + "│"
            )

            if counter < len(metrics):
                print(
                    "├"
                    + "─" * (longest_metric + 6)
                    + "┼"
                    + "─" * (longest_value + 4)
                    + "┤"
                )
        print("└" + "─" * (longest_metric + 6) + "┴" + "─" * (longest_value + 4) + "┘")

    with open(data_file, "wb") as data:
        pickle.dump(metrics, data)


main()
