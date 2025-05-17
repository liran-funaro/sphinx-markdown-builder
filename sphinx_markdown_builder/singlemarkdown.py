"""Single Markdown builder."""

from __future__ import annotations

import os
from io import StringIO
from typing import TYPE_CHECKING, Any

from docutils import nodes
from sphinx.environment.adapters.toctree import global_toctree_for_doc
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.osutil import ensuredir, os_path

from sphinx_markdown_builder.builder import MarkdownBuilder
from sphinx_markdown_builder.singletranslator import SingleMarkdownTranslator
from sphinx_markdown_builder.writer import MarkdownWriter

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

logger = logging.getLogger(__name__)


class SingleFileMarkdownBuilder(MarkdownBuilder):
    """Builds the whole document tree as a single Markdown page."""

    name = "singlemarkdown"
    epilog = __("The Markdown page is in %(outdir)s.")

    # These are copied from SingleFileHTMLBuilder
    copysource = False

    # Use the custom translator for single file output
    default_translator_class = SingleMarkdownTranslator

    def get_outdated_docs(self) -> str | list[str]:
        return "all documents"

    def get_target_uri(self, docname: str, typ: str | None = None) -> str:
        if docname in self.env.all_docs:
            # All references are on the same page, use anchors
            # Add anchor for document
            return f"#{docname}"
        # External files like images or other resources
        return docname + self.out_suffix

    def get_relative_uri(self, from_: str, to: str, typ: str | None = None) -> str:
        # Ignore source - all links are in the same document
        return self.get_target_uri(to, typ)

    def _get_local_toctree(self, docname: str, collapse: bool = True, **kwargs: Any) -> str:
        if isinstance(includehidden := kwargs.get("includehidden"), str):
            if includehidden.lower() == "false":
                kwargs["includehidden"] = False
            elif includehidden.lower() == "true":
                kwargs["includehidden"] = True
        if kwargs.get("maxdepth") == "":
            kwargs.pop("maxdepth")
        toctree = global_toctree_for_doc(self.env, docname, self, collapse=collapse, **kwargs)
        return self.render_partial(toctree)["fragment"]

    def assemble_doctree(self) -> nodes.document:
        master = self.config.root_doc
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self, set(), master, tree, logger.info, [master])
        tree["docname"] = master
        self.env.resolve_references(tree, master, self)
        return tree

    def assemble_toc_secnumbers(self) -> dict[str, dict[str, tuple[int, ...]]]:
        new_secnumbers: dict[str, tuple[int, ...]] = {}
        for docname, secnums in self.env.toc_secnumbers.items():
            for id_, secnum in secnums.items():
                alias = f"{docname}/{id_}"
                new_secnumbers[alias] = secnum

        return {self.config.root_doc: new_secnumbers}

    def assemble_toc_fignumbers(
        self,
    ) -> dict[str, dict[str, dict[str, tuple[int, ...]]]]:
        new_fignumbers: dict[str, dict[str, tuple[int, ...]]] = {}
        for docname, fignumlist in self.env.toc_fignumbers.items():
            for figtype, fignums in fignumlist.items():
                alias = f"{docname}/{figtype}"
                new_fignumbers.setdefault(alias, {})
                for id_, fignum in fignums.items():
                    new_fignumbers[alias][id_] = fignum

        return {self.config.root_doc: new_fignumbers}

    def get_doc_context(
        self,
        docname: str,  # pylint: disable=unused-argument
        body: str,
        metatags: str,
    ) -> dict[str, Any]:
        # no relation links...
        toctree = global_toctree_for_doc(self.env, self.config.root_doc, self, collapse=False)
        # if there is no toctree, toc is None
        if toctree:
            toc = self.render_partial(toctree)["fragment"]
            display_toc = True
        else:
            toc = ""
            display_toc = False
        return {
            "parents": [],
            "prev": None,
            "next": None,
            "docstitle": None,
            "title": self.config.html_title,
            "meta": None,
            "body": body,
            "metatags": metatags,
            "rellinks": [],
            "sourcename": "",
            "toc": toc,
            "display_toc": display_toc,
        }

    def write_documents(self, _docnames: set[str]) -> None:
        # Prepare writer for output
        self.writer = MarkdownWriter(self)

        # Prepare for writing all documents
        self.prepare_writing(self.env.all_docs)

        # To store final output
        content_parts = []

        # Add main header
        content_parts.append(f"# {self.config.project} Documentation\n\n")

        # Add table of contents
        content_parts.append("## Table of Contents\n\n")

        # The list of docnames to process - start with root doc and include all docnames
        docnames = [self.config.root_doc] + list(self.env.found_docs - {self.config.root_doc})

        # Add TOC entries
        for docname in docnames:
            if docname == self.config.root_doc:
                content_parts.append(f"* [Main Document](#{docname})\n")
            else:
                title = docname.rsplit("/", 1)[-1].replace("_", " ").replace("-", " ").title()
                content_parts.append(f"* [{title}](#{docname})\n")

        content_parts.append("\n")

        # Process each document
        for docname in docnames:
            logger.info("Adding content from %s", docname)

            try:
                # Get the doctree for this document
                doc = self.env.get_doctree(docname)

                # Add anchor for linking
                content_parts.append(f'\n<a id="{docname}"></a>\n\n')

                # Generate title based on docname
                if docname == self.config.root_doc:
                    title = "Main Document"
                else:
                    title = docname.rsplit("/", 1)[-1].replace("_", " ").replace("-", " ").title()

                content_parts.append(f"## {title}\n\n")

                # Get markdown writer output for this document
                self.writer = MarkdownWriter(self)

                destination = StringIO()
                self.writer.write(doc, destination)  # Use StringIO as destination
                content_parts.append(self.writer.output)
                content_parts.append("\n\n")

            except Exception as e:
                logger.warning("Error adding content from %s: %s", docname, e)

        # Combine all content
        final_content = "".join(content_parts)

        # Write to output file
        outfilename = os.path.join(self.outdir, os_path(self.config.root_doc) + self.out_suffix)

        # Ensure output directory exists
        ensuredir(os.path.dirname(outfilename))

        try:
            with open(outfilename, "w", encoding="utf-8") as f:
                f.write(final_content)
        except OSError as err:
            logger.warning(__("error writing file %s: %s"), outfilename, err)


def setup(app: Sphinx) -> ExtensionMetadata:
    app.setup_extension("sphinx_markdown_builder")

    app.add_builder(SingleFileMarkdownBuilder)

    return {
        "version": "builtin",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
