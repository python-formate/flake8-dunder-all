"""a docstring"""
# stdlib
import ast
import pathlib

# this package
from flake8_dunder_all import Plugin, check_and_add_all

print(list(Plugin(ast.parse(pathlib.Path("flake8_dunder_all/__init__.py").read_text())).run()))

print(check_and_add_all(pathlib.Path("flake8_dunder_all/__init__.py")))
print(check_and_add_all(__file__))
print(check_and_add_all("/home/domdf/Python/01 GitHub Repos/flake8-dunder-all/.pre-commit-config.yaml"))
