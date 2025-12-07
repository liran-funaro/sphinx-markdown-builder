"""
A Sphinx extension to add markdown generation support.
"""

from sphinx.util.typing import ExtensionMetadata

from sphinx_markdown_builder.builder import MarkdownBuilder
from sphinx_markdown_builder.singlemarkdown import SingleFileMarkdownBuilder

__version__ = "0.6.9"
__docformat__ = "reStructuredText"


def setup(app) -> ExtensionMetadata:
    """Setup the Sphinx extension.

    This is the main entry point for the extension.
    """
    # Register the regular markdown builder
    app.add_builder(MarkdownBuilder)

    # Register the single file markdown builder
    app.add_builder(SingleFileMarkdownBuilder)

    # Add configuration values
    app.add_config_value("markdown_http_base", "", "html", str)
    app.add_config_value("markdown_uri_doc_suffix", ".md", "html", str)
    app.add_config_value("markdown_file_suffix", ".md", "html", str)
    app.add_config_value("markdown_anchor_sections", False, "html", bool)
    app.add_config_value("markdown_anchor_signatures", False, "html", bool)
    app.add_config_value("markdown_docinfo", False, "html", bool)
    app.add_config_value("markdown_bullet", "*", "html", str)
    app.add_config_value("markdown_flavor", "", "html", str)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
