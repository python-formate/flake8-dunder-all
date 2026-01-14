# stdlib
import ast
import re
import sys
from typing import List, Set

# 3rd party
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture
from consolekit.terminal_colours import Fore
from domdf_python_tools.paths import PathPlus

# this package
from flake8_dunder_all import AlphabeticalOptions, Plugin, Visitor, check_and_add_all
from flake8_dunder_all.utils import mark_text_ranges
from tests.common import (
		if_type_checking_else_source,
		if_type_checking_source,
		if_type_checking_try_finally_source,
		if_type_checking_try_source,
		mangled_source,
		not_type_checking_if_source,
		results,
		testing_source_a,
		testing_source_b,
		testing_source_c,
		testing_source_d,
		testing_source_e,
		testing_source_e_tuple,
		testing_source_f,
		testing_source_f_tuple,
		testing_source_g,
		testing_source_h,
		testing_source_i,
		testing_source_j,
		testing_source_k,
		testing_source_l,
		testing_source_m,
		testing_source_n
		)


@pytest.mark.parametrize(
		"source, expects",
		[
				pytest.param("import foo", set(), id="just an import"),
				pytest.param('"""a docstring"""', set(), id="just a docstring"),
				pytest.param(testing_source_a, set(), id="import and docstring"),
				pytest.param(testing_source_b, {"1:0: DALL000 Module lacks __all__."}, id="function no __all__"),
				pytest.param(testing_source_c, {"1:0: DALL000 Module lacks __all__."}, id="class no __all__"),
				pytest.param(
						testing_source_d,
						{"1:0: DALL000 Module lacks __all__."},
						id="function and class no __all__.",
						),
				pytest.param(testing_source_e, set(), id="function and class with __all__."),
				pytest.param(testing_source_f, set(), id="function and class with __all__. and extra variable"),
				pytest.param(
						testing_source_g,
						{"1:0: DALL000 Module lacks __all__."},
						id="async function no __all__",
						),
				pytest.param(testing_source_h, set(), id="from import"),
				pytest.param(testing_source_i, {"1:0: DALL000 Module lacks __all__."}, id="lots of lines"),
				pytest.param(testing_source_j, {"1:0: DALL000 Module lacks __all__."}, id="multiline import"),
				],
		)
def test_plugin(source: str, expects: Set[str]):
	assert results(source) == expects


@pytest.mark.parametrize(
		"source, dunder_all_alphabetical, expects",
		[
				pytest.param(
						"__all__ = ['foo', 'bar', 'Baz']",
						AlphabeticalOptions.NONE,
						set(),
						id="NONE_wrong_order",
						),
				pytest.param(
						"__all__ = ['bar', 'Baz', 'foo']",
						AlphabeticalOptions.NONE,
						set(),
						id="NONE_right_order_1",
						),
				pytest.param(
						"__all__ = ['Bar', 'baz', 'foo']",
						AlphabeticalOptions.NONE,
						set(),
						id="NONE_right_order_2",
						),
				pytest.param(
						"__all__ = ['foo', 'bar', 'Baz']",
						AlphabeticalOptions.IGNORE,
						{"1:0: DALL001 __all__ not sorted alphabetically."},
						id="IGNORE_wrong_order",
						),
				pytest.param(
						"__all__ = ['bar', 'Baz', 'foo']",
						AlphabeticalOptions.IGNORE,
						set(),
						id="IGNORE_right_order",
						),
				pytest.param(
						"__all__ = ['Baz', 'bar', 'foo']",
						AlphabeticalOptions.LOWER,
						{"1:0: DALL001 __all__ not sorted alphabetically (lowercase first)."},
						id="LOWER_wrong_order",
						),
				pytest.param(
						"__all__ = ['bar', 'foo', 'Baz']",
						AlphabeticalOptions.LOWER,
						set(),
						id="LOWER_right_order",
						),
				pytest.param(
						"__all__ = ['bar', 'Baz', 'foo']",
						AlphabeticalOptions.UPPER,
						{"1:0: DALL001 __all__ not sorted alphabetically (uppercase first)."},
						id="UPPER_wrong_order",
						),
				pytest.param(
						"__all__ = ['Baz', 'bar', 'foo']",
						AlphabeticalOptions.UPPER,
						set(),
						id="UPPER_right_order_1",
						),
				pytest.param(
						"__all__ = ['Baz', 'Foo', 'bar']",
						AlphabeticalOptions.UPPER,
						set(),
						id="UPPER_right_order_2",
						),
				],
		)
