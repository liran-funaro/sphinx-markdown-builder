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
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Type, Union

from docutils import languages, nodes
from sphinx.util.docutils import SphinxTranslator
from sphinx.util.osutil import relative_uri

from sphinx_markdown_builder import contexts, escape

if TYPE_CHECKING:  # pragma: no cover
    from sphinx_markdown_builder import MarkdownBuilder

VISIT_DEPART_PATTERN = re.compile("(visit|depart)_(.+)")
SKIP = contexts.UniqueString("skip")

DOC_INFO_FIELDS = "author", "contact", "copyright", "date", "organization", "revision", "status", "version"

# Defines context items, skip, or None (keep processing sub-tree).
PREDEFINED_ELEMENTS: Dict[str, Union[contexts.PushContext, contexts.PushBox, contexts.UniqueString, None]] = (
    dict(  # pylint: disable=use-dict-literal
        # Doctree elements for which Markdown element is <prefix><content><suffix>
        emphasis=contexts.ITALIC,
        strong=contexts.STRONG,
        subscript=contexts.SUBSCRIPT,
        superscript=contexts.SUBSCRIPT,
        desc_annotation=contexts.ITALIC,
        literal_strong=contexts.STRONG,
        literal_emphasis=contexts.ITALIC,
        # Doc info elements
        docinfo=contexts.DOC_INFO,
        docinfo_item=contexts.DOC_INFO,
        **dict.fromkeys(DOC_INFO_FIELDS, contexts.DOC_INFO),
        authors=None,  # not used: visit_author is called anyway for each author.
        # Admonitions
        important=contexts.PushBox("IMPORTANT"),
        warning=contexts.PushBox("WARNING"),
        note=contexts.PushBox("NOTE"),
        seealso=contexts.PushBox("NOTE", "See also"),
        attention=contexts.PushBox("IMPORTANT"),
        hint=contexts.PushBox("TIP"),
        tip=contexts.PushBox("TIP"),
        caution=contexts.PushBox("CAUTION"),
        danger=contexts.PushBox("CAUTION"),
        error=contexts.PushBox("CAUTION"),
        admonition=contexts.PushBox("NOTE"),
        sidebar=contexts.PushBox("TIP"),
        versionmodified=contexts.PushBox("WARNING"),  # “versionadded”, “versionchanged” and “deprecated” directives.
        # Doctree elements to skip subtree
        autosummary_toc=SKIP,
        nbplot_epilogue=SKIP,
        nbplot_not_rendered=SKIP,
        nbplot_container=SKIP,
        code_links=SKIP,
        index=SKIP,
        substitution_definition=SKIP,  # the doctree already contains the text with substitutions applied.
        runrole_reference=SKIP,
        # Doctree elements to ignore
        document=None,
        container=None,
        inline=None,
        abbreviation=None,  # e.g., the keyword-only '*' in signatures
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
        tabular_col_spec=None,
        colspec=None,
        tgroup=None,
        figure=None,
        legend=None,
        desc_signature_line=None,
    )
)


def pushing_context(method):
    """Marks method as pushing context"""
    return _assign_visit_method(method, "__pushing_context__", 1)


def pushing_multi_context(count):
    """Marks method as pushing multiple context"""
    return lambda method: _assign_visit_method(method, "__pushing_context__", count)


def pushing_status(method):
    """Marks method as status context"""
    return _assign_visit_method(method, "__pushing_status__", True)


def _assign_visit_method(method, variable: str, value):
    match = VISIT_DEPART_PATTERN.fullmatch(method.__name__)
    assert match is not None
    state, _ = match.groups()
    assert state == "visit"
    setattr(method, variable, value)
    return method


class UnknownVisit(Exception):
    """A visit/depart handler met a node outside the context it supports (e.g., a `label` outside a footnote)."""


