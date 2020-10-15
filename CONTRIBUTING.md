# Contributing

Pull requests are welcome!

But please create an issue and state the problem to be resolved first so we can have a clear idea.

You can also help by filing bug reports.

This package uses the following for development:

| Package         | Purpose              |
| -------         | -------              |
| pytest          | Testing              |
| vulture         | Dead code detection  |
| mypy            | Static type checking |
| pylint & flake8 | Linting              |
| coverage        | Test coverage        |
| tox             | Test automation      |

Use the following command to install them.

    pip install -r requirements-dev.txt

## Tests (pytest)

Make sure to add tests for any new piece of code using pytest.

    pytest

## Dead code detection (vulture)

Vulture to check for dead code.

    tox -e vulture

## Static type checking (mypy)

Use type annotations for every function definition and apply mypy for static type checking.

    tox -e mypy

## Linting (pylint and flake8)

Use both pylint and flake8 for linting.

    tox -e pylint,flake8

## Test coverage (coverage)

Ensure proper test coverage with coverage.py

    tox -e coverage

## All checks

Run all checks with

    tox
