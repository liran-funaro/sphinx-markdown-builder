"""
Custom docutils translator for markdown.

See Also
========
The Docutils Document Tree:
https://docutils.sourceforge.io/docs/ref/doctree.html

reStructuredText Markup Specification/Directives:
https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html
https://docutils.sourceforge.net/docs/ref/rst/directives.html

Doctree node classes added by Sphinx:
https://www.sphinx-doc.org/en/master/extdev/nodes.html

reStructuredText Primer:
https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

HTML5 translator (example):
https://github.com/sphinx-doc/sphinx/blob/master/sphinx/writers/html5.py

Base HTML5 translator (example):
https://github.com/docutils/docutils/blob/master/docutils/docutils/writers/html5_polyglot/__init__.py
"""

import dataclasses
import posixpath
import re
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Union

from docutils import languages, nodes
from sphinx.util.docutils import SphinxTranslator
from sphinx.util.osutil import relative_uri

from sphinx_markdown_builder.contexts import (
    CommaSeparatedContext,
    ContextStatus,
    DOC_INFO_CONTEXT,
    IndentContext,
    ITALIC_CONTEXT,
    ListMarker,
    MetaContext,
    PushContext,
    STRONG_CONTEXT,
    SubContext,
    SubContextParams,
    SUBSCRIPT_CONTEXT,
    TableContext,
    TitleContext,
    UniqueString,
    WrappedContext,
    FootNoteContext,
)
from sphinx_markdown_builder.escape import escape_html_quote, escape_markdown_chars

if TYPE_CHECKING:  # pragma: no cover
    from sphinx_markdown_builder import MarkdownBuilder

VISIT_DEPART_PATTERN = re.compile("(visit|depart)_(.+)")
SKIP = UniqueString("skip")

DOC_INFO_FIELDS = "author", "contact", "copyright", "date", "organization", "revision", "status", "version"

# Defines context items, skip, or None (keep processing sub-tree).
PREDEFINED_ELEMENTS: Dict[str, Union[PushContext, UniqueString, None]] = dict(  # pylint: disable=use-dict-literal
    # Doctree elements for which Markdown element is <prefix><content><suffix>
    emphasis=ITALIC_CONTEXT,
    strong=STRONG_CONTEXT,
    subscript=SUBSCRIPT_CONTEXT,
    superscript=SUBSCRIPT_CONTEXT,
    desc_annotation=ITALIC_CONTEXT,
    literal_strong=STRONG_CONTEXT,
    literal_emphasis=ITALIC_CONTEXT,
    field_name=PushContext(WrappedContext, "**", ":**"),  # e.g 'returns', 'parameters'
    # Doc info elements
    docinfo=DOC_INFO_CONTEXT,
    docinfo_item=DOC_INFO_CONTEXT,
    **dict.fromkeys(DOC_INFO_FIELDS, DOC_INFO_CONTEXT),
    authors=None,  # not used: visit_author is called anyway for each author.
    # Doctree elements to skip subtree
    autosummary_toc=SKIP,
    nbplot_epilogue=SKIP,
    nbplot_not_rendered=SKIP,
    nbplot_container=SKIP,
    code_links=SKIP,
    index=SKIP,
    substitution_definition=SKIP,  # the doctree already contains the text with substitutions applied.
    runrole_reference=SKIP,
    toctree=SKIP,
    viewcode_anchor=SKIP,
    # Doctree elements to ignore
    document=None,
    container=None,
    inline=None,
    abbreviation=None,
    definition_list=None,
    definition_list_item=None,
    glossary=None,
    field_list_item=None,
    mpl_hint=None,
    pending_xref=None,
    compound=None,
    desc_addname=None,  # module pre-roll for class/method
    desc_content=None,  # the description of the class/method
    desc_name=None,  # name of the class/method
    title_reference=None,
    autosummary_table=None,  # Sphinx autosummary
    # See https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html.
    # Ignored table elements
    raw=None,
    tabular_col_spec=None,
    colspec=None,
    tgroup=None,
    figure=None,
    caption=None,
    desc_signature_line=None,
)


