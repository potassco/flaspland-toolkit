---
title: "Command line reference"
icon: "material/console"
---

# Command line reference

All commands work in the current folder: environments are read from and
written to `envs/`, results to `output/`. Run `flaspland <command> -h` to see
the options in the terminal.

## flaspland init

Creates `config.toml` with the default settings for `flaspland build`, so you
can edit them.

```console
flaspland init [--force]
```

| Option | Meaning |
| --- | --- |
| `--force` | Overwrite an existing `config.toml`. |

## flaspland build

Generates environments and saves each one to `envs/lp/`, `envs/pkl/` and
`envs/png/`.

```console
flaspland build [num_envs] [options]
```

Settings are taken from `config.toml` in the current folder, if it exists,
unless given as a flag (flag > config file > built-in default).

| Option | Default | Meaning |
| --- | --- | --- |
| `num_envs` | `1` | Number of environments to create. |
| `-c`, `--config FILE` | `config.toml` | TOML file with the settings. |
| `-s`, `--seed N` | random | First seed. Every attempt uses the next seed, so a run can be repeated exactly. |
| `--width N`, `--height N` | `30` | Size of the grid in cells. |
| `--cities N` | `2` | Maximum number of cities (at least 2). |
| `--grid-mode` / `--no-grid-mode` | off | Place cities on a regular grid instead of randomly. |
| `--rails-between-cities N` | `2` | Maximum rails connecting two cities. |
| `--rail-pairs-in-city N` | `2` | Maximum parallel track pairs in a city. |
| `-a`, `--agents N` | `2` | Number of trains. |
| `-l`, `--line-length N` | Flatland default | Cities each train visits, counting start and end (`3` = one intermediate stop). Needs `--cities` ≥ `N`. |
| `--speed-ratio-map MAP` | `1.0:1.0` | Share of trains per speed, e.g. `1.0:0.5,0.5:0.5`. Shares must add up to 1. |
| `--remove-agents-at-target` / `--no-remove-agents-at-target` | on | Take trains off the grid when they arrive. |
| `--malfunction-rate P` | `0.0` | Chance per train and step of a breakdown (0 = none). |
| `--min-duration N`, `--max-duration N` | `20`, `50` | Shortest and longest breakdown, in steps. |

Environments are named `env_<number>--<trains>_<cities>`. Numbering continues
after the highest existing environment.

### config.toml

The same settings as the flags, using the names below. Only the keys you want
to change need to be present. `flaspland init` creates a commented version of
this file.

```toml
width  = 30
height = 30
max_num_cities = 2
grid_mode = false
max_rails_between_cities = 2
max_rail_pairs_in_city = 2

number_of_agents = 2
remove_agents_at_target = true
# line_length = 3

malfunction_rate = 0.0
min_duration = 20
max_duration = 50

# seed = 42

# keep this section last
[speed_ratio_map]
"1.0" = 1.0
```

## flaspland solve

Solves an environment with your encodings, simulates the plan in Flatland and
replans when a train breaks down.

```console
flaspland solve ENV ENCODING [ENCODING ...] [options] [-- CLINGO_OPTIONS]
```

| Argument | Meaning |
| --- | --- |
| `ENV` | The environment, a `.pkl` file created by `flaspland build`. |
| `ENCODING` | One or more `.lp` files, for example a single main file of `#include` statements. |
| `--time-limit SECONDS` | Stop each clingo call after this many seconds and use the best plan found so far. |
| `--no-render` | Simulate without drawing the animation (much faster). |
| `-- CLINGO_OPTIONS` | Everything after `--` is passed to clingo, e.g. `-- --parallel-mode=4`. |

clingo runs with its usual settings: it stops at the first plan, unless the
encodings contain optimisation statements, in which case it continues until the
optimal plan is found. The last plan clingo reports is simulated, and
`flaspland solve` prints which one it used.

Each run creates a new folder `output/<date>_<time>/` containing:

| File | Contents |
| --- | --- |
| `animation.gif` | The simulation, one frame per step (not created with `--no-render`). |
| `paths.csv` | One line per train and step: `agent;timestep;position;direction;status;given_command`. |

The `status` column is one of `waiting`, `ready to depart`, `moving`,
`stopped`, `malfunction (on map)`, `malfunction (off map)` and `done`.
