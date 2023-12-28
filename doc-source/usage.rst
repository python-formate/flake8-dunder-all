========
Usage
========

This library provides the Flake8 plugin ``flake8-dunder-all`` as well as the
``ensure-dunder-all`` script which adds ``__all__`` to files that require it.


Flake8 codes
--------------

.. flake8-codes:: flake8_dunder_all

	DAL000

.. note::

	In version ``0.3.1`` the entry point changed from ``DALL`` to ``DAL``, due to changes in flake8 itself.
	Furthermore, in version ``0.4.0`` the codes also changed from ``DALLXXX`` to ``DALXXX`` and need to be updated.


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

.. pre-commit:flake8:: 0.3.1


Using the script as a pre-commit hook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will add ``__all__`` to files that require them and prevent the commit if any changes were made.

See `pre-commit <https://github.com/pre-commit/pre-commit>`_ for instructions.

Sample ``.pre-commit-config.yaml``:

.. pre-commit::
	:rev: v0.3.1
