"""Configuration file for the Sphinx documentation builder."""
import sys
from pathlib import Path

mod_path = Path(__file__).parent.parent.absolute()
if mod_path not in sys.path:
    sys.path.insert(0, str(mod_path))


project = "sphinx_markdown_builder"
copyright = "Copyright (c) 2023-2026, Liran Funaro."
author = "Liran Funaro"
version = "0.6.11"

extensions = [
    "sphinx.ext.autodoc",  # Core library for html generation from docstrings
    "sphinx.ext.autosummary",  # Create neat summary tables
    "sphinx.ext.intersphinx",  # Link to other project's documentation (see mapping below)
    "sphinx_markdown_builder",
    "sphinxcontrib.httpdomain",
    "sphinx_inline_tabs",  # Emits `label` nodes outside of footnotes
    "sphinx.ext.napoleon",  # Google-style docstrings
]
napoleon_numpy_docstring = False  # Keeps the existing NumPy-style sections as they are


def edx_rtd_url(slug):
    """Make an RTD URL for a book that doesn't branch for each release."""
    return f"https://edx.readthedocs.io/projects/{slug}/en/latest/"


def openedx_rtd_url(slug):
    """Make an RTD URL for a book that branches for each release."""
    return f"https://edx.readthedocs.io/projects/{slug}/en/latest/"


intersphinx_mapping = {
    # Keep the Python inventory aligned with the expected Markdown snapshots.
    "python": ("https://docs.python.org/3/", "https://docs.python.org/3.11/objects.inv"),
    "torch": ("https://pytorch.org/docs/stable/", None),
    "opencoursestaff": (
        openedx_rtd_url("open-edx-building-and-running-a-course"),
        None,
    ),
    "data": (edx_rtd_url("devdata"), None),
    "partnercoursestaff": (edx_rtd_url("edx-partner-course-staff"), None),
    "insights": (edx_rtd_url("edx-insights"), None),
    "xblocktutorial": (edx_rtd_url("xblock-tutorial"), None),
    "installation": (openedx_rtd_url("edx-installing-configuring-and-running"), None),
    "olx": (edx_rtd_url("edx-open-learning-xml"), None),
    "openlearners": (openedx_rtd_url("open-edx-learner-guide"), None),
    "opendevelopers": (edx_rtd_url("edx-developer-guide"), None),
    "opendataapi": (edx_rtd_url("edx-data-analytics-api"), None),
    "openreleasenotes": (edx_rtd_url("open-edx-release-notes"), None),
}

autosummary_generate = True  # Turn on sphinx.ext.autosummary
autoclass_content = "both"  # Add __init__ doc (i.e., params) to class summaries
autodoc_inherit_docstrings = True  # If no docstring, inherit from base class
set_type_checking_flag = True  # Enable 'expensive' imports for sphinx_autodoc_typehints
autodoc_typehints = "description"  # Sphinx-native method. Not as good as sphinx_autodoc_typehints
add_module_names = False  # Remove namespaces from class/method signatures
autodoc_member_order = "bysource"

templates_path = ["_templates"]
exclude_patterns = ["expected"]
# image-target.rst links to a missing download on purpose, to test the unregistered-file fallback.
suppress_warnings = ["download.not_readable"]

language = "en"

# The overrides build (`-t numpydoc`) also runs numpydoc, which rewrites every autodoc docstring.
if tags.has("numpydoc"):  # noqa: F821 (Sphinx injects `tags`)
    extensions.append("numpydoc")
    # numpydoc labels the citations of a References section by a hash of the docstring. `my_module` is documented on
    # two pages (`auto-module` and the autosummary `library/my_module`), so the same labels are defined twice.
    suppress_warnings.append("ref.citation")
    # numpydoc lists class members in an autosummary. Without a toctree, it needs no generated stub pages.
    numpydoc_class_members_toctree = False
