# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pnh'
copyright = '2024,25 pnh Developers'
author = 'pnh Developers'
release = '0.0.6'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc','sphinx.ext.doctest','matplotlib.sphinxext.plot_directive','sphinx.ext.mathjax']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
#html_static_path = ['_static']


plot_include_source = False
plot_formats = [('png', 300)]      # Format and DPI
plot_html_show_formats = True     # Don’t show download links
#plot_rcparams = {'figure.figsize': (6, 4)}  # Default plot size