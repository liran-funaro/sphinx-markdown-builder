"""
Unit tests for the markdown builder
"""
import logging
from unittest.mock import Mock

import docutils.nodes
import pytest
from tabulate import tabulate
import sphinx.util.logging

from sphinx_markdown_builder.contexts import SubContext, TableContext
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


@pytest.mark.parametrize("compact", [False, True], ids=["default", "compact"])
def test_table_formatting(compact):
    ctx = TableContext(compact=compact)
    ctx.headers = [[["Name"], ["Description"]]]
    ctx.body = [
        [["short"], ["A much longer description"]],
        [["another value"], ["Brief"]],
    ]

    if compact:
        expected = (
            "| Name | Description |\n"
            "| --- | --- |\n"
            "| short | A much longer description |\n"
            "| another value | Brief |"
        )
    else:
        expected = tabulate(
            [
                ["short", "A much longer description"],
                ["another value", "Brief"],
            ],
            headers=["Name", "Description"],
            tablefmt="github",
        )

    assert ctx.make() == expected


def test_compact_table_preserves_cell_content():
    ctx = TableContext(compact=True)
    ctx.headers = [[["Value"], ["Description"]]]
    ctx.body = [
        [["001"], ["First line\nSecond line"]],
        [["`example()`"], ["**Important**"]],
    ]

    assert ctx.make() == (
        "| Value | Description |\n"
        "| --- | --- |\n"
        "| 001 | First line<br/>Second line |\n"
        "| `example()` | **Important** |"
    )


def test_compact_table_without_content():
    ctx = TableContext(compact=True)

    assert ctx.make() == ""
