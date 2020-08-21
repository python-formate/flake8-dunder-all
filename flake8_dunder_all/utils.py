#!/usr/bin/env python3
#
#  utils.py
"""
General utility functions.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
#  get_docstring_lineno based on the "ast" module from CPython
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
#

# stdlib
import ast
import re
from textwrap import dedent, indent
from typing import Optional

__all__ = ["get_docstring_lineno", "tidy_docstring"]


def get_docstring_lineno(node: ast.AST) -> Optional[int]:
	"""
	Returns the linenumber of the start of the docstring for ``node``.

	:param node:
	"""

	if not (node.body and isinstance(node.body[0], ast.Expr)):
		return None

	node = node.body[0].value

	if isinstance(node, ast.Str):
		return node.lineno
	elif isinstance(node, ast.Constant) and isinstance(node.value, str):
		return node.lineno  # pragma: no cover
	else:
		return None


def tidy_docstring(docstring: Optional[str]) -> str:
	"""
	Tidy up the docstring for use as help text.
	"""

	if docstring is None:
		return ''

	docstring = dedent(docstring).strip()
	docstring = re.sub(r"``(\d+)``", r"\1", docstring)
	docstring = re.sub(r"\t", "  ", docstring)
	docstring = re.sub("``([^`]*)``", r"'\1'", docstring)

	return f"\n{docstring}"
