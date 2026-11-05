---
name: pr-review
description: Use when reviewing a pull request, or when checking your own changes before opening one.
---

Review the requested pull request against this repository's diff-based test workflow and the maintainer's conventions.

1. Read the pull request description, changed files, and linked issue.
2. Identify whether the change affects the Markdown translator, RST parsing, output metadata, configuration, or tests.
3. Check the touched code paths and every caller of changed functions before judging behavior.
4. Run `make lint`.
5. Run `make test`.
6. If generated output changes, inspect `make diff` with the repository's configured diff tool and verify that the files under `tests/expected` intentionally and completely express the new behavior.
7. Confirm that Sphinx core behavior, other builders, and the public API remain unchanged unless the issue explicitly requests a change.
8. Check the diff against every rule in [`RULES.md`](RULES.md). The step is done when each rule is either tied to the specific hunks that pass or break it, or marked as not touched by this diff.
9. Report the result with:
    - A two-sentence summary of the change.
    - Commands run and whether they passed.
    - Behavioral risks, especially changes to generated Markdown or compatibility.
    - Missing test coverage.
    - A numbered list of required and suggested changes. Name the `RULES.md` rule behind each finding and show the fix in its "This" form, as a suggestion block where the change is small.
    - A verdict: approve, request changes, or discuss first.

Base the verdict on whether the expected output represents the intended behavior and the diff follows `RULES.md`; passing checks are necessary but not sufficient.
