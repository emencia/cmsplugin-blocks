# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import datetime
import os
import sys


# Settings file required by Django
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings")


# Setup Django
import django
django.setup()


# Get the module version
from cmsplugin_blocks import __version__ as cmsplugin_blocks_version


# -- Project information -----------------------------------------------------

now = datetime.date.today()
project = "cmsplugin-blocks"
copyright = "2017-{}, Emencia".format(now.year)
author = "David Thenon"

# The short X.Y version
version = cmsplugin_blocks_version
# The full version, including alpha/beta/rc tags
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# Use index.rst as root content doc file
master_doc = "index"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes. Default to builtin theme "alabaster" if sphinx rtd
# is not available.
#
html_theme = "alabaster"
try:
    import sphinx_rtd_theme
except ImportError:
    pass
else:
    html_theme = "sphinx_rtd_theme"

    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Autodoc config---------- -------------------------------------------------

# Do not order autodoc contents by alphabetical, keep to the source order
autodoc_member_order = "bysource"
