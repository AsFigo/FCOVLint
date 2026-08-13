import os
import sys

# Add 'rules' folder to Python path (relative to docs/source)
sys.path.insert(0, os.path.abspath("../../src"))
sys.path.insert(0, os.path.abspath("../../bin"))

project = "FCOVLint"
copyright = "2026, AsFigo, UK "
author = "Srinivasan Venkataramanan, Ajeetha Kumari Venkatesan "

extensions = [
    "sphinx.ext.autodoc",  # Pulls docstrings from Python modules
    "sphinx.ext.napoleon",  # Supports Google/NumPy style docstrings
    "myst_parser",  # Allows mixing Markdown (.md) and reST (.rst)
]

# Configure autodoc defaults
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "exclude-members": "apply, lvMsg",  # Explicitly hide internal methods/attrs
    "show-inheritance": True,
}
autodoc_mock_imports = ["anytree", "tomli", "verible_verilog_syntax"]

autodoc_docstring_signature = True

# Theme settings
html_theme = "furo"
html_title = "FCOVLint Documentation"
