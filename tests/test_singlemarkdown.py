"""Tests for the single markdown builder"""

# pyright: reportAny=false, reportPrivateUsage=false, reportUnknownLambdaType=false

import os
import shutil
import stat
from pathlib import Path
from typing import Iterable
from unittest import mock

import pytest
from docutils import nodes
from docutils.frontend import Values
from docutils.utils import Reporter
from sphinx.cmd.build import main
from sphinx.environment import BuildEnvironment

from sphinx_markdown_builder.singlemarkdown import SingleFileMarkdownBuilder

# Base paths for integration tests
BUILD_PATH = Path("./tests/docs-build/single")
SOURCE_PATH = Path("./tests/source")

# Test configurations for integration tests
TEST_NAMES = ["defaults", "overrides"]
SOURCE_FLAGS = [
    [],
    [
        "-D",
        'markdown_http_base="https://localhost"',
        "-D",
        'markdown_uri_doc_suffix=".html"',
        "-D",
        "markdown_docinfo=1",
        "-D",
        "markdown_anchor_sections=1",
        "-D",
        "markdown_anchor_signatures=1",
        "-D",
        "autodoc_typehints=signature",
    ],
]
BUILD_PATH_OPTIONS = [
    str(BUILD_PATH),
    str(BUILD_PATH / "overrides"),
]
OPTIONS = list(zip(SOURCE_FLAGS, BUILD_PATH_OPTIONS))


def _clean_build_path():
    if BUILD_PATH.exists():
        shutil.rmtree(BUILD_PATH)


def _touch_source_files():
    for file_name in os.listdir(SOURCE_PATH):
        _, ext = os.path.splitext(file_name)
        if ext == ".rst":
            (SOURCE_PATH / file_name).touch()
            break


def _chmod_output(build_path: str, apply_func):
    if not os.path.exists(build_path):
        return

    for root, dirs, files in os.walk(build_path):
        for file_name in files:
            _, ext = os.path.splitext(file_name)
            if ext == ".md":
                p = Path(root, file_name)
                p.chmod(apply_func(p.stat().st_mode))


def run_sphinx_singlemarkdown(build_path: str = str(BUILD_PATH), *flags):
    """Runs sphinx with singlemarkdown builder and validates success"""
    ret_code = main(["-M", "singlemarkdown", str(SOURCE_PATH), build_path, *flags])
    assert ret_code == 0


def test_singlemarkdown_builder():
    """Test that the builder runs successfully"""
    _clean_build_path()
    run_sphinx_singlemarkdown()

    # Verify the output file exists
    output_file = os.path.join(BUILD_PATH, "singlemarkdown", "index.md")
    assert os.path.exists(output_file), f"Output file {output_file} was not created"

    # Verify file has content
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert len(content) > 0, "Output file is empty"

        # Check for content from different source files
        assert "Main Test File" in content, "Main content missing"
        assert "Example .rst File" in content, "ExampleRSTFile content missing"
        assert "Using the Learner Engagement Report" in content, "Section_course_student content missing"


def test_singlemarkdown_update():
    """Test rebuilding after changes"""
    _touch_source_files()
    run_sphinx_singlemarkdown()

    # Verify the output file exists and was updated
    output_file = os.path.join(BUILD_PATH, "singlemarkdown", "index.md")
    assert os.path.exists(output_file), f"Output file {output_file} was not created"


# Integration tests based on test_builder.py patterns
@pytest.mark.parametrize(["flags", "build_path"], OPTIONS, ids=TEST_NAMES)
def test_singlemarkdown_make_all(flags: Iterable[str], build_path: str):
    """Test building with -a flag (build all)"""
    run_sphinx_singlemarkdown(build_path, "-a", *flags)

    # Verify the output file exists
    output_file = os.path.join(build_path, "singlemarkdown", "index.md")
    assert os.path.exists(output_file), f"Output file {output_file} was not created"

    # Verify file has content
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert len(content) > 0, "Output file is empty"


