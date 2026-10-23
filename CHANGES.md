# Changes

## Unreleased

- declare all runtime dependencies in `pyproject.toml`, so `pip install -e .`
  installs everything (Python 3.11 or 3.12)
- `solve.py` takes encodings on the command line instead of `asp/params.py`
- `solve.py` supports flatland 4.3 and gives clear errors for outdated `.pkl`
  files and when no plan is found
- documentation: getting started, examples, problem specification, encodings,
  command line reference and troubleshooting

## v0.1.0

- create project
