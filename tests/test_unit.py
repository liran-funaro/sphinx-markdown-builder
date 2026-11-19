"""
Unit tests for the markdown builder
"""

import logging
from unittest.mock import Mock

import docutils.nodes
from docutils.utils import new_document
import pytest
import sphinx.util.logging
import yaml

from sphinx_markdown_builder import contexts
from sphinx_markdown_builder.translator import DOC_INFO_FIELDS, MarkdownTranslator, UnknownVisit


def make_mock():
    document = Mock(name="document")
    document.settings.language_code = "en"
    builder = Mock(name="builder")
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


# No fixture reaches this: Sphinx moves the docinfo into `env.metadata` and removes it before writing.
def test_multiple_authors_are_serialized_as_list():
    document = new_document("test")
    document += docutils.nodes.docinfo(
        "",
        docutils.nodes.author("", "Alice"),
        docutils.nodes.author("", "Bob"),
    )
    builder = Mock(name="builder")
    translator = MarkdownTranslator(document, builder)
    document.walkabout(translator)

    markdown = translator.astext()
    assert markdown.startswith("---\n")
    assert yaml.safe_load(markdown.split("---", 2)[1]) == {"author": ["Alice", "Bob"]}
    assert markdown.endswith("---\n\n")


# No fixture reaches this: Sphinx moves the docinfo into `env.metadata` and removes it before writing.
@pytest.mark.parametrize("field", DOC_INFO_FIELDS)
def test_docinfo_fields_override_config(field):
    document = new_document("test")
    value = 'Example *text*: "quotes" #1 \\ docs\nSecond line'
    node = getattr(docutils.nodes, field)("", value)
    document += docutils.nodes.docinfo("", node)
    builder = Mock(name="builder")
    builder.config.markdown_docinfo = True
    setattr(builder.config, field, "Config value")
    translator = MarkdownTranslator(document, builder)
    document.walkabout(translator)

    markdown = translator.astext()
    assert markdown.startswith("---\n")
    assert yaml.safe_load(markdown.split("---")[1]) == {field: value}


class FakeNode1(docutils.nodes.General, docutils.nodes.Element):
    pass


class FakeNode2(docutils.nodes.General, docutils.nodes.Element):
    pass


def test_unknown_visit(caplog):
    logging.getLogger(sphinx.util.logging.NAMESPACE).propagate = True
    mt = make_mock()

    test_nodes = [FakeNode1(), FakeNode2()]

    for node in test_nodes:
        with pytest.raises(docutils.nodes.SkipNode):
            mt.dispatch_visit(node)

        with pytest.raises(docutils.nodes.SkipNode):
            mt.dispatch_visit(node)

    # Deduplicate: pytest >= 9.1 may capture the same record multiple times
    unknown_messages = {rec.message for rec in caplog.records if "unknown node" in rec.message}
    assert len(unknown_messages) == len(test_nodes)
    for node in test_nodes:
        assert sum(node.__class__.__name__ in msg for msg in unknown_messages) == 1


def test_typed_ctx_mismatch(caplog):
    """
    Covers the fallback for a node visited outside the context it requires.
    No test source reaches it, and a source that did would warn, which fails the diff build (-W).
    """
    logging.getLogger(sphinx.util.logging.NAMESPACE).propagate = True
    mt = make_mock()

    with pytest.raises(UnknownVisit):
        mt._typed_ctx(contexts.Table)  # pylint: disable=protected-access

    # dispatch_visit() turns UnknownVisit into an "unknown node type" warning and skips the node
    mt.visit_paragraph = lambda node: mt._typed_ctx(contexts.Table)  # pylint: disable=protected-access
    with pytest.raises(docutils.nodes.SkipNode):
        mt.dispatch_visit(docutils.nodes.paragraph())

    assert any("unknown node type" in rec.message and "paragraph" in rec.message for rec in caplog.records)


def test_problematic():
    mt = make_mock()
    node = docutils.nodes.problematic(text="text")
    mt.add("prefix")
    with pytest.raises(docutils.nodes.SkipNode):
        mt.dispatch_visit(node)
    mt.add("suffix")
    assert mt.astext() == "prefix\n\n```\ntext\n```\n\nsuffix\n"
