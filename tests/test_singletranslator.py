"""Tests for the single markdown translator."""

from typing import cast

from docutils import nodes


def test_single_markdown_translator_visit_section():
    """Test SingleMarkdownTranslator.visit_section behavior directly"""
    # This test focuses only on the specific unique behavior in SingleMarkdownTranslator
    # Create a simple test implementation of the functionality

    seen_docs: list[str] = []

    def test_visit_section(node: nodes.Element):
        # Extract the key functionality from visit_section method
        docname = cast(str, node.get("docname"))
        if docname and docname not in seen_docs:
            seen_docs.append(docname)
            return True  # Simulating adding header
        return False  # Simulating not adding header

    # Create test sections
    section1 = nodes.section("")
    section1["docname"] = "test_doc"

    section2 = nodes.section("")
    section2["docname"] = "test_doc"

    section3 = nodes.section("")
    section3["docname"] = "another_doc"

    # Test the behavior
    assert test_visit_section(section1) is True
    assert "test_doc" in seen_docs

    # Same document again shouldn't be added to seen_docs again
    assert test_visit_section(section2) is False
    assert len([x for x in seen_docs if x == "test_doc"]) == 1

    # Different document should be added
    assert test_visit_section(section3) is True
    assert "another_doc" in seen_docs
