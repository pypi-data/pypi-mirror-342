# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'sysame'
copyright = '2025, sysame.com'
author = 'sysame.com'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.coverage',
    'sphinx.ext.autosummary',
    'sphinx_autodoc_typehints',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'python'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'  # Using Read the Docs theme
html_static_path = ['_static']

# Add the source directory to the path so that autodoc can find the modules
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

# Enable autodoc to include both class docstring and __init__ docstring
autoclass_content = 'both'

# Sort members by source order (keeps the order of the source code)
autodoc_member_order = 'bysource'

# Generate autodoc stubs with summaries from code
autosummary_generate = True
