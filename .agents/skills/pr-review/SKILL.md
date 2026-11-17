---
name: pr-review
description: Use when reviewing a pull request, or when checking your own changes before opening one.
---

Review the requested pull request against this repository's diff-based test workflow and the maintainer's conventions.

1. Read the pull request description, changed files, and linked issue.
   Check that the description follows [`.github/pull_request_template.md`](../../../.github/pull_request_template.md) as described in the [commit-and-issue skill](../commit-and-issue/SKILL.md): only the template headers, no verification rundown, and a linked issue.
2. Identify whether the change affects the Markdown translator, RST parsing, output metadata, configuration, or tests.
3. Check the touched code paths and every caller of changed functions before judging behavior.
4. Run `make lint`.
5. Run `make test`.
6. If generated output changes, inspect `make diff` with the repository's configured diff tool and verify that the files under `tests/expected` intentionally and completely express the new behavior.
7. Confirm that Sphinx core behavior, other builders, and the public API remain unchanged unless the issue explicitly requests a change.
8. Check the diff against every rule in [`RULES.md`](RULES.md). The step is done when each rule is either tied to the specific hunks that pass or break it, or marked as not touched by this diff.
9. Use the [ponytail-review skill](../ponytail-review/SKILL.md) on the diff and connected code, and include its findings in the review.
10. Use the [doc-audit skill](../doc-audit/SKILL.md) and include any stale or missing documentation as findings.
11. Report the result with:
    - A two-sentence summary of the change.
    - Commands run and whether they passed.
    - Behavioral risks, especially changes to generated Markdown or compatibility.
    - Missing test coverage.
    - A numbered list of required and suggested changes. Name the `RULES.md` rule behind each finding and show the fix in its "This" form, as a suggestion block where the change is small.
    - A verdict: approve, request changes, or discuss first.

Base the verdict on whether the expected output represents the intended behavior and the diff follows `RULES.md`; passing checks are necessary but not sufficient.

## Posting the review to GitHub

Only when the user asks to post the review:

1. Record the commit you reviewed, so the comments attach to the code you read even if new commits are pushed meanwhile:

   ```bash
   gh pr view <NUMBER> --repo liran-funaro/sphinx-markdown-builder --json headRefOid -q .headRefOid
   ```

2. Write the full review to `PR_<NUMBER>_REVIEW.md` first and re-read it. For each finding you could not confirm in the code, either drop it (if it is speculative) or keep it labeled "Possible issue (could not confirm)" (if the evidence makes it likely).
3. Show the review to the user and wait for explicit approval. Ask how to post it:
   - **Pending (draft)**: the review is saved on GitHub but not published. Only the user sees it, can edit or delete its comments there, and publishes it from the PR's "Finish your review" button. GitHub allows one pending review per user per PR, so if one already exists, ask the user to submit or delete it first.
   - **Publish now**: posted as a comment review right away.
4. Never post `APPROVE` or `REQUEST_CHANGES`. The verdict goes in the summary text. When the review is pending, the user picks the review type on publishing.
5. Post the summary and all inline comments as one review, from a JSON file:

   ```bash
   gh api -X POST repos/liran-funaro/sphinx-markdown-builder/pulls/<NUMBER>/reviews --input /tmp/review.json
   ```

   ```json
   {
     "commit_id": "<the SHA from step 1>",
     "event": "COMMENT",
     "body": "<summary, verdict, and findings outside the diff>",
     "comments": [
       {"path": "sphinx_markdown_builder/translator.py", "line": 42, "side": "RIGHT", "body": "<finding>"}
     ]
   }
   ```

   For a pending review, leave out the `event` field; GitHub then keeps the review as `PENDING`. Give the user the PR's "Files changed" URL to review and publish it.

   An inline comment's `line` must be inside a diff hunk. Put findings about code outside the diff in `body`. Comment once on a repeated pattern and list the other lines.
6. Use a `suggestion` block for small, concrete fixes, and wrap explanations longer than about five lines in `<details>`.
