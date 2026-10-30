# flaspland

Welcome to the `flaspland-toolkit`!

## Installation

Install the toolkit once; the `flaspland` command then works in any folder.

```bash
git clone https://github.com/potassco/flaspland-toolkit.git && cd flaspland-toolkit
conda env create -f environment.yml 
```

After installing the project, activate the newly-created environment and navigate to your project repository. Once inside, initialize the flaspland tool for that repository.
```bash
conda activate flaspland
cd my-project-repo
flaspland init
```

From there you are free to start using `flaspland` with your project.

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
