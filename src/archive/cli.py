"""`flasp` command-line interface.

Two subcommands:

    flasp build -n N [overrides...]
        Generate N environments using defaults from flaspland.toml,
        writing .pkl / .lp / .png triples into --out-dir (default: envs/).

    flasp run --env env.pkl --enc encoding.lp [--replan replan.lp]
        Solve an environment with an ASP encoding and simulate it.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import click

from . import __version__
from .build import build_environment
from .config import build_params, load_config
from .run import run as run_simulation


@click.group()
@click.version_option(__version__, prog_name="flasp")
def main() -> None:
    """flaspland — Flatland + ASP toolkit."""


# ---------------------------------------------------------------------------
# flasp build
# ---------------------------------------------------------------------------

@main.command()
@click.option("-n", "--num", type=int, default=1, show_default=True,
              help="Number of environments to generate.")
@click.option("--out-dir", type=click.Path(file_okay=False), default="envs",
              show_default=True, help="Directory to write outputs into.")
@click.option("--config", "config_path", type=click.Path(exists=True, dir_okay=False),
              default=None, help="Path to flaspland.toml (default: search upward).")
@click.option("--overwrite", is_flag=True, default=False,
              help="Regenerate even if output files already exist.")
# Per-parameter overrides (None = fall back to the toml default)
@click.option("--width", type=int, default=None, help="Grid width.")
@click.option("--height", type=int, default=None, help="Grid height.")
@click.option("--agents", type=int, default=None, help="Number of agents.")
@click.option("--max-cities", type=int, default=None, help="Max cities.")
@click.option("--seed", type=int, default=None,
              help="Base seed. For -n > 1, subsequent envs use seed+1, seed+2, ...")
@click.option("--grid-mode/--no-grid-mode", default=None,
              help="Toggle Flatland grid_mode.")
@click.option("--max-rails-between-cities", type=int, default=None)
@click.option("--max-rail-pairs-in-city", type=int, default=None)
def build(
    num: int,
    out_dir: str,
    config_path: Optional[str],
    overwrite: bool,
    **overrides,
) -> None:
    """Build N environments using flaspland.toml defaults + flag overrides."""
    cfg = load_config(Path(config_path) if config_path else None)
    params = build_params(cfg, overrides)

    out = Path(out_dir)
    base_seed = params.get("seed", 0)

    click.echo(f"Building {num} environment(s) → {out}/")
    for i in range(num):
        env_params = dict(params)
        env_params["seed"] = base_seed + i
        stem = out / f"env_{i}"
        try:
            paths = build_environment(env_params, stem, overwrite=overwrite)
        except FileExistsError as e:
            click.echo(f"  – env_{i}: {e}", err=True)
            continue
        click.echo(f"  ✓ env_{i}: {paths['pkl'].name}, {paths['lp'].name}, {paths['png'].name}")


# ---------------------------------------------------------------------------
# flasp run
# ---------------------------------------------------------------------------

@main.command()
@click.option("--env", "env_path", required=True,
              type=click.Path(exists=True, dir_okay=False, path_type=Path),
              help="Path to the environment .pkl produced by `flasp build`.")
@click.option("--enc", "encoding_path", required=True,
              type=click.Path(exists=True, dir_okay=False, path_type=Path),
              help="Path to the primary ASP encoding .lp.")
@click.option("--replan", "replan_path", default=None,
              type=click.Path(exists=True, dir_okay=False, path_type=Path),
              help="Optional replanning encoding (used on malfunction).")
def run(env_path: Path, encoding_path: Path, replan_path: Optional[Path]) -> None:
    """Solve and simulate an environment with an ASP encoding."""
    click.echo(f"Running: env={env_path}  enc={encoding_path}"
               + (f"  replan={replan_path}" if replan_path else ""))
    result = run_simulation(env_path, encoding_path, replan_path)
    click.echo(f"  done in {result.get('timesteps', '?')} timesteps  "
               f"(all_arrived={result.get('all_arrived')})")


if __name__ == "__main__":  # pragma: no cover
    main()
