---
icon: material/help-circle
---

# Help

## Troubleshooting

Find the message you see below. Most problems come from the Python environment
or from running a command in the wrong folder.

### Installation

??? failure "`requires a different Python: 3.13.x not in '<3.13,>=3.11'`"
    flaspland needs Python 3.11 or 3.12. Create an environment with a supported
    version and install again. In the `flaspland-toolkit` folder, run:

    ```console
    conda env create -f environment.yml
    conda activate flaspland
    ```

    See [Getting started](../getting_started.md#installation) for `venv`
    instructions.

??? failure "`zsh: no matches found: .[doc]`"
    The default shell on macOS treats square brackets specially. Put the
    argument in quotes:

    ```console
    pip install -e ".[doc]"
    ```

??? failure "`flaspland: command not found` or `ModuleNotFoundError: No module named 'flatland'`"
    flaspland is not installed in the Python you are using. Usually the
    environment is not activated in this terminal: run
    `conda activate flaspland` (or activate your `venv`, see
    [Getting started](../getting_started.md#activate-the-environment)) and try
    again. If that does not help, run `pip install -e .` in the
    `flaspland-toolkit` folder with the environment activated.

### Running flaspland build and flaspland solve

??? failure "`Could not load '….pkl' (No module named 'flatland.core.grid.rail_env_grid')`"
    The `.pkl` file was created with a different version of Flatland. Flatland
    reorganises its code between releases, so saved environments only load with
    the version that created them. Create the environment again with
    `flaspland build`.

??? failure "`error: file could not be opened` (from clingo)"
    clingo cannot find one of the encoding files. Paths on the command line are
    relative to the folder you are in, so check the path (tab completion
    helps). Paths inside `#include` statements are relative to the file
    containing them.

??? failure "`No plan found for the initial plan` / `No plan found while replanning after a malfunction`"
    clingo found no answer set (look for `UNSATISFIABLE` above the message) or
    stopped because of an error in an encoding (look for `error:`).

    - **UNSATISFIABLE at the start**: the encoding has no plan for this
      environment. Test it directly with
      `python -m clingo envs/lp/<env>.lp <encoding>.lp` and remove constraints
      until it becomes satisfiable, to find the one that is too strict.
    - **UNSATISFIABLE while replanning**: the new plan has to keep the
      executed actions and let the broken train wait. Fixed plans such as
      `test.lp` cannot do that. See
      [Replanning after a malfunction](../reference/problem/index.md#replanning-after-a-malfunction).

??? warning "`UserWarning: Simulation has reached its end before actions list has been exhausted.`"
    Flatland ended the episode (all trains arrived, or the step limit
    `global(T)` was reached) while the plan still had actions left. If all
    trains arrived this is harmless; otherwise the plan is too slow.

??? info "`info: atom does not occur in any rule head` and `warning: already included file`"
    These are clingo notices, not errors. The first one often appears while
    replanning, when the added facts mention an action your encoding never
    derives. The second one means a file was included twice and only loaded
    once.

??? question "`flaspland solve` runs for a very long time"
    - Look at the clingo output. If it keeps printing `Answer:` lines with a
      decreasing `Optimization:` value, clingo is still improving the plan:
      add `--time-limit 60` to simulate the best plan found after a minute.
      See [Optimisation and time limits](../examples/index.md#optimisation-and-time-limits).
    - If clingo prints nothing for a long time, grounding or solving your
      encoding is hard. Test it on a small environment with
      `python -m clingo envs/lp/<env>.lp <encoding>.lp --stats`.
    - Add `--no-render` if the simulation itself is slow: drawing the
      animation takes most of that time.

??? question "My environments or results are in a different folder"
    `flaspland build` writes to `envs/` and `flaspland solve` writes to
    `output/` in the folder you run them from. Run them in your project
    folder.

??? question "`[--no-render]` is treated as a file name"
    Square brackets in usage messages only mean "optional". Type the option
    without them: `flaspland solve envs/pkl/test.pkl test.lp --no-render`.

## Further help

!!! tip "Search"
    Use the search bar at the top of this page to find what you are looking
    for.

!!! tip "Look at the examples"
    The [examples](../examples/index.md) show the most common tasks step by
    step.

!!! question "Open an issue"
    Search the [issue tracker][issues] first, then open an [issue][new_issue]
    describing your problem. Include the full command you ran, the complete
    error message, and the output of `flaspland --version`,
    `python --version` and `pip show flatland-rl clingo`.

!!! tip "Mailing list"
    The Potassco [mailing list][mailing_list] may already have an answer. You
    can also [subscribe] to get updates and join the community.

## General ASP support

- Take a look at the [support page][support_page] of Potassco.

[mailing_list]: https://sourceforge.net/p/potassco/mailman/potassco-users/
[subscribe]: https://sourceforge.net/projects/potassco/lists/potassco-users/
[support_page]: https://potassco.org/support/
[new_issue]: https://github.com/potassco/flaspland-toolkit/issues/new
[issues]: https://github.com/potassco/flaspland-toolkit/issues