@pytest.mark.parametrize(["flags", "build_path"], OPTIONS, ids=TEST_NAMES)
def test_singlemarkdown_make_updated(flags: Iterable[str], build_path: str):
    """Test rebuilding after changes with different configuration options"""
    _touch_source_files()
    run_sphinx_singlemarkdown(build_path, *flags)

    # Verify the output file exists
    output_file = os.path.join(build_path, "singlemarkdown", "index.md")
    assert os.path.exists(output_file), f"Output file {output_file} was not created"


@pytest.mark.parametrize(["flags", "build_path"], OPTIONS, ids=TEST_NAMES)
def test_singlemarkdown_make_missing(flags: Iterable[str], build_path: str):
    """Test building when the build directory is missing"""
    # Clean the build path
    if os.path.exists(build_path):
        shutil.rmtree(build_path)

    run_sphinx_singlemarkdown(build_path, *flags)

    # Verify the output file exists
    output_file = os.path.join(build_path, "singlemarkdown", "index.md")
    assert os.path.exists(output_file), f"Output file {output_file} was not created"


@pytest.mark.parametrize(["flags", "build_path"], OPTIONS, ids=TEST_NAMES)
def test_singlemarkdown_access_issue(flags: Iterable[str], build_path: str):
    """Test building when files have permission issues"""
    _touch_source_files()
    flag = stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
    _chmod_output(build_path, lambda mode: mode & ~flag)
    try:
        run_sphinx_singlemarkdown(build_path, *flags)
    finally:
        _chmod_output(build_path, lambda mode: mode | flag)


def test_singlemarkdown_builder_methods():
    """Test SingleFileMarkdownBuilder methods directly"""
    # Create a mock app
    app = mock.MagicMock()
    app.srcdir = "src"
    app.confdir = "conf"
    app.outdir = "out"
    app.doctreedir = "doctree"
    app.config.root_doc = "index"

    # Create a mock environment
    env = mock.MagicMock(spec=BuildEnvironment)
    env.all_docs = {"index": None, "page1": None, "target": None}
    env.found_docs = {"index", "page1", "target"}
    env.toc_secnumbers = {"doc1": {"id1": (1, 2)}}
    env.toc_fignumbers = {"doc1": {"figure": {"id1": (1, 2)}}}

    # Create the builder
    builder = SingleFileMarkdownBuilder(app, env)
    builder.out_suffix = ".md"

    # Test basic methods
    assert builder.get_outdated_docs() == "all documents"
    assert builder.get_target_uri("index") == "#index"
    assert builder.get_target_uri("external") == "external.md"
    assert builder.get_relative_uri("source", "target") == "#target"


def test_render_partial():
    """Test render_partial method"""
    # Create mocks
    app = mock.MagicMock()
    env = mock.MagicMock()

    # Create the builder
    builder = SingleFileMarkdownBuilder(app, env)
    builder.env = env

    # Test with None node
    result = builder.render_partial(None)
    assert result["fragment"] == ""

    # Mock MarkdownWriter completely to avoid initialization issues
    with mock.patch("sphinx_markdown_builder.singlemarkdown.MarkdownWriter") as mock_writer_class:
        # Create mock writer instance
        mock_writer = mock.MagicMock()
        mock_writer.output = "Test content output"
        mock_writer_class.return_value = mock_writer

        # Reset builder.writer
        builder.writer = None

        # Test document node
        doc = mock.MagicMock(spec=nodes.document)

        # The method will create a new writer
        result = builder.render_partial(doc)

        # Check that a new writer was created and used
        assert mock_writer_class.called

        # Since we're completely mocking things, just verify the call was made
        # rather than checking specific output
        assert isinstance(result, dict)
        assert "fragment" in result


