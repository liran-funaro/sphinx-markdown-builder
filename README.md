# sphinx-markdown-builder

[![PyPI version](https://img.shields.io/pypi/v/sphinx-markdown-builder.svg)](https://pypi.org/project/sphinx-markdown-builder/)
[![PyPI downloads](https://img.shields.io/pypi/dm/sphinx-markdown-builder.svg)](https://pypi.org/project/sphinx-markdown-builder/)
[![Python Versions](https://img.shields.io/pypi/pyversions/sphinx-markdown-builder.svg)](https://pypi.org/project/sphinx-markdown-builder/)
[![Coverage Status](https://coveralls.io/repos/github/liran-funaro/sphinx-markdown-builder/badge.svg?branch=main&cache-bust=1)](https://coveralls.io/github/liran-funaro/sphinx-markdown-builder?branch=main)

A Sphinx extension to add markdown generation support.

## Install

```sh
pip3 install sphinx-markdown-builder==0.6.11
```

## Usage

Add the extension to your `conf.py` file:
```python
extensions = [
    ...,
    "sphinx_markdown_builder",
    ...,
]
```

Build markdown files with `sphinx-build` command
```sh
sphinx-build -M markdown ./docs ./build
```

## Configurations

You can add the following configurations to your `conf.py` file:

* `markdown_anchor_sections`/`markdown_anchor_signatures`: If set to `True`, 
  then anchors will be added before each section/function/class signature. 
  This allows references to a specific anchor in the document.
* `markdown_docinfo`: If set to `True`, adds YAML frontmatter at the beginning of each document
  containing available author, contact, copyright, date, organization, revision, status, and version
  metadata (default: `False`). A field in the document's
  [file-wide metadata](https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html#file-wide-metadata)
  replaces the `conf.py` value, and `:authors:` gives a list. Other fields are left out.
* `markdown_http_base`: If set, all references will link to this prefix address
* `markdown_uri_doc_suffix`: If set, all references will link to documents with this suffix.
* `markdown_file_suffix`: Sets the file extension for generated markdown files (default: `.md`).
* `markdown_bullet`: Sets the bullet marker.
* `markdown_flavor`: If set to `github`, output will suit GitHub's flavor of Markdown.
* `markdown_compact_tables`: If set to `True`, generates Markdown tables without
  column-alignment padding. Defaults to `False`, preserving the existing formatting.
* `markdown_suppress_comments`: If set to `True`, reStructuredText comments (`.. text`) are left out of the output,
  as in Sphinx's HTML builder. Defaults to `False`, which renders each comment as `<!-- text -->`.
* `markdown_include_raw_types`: The `raw` directive formats to write to the output, verbatim
  (default: `["html", "markdown"]`). Raw content of any other format (e.g., `latex`) is left out.
  Set it to `["markdown"]` to leave out raw HTML as well.
* `markdown_abbreviation_first`: How the first occurrence of an abbreviation (`:abbr:`) in a document is written:
  `"inline"` (default) writes `LLM (Large Language Model)`, and `"footnote"` writes `LLM[^abbr-1]`,
  with `[^abbr-1]: **LLM**: Large Language Model` at the end of the document.
* `markdown_abbreviation_repeat`: How the later occurrences of an abbreviation are written:
  `"plain"` (default) writes `LLM`, `"inline"` writes `LLM (Large Language Model)`,
  and `"footnote"` writes `LLM[^abbr-1]`, sharing the footnote of the other occurrences.
  Inside code blocks, where a footnote can't link, the inline form is written instead of a footnote.

For example, if your `conf.py` file have the following configuration:

```python
markdown_http_base = "https://your-domain.com/docs"
markdown_uri_doc_suffix = ".html"
markdown_bullet = "*"
```

Then a reference to `your-doc-name#your-header` will be substituted with `https://your-domain.com/docs/your-doc-name.html#your-header`. 


## Contributing

See the [code contribution guidelines](CONTRIBUTING.md) for more information.

## Credits
This project forked from [clayrisser/sphinx-markdown-builder], which was developed by [Clay Risser] under the [MIT] license.

The original implementation was based on [doctree2md] by [Matthew Brett] under the [BSD-2] license.

## License

[MIT]

[clayrisser/sphinx-markdown-builder]: https://github.com/clayrisser/sphinx-markdown-builder
[Clay Risser]: https://github.com/clayrisser
[doctree2md]: https://github.com/matthew-brett/nb2plots/blob/master/nb2plots/doctree2md.py
[Matthew Brett]: https://github.com/matthew-brett
[MIT]: LICENSE
[BSD-2]: https://github.com/matthew-brett/nb2plots/blob/main/LICENSE
