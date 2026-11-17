---
name: commit-and-issue
description: Write a commit message (which becomes the GitHub PR description verbatim) or open a GitHub issue for sphinx-markdown-builder, following the repo's PR template. Use whenever the user wants to commit changes, write or fix a commit/PR message, prepare a PR description, or file a GitHub issue — even for terse asks like "commit this", "write the PR description", or "file an issue for this bug".
---

# Commit messages and GitHub issues

This repo squash-merges PRs, and **the PR description becomes the squash commit body**. So a
commit message is the PR description, reviewed as-is. Write it to the PR template and keep the
exact wording the user approves.

The upstream repo for all `gh` operations is **`liran-funaro/sphinx-markdown-builder`**.

- **Committing / writing a commit or PR message** → [Writing a commit message](#writing-a-commit-message)
- **Filing a GitHub issue** → [Opening a GitHub issue](#opening-a-github-issue)

## Shared conventions

**Formal headers only** — A commit/PR body uses **only** the headers from
`.github/pull_request_template.md`: `#### Type of change`, `#### Description`,
`#### Additional details (Optional)`, `#### Related issues`. Never invent others (no
`## Summary`, `## Changes`, `## Checks`, `## Before / after`, `#### Motivation`, …). Anything
worth saying goes inside a formal section. Issues are not bound by this.

**Issue references** — Use `#NNN`. The keyword decides whether merging **auto-closes** the
issue, and it is **always lowercase**:

- Closing: `resolves` / `fixes` / `closes`. Default to `- resolves #141`.
- Non-closing: `- resolves partly #141`, `- related to #141`, `- follows up on #131`.

## Writing a commit message

### 1. Inspect what is being committed

```bash
git status
git diff --staged        # add `git diff` if nothing is staged yet
git log -10              # match current phrasing
```

If nothing is staged, confirm what to stage before writing the message.

### 2. Subject line

A short imperative sentence describing the change, e.g.
`Render labels outside footnotes as bold lines`.

- Roughly ≤ 70 chars, specific about what changed. Mention the config option or node name
  when that is the change (`Add markdown_suppress_comments to leave comments out of the output`).
- **Do not append `(#NNN)`** — GitHub adds it on squash-merge.
- Prefix `[BREAKING]` when the change alters existing Markdown output or configuration in a way
  users must react to.

### 3. Body from the PR template

Follow `.github/pull_request_template.md`. Strip every HTML comment (`<!-- ... -->`).

```
#### Type of change

- <one or more of: Bug fix / New feature / Improvement (improvement to code, performance, etc) / Test update / Documentation update / Breaking change>

#### Description

- <Concise — see below.>

#### Additional details (Optional)

<Optional: implementation notes, output changes, notes to reviewers.>

#### Related issues

- resolves #NNN
```

**Description — concise, not a pitch.** The linked issue carries the motivation and the
problem. The Description tells a reviewer *what this change does*:

- Lead with what changed, as `-` bullets when there's more than one point.
- Name new config options and their defaults, and new or changed node handlers.
- Include only what is **not already in the linked issue**. Don't restate the problem, propose
  future work, or sell.

**Additional details** — the place for things a reviewer needs beyond the diff:

- **Output changes**: which generated Markdown changes for existing users. A short before/after
  snippet is welcome when the output change is the point.
- Implementation choices worth flagging, and how this differs from an earlier attempt (e.g. a
  superseded PR).

**Type of change**: pick from the template list; list several when the change spans categories.

**Related issues — expected.** Ask which issue this resolves. If there isn't one, offer to open
one first and link it. Omit only for a trivial, untracked change.

**Never put in the body:** a hand-written `Signed-off-by:` trailer (added by `git commit -s`),
a `---------` separator (inserted by GitHub's squash), or labels (applied with `gh`).

**Don't narrate verification.** No `Checks` / `Commands` rundown of `make lint`, `make test`,
or coverage — CI runs them on every PR. Still run them before submitting (see `AGENTS.md`). The
exception is a step a *reviewer* must run to observe the effect (e.g. a specific `-D` override
or `make doc-xml` doctree shape), which goes in `#### Additional details`.

### 4. Show the message, then commit with sign-off

Show the full drafted message and get the user's approval before committing. Then write it to a
temp file and commit with `-F` and `-s`:

```bash
git commit -s -F /tmp/commit-msg.txt
```

Amend with `git commit -s --amend -F /tmp/commit-msg.txt`.

**Commit with `-F`, never through the editor.** Editor cleanup (`strip`) deletes every line
starting with `#`, which eats the `#### ` headers. `-F` uses `whitespace` cleanup and keeps them.
If you must edit interactively, add `--cleanup=whitespace`.

### 5. Push and open the PR

Read `git remote -v` and pick the remote by URL, not by name. If you have push access to
`liran-funaro/sphinx-markdown-builder`, push the branch there; otherwise push to your fork and
pass `--head <your-user>:<branch>`.

```bash
git push -u <remote> <branch>
gh pr create --repo liran-funaro/sphinx-markdown-builder --base main \
  --title "<subject line>" --body-file /tmp/pr-body.md
```

The PR body is the commit message body verbatim (subject and `Signed-off-by:` removed). To
update an existing PR: `gh pr edit <num> --body-file /tmp/pr-body.md`. Apply labels with
`gh pr edit <num> --add-label ...`.

## Opening a GitHub issue

1. **Understand it** — bug, feature, or discrepancy with Sphinx's output. Read the relevant code
   so the body can cite `file.py:line`.
2. **Pick the template** from `.github/ISSUE_TEMPLATE/` (`bug_report.md`, `feature_request.md`,
   `discrepancy_report.md`) and fill its sections. Include the RST input and the actual vs.
   expected Markdown where relevant. This is where motivation and background live; the PR later
   just points back here.
3. **Title** — a short description of the problem, not the fix.
4. **Labels** — propose from `gh label list` (e.g. `bug`, `enhancement`, `documentation`,
   `tests`, `CI`, `code cleanup`, `agents`). Don't invent labels.
5. Show the proposed command for approval, then:

```bash
gh issue create --repo liran-funaro/sphinx-markdown-builder \
  --title "<title>" --body-file /tmp/issue-body.md --label bug
```

Report the issue URL. If an upcoming commit resolves it, add it to `#### Related issues`.
