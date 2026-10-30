"""Run a dummy simulation from a pickled environment and an ASP encoding.

This is a placeholder implementation: it validates inputs and prints a
canned fake-simulation summary so the CLI pipeline can be exercised
end-to-end before the real Clingo + Flatland loop is wired in.
"""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any


def run(
    env_path: Path,
    encoding_path: Path,
    replan_encoding_path: Path | None = None,
) -> dict[str, Any]:
    """Pretend to solve and simulate. Returns a result dict."""
    if not env_path.exists():
        raise FileNotFoundError(f"Environment file not found: {env_path}")
    if not encoding_path.exists():
        raise FileNotFoundError(f"Encoding file not found: {encoding_path}")

    lp_path = env_path.with_suffix(".lp")
    if not lp_path.exists():
        raise FileNotFoundError(
            f"ASP facts file not found: {lp_path} "
            "(expected alongside the .pkl from `flasp build`)"
        )

    with open(env_path, "rb") as f:
        env = pickle.load(f)
    env_facts_preview = lp_path.read_text(encoding="utf-8").splitlines()[:3]

    print("  [dummy run] loaded env.pkl")
    if isinstance(env, dict) and "params" in env:
        p = env["params"]
        print(f"  [dummy run] params: width={p.get('width')} "
              f"height={p.get('height')} "
              f"agents={p.get('agents')} "
              f"seed={p.get('seed')}")
    print(f"  [dummy run] encoding: {encoding_path.name}")
    if replan_encoding_path is not None:
        print(f"  [dummy run] replan:   {replan_encoding_path.name}")
    print(f"  [dummy run] first facts: {env_facts_preview}")

    # Fake plan: three timesteps, two agents.
    fake_plan = [
        (0, "move_forward", 0),
        (1, "move_forward", 0),
        (0, "move_forward", 1),
        (1, "wait",         1),
        (0, "move_forward", 2),
        (1, "move_forward", 2),
    ]
    for agent, action, t in fake_plan:
        print(f"    t={t}  agent={agent}  action={action}")

    print("  [dummy run] all agents arrived (fake)")
    return {"all_arrived": True, "timesteps": 3, "plan": fake_plan}
