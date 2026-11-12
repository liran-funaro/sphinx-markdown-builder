"""
A Sphinx extension to add markdown generation support.
"""

from sphinx_markdown_builder.builder import MarkdownBuilder

__version__ = "0.6.11"
__docformat__ = "reStructuredText"


def setup(app):
    app.add_builder(MarkdownBuilder)
    app.add_config_value("markdown_http_base", "", "env", str)
    app.add_config_value("markdown_uri_doc_suffix", ".md", "env", str)
    app.add_config_value("markdown_file_suffix", ".md", "env", str)
    app.add_config_value("markdown_anchor_sections", False, "env", bool)
    app.add_config_value("markdown_anchor_signatures", False, "env", bool)
    app.add_config_value("markdown_docinfo", False, "env", bool)
    app.add_config_value("markdown_bullet", "*", "env", str)
    app.add_config_value("markdown_flavor", "", "env", str)
    app.add_config_value("markdown_compact_tables", False, "env", bool)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
