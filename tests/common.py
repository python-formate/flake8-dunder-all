# stdlib
import ast
from typing import Set

# this package
from flake8_dunder_all import Plugin


def results(s: str) -> Set[str]:
	return {"{}:{}: {}".format(*r) for r in Plugin(ast.parse(s)).run()}


testing_source_a = '''
"""a docstring"""
import foo
'''

testing_source_b = '''
"""a docstring"""
import foo

def a_function(): ...
'''

testing_source_c = '''
"""a docstring"""
import foo

class Foo: ...
'''

testing_source_d = '''
"""a docstring"""
import foo

class Foo: ...

def a_function(): ...
'''

testing_source_e = '''
"""a docstring"""
import foo

__all__ = ["Foo", "a_function"]

class Foo: ...

def a_function(): ...
'''

# tests visit_Name fully
testing_source_f = '''
"""a docstring"""
import foo


__version__: str = "1.2.3"
__all__ = ["Foo", "a_function"]

class Foo: ...

def a_function(): ...
'''

testing_source_g = '''
"""a docstring"""
import foo

async def a_function(): ...
'''

testing_source_h = "from foo import bar"

testing_source_i = '''
"""a docstring"""
import foo




async def a_function(): ...
'''

testing_source_j = """
from tests.common import (
		mangled_source,
		results,
		testing_source_a,
		testing_source_b,
		testing_source_c,
		testing_source_d,
		testing_source_e,
		testing_source_f,
		testing_source_g,
		testing_source_h,
		testing_source_i
		)


async def a_function(): ...
"""

testing_source_k = '''
"""a docstring"""

@overload
def a_function(): ...
'''

testing_source_l = '''
"""a docstring"""

@typing.overload
def a_function(): ...
'''

mangled_source = '''
"""a docstring
import foo

asyn def a_function): ...
'''
