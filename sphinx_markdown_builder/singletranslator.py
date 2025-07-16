"""Custom translator for single markdown file output."""

# pyright: reportImplicitOverride=false

import re
from typing import TYPE_CHECKING, cast

from docutils import nodes

from sphinx_markdown_builder.translator import MarkdownTranslator

if TYPE_CHECKING:  # pragma: no cover
    from sphinx_markdown_builder.singlemarkdown import SingleFileMarkdownBuilder


class SingleMarkdownTranslator(MarkdownTranslator):
    """Translator that ensures proper content inclusion for a single markdown file."""

    def __init__(self, document: nodes.document, builder: "SingleFileMarkdownBuilder"):
        super().__init__(document, builder)
        # Keep track of document names we've seen to avoid duplications
        self._seen_docs: list[str] = []

    def visit_section(self, node: nodes.Element):
        """Capture section node visit to ensure proper handling."""
        # Add anchors for document sectioning
        docname: str = cast(str, node.get("docname"))
        if docname and docname not in self._seen_docs:
            self._seen_docs.append(docname)
            self.add(f'<a id="document-{docname}"></a>', prefix_eol=2)
            # Add a title with the document name
            safe_name = re.sub(r"[^a-zA-Z0-9-]", " ", docname.split("/")[-1]).title()
            self.add(f"# {safe_name}", prefix_eol=1, suffix_eol=2)

        # Call the parent's visit_section method
        MarkdownTranslator.visit_section(self, node)
