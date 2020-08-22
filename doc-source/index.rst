##################
flake8-dunder-all
##################

.. start short_desc

**A Flake8 plugin and pre-commit hook which checks to ensure modules have defined '__all__'.**

.. end short_desc

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/flake8-dunder-all/latest?logo=read-the-docs
	:target: https://flake8-dunder-all.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

.. |docs_check| image:: https://github.com/domdfcoding/flake8-dunder-all/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/flake8-dunder-all/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/flake8-dunder-all/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/flake8-dunder-all
	:alt: Travis Build Status

.. |actions_windows| image:: https://github.com/domdfcoding/flake8-dunder-all/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/flake8-dunder-all/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Tests Status

.. |actions_macos| image:: https://github.com/domdfcoding/flake8-dunder-all/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/flake8-dunder-all/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Tests Status

.. |requires| image:: https://requires.io/github/domdfcoding/flake8-dunder-all/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/flake8-dunder-all/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/flake8-dunder-all/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/flake8-dunder-all?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/flake8-dunder-all?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/flake8-dunder-all
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/flake8-dunder-all
	:target: https://pypi.org/project/flake8-dunder-all/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/flake8-dunder-all?logo=python&logoColor=white
	:target: https://pypi.org/project/flake8-dunder-all/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/flake8-dunder-all
	:target: https://pypi.org/project/flake8-dunder-all/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/flake8-dunder-all
	:target: https://pypi.org/project/flake8-dunder-all/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/flake8-dunder-all?logo=anaconda
	:target: https://anaconda.org/domdfcoding/flake8-dunder-all
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/flake8-dunder-all?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/flake8-dunder-all
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/domdfcoding/flake8-dunder-all
	:target: https://github.com/domdfcoding/flake8-dunder-all/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/flake8-dunder-all
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/flake8-dunder-all/v0.0.4
	:target: https://github.com/domdfcoding/flake8-dunder-all/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/flake8-dunder-all
	:target: https://github.com/domdfcoding/flake8-dunder-all/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. end shields

Installation
---------------

.. start installation

.. tabs::

	.. tab:: from PyPI

		.. prompt:: bash

			python3 -m pip install flake8-dunder-all --user

	.. tab:: from Anaconda

		First add the required channels

		.. prompt:: bash

			conda config --add channels http://conda.anaconda.org/domdfcoding
			conda config --add channels http://conda.anaconda.org/conda-forge

		Then install

		.. prompt:: bash

			conda install flake8-dunder-all

	.. tab:: from GitHub

		.. prompt:: bash

			python3 -m pip install git+https://github.com/domdfcoding/flake8-dunder-all@master --user

.. end installation


Usage
--------

This library provides the Flake8 plugin ``flake8-dunder-all`` as well as the ``ensure-dunder-all``,script which adds ``__all__`` to files that require it.


Using the Flake8 plugin as a pre-commit hook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will only check for missing ``__all__`` variables but won't add them.

See `pre-commit <https://github.com/pre-commit/pre-commit>`_ for instructions

Sample `.pre-commit-config.yaml`:

.. code-block:: yaml

	 - repo: https://gitlab.com/pycqa/flake8
	   rev: 3.8.1
	   hooks:
	    - id: flake8
	      additional_dependencies: [flake8-dunder-all==0.0.4]


Using the script as a pre-commit hook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will add ``__all__`` variables to files that require them and prevent the commit if any changes were made.

See `pre-commit <https://github.com/pre-commit/pre-commit>`_ for instructions

Sample `.pre-commit-config.yaml`:

.. code-block:: yaml

	 - repo: https://github.com/domdfcoding/flake8-dunder-all
	   rev: v0.0.4
	   hooks:
	    - id: ensure-dunder-all


.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3
	:caption: Documentation

	plugin
	script
	API Reference<docs>
	contributing
	Source

.. start links

View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

`Browse the GitHub Repository <https://github.com/domdfcoding/flake8-dunder-all>`__

.. end links
