"""Entry point for the program."""

import argparse
import configparser
import pickle
import sys
from pathlib import Path

from .action_handlers import (
    add_to_metric,
    create_metric,
    delete_metrics,
    list_metrics,
    remove_metric,
    reset_metric,
    update_metric,
)


def main():
    """Handles the parser setup and dispatches arguments to action handlers."""

    config = configparser.ConfigParser()
    config.read("config.ini")
    data_file = Path(config["path"]["data_file_path"])

    if not data_file.is_file():
        with open(data_file, "wb") as data:
            pickle.dump([], data)

    with open(data_file, "rb") as data:
        metrics = pickle.load(data)

    help_message = """python -m metrics_tracker [-h] [-c/--create <metric_name>] [-a/--add <metric_id> <amount_to_add]
                                 [-u/--update <metric_id> <new_metric_name>] [--reset <metric_id>]
                                 [--remove <metric_id>] [--delete] [-l/--list]"""

    parser = argparse.ArgumentParser(
        prog="python -m metrics_tracker",
        usage=help_message,
        description="A commmand-line metrics tracker. When run with no arguments, this help message will be displayed.",
    )

    parser.add_argument(
        "-c", "--create", help="add a metric <metric_name>", metavar="metric_name"
    )
    parser.add_argument(
        "-a",
        "--add",
        nargs=2,
        type=int,
        help="add <amount_to_add> to the metric with ID <metric_id>",
        metavar=("metric_id", "amount_to_add"),
    )
    parser.add_argument(
        "-u",
        "--update",
        nargs=2,
        help="update the name of metric with ID <metric_id> to be <new_metric_name>",
        metavar=("metric_id", "new_metric_name"),
    )
    parser.add_argument(
        "--reset",
        type=int,
        help="reset the value of metric with ID <metric_id> to 0",
        metavar="metric_id",
    )
    parser.add_argument(
        "--remove",
        type=int,
        help="remove a metric with ID <metric_id>",
        metavar="metric_id",
    )
    parser.add_argument("--delete", action="store_true", help="delete all metrics")
    parser.add_argument("-l", "--list", action="store_true", help="list all metrics")

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


if __name__ == "__main__":
    main()
