#!/usr/bin/env python3
#
#  __init__.py
"""
A Flake8 plugin and pre-commit hook which checks to ensure modules have defined ``__all__``.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on flake8_2020
#  Copyright (c) 2019 Anthony Sottile
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#

# stdlib
import ast
from typing import Any, Generator, List, Tuple, Type

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.terminal_colours import Fore
from domdf_python_tools.utils import stderr_writer

# this package
from flake8_dunder_all.utils import get_docstring_lineno

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "MIT"
__version__: str = "0.0.1"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["Visitor", "Plugin", "check_and_add_all", "DALL000"]

DALL000 = "DALL000 Module lacks __all__."  # noqa: E501


class Visitor(ast.NodeVisitor):
	"""
	AST :class:`~ast.NodeVisitor` to check a module has defined ``__all__``, and add one if it not.
	"""

	def __init__(self) -> None:
		self.found_all = False

		# List of functions and classed defined in this module
		self.members: List[str] = []

		# Lineno of last top-level import
		self.last_import = 0

	def visit_Name(self, node: ast.Name):
		"""
		Visit a variable.

		:param node: The node being visited.
		"""

		if node.id == "__all__":
			self.found_all = True
		else:
			self.generic_visit(node)

	def visit_FunctionDef(self, node: ast.FunctionDef):
		"""
		Visit ``def foo(): ...``.

		:param node: The node being visited.
		"""

		# Don't generic visit
		if not node.name.startswith("_"):
			self.members.append(node.name)

	def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
		"""
		Visit ``async def foo(): ...``.

		:param node: The node being visited.
		"""

		# Don't generic visit
		if not node.name.startswith("_"):
			self.members.append(node.name)

	def visit_ClassDef(self, node: ast.ClassDef):
		"""
		Visit ``class Foo: ...``.

		:param node: The node being visited.
		"""

		# Don't generic visit
		if not node.name.startswith("_"):
			self.members.append(node.name)

	def visit_Import(self, node: ast.Import):
		"""
		Visit ``import foo``.

		:param node: The node being visited
		"""

		# Don't generic visit
		if not node.col_offset and node.lineno > self.last_import:
			self.last_import = node.lineno

	def visit_ImportFrom(self, node: ast.ImportFrom):
		"""
		Visit ``from foo import bar``.

		:param node: The node being visited
		"""

		# Don't generic visit
		if not node.col_offset and node.lineno > self.last_import:
			self.last_import = node.lineno


class Plugin:
	"""
	A Flake8 plugin which checks to ensure modules have defined '__all__'.

	:param tree: The abstract syntax tree (AST) to check.
	"""

	name: str = __name__
	version: str = __version__  #: The plugin version

	def __init__(self, tree: ast.AST):
		self._tree = tree

	def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
		"""
		Run the plugin.

		Yields four-element tuples, consisting of:

		#. The line number of the error.
		#. The column offset of the error.
		#. The error message.
		#. The class of the plugin raising the error.
		"""

		visitor = Visitor()
		visitor.visit(self._tree)

		if visitor.found_all:
			return
		elif not visitor.members:
			return
		else:
			yield 0, 0, DALL000, type(self)


def check_and_add_all(filename: PathPlus, quote_type: str = '"') -> int:
	"""
	Check the given filename for the presence of a ``__all__`` variable, and add one if none is found.

	:param filename: The filename of the Python source file (``.py``) to check.
	:param quote_type: The type of quote to use for strings.

	:returns: ``0`` if the file already contains a ``__all__`` variable or has no function or class definitions;
		``1`` otherwise. ``4`` indicates an error parsing the file.
	"""

	quotes = {"'", '"'}
	quotes.remove(quote_type)
	bad_quote, *_ = tuple(quotes)

	filename = PathPlus(filename)

	try:
		tree = ast.parse(filename.read_text())
	except SyntaxError:
		stderr_writer(Fore.RED(f"'{filename}' does not appear to be a valid Python source file."))
		return 4

	visitor = Visitor()
	visitor.visit(tree)

	if visitor.found_all:
		return 0
	else:
		docstring_start = (get_docstring_lineno(tree) or 0) - 1
		docstring = ast.get_docstring(tree, clean=False) or ''
		docstring_end = len(docstring.split("\n")) + docstring_start

		insertion_position = max(docstring_end, visitor.last_import) + 1

		if not visitor.members:
			return 0

		members = repr(visitor.members).replace(bad_quote, quote_type)

		lines = filename.read_text().split("\n")

		# Ensure there don't end up too many lines
		if lines[insertion_position].strip():
			lines.insert(insertion_position, "\n")
		else:
			lines.insert(insertion_position, "")

		lines.insert(insertion_position, f"__all__ = {members}")

		filename.write_clean("\n".join(lines))

		return 1
