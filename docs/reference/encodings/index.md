---
icon: material/file-code
---

# Encodings

An encoding is one or more `.lp` files that turn the
[input facts](../problem/index.md#input) of an environment into a plan made of
[`action/3` atoms](../problem/index.md#output).

## Passing encodings to `flaspland solve`

Every argument after the environment is loaded into clingo:

```console
flaspland solve envs/pkl/env_001--2_2.pkl encodings/main.lp
```

The recommended setup is one main file per variant that only contains
`#include` statements:

```prolog title="encodings/main.lp"
#include "paths.lp".
#include "timing.lp".
#include "collisions.lp".
```

- `#include` paths are relative to the file that contains them.
- Each file is included only once, even if several files include it.
- `flaspland solve` adds the environment facts itself; do not include
  `envs/lp/*.lp`.

## Testing an encoding without simulating

While developing, it is often quicker to run clingo directly on the facts of an
environment and look at the answer:

```console
python -m clingo envs/lp/env_001--2_2.lp encodings/main.lp
```

Add `#show action/3.` to your encoding to see only the plan. Once the actions
look right, run the full simulation with `flaspland solve`.

!!! tip
    `python -m clingo` is the clingo that was installed with flaspland, so it
    always matches the version `flaspland solve` uses.

## Things to keep in mind

- **Which plan is used:** without optimisation statements, the first plan
  clingo finds is simulated. With `#minimize` or weak constraints, clingo
  continues until the plan is optimal and that plan is simulated; use
  `--time-limit` if this takes too long. See
  [Optimisation and time limits](../../examples/index.md#optimisation-and-time-limits).
- **Output:** while solving, clingo prints the `action/3` atoms of each plan it
  finds, plus anything your encodings `#show`.
- **Fixed plans** like `test.lp` work only on the environment they were written
  for, and cannot react to [malfunctions](../problem/index.md#replanning-after-a-malfunction).
