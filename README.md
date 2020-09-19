# Metrics Tracker

A command-line metrics tracker.

## Installation

1. Clone this repo:

```bash
git clone https://github.com/ziebam/metrics_tracker.git
```

2. Specify the path to the file where you want to store your metrics by editing the `config.ini` file in the root directory. The path has to be absolute and the target file has to have a `.pickle` extension. For example:

```bash
[paths]
data_file_path = D:\dev\metrics_tracker\data.pickle
```

3. Install the project with `pip install .` to use it with an `mt` alias.

The project does not have any dependencies other than Python 3.8+, so there is no need to set up a venv.

## Usage

Run the script with `mt -h` to see a relevant help message.

## License

[MIT](LICENSE)
