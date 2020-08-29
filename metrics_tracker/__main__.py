import argparse
import pickle
import sys
from pathlib import Path

from .action_handlers import (
    add_to_metric,
    create_metric,
    update_metric,
    reset_metric,
    remove_metric,
    delete_metrics,
    list_metrics,
)


def main():
    data_file = Path("data.pickle")

    if not data_file.is_file():
        with open(data_file, "wb") as data:
            pickle.dump([], data)

    with open(data_file, "rb") as data:
        metrics = pickle.load(data)

    parser = argparse.ArgumentParser(prog="Metrics Tracker")

    parser.add_argument("-c", "--create", metavar="metric_name")
    parser.add_argument(
        "-a", "--add", nargs=2, type=int, metavar=("metric_id", "amount_to_add")
    )
    parser.add_argument(
        "-u", "--update", nargs=2, metavar=("metric_id", "new_metric_name")
    )
    parser.add_argument("--reset", type=int, metavar="metric_id")
    parser.add_argument("--remove", type=int, metavar="metric_id")
    parser.add_argument("--delete", action="store_true")
    parser.add_argument("-l", "--list", action="store_true")

    if len(sys.argv) == 1:
        sys.exit(parser.print_help())

    args = parser.parse_args()

    if metric_name := args.create:
        create_metric(metric_name, metrics)

    if args.add:
        add_to_metric(*args.add, metrics)

    if args.update:
        update_metric(*args.update, metrics)

    if metric_id := args.reset:
        reset_metric(metric_id, metrics)

    if metric_id := args.remove:
        remove_metric(metric_id, metrics)

    if args.delete:
        delete_metrics(metrics)

    if args.list:
        list_metrics(metrics)

    with open(data_file, "wb") as data:
        pickle.dump(metrics, data)


main()
