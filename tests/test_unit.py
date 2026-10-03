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

from sphinx_markdown_builder.contexts import SubContext
from sphinx_markdown_builder.translator import DOC_INFO_FIELDS, MarkdownTranslator


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


@pytest.mark.parametrize("version", ["0.6", "0.6.11", "001", "true", "2026-10-03"])
def test_docinfo_frontmatter(version):
    document = Mock(name="document")
    document.settings.language_code = "en"
    builder = Mock(name="builder")
    builder.config.markdown_docinfo = True
    builder.config.author = 'Example: "Team" #1 \\ docs\nSecond line'
    builder.config.version = version
    translator = MarkdownTranslator(document, builder)
    translator.add("# Document")

    markdown = translator.astext()
    assert markdown.startswith("---\n")
    _, frontmatter, body = markdown.split("---", 2)
    assert yaml.safe_load(frontmatter) == {"author": builder.config.author, "version": version}
    assert body == "\n\n# Document\n"


def test_compact_frontmatter():
    document = new_document("test")
    document += docutils.nodes.docinfo(
        "",
        docutils.nodes.author("", "Example Team"),
        docutils.nodes.version("", "0.6"),
    )
    builder = Mock(name="builder")
    translator = MarkdownTranslator(document, builder)
    document.walkabout(translator)
    assert translator.astext() == "---\nauthor: Example Team\nversion: '0.6'\n---\n\n"


@pytest.mark.parametrize("enabled", [False, True])
def test_no_empty_frontmatter(enabled):
    document = Mock(name="document")
    document.settings.language_code = "en"
    builder = Mock(name="builder")
    builder.config.markdown_docinfo = enabled
    builder.config.version = "" if enabled else "0.6"
    translator = MarkdownTranslator(document, builder)
    translator.add("# Document")
    assert translator.astext() == "# Document\n"


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


def test_problematic():
    mt = make_mock()
    node = docutils.nodes.problematic(text="text")
    mt.add("prefix")
    with pytest.raises(docutils.nodes.SkipNode):
        mt.dispatch_visit(node)
    mt.add("suffix")
    assert mt.astext() == "prefix\n\n```\ntext\n```\n\nsuffix\n"
