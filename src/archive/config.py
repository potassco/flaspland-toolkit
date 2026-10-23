"""Load flaspland.toml defaults and merge CLI overrides."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]


CONFIG_FILENAME = "flaspland.toml"


def find_config(start: Path | None = None) -> Path | None:
    directory = (start or Path.cwd()).resolve()
    for parent in [directory, *directory.parents]:
        candidate = parent / CONFIG_FILENAME
        if candidate.exists():
            return candidate
    return None


def load_config(path: Path | None = None) -> dict[str, Any]:
    config_path = path or find_config()
    if config_path is None:
        return {}
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def build_params(config: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    """Compose the parameter dict for one build.

    Starts from `[build]` in flaspland.toml, flattens the nested
    `[build.speeds]` and `[build.malfunctions]` tables, then applies CLI
    overrides (which win when not None).
    """
    build_section = dict(config.get("build", {}))
    speeds = build_section.pop("speeds", {})
    malfunctions = build_section.pop("malfunctions", {})

    params: dict[str, Any] = dict(build_section)
    if speeds:
        raw_map = speeds.get("speed_ratio_map", {})
        params["speed_ratio_map"] = {float(k): float(v) for k, v in raw_map.items()}
    if malfunctions:
        params["malfunction_rate"] = malfunctions.get("rate", 0.0)
        params["malfunction_min_duration"] = malfunctions.get("min_duration", 0)
        params["malfunction_max_duration"] = malfunctions.get("max_duration", 0)

    for key, value in overrides.items():
        if value is not None:
            params[key] = value

    return params
