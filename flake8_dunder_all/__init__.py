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
from enum import Enum
from typing import Any, Generator, Optional, Sequence, Set, Tuple, Type, Union, cast

# 3rd party
import natsort
from consolekit.terminal_colours import Fore
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from domdf_python_tools.utils import stderr_writer
from flake8.options.manager import OptionManager  # type: ignore
from flake8.style_guide import find_noqa  # type: ignore

# this package
from flake8_dunder_all.utils import get_docstring_lineno, mark_text_ranges

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "MIT"
__version__: str = "0.1.8"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = [
		"check_and_add_all",
		"AlphabeticalOptions",
		"DALL000",
		"DALL001",
		"DALL002",
		"Plugin",
		"Visitor",
		]

DALL000 = "DALL000 Module lacks __all__"
DALL001 = "DALL001 __all__ not sorted alphabetically"
DALL002 = "DALL002 __all__ not a list of strings"


class AlphabeticalOptions(Enum):
	"""
	Enum of possible values for the ``--dunder-all-alphabetical`` option.

	.. versionadded:: 0.2.0
	"""

	UPPER = "upper"
	LOWER = "lower"
	IGNORE = "ignore"
	NONE = "none"


class Visitor(ast.NodeVisitor):
	"""
	AST :class:`~ast.NodeVisitor` to check a module has defined ``__all__``, and add one if it not.

	:param use_endlineno: Flag to indicate whether the end_lineno functionality is available.
		This functionality is available on Python 3.8 and above, or when the tree has been passed through
		:func:`flake8_dunder_all.utils.mark_text_ranges``.

	.. versionchanged:: 0.2.0

		Added the ``sorted_upper_first``, ``sorted_lower_first`` and ``all_lineno`` attributes.
	"""

	found_all: bool  #: Flag to indicate a ``__all__`` declaration has been found in the AST.
	last_import: int  #: The lineno of the last top-level import
	members: Set[str]  #: List of functions and classed defined in the AST
	use_endlineno: bool
	all_members: Optional[Sequence[str]]  #: The value of ``__all__``.
	all_lineno: int  #: The line number where ``__all__`` is defined.

	def __init__(self, use_endlineno: bool = False) -> None:
		self.found_all = False
		self.members = set()
		self.last_import = 0
		self.use_endlineno = use_endlineno
		self.all_members = None
		self.all_lineno = -1

	def visit_Assign(self, node: ast.Assign) -> None:  # noqa: D102
		targets = []
		for t in node.targets:
			if isinstance(t, ast.Name):
				targets.append(t.id)

		if "__all__" in targets:
			self.found_all = True
			self.all_lineno = node.lineno
			self.all_members = self._parse_all(cast(ast.List, node.value))

	def visit_AnnAssign(self, node: ast.AnnAssign) -> None:  # noqa: D102
		if isinstance(node.target, ast.Name):
			if node.target.id == "__all__":
				self.all_lineno = node.lineno
				self.found_all = True
				self.all_members = self._parse_all(cast(ast.List, node.value))

	@staticmethod
	def _parse_all(all_node: ast.List) -> Optional[Sequence[str]]:
		try:
			all_ = ast.literal_eval(all_node)
		except ValueError:
			return None

		if not isinstance(all_, Sequence):
			return None

		return all_

	def handle_def(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]):
		"""
		Handles ``def foo(): ...``, ``async def foo(): ...`` and ``class Foo: ...``.

		:param node: The node being visited.
		"""

		decorators = []

		for deco in node.decorator_list:
			if isinstance(deco, ast.Name):
				decorators.append(deco.id)
			elif isinstance(deco, ast.Attribute):
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

	def visit_FunctionDef(self, node: ast.FunctionDef):
		"""
		Visit ``def foo(): ...``.

		:param node: The node being visited.
		"""

		# Don't generic visit
		self.handle_def(node)

	def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
		"""
		Visit ``async def foo(): ...``.

		:param node: The node being visited.
		"""

		# Don't generic visit
		self.handle_def(node)

	def visit_ClassDef(self, node: ast.ClassDef):
		"""
		Visit ``class Foo: ...``.

		:param node: The node being visited.
		"""

		# Don't generic visit
		self.handle_def(node)

	def handle_import(self, node: Union[ast.Import, ast.ImportFrom]):
		"""
		Handles ``import foo`` and ``from foo import bar``.

		:param node: The node being visited
		"""

		if self.use_endlineno:
			if not node.col_offset and node.end_lineno > self.last_import:  # type: ignore
				self.last_import = node.end_lineno  # type: ignore
		else:
			if not node.col_offset and node.lineno > self.last_import:
				self.last_import = node.lineno

	def visit_Import(self, node: ast.Import):
		"""
		Visit ``import foo``.

		:param node: The node being visited
		"""

		# Don't generic visit
		self.handle_import(node)

	def visit_ImportFrom(self, node: ast.ImportFrom):
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
	dunder_all_alphabetical: AlphabeticalOptions = AlphabeticalOptions.NONE

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
			if visitor.all_members is None:
				yield visitor.all_lineno, 0, DALL002, type(self)

			elif self.dunder_all_alphabetical == AlphabeticalOptions.IGNORE:
				# Alphabetical, upper or lower don't matter
				sorted_alphabetical = natsort.natsorted(visitor.all_members, key=str.lower)
				if visitor.all_members != sorted_alphabetical:
					yield visitor.all_lineno, 0, f"{DALL001}", type(self)
			elif self.dunder_all_alphabetical == AlphabeticalOptions.UPPER:
				# Alphabetical, uppercase grouped first
				sorted_alphabetical = natsort.natsorted(visitor.all_members)
				if visitor.all_members != sorted_alphabetical:
					yield visitor.all_lineno, 0, f"{DALL001} (uppercase first)", type(self)
			elif self.dunder_all_alphabetical == AlphabeticalOptions.LOWER:
				# Alphabetical, lowercase grouped first
				sorted_alphabetical = natsort.natsorted(visitor.all_members, alg=natsort.ns.LOWERCASEFIRST)
				if visitor.all_members != sorted_alphabetical:
					yield visitor.all_lineno, 0, f"{DALL001} (lowercase first)", type(self)

		elif not visitor.members:
			return

		else:
			yield 1, 0, DALL000, type(self)

	@classmethod
	def add_options(cls, option_manager: OptionManager) -> None:  # noqa: D102  # pragma: no cover

		option_manager.add_option(
				"--dunder-all-alphabetical",
				choices=[member.value for member in AlphabeticalOptions],
				parse_from_config=True,
				default=AlphabeticalOptions.NONE.value,
				help=(
						"Require entries in '__all__' to be alphabetical ([upper] or [lower]case first)."
						"(Default: %(default)s)"
						),
				)

	@classmethod
	def parse_options(cls, options):  # noqa: D102  # pragma: no cover
		# note: this sets the option on the class and not the instance
		cls.dunder_all_alphabetical = AlphabeticalOptions(options.dunder_all_alphabetical)


