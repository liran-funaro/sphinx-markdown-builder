"""
Unit tests for the markdown builder
"""
import logging
from unittest.mock import Mock

import docutils.nodes
import pytest
import sphinx.util.logging

from sphinx_markdown_builder.contexts import SubContext
from sphinx_markdown_builder.translator import MarkdownTranslator


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
    ctx = SubContext()
    # We add spaces to make sure we ignore them
    ctx.add("\n \t ")
    ctx.add("test", prefix_eol=1)
    ctx.force_eol(1)
    assert ctx.make() == "\n \t test\n"


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

    assert sum("unknown node" in rec.message for rec in caplog.records) == len(test_nodes)
    for node in test_nodes:
        assert sum(node.__class__.__name__ in rec.message for rec in caplog.records) == 1


def test_problematic():
    mt = make_mock()
    node = docutils.nodes.problematic(text="text")
    mt.add("prefix")
    with pytest.raises(docutils.nodes.SkipNode):
        mt.dispatch_visit(node)
    mt.add("suffix")
    assert mt.astext() == "prefix\n\n```\ntext\n```\n\nsuffix\n"
