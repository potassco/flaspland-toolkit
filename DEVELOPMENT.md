# Development

This page is for people working on the toolkit itself. Users of the toolkit
only need the installation instructions in the README.

## Project layout

```text
src/flaspland/          # the Python package behind the `flaspland` command
├── cli.py              # `flaspland` command: dispatches to init, build and solve
├── build.py            # `flaspland build`
├── solve.py            # `flaspland solve`
├── config.toml         # template copied by `flaspland init`
└── modules/            # helpers: conversion to clingo facts, saving, clingo app
examples/               # sample environment and solution, exploration notebook
tests/                  # unit tests (run with nox, see below)
docs/                   # documentation (mkdocs)
src/archive/            # earlier prototype, not installed
```

The package is installed in editable mode (`pip install -e .`), so changes to
`src/flaspland` take effect without reinstalling.

## Tests and checks

The project template comes with several tools for keeping the code healthy.
All of them are run through [nox], a tool that creates a fresh virtual
environment for each task. We recommend installing nox using [pipx] to have it
available globally.

```bash
# install
python -m pip install pipx
python -m pipx install nox

# run the default sessions (the tests)
nox

# list all sessions
nox -l

# run individual session
nox -s session_name

# run individual session (reuse install)
nox -Rs session_name
```

| Session | What it does | Runs by default / in CI |
| --- | --- | --- |
| `test` | Runs the unit tests in `tests/` and reports the test coverage. | yes |
| `lint_pylint` | [pylint] looks for likely bugs and style problems. | no |
| `typecheck` | [mypy] checks type annotations (`--strict`). | no |
| `dev` | Creates `.nox/dev`, an environment with all development tools. | no |

The lint and type checks are not run by default because the code does not
follow their (strict) rules yet; run them by hand to see what they report.
Once the code passes them, add them back to `nox.options.sessions` in
`noxfile.py` so that CI enforces them.

Note that the nox sessions create [editable] installs. In case there are
issues, try recreating environments by dropping the `-R` option.

### Automatic formatting

We also provide a [pre-commit][pre] config that formats the code (black, isort,
autoflake) and Markdown files (mdformat) before every commit. It is optional
and only active on machines where it has been set up:

```bash
python -m pipx install pre-commit
pre-commit install
```

Running it for the first time reformats most Python files, so do this in a
separate commit (`pre-commit run --all`).

## Continuous integration

GitHub Actions run the following workflows (see `.github/workflows/`):

- `test.yml`: runs `nox` (the tests) on Linux, macOS and Windows with Python
  3.11 and 3.12, on every push to `main`, `master`, `devel` or `wip`, and on
  pull requests.
- `doc.yml`: builds the documentation and publishes it on GitHub Pages when a
  version tag is pushed (see [DEPLOYMENT.md](./DEPLOYMENT.md)).
- `deploy.yml`: publishes the package on PyPI when a version tag is pushed.

## Documentation

Make sure the documentation dependencies for the project are properly installed
with

```bash
pip install -e ".[doc]"
```

To run the documentation locally use the following command and click the
provided link to open it in the browser.

```bash
mkdocs serve
```

[editable]: https://setuptools.pypa.io/en/latest/userguide/development_mode.html
[mypy]: https://mypy.readthedocs.io/
[nox]: https://nox.thea.codes/en/stable/index.html
[pipx]: https://pypa.github.io/pipx/
[pre]: https://pre-commit.com/
[pylint]: https://pylint.readthedocs.io/