def check_and_add_all(filename: PathLike, quote_type: str = '"') -> int:
	"""
	Check the given filename for the presence of a ``__all__`` declaration, and add one if none is found.

	:param filename: The filename of the Python source file (``.py``) to check.
	:param quote_type: The type of quote to use for strings.

	:returns:

	* ``0`` if the file already contains a ``__all__`` declaration,
	  has no function or class definitions, or has a ``  # noqa: DALL000  ` comment.
	* ``1`` If ``__all__`` is absent.
	* ``4`` if an error was encountered when parsing the file.

	.. versionchanged:: 0.2.0

		Now returns ``0`` and doesn't add ``__all__`` if the file contains a ``# noqa: DALL000`` comment.
	"""

	quotes = {"'", '"'}
	quotes.remove(quote_type)
	bad_quote, *_ = tuple(quotes)

	filename = PathPlus(filename)

	try:
		source = filename.read_text()
		for line in source.splitlines():
			noqas = find_noqa(line)
			if noqas is not None:
				if "DALL000" in noqas.group(1).rstrip().upper().split(','):
					return 0

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

		members = repr(sorted(visitor.members)).replace(bad_quote, quote_type)

		lines = filename.read_text().split('\n')

		# Ensure there don't end up too many lines
		if lines[insertion_position].strip():
			lines.insert(insertion_position, '\n')
		else:
			lines.insert(insertion_position, '')

		lines.insert(insertion_position, f"__all__ = {members}")

		filename.write_clean('\n'.join(lines))

		return 1
