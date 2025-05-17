"""
Tests for the single markdown builder
"""

import os
import shutil
from pathlib import Path

from sphinx.cmd.build import main

BUILD_PATH = "./tests/docs-build/single"
SOURCE_PATH = "./tests/source"


def _clean_build_path():
    if os.path.exists(BUILD_PATH):
        shutil.rmtree(BUILD_PATH)


def _touch_source_files():
    for file_name in os.listdir(SOURCE_PATH):
        _, ext = os.path.splitext(file_name)
        if ext == ".rst":
            Path(SOURCE_PATH, file_name).touch()
            break


def run_sphinx_singlemarkdown():
    """Runs sphinx with singlemarkdown builder and validates success"""
    ret_code = main(["-M", "singlemarkdown", SOURCE_PATH, BUILD_PATH])
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
        assert "Using the Learner Engagement Report" in content, (
            "Section_course_student content missing"
        )


def test_singlemarkdown_update():
    """Test rebuilding after changes"""
    _touch_source_files()
    run_sphinx_singlemarkdown()

    # Verify the output file exists and was updated
    output_file = os.path.join(BUILD_PATH, "singlemarkdown", "index.md")
    assert os.path.exists(output_file), f"Output file {output_file} was not created"


if __name__ == "__main__":
    test_singlemarkdown_builder()
    test_singlemarkdown_update()
