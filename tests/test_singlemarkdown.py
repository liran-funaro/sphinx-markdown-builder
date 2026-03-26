"""Tests for the single markdown builder"""

# pyright: reportAny=false, reportPrivateUsage=false, reportUnknownLambdaType=false

import os
import shutil
import stat
from difflib import unified_diff
from collections.abc import Iterable
from pathlib import Path
from typing import Callable, Optional
from unittest import mock

import pytest
from docutils import nodes
from docutils.utils import new_document
from sphinx.cmd.build import main
from sphinx.environment import BuildEnvironment

from sphinx_markdown_builder.singlemarkdown import SingleFileMarkdownBuilder, setup

# Base paths for integration tests
BUILD_PATH = Path("./tests/docs-build/single")
SOURCE_PATH = Path("./tests/source")
EXPECTED_SINGLE_PATH = Path("./tests/expected/single.md")

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
    BUILD_PATH,
    BUILD_PATH / "overrides",
]
OPTIONS = list(zip(SOURCE_FLAGS, BUILD_PATH_OPTIONS))


def _new_test_document() -> nodes.document:
    return new_document("test")


def _configure_write_documents_builder(
    builder: SingleFileMarkdownBuilder,
    env: mock.MagicMock,
    all_docs: dict[str, None],
    found_docs: set[str],
) -> None:
    env.all_docs = all_docs
    env.found_docs = found_docs
    builder.outdir = BUILD_PATH
    os.makedirs(os.path.join(BUILD_PATH), exist_ok=True)


def _run_write_documents(builder: SingleFileMarkdownBuilder, open_side_effect: Optional[OSError] = None) -> None:
    builder.prepare_writing = mock.MagicMock()
    with mock.patch("sphinx_markdown_builder.singlemarkdown.MarkdownWriter") as mock_writer_class:
        writer_mock = mock.MagicMock()
        writer_mock.output = "Test output"
        mock_writer_class.return_value = writer_mock
        if open_side_effect is None:
            builder.write_documents(set())
            return
        with mock.patch("builtins.open", side_effect=open_side_effect):
            builder.write_documents(set())


def _clean_build_path():
    if BUILD_PATH.exists():
        shutil.rmtree(BUILD_PATH)


def _touch_source_files():
    for file_name in os.listdir(SOURCE_PATH):
        _, ext = os.path.splitext(file_name)
        if ext == ".rst":
            (SOURCE_PATH / file_name).touch()
            break


def _chmod_output(build_path: Path, apply_func: Callable[[int], int]) -> None:
    if not build_path.exists():
        return

    for root, _dirs, files in os.walk(build_path):
        for file_name in files:
            _, ext = os.path.splitext(file_name)
            if ext == ".md":
                p = Path(root, file_name)
                p.chmod(apply_func(p.stat().st_mode))


def run_sphinx_singlemarkdown(build_path: Path = BUILD_PATH, *flags: str):
    """Runs sphinx with singlemarkdown builder and validates success"""
    ret_code = main(["-M", "singlemarkdown", str(SOURCE_PATH), str(build_path), "-t", "Partners", *flags])
    assert ret_code == 0


def _singlemarkdown_output_file(build_path: Path) -> Path:
    return build_path / "singlemarkdown" / "index.md"


def _assert_singlemarkdown_output_exists(build_path: Path) -> Path:
    output_file = _singlemarkdown_output_file(build_path)
    assert output_file.exists(), f"Output file {output_file} was not created"
    return output_file


def _assert_singlemarkdown_output_nonempty(build_path: Path) -> str:
    output_file = _assert_singlemarkdown_output_exists(build_path)
    content = output_file.read_text(encoding="utf-8")
    assert content, "Output file is empty"
    return content


def _assert_matches_expected(actual: str, expected_path: Path) -> None:
    expected = expected_path.read_text(encoding="utf-8")
    if actual == expected:
        return

    diff = "\n".join(
        unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            fromfile=str(expected_path),
            tofile="generated singlemarkdown output",
            lineterm="",
        )
    )
    raise AssertionError(f"singlemarkdown output mismatch:\n{diff}")


