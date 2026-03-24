"""Single Markdown builder."""

# pyright: reportIncompatibleMethodOverride=false, reportImplicitOverride=false

from __future__ import annotations

import os
import re
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

    _NAV_ARTIFACT_TEXTS = frozenset({"genindex", "modindex", "search"})

    default_translator_class: type[SphinxTranslator] = MarkdownTranslator
    heading_level_offset: int = 0

    @classmethod
    def _is_nav_artifact_list_item(cls, node: nodes.list_item) -> bool:
        text = " ".join(node.astext().split()).strip().lower()
        return text in cls._NAV_ARTIFACT_TEXTS

    @staticmethod
    def _remove_node(node: nodes.Node) -> None:
        if node.parent is not None:
            node.parent.remove(node)

    @classmethod
    def _prune_empty_containers(cls, doc: nodes.document) -> None:
        changed = True
        while changed:
            changed = False

            for bullet_list in list(doc.findall(nodes.bullet_list)):
                if len(bullet_list.children) == 0:
                    cls._remove_node(bullet_list)
                    changed = True

            for section in list(doc.findall(nodes.section)):
                children_without_title = [child for child in section.children if not isinstance(child, nodes.title)]
                if len(children_without_title) == 0:
                    cls._remove_node(section)
                    changed = True

    @classmethod
    def _remove_nav_artifact_lists(cls, doc: nodes.document) -> None:
        for bullet_list in list(doc.findall(nodes.bullet_list)):
            list_items = [child for child in bullet_list.children if isinstance(child, nodes.list_item)]
            if list_items and all(cls._is_nav_artifact_list_item(item) for item in list_items):
                cls._remove_node(bullet_list)

    @staticmethod
    def _prepare_doctree_for_llm(doc: nodes.document) -> nodes.document:
        llm_doc = cast(nodes.document, doc.deepcopy())

        for target in list(llm_doc.findall(nodes.target)):
            SingleFileMarkdownBuilder._remove_node(target)

        for transition in list(llm_doc.findall(nodes.transition)):
            SingleFileMarkdownBuilder._remove_node(transition)

        for comment in list(llm_doc.findall(nodes.comment)):
            SingleFileMarkdownBuilder._remove_node(comment)

        SingleFileMarkdownBuilder._remove_nav_artifact_lists(llm_doc)
        SingleFileMarkdownBuilder._prune_empty_containers(llm_doc)

        return llm_doc

    def _cleanup_for_llm(self, content: str) -> str:
        # Normalize whitespace while keeping paragraph breaks intact.
        content = re.sub(r"[ \t]+\n", "\n", content)
        content = re.sub(r"\n{3,}", "\n\n", content)
        return content.strip() + "\n"

    def _render_doctree(self, doctree: nodes.document) -> str:
        writer = MarkdownWriter(self)
        destination = StringOutput(encoding="utf-8")
        _ = writer.write(doctree, destination)
        return writer.output or ""

    def _render_toctree_fragment(self, docname: str, collapse: bool = False) -> str:
        toctree = global_toctree_for_doc(self.env, docname, self, collapse=collapse)
        return str(self.render_partial(toctree)["fragment"]) if toctree else ""

    def _ordered_docnames(self, root_doc: str) -> list[str]:
        """Return documents in depth-first toctree order from the root document."""
        docnames: list[str] = []
        seen: set[str] = set()
        raw_toctree_includes = getattr(self.env, "toctree_includes", None)
        toctree_includes = raw_toctree_includes if isinstance(raw_toctree_includes, dict) else {}

        def visit(docname: str) -> None:
            if docname in seen:
                return
            seen.add(docname)
            docnames.append(docname)
            for child in toctree_includes.get(docname, []):
                visit(child)

        visit(root_doc)
        return docnames

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

    def _append_table_of_contents(self, content_parts: list[str], docnames: list[str], root_doc: str) -> None:
        content_parts.append("## Table of Contents\n\n")
        for docname in docnames:
            if docname == root_doc:
                content_parts.append(f"* [Main Document](#{docname})\n")
                continue
            title = docname.rsplit("/", 1)[-1].replace("_", " ").replace("-", " ").title()
            content_parts.append(f"* [{title}](#{docname})\n")
        content_parts.append("\n")

    def _append_doc_content(self, content_parts: list[str], docname: str, llm_cleanup_enabled: bool) -> None:
        logger.info("Adding content from %s", docname)
        try:
            doc = self.env.get_doctree(docname)
            if llm_cleanup_enabled:
                doc = self._prepare_doctree_for_llm(doc)
            else:
                content_parts.append(f'\n<a id="{docname}"></a>\n\n')
            content_parts.append(self._render_doctree(doc))
            content_parts.append("\n\n")
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.warning("Error adding content from %s: %s", docname, e)

    def write_documents(self, _docnames: set[str]) -> None:
        self.writer: Optional[MarkdownWriter] = MarkdownWriter(self)
        self.prepare_writing(set(self.env.all_docs))
        project = cast(str, self.config.project)
        root_doc = cast(str, self.config.root_doc)
        docnames = self._ordered_docnames(root_doc)
        llm_cleanup_enabled = str(self.config.singlemarkdown_flavor).lower() == "llm"
        content_parts: list[str] = [f"# {project} Documentation\n\n"]

        had_offset_attr = hasattr(self, "heading_level_offset")
        previous_offset = cast(int, getattr(self, "heading_level_offset", 0))
        # Keep the synthetic documentation title as the only H1.
        self.heading_level_offset = 1

        try:
            if not llm_cleanup_enabled:
                self._append_table_of_contents(content_parts, docnames, root_doc)

            for docname in docnames:
                self._append_doc_content(content_parts, docname, llm_cleanup_enabled)
        finally:
            if had_offset_attr:
                self.heading_level_offset = previous_offset
            else:
                delattr(self, "heading_level_offset")
        final_content = "".join(content_parts)
        if llm_cleanup_enabled:
            final_content = self._cleanup_for_llm(final_content)
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
