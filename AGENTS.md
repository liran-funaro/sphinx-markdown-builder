# AGENTS.md — sphinx-markdown-builder

## Project Overview

A Sphinx extension that adds a markdown builder, enabling `sphinx-build -M markdown` to generate Markdown output from
RST documentation sources.

## Quick-Start Checklist

- [ ] Read `README.md` and `CONTRIBUTING.md` before making changes.
- [ ] Run `make test` to verify generated markdown matches expected output.
- [ ] Run `make lint` to check coding conventions.

## Local Development Commands

| Task                       | Command                 |
|----------------------------|-------------------------|
| Install (dev dependencies) | `pip install -e .[dev]` |
| Build docs (markdown)      | `make docs`             |
| Build AST tree (xml)       | `make doc-xml`          |
| Run tests                  | `make test`             |
| Lint                       | `make lint`             |
| Clean build artifacts      | `make clean`            |

## Testing

- Tests are **diff-based**: `make test` builds markdown from `tests/source` and compares the output in
  `tests/docs-build/markdown/` against `tests/expected/`.
- To visually inspect differences after a failure, run `make diff` (uses `meld` by default; override with
  `DIFFTOOL=<tool>`).
- When adding or changing functionality, update or add corresponding expected output files in `tests/expected`.
- Run `pytest --cov=sphinx_markdown_builder` for unit tests with coverage.
- **White-box (unit) tests are discouraged**: The diff-based tests should cover all functionality. Use white-box tests
  only when diff tests cannot adequately verify the behavior.

## Code Style

- **Black**: line length `120`.
- **Flake8**: select `E,F,W,C`, max complexity `10`, max line length `120`.
- **Pylint**: disable `C0116` (missing function docstring) and `C0115` (missing class docstring).
- Run `make lint` to check all linters before submitting changes.

## Architecture

- Main package: `sphinx_markdown_builder` — the Sphinx builder extension.
- Entry point registered in `pyproject.toml` under `[project.entry-points."sphinx.builders"]`.
- Test source docs: `tests/source` (RST files + `conf.py`).
- Test sample module: `tests/my_module` (used with `sphinx.ext.autodoc`).
- Expected test output: `tests/expected`.
- **Debugging**: `make doc-xml` generates the intermediate XML doctree — this is the input to the markdown translator and is essential for debugging translation issues.

## Versioning

- Version is managed via `bumpver` in `pyproject.toml`.
- Version strings appear in multiple files; use `bumpver` to update them consistently.
- Do not manually edit version numbers across files.

## Pull Requests

- Before submitting a PR, run `ponytail review` to validate your changes. See
  the [ponytail-review skill](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-review/SKILL.md) for
  details.

## Non-Goals

- Do not modify Sphinx core behavior outside the markdown builder scope.
- Do not bump major versions without discussion.
