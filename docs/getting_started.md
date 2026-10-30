---
hide:
  - navigation
---

# Getting started

flaspland is installed once on your machine. After that, the `flaspland`
command works in any folder, for example in your own (course) repository.

## Requirements

- **Python 3.11 or 3.12.** Python 3.13 and newer are not supported yet: Flatland
  needs `numpy<2`, which is not available for them. The installation below
  creates an environment with the right version for you.
- **git**, to download the toolkit.

## Installation

=== "conda (recommended)"

    ```console
    git clone https://github.com/potassco/flaspland-toolkit.git
    cd flaspland-toolkit
    conda env create -f environment.yml
    ```

    This creates a conda environment called `flaspland` with Python 3.12 and
    everything flaspland needs.

=== "venv (macOS / Linux)"

    ```console
    git clone https://github.com/potassco/flaspland-toolkit.git
    cd flaspland-toolkit
    python3.12 -m venv .venv
    source .venv/bin/activate
    pip install -e .
    ```

=== "venv (Windows)"

    ```console
    git clone https://github.com/potassco/flaspland-toolkit.git
    cd flaspland-toolkit
    py -3.12 -m venv .venv
    .venv\Scripts\activate
    pip install -e .
    ```

The installation pulls in Flatland, clingo, imageio and Pillow. The exact list
lives in the `dependencies` section of `pyproject.toml`, so every machine
installs the same versions.

## Activate the environment

In every new terminal, activate the environment before using flaspland. This
works from any folder:

=== "conda"

    ```console
    conda activate flaspland
    ```

=== "venv (macOS / Linux)"

    ```console
    source /path/to/flaspland-toolkit/.venv/bin/activate
    ```

=== "venv (Windows)"

    ```console
    \path\to\flaspland-toolkit\.venv\Scripts\activate
    ```

Check that it works:

```console
flaspland --version
```

## Start your own project

Go to the folder you want to work in, for example your group's repository, and
run:

```console
flaspland init                                      # create config.toml
flaspland build 3                                   # generate 3 environments into envs/
flaspland solve envs/pkl/env_001--2_2.pkl encodings/main.lp
```

`flaspland solve` needs an encoding, of course. See
[Problem specification](reference/problem/index.md) for what it receives and
must produce, and [Examples](examples/index.md#organising-encodings-with-include)
for how to organise it.

Your folder will then look like this:

```text
my-project/
├── config.toml       # settings for `flaspland build` (created by `flaspland init`)
├── encodings/
│   └── main.lp       # your encodings
├── envs/
│   ├── lp/           # environments as clingo facts   (input for your encoding)
│   ├── pkl/          # environments as Flatland files (input for `flaspland solve`)
│   └── png/          # environments as pictures
└── output/           # created by `flaspland solve`: one folder per run
```

!!! tip
    Add `output/` to your repository's `.gitignore`: every run creates a new
    folder with an animation in it.

## Try the sample solution

The toolkit comes with a small environment and a hand-written solution for it:

```console
cd flaspland-toolkit/examples
flaspland solve envs/pkl/test.pkl test.lp
```

When it finishes you will find a new folder `output/<date>_<time>/` with:

- `animation.gif`: the trains moving through the network, and
- `paths.csv`: the position, direction and status of every train at every step.

If you see an error instead, look it up on the [Help](community/help.md) page.

## Updating

```console
cd flaspland-toolkit
git pull
```

The toolkit is installed in editable mode, so the update takes effect
immediately. If `git pull` changed `pyproject.toml`, also run `pip install -e .`
again (with the environment activated) to pick up new dependencies.
