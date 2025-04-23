import os
from pathlib import Path

import pytest


def pytest_configure(config) -> None:  # type: ignore[no-untyped-def]  # see https://stackoverflow.com/questions/65491369/how-to-specify-mypy-type-pytest-configure-fixtures
    # required to make sure files are created in the same directory as the test file
    os.chdir(Path(__file__).parent.resolve())


@pytest.fixture(autouse=True)
def setup_and_teardown():  # type: ignore[no-untyped-def]  # see https://stackoverflow.com/questions/65491369/how-to-specify-mypy-type-pytest-configure-fixtures
    # Setup code
    yield
    # Teardown code
    for path in Path(__file__).resolve().parent.iterdir():
        print(path)
        if path.name.endswith(".gitignore"):
            path.unlink()
        elif path.name.endswith(".prettierignore"):
            path.unlink()
