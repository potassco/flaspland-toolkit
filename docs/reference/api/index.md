---
title: "Command line reference"
icon: "material/console"
---

# Command line reference

Both tools are run from the `src/flaspland` folder.

## build.py

Generates environments and saves each one to `envs/lp/`, `envs/pkl/` and
`envs/png/`.

```console
python build.py [num_envs] [options]
```

Settings are taken from `config.toml` unless given as a flag
(flag > config file > built-in default).

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
to change need to be present.

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

## solve.py

Solves an environment with your encodings, simulates the plan in Flatland and
replans when a train breaks down.

```console
python solve.py ENV ENCODING [ENCODING ...] [--no-render]
```

| Argument | Meaning |
| --- | --- |
| `ENV` | The environment, a `.pkl` file created by `build.py`. |
| `ENCODING` | One or more `.lp` files, for example a single main file of `#include` statements. |
| `--no-render` | Simulate without drawing the animation (much faster). |

Each run creates a new folder `output/<timestamp>/` containing:

| File | Contents |
| --- | --- |
| `animation.gif` | The simulation, one frame per step (not created with `--no-render`). |
| `paths.csv` | One line per train and step: `agent;timestep;position;direction;status;given_command`. |

The `status` column is one of `waiting`, `ready to depart`, `moving`,
`stopped`, `malfunction (on map)`, `malfunction (off map)` and `done`.
