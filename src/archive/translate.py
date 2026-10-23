"""
A Python file that uses the Clingo API to translate 
a given Flatland environment into a standard fact format.
"""
from importlib.resources import path
import pickle
import sys

from clingo import Function, Number, Symbol
from typing import Iterator, List
from pickle import dump, load
from argparse import FileType

# basic facts
def _cell(x: int, y: int, t: int) -> Function:
    """Returns a fact representing a cell at coordinates (X,Y) with track type T."""
    return Function("cell", [Function("", [Number(x), Number(y)]), Number(t)])

def _train(z: int) -> Function:
    """Returns a fact representing a train with handle Z."""
    return Function("train", [Number(z)])

def _global(g: int) -> Function:
    """Returns a fact representing the global maximum number of steps G."""
    return Function("global", [Number(g)])

def grid_facts(env) -> Iterator[Symbol]:
    """Returns an iterator of cell facts representing the grid of the Flatland environment."""
    yield _global(env._max_episode_steps)
    for c in range(env.width):
        for r in range(env.height):
            yield _cell(c,r,env.rail.grid[c][r])

def train_facts(env) -> Iterator[Symbol]:
    """Returns an iterator of train facts representing the trains in the Flatland environment."""
    dirs = {
        0: Function("n"),
        1: Function("e"),
        2: Function("s"),
        3: Function("w"),
    }

    for i, agent in enumerate(env.agents):
        yield _train(i)
        yield Function("start", [
            Number(i),
            Function("", [
                Number(env.agents[i].initial_position[0]),
                Number(env.agents[i].initial_position[1])
            ]),
            Number(env.agents[i].earliest_departure),
            dirs[env.agents[i].initial_direction]
        ])
        yield Function("end", [
            Number(i), 
            Function("", [
                Number(env.agents[i].target[0]),
                Number(env.agents[i].target[1])
            ]), Number(env.agents[i].latest_arrival)])
        yield Function("speed", [
            Number(i), 
            Number(int(1/env.agents[i].speed_counter.speed))
            ])

def env_to_symbols(env) -> List[Symbol]:
    return sorted({*grid_facts(env), *train_facts(env)}, key=str)

# file management
def load_env(path: str):
    with open(sys.argv[1], 'rb') as f:
        return pickle.load(f)

def main(argv=None) -> int:
    import argparse, sys
    p = argparse.ArgumentParser(description="Flatland env -> ASP facts")
    p.add_argument("env", help="path to saved environment (.pkl)")
    p.add_argument("-o", "--out", type=argparse.FileType("w"), default=sys.stdout)
    args = p.parse_args(argv)

    symbols = env_to_symbols(load_env(args.env))
    args.out.write("\n".join(str(s) for s in symbols))
    args.out.write("\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())