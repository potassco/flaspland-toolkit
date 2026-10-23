"""
The `flaspland` command: dispatches to `flaspland init`, `flaspland build` and `flaspland solve`.
"""

import shutil
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path

from . import __version__

COMMANDS = {
    "init": "create config.toml with the default settings for 'flaspland build'",
    "build": "generate Flatland environments into envs/",
    "solve": "solve an environment with your encodings and simulate the plan",
}

CONFIG_TEMPLATE = Path(__file__).resolve().parent / "config.toml"


def init(argv) -> int:
    """ copy the default config.toml into the current folder """
    parser = ArgumentParser(prog="flaspland init", description=COMMANDS["init"].capitalize() + ".")
    parser.add_argument("--force", action="store_true", help="overwrite an existing config.toml")
    args = parser.parse_args(argv)

    target = Path("config.toml")
    if target.exists() and not args.force:
        raise SystemExit("config.toml already exists; use --force to overwrite it")
    shutil.copyfile(CONFIG_TEMPLATE, target)
    print("created config.toml; edit it and run 'flaspland build'")
    return 0


def main(argv=None) -> int:
    """ run the flaspland command line interface """
    argv = sys.argv[1:] if argv is None else list(argv)

    # the commands are imported only when used, as loading Flatland takes a moment
    if argv and argv[0] == "init":
        return init(argv[1:])
    if argv and argv[0] == "build":
        from . import build  # pylint: disable=import-outside-toplevel
        return build.main(argv[1:])
    if argv and argv[0] == "solve":
        from . import solve  # pylint: disable=import-outside-toplevel
        return solve.main(argv[1:])

    commands = "\n".join(f"  {name:8}{text}" for name, text in COMMANDS.items())
    parser = ArgumentParser(
        prog="flaspland",
        description="Generate Flatland environments and solve them with clingo.",
        epilog=f"commands:\n{commands}\n\nRun 'flaspland <command> -h' for the options of a command.",
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("command", choices=COMMANDS, metavar="command", help="one of: " + ", ".join(COMMANDS))
    if not argv:
        parser.print_help()
        return 1
    parser.parse_args(argv)  # prints the help, the version or an error and exits
    return 1
