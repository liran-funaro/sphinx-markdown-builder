"""
Integration tests for the markdown builder
"""

import os
import shutil
import stat
from pathlib import Path
from typing import Iterable

import pytest
from sphinx.cmd.build import main

BUILD_PATH = "./tests/docs-build"
SOURCE_PATH = "./tests/source"

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
        "-D",
        "markdown_bullet=-",
        "-D",
        "markdown_file_suffix=.html.md",
        "-D",
        "markdown_flavor=github",
        "-j",
        "8",
    ],
]
BUILD_PATH_OPTIONS = [BUILD_PATH, os.path.join(BUILD_PATH, "overrides")]
OPTIONS = list(zip(SOURCE_FLAGS, BUILD_PATH_OPTIONS))


def _rm_build_path(build_path: str):
    if os.path.exists(build_path):
        shutil.rmtree(build_path)


def _touch_sources():
    for file_name in os.listdir(SOURCE_PATH):
        _, ext = os.path.splitext(file_name)
        if ext == ".rst":
            Path(SOURCE_PATH, file_name).touch()
            break


def _chmod_output(build_path: str, apply_func):
    if not os.path.exists(build_path):
        return

    for root, dirs, files in os.walk(build_path):
        for file_name in files:
            # Check if file ends with .md
            if file_name.endswith(".md"):
                p = Path(root, file_name)
                p.chmod(apply_func(p.stat().st_mode))


def run_sphinx(build_path, *flags):
    """Runs sphinx and validate success"""
    ret_code = main(["-M", "markdown", SOURCE_PATH, build_path, *flags])
    assert ret_code == 0


@pytest.mark.parametrize(["flags", "build_path"], OPTIONS, ids=TEST_NAMES)
def test_builder_make_all(flags: Iterable[str], build_path: str):
    run_sphinx(build_path, "-a", *flags)


@pytest.mark.parametrize(["flags", "build_path"], OPTIONS, ids=TEST_NAMES)
def test_builder_make_updated(flags: Iterable[str], build_path: str):
    _touch_sources()
    run_sphinx(build_path, *flags)


@pytest.mark.parametrize(["flags", "build_path"], OPTIONS, ids=TEST_NAMES)
def test_builder_make_missing(flags: Iterable[str], build_path: str):
    _rm_build_path(build_path)
    run_sphinx(build_path, *flags)


@pytest.mark.parametrize(["flags", "build_path"], OPTIONS, ids=TEST_NAMES)
def test_builder_access_issue(flags: Iterable[str], build_path: str):
    _touch_sources()
    flag = stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
    _chmod_output(build_path, lambda mode: mode & ~flag)
    try:
        run_sphinx(build_path, *flags)
    finally:
        _chmod_output(build_path, lambda mode: mode | flag)


def _has_suffix_in_path(path: str, suffix: str) -> bool:
    """Checks that at least one file with the given suffix exists"""
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(suffix):
                return True
    return False


def test_custom_file_suffix():
    """Test that markdown_file_suffix configuration generates files with correct suffix"""
    build_path = os.path.join(BUILD_PATH, "test_suffix")
    suffix = ".html.md"

    # Clean and build
    _rm_build_path(build_path)
    run_sphinx(build_path, "-a", "-D", f"markdown_file_suffix={suffix}")

    # Verify files have the correct suffix
    markdown_dir = os.path.join(build_path, "markdown")
    assert os.path.exists(markdown_dir), f"Markdown output directory not found: {markdown_dir}"

    # Check that at least one file with the custom suffix exists
    assert _has_suffix_in_path(markdown_dir, suffix), f"No files with suffix '{suffix}' found in {markdown_dir}"

    # Clean up
    _rm_build_path(build_path)
