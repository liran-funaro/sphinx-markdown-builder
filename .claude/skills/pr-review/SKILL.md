---
name: pr-review
description: Review a pull request for the Sphinx Markdown Builder by checking the implementation, generated Markdown output, test expectations, lint, and documentation.
---

Review the requested pull request against this repository's diff-based test workflow.

1. Read the pull request description, changed files, and linked issue.
2. Identify whether the change affects the Markdown translator, RST parsing, output metadata, configuration, or tests.
3. Check the touched code paths and every caller of changed functions before judging behavior.
4. Run `make lint`.
5. Run `make test`.
6. If generated output changes, inspect `make diff` with the repository's configured diff tool and verify that the files under `tests/expected` intentionally and completely express the new behavior.
7. For a new feature, add or update a diff-based fixture before adding a white-box test. Prefer expected-output fixtures because this repository's primary contract is the generated Markdown.
8. Confirm that Sphinx core behavior, other builders, and the public API remain unchanged unless the issue explicitly requests a change.
9. Confirm that version numbers are not changed manually; use the repository's versioning tool only when the maintainers request a release.
10. Report the result with:
    - A two-sentence summary of the change.
    - Commands run and whether they passed.
    - Behavioral risks, especially changes to generated Markdown or compatibility.
    - Missing test coverage.
    - A numbered list of required and suggested changes.
    - A verdict: approve, request changes, or discuss first.

Do not approve a change solely because the checks pass. Verify that the expected output represents the intended behavior.
