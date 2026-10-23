# flaspland

Generate [Flatland](https://flatland.aicrowd.com) railway environments and solve
them with answer set programming using [clingo](https://potassco.org/clingo/).

## Installation

flaspland needs **Python 3.11 or 3.12**. Create an environment and install
everything with one command:

```bash
conda create -n flaspland python=3.12 -y && conda activate flaspland
git clone https://github.com/potassco/flaspland-toolkit.git && cd flaspland-toolkit && pip install -e .
```

All required packages are listed under `dependencies` in `pyproject.toml`. See
the [getting started guide](docs/getting_started.md) for `venv` and Windows
instructions.

## Usage

The tools are run from `src/flaspland`:

```bash
cd src/flaspland

# solve the sample environment with the sample solution
python solve.py envs/pkl/test.pkl test.lp

# generate new environments (settings in config.toml)
python build.py 5 --agents 3

# solve one of them with your own encodings
python solve.py envs/pkl/env_001--3_2.pkl encodings/main.lp
```

Results are saved to `output/<timestamp>/` as `animation.gif` and `paths.csv`.
Run `python build.py -h` or `python solve.py -h` for all options.

## Documentation

The documentation covers installation, examples, the input and output format
of encodings, and troubleshooting. To view it locally:

```bash
pip install -e ".[doc]"
mkdocs serve -o
```

Instructions to install and use `nox` can be found in
[DEVELOPMENT.md](./DEVELOPMENT.md).
