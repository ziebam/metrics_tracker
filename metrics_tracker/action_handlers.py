"""Action handlers for the parsed data."""

import sys

from .pprinting_utils import clear_screen, decision_confirmed, print_data


def create_metric(metric_name, metrics):
    """Creates the metric.

    Args:
        metric_name: A name for the new metric.
        metrics: A list of all metrics.
    """

    metric_id = len(metrics) + 1
    metrics.append([metric_id, metric_name, 0])

    clear_screen()
    print(f'Created metric "{metric_name}" succesfully.')
    print_data(metrics)


def add_to_metric(metric_id, amount_to_add, metrics):
    """Adds a value to the metric.

    Args:
        metric_id: ID of the metric. The metrics are one-indexed.
        amount_to_add: A value to add to the metric.
        metrics: A list of all metrics.
    """

    index = metric_id - 1
    metrics[index][2] += amount_to_add

    clear_screen()
    print(f'Added {amount_to_add} to the metric "{metrics[index][1]}" succesfully.')
    print_data(metrics)


def update_metric(metric_id, new_metric_name, metrics):
    """Updates the metric's name.

    Args:
        metric_id: ID of the metric. The metrics are one-indexed.
        new_metric_name: A name to set the old name to.
        metrics: A list of all metrics.
    """

    index = int(metric_id) - 1
    old_name = metrics[index][1]

    metrics[index][1] = new_metric_name

    clear_screen()
    print(
        f'Updated the name of metric "{old_name}" to "{new_metric_name}" succesfully.'
    )
    print_data(metrics)


def reset_metric(metric_id, metrics):
    """Resets a metric's value to 0.

    Args:
        metric_id: ID of the metric. The metrics are one-indexed.
        metrics: A list of all metrics.
    """

    if decision_confirmed():
        index = metric_id - 1
        metrics[index][2] = 0

        clear_screen()
        print(f'Reset metric "{metrics[index][1]}" to 0 succesfully.')
        print_data(metrics)
    else:
        sys.exit("Operation cancelled. Aborting.")


def remove_metric(metric_id, metrics):
    """Removes a metric.

    Args:
        metric_id: ID of the metric. The metrics are one-indexed.
        metrics: A list of all metrics.
    """

    if decision_confirmed():
        index = metric_id - 1
        metric_name = metrics[index][1]

        for metric in metrics[index + 1 :]:
            metric[0] -= 1

        del metrics[index]

        clear_screen()
        print(f'Removed metric "{metric_name}" succesfully.')
        print_data(metrics)
    else:
        sys.exit("Operation cancelled. Aborting.")


def delete_metrics(metrics):
    """Deletes all metrics.

    Args:
        metrics: A list of all metrics.
    """

    if decision_confirmed():
        metrics.clear()
        clear_screen()
        print("Deleted the data succesfully.\n")
    else:
        sys.exit("Operation cancelled. Aborting.")


def list_metrics(metrics):
    """Pretty-prints the metrics to the terminal.

    Args:
        metrics: A list of all metrics.
    """

    if metrics:
        clear_screen()
        print_data(metrics)
    else:
        sys.exit("There isn't any data to list. Aborting.")
