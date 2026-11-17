---
name: doc-audit
description: Use after finishing a change to sphinx-markdown-builder that touched config options, node handlers, make targets, test layout, or file paths, or when asked to "check the docs" or "did I make anything obsolete?". Reports documentation, agent instructions, and skills made stale by the diff. Audits existing files only; it does not write new docs.
---

# Auditing docs and agent instructions after a change

A change can quietly invalidate the README, `CONTRIBUTING.md`, `AGENTS.md`, or a skill: a new
config option nobody documented, a renamed make target, a moved test file. This skill checks the
existing docs against the diff and reports what is stale. It doesn't write new documentation.

Prefer running it on a subagent: the deliverable is only the report below.

## 1. Establish the change set

```bash
base=$(git merge-base origin/main HEAD)
git diff --stat "$base"
git diff "$base"            # branch + working tree (tracked files only)
git ls-files --others --exclude-standard                    # new, untracked files
git ls-files --others --ignored --exclude-standard .agents  # new skills (.gitignore has skills/)
```

`git diff` doesn't show new files that are not yet added, so read the files from the last two
commands too.

Extract the vocabulary to grep for:

- **Config options**: added, renamed, or removed `app.add_config_value(...)` calls in
  `sphinx_markdown_builder/__init__.py`, and changed defaults.
- **Node handlers**: new or removed `visit_*` / `depart_*` methods and `PREDEFINED_ELEMENTS`
  entries in `sphinx_markdown_builder/translator.py`.
- **Make targets and test layout**: changes to `Makefile`, `tests/test_builder.py`, or files
  under `tests/`.
- **Paths and symbols**: moved or renamed files, and renamed classes or functions.
- **Dependencies and Python versions**: `pyproject.toml` changes.

## 2. Check each target

| Target | Stale when |
|---|---|
| `README.md` "Configurations" | An option in `add_config_value` is missing, has a wrong default, or describes old behavior. Every option must be listed. |
| `README.md` "Usage" | Install or usage changed. |
| `CONTRIBUTING.md` | Make targets, test folders, or the contribution workflow changed. |
| `AGENTS.md` | Commands table, Testing, Code Style, or Architecture paths no longer match `Makefile`, `pyproject.toml`, or the tree. |
| `.agents/skills/**` | A skill names a file, make target, option, or step that no longer exists or now works differently (e.g. `tests` skill on the overrides build, `pr-review/RULES.md` examples). |
| `.github/` templates | Labels, sections, or paths they mention changed. |

For each item in the vocabulary, grep the corpus:

```bash
grep -rn -e '<term>' --include='*.md' README.md CONTRIBUTING.md AGENTS.md .agents .github
```

Use `grep` over these paths, not `git grep`: it also searches new skills that are untracked or
matched by the `skills/` ignore rule.

Check the reverse too: each option, target, or path the docs mention still exists.

Skip `tests/expected/` and `tests/source/` (they are test data, not docs) and version strings
(managed by `bumpver`).

## 3. Report

```
## Doc audit: <branch>

### Stale (fix before merging)
- README.md:47 — `markdown_foo` default is `True` in __init__.py:24, docs say `False`.
  Suggested: "...(default: `True`)".

### Missing
- README.md "Configurations" — `markdown_bar` (added in __init__.py:25) is not documented.

### Checked, no change needed
- AGENTS.md, CONTRIBUTING.md, .agents/skills/tests
```

Cite `file:line` for each finding and give a concrete suggested edit. Apply the edits only if
the user asks.