def test_plugin_alphabetical(source: str, expects: Set[str], dunder_all_alphabetical: AlphabeticalOptions):
	plugin = Plugin(ast.parse(source), "mod.py")
	plugin.dunder_all_alphabetical = dunder_all_alphabetical
	assert {"{}:{}: {}".format(*r) for r in plugin.run() if "DALL0" in r[2]} == expects


@pytest.mark.parametrize(
		"source, dunder_all_alphabetical, expects",
		[
				pytest.param(
						"__all__: List[str] = ['foo', 'bar', 'Baz']",
						AlphabeticalOptions.NONE,
						set(),
						id="NONE_wrong_order",
						),
				pytest.param(
						"__all__: List[str] = ['bar', 'Baz', 'foo']",
						AlphabeticalOptions.NONE,
						set(),
						id="NONE_right_order_1",
						),
				pytest.param(
						"__all__: List[str] = ['Bar', 'baz', 'foo']",
						AlphabeticalOptions.NONE,
						set(),
						id="NONE_right_order_1",
						),
				pytest.param(
						"__all__: List[str] = ['foo', 'bar', 'Baz']",
						AlphabeticalOptions.IGNORE,
						{"1:0: DALL001 __all__ not sorted alphabetically."},
						id="IGNORE_wrong_order",
						),
				pytest.param(
						"__all__: List[str] = ['bar', 'Baz', 'foo']",
						AlphabeticalOptions.IGNORE,
						set(),
						id="IGNORE_right_order",
						),
				pytest.param(
						"__all__: List[str] = ['Baz', 'bar', 'foo']",
						AlphabeticalOptions.LOWER,
						{"1:0: DALL001 __all__ not sorted alphabetically (lowercase first)."},
						id="LOWER_wrong_order",
						),
				pytest.param(
						"__all__: List[str] = ['bar', 'foo', 'Baz']",
						AlphabeticalOptions.LOWER,
						set(),
						id="LOWER_right_order",
						),
				pytest.param(
						"__all__: List[str] = ['bar', 'Baz', 'foo']",
						AlphabeticalOptions.UPPER,
						{"1:0: DALL001 __all__ not sorted alphabetically (uppercase first)."},
						id="UPPER_wrong_order",
						),
				pytest.param(
						"__all__: List[str] = ['Baz', 'bar', 'foo']",
						AlphabeticalOptions.UPPER,
						set(),
						id="UPPER_right_order_1",
						),
				pytest.param(
						"__all__: List[str] = ['Baz', 'Foo', 'bar']",
						AlphabeticalOptions.UPPER,
						set(),
						id="UPPER_right_order_2",
						),
				],
		)
def test_plugin_alphabetical_ann_assign(
		source: str,
		expects: Set[str],
		dunder_all_alphabetical: AlphabeticalOptions,
		):
	plugin = Plugin(ast.parse(source), "mod.py")
	plugin.dunder_all_alphabetical = dunder_all_alphabetical
	assert {"{}:{}: {}".format(*r) for r in plugin.run() if "DALL0" in r[2]} == expects


@pytest.mark.parametrize(
		"source, dunder_all_alphabetical",
		[
				pytest.param("__all__ = 12345", AlphabeticalOptions.IGNORE, id="IGNORE_123"),
				pytest.param("__all__ = 12345", AlphabeticalOptions.LOWER, id="LOWER_123"),
				pytest.param("__all__ = 12345", AlphabeticalOptions.NONE, id="NONE_123"),
				pytest.param("__all__ = 12345", AlphabeticalOptions.UPPER, id="UPPER_123"),
				pytest.param("__all__ = abc", AlphabeticalOptions.IGNORE, id="IGNORE_abc"),
				pytest.param("__all__ = abc", AlphabeticalOptions.LOWER, id="LOWER_abc"),
				pytest.param("__all__ = abc", AlphabeticalOptions.NONE, id="NONE_abc"),
				pytest.param("__all__ = abc", AlphabeticalOptions.UPPER, id="UPPER_abc"),
				],
		)
def test_plugin_alphabetical_not_list(source: str, dunder_all_alphabetical: AlphabeticalOptions):
	plugin = Plugin(ast.parse(source), "mod.py")
	plugin.dunder_all_alphabetical = dunder_all_alphabetical
	msg = "1:0: DALL002 __all__ not a list or tuple of strings."
	assert {"{}:{}: {}".format(*r) for r in plugin.run() if "DALL0" in r[2]} == {msg}


