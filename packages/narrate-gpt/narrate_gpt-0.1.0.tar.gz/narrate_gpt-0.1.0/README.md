# narrate-gpt

A simple template for Python projects, with CI/CD configured through GitHub Actions.  Compatible with any virtual environment manager (e.g. `uv`, `venv`, `pyenv`, `poetry`, `conda`).

## Install

```bash
pip install "narrate-gpt @ git+ssh://git@github.com/fkodom/narrate-gpt.git"

# Install all dev dependencies (tests etc.)
pip install "narrate-gpt[test] @ git+ssh://git@github.com/fkodom/narrate-gpt.git"

# Setup pre-commit hooks
pre-commit install
```


## Tooling

| Tool | Description | Runs on |
| --- | --- | --- |
| [black](https://github.com/psf/black) | Code formatter | - `git commit` (through `pre-commit`) <br> - `git push` <br> - pull requests |
| [ruff](https://github.com/astral-sh/ruff) | Code linter | - `git commit` (through `pre-commit`) <br> - `git push` <br> - pull requests |
| [pytest](https://github.com/pytest-dev/pytest) | Unit testing framework | - `git push` <br> - pull requests |
| [mypy](https://github.com/python/mypy) | Static type checker | - `git push` <br> - pull requests |
| [pre-commit](https://github.com/pre-commit/pre-commit) | Pre-commit hooks | - `git commit` |
| [twine](https://github.com/pypa/twine) $\dagger$ | PyPI package uploader | - New release (`git tag`) |

> $\dagger$ Requires enabling the `publish.yaml` workflow.  To activate, move the file from `.github/disabled-workflows/publish.yaml.disabled` to `.github/workflows/publish.yaml`, and set a valid PyPI token as `PYPI_API_TOKEN` in the repo secrets.
>
> Then tag a new release of this repo, and GHA will automatically build and publish a Python wheel (`.whl`) to PyPI.
