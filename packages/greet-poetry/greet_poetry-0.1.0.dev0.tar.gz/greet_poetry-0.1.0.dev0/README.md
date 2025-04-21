# Greet Poetry

<a href="https://github.com/seriquynh/greet-poetry/actions"><img src="https://github.com/seriquynh/greet-poetry/workflows/test/badge.svg" alt="CI Status"></a>
<a href="https://pypi.org/project/greet-poetry"><img src="https://img.shields.io/pypi/dm/greet-poetry" alt="Monthly Downloads"></a>
<a href="https://pypi.org/project/greet-poetry"><img src="https://img.shields.io/pypi/v/greet-poetry" alt="Latest Stable Version"></a>
<a href="https://pypi.org/project/greet-poetry"><img src="https://img.shields.io/pypi/l/greet-poetry" alt="The MIT License"></a>

## Introduction

This is a Python package template using Poetry.

## Requirements

- Python `3.11`, `3.12`, `3.13`

## Development

Install the `poetry` CLI.

```bash
pip install poetry
```

Install the project dependencies.

```bash
poetry install
```

Fix code style using `autoflake`, `black` and `isort`.

```bash
poetry run autoflake --in-place --remove-unused-variables -r src/ tests/; poetry run black src/ tests/; poetry run isort src/ tests/;
```

Analyze code using `mypy`.

```bash
poetry run mypy src/ tests/
```

Run tests using `pytest`.

```bash
poetry run pytest
```

Build and publish to `PyPI`.

```bash
poetry build

poetry config pypi-token.pypi <pypi-api-token>

peotry publish
```

## License

Greet Poetry is licensed under the [MIT license](LICENSE.md).
