# stdlib
import ast

# this package
from flake8_dunder_all.utils import get_docstring_lineno, tidy_docstring


def test_get_docstring_lineno():
	assert get_docstring_lineno(ast.parse('"""a docstring"""')) == 1
	assert get_docstring_lineno(ast.parse('\n"""a docstring"""')) == 2
	assert get_docstring_lineno(ast.parse('\n\n"""a docstring"""')) == 3
	assert get_docstring_lineno(ast.parse('\n\n\n"""a docstring"""')) == 4
	assert get_docstring_lineno(ast.parse('\n\n\n\n"""a docstring"""')) == 5

	assert get_docstring_lineno(ast.parse('')) is None
	assert get_docstring_lineno(ast.parse('print("Hello World")')) is None


def test_tidy_docstring():
	assert tidy_docstring("""

""") == '\n'

	assert tidy_docstring("""

	""") == '\n'

	assert tidy_docstring("""	hello
	world
""") == '\nhello\nworld'

	for i in range(100):
		assert tidy_docstring(f"``{i}``") == f'\n{i}'

	for word in "the quick brown fox jumps over the lazy dog".split(' '):
		assert tidy_docstring(f"``{word}``") == f"\n'{word}'"

		assert tidy_docstring("""	hello
					world
	""") == '\nhello\n        world'

	assert tidy_docstring(None) == ''
