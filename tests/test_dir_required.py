from __future__ import annotations

# stdlib
import ast
import inspect
from typing import Any

# this package
from flake8_dunder_all import Plugin


def from_source(source: str, filename: str) -> list[tuple[int, int, str, type[Any]]]:
	source_clean = inspect.cleandoc(source)
	plugin = Plugin(ast.parse(source_clean), filename)
	return list(plugin.run())


def test_dir_required_non_init():
	source = """
	import foo
	"""
	results = from_source(source, "module.py")
	assert any("DALL100" in r[2] for r in results)


def test_dir_required_non_init_with_dir():
	# __dir__ defined, should not yield DALL100
	source_with_dir = """
	def __dir__():
		return []\n"""
	results = from_source(source_with_dir, "module.py")
	assert not any("DALL100" in r[2] for r in results)


def test_dir_required_empty():
	source = """\nimport foo\n"""
	# No __dir__ defined but no members present, should not yield DALL101
	results = from_source(source, "__init__.py")
	assert not any("DALL101" in r[2] for r in results)


def test_dir_required_init():
	source = """\nimport foo\n\nclass Foo: ...\n"""
	# No __dir__ defined, should yield DALL101
	results = from_source(source, "__init__.py")
	assert any("DALL101" in r[2] for r in results)


def test_dir_required_init_with_dir():
	# __dir__ defined, should not yield DALL101
	source_with_dir = """\ndef __dir__():\n	return []\n"""
	results = from_source(source_with_dir, "__init__.py")
	assert not any("DALL101" in r[2] for r in results)
