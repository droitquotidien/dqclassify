# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Classification d'alinéas modificateurs"
copyright = '2024, LP, GAS'
author = 'LP, GAS'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
	"myst_parser",
	"sphinx.ext.autodoc",
	"sphinx.ext.autosummary",
	"sphinx.ext.intersphinx",
	"sphinx.ext.napoleon",
	"sphinxcontrib.bibtex",
]

templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

bibtex_bibfiles = ["dq.bib"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_title = project 

