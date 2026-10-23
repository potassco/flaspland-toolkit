"""
Tests for the flaspland command line tools.

They run the commands in a temporary folder, the way a user would in their own
repository, using the sample environment from examples/.
"""

import contextlib
import io
import pickle
import shutil
import tempfile
from pathlib import Path
from unittest import TestCase

from flaspland import cli, solve
from flaspland.modules.convert import convert_to_clingo

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


class InTempDir(TestCase):
    """
    Run each test in a fresh temporary folder that contains the sample files.
    """

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        self.addCleanup(tmp.cleanup)
        self.enterContext(contextlib.chdir(tmp.name))
        shutil.copy(EXAMPLES / "envs" / "pkl" / "test.pkl", "test.pkl")
        shutil.copy(EXAMPLES / "test.lp", "test.lp")


class TestCLI(InTempDir):
    """
    The `flaspland` dispatcher and `flaspland init`.
    """

    def test_help(self) -> None:
        """
        Without a command, the help is printed.
        """
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(cli.main([]), 1)
        for command in ("init", "build", "solve"):
            self.assertIn(command, out.getvalue())

    def test_unknown_command(self) -> None:
        """
        An unknown command is an error.
        """
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as ctx:
            cli.main(["bogus"])
        self.assertEqual(ctx.exception.code, 2)

    def test_init(self) -> None:
        """
        `init` creates config.toml once and does not overwrite it.
        """
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["init"]), 0)
        self.assertIn("number_of_agents", Path("config.toml").read_text(encoding="utf-8"))
        with self.assertRaises(SystemExit):
            cli.main(["init"])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["init", "--force"]), 0)


class TestBuild(InTempDir):
    """
    `flaspland build`.
    """

    def test_build(self) -> None:
        """
        An environment is saved in all three formats under envs/.
        """
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cli.main(["build", "--seed", "1", "--width", "25", "--height", "25"]), 0)
        name = "env_001--2_2"
        for ext in ("lp", "pkl", "png"):
            self.assertTrue(Path("envs", ext, f"{name}.{ext}").is_file())
        facts = Path("envs", "lp", f"{name}.lp").read_text(encoding="utf-8")
        self.assertIn("train(1).", facts)

    def test_config(self) -> None:
        """
        Settings are read from config.toml in the current folder; flags override them.
        """
        Path("config.toml").write_text("number_of_agents = 3\n", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            cli.main(["build", "--seed", "1", "--width", "25", "--height", "25"])
            cli.main(["build", "--seed", "1", "--width", "25", "--height", "25", "--agents", "1"])
        self.assertTrue(Path("envs", "pkl", "env_001--3_2.pkl").is_file())
        self.assertTrue(Path("envs", "pkl", "env_002--1_2.pkl").is_file())


class TestSolve(InTempDir):
    """
    `flaspland solve`.
    """

    def run_solve(self, *args: str) -> str:
        """
        Run `flaspland solve` and return what it printed.
        """
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cli.main(["solve", *args]), 0)
        return out.getvalue()

    def test_sample(self) -> None:
        """
        The sample solution runs and writes the animation and the log.
        """
        self.run_solve("test.pkl", "test.lp")
        (output,) = Path("output").iterdir()
        self.assertTrue((output / "animation.gif").is_file())
        lines = (output / "paths.csv").read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], "agent;timestep;position;direction;status;given_command")
        self.assertIn("0;2;(13, 10);e;moving;move_forward", lines)

    def test_optimization(self) -> None:
        """
        With optimization statements the optimal model is used, unless clingo is told otherwise.
        """
        Path("opt.lp").write_text(
            '#include "test.lp".\n{ x(1..5) }.\n:- not x(_).\n#minimize { X : x(X) }.\n', encoding="utf-8"
        )
        self.assertIn("with cost [1] (optimal)", self.run_solve("test.pkl", "opt.lp", "--no-render"))
        first = self.run_solve("test.pkl", "opt.lp", "--no-render", "--", "-n", "1")
        self.assertIn("using model 1 ", first)
        self.assertIn("optimality not proven", first)

    def test_unsatisfiable(self) -> None:
        """
        A clear error is given when there is no plan.
        """
        Path("unsat.lp").write_text('#include "test.lp".\n:- action(train(0),wait,0).\n', encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as ctx:
            cli.main(["solve", "test.pkl", "unsat.lp", "--no-render"])
        self.assertIn("No plan found", str(ctx.exception.code))

    def test_missing_environment(self) -> None:
        """
        A missing environment file is reported without a traceback.
        """
        with self.assertRaises(SystemExit) as ctx:
            cli.main(["solve", "missing.pkl", "test.lp"])
        self.assertIn("missing.pkl", str(ctx.exception.code))

    def test_clingo_arguments(self) -> None:
        """
        Arguments after `--` and --time-limit are passed on to clingo.
        """
        args = solve.get_args(["e.pkl", "a.lp", "b.lp", "--time-limit", "5", "--", "-t", "4"])
        self.assertEqual(args.encodings, ["a.lp", "b.lp"])
        self.assertEqual(args.clingo_args, ["-t", "4", "--time-limit=5"])


class TestConvert(TestCase):
    """
    Conversion of environments to clingo facts.
    """

    def test_sample_facts(self) -> None:
        """
        The facts of the sample environment match envs/lp/test.lp.
        """
        with open(EXAMPLES / "envs" / "pkl" / "test.pkl", "rb") as f:
            env = pickle.load(f)
        facts = convert_to_clingo(env)
        self.assertIn("start(0,(13,10),0,e).", facts)
        self.assertIn("end(1,(14,10),34).", facts)
        self.assertEqual(facts, (EXAMPLES / "envs" / "lp" / "test.lp").read_text(encoding="utf-8"))
