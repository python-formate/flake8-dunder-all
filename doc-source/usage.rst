========
Usage
========

This library provides the Flake8 plugin ``flake8-dunder-all`` as well as the
``ensure-dunder-all`` script which adds ``__all__`` to files that require it.


Flake8 codes
--------------

.. flake8-codes:: flake8_dunder_all

	DALL000
	DALL001
	DALL002


For the ``DALL001`` option there exists a configuration option (``dunder-all-alphabetical``)
which controls the alphabetical grouping expected of ``__all__``.
The options are:

* ``ignore`` -- ``__all__`` should be sorted alphabetically ignoring case, e.g. ``['bar', 'Baz', 'foo']``
* ``lower`` -- group lowercase names first, then uppercase names, e.g. ``['bar', 'foo', 'Baz']``
* ``upper`` -- group uppercase names first, then uppercase names, e.g. ``['Baz', 'Foo', 'bar']``

If the ``dunder-all-alphabetical`` option is omitted the ``DALL001`` check is disabled.

.. versionchanged:: 0.5.0  Added the ``DALL001`` and ``DALL002`` checks.

.. note::

	In version ``0.5.0`` the entry point changed from ``DALL`` to ``DAL``, due to changes in flake8 itself.
	However, the codes remain ``DALLXXX`` and should continue to work as normal.


``ensure-dunder-all`` script
--------------------------------

.. click:: flake8_dunder_all.__main__:main
	:prog: ensure-dunder-all
	:nested: none


pre-commit hooks
-------------------


Using the Flake8 plugin as a pre-commit hook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will only check for missing ``__all__`` declarations but won't add them.

See `pre-commit <https://github.com/pre-commit/pre-commit>`_ for instructions

Sample ``.pre-commit-config.yaml``:

.. pre-commit:flake8:: 0.5.0


Using the script as a pre-commit hook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will add ``__all__`` to files that require them and prevent the commit if any changes were made.

See `pre-commit <https://github.com/pre-commit/pre-commit>`_ for instructions.

Sample ``.pre-commit-config.yaml``:

.. pre-commit::
	:rev: v0.5.0
