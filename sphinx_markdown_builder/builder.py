"""
Custom docutils builder for Markdown.
"""

import os
import posixpath
import shutil
from contextlib import contextmanager

from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.environment import BuildEnvironment
from sphinx.locale import __
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util import logging
from sphinx.util.nodes import NodeMatcher
from sphinx.util.osutil import ensuredir, os_path

from sphinx_markdown_builder.translator import MarkdownTranslator

logger = logging.getLogger(__name__)


class MarkdownBuilder(Builder):
    name = "markdown"
    format = "markdown"
    epilog = __("The markdown files are in %(outdir)s.")

    allow_parallel = True
    default_translator_class = MarkdownTranslator

    out_suffix = ".md"
    download_dir = "_downloads"

    def __init__(self, app: Sphinx, env: BuildEnvironment):
        super().__init__(app, env)
        self.current_doc_name = None
        # (page URI, id) pairs that links point to. The translator writes an anchor for each.
        self.linked_ids: set[tuple[str, str]] = set()

    def init(self):
        self.out_suffix = self.config.markdown_file_suffix

    def get_outdated_docs(self):
        for doc_name in self.env.found_docs:
            if doc_name not in self.env.all_docs:
                yield doc_name
                continue

            source_mtime = self._get_source_mtime(doc_name)
            target_mtime = self._get_target_mtime(doc_name)
            if source_mtime is None or target_mtime is None or source_mtime > target_mtime:
                yield doc_name

    def _get_source_mtime(self, doc_name: str):
        source_name = self.env.doc2path(doc_name)
        return get_mod_time_if_exists(source_name)

    def _get_target_mtime(self, doc_name: str):
        target_name = os.path.join(self.outdir, doc_name + self.out_suffix)
        return get_mod_time_if_exists(target_name, log_error=False)

    def get_target_uri(self, docname: str, typ: str | None = None):
        """
        Returns the target file name.
        By default, we link to the currently generated Markdown files.
        But, we also support linking to external document (e.g., an HTML web page).
        """
        return f"{docname}{self.config.markdown_uri_doc_suffix}"

    def prepare_writing(self, docnames):
        """
        Collects the ids that links point to, so the translator writes their anchors even when
        `markdown_anchor_sections` or `markdown_anchor_signatures` is off. Without it, a table-of-contents entry or a
        cross-reference to an object or a section links to an anchor the page doesn't have.

        Why this resolves every page before writing any:
        - The translator writes a page's anchors as it writes the page, but the links to that page can be on any page,
          including the pages written after it. Only the links already on this page are known at that point.
        - Every page, not only the pages to write: a page that is rewritten still needs the anchors that links on the
          unchanged pages point to.
        - Resolved, not as read: before resolution, a cross-reference is a `pending_xref` that only its domain knows
          how to resolve, and a table of contents is a `toctree` node with no links yet.

        Writing the pages then resolves each one again, which costs build time. The alternatives avoid it at another
        cost:
        - Anchor every id, as the HTML builder does with its `id` attributes. That is what the two options do, and it
          adds an anchor line for every section and signature, even those nothing links to.
        - Fix the anchors in each written file after all pages are written, as the Texinfo builder does in its single
          file. That rewrites every file, and needs the links of the unchanged pages saved between builds.
        Logging is silenced here, because writing the pages logs the same warnings again.
        """
        self.linked_ids = set()
        if not docnames or (self.config.markdown_anchor_sections and self.config.markdown_anchor_signatures):
            return
        # An incremental build rewrites only changed pages. A page that is not rewritten keeps the anchors it had, even
        # when a changed page adds a link to it. A full build (-E) adds the anchor.
        with logging.suppress_logging():
            for doc_name in self.env.found_docs:
                page_uri = posixpath.normpath(self.get_target_uri(doc_name))
                for node in self.env.get_and_resolve_doctree(doc_name, self).findall(nodes.reference):
                    # A link to the same page has `refid` (see Sphinx's `make_refnode`). Any other link has `refuri`,
                    # relative to the page the link is on, with the id after `#`. An external URL matches no page.
                    uri, _, ref_id = node.get("refuri", "").partition("#")
                    if node.get("refid"):
                        self.linked_ids.add((page_uri, node["refid"]))
                    elif ref_id:
                        target_uri = posixpath.join(posixpath.dirname(page_uri), uri) if uri else page_uri
                        self.linked_ids.add((posixpath.normpath(target_uri), ref_id))

    def write_doc(self, docname: str, doctree: nodes.document):
        self.current_doc_name = docname
        visitor = self.create_translator(doctree, self)
        doctree.walkabout(visitor)
        out_filename = os.path.join(self.outdir, f"{os_path(docname)}{self.out_suffix}")
        ensuredir(os.path.dirname(out_filename))

        with io_handler(out_filename):
            with open(out_filename, "w", encoding="utf-8") as file:
                file.write(visitor.astext())

    def finish(self):
        for src_file_name, (_, dst_path) in self.env.dlfiles.items():
            source_path = os.path.join(self.srcdir, src_file_name)
            destination = os.path.join(self.outdir, self.download_dir, dst_path)
            ensuredir(os.path.dirname(destination))
            with io_handler(source_path):
                shutil.copyfile(source_path, destination)


def get_mod_time_if_exists(file_path, log_error=True):
    with io_handler(file_path, log_error):
        return os.path.getmtime(file_path)


@contextmanager
def io_handler(file_path: str, log_error=True):
    try:
        yield
    except (IOError, OSError) as err:
        if log_error:
            logger.warning(__("error accessing file %s: %s"), file_path, err)


class KeepCitationReferences(SphinxPostTransform):
    """
    Keeps citation references as `citation_reference` nodes, which the translator renders like footnote references.
    Sphinx turns a citation reference into a `pending_xref` in the citation domain (see `CitationReferenceTransform`),
    which it would resolve into a plain reference, the same as any other link to the citation. The LaTeX builder keeps
    them the same way.
    """

    builders = ("markdown",)
    default_priority = 5  # Before `ReferencesResolver` (10)

    def run(self, **kwargs):
        citations = self.env.get_domain("citation").citations
        matcher = NodeMatcher(addnodes.pending_xref, refdomain="citation", reftype="ref")
        for node in list(self.document.findall(matcher)):
            doc_name, label_id, _ = citations.get(node.get("reftarget"), ("", "", 0))
            if doc_name:
                node.replace_self(nodes.citation_reference("", "", *node.children, docname=doc_name, refname=label_id))