def test_plugin_alphabetical_tuple():
	plugin = Plugin(ast.parse("__all__ = ('bar',\n'foo')"), "mod.py")
	plugin.dunder_all_alphabetical = AlphabeticalOptions.IGNORE
	assert {"{}:{}: {}".format(*r) for r in plugin.run() if "DALL0" in r[2]} == set()


@pytest.mark.parametrize(
		"source, members, found_all, last_import",
		[
				pytest.param("import foo", [], False, 1, id="just an import"),
				pytest.param('"""a docstring"""', [], False, 0, id="just a docstring"),
				pytest.param(testing_source_a, [], False, 3, id="import and docstring"),
				pytest.param(testing_source_b, ["a_function"], False, 3, id="function no __all__"),
				pytest.param(testing_source_c, ["Foo"], False, 3, id="class no __all__"),
				pytest.param(
						testing_source_d,
						["Foo", "a_function"],
						False,
						3,
						id="function and class no __all__",
						),
				pytest.param(
						testing_source_e,
						["Foo", "a_function"],
						True,
						3,
						id="function and class with __all__",
						),
				pytest.param(
						testing_source_f,
						["Foo", "a_function"],
						True,
						3,
						id="function and class with __all__ and extra variable",
						),
				pytest.param(testing_source_g, ["a_function"], False, 3, id="async function no __all__"),
				pytest.param(testing_source_h, [], False, 1, id="from import"),
				pytest.param(testing_source_i, ["a_function"], False, 3, id="lots of lines"),
				pytest.param(testing_source_j, ["a_function"], False, 2, id="multiline import"),
				pytest.param(testing_source_m, ["a_function"], False, 7, id="if False"),
				pytest.param(if_type_checking_source, ["a_function"], False, 5, id="if TYPE_CHECKING:"),
				],
		)
def test_visitor(source: str, members: List[str], found_all: bool, last_import: int):
	visitor = Visitor()
	visitor.visit(ast.parse(source))

	assert sorted(visitor.members) == members
	assert visitor.found_all is found_all
	assert visitor.last_import is last_import


@pytest.mark.parametrize(
		"source, members, found_all, last_import",
		[
				pytest.param("import foo", [], False, 1, id="just an import"),
				pytest.param('"""a docstring"""', [], False, 0, id="just a docstring"),
				pytest.param(testing_source_a, [], False, 3, id="import and docstring"),
				pytest.param(testing_source_b, ["a_function"], False, 3, id="function no __all__"),
				pytest.param(testing_source_c, ["Foo"], False, 3, id="class no __all__"),
				pytest.param(
						testing_source_d,
						["Foo", "a_function"],
						False,
						3,
						id="function and class no __all__",
						),
				pytest.param(
						testing_source_e,
						["Foo", "a_function"],
						True,
						3,
						id="function and class with __all__",
						),
				pytest.param(
						testing_source_f,
						["Foo", "a_function"],
						True,
						3,
						id="function and class with __all__ and extra variable",
						),
				pytest.param(testing_source_g, ["a_function"], False, 3, id="async function no __all__"),
				pytest.param(testing_source_h, [], False, 1, id="from import"),
				pytest.param(testing_source_i, ["a_function"], False, 3, id="lots of lines"),
				pytest.param(testing_source_j, ["a_function"], False, 14, id="multiline import"),
				pytest.param(testing_source_m, ["a_function"], False, 7, id="if False"),
				pytest.param(if_type_checking_source, ["a_function"], False, 5, id="if TYPE_CHECKING:"),
				pytest.param(if_type_checking_else_source, ["a_function"], False, 5, id="if TYPE_CHECKING else"),
				pytest.param(if_type_checking_try_source, ["a_function"], False, 8, id="if TYPE_CHECKING try"),
				pytest.param(not_type_checking_if_source, ["a_function"], False, 2, id="not TYPE_CHECKING if"),
				pytest.param(
						if_type_checking_try_finally_source,
						["a_function"],
						False,
						10,
						id="if TYPE_CHECKING try finally",
						),
				],
		)
