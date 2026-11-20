"""
Unit tests for the markdown builder
"""

import logging
from unittest.mock import Mock

import docutils.nodes
import pytest
import sphinx.addnodes
import sphinx.util.logging

from sphinx_markdown_builder import contexts
from sphinx_markdown_builder.translator import MarkdownTranslator, UnknownVisit


def make_mock():
    document = Mock(name="document")
    document.settings.language_code = "en"
    builder = Mock(name="builder")
    builder.config.markdown_docinfo = False
    return MarkdownTranslator(document, builder)


def test_bad_attribute():
    mt = make_mock()

    with pytest.raises(AttributeError):
        print(mt.some_bad_argument)

    with pytest.raises(AttributeError):
        print(mt.visit_some_bad_argument)

    with pytest.raises(AttributeError):
        print(mt.depart_some_bad_argument)


def test_trailing_eol():
    ctx = contexts.Base()
    # We add spaces to make sure we ignore them
    ctx.add("\n \t ")
    ctx.add("test", prefix_eol=1)
    ctx.force_eol(1)
    assert ctx.make() == "\n \t test\n"


def test_parameter_list_drops_the_items_space():
    # No fixture reaches this: a parameter never starts with emphasis. `add()` puts a space between an item that starts
    # with emphasis and the word before it, but a bracket or a separator comes between them in the output.
    params = contexts.ParameterList()
    for is_required, text in [(False, "a"), (False, "*(b)*"), (True, "*(c)*"), (True, "*(d)*"), (False, "*(e)*")]:
        params.enter_parameter(is_required)
        params.add(text, prefix_chars=r"\w", suffix_chars=r"\w")
    assert params.make() == "[a, ][*(b)*, ]*(c)*, *(d)*[, *(e)*]"


class FakeNode1(docutils.nodes.General, docutils.nodes.Element):
    pass


class FakeNode2(docutils.nodes.General, docutils.nodes.Element):
    pass


def test_unknown_visit(caplog):
    """
    Covers the fallback for a node type without a handler, e.g., from an extension.
    No test source reaches it, and a source that did would warn, which fails the diff build (-W).
    """
    logging.getLogger(sphinx.util.logging.NAMESPACE).propagate = True
    mt = make_mock()

    test_nodes = [FakeNode1("", docutils.nodes.paragraph(text="Kept as is.")), FakeNode2(), FakeNode1()]
    for node in test_nodes:
        node.walkabout(mt)

    # The children of an unknown node are rendered as if it were not there
    assert mt.astext() == "Kept as is.\n"

    # Warn once per node type. Deduplicate: pytest >= 9.1 may capture the same record multiple times
    unknown_messages = {rec.message for rec in caplog.records if "unknown node" in rec.message}
    for node_type in ("FakeNode1", "FakeNode2"):
        assert sum(node_type in msg for msg in unknown_messages) == 1


def test_typed_ctx_mismatch(caplog):
    """
    Covers the fallback for a node visited outside the context it requires.
    No test source reaches it, and a source that did would warn, which fails the diff build (-W).
    """
    logging.getLogger(sphinx.util.logging.NAMESPACE).propagate = True
    mt = make_mock()

    with pytest.raises(UnknownVisit):
        mt._typed_ctx(contexts.Table)  # pylint: disable=protected-access

    # dispatch_visit() turns UnknownVisit into an "unknown node type" warning, and skips only the node's departure
    mt.visit_paragraph = lambda node: mt._typed_ctx(contexts.Table)  # pylint: disable=protected-access
    with pytest.raises(docutils.nodes.SkipDeparture):
        mt.dispatch_visit(docutils.nodes.paragraph())

    # The children are still rendered, and the departure doesn't pop a context the visit never pushed
    docutils.nodes.paragraph(text="Kept as is.").walkabout(mt)
    assert mt.astext() == "Kept as is.\n"

    assert any("unknown node type" in rec.message and "paragraph" in rec.message for rec in caplog.records)


def test_problematic():
    mt = make_mock()
    node = docutils.nodes.problematic(text="text")
    mt.add("prefix")
    with pytest.raises(docutils.nodes.SkipNode):
        mt.dispatch_visit(node)
    mt.add("suffix")
    assert mt.astext() == "prefix\n\n```\ntext\n```\n\nsuffix\n"


def test_legacy_productionlist():
    """
    Covers the production layout of older Sphinx (e.g., 5.1): the rule name is only in `tokenname`.
    The diff build runs a recent Sphinx, whose productions also hold the name and the aligned line.
    """
    mt = make_mock()
    grammar = sphinx.addnodes.productionlist()
    grammar += sphinx.addnodes.production("", ' "a"', tokenname="short")
    grammar += sphinx.addnodes.production("", ' "b"', tokenname="longer")
    grammar += sphinx.addnodes.production("", ' | "c"', tokenname="")
    grammar.walkabout(mt)
    assert mt.astext() == '```\nshort  ::= "a"\nlonger ::= "b"\n           | "c"\n```\n'