def _make_builder(
    root_doc: str = "index",
    html_title: str = "Test Title",
    project: str = "Test Project",
) -> tuple[SingleFileMarkdownBuilder, mock.MagicMock, mock.MagicMock]:
    app = mock.MagicMock()
    env = mock.MagicMock()
    app.config.root_doc = root_doc
    app.config.html_title = html_title
    app.config.project = project
    builder = SingleFileMarkdownBuilder(app, env)
    builder.env = env
    builder.out_suffix = ".md"
    return builder, app, env


def _write_only_scenarios_project(base: Path) -> tuple[Path, Path]:
    src = base / "src"
    out = base / "build"
    src.mkdir(parents=True, exist_ok=True)

    (src / "conf.py").write_text(
        "extensions = ['sphinx_markdown_builder']\n"
        "project = 'only-scenarios'\n"
        "root_doc = 'index'\n",
        encoding="utf-8",
    )

    (src / "index.rst").write_text(
        "Only Scenarios\n"
        "==============\n\n"
        ".. only:: html\n\n"
        "   HTML_ONLY_TOKEN\n\n"
        ".. only:: markdown\n\n"
        "   MARKDOWN_ONLY_TOKEN\n\n"
        ".. only:: singlemarkdown\n\n"
        "   SINGLEMARKDOWN_ONLY_TOKEN\n\n"
        ".. only:: markdown or singlemarkdown\n\n"
        "   BOTH_MD_AND_SINGLE_TOKEN\n",
        encoding="utf-8",
    )

    return src, out


def test_singlemarkdown_expected_output():
    """Test full singlemarkdown output against a golden expected file."""
    _clean_build_path()
    run_sphinx_singlemarkdown(BUILD_PATH, "-a")

    actual = _assert_singlemarkdown_output_nonempty(BUILD_PATH)
    _assert_matches_expected(actual, EXPECTED_SINGLE_PATH)


def test_singlemarkdown_update():
    """Test rebuilding after changes"""
    _touch_source_files()
    run_sphinx_singlemarkdown()
    _assert_singlemarkdown_output_exists(BUILD_PATH)


# Integration tests based on test_builder.py patterns
@pytest.mark.parametrize(["flags", "build_path"], OPTIONS, ids=TEST_NAMES)
def test_singlemarkdown_make_all(flags: Iterable[str], build_path: Path):
    """Test building with -a flag (build all)"""
    run_sphinx_singlemarkdown(build_path, "-a", *flags)
    _ = _assert_singlemarkdown_output_nonempty(build_path)


@pytest.mark.parametrize(["flags", "build_path"], OPTIONS, ids=TEST_NAMES)
def test_singlemarkdown_make_updated(flags: Iterable[str], build_path: Path):
    """Test rebuilding after changes with different configuration options"""
    _touch_source_files()
    run_sphinx_singlemarkdown(build_path, *flags)
    _assert_singlemarkdown_output_exists(build_path)


@pytest.mark.parametrize(["flags", "build_path"], OPTIONS, ids=TEST_NAMES)
def test_singlemarkdown_make_missing(flags: Iterable[str], build_path: Path):
    """Test building when the build directory is missing"""
    if os.path.exists(build_path):
        shutil.rmtree(build_path)

    run_sphinx_singlemarkdown(build_path, *flags)
    _assert_singlemarkdown_output_exists(build_path)


@pytest.mark.parametrize(["flags", "build_path"], OPTIONS, ids=TEST_NAMES)
def test_singlemarkdown_access_issue(flags: Iterable[str], build_path: Path):
    """Test building when files have permission issues"""
    _touch_source_files()
    flag = stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
    _chmod_output(build_path, lambda mode: mode & ~flag)
    try:
        run_sphinx_singlemarkdown(build_path, *flags)
    finally:
        _chmod_output(build_path, lambda mode: mode | flag)


def test_singlemarkdown_builder_methods(tmp_path):
    """Test SingleFileMarkdownBuilder methods directly"""
    # Create a mock app
    app = mock.MagicMock()
    app.srcdir = "src"
    app.confdir = "conf"
    app.outdir = "out"
    app.doctreedir = str(tmp_path / "doctree")
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


