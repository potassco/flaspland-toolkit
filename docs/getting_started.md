---
hide:
  - navigation
---

# Getting started

## Requirements

- **Python 3.11 or 3.12.** Python 3.13 and newer are not supported yet: Flatland
  needs `numpy<2`, which is not available for them.
- **git**, to download the project.

Check your version with `python --version`. If it is not 3.11 or 3.12, create a
separate environment with the right version first (see below). This also keeps
flaspland's packages away from your other projects.

## Installation

=== "conda"

    ```console
    conda create -n flaspland python=3.12 -y
    conda activate flaspland
    git clone https://github.com/potassco/flaspland-toolkit.git && cd flaspland-toolkit && pip install -e .
    ```

=== "venv (macOS / Linux)"

    ```console
    git clone https://github.com/potassco/flaspland-toolkit.git && cd flaspland-toolkit
    python3.12 -m venv .venv
    source .venv/bin/activate
    pip install -e .
    ```

=== "venv (Windows)"

    ```console
    git clone https://github.com/potassco/flaspland-toolkit.git && cd flaspland-toolkit
    py -3.12 -m venv .venv
    .venv\Scripts\activate
    pip install -e .
    ```

`pip install -e .` installs everything flaspland needs: Flatland, clingo,
imageio and Pillow. The exact list lives in the `dependencies` section of
`pyproject.toml`, so every machine installs the same versions.

!!! note "Remember to activate"
    Run `conda activate flaspland` (or `source .venv/bin/activate`) in every new
    terminal before using flaspland.

## Check that it works

The tools are run from the `src/flaspland` folder:

```console
cd src/flaspland
python solve.py envs/pkl/test.pkl test.lp
```

This loads the sample environment `test.pkl`, solves it with the sample
solution `test.lp` and simulates the result. When it finishes you will find a
new folder `output/<timestamp>/` with:

- `animation.gif`: the trains moving through the network, and
- `paths.csv`: the position, direction and status of every train at every step.

If you see an error instead, look it up on the [Help](community/help.md) page.

## Project layout

```text
src/flaspland/
├── build.py        # generate environments
├── config.toml     # default parameters for build.py
├── solve.py        # solve an environment with your encodings and simulate it
├── test.lp         # sample solution for envs/pkl/test.pkl
├── envs/
│   ├── lp/         # environments as clingo facts   (input for your encoding)
│   ├── pkl/        # environments as Flatland files (input for solve.py)
│   └── png/        # environments as pictures
├── modules/        # helper code used by build.py and solve.py
└── output/         # created by solve.py: one folder per run
```

## Next steps

1. Generate your own environments: [Examples](examples/index.md#generating-environments).
2. Read what your encoding receives and must produce:
   [Problem specification](reference/problem/index.md).
3. Write an encoding and run it:
   [Organising encodings](examples/index.md#organising-encodings-with-include).