def _assign_visit_method(method, variable: str):
    match = VISIT_DEPART_PATTERN.fullmatch(method.__name__)
    assert match is not None
    state, _ = match.groups()
    assert state == "visit"
    setattr(method, variable, True)
    return method


def pushing_context(method):
    """Marks method as pushing context"""
    return _assign_visit_method(method, "__pushing_context__")


def pushing_status(method):
    """Marks method as status context"""
    return _assign_visit_method(method, "__pushing_status__")


class MarkdownTranslator(SphinxTranslator):  # pylint: disable=too-many-public-methods
    def __init__(self, document: nodes.document, builder: "MarkdownBuilder"):
        super().__init__(document, builder)
        self.builder: "MarkdownBuilder" = builder
        # noinspection PyUnresolvedReferences
        self.language = languages.get_language(self.settings.language_code, document.reporter)
        # Warn only once per writer about unsupported elements
        self._warned = set()

        # FIFO Sub context allow us to handle unique cases when post-processing is required
        self._ctx_queue: List[SubContext] = [SubContext()]
        self._doc_info: SubContext = SubContext()
        self._status_queue: List[ContextStatus] = [ContextStatus()]

        if self.config.markdown_docinfo:
            self._add_doc_info_from_config()

    def _add_doc_info_from_config(self):
        for key in DOC_INFO_FIELDS:
            value = getattr(self.config, key, "")
            if isinstance(value, str):
                self._push_context(MetaContext(key))
                self.ctx.add(value)
                self._pop_context()

    @property
    def ctx(self) -> SubContext:
        return self._ctx_queue[-1]

    def _push_context(self, ctx: SubContext):
        self._ctx_queue.append(ctx)

    def _title_level(self, base_level: int) -> int:
        offset = int(getattr(self.builder, "heading_level_offset", 0))
        return min(6, max(1, base_level + offset))

    def _title_breaker(self) -> str:
        if self.config.markdown_flavor == "llm":
            return " "
        return "<br/>"

    def _table_cell_breaker(self) -> str:
        if self.config.markdown_flavor == "llm":
            return " "
        return "<br/>"

    def _pop_context(self, _node=None, count=1):
        for _ in range(count):
            if len(self._ctx_queue) <= 1:
                break

            last_ctx = self._ctx_queue.pop()
            ctx = self.ctx if last_ctx.params.target == "body" else self._doc_info
            ctx.add(last_ctx.make(), last_ctx.params.prefix_eol, last_ctx.params.suffix_eol)

    def _push_box(self, title: str):
        level = self._title_level(4)
        self.add(f"{'#' * level} {title}", prefix_eol=2)
        self._push_context(SubContext(SubContextParams(1, 2)))

    def _push_admonition(self, title: str):
        level = self._title_level(5)
        self._push_context(IndentContext("> ", empty=True, params=SubContextParams(1, 2)))
        self.add(f"{'#' * level} {title}", prefix_eol=1, suffix_eol=1)

    @property
    def status(self) -> ContextStatus:
        return self._status_queue[-1]

    def _push_status(self, **changes):
        cur_status = self.status
        self._status_queue.append(dataclasses.replace(cur_status, **changes))

    def _pop_status(self, _node=None, count=1):
        count = min(len(self._status_queue) - 1, count)
        self._status_queue = self._status_queue[:-count]

    def _pop_context_and_status(self, node=None):
        self._pop_context(node)
        self._pop_status(node)

    def astext(self):
        """Return the final formatted document as a string."""
        self._pop_context(count=2**31)
        assert len(self._ctx_queue) == 1

        ctx = SubContext()
        for sub_ctx in (self._doc_info, self._ctx_queue[0]):
            ctx.add(sub_ctx.make().strip(), prefix_eol=2, suffix_eol=1)
        ctx.force_eol(1)
        return ctx.make()

    def add(self, value: str, prefix_eol: int = 0, suffix_eol: int = 0):
        """See `SubContext.add()`"""
        self.ctx.add(value, prefix_eol, suffix_eol)

    def ensure_eol(self, count=1):
        """Ensure the last line in current base is terminated by X new lines."""
        self.ctx.ensure_eol(count)

    def _pass(self, _node=None):
        pass

    def _skip(self, _node=None):
        raise nodes.SkipNode

    def _has_attr(self, item):
        try:
            super().__getattribute__(item)
            return True
        except AttributeError:
            return False

    def _get_attr(self, item, default=None):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return default

    def __getattribute__(self, item):
        """Uses some predefined rules to reduce the visit/depart method clutter in the class"""
        try:
            # First try to get an existing attribute
            return super().__getattribute__(item)
        except AttributeError as ex:
            predefined_method = self._find_predefined_method(item)
            if predefined_method is not None:
                return predefined_method
            raise ex

    def _find_predefined_action(self, state: str, element: str):
        action = PREDEFINED_ELEMENTS.get(element, "__undefined__")
        if action is None:
            return self._pass
        if action is SKIP:
            return self._skip
        if isinstance(action, PushContext):
            if state == "visit":
                return lambda node: self._push_context(action.create(node, element))
            return self._pop_context
        return None

    def _find_pushing_method(self, state: str, element: str):
        if state != "depart":
            return None

        # If the visit method is marked as pushing, then pop the context/status
        visit_method = self._get_attr(f"visit_{element}", None)
        is_pushing_ctx = getattr(visit_method, "__pushing_context__", False)
        is_pushing_status = getattr(visit_method, "__pushing_status__", False)
        if is_pushing_ctx and is_pushing_status:
            return self._pop_context_and_status
        if is_pushing_ctx:
            return self._pop_context
        if is_pushing_status:
            return self._pop_status
        return None

    def _is_element_defined(self, element: str):
        return self._has_attr(f"visit_{element}") or self._has_attr(f"depart_{element}")

    def _find_predefined_method(self, item) -> Optional[Callable]:  # pylint: disable=too-many-return-statements
        match = VISIT_DEPART_PATTERN.fullmatch(item)
        if match is None:
            # We only care about visit/depart methods
            return None
        state, element = match.groups()

        method = self._find_predefined_action(state, element)
        if method is not None:
            return method

        method = self._find_pushing_method(state, element)
        if method is not None:
            return method

        # If one of the handlers is defined, automatically add the other as an empty handler
        if self._is_element_defined(element):
            return self._pass

        return None

    def unknown_visit(self, node):
        """Warn once per instance for unsupported nodes."""
        node_type = node.__class__.__name__
        if node_type not in self._warned:
            super().unknown_visit(node)
            self._warned.add(node_type)
        raise nodes.SkipNode

    ################################################################################
    # visit/depart handlers
    ################################################################################

    @pushing_context
    def visit_important(self, _node):
        """Sphinx important directive."""
        self._push_admonition("IMPORTANT")

    @pushing_context
    def visit_warning(self, _node):
        """Sphinx warning directive."""
        self._push_admonition("WARNING")

    @pushing_context
    def visit_caution(self, _node):
        self._push_admonition("CAUTION")

    @pushing_context
    def visit_note(self, _node):
        """Sphinx note directive."""
        self._push_admonition("NOTE")

    @pushing_context
    def visit_seealso(self, _node):
        """Sphinx see also directive."""
        self._push_admonition("SEE ALSO")

    @pushing_context
    def visit_attention(self, _node):
        self._push_admonition("ATTENTION")

    @pushing_context
    def visit_hint(self, _node):
        """Sphinx hint directive."""
        self._push_admonition("HINT")

    @pushing_context
    def visit_tip(self, _node):
        """Sphinx tip directive."""
        self._push_admonition("TIP")

    @pushing_context
    def visit_danger(self, _node):
        """Sphinx danger directive."""
        self._push_admonition("DANGER")

    @pushing_context
    def visit_error(self, _node):
        """Sphinx error directive."""
        self._push_admonition("ERROR")

    def visit_image(self, node):
        """Image directive."""
        uri = node["uri"]
        alt = node.attributes.get("alt", "image")
        # We don't need to add EOL before/after the image.
        # It will be handled by the visit/depart handlers of the paragraph.
        self.add(f"![{alt}]({uri})")

    # noinspection PyPep8Naming
    def visit_Text(self, node):  # pylint: disable=invalid-name
        text = node.astext().replace("\r", "")
        # Replace line breaks with spaces to create single-line paragraphs
        if self.config.markdown_flavor == "github" and not self.status.preserve_line_breaks:
            text = text.replace("\n", " ")
        if self.status.escape_text:
            text = escape_markdown_chars(text)
        self.add(text)

    @pushing_context
    @pushing_status
    def visit_comment(self, _node):
        self._push_status(escape_text=False)
        self._push_context(WrappedContext("<!-- ", " -->", params=SubContextParams(1)))

    @pushing_context
    def visit_paragraph(self, _node):
        if self.status.list_marker is None:
            params = SubContextParams(2, 2)
        else:
            # Full paragraph spacing inside a list might trigger redundant spacing for some markdown compilers.
            # So we will add double EOL after the paragraph only if the next element requires it (e.g., code block).
            params = SubContextParams(2, 1)
        self._push_context(SubContext(params))

    visit_compact_paragraph = visit_paragraph

    ################################################################################
    # Line block
    ################################################################################
    # line_block
    #   line
    #   line
    #   line
    ################################################################################

    @pushing_context
    def visit_line_block(self, _node):
        self._push_context(SubContext(SubContextParams(1, 1)))

    @pushing_context
    def visit_line(self, _node):
        self._push_context(SubContext(SubContextParams(1, 1)))

    def depart_line(self, _node):
        self._pop_context()
        if self.config.markdown_flavor == "llm":
            return
        self.add("<br/>", prefix_eol=1, suffix_eol=1)

    ################################################################################
    # Definition / Glossaries
    # A definition_list can be outside a glossary. In which case, the term won't
    # have IDs, thus not having anchors.
    ################################################################################
    # glossary
    #   definition_list
    #     definition_list_item
    #       term
    #         index entries
    #       definition
    #         paragraph
    ################################################################################

    def visit_term(self, node):
        self.ensure_eol(2)
        for anchor in node.get("ids", []):
            self._add_anchor(anchor)
        self.ensure_eol(2)

    @pushing_context
    def visit_definition(self, _node):
        self._push_context(
            IndentContext(": ", only_first=True, support_multi_line_break=True, params=SubContextParams(1, 2))
        )

    def visit_math_block(self, _node):
        """docutils math block"""
        self._push_status(escape_text=False, preserve_line_breaks=True)
        self.add("$$", prefix_eol=1, suffix_eol=1)

    def depart_math_block(self, _node):
        """docutils math block"""
        self.add("$$", prefix_eol=1, suffix_eol=2)
        self._pop_status()

    def visit_math(self, _node):
        """docutils math node"""
        self._push_status(escape_text=False)
        self.add("$")

    def depart_math(self, _node):
        """docutils math node"""
        self.add("$")
        self._pop_status()

    def visit_literal(self, _node):
        self._push_status(escape_text=False)
        self.add("`")

    def depart_literal(self, _node):
        self.add("`")
        self._pop_status()

    def visit_literal_block(self, node):
        self._push_status(escape_text=False, preserve_line_breaks=True)
        code_type = ""
        classes = node.get("classes", [])
        if "code" in classes:
            code_idx = classes.index("code") + 1
            if code_idx < len(classes):
                code_type = classes[code_idx]
        if "language" in node:
            code_type = node["language"]
        elif self.status.code_language:
            code_type = self.status.code_language
        if code_type == "default":
            code_type = ""
        self.add(f"```{code_type}", prefix_eol=1, suffix_eol=1)

    def depart_literal_block(self, _node):
        self.add("```", prefix_eol=1, suffix_eol=2)
        self._pop_status()

    def visit_doctest_block(self, _node):
        self._push_status(escape_text=False, preserve_line_breaks=True)
        self.add("```pycon", prefix_eol=1, suffix_eol=1)

    depart_doctest_block = depart_literal_block

    @pushing_context
    def visit_block_quote(self, _node):
        self._push_context(IndentContext("> "))

    def visit_problematic(self, node):
        self.add(f"```\n{node.astext()}\n```", prefix_eol=2, suffix_eol=2)
        raise nodes.SkipNode

    @pushing_status
    def visit_section(self, node):
        self.ensure_eol(2)
        if self.config.markdown_anchor_sections:
            for anchor in node.get("ids", []):
                self._add_anchor(anchor)

        self._push_status(section_level=self.status.section_level + 1)

    @pushing_context
    def visit_title(self, _node):
        if isinstance(self.ctx, TableContext):
            level = 4
        else:
            level = self.status.section_level
        self._push_context(TitleContext(self._title_level(level), breaker=self._title_breaker()))

    @pushing_context
    @pushing_status
    def visit_subtitle(self, _node):  # pragma: no cover
        """
        Docutils does not promote subtitles, so this might never be called.
        However, we keep it here in case some future version will change this behaviour.
        """
        self._push_status(section_level=self.status.section_level + 1)
        self._push_context(TitleContext(self._title_level(self.status.section_level), breaker=self._title_breaker()))

    @pushing_context
    def visit_rubric(self, _node):
        """Sphinx Rubric, a heading without relation to the document sectioning"""
        self._push_context(TitleContext(self._title_level(3), breaker=self._title_breaker()))

    def visit_transition(self, _node):
        """Simply replace a transition by a horizontal rule."""
        # Can use three or more '*', '_' or '-'.
        self.add("---", prefix_eol=2, suffix_eol=1)
        raise nodes.SkipNode

    def visit_only(self, node):
        expr = node.get("expr", "")
        tags = getattr(self.builder, "tags", None)
        if not expr or tags is None:
            return
        if not tags.eval_condition(expr):
            raise nodes.SkipNode

    def _adjust_url(self, url: str):
        """Replace `refuri` in reference with HTTP address, if possible"""
        if not self.config.markdown_http_base:
            return url

        # If HTTP page build URL known, make link relative to that.
        this_doc = self.builder.current_doc_name
        if url == "":  # Reference to this doc
            url = self.builder.get_target_uri(this_doc)
        else:  # URL is relative to the current docname.
            this_dir = posixpath.dirname(this_doc)
            if this_dir:
                url = posixpath.normpath(f"{this_dir}/{url}")
        return f"{self.config.markdown_http_base}/{url}"

    def _fetch_ref_uri(self, node):
        uri = node.get("refuri", "")

        # Do not modify external URL in any way
        if not node.get("internal", self.status.default_ref_internal):
            return uri

        uri = self._adjust_url(uri)

        # Whatever the URL is, add the anchor to it
        ref_id = node.get("refid", None)
        if ref_id is not None:
            uri = f"#{ref_id}"

        return uri

    @pushing_context
    def visit_reference(self, node):
        # If this reference was already moved into a card title, skip it.
        if node.get("md_moved_to_title", False):
            raise nodes.SkipNode

        is_internal = bool(node.get("internal", self.status.default_ref_internal))
        is_llm = self.config.markdown_flavor == "llm"
        is_single = getattr(self.builder, "name", "") == "singlemarkdown"
        if is_llm and is_single and is_internal:
            self._push_context(WrappedContext("", ""))
            return

        url = self._fetch_ref_uri(node)
        self._push_context(WrappedContext("[", f"]({url})"))

    def visit_pending_xref(self, node):
        # Keep default behavior (child text passes through), unless this node
        # was already moved into a card title link.
        if node.get("md_moved_to_title", False):
            raise nodes.SkipNode

    @pushing_context
    def visit_download_reference(self, node):
        # Sphinx sets `refuri` for external targets; preserve those URLs verbatim.
        if "refuri" in node:
            target = node["refuri"]
        # For readable internal targets, `filename` is the registered, hashed
        # destination. Link to the copied file relative to the current output page.
        elif "filename" in node:
            target = relative_uri(
                self.builder.get_target_uri(self.builder.current_doc_name),
                posixpath.join(self.builder.download_dir, node["filename"]),
            )
            target = self._adjust_url(target)
        # If Sphinx could not register the internal file, only its original
        # `reftarget` remains; retain the previous URL-adjustment fallback.
        else:
            target = self._adjust_url(node.get("reftarget", ""))
        self._push_context(WrappedContext("[", f"]({target})"))

    def _add_anchor(self, anchor: str):
        if self.config.markdown_flavor == "llm":
            return
        content = f'<a id="{escape_html_quote(anchor)}"></a>'
        # Prevent adding the same anchor twice in the same context
        if content not in self.ctx.content:
            self.add(content, prefix_eol=2, suffix_eol=1)

    def visit_target(self, node):
        ref_id = node.get("refid", None)
        if ref_id is None:
            return
        self._add_anchor(ref_id)

    @pushing_context
    @pushing_status
    def visit_topic(self, _node):
        self._push_status(default_ref_internal=True, section_level=5)
        self._push_context(IndentContext("> ", empty=True))

    def visit_container(self, node):
        """Handle generic container nodes and special-case sphinx-design cards.

        We push a blockquote context for top-level sphinx-design cards (class
        `sd-card`) so their contents are rendered as a Markdown blockquote. We
        also special-case containers with class `sd-card-title` to render the
        title as a linked level-4 heading inside the blockquote.
        """
        classes = node.attributes.get("classes", []) or []

        # Handle sphinx-design card containers and titles using small helpers
        # to keep this method simple and under the complexity threshold.
        if "sd-card" in classes:
            self._handle_sd_card(node)
            return

        if "sd-card-title" in classes:
            self._handle_sd_card_title(node)
            return

    def _handle_sd_card(self, node):
        # Ensure an extra blank line after the card so adjacent cards don't
        # merge into the same blockquote in Markdown output.
        self._push_context(IndentContext("> ", empty=True, params=SubContextParams(1, 2)))
        # mark the node so depart_container knows to pop
        # Store a marker in the node attributes when possible so downstream
        # handlers can detect that we pushed a card context. Use the node
        # attribute mapping if available to avoid touching protected members.
        if hasattr(node, "attributes") and isinstance(node.attributes, dict):
            node["md_card_pushed"] = True

    def _find_card_container(self, node):
        container = node
        while container is not None and "sd-card" not in (container.attributes.get("classes", []) or []):
            container = getattr(container, "parent", None)
        return container

    def _find_stretched_link(self, container):
        if container is None:
            return None
        for child in container.traverse():
            child_classes = child.attributes.get("classes", []) if hasattr(child, "attributes") else []
            if "sd-stretched-link" in child_classes:
                return child
        return None

    def _href_from_link_node(self, link_node):
        if link_node is None:
            return None
        if isinstance(link_node, nodes.reference):
            try:
                return self._fetch_ref_uri(link_node)
            except (AttributeError, KeyError, TypeError):
                return ""
        return link_node.get("refuri") or link_node.get("reftarget") or ""

    def _normalize_card_href(self, href: Optional[str]) -> Optional[str]:
        if not href:
            return href
        if href.endswith(".html"):
            return href[:-5] + (self.config.markdown_uri_doc_suffix or ".md")
        is_http = href.startswith("http://") or href.startswith("https://")
        if not (is_http or href.endswith(self.config.markdown_uri_doc_suffix)):
            return href + (self.config.markdown_uri_doc_suffix or ".md")
        return href

    def _handle_sd_card_title(self, node):
        container = self._find_card_container(node)
        link_node = self._find_stretched_link(container)

        title = node.astext().strip()
        level = self._title_level(4)

        href = self._href_from_link_node(link_node)
        if link_node is not None:
            if hasattr(link_node, "attributes") and isinstance(link_node.attributes, dict):
                link_node["md_moved_to_title"] = True

        href = self._normalize_card_href(href)

        if self.status.escape_text:
            title = escape_markdown_chars(title)

        is_llm = self.config.markdown_flavor == "llm"
        is_singlemarkdown = getattr(self.builder, "name", "") == "singlemarkdown"
        is_internal_href = href and not (href.startswith("http://") or href.startswith("https://"))

        if is_llm and is_singlemarkdown and is_internal_href:
            self.add(f"{('#' * level)} {title}", prefix_eol=1, suffix_eol=1)
        elif href:
            self.add(f"{('#' * level)} [{title}]({href})", prefix_eol=1, suffix_eol=1)
        else:
            self.add(f"{('#' * level)} {title}", prefix_eol=1, suffix_eol=1)

        raise nodes.SkipNode

    def depart_container(self, node):
        # If we marked the node as having pushed a card context, pop it now.
        if node.get("md_card_pushed", False):
            if len(self._ctx_queue) > 1:
                self._pop_context(node)

    ################################################################################
    # lists
    ################################################################################
    # enumerated_list/bullet_list
    #     list_item
    #       paragraph (optional)
    ###############################################################################

    def _start_list(self, marker: Union[int, str]):
        self.ensure_eol()
        if isinstance(marker, str) and marker[-1] != " ":
            marker += " "
        self._push_status(list_marker=ListMarker(marker))

    def _end_list(self, _node=None):
        self._pop_status()
        # We need two line breaks to make sure the next paragraph will not merge into the list
        self.ensure_eol(2)

    def _start_list_item(self, _node=None):
        marker = self.status.list_marker
        marker.inc()
        self._push_context(IndentContext(marker, only_first=True, params=SubContextParams(1, 1)))

    _end_list_item = _pop_context

    def visit_enumerated_list(self, _node):
        self._start_list(0)

    depart_enumerated_list = _end_list

    def visit_bullet_list(self, node):
        self._start_list(node.attributes.get("bullet", self.config.markdown_bullet))

    depart_bullet_list = _end_list
    visit_list_item = _start_list_item
    depart_list_item = _end_list_item

    ################################################################################
    # option lists
    ################################################################################
    # option_list
    #   option_list_item
    #     option_group
    #     description
    ###############################################################################

    def visit_option_list(self, _node):
        self._start_list("*")

    depart_option_list = _end_list
    visit_option_list_item = _start_list_item
    depart_option_list_item = _end_list_item

    def visit_option_group(self, node):
        self.add(f"`{escape_markdown_chars(node.astext())}`", suffix_eol=1)
        raise nodes.SkipNode

    def visit_description(self, _node):
        pass

    depart_description = _pass

    ################################################################################
    # desc
    ################################################################################
    # desc (desctype: {function, class, method, etc.)
    #   desc_signature
    #     desc_signature_line (optional nesting)
    #         desc_name
    #           desc_annotation (optional)
    #         desc_parameterlist
    #           desc_annotation
    #           desc_parameter
    #         desc_returns
    #   desc_content
    #     field_list
    #       field
    #         field_name (e.g 'returns/parameters/raises')
    #         field_body
    ################################################################################

    @pushing_status
    def visit_desc(self, node):
        self._push_status(desc_type=node.attributes.get("desctype", ""))

    @pushing_context
    def visit_desc_signature(self, node):
        """the main signature of class/method"""

        # Insert anchors if enabled by the config
        if self.config.markdown_anchor_signatures:
            for anchor in node.get("ids", []):
                self._add_anchor(anchor)

        # We don't want methods to be at the same level as classes,
        # If signature has a non-null class, that's means it is a signature
        # of a class method
        h_level = 4 if node.get("class", None) else 3
        self._push_context(TitleContext(self._title_level(h_level)))

    def visit_desc_parameterlist(self, _node):
        self._push_context(WrappedContext("(", ")", wrap_empty=True))
        self._push_context(CommaSeparatedContext(", "))

    def depart_desc_parameterlist(self, _node):
        self._pop_context(count=2)

    @property
    def sep_ctx(self) -> Optional[CommaSeparatedContext]:
        for ctx in reversed(self._ctx_queue):
            if isinstance(ctx, CommaSeparatedContext):
                return ctx
        return None

    def visit_desc_parameter(self, _node):
        """single method/class ctr param"""
        sep_ctx = self.sep_ctx
        if sep_ctx is not None:
            sep_ctx.enter_parameter()  # workaround pylint: disable=no-member

    def depart_desc_parameter(self, _node):
        sep_ctx = self.sep_ctx
        if sep_ctx is not None:
            sep_ctx.exit_parameter()  # workaround pylint: disable=no-member

    @pushing_context
    def visit_desc_optional(self, _node):
        self._push_context(WrappedContext("[", "]"))

    def visit_field_list(self, _node):
        self._start_list("*")

    depart_field_list = _end_list
    visit_field = _start_list_item
    depart_field = _end_list_item

    def visit_desc_returns(self, _node):
        self.add(" → ")

    @pushing_context
    def visit_field_body(self, _node):
        self._push_context(SubContext(SubContextParams(1, 1)))

    @pushing_context
    def visit_versionmodified(self, node):
        """
        Node for version change entries.
        Currently used for “versionadded”, “versionchanged” and “deprecated” directives.
        Type will hold something like 'deprecated'
        """
        node_type = node.attributes["type"].capitalize()
        self._push_box(node_type)

    def visit_highlightlang(self, node):
        """Apply default language for subsequent literal blocks."""
        lang = node.get("lang", "")
        self._status_queue[-1] = dataclasses.replace(self.status, code_language=lang)

    ################################################################################
    # tables
    ################################################################################
    # table
    #   tgroup [cols=x]
    #     colspec
    #     thead
    #       row
    #         entry
    #           paragraph (optional)
    #     tbody
    #       row
    #         entry
    #           paragraph (optional)
    ###############################################################################

    @property
    def table_ctx(self) -> TableContext:
        ctx = self.ctx
        assert isinstance(ctx, TableContext)
        return ctx

    @pushing_context
    def visit_table(self, _node):
        self._push_context(TableContext(params=SubContextParams(2, 1), cell_breaker=self._table_cell_breaker()))

    def visit_thead(self, _node):
        self.table_ctx.enter_head()  # workaround pylint: disable=no-member

    def depart_thead(self, _node):
        self.table_ctx.exit_head()  # workaround pylint: disable=no-member

    def visit_tbody(self, _node):
        self.table_ctx.enter_body()  # workaround pylint: disable=no-member

    def depart_tbody(self, _node):
        self.table_ctx.exit_body()  # workaround pylint: disable=no-member

    def visit_row(self, _node):
        self.table_ctx.enter_row()  # workaround pylint: disable=no-member

    def depart_row(self, _node):
        self.table_ctx.exit_row()  # workaround pylint: disable=no-member

    def visit_entry(self, _node):
        self.table_ctx.enter_entry()  # workaround pylint: disable=no-member

    def depart_entry(self, _node):
        self.table_ctx.exit_entry()  # workaround pylint: disable=no-member

    ################################################################################
    # footnote
    ################################################################################
    # footnote_reference
    # ...
    # footnote
    #   label
    #   paragraph
    ###############################################################################

    @property
    def footnote_ctx(self) -> FootNoteContext:
        ctx = self.ctx
        assert isinstance(ctx, FootNoteContext)
        return ctx

    @pushing_context
    def visit_footnote_reference(self, _node):
        # https://www.markdownguide.org/extended-syntax/#footnotes
        self._push_context(WrappedContext("[^", "]"))

    @pushing_context
    def visit_footnote(self, node):
        ids = node.get("ids", "")
        if isinstance(ids, (list, tuple)):
            ids = ",".join(ids)
        names = node.get("names", "")
        if isinstance(names, (list, tuple)):
            names = ",".join(names)
        # https://www.markdownguide.org/extended-syntax/#footnotes
        self._push_context(FootNoteContext(ids, names, params=SubContextParams(1, 1)))

    def visit_label(self, node):
        try:
            self.footnote_ctx.visit_label()  # workaround pylint: disable=no-member
        except AssertionError:
            self.unknown_visit(node)

    def depart_label(self, node):
        try:
            self.footnote_ctx.depart_label()  # workaround pylint: disable=no-member
        except AssertionError:
            self.unknown_visit(node)
