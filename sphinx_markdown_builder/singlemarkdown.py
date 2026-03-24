"""Single Markdown builder."""

# pyright: reportIncompatibleMethodOverride=false, reportImplicitOverride=false

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Optional, Union, cast

from docutils import nodes
from docutils.io import StringOutput
from sphinx._cli.util.colour import darkgreen
from sphinx.environment.adapters.toctree import global_toctree_for_doc
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.docutils import SphinxTranslator, new_document
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.osutil import ensuredir, os_path

from sphinx_markdown_builder.builder import MarkdownBuilder
from sphinx_markdown_builder.translator import MarkdownTranslator
from sphinx_markdown_builder.writer import MarkdownWriter

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

logger = logging.getLogger(__name__)


class SingleFileMarkdownBuilder(MarkdownBuilder):
    """Builds the whole document tree as a single Markdown page."""

    name: str = "singlemarkdown"
    epilog: str = __("The Markdown page is in %(outdir)s.")

    # These are copied from SingleFileHTMLBuilder
    copysource: bool = False

    default_translator_class: type[SphinxTranslator] = MarkdownTranslator

    def _render_doctree(self, doctree: nodes.document) -> str:
        writer = MarkdownWriter(self)
        destination = StringOutput(encoding="utf-8")
        _ = writer.write(doctree, destination)
        return writer.output or ""

    def _render_toctree_fragment(self, docname: str, collapse: bool = False) -> str:
        toctree = global_toctree_for_doc(self.env, docname, self, collapse=collapse)
        return str(self.render_partial(toctree)["fragment"]) if toctree else ""

    def get_outdated_docs(self) -> Union[str, list[str]]:
        return "all documents"

    def get_target_uri(self, docname: str, typ: Optional[str] = None) -> str:
        if docname in self.env.all_docs:
            return f"#{docname}"
        return docname + self.out_suffix

    def get_relative_uri(self, from_: str, to: str, typ: Optional[str] = None) -> str:
        return self.get_target_uri(to, typ)

    def render_partial(self, node: Optional[nodes.Node]) -> dict[str, Union[str, bytes]]:
        """Utility: Render a lone doctree node."""
        if node is None:
            return {"fragment": ""}
        doctree = node if isinstance(node, nodes.document) else new_document("", self.env.settings)
        if doctree is not node:
            doctree.append(node)
        fragment = self._render_doctree(doctree)
        return {
            "fragment": fragment,
            "title": "",
            "css": "",
            "js": "",
            "script": "",
        }

    def _get_local_toctree(
        self,
        docname: str,
        collapse: bool = True,
        **kwargs: Union[bool, int, str],
    ) -> str:
        includehidden = kwargs.get("includehidden")
        if isinstance(includehidden, str):
            if includehidden.lower() == "false":
                kwargs["includehidden"] = False
            elif includehidden.lower() == "true":
                kwargs["includehidden"] = True
        if kwargs.get("maxdepth") == "":
            _ = kwargs.pop("maxdepth")
        toctree = global_toctree_for_doc(
            self.env,
            docname,
            self,
            collapse=collapse,
            **kwargs,  # pyright: ignore[reportArgumentType]
        )
        return str(self.render_partial(toctree)["fragment"])

    def assemble_doctree(self) -> nodes.document:
        master = cast(str, self.config.root_doc)
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self, set(), master, tree, darkgreen, [master])
        tree["docname"] = master
        self.env.resolve_references(tree, master, self)
        return tree

    def assemble_toc_secnumbers(self) -> dict[str, dict[str, tuple[int, ...]]]:
        new_secnumbers: dict[str, tuple[int, ...]] = {}
        for docname, secnums in self.env.toc_secnumbers.items():
            for id_, secnum in secnums.items():
                alias = f"{docname}/{id_}"
                new_secnumbers[alias] = secnum

        root_doc = cast(str, self.config.root_doc)
        return {root_doc: new_secnumbers}

    def assemble_toc_fignumbers(
        self,
    ) -> dict[str, dict[str, dict[str, tuple[int, ...]]]]:
        new_fignumbers: dict[str, dict[str, tuple[int, ...]]] = {}
        for docname, fignumlist in self.env.toc_fignumbers.items():
            for figtype, fignums in fignumlist.items():
                alias = f"{docname}/{figtype}"
                _ = new_fignumbers.setdefault(alias, {})
                for id_, fignum in fignums.items():
                    new_fignumbers[alias][id_] = fignum

        root_doc = cast(str, self.config.root_doc)
        return {root_doc: new_fignumbers}

    def get_doc_context(
        self,
        docname: str,  # pylint: disable=unused-argument  # pyright: ignore[reportUnusedParameter]
        body: str,
        metatags: str,
    ) -> dict[str, Union[str, bytes, bool, list[dict[str, str]], None]]:
        root_doc = cast(str, self.config.root_doc)
        toc = self._render_toctree_fragment(root_doc, collapse=False)
        return {
            "parents": [],
            "prev": None,
            "next": None,
            "docstitle": None,
            "title": cast(str, self.config.html_title),
            "meta": None,
            "body": body,
            "metatags": metatags,
            "rellinks": [],
            "sourcename": "",
            "toc": toc,
            "display_toc": bool(toc),
        }

    def write_documents(self, _docnames: set[str]) -> None:
        self.writer: Optional[MarkdownWriter] = MarkdownWriter(self)
        self.prepare_writing(set(self.env.all_docs))
        project = cast(str, self.config.project)
        root_doc = cast(str, self.config.root_doc)
        docnames = [root_doc] + sorted(self.env.found_docs - {root_doc})
        content_parts: list[str] = [f"# {project} Documentation\n\n", "## Table of Contents\n\n"]

        for docname in docnames:
            if docname == root_doc:
                content_parts.append(f"* [Main Document](#{docname})\n")
            else:
                title = docname.rsplit("/", 1)[-1].replace("_", " ").replace("-", " ").title()
                content_parts.append(f"* [{title}](#{docname})\n")

        content_parts.append("\n")
        for docname in docnames:
            logger.info("Adding content from %s", docname)

            try:
                doc = self.env.get_doctree(docname)
                content_parts.append(f'\n<a id="{docname}"></a>\n\n')
                content_parts.append(self._render_doctree(doc))
                content_parts.append("\n\n")

            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning("Error adding content from %s: %s", docname, e)
        final_content = "".join(content_parts)
        outfilename = os.path.join(self.outdir, os_path(root_doc) + self.out_suffix)
        ensuredir(os.path.dirname(outfilename))

        try:
            with open(outfilename, "w", encoding="utf-8") as f:
                _ = f.write(final_content)
        except OSError as err:
            logger.warning(__("error writing file %s: %s"), outfilename, err)


def setup(app: Sphinx) -> ExtensionMetadata:
    """Setup the singlemarkdown builder extension.

    This follows the pattern from Sphinx's own singlehtml.py.
    """
    # Setup the main extension first
    app.setup_extension("sphinx_markdown_builder")

    # No need to register the builder here as it's already registered in __init__.py

    return {
        "version": "builtin",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
