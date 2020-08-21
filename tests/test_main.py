# stdlib
import re
from typing import List

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.terminal_colours import Fore

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
				pytest.param('import foo', [], 0, id="just an import"),
				pytest.param('"""a docstring"""', [], 0, id="just a docstring"),
				pytest.param(testing_source_a, [], 0, id="import and docstring"),
				pytest.param(testing_source_b, ['a_function'], 1, id="function no __all__"),
				pytest.param(testing_source_c, ['Foo'], 1, id="class no __all__"),
				pytest.param(testing_source_d, ['Foo', 'a_function'], 1, id="function and class no __all__"),
				pytest.param(testing_source_e, ['Foo', 'a_function'], 0, id="function and class with __all__"),
				pytest.param(
						testing_source_f, ['Foo', 'a_function'],
						0,
						id="function and class with __all__ and extra variable"
						),
				pytest.param(testing_source_g, ["a_function"], 1, id="async function no __all__"),
				pytest.param(testing_source_h, [], 0, id="from import"),
				pytest.param(testing_source_i, [], 1, id="lots of lines"),
				]
		)
def test_main(tmpdir, source, members: List[str], ret):
	tmpfile = PathPlus(tmpdir) / "source.py"
	tmpfile.write_text(source)

	assert main([str(tmpfile)]) == ret

	if members:
		members_string = ", ".join(f'"{m}"' for m in members)
		assert f"__all__ = [{members_string}]" in tmpfile.read_text()


@pytest.mark.parametrize(
		"source, members, ret",
		[
				pytest.param('import foo', [], 0, id="just an import"),
				pytest.param('"""a docstring"""', [], 0, id="just a docstring"),
				pytest.param(testing_source_a, [], 0, id="import and docstring"),
				pytest.param(testing_source_b, ['a_function'], 1, id="function no __all__"),
				pytest.param(testing_source_c, ['Foo'], 1, id="class no __all__"),
				pytest.param(testing_source_d, ['Foo', 'a_function'], 1, id="function and class no __all__"),
				pytest.param(testing_source_g, ["a_function"], 1, id="async function no __all__"),
				pytest.param(testing_source_h, [], 0, id="from import"),
				pytest.param(testing_source_i, [], 1, id="lots of lines"),
				]
		)
def test_main_single_quotes(capsys, tmpdir, source, members: List[str], ret):
	tmpfile = PathPlus(tmpdir) / "source.py"
	tmpfile.write_text(source)

	assert main([str(tmpfile), "--quote-type='"]) == ret

	if members:
		members_string = ", ".join(f"'{m}'" for m in members)
		assert f"__all__ = [{members_string}]" in tmpfile.read_text()

	assert capsys.readouterr().out == f"Checking {tmpfile}\n"


@pytest.mark.parametrize("source, members", [
		pytest.param(mangled_source, [], id="mangled"),
		])
def test_main_mangled(tmpdir, capsys, source, members):
	tmpfile = PathPlus(tmpdir) / "source.py"
	tmpfile.write_text(source)
	assert main([str(tmpfile)]) == 4

	stderr = capsys.readouterr().err
	assert re.match(r".*'.*source.py' does not appear to be a valid Python source file\..*\n", stderr)
	assert stderr.startswith(Fore.RED)
	assert stderr.endswith(f"{Fore.RESET}\n")


# TODO: Test the number of lines in the output


def test_main_no_filenames(capsys):
	main([])

	assert capsys.readouterr().out == ''