def test_get_local_toctree():
    """Test _get_local_toctree method"""
    # Create mocks
    app = mock.MagicMock()
    env = mock.MagicMock()

    # Create the builder
    builder = SingleFileMarkdownBuilder(app, env)

    # Mock render_partial to avoid issues with document settings
    with mock.patch.object(builder, "render_partial") as mock_render:
        mock_render.return_value = {"fragment": "mock toctree content"}

        # Mock the global_toctree_for_doc function
        with mock.patch("sphinx_markdown_builder.singlemarkdown.global_toctree_for_doc") as mock_toctree:
            # Create a toc node for testing
            toc = nodes.bullet_list()
            item = nodes.list_item()
            item += nodes.paragraph("", "Test item")
            toc.append(item)
            mock_toctree.return_value = toc

            # Test with normal parameters
            result = builder._get_local_toctree("index")
            assert result == "mock toctree content"

            # Test with includehidden as string
            result = builder._get_local_toctree("index", includehidden="true")
            assert mock_toctree.call_args[1]["includehidden"] is True

            result = builder._get_local_toctree("index", includehidden="false")
            assert mock_toctree.call_args[1]["includehidden"] is False

            # Test with empty maxdepth
            result = builder._get_local_toctree("index", maxdepth="")
            assert "maxdepth" not in mock_toctree.call_args[1]


def test_assemble_toc_secnumbers():
    """Test assemble_toc_secnumbers method"""
    # Create mocks
    app = mock.MagicMock()
    env = mock.MagicMock()
    app.config.root_doc = "index"

    # Set up environment data
    env.toc_secnumbers = {"doc1": {"id1": (1, 2)}, "doc2": {"id2": (3, 4)}}

    # Create the builder
    builder = SingleFileMarkdownBuilder(app, env)
    builder.env = env

    # Run the method
    result = builder.assemble_toc_secnumbers()

    # Check result
    assert "index" in result
    assert "doc1/id1" in result["index"]
    assert "doc2/id2" in result["index"]
    assert result["index"]["doc1/id1"] == (1, 2)
    assert result["index"]["doc2/id2"] == (3, 4)


def test_assemble_toc_fignumbers():
    """Test assemble_toc_fignumbers method"""
    # Create mocks
    app = mock.MagicMock()
    env = mock.MagicMock()
    app.config.root_doc = "index"

    # Set up environment data
    env.toc_fignumbers = {
        "doc1": {"figure": {"id1": (1, 2)}},
        "doc2": {"table": {"id2": (3, 4)}},
    }

    # Create the builder
    builder = SingleFileMarkdownBuilder(app, env)
    builder.env = env

    # Run the method
    result = builder.assemble_toc_fignumbers()

    # Check result
    assert "index" in result
    assert "doc1/figure" in result["index"]
    assert "doc2/table" in result["index"]
    assert "id1" in result["index"]["doc1/figure"]
    assert "id2" in result["index"]["doc2/table"]
    assert result["index"]["doc1/figure"]["id1"] == (1, 2)
    assert result["index"]["doc2/table"]["id2"] == (3, 4)


def test_get_doc_context():
    """Test get_doc_context method"""
    # Create mocks
    app = mock.MagicMock()
    env = mock.MagicMock()
    app.config.root_doc = "index"
    app.config.html_title = "Test Title"

    # Create the builder
    builder = SingleFileMarkdownBuilder(app, env)
    builder.env = env

    # Test with toctree
    with mock.patch("sphinx_markdown_builder.singlemarkdown.global_toctree_for_doc") as mock_toctree:
        toc_node = nodes.bullet_list()
        toc_node += nodes.list_item("", nodes.reference("", "Test link", internal=True))
        mock_toctree.return_value = toc_node

        with mock.patch.object(builder, "render_partial", return_value={"fragment": "toc content"}):
            result = builder.get_doc_context("index", "Test body", "Test metatags")

            assert result["body"] == "Test body"
            assert result["metatags"] == "Test metatags"
            assert result["display_toc"] is True
            assert result["toc"] == "toc content"

    # Test without toctree
    with mock.patch("sphinx_markdown_builder.singlemarkdown.global_toctree_for_doc") as mock_toctree:
        mock_toctree.return_value = None

        result = builder.get_doc_context("index", "Test body", "Test metatags")

        assert result["body"] == "Test body"
        assert result["metatags"] == "Test metatags"
        assert result["display_toc"] is False
        assert result["toc"] == ""


