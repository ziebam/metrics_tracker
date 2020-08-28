import argparse
import pickle
import sys
from pathlib import Path

from .pprinting_utils import clear_screen, decision_confirmed, print_data


def main():
    data_file = Path("data.pickle")

    if not data_file.is_file():
        with open(data_file, "wb") as data:
            pickle.dump([], data)

    with open(data_file, "rb") as data:
        metrics = pickle.load(data)

    parser = argparse.ArgumentParser(prog="Metrics Tracker")

    parser.add_argument("-c", "--create", metavar="metric")
    parser.add_argument(
        "-a", "--add", nargs=2, type=int, metavar=("metric_id", "amount")
    )
    parser.add_argument("-u", "--update", nargs=2, metavar=("metric_id", "new_name"))
    parser.add_argument("--reset", type=int, metavar="metric_id")
    parser.add_argument("--remove", type=int, metavar="metric_id")
    parser.add_argument("--delete", action="store_true")
    parser.add_argument("--list", action="store_true")

    if len(sys.argv) == 1:
        sys.exit(parser.print_help())

    args = parser.parse_args()

    if args.create:
        metric_id = len(metrics) + 1
        metric = args.create
        metrics.append([metric_id, metric, 0])

        clear_screen()
        print(f'Created metric "{metric}" succesfully.')
        print_data(metrics)

    if args.add:
        index, to_add = (args.add[0] - 1, args.add[1])
        metrics[index][2] += to_add

        clear_screen()
        print(f'Added {to_add} to the metric "{metrics[index][1]}" succesfully.')
        print_data(metrics)

    if args.update:
        index, new_name = (int(args.update[0]) - 1, args.update[1])
        old_name = metrics[index][1]

        metrics[index][1] = new_name

        clear_screen()
        print(f'Updated name of metric "{old_name}" to "{new_name}" succesfully.')
        print_data(metrics)

    if args.reset:
        if decision_confirmed():
            index = args.reset - 1
            metrics[index][2] = 0

            clear_screen()
            print(f'Reset metric "{metrics[index][1]}" to 0 succesfully.')
            print_data(metrics)
        else:
            sys.exit("Operation cancelled. Aborting.")

    if args.remove:
        if decision_confirmed():
            index = args.remove - 1
            name = metrics[index][1]

            for metric in metrics[index + 1 :]:
                metric[0] -= 1

            del metrics[index]

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
            clear_screen()
            print_data(metrics)
        else:
            sys.exit("There isn't any data to list. Aborting.")

    with open(data_file, "wb") as data:
        pickle.dump(metrics, data)


main()
