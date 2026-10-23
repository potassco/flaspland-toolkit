---
icon: material/file-code
---

# Encodings

An encoding is one or more `.lp` files that turn the
[input facts](../problem/index.md#input) of an environment into a plan made of
[`action/3` atoms](../problem/index.md#output).

## Passing encodings to `solve.py`

Every argument after the environment is loaded into clingo:

```console
python solve.py envs/pkl/env_001--2_2.pkl encodings/main.lp
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
- `solve.py` adds the environment facts itself; do not include `envs/lp/*.lp`.

## Testing an encoding without simulating

While developing, it is often quicker to run clingo directly on the facts of an
environment and look at the answer:

```console
python -m clingo envs/lp/env_001--2_2.lp encodings/main.lp
```

Add `#show action/3.` to your encoding to see only the plan. Once the actions
look right, run the full simulation with `solve.py`.

!!! tip
    `python -m clingo` is the clingo that was installed with flaspland, so it
    always matches the version `solve.py` uses.

## Things to keep in mind

- **Enumeration:** `solve.py` asks clingo for *all* models and simulates the
  last one. An encoding with many equally good answers can therefore take a
  long time. Use optimisation statements (`#minimize`) so that clingo
  reports better and better plans, or make sure the plan is unique.
- **Fixed plans** like `test.lp` work only on the environment they were written
  for, and cannot react to [malfunctions](../problem/index.md#replanning-after-a-malfunction).
