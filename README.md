# flaspland

> Remove this block after following the instructions below to use the template.
>
> This project template is configured to ease collaboration. Linters,
> formatters, and actions are already configured and ready to use.
>
> To use the project template, run the `init.py` script to give the project a
> name and some metadata. The script can then be removed and the
> `pyproject.toml` file be adjusted as needed.

## Installation

To install the project, run

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

Run the following for basic usage information:

```bash
flaspland -h
```

To generate and open the documentation, run

```bash
mkdocs serve -o
```

Make sure to install the optional documentation dependencies via

```bash
pip install .[doc]
```

Instructions to install and use `nox` can be found in
[DEVELOPMENT.md](./DEVELOPMENT.md)