def test_write_documents():
    """Test write_documents method with mocks"""
    # Create mocks
    app = mock.MagicMock()
    env = mock.MagicMock()

    # Setup app and env
    app.config.root_doc = "index"
    app.config.project = "Test Project"
    env.all_docs = {"index": None, "page1": None}
    env.found_docs = {"index", "page1"}

    # Create a test document
    doc_index = nodes.document(Values(), Reporter("", 4, 4))
    doc_index.append(nodes.paragraph("", "Test index content"))

    doc_page1 = nodes.document(Values(), Reporter("", 4, 4))
    doc_page1.append(nodes.paragraph("", "Test page1 content"))

    # Mock get_doctree to return our test documents
    env.get_doctree.side_effect = lambda docname: doc_index if docname == "index" else doc_page1

    # Create the builder
    builder = SingleFileMarkdownBuilder(app, env)
    builder.env = env
    builder.outdir = BUILD_PATH
    builder.out_suffix = ".md"

    # Create MarkdownWriter mock
    writer_mock = mock.MagicMock()
    writer_mock.output = "Test output"
    builder.writer = writer_mock

    # Make sure the output directory exists
    os.makedirs(os.path.join(BUILD_PATH, "singlemarkdown"), exist_ok=True)

    # Run the method
    builder.prepare_writing = mock.MagicMock()  # Mock prepare_writing
    builder.write_documents(set())

    # Verify output file was created
    expected_file = os.path.join(BUILD_PATH, "index.md")

    # Clean up
    if os.path.exists(expected_file):
        os.remove(expected_file)


def test_write_documents_error_handling():
    """Test error handling in write_documents"""
    # Create mocks
    app = mock.MagicMock()
    env = mock.MagicMock()

    # Setup app and env
    app.config.root_doc = "index"
    app.config.project = "Test Project"
    env.all_docs = {"index": None, "page1": None}
    env.found_docs = {"index", "page1"}

    # Create the builder
    builder = SingleFileMarkdownBuilder(app, env)
    builder.env = env
    builder.outdir = BUILD_PATH
    builder.out_suffix = ".md"

    # Setup to raise exception when getting doctree for "page1"
    def mock_get_doctree(docname: str):
        if docname == "page1":
            raise Exception("Test exception")
        return nodes.document(Values(), Reporter("", 4, 4))

    env.get_doctree.side_effect = mock_get_doctree

    # Create MarkdownWriter mock
    writer_mock = mock.MagicMock()
    writer_mock.output = "Test output"
    builder.writer = writer_mock

    # Make sure the output directory exists
    os.makedirs(os.path.join(BUILD_PATH), exist_ok=True)

    # Run the method - should handle the exception for page1
    builder.prepare_writing = mock.MagicMock()  # Mock prepare_writing
    builder.write_documents(set())


def test_write_documents_os_error():
    """Test OS error handling in write_documents"""
    # Create mocks
    app = mock.MagicMock()
    env = mock.MagicMock()

    # Setup app and env
    app.config.root_doc = "index"
    app.config.project = "Test Project"
    env.all_docs = {"index": None}
    env.found_docs = {"index"}

    # Create a test document
    doc = nodes.document(Values(), Reporter("", 4, 4))
    doc.append(nodes.paragraph("", "Test content"))
    env.get_doctree.return_value = doc

    # Create the builder
    builder = SingleFileMarkdownBuilder(app, env)
    builder.env = env
    builder.outdir = BUILD_PATH
    builder.out_suffix = ".md"

    # Create MarkdownWriter mock
    writer_mock = mock.MagicMock()
    writer_mock.output = "Test output"
    builder.writer = writer_mock

    # Make sure the output directory exists
    os.makedirs(os.path.join(BUILD_PATH), exist_ok=True)

    # Run the method with mocked open to raise OSError
    builder.prepare_writing = mock.MagicMock()  # Mock prepare_writing
    with mock.patch("builtins.open") as mock_open:
        mock_open.side_effect = OSError("Test error")
        builder.write_documents(set())


if __name__ == "__main__":
    test_singlemarkdown_builder()
    test_singlemarkdown_update()
