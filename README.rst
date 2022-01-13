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
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy| |pre_commit_ci|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/flake8-dunder-all/latest?logo=read-the-docs
	:target: https://flake8-dunder-all.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/flake8-dunder-all/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/flake8-dunder-all/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/flake8-dunder-all/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/flake8-dunder-all/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/flake8-dunder-all/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/flake8-dunder-all/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/flake8-dunder-all/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/flake8-dunder-all/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/flake8-dunder-all/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/flake8-dunder-all/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/flake8-dunder-all/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/flake8-dunder-all/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

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

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/flake8-dunder-all/v0.1.7
	:target: https://github.com/domdfcoding/flake8-dunder-all/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/flake8-dunder-all
	:target: https://github.com/domdfcoding/flake8-dunder-all/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2022
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/flake8-dunder-all
	:target: https://pypi.org/project/flake8-dunder-all/
	:alt: PyPI - Downloads

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/flake8-dunder-all/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/flake8-dunder-all/master
	:alt: pre-commit.ci status

.. end shields

|

Installation
--------------

.. start installation

``flake8-dunder-all`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install flake8-dunder-all

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels http://conda.anaconda.org/conda-forge
		$ conda config --add channels http://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install flake8-dunder-all

.. end installation

Flake8 codes
--------------

============== ====================================
Code           Description
============== ====================================
DALL000        Module lacks __all__.
============== ====================================


Use as a pre-commit hook
--------------------------

See `pre-commit <https://github.com/pre-commit/pre-commit>`_ for instructions

Sample ``.pre-commit-config.yaml``:

.. code-block:: yaml

	 - repo: https://gitlab.com/pycqa/flake8
	   rev: 3.8.1
	   hooks:
	    - id: flake8
	      additional_dependencies: [flake8-dunder-all==0.1.7]

``ensure-dunder-all`` script

There is also a script which will automatically add __all__ for files which don't have it.

See `the documentation <https://flake8-dunder-all.readthedocs.io/en/latest/usage.html#ensure-dunder-all-script>`_
for details.
