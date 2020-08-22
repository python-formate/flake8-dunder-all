#!/usr/bin/env python3
#
#  __main__.py
"""
Command-line entry point for flake8-dunder-all.
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

# stdlib
import argparse
import sys
from typing import Optional, Sequence

# this package
from flake8_dunder_all import check_and_add_all
from flake8_dunder_all.utils import tidy_docstring

__all__ = ["main"]


def main(argv: Optional[Sequence[str]] = None) -> int:
	"""
	Given a list of Python source files, check each file defines ``__all__``.

	Exit codes:

		``0``: The file already contains a ``__all__`` variable or has no function or class definitions
		``1``: A ``__all__`` variable. was added to the file.
		``4``: A file could not be parsed due to a syntax error.
		``5``: Bitwise OR of ``1`` and ``4``.

	"""
	parser = argparse.ArgumentParser(
			description=tidy_docstring(main.__doc__),
			formatter_class=argparse.RawTextHelpFormatter,
			)
	parser.add_argument('filenames', type=str, nargs='*', help="The filename(s) to lint.", metavar="FILENAME")
	parser.add_argument(
			'--quote-type', type=str, default='"', help="The type of quote to use. (default: %(default)s)"
			)
	args = parser.parse_args(argv)

	retv = 0

	for filename in args.filenames:
		filename = filename.strip()
		print(f"Checking {filename}")
		retv |= check_and_add_all(filename=filename, quote_type=args.quote_type)

	return retv


if __name__ == "__main__":
	sys.exit(main())
