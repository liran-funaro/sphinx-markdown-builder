"""
Unit tests for the markdown builder
"""
import logging
from unittest.mock import Mock

import docutils.nodes
import pytest
from sphinx import addnodes
import sphinx.util.logging

from sphinx_markdown_builder.contexts import SubContext
from sphinx_markdown_builder.translator import MarkdownTranslator


def make_mock():
    document = Mock(name="document")
    document.settings.language_code = "en"
    builder = Mock(name="builder")
    builder.heading_level_offset = 0
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


def test_desc_optional_is_wrapped_in_brackets():
    mt = make_mock()
    node = addnodes.desc_optional()

    mt.visit_desc_optional(node)
    mt.add("timeout")
    mt.depart_desc_optional(node)

    assert "[timeout]" in mt.astext()


def test_desc_parameter_without_parameterlist_does_not_fail():
    mt = make_mock()
    node = addnodes.desc_parameter()

    mt.add("prefix ")
    mt.visit_desc_parameter(node)
    mt.add("value")
    mt.depart_desc_parameter(node)

    assert "prefix value" in mt.astext()


def test_desc_parameter_inside_optional_uses_nearest_sep_context():
    mt = make_mock()
    parameterlist = addnodes.desc_parameterlist()
    optional = addnodes.desc_optional()
    first = addnodes.desc_parameter()
    second = addnodes.desc_parameter()

    mt.visit_desc_parameterlist(parameterlist)
    mt.visit_desc_optional(optional)

    mt.visit_desc_parameter(first)
    mt.add("timeout")
    mt.depart_desc_parameter(first)

    mt.depart_desc_optional(optional)

    mt.visit_desc_parameter(second)
    mt.add("retries")
    mt.depart_desc_parameter(second)

    mt.depart_desc_parameterlist(parameterlist)

    assert "[timeout], retries" in mt.astext()


def test_caution_is_rendered_as_admonition():
    mt = make_mock()
    node = docutils.nodes.caution()

    mt.visit_caution(node)
    mt.add("Handle with care")
    mt.depart_caution(node)

    output = mt.astext()
    assert "CAUTION" in output
    assert "Handle with care" in output


def test_highlightlang_sets_default_code_language():
    mt = make_mock()
    node = addnodes.highlightlang(lang="python", force=False, linenothreshold=0)
    code = docutils.nodes.literal_block("", "")
    code["classes"] = []

    mt.visit_highlightlang(node)
    mt.visit_literal_block(code)
    mt.add("print('ok')")
    mt.depart_literal_block(code)

    assert "```python" in mt.astext()
