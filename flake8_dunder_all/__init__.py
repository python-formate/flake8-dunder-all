#!/usr/bin/env python3
#
#  __init__.py
"""
A Flake8 plugin and pre-commit hook which checks to ensure modules have defined ``__all__``.
"""
#
#  Copyright (c) 2020-2022 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import sys
from typing import Any, Generator, List, Set, Tuple, Type, Union

# 3rd party
from consolekit.terminal_colours import Fore
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from domdf_python_tools.utils import stderr_writer

# this package
from flake8_dunder_all.utils import find_noqa, get_docstring_lineno, mark_text_ranges

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "MIT"
__version__: str = "0.3.1"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ("Visitor", "Plugin", "check_and_add_all", "DALL000")

DALL000 = "DALL000 Module lacks __all__."


class Visitor(ast.NodeVisitor):
	"""
	AST :class:`~ast.NodeVisitor` to check a module has defined ``__all__``, and add one if it not.

	:param use_endlineno: Flag to indicate whether the end_lineno functionality is available.
		This functionality is available on Python 3.8 and above, or when the tree has been passed through
		:func:`flake8_dunder_all.utils.mark_text_ranges``.
	"""

	found_all: bool  #: Flag to indicate a ``__all__`` declaration has been found in the AST.
	last_import: int  #: The lineno of the last top-level import
	members: Set[str]  #: List of functions and classed defined in the AST
	use_endlineno: bool

	def __init__(self, use_endlineno: bool = False) -> None:
		self.found_all = False
		self.members = set()
		self.last_import = 0
		self.use_endlineno = use_endlineno

	def visit_Name(self, node: ast.Name) -> None:
		"""
		Visit a variable.

		:param node: The node being visited.
		"""

		if node.id == "__all__":
			self.found_all = True
		else:
			self.generic_visit(node)

	def handle_def(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]) -> None:
		"""
		Handles ``def foo(): ...``, ``async def foo(): ...`` and ``class Foo: ...``.

		:param node: The node being visited.
		"""

		decorators = []

		NameNode, AttributeNode = ast.Name, ast.Attribute

		for deco in node.decorator_list:
			# pylint: disable =
			if isinstance(deco, NameNode):
				decorators.append(deco.id)
			elif isinstance(deco, AttributeNode):
				parts = [deco.attr]

				# last_part = deco.value
				#
				# while True:
				# 	if isinstance(last_part, ast.Attribute):
				# 		parts.append(last_part.attr)
				# 		last_part = last_part.value
				# 	elif isinstance(last_part, ast.Name):
				# 		parts.append(last_part.id)
				# 		break
				# 	else:
				# 		break

				decorators.append('.'.join(reversed(parts)))

		if not node.name.startswith('_') and "overload" not in decorators:
			self.members.add(node.name)

	def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
		"""
		Visit ``def foo(): ...``.

		:param node: The node being visited.
		"""

		# Don't generic visit
		self.handle_def(node)

	def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
		"""
		Visit ``async def foo(): ...``.

		:param node: The node being visited.
		"""

		# Don't generic visit
		self.handle_def(node)

	def visit_ClassDef(self, node: ast.ClassDef) -> None:
		"""
		Visit ``class Foo: ...``.

		:param node: The node being visited.
		"""

		# Don't generic visit
		self.handle_def(node)

	def handle_import(self, node: Union[ast.Import, ast.ImportFrom]) -> None:
		"""
		Handles ``import foo`` and ``from foo import bar``.

		:param node: The node being visited
		"""

		if self.use_endlineno:
			if not node.col_offset and node.end_lineno > self.last_import:  # type: ignore[union-attr]
				self.last_import = node.end_lineno  # type: ignore[union-attr]
		else:
			if not node.col_offset and node.lineno > self.last_import:
				self.last_import = node.lineno

	def visit_Import(self, node: ast.Import) -> None:
		"""
		Visit ``import foo``.

		:param node: The node being visited
		"""

		# Don't generic visit
		self.handle_import(node)

	def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
		"""
		Visit ``from foo import bar``.

		:param node: The node being visited
		"""

		# Don't generic visit
		self.handle_import(node)


class Plugin:
	"""
	A Flake8 plugin which checks to ensure modules have defined ``__all__``.

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
			yield 1, 0, DALL000, type(self)


def check_and_add_all(filename: PathLike, quote_type: str = '"', use_tuple: bool = False) -> int:
	"""
	Check the given filename for the presence of a ``__all__`` declaration, and add one if none is found.

	:param filename: The filename of the Python source file (``.py``) to check.
	:param quote_type: The type of quote to use for strings.
	:param use_tuple: Whether to use tuples instead of lists for ``__all__``.

	:returns:

	* ``0`` if the file already contains a ``__all__`` declaration,
	  has no function or class definitions, or has a ``  # noqa: DALL000  ` comment.
	* ``1`` If ``__all__`` is absent.
	* ``4`` if an error was encountered when parsing the file.

	.. versionchanged:: 0.2.0

		Now returns ``0`` and doesn't add ``__all__`` if the file contains a ``noqa: DALL000`` comment.

	.. versionchanged:: 0.3.0  Added the ``use_tuple`` argument.
	"""

	filename = PathPlus(filename)

	try:
		source = filename.read_text()
		for line in source.splitlines():
			noqas = find_noqa(line)
			if noqas is not None:
				if noqas["codes"]:
					# pylint: disable=loop-invariant-statement
					noqa_list: List[str] = noqas["codes"].rstrip().upper().split(',')
					if "DALL000" in noqa_list:
						return 0
					# pylint: enable=loop-invariant-statement

		tree = ast.parse(source)
		if sys.version_info < (3, 8):  # pragma: no cover (py38+)
			mark_text_ranges(tree, source)

	except SyntaxError:
		stderr_writer(Fore.RED(f"'{filename}' does not appear to be a valid Python source file."))
		return 4

	visitor = Visitor(use_endlineno=True)
	visitor.visit(tree)

	if visitor.found_all:
		return 0
	else:
		docstring_start = (get_docstring_lineno(tree) or 0) - 1
		docstring = ast.get_docstring(tree, clean=False) or ''
		docstring_end = len(docstring.split('\n')) + docstring_start

		insertion_position = max(docstring_end, visitor.last_import) + 1

		if not visitor.members:
			return 0

		members = f"{quote_type}, {quote_type}".join(sorted(visitor.members))

		lines = filename.read_text().split('\n')

		# Ensure there don't end up too many lines
		if lines[insertion_position].strip():
			lines.insert(insertion_position, '\n')
		else:
			lines.insert(insertion_position, '')

		if use_tuple:
			lines.insert(insertion_position, f"__all__ = ({quote_type}{members}{quote_type}, )")
		else:
			lines.insert(insertion_position, f"__all__ = [{quote_type}{members}{quote_type}]")

		filename.write_clean('\n'.join(lines))

		return 1