def test_write_uses_base_builder_pipeline(tmp_path):
    """Singlemarkdown should rely on Builder.write() and delegate to write_documents()."""
    app = mock.MagicMock()
    env = mock.MagicMock(spec=BuildEnvironment)
    app.config.root_doc = "index"
    env.found_docs = {"index", "other"}
    env.files_to_rebuild = {}
    env.toctree_includes = {}

    builder = SingleFileMarkdownBuilder(app, env)
    builder.prepare_writing = mock.MagicMock()
    builder.copy_assets = mock.MagicMock()
    builder.write_documents = mock.MagicMock()

    builder.write(build_docnames={"other"}, updated_docnames=[], method="all")

    builder.prepare_writing.assert_called_once_with({"other"})
    builder.copy_assets.assert_called_once()
    builder.write_documents.assert_called_once()
    called_docnames = builder.write_documents.call_args.args[0]
    assert called_docnames == {"other"}
    assert "other" in called_docnames


def test_write_serial_uses_single_file_generation_path(tmp_path):
    """Legacy _write_serial hook should generate the merged singlemarkdown output."""
    app = mock.MagicMock()
    env = mock.MagicMock(spec=BuildEnvironment)

    builder = SingleFileMarkdownBuilder(app, env)
    builder._write_single_markdown = mock.MagicMock()

    builder._write_serial(["index", "other"])

    builder._write_single_markdown.assert_called_once()


def test_write_parallel_uses_single_file_generation_path(tmp_path):
    """Legacy _write_parallel hook should generate one merged output file."""
    app = mock.MagicMock()
    env = mock.MagicMock(spec=BuildEnvironment)

    builder = SingleFileMarkdownBuilder(app, env)
    builder._write_single_markdown = mock.MagicMock()

    builder._write_parallel(["index", "other"], 2)

    builder._write_single_markdown.assert_called_once()


def test_render_partial(tmp_path, monkeypatch):
    """Test render_partial method"""
    monkeypatch.chdir(tmp_path)
    builder, _, _ = _make_builder()

    # Test with None node
    result = builder.render_partial(None)
    assert result["fragment"] == ""

    with mock.patch("sphinx_markdown_builder.singlemarkdown.MarkdownWriter") as mock_writer_class:
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


def test_render_partial_non_document_node(tmp_path, monkeypatch):
    """Test render_partial with a non-document node."""
    monkeypatch.chdir(tmp_path)
    builder, _, env = _make_builder()
    env.settings = mock.MagicMock()

    with mock.patch("sphinx_markdown_builder.singlemarkdown.MarkdownWriter") as mock_writer_class:
        mock_writer = mock.MagicMock()
        mock_writer.output = None
        mock_writer_class.return_value = mock_writer

        paragraph = nodes.paragraph("", "Partial content")
        result = builder.render_partial(paragraph)

        assert isinstance(result, dict)
        assert result["fragment"] == ""
        assert mock_writer.write.called


def test_get_local_toctree(tmp_path, monkeypatch):
    """Test _get_local_toctree method"""
    monkeypatch.chdir(tmp_path)
    builder, _, _ = _make_builder()

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


def test_assemble_doctree(tmp_path, monkeypatch):
    """Test assemble_doctree method."""
    monkeypatch.chdir(tmp_path)
    builder, _, env = _make_builder()

    tree = _new_test_document()
    env.get_doctree.return_value = tree

    with mock.patch("sphinx_markdown_builder.singlemarkdown.inline_all_toctrees", return_value=tree) as mock_inline:
        result = builder.assemble_doctree()

    assert result is tree
    assert result["docname"] == "index"
    mock_inline.assert_called_once()
    env.resolve_references.assert_called_once_with(tree, "index", builder)


def test_assemble_toc_secnumbers(tmp_path, monkeypatch):
    """Test assemble_toc_secnumbers method"""
    monkeypatch.chdir(tmp_path)
    builder, _, env = _make_builder()

    # Set up environment data
    env.toc_secnumbers = {"doc1": {"id1": (1, 2)}, "doc2": {"id2": (3, 4)}}

    # Run the method
    result = builder.assemble_toc_secnumbers()

    # Check result
    assert "index" in result
    assert "doc1/id1" in result["index"]
    assert "doc2/id2" in result["index"]
    assert result["index"]["doc1/id1"] == (1, 2)
    assert result["index"]["doc2/id2"] == (3, 4)


