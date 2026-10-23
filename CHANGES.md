# Changes

## Unreleased

- declare all runtime dependencies in `pyproject.toml`, so `pip install -e .`
  installs everything (Python 3.11 or 3.12)
- `solve.py` takes encodings on the command line instead of `asp/params.py`
- `solve.py` supports flatland 4.3 and gives clear errors for outdated `.pkl`
  files and when no plan is found
- documentation: getting started, examples, problem specification, encodings,
  command line reference and troubleshooting
- installable `flaspland` command with `flaspland init`, `flaspland build` and
  `flaspland solve` that work in any folder; `environment.yml` for conda
- `flaspland solve`: `--time-limit`, clingo options after `--`, prints which
  model is simulated, shows only `action/3` (plus your `#show`s) while solving,
  and saves results to `output/<date>_<time>/`
- the sample environment and solution moved to `examples/`
- tests for the command line tools; CI runs them with Python 3.11 and 3.12

## v0.1.0

- create project
