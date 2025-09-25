# sphinx-markdown-builder

[![Coverage Status](https://coveralls.io/repos/github/liran-funaro/sphinx-markdown-builder/badge.svg?branch=main&cache-bust=1)](https://coveralls.io/github/liran-funaro/sphinx-markdown-builder?branch=main)

A Sphinx extension to add markdown generation support.

## Install

```sh
pip3 install sphinx-markdown-builder==0.6.8
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
* `markdown_docinfo`: Adds metadata to the top of each document containing author, copyright, and version.
* `markdown_http_base`: If set, all references will link to this prefix address
* `markdown_uri_doc_suffix`: If set, all references will link to documents with this suffix.
* `markdown_file_suffix`: Sets the file extension for generated markdown files (default: `.md`).
* `markdown_bullet`: Sets the bullet marker.
* `markdown_flavor`: If set to `github`, output will suit GitHub's flavor of Markdown.

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
