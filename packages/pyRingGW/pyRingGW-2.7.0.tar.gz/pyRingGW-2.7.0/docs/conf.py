# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

#import os
#import sys
#sys.path.insert(0, os.path.abspath('..'))

from pyRing import pyRing

# -- Project information -----------------------------------------------------

project = 'pyRing'
copyright = '2024, Gregorio Carullo, Walter Del Pozzo, John Veitch'
author = 'Gregorio Carullo, Walter Del Pozzo, John Veitch'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
#extensions = ['myst_parser', 'sphinx.ext.autodoc', 'sphinx.ext.napoleon']
extensions = ['myst_parser',
              'sphinx.ext.autodoc',
              'sphinx.ext.doctest',
              'sphinx.ext.intersphinx',
              'sphinx.ext.mathjax',
              'sphinx.ext.githubpages',
              'sphinx.ext.ifconfig',
              'sphinx.ext.viewcode',
              'sphinx.ext.napoleon']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

source_suffix = ['.rst', '.md']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
pygments_style = 'sphinx'

import kotti_docs_theme
html_theme = 'kotti_docs_theme'
html_theme_path = [kotti_docs_theme.get_theme_dir()]

htmlhelp_basename = 'pyRingdocs'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The version info for the project you're documenting, acts as replacement fo    r
# |version| and |release|, also used in various other places throughout the
# built documents.

import pyRing
#
# The short X.Y version.
version = pyRing.__version__
# The full version, including alpha/beta/rc tags.
release = pyRing.__version__
