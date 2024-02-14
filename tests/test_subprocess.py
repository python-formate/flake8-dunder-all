# stdlib
import os
import subprocess
import sys

# 3rd party
from domdf_python_tools.paths import PathPlus, in_directory


def test_subprocess(tmp_pathplus: PathPlus, monkeypatch):
	monkeypatch.delenv("COV_CORE_SOURCE", raising=False)
	monkeypatch.delenv("COV_CORE_CONFIG", raising=False)
	monkeypatch.delenv("COV_CORE_DATAFILE", raising=False)
	monkeypatch.setenv("PYTHONWARNINGS", "ignore")

	(tmp_pathplus / "code.py").write_text("\n\t\ndef foo():\n\tpass\n\t")

	with in_directory(tmp_pathplus):
		result = subprocess.run(
				[sys.executable, "-m", "flake8", "code.py"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				)

	assert result.returncode == 1
	assert result.stderr == b''
	assert result.stdout == b"""\
code.py:1:1: DAL000 Module lacks __all__.
code.py:2:1: W191 indentation contains tabs
code.py:2:1: W293 blank line contains whitespace
code.py:4:1: W191 indentation contains tabs
code.py:5:1: W191 indentation contains tabs
code.py:5:1: W293 blank line contains whitespace
code.py:5:2: W292 no newline at end of file
"""

	with in_directory(tmp_pathplus):
		result = subprocess.run(
				[sys.executable, "-m", "flake8", "code.py", "--select", "DAL000"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				)

	assert result.returncode == 1
	assert result.stderr == b''
	assert result.stdout == b"code.py:1:1: DAL000 Module lacks __all__.\n"

	(tmp_pathplus / "tox.ini").write_text("""

[flake8]
select = DAL000
	""")

	with in_directory(tmp_pathplus):
		result = subprocess.run(
				[sys.executable, "-m", "flake8", "code.py"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				)

	assert result.returncode == 1
	assert result.stderr == b''
	assert result.stdout == b"code.py:1:1: DAL000 Module lacks __all__.\n"

	tox_ini = tmp_pathplus / "tox.ini"
	tox_ini.write_text("""

[flake8]
select = DAL000
per-file-ignores =
    code.py: DAL000
	""")

	with in_directory(tmp_pathplus):
		result = subprocess.run(
				[sys.executable, "-m", "flake8", "code.py"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				)

	assert result.returncode == 0
	assert result.stderr == b''
	assert result.stdout == b''


def test_subprocess_noqa(tmp_pathplus: PathPlus, monkeypatch):
	monkeypatch.delenv("COV_CORE_SOURCE", raising=False)
	monkeypatch.delenv("COV_CORE_CONFIG", raising=False)
	monkeypatch.delenv("COV_CORE_DATAFILE", raising=False)
	monkeypatch.setenv("PYTHONWARNINGS", "ignore")

	(tmp_pathplus / "code.py").write_text("# noq" + "a: DAL000\n\n\t\ndef foo():\n\tpass\n\t")

	with in_directory(tmp_pathplus):
		result = subprocess.run(
				[sys.executable, "-m", "flake8", "code.py"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				)

	assert result.returncode == 1
	assert result.stderr == b''
	assert result.stdout == b"""\
code.py:3:1: W191 indentation contains tabs
code.py:3:1: W293 blank line contains whitespace
code.py:5:1: W191 indentation contains tabs
code.py:6:1: W191 indentation contains tabs
code.py:6:1: W293 blank line contains whitespace
code.py:6:2: W292 no newline at end of file
"""

	with in_directory(tmp_pathplus):
		result = subprocess.run(
				[sys.executable, "-m", "flake8", "code.py", "--select", "DAL000"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				)

	assert result.returncode == 0
	assert result.stderr == b''
	assert result.stdout == b''

	(tmp_pathplus / "tox.ini").write_text("""

[flake8]
select = DAL000
	""")

	with in_directory(tmp_pathplus):
		result = subprocess.run(
				[sys.executable, "-m", "flake8", "code.py"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				)

	assert result.returncode == 0
	assert result.stderr == b''
	assert result.stdout == b''

	tox_ini = tmp_pathplus / "tox.ini"
	tox_ini.write_text("""

[flake8]
select = DAL000
per-file-ignores =
    code.py: DAL000
	""")

	with in_directory(tmp_pathplus):
		result = subprocess.run(
				[sys.executable, "-m", "flake8", "code.py"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				)

	assert result.returncode == 0
	assert result.stderr == b''
	assert result.stdout == b''
