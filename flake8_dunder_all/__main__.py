#!/usr/bin/env python3
#
#  __main__.py
"""
Command-line entry point for flake8-dunder-all.
"""
#
#  Copyright (c) 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import sys
from typing import Iterable

# 3rd party
import click
from consolekit import click_command
from consolekit.commands import MarkdownHelpCommand
from consolekit.options import auto_default_option, flag_option

# this package
from flake8_dunder_all import check_and_add_all

__all__ = ("main", )


@click.argument("filenames", type=click.STRING, nargs=-1, metavar="FILENAME")
@auto_default_option("--quote-type", type=click.STRING, help="The type of quote to use.", show_default=True)
@flag_option("--use-tuple", help="Use tuples instead of lists for __all__.", default=False)
@click_command(cls=MarkdownHelpCommand)
def main(filenames: Iterable[str], quote_type: str = '"', use_tuple: bool = False) -> None:
	"""
	Given a list of Python source files, check each file defines ``__all__``.

	Exit codes:

	* 0: The file already contains a ``__all__`` declaration or has no function or class definitions.
	* 1: A ``__all__`` declaration was added to the file.
	* 4: A file could not be parsed due to a syntax error.
	* 5: Bitwise OR of 1 and 4.
	"""

	retv = 0

	for filename in filenames:
		filename = filename.strip()
		click.echo(f"Checking {filename}")
		retv |= check_and_add_all(filename=filename, quote_type=quote_type, use_tuple=use_tuple)

	sys.exit(retv)


if __name__ == "__main__":
	sys.exit(main())