def test_visitor_endlineno(source: str, members: List[str], found_all: bool, last_import: int):
	visitor = Visitor(True)
	tree = ast.parse(source)
	mark_text_ranges(tree, source)
	visitor.visit(tree)

	assert sorted(visitor.members) == members
	assert visitor.found_all is found_all
	assert visitor.last_import is last_import


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
						testing_source_f,
						["Foo", "a_function"],
						0,
						id="function and class with __all__ and extra variable",
						),
				pytest.param(testing_source_g, ["a_function"], 1, id="async function no __all__"),
				pytest.param(testing_source_h, [], 0, id="from import"),
				pytest.param(testing_source_i, [], 1, id="lots of lines"),
				pytest.param(testing_source_k, [], 0, id="overload"),
				pytest.param(testing_source_l, [], 0, id="typing.overload"),
				pytest.param(testing_source_m, [], 1, id="if False"),
				pytest.param(testing_source_n, [], 1, id="if TYPE_CHECKING"),
				pytest.param(if_type_checking_else_source, [], 1, id="if TYPE_CHECKING else"),
				pytest.param(if_type_checking_try_source, [], 1, id="if TYPE_CHECKING try"),
				pytest.param(if_type_checking_try_finally_source, [], 1, id="if TYPE_CHECKING try finally"),
				pytest.param(not_type_checking_if_source, [], 1, id="not TYPE_CHECKING if"),
				],
		)
def test_check_and_add_all(
		tmp_pathplus: PathPlus,
		source: str,
		members: List[str],
		ret: int,
		advanced_file_regression: AdvancedFileRegressionFixture,
		):
	tmpfile = tmp_pathplus / "source.py"
	tmpfile.write_text(source)

	assert check_and_add_all(tmpfile) == ret
	advanced_file_regression.check_file(tmpfile)

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
				pytest.param(
						testing_source_e_tuple,
						["Foo", "a_function"],
						0,
						id="function and class with __all__",
						),
				pytest.param(
						testing_source_f_tuple,
						["Foo", "a_function"],
						0,
						id="function and class with __all__ and extra variable",
						),
				pytest.param(testing_source_g, ["a_function"], 1, id="async function no __all__"),
				pytest.param(testing_source_h, [], 0, id="from import"),
				pytest.param(testing_source_i, [], 1, id="lots of lines"),
				pytest.param(testing_source_k, [], 0, id="overload"),
				pytest.param(testing_source_l, [], 0, id="typing.overload"),
				pytest.param(testing_source_m, [], 1, id="if False"),
				pytest.param(testing_source_n, [], 1, id="if TYPE_CHECKING"),
				],
		)
def test_check_and_add_all_tuples(
		tmp_pathplus: PathPlus,
		source: str,
		members: List[str],
		ret: int,
		advanced_file_regression: AdvancedFileRegressionFixture,
		):
	tmpfile = tmp_pathplus / "source.py"
	tmpfile.write_text(source)

	assert check_and_add_all(tmpfile, use_tuple=True) == ret
	advanced_file_regression.check_file(tmpfile)

	if members:
		members_string = ", ".join(f'"{m}"' for m in members)
		assert f"__all__ = ({members_string}, )" in tmpfile.read_text()


@pytest.mark.skipif(condition=not (sys.version_info < (3, 8)), reason="Not required after python 3.8")
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
				pytest.param(testing_source_m, [], 1, id="if False"),
				pytest.param(testing_source_n, [], 1, id="if TYPE_CHECKING"),
				],
		)
def test_check_and_add_all_single_quotes(tmp_pathplus: PathPlus, source: str, members: List[str], ret: int):
	tmpfile = tmp_pathplus / "source.py"
	tmpfile.write_text(source)

	assert check_and_add_all(tmpfile, quote_type="'") == ret

	if members:
		members_string = ", ".join(f"'{m}'" for m in members)
		assert f"__all__ = [{members_string}]" in tmpfile.read_text()


@pytest.mark.parametrize(
		"source, members",
		[
				pytest.param(mangled_source, [], id="mangled"),
				],
		)
def test_check_and_add_all_mangled(tmp_pathplus: PathPlus, capsys, source: str, members: List[str]):
	tmpfile = tmp_pathplus / "source.py"
	tmpfile.write_text(source)
	assert check_and_add_all(tmpfile) == 4

	stderr = capsys.readouterr().err
	assert re.match(r".*'.*source.py' does not appear to be a valid Python source file\..*\n", stderr)
	assert stderr.startswith(Fore.RED)
	assert stderr.endswith(f"{Fore.RESET}\n")


# TODO: Test the number of lines in the output