def test_assemble_toc_fignumbers(tmp_path, monkeypatch):
    """Test assemble_toc_fignumbers method"""
    monkeypatch.chdir(tmp_path)
    builder, _, env = _make_builder()

    # Set up environment data
    env.toc_fignumbers = {
        "doc1": {"figure": {"id1": (1, 2)}},
        "doc2": {"table": {"id2": (3, 4)}},
    }

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


def test_get_doc_context(tmp_path, monkeypatch):
    """Test get_doc_context method"""
    monkeypatch.chdir(tmp_path)
    builder, _, _ = _make_builder()

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


def test_write_documents(tmp_path, monkeypatch):
    """Test write_documents method with mocks"""
    monkeypatch.chdir(tmp_path)
    builder, _, env = _make_builder()
    _configure_write_documents_builder(builder, env, {"index": None, "page1": None}, {"index", "page1"})

    # Create a test document
    doc_index = _new_test_document()
    doc_index.append(nodes.paragraph("", "Test index content"))

    doc_page1 = _new_test_document()
    doc_page1.append(nodes.paragraph("", "Test page1 content"))

    # Mock get_doctree to return our test documents
    env.get_doctree.side_effect = lambda docname: doc_index if docname == "index" else doc_page1

    _run_write_documents(builder)

    # Verify output file was created
    expected_file = os.path.join(BUILD_PATH, "index.md")

    # Clean up
    if os.path.exists(expected_file):
        os.remove(expected_file)


def test_write_documents_uses_toctree_order(tmp_path, monkeypatch):
    """Single markdown output should follow depth-first toctree order."""
    monkeypatch.chdir(tmp_path)
    builder, _, env = _make_builder(project="Order Test")
    _configure_write_documents_builder(
        builder,
        env,
        {
            "index": None,
            "z-last": None,
            "a-first": None,
            "mid": None,
            "orphan": None,
        },
        {"index", "z-last", "a-first", "mid", "orphan"},
    )

    env.toctree_includes = {
        "index": ["mid", "a-first"],
        "mid": ["z-last"],
    }

    seen_docnames: list[str] = []

    def get_doc(docname: str) -> nodes.document:
        seen_docnames.append(docname)
        return _new_test_document()

    env.get_doctree.side_effect = get_doc

    _run_write_documents(builder)

    assert seen_docnames == ["index", "mid", "z-last", "a-first"]


def test_write_documents_error_handling(tmp_path, monkeypatch):
    """Test error handling in write_documents"""
    monkeypatch.chdir(tmp_path)
    builder, _, env = _make_builder()
    _configure_write_documents_builder(builder, env, {"index": None, "page1": None}, {"index", "page1"})

    # Setup to raise exception when getting doctree for "page1"
    def mock_get_doctree(docname: str):
        if docname == "page1":
            raise Exception("Test exception")
        return _new_test_document()

    env.get_doctree.side_effect = mock_get_doctree

    _run_write_documents(builder)


def test_write_documents_os_error(tmp_path, monkeypatch):
    """Test OS error handling in write_documents"""
    monkeypatch.chdir(tmp_path)
    builder, _, env = _make_builder()
    _configure_write_documents_builder(builder, env, {"index": None}, {"index"})

    # Create a test document
    doc = _new_test_document()
    doc.append(nodes.paragraph("", "Test content"))
    env.get_doctree.return_value = doc

    _run_write_documents(builder, OSError("Test error"))


def test_setup_registers_extension():
    """Test setup function metadata and extension registration."""
    app = mock.MagicMock()

    metadata = setup(app)

    app.setup_extension.assert_called_once_with("sphinx_markdown_builder")
    assert metadata["version"] == "builtin"
    assert metadata["parallel_read_safe"] is True
    assert metadata["parallel_write_safe"] is True
