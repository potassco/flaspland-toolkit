# flaspland

Generate [Flatland](https://flatland.aicrowd.com) railway environments and solve
them with answer set programming using [clingo](https://potassco.org/clingo/).

## Installation

Install the toolkit once; the `flaspland` command then works in any folder.

```bash
git clone https://github.com/potassco/flaspland-toolkit.git
cd flaspland-toolkit
conda env create -f environment.yml
```

This creates a conda environment `flaspland` with Python 3.12 and all
dependencies. Without conda, use any Python 3.11 or 3.12 environment and run
`pip install -e .` in this folder. See the
[getting started guide](docs/getting_started.md) for details.

## Usage

Activate the environment and go to your own project folder:

```bash
conda activate flaspland
cd my-project

flaspland init                       # create config.toml with the build settings
flaspland build 5 --agents 3         # generate environments into envs/
flaspland solve envs/pkl/env_001--3_2.pkl encodings/main.lp
```

Results are saved to `output/<date>_<time>/` as `animation.gif` and
`paths.csv`. Run `flaspland <command> -h` for all options.

To try the sample solution that comes with the toolkit:

```bash
cd flaspland-toolkit/examples
flaspland solve envs/pkl/test.pkl test.lp
```

## Documentation

The documentation covers installation, examples, the input and output format
of encodings, and troubleshooting. To view it locally:

```bash
pip install -e ".[doc]"
mkdocs serve -o
```

Instructions for running the tests and code checks can be found in
[DEVELOPMENT.md](./DEVELOPMENT.md).
