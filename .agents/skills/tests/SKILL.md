---
name: tests
description: Use when adding or changing a test case for sphinx-markdown-builder — a new node handler, a config option, a Sphinx extension or domain fixture, or expected output that exposes a discrepancy — or when `make test` fails and the expected output needs updating.
---

# Adding a diff-based test case

Tests here are golden files: input in `tests/source/` (RST) or `tests/my_module/` (Python for
autodoc), expected Markdown in `tests/expected/`, and one build that diffs them. The why behind
each step is in [`pr-review/RULES.md`](../pr-review/RULES.md) rules 1–3.

## 1. Add the input

- **RST behavior** → add a section to the existing file that fits (`blocks.rst`, `links.rst`,
  `tables.rst`, …). Create a new `.rst` only when the feature needs its own setup, and then add
  it to the `toctree` in `tests/source/index.rst` (which changes `tests/expected/index.md` too).
- **Autodoc / Python domain** → add a real function or class to `tests/my_module/` whose
  signature and docstring match what it actually does. Don't hand-write a `py:function`
  directive to fake the node tree an extension would produce (rule 2).
- **Sphinx extension** → enable it in `tests/source/conf.py` and add it to the `dev` extras in
  `pyproject.toml` if it isn't there.

## 2. Check the doctree

```bash
make doc-xml   # writes tests/docs-build/xml/
```

Confirm the node shape the translator will see, e.g. `desc_parameterlist > desc_optional`.

## 3. Cover a config option

A new `markdown_*` option goes into the **existing** overrides build — never a new build step
(rule 3). Add it in both places, with the same value:

1. The `-D` flags of the "Building markdown with configuration overrides..." step in the
   `Makefile` `test-diff` target.
2. `SOURCE_FLAGS[1]` in `tests/test_builder.py`, so pytest coverage sees it.

The overrides build writes to `tests/docs-build/overrides/markdown/`. If the option changes a
file not already copied, add one `cp` line in `test-diff` following the existing pattern
(`<name>.markdown` → `overrides-<name>.markdown`), then commit the matching file in
`tests/expected/`.

## 4. Generate and review the expected output

```bash
make test-diff                      # fails, showing the diff
make diff                           # or DIFFTOOL=<tool>; review every change
cp tests/docs-build/markdown/<file> tests/expected/<file>
make test                           # diff tests + pytest with coverage
```

Read the generated Markdown before copying it: the expected file is the spec. Every changed line
in `tests/expected/` must be intended. An unrelated change means the code change leaks.

A test-only PR may commit expected output that shows the *correct* Markdown and so fails CI
(see `CONTRIBUTING.md`, "Contributing Tests"). Say so in the PR's `#### Additional details`.

## 5. Unit tests only as a last resort

Add a `tests/test_*.py` white-box test only for a path no RST or Python fixture can reach, e.g. a
defensive fallback. Coverage must stay at 100%.
