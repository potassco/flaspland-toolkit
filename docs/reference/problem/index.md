---
icon: material/head-dots-horizontal
---

# Problem specification

A Flatland environment is a grid of cells, some of which contain railway track.
Every train has a start cell, a departure time, a target cell and a latest
arrival time. The task is to tell every train, at every time step, which action
to take so that all trains reach their targets in time without colliding.

Your encoding receives the environment as facts (input) and must produce one
action per train and time step (output).

## Coordinates and directions

- Cells are written `(Y,X)`: `Y` is the row (0 at the top) and `X` the
  column (0 on the left).
- Directions are `n`, `e`, `s` and `w`.

## Input

These facts are generated from the environment. You can see them for any
environment in `envs/lp/<name>.lp`.

| Fact | Meaning |
| --- | --- |
| `global(T)` | The simulation runs for at most `T` steps. |
| `train(ID)` | There is a train with number `ID`. |
| `speed(ID,S)` | Train `ID` needs `S` steps per cell (`1` = full speed). |
| `start(ID,(Y,X),Dep,Dir)` | Train `ID` starts at cell `(Y,X)` facing `Dir`, and may depart at step `Dep` at the earliest. |
| `waypoint(ID,Ord,(Y,X),Dir,Arr,Dep)` | Intermediate stop number `Ord` of train `ID`: reach `(Y,X)` facing `Dir` by step `Arr`, leave at step `Dep` at the earliest. Only present when environments are built with `--line-length 3` or more. |
| `end(ID,(Y,X),Arr)` | Train `ID` must reach cell `(Y,X)` by step `Arr`. |
| `cell((Y,X),V)` | Cell `(Y,X)` has track type `V` (see below). `V = 0` means there is no track. |

### Track types

The value `V` in `cell((Y,X),V)` is a 16-bit number that says which moves the
cell allows. Read it in binary as four groups of four bits, for a train facing
**N, E, S, W** (in that order). Within each group the bits say whether the train
may leave the cell going **N, E, S, W**.

| `V` | Binary | Meaning |
| --- | --- | --- |
| `32800` | `1000 0000 0010 0000` | Straight north–south track: facing N go N, facing S go S. |
| `1025` | `0000 0100 0000 0001` | Straight east–west track: facing E go E, facing W go W. |
| `4608` | `0001 0010 0000 0000` | Curve: facing N go W, facing E go S. |
| `37408` | `1001 0010 0010 0000` | Switch: facing N go N or W, facing E go S, facing S go S. |

In clingo you can decode a value with integer arithmetic, for example "a train
facing direction number `D` (N=0, E=1, S=2, W=3) can leave towards direction
number `O`":

```prolog
dir(n,0). dir(e,1). dir(s,2). dir(w,3).
allowed((Y,X),D,O) :- cell((Y,X),V), dir(_,D), dir(_,O),
                      (V / 2**(15 - 4*D - O)) \ 2 = 1.
```

## Output

Your encoding must produce atoms of the form

```prolog
action(train(ID),Action,T).
```

for every train `ID` and time step `T`, starting at `0`, where `Action` is one of

| Action | Effect |
| --- | --- |
| `move_forward` | Enter the map (if not on it yet), or keep going straight / follow the track. |
| `move_left` | Take the left branch at a switch. |
| `move_right` | Take the right branch at a switch. |
| `wait` | Stay where you are. |

`flaspland solve` uses the last model clingo reports: the first plan found,
or, with optimisation statements, the best plan found. Other atoms in the model
are ignored.

`test.lp` is an example of a complete, valid output for `envs/pkl/test.pkl`.

## Replanning after a malfunction

When a train breaks down during the simulation, `flaspland solve` runs your encodings
again on the same environment, with these extra facts and constraints added:

| Added | Meaning |
| --- | --- |
| `:- not action(train(ID),A,T).` | Actions that have already been executed. They are fixed. |
| `malfunction(ID,D,T).` | Train `ID` broke down at step `T` for `D` steps. |
| `:- not action(train(ID),wait,T).` | The broken train has to wait during its repair. |
| `planned_action(train(ID),A,T).` | The remaining part of the previous plan, which you can reuse, for example to change as little as possible. |

The new plan must again consist of `action/3` atoms as described above.
