===================
ensure-dunder-all
===================

Command line script usage:

.. code-block:: bash

	ensure-dunder-all [-h] [--quote-type QUOTE_TYPE] [FILENAME [FILENAME ...]]


Given a list of Python source files, check each file defines ``__all__``.

Exit codes
-------------

	| ``0``: The file already contains a ``__all__`` variable or has no function or class definitions
	| ``1``: A ``__all__`` variable. was added to the file.
	| ``4``: A file could not be parsed due to a syntax error.
	| ``5``: Bitwise OR of ``1`` and ``4``.


Positional arguments
----------------------

.. confval:: FILENAME

	The filename(s) to lint.

optional arguments
----------------------

.. confval:: -h, --help

	Show the help message and exit

.. confval:: --quote-type QUOTE_TYPE

	The type of quote to use. Default ``"``