class MarkdownTranslator(SphinxTranslator):  # pylint: disable=too-many-public-methods
    ################################################################################
    # Core methods
    ################################################################################

    def __init__(self, document: nodes.document, builder: "MarkdownBuilder"):
        super().__init__(document, builder)
        self.builder: "MarkdownBuilder" = builder
        self.language = languages.get_language(self.settings.language_code, document.reporter)
        # Warn only once per writer about unsupported elements
        self._warned = set()

        # A stack of nested contexts. Output goes to the last one, which renders into its parent when popped.
        self._ctx_queue: List[contexts.Base] = [contexts.Base()]
        self._doc_info: contexts.Base = contexts.Base()
        self._status_queue: List[contexts.Status] = [contexts.Status()]

        if self.config.markdown_docinfo:
            for key in DOC_INFO_FIELDS:
                value = getattr(self.config, key, "")
                if isinstance(value, str):
                    self._push_context(contexts.Meta(key))
                    self.ctx.add(value)
                    self._pop_context()

    @property
    def ctx(self) -> contexts.Base:
        return self._ctx_queue[-1]

    def _typed_ctx(self, ctx_type: Type[contexts.BaseT]) -> contexts.BaseT:
        """The current context, if it is of the type the visited node requires"""
        ctx = self.ctx
        if isinstance(ctx, ctx_type):
            return ctx
        raise UnknownVisit

    def _push_context(self, ctx: contexts.Base):
        key = ctx.nesting_key
        if key is not None and any(outer.nesting_key == key for outer in self._ctx_queue):
            # It doesn't nest (see `contexts.Base.nesting_key`), so its content joins the open context.
            ctx = contexts.Base()
        self._ctx_queue.append(ctx)

    def _pop_context(self, _node=None, count=1):
        for _ in range(count):
            if len(self._ctx_queue) <= 1:
                break

            last_ctx = self._ctx_queue.pop()
            ctx = self.ctx if last_ctx.params.target == "body" else self._doc_info
            ctx.add(last_ctx.make(), last_ctx.params)

    @property
    def status(self) -> contexts.Status:
        return self._status_queue[-1]

    def _push_status(self, **changes):
        cur_status = self.status
        self._status_queue.append(dataclasses.replace(cur_status, **changes))

    def _pop_status(self, _node=None, count=1):
        count = min(len(self._status_queue) - 1, count)
        self._status_queue = self._status_queue[:-count]

    def add(self, value: str, spacing: contexts.Spacing = contexts.Spacing(), **kwargs):
        """
        See `contexts.Base.add()`

        Other Parameters
        ----------------
        prefix_eol : int
        suffix_eol : int
        prefix_chars : str
        suffix_chars : str
        prefix_mark : str
        suffix_mark : str
        """
        self.ctx.add(value, spacing, **kwargs)

    def ensure_eol(self, count=1):
        """Ensure the last line in current base is terminated by X new lines."""
        self.ctx.ensure_eol(count)

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

    def _find_predefined_method(self, item) -> Optional[Callable]:
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
            return _pass

        return None

    def _find_predefined_action(self, state: str, element: str):  # pylint: disable=too-many-return-statements
        action = PREDEFINED_ELEMENTS.get(element, "__undefined__")
        if action is None:
            return _pass
        if action is SKIP:
            return _skip
        if isinstance(action, contexts.PushContext):
            if state == "visit":
                create = action.create
                return lambda node: self._push_context(create(node, element))
            return self._pop_context
        if isinstance(action, contexts.PushBox):
            if state == "visit":
                title, heading = action.title, action.heading
                return lambda node: self._push_box(title, heading)
            return self._pop_context_and_status
        return None

    def _push_box(self, title: str, heading: str | None = None):
        self.add(f"> [!{title}]")
        self._push_context(contexts.Indent(prefix="> ", empty=True, params=contexts.BaseParams(1, 2)))
        self._push_status(section_level=3)
        if heading is not None:
            self.add(f"### {heading}")

    def _pop_context_and_status(self, node=None, count=1):
        self._pop_context(node, count=count)
        self._pop_status(node)

    def _find_pushing_method(self, state: str, element: str):
        if state != "depart":
            return None

        # If the visit method is marked as pushing, then pop the context/status
        visit_method = self._get_attr(f"visit_{element}", None)
        pushing_ctx_count = getattr(visit_method, "__pushing_context__", 0)
        is_pushing_status = getattr(visit_method, "__pushing_status__", False)
        if pushing_ctx_count and is_pushing_status:
            return lambda node: self._pop_context_and_status(node, count=pushing_ctx_count)
        if pushing_ctx_count:
            return lambda node: self._pop_context(node, count=pushing_ctx_count)
        if is_pushing_status:
            return self._pop_status
        return None

    def _get_attr(self, item, default=None):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return default

    def _is_element_defined(self, element: str):
        return self._has_attr(f"visit_{element}") or self._has_attr(f"depart_{element}")

    def _has_attr(self, item):
        try:
            super().__getattribute__(item)
            return True
        except AttributeError:
            return False

    ################################################################################
    # Override translator API
    ################################################################################

    def astext(self):
        """Return the final formatted document as a string."""
        self._pop_context(count=2**31)
        assert len(self._ctx_queue) == 1

        ctx = contexts.Base()
        for sub_ctx in (self._doc_info, self._ctx_queue[0]):
            ctx.add(sub_ctx.make().strip(), prefix_eol=2, suffix_eol=1)
        ctx.force_eol(1)
        return ctx.make()

    def dispatch_visit(self, node):
        # A handler raises UnknownVisit when the node is outside the context it supports.
        # unknown_visit() then raises SkipNode, so the node's children and departure are skipped too.
        try:
            super().dispatch_visit(node)
        except UnknownVisit:
            self.unknown_visit(node)

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

    def visit_image(self, node):
        """Image directive."""
        uri = escape.link_destination(node["uri"])
        alt = escape.alt_text(node.attributes.get("alt", "image"))
        # We don't need to add EOL before/after the image.
        # It will be handled by the visit/depart handlers of the paragraph.
        self.add(f"![{alt}]({uri})")

    @pushing_context
    def visit_caption(self, node):
        """Figure caption."""
        self._push_context(contexts.Wrapped("*", params=contexts.BaseParams(2, 2)))

    def visit_Text(self, node):  # pylint: disable=invalid-name
        text = node.astext().replace("\r", "")
        # Replace line breaks with spaces to create single-line paragraphs
        if self.config.markdown_flavor == "github" and not self.status.preserve_line_breaks:
            text = text.replace("\n", " ")
        if self.status.escape_text:
            text = escape.markdown_chars(text)
        self.add(text)

    @pushing_context
    @pushing_status
    def visit_raw(self, node):
        # `format` holds one or more space-separated output formats (e.g., "html" or "html latex").
        include = {raw_type.lower() for raw_type in self.config.markdown_include_raw_types}
        if not include.intersection(node["format"].lower().split()):
            raise nodes.SkipNode  # Nothing was pushed yet, and SkipNode also skips the departure.
        # The content is written verbatim by `visit_Text`.
        self._push_status(escape_text=False, preserve_line_breaks=True)
        # The raw directive and the raw role both make a `raw` node, so its parent tells them apart (as in docutils'
        # HTML writer). A raw role is inside a text element (e.g., a paragraph): EOLs would split it, so add none.
        # A raw directive is a block of its own: separate it from its neighbors, which may be other raw blocks.
        eol = 0 if isinstance(node.parent, nodes.TextElement) else 2
        self._push_context(contexts.Base(contexts.BaseParams(eol, eol)))

    @pushing_context
    @pushing_status
    def visit_comment(self, node):
        if self.config.markdown_suppress_comments:
            raise nodes.SkipNode  # Nothing was pushed yet, and SkipNode also skips the departure.
        self._push_status(escape_text=False)
        self._push_context(contexts.Comment(contexts.BaseParams(1)))

    @pushing_context
    def visit_paragraph(self, node):
        if self.status.list_marker is None:
            params = contexts.BaseParams(2, 2)
        else:
            # Full paragraph spacing inside a list might trigger redundant spacing for some markdown compilers.
            # So we will add double EOL after the paragraph only if the next element requires it (e.g., code block).
            params = contexts.BaseParams(2, 1)
        self._push_context(contexts.Base(params))

    visit_compact_paragraph = visit_paragraph
    # sphinx-design cards wrap their title and link in this node, outside any paragraph:
    # container(card) > container(card-body) > container(card-title) > PassthroughTextElement (the title),
    # and container(card) > PassthroughTextElement > reference (the card link).
    visit_PassthroughTextElement = visit_paragraph

    ################################################################################
    # Line block
    ################################################################################
    # line_block
    #   line
    #   line
    #   line
    ################################################################################

    @pushing_context
    def visit_line_block(self, node):
        self._push_context(contexts.Base(contexts.BaseParams(1, 1)))

    @pushing_context
    def visit_line(self, node):
        self._push_context(contexts.Base(contexts.BaseParams(1, 1)))

    def depart_line(self, node):
        self._pop_context()
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
    #       classifier (optional, repeatable; e.g., "term : type")
    #       definition
    #         paragraph
    ################################################################################

    def visit_term(self, node):
        self.ensure_eol(2)
        for anchor in node.get("ids", []):
            self._add_anchor(anchor)
        self.ensure_eol(2)

    @pushing_context
    def visit_classifier(self, node):
        """A definition list classifier, e.g., numpydoc parameter types: rendered as `term : *type*`"""
        self.add(" : ")
        self._push_context(contexts.ITALIC.create(node, "classifier"))

    @pushing_context
    def visit_definition(self, node):
        self._push_context(
            contexts.Indent(": ", only_first=True, support_multi_line_break=True, params=contexts.BaseParams(1, 2))
        )

    def visit_math_block(self, node):
        """docutils math block"""
        self._push_status(escape_text=False, preserve_line_breaks=True)
        self.add("$$", prefix_eol=1, suffix_eol=1)

    def depart_math_block(self, node):
        """docutils math block"""
        self.add("$$", prefix_eol=1, suffix_eol=2)
        self._pop_status()

    def visit_math(self, node):
        """docutils math node"""
        self._push_status(escape_text=False)
        self.add("$")

    def depart_math(self, node):
        """docutils math node"""
        self.add("$")
        self._pop_status()

    @pushing_context
    @pushing_status
    def visit_literal(self, node):
        self._push_status(escape_text=False)
        self._push_context(contexts.InlineCode())

    @pushing_context
    @pushing_status
    def visit_literal_block(self, node):
        self._push_status(escape_text=False, preserve_line_breaks=True)
        # Sphinx sets `language` on every literal_block (the `Code` directive and `HighlightLanguageTransform`).
        # docutils and Sphinx < 2 kept it in `classes` (["code", <lang>]), which no supported Sphinx produces.
        self._push_context(contexts.CodeBlock(node.get("language", "")))

    @pushing_context
    @pushing_status
    def visit_doctest_block(self, node):
        self._push_status(escape_text=False, preserve_line_breaks=True)
        self._push_context(contexts.CodeBlock("pycon"))

    @pushing_context
    def visit_block_quote(self, node):
        self._push_context(contexts.Indent("> "))

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
    def visit_title(self, node):
        if isinstance(self.ctx, contexts.Table):
            level = 4
        else:
            level = self.status.section_level
        self._push_context(contexts.Title(level))

    @pushing_context
    @pushing_status
    def visit_subtitle(self, node):  # pragma: no cover
        """
        Docutils does not promote subtitles, so this might never be called.
        However, we keep it here in case some future version will change this behaviour.
        """
        self._push_status(section_level=self.status.section_level + 1)
        self._push_context(contexts.Title(self.status.section_level))

    @pushing_context
    def visit_rubric(self, node):
        """Sphinx Rubric, a heading without relation to the document sectioning"""
        self._push_context(contexts.Title(3))

    def visit_transition(self, node):
        """Simply replace a transition by a horizontal rule."""
        # Can use three or more '*', '_' or '-'.
        self.add("---", prefix_eol=2, suffix_eol=1)
        raise nodes.SkipNode

    @pushing_context
    def visit_reference(self, node: nodes.reference):
        ref_id: str | None = node.get("refid")
        ref_uri: str = node.get("refuri", "")
        is_internal = bool(node.get("internal", self.status.default_ref_internal))

        if ref_id:
            # Same-document reference: docutils uses refid for targets in the same document
            target = f"#{ref_id}"
        elif is_internal:
            # Internal reference: adjust relative URL to destination
            target = self._adjust_url(ref_uri)
        else:
            # External reference: preserve target URL verbatim
            target = ref_uri

        self._push_context(contexts.Wrapped("[", f"]({escape.link_destination(target)})"))

    def _adjust_url(self, url: str):
        """Replace `refuri` in reference with HTTP address, if possible"""
        if not self.config.markdown_http_base:
            return url

        # If HTTP page build URL known, make link relative to that.
        this_doc = self.builder.current_doc_name
        if url == "":  # Reference to this doc
            url = self.builder.get_target_uri(this_doc)
        else:  # URL is relative to the current docname, or absolute from the source root.
            url = posixpath.normpath(posixpath.join(posixpath.dirname(this_doc), url))
        return posixpath.join(self.config.markdown_http_base, url.lstrip("/"))

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
        self._push_context(contexts.Wrapped("[", f"]({escape.link_destination(target)})"))

    def _add_anchor(self, anchor: str):
        content = f'<a id="{escape.html_quote(anchor)}"></a>'
        # Prevent adding the same anchor twice in the same context
        if content not in self.ctx.content:
            self.add(content, prefix_eol=2, suffix_eol=1)

    def visit_target(self, node):
        # A target moves its id onto the element after it (`refid`), except before a footnote or a citation, where it
        # keeps its own `ids`. A target with `refuri` is an external link, which needs no anchor.
        ref_id = node.get("refid")
        if ref_id is not None:
            self._add_anchor(ref_id)
        elif "refuri" not in node:
            for anchor in node.get("ids", ()):
                self._add_anchor(anchor)

    @pushing_context
    @pushing_status
    def visit_topic(self, node):
        self._push_status(default_ref_internal=True, section_level=5)
        self._push_context(contexts.Indent("> ", empty=True))

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
        self._push_status(list_marker=contexts.ListMarker(marker))

    def _end_list(self, _node=None):
        self._pop_status()
        # We need two line breaks to make sure the next paragraph will not merge into the list
        self.ensure_eol(2)

    def _start_list_item(self, _node=None):
        marker = self.status.list_marker
        marker.inc()
        self._push_context(contexts.Indent(marker, only_first=True, params=contexts.BaseParams(1, 1)))

    _end_list_item = _pop_context

    def visit_enumerated_list(self, node):
        self._start_list(node.get("start", 1) - 1)

    depart_enumerated_list = _end_list

    def visit_bullet_list(self, node):
        self._start_list(node.attributes.get("bullet", self.config.markdown_bullet))

    depart_bullet_list = _end_list
    visit_list_item = _start_list_item
    depart_list_item = _end_list_item

    ################################################################################
    # desc
    ################################################################################
    # desc (desctype: {function, class, method, etc.)
    #   desc_signature
    #     desc_signature_line (optional nesting)
    #         desc_name
    #           desc_annotation (optional)
    #         desc_parameterlist
    #           desc_annotation (optional, outside any parameter, e.g., httpdomain's `int:`)
    #           desc_parameter (also the `/` and `*` markers of Python signatures)
    #           desc_optional (e.g., `f(a[, b[, c]])`, from textual signatures only)
    #             desc_parameter
    #             desc_optional (optional nesting)
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
        self._push_context(contexts.Title(h_level))

    @pushing_multi_context(2)
    def visit_desc_parameterlist(self, node):
        self._push_context(contexts.Wrapped("(", ")", wrap_empty=True))
        self._push_context(contexts.ParameterList())

    @pushing_context
    def visit_desc_parameter(self, node):
        """single method/class ctr param"""
        self.param_list_ctx.enter_parameter(is_required=True)
        self._push_context(contexts.Base())

    @property
    def param_list_ctx(self) -> contexts.ParameterList:
        return self._typed_ctx(contexts.ParameterList)

    @pushing_context
    def visit_desc_optional(self, node):
        self.param_list_ctx.enter_parameter(is_required=False)
        self._push_context(contexts.ParameterList())

    def visit_field_list(self, node):
        self._start_list("*")

    @pushing_context
    def visit_field_name(self, node):
        """A bold field name with a colon, e.g., `**Parameters:**`"""
        self._push_context(contexts.STRONG.create(node, "field_name"))

    def depart_field_name(self, node):
        self.add(":")
        self._pop_context()

    depart_field_list = _end_list
    visit_field = _start_list_item
    depart_field = _end_list_item

    def visit_desc_returns(self, node):
        self.add(" → ")

    @pushing_context
    def visit_field_body(self, node):
        self._push_context(contexts.Base(contexts.BaseParams(1, 1)))

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

    @pushing_context
    def visit_table(self, node):
        self._push_context(
            contexts.Table(
                params=contexts.BaseParams(2, 1),
                compact=self.config.markdown_compact_tables,
            )
        )

    def visit_thead(self, node):
        self.table_ctx.enter_head()

    @property
    def table_ctx(self) -> contexts.Table:
        return self._typed_ctx(contexts.Table)

    def depart_thead(self, node):
        self.table_ctx.exit_head()

    def visit_tbody(self, node):
        self.table_ctx.enter_body()

    def depart_tbody(self, node):
        self.table_ctx.exit_body()

    def visit_row(self, node):
        self.table_ctx.enter_row()

    def depart_row(self, node):
        self.table_ctx.exit_row()

    def visit_entry(self, node):
        self.table_ctx.enter_entry()

    def depart_entry(self, node):
        self.table_ctx.exit_entry()

    ################################################################################
    # footnote
    ################################################################################
    # footnote_reference
    # ...
    # footnote
    #   label
    #   paragraph
    #
    # citation (e.g., numpydoc's References section) is rendered like a footnote
    # citation_reference is rendered like a footnote_reference (see `builder.KeepCitationReferences`)
    ###############################################################################

    @pushing_context
    def visit_footnote_reference(self, node):
        ref_id = node.get("refid", "")
        self._push_context(contexts.Wrapped("<sup>[", f"](#{ref_id})</sup>"))

    @pushing_context
    @pushing_status
    def visit_citation_reference(self, node):
        """Links to the citation's anchor on this page, otherwise to its page with the anchor"""
        doc_name, label_id = node.get("docname"), node.get("refname")
        this_doc = self.builder.current_doc_name
        if doc_name == this_doc:
            target = f"#{label_id}"
        else:
            target = self._adjust_url(f"{self.builder.get_relative_uri(this_doc, doc_name)}#{label_id}")
        # The text of a citation reference is its bracketed label (`[1]`): its brackets build the link, so keep them.
        self._push_status(escape_text=False)
        self._push_context(contexts.Wrapped("<sup>", f"({escape.link_destination(target)})</sup>"))

    @pushing_context
    def visit_footnote(self, node):
        ids = node.get("ids", "")
        if isinstance(ids, (list, tuple)):
            ids = ",".join(ids)
        names = node.get("names", "")
        if isinstance(names, (list, tuple)):
            names = ",".join(names)
        self._push_context(contexts.FootNote(ids, names, params=contexts.BaseParams(1, 1)))

    @pushing_context
    def visit_citation(self, node):
        self.visit_footnote(node)

    def visit_label(self, node):
        if isinstance(self.ctx, contexts.FootNote):
            self.ctx.visit_label()
        else:
            # Outside a footnote, e.g., a sphinx-inline-tabs tab title:
            # container(type="tab") > label (the title) + container(classes="tab-content").
            # Render the title as a bold line.
            self._push_context(contexts.Wrapped("**", params=contexts.BaseParams(2, 2)))

    def depart_label(self, node):
        if isinstance(self.ctx, contexts.FootNote):
            self.ctx.depart_label()
        else:
            self._pop_context()


def _pass(_node=None):
    pass


def _skip(_node=None):
    raise nodes.SkipNode
