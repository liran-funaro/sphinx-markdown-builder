"""Single Markdown builder."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Set

from docutils import nodes
from sphinx.environment.adapters.toctree import global_toctree_for_doc
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.display import progress_message
from sphinx.util.nodes import inline_all_toctrees

from sphinx_markdown_builder.builder import MarkdownBuilder

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

logger = logging.getLogger(__name__)


class SingleFileMarkdownBuilder(MarkdownBuilder):
    """Builds the whole document tree as a single Markdown page."""

    name = "singlemarkdown"
    epilog = __("The Markdown page is in %(outdir)s.")

    def get_outdated_docs(self) -> str | list[str]:
        return "all documents"

    def get_target_uri(self, docname: str, typ: str | None = None) -> str:
        if docname in self.env.all_docs:
            # All references are on the same page, use section anchors
            return f"#{docname}"
        # External files (like images, etc.) use regular approach
        return super().get_target_uri(docname, typ)

    def get_relative_uri(self, from_: str, to: str, typ: str | None = None) -> str:
        # Ignore source
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
        logger.info(master)
        tree = inline_all_toctrees(self, set(), master, tree, logger.info, [master])
        tree["docname"] = master
        self.env.resolve_references(tree, master, self)
        return tree

    def assemble_toc_secnumbers(self) -> dict[str, dict[str, tuple[int, ...]]]:
        # Assemble toc_secnumbers to resolve section numbers
        new_secnumbers: dict[str, tuple[int, ...]] = {}
        for docname, secnums in self.env.toc_secnumbers.items():
            for id_, secnum in secnums.items():
                alias = f"{docname}/{id_}"
                new_secnumbers[alias] = secnum

        return {self.config.root_doc: new_secnumbers}

    def assemble_toc_fignumbers(
        self,
    ) -> dict[str, dict[str, dict[str, tuple[int, ...]]]]:
        # Assemble toc_fignumbers to resolve figure numbers
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
        # simplified context since everything is in one file
        toctree = global_toctree_for_doc(self.env, self.config.root_doc, self, collapse=False)

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
            "title": self.config.root_doc,
            "meta": None,
            "body": body,
            "metatags": metatags,
            "rellinks": [],
            "sourcename": "",
            "toc": toc,
            "display_toc": display_toc,
        }

    def write_documents(self, _docnames: Set[str]) -> None:
        self.prepare_writing(self.env.all_docs.keys())

        with progress_message(__("assembling single document")):
            doctree = self.assemble_doctree()
            self.env.toc_secnumbers = self.assemble_toc_secnumbers()
            self.env.toc_fignumbers = self.assemble_toc_fignumbers()

        with progress_message(__("writing")):
            # Limit to root_doc so we don't duplicate processing
            self.write_doc(self.config.root_doc, doctree)


def setup(app: Sphinx) -> ExtensionMetadata:
    app.setup_extension("sphinx_markdown_builder")

    app.add_builder(SingleFileMarkdownBuilder)

    return {
        "version": "builtin",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
