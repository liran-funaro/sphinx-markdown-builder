"""
Custom translator for single markdown file output.
"""

import re

from sphinx_markdown_builder.translator import MarkdownTranslator


class SingleMarkdownTranslator(MarkdownTranslator):
    """Translator that ensures proper content inclusion for a single markdown file."""

    def __init__(self, document, builder):
        super().__init__(document, builder)
        # Keep track of document names we've seen to avoid duplications
        self._seen_docs: list[str] = []

    def visit_section(self, node):
        """Capture section node visit to ensure proper handling."""
        # Add anchors for document sectioning
        docname = node.get("docname")
        if docname and docname not in self._seen_docs:
            self._seen_docs.append(docname)
            self.add(f'<a id="document-{docname}"></a>', prefix_eol=2)
            # Add a title with the document name
            safe_name = re.sub(r"[^a-zA-Z0-9-]", " ", docname.split("/")[-1]).title()
            self.add(f"# {safe_name}", prefix_eol=1, suffix_eol=2)

        # Call the parent's visit_section method
        MarkdownTranslator.visit_section(self, node)
