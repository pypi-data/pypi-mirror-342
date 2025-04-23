from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from easyignore.main import app

runner = CliRunner()


@pytest.fixture()
def directory() -> Path:
    return Path(__file__).parent.resolve()


@pytest.fixture()
def example_gitignore() -> str:
    path = Path("testdata/.gitignore")
    return path.read_text()


def test_app() -> None:
    result = runner.invoke(app, ["python", "-o"])
    assert result.exit_code == 0
    assert Path(".gitignore").exists()


def test_multiple_args() -> None:
    result = runner.invoke(app, ["python", "node", "-o"])
    assert result.exit_code == 0
    assert Path(".gitignore").exists()
    result = runner.invoke(app, ["python", "node", "react", "-o"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "c++", "rust", "csharp", "-o"])
    assert result.exit_code == 0


def test_invalid_args() -> None:
    result = runner.invoke(app, ["python", "node", "invalidlang"])
    assert result.exit_code == 2
    # test for notification of invalid language
    assert "Invalid value for LANGUAGES: 'invalidlang'" in result.stdout
    # test for generating close matches
    assert "pythonvanilla  leiningen  xilinx  vivado  vaadin" in result.stdout
    assert not Path(".gitignore").exists()


def test_help() -> None:
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["-h"])
    assert result.exit_code == 0


def test_file() -> None:
    result = runner.invoke(app, ["react", "--file", ".prettierignore"])
    assert result.exit_code == 0
    assert Path(".prettierignore").exists()
    result = runner.invoke(app, ["python", "--overwrite", "-f", ".prettierignore"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "--append", "-f", ".prettierignore"])
    assert result.exit_code == 0


def test_append() -> None:
    result = runner.invoke(app, ["python", "-a"])
    assert result.exit_code == 0
    assert Path(".gitignore").exists()
    result = runner.invoke(app, ["python", "--append"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "-o", "-a"])
    assert result.exit_code == 2
    assert "Invalid value for append / overwrite" in result.stdout


def test_overwrite() -> None:
    result = runner.invoke(app, ["python", "-o"])
    assert result.exit_code == 0
    assert Path(".gitignore").exists()
    result = runner.invoke(app, ["python", "--overwrite"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "-a", "-o"])
    assert result.exit_code == 2
    assert "Invalid value for append / overwrite" in result.stdout


def test_list() -> None:
    result = runner.invoke(app, ["python", "-l"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "--list"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "-o", "-l"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "--overwrite", "--list"])
    assert result.exit_code == 0
    assert not Path(".gitignore").exists()


def test_directory(directory: Path) -> None:
    # first test with no overwrite - should work since the file doesn't exist
    result = runner.invoke(app, ["python", "-d", str(directory)])
    assert result.exit_code == 0
    assert Path(".gitignore").exists()
    # subsequent tests need to overwrite
    result = runner.invoke(app, ["python", "-o", "-d", str(directory)])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python", "--overwrite", "--directory", str(directory)])
    assert result.exit_code == 0


def test_no_options() -> None:
    result = runner.invoke(app, ["python"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["python"], input="a")
    assert result.exit_code == 0
    result = runner.invoke(app, ["python"], input="o")
    assert result.exit_code == 0
    result = runner.invoke(app, ["python"], input="c")
    assert result.exit_code == 1


def test_print(example_gitignore: str) -> None:
    result = runner.invoke(app, ["python", "-p"])
    assert result.exit_code == 0
    assert not Path(".gitignore").exists()
    assert result.stdout.strip() == example_gitignore.strip()
    result = runner.invoke(app, ["python", "--print"])
    assert result.exit_code == 0
    assert not Path(".gitignore").exists()
    assert result.stdout.strip() == example_gitignore.strip()
