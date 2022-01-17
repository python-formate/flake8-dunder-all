# stdlib
import re
from typing import List

# 3rd party
import pytest
from click.testing import CliRunner, Result
from coincidence.regressions import AdvancedFileRegressionFixture
from consolekit.terminal_colours import Fore
from domdf_python_tools.paths import PathPlus

# this package
from flake8_dunder_all.__main__ import main
from tests.test_flake8_dunder_all import (
		mangled_source,
		testing_source_a,
		testing_source_b,
		testing_source_c,
		testing_source_d,
		testing_source_e,
		testing_source_f,
		testing_source_g,
		testing_source_h,
		testing_source_i
		)


@pytest.mark.parametrize(
		"source, members, ret",
		[
				pytest.param("import foo", [], 0, id="just an import"),
				pytest.param('"""a docstring"""', [], 0, id="just a docstring"),
				pytest.param(testing_source_a, [], 0, id="import and docstring"),
				pytest.param(testing_source_b, ["a_function"], 1, id="function no __all__"),
				pytest.param(testing_source_c, ["Foo"], 1, id="class no __all__"),
				pytest.param(testing_source_d, ["Foo", "a_function"], 1, id="function and class no __all__"),
				pytest.param(testing_source_e, ["Foo", "a_function"], 0, id="function and class with __all__"),
				pytest.param(
						testing_source_f, ["Foo", "a_function"],
						0,
						id="function and class with __all__ and extra variable"
						),
				pytest.param(testing_source_g, ["a_function"], 1, id="async function no __all__"),
				pytest.param(testing_source_h, [], 0, id="from import"),
				pytest.param(testing_source_i, [], 1, id="lots of lines"),
				pytest.param(
						f"  # noqa: DALL000  \n{testing_source_g}",
						[],
						0,
						id="async function no __all__ and noqa",
						),
				]
		)
def test_main(tmp_pathplus: PathPlus, source: str, members: List[str], ret: int):
	tmpfile = tmp_pathplus / "source.py"
	tmpfile.write_text(source)

	runner = CliRunner()
	result: Result = runner.invoke(main, catch_exceptions=False, args=[str(tmpfile)])
	assert result.exit_code == ret

	if members:
		members_string = ", ".join(f'"{m}"' for m in members)
		assert f"__all__ = [{members_string}]" in tmpfile.read_text()


@pytest.mark.parametrize(
		"source, members, ret",
		[
				pytest.param("import foo", [], 0, id="just an import"),
				pytest.param('"""a docstring"""', [], 0, id="just a docstring"),
				pytest.param(testing_source_a, [], 0, id="import and docstring"),
				pytest.param(testing_source_b, ["a_function"], 1, id="function no __all__"),
				pytest.param(testing_source_c, ["Foo"], 1, id="class no __all__"),
				pytest.param(testing_source_d, ["Foo", "a_function"], 1, id="function and class no __all__"),
				pytest.param(testing_source_g, ["a_function"], 1, id="async function no __all__"),
				pytest.param(testing_source_h, [], 0, id="from import"),
				pytest.param(testing_source_i, [], 1, id="lots of lines"),
				]
		)
def test_main_single_quotes(capsys, tmp_pathplus: PathPlus, source: str, members: List[str], ret: int):
	tmpfile = tmp_pathplus / "source.py"
	tmpfile.write_text(source)

	runner = CliRunner()
	result: Result = runner.invoke(main, catch_exceptions=False, args=[str(tmpfile), "--quote-type='"])
	assert result.exit_code == ret

	if members:
		members_string = ", ".join(f"'{m}'" for m in members)
		assert f"__all__ = [{members_string}]" in tmpfile.read_text()

	assert result.stdout == f"Checking {tmpfile}\n"


@pytest.mark.parametrize("source, members", [
		pytest.param(mangled_source, [], id="mangled"),
		])
def test_main_mangled(tmp_pathplus: PathPlus, capsys, source: str, members: List[str]):
	tmpfile = tmp_pathplus / "source.py"
	tmpfile.write_text(source)

	runner = CliRunner(mix_stderr=False)
	result: Result = runner.invoke(main, catch_exceptions=False, args=[str(tmpfile)])
	assert result.exit_code == 4

	stderr = result.stderr
	assert re.match(r".*'.*source.py' does not appear to be a valid Python source file\..*\n", stderr)
	assert stderr.startswith(Fore.RED)
	assert stderr.endswith(f"{Fore.RESET}\n")


# TODO: Test the number of lines in the output


def test_main_no_filenames(capsys):
	runner = CliRunner()
	result: Result = runner.invoke(main, catch_exceptions=False)

	assert result.stdout == ''


def test_main_help(capsys, advanced_file_regression: AdvancedFileRegressionFixture):
	runner = CliRunner()

	result: Result = runner.invoke(main, catch_exceptions=False, args=["-h"])
	advanced_file_regression.check(result.stdout)

	result = runner.invoke(main, catch_exceptions=False, args=["--help"])
	advanced_file_regression.check(result.stdout)
