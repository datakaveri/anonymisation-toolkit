# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Anonymisation Toolkit'
copyright = '2024, Center for Data for Public Good'
author = 'Novoneel Chakraborty'
release = '0.1.0'
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon', 'autoapi.extension', 'sphinx.ext.viewcode', 'sphinx.ext.githubpages']

autoapi_dirs = ['../src/cdpg_anonkit/']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = 'furo'
html_logo = '/home/novoneel-iudx/anonymisation-toolkit/docs/_build/html/_static/cdpg-logo_hires.png'
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "orange",
        "color-brand-secondary": "blue",
        "color-brand-content": "#CC3333",
        "color-admonition-background": "blue",
    },
    "navigation_with_keys": True,
    'sidebar_hide_name': True,
}

html_baseurl = 'https://novoneel-iudx.github.io/differential-privacy-toolkit/'
html_extra_path = ['.nojekyll']

