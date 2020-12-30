========
Usage
========

This library provides the Flake8 plugin ``flake8-dunder-all`` as well as the
``ensure-dunder-all`` script which adds ``__all__`` to files that require it.


Flake8 codes
--------------

.. flake8-codes:: flake8_dunder_all

	DALL000


``ensure-dunder-all`` script
--------------------------------

Command line script usage:

.. code-block:: bash

	ensure-dunder-all [-h] [--quote-type QUOTE_TYPE] [FILENAME [FILENAME ...]]


Given a list of Python source files, check each file defines ``__all__``.

Exit codes
^^^^^^^^^^^^^^

	| ``0``: The file already contains a ``__all__`` declaration or has no function or class definitions
	| ``1``: A ``__all__`` declaration. was added to the file.
	| ``4``: A file could not be parsed due to a syntax error.
	| ``5``: Bitwise OR of ``1`` and ``4``.


Positional arguments
^^^^^^^^^^^^^^^^^^^^^^^^^

.. confval:: FILENAME

	The filename(s) to lint.

optional arguments
^^^^^^^^^^^^^^^^^^^^^^^

.. confval:: -h, --help

	Show the help message and exit

.. confval:: --quote-type QUOTE_TYPE

	The type of quote to use. Default ``"``


pre-commit hooks
-------------------


Using the Flake8 plugin as a pre-commit hook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will only check for missing ``__all__`` declarations but won't add them.

See `pre-commit <https://github.com/pre-commit/pre-commit>`_ for instructions

Sample ``.pre-commit-config.yaml``:

.. pre-commit:flake8:: 0.1.3


Using the script as a pre-commit hook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will add ``__all__`` to files that require them and prevent the commit if any changes were made.

See `pre-commit <https://github.com/pre-commit/pre-commit>`_ for instructions

Sample ``.pre-commit-config.yaml``:

.. pre-commit::
	:rev: v0.1.3
