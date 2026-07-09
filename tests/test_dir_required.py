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

	class Foo: ...
	"""
	results = from_source(source, "module.py")
	assert any("DALL100" in r[2] for r in results)


def test_dir_required_non_init_with_dir():
	# __dir__ defined, should not yield DALL100
	source_with_dir = """
	class Foo: ...

	def __dir__():
		return []
	"""
	results = from_source(source_with_dir, "module.py")
	assert not any("DALL100" in r[2] for r in results)


def test_dir_required_empty():
	# No public members, so __dir__ is not required
	source = """\nimport foo\n"""
	results = from_source(source, "module.py")
	assert not any("DALL100" in r[2] for r in results)


def test_dir_required_empty_init():
	# No public members, so __dir__ is not required in __init__.py either
	source = """\nimport foo\n"""
	results = from_source(source, "__init__.py")
	assert not any("DALL101" in r[2] for r in results)


def test_dir_required_init():
	source = """\nimport foo\n\nclass Foo: ...\n"""
	# No __dir__ defined, should yield DALL101
	results = from_source(source, "__init__.py")
	assert any("DALL101" in r[2] for r in results)


def test_dir_required_init_with_dir():
	# __dir__ defined, should not yield DALL101
	source_with_dir = """
	class Foo: ...

	def __dir__():
		return []
	"""
	results = from_source(source_with_dir, "__init__.py")
	assert not any("DALL101" in r[2] for r in results)


def test_dir_required_async_def_does_not_satisfy():
	# ``async def __dir__`` can't be used by ``dir(module)``, so DALL100 still applies
	source = """
	import foo

	class Foo: ...

	async def __dir__():
		return []
	"""
	results = from_source(source, "module.py")
	assert any("DALL100" in r[2] for r in results)


def test_dir_required_class_does_not_satisfy():
	# ``class __dir__`` can't be used by ``dir(module)``, so DALL100 still applies
	source = """
	import foo

	class Foo: ...

	class __dir__: ...
	"""
	results = from_source(source, "module.py")
	assert any("DALL100" in r[2] for r in results)
