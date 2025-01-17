import os
import sys
import mock
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MIT 6.01SC Introduction To Electrical Engineering And Computer Science I'
copyright = '2024, Muhammed Abdullah'
author = 'Muhammed Abdullah'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinxcontrib.restbuilder',
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.napoleon',
        'sphinx.ext.viewcode',
        'sphinx.ext.duration',
        'sphinx.ext.intersphinx',   # to use autolinking
        'sphinx_rtd_theme',
        'myst_parser', 
        'sphinx_design',            # for tabs and dropdown
        'sphinx_simplepdf',
        'sphinxcontrib.video',      # for videos
        ]

source_suffix = ['.rst', '.md']

toc_object_entries = False          # Create table of contents entries for domain objects (e.g. functions, classes, attributes, etc.). Default is True.

myst_enable_extensions = [
    "colon_fence",          # Enable code fences using ::: delimiters instead of ````
    # "deflist",
    "html_image",
    "dollarmath",           # Enable parsing of dollar $ and $$ encapsulated math
]

# To have class CombinedDynamicMoveToPoint instead of  class dynamicMoveToPoint.CombinedDynamicMoveToPoint
add_module_names = False    # https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-add_module_names

## Extension Settings
# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_ivar = True
napoleon_use_param = True

autosummary_generate = True
autoclass_content = 'both'
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'undoc-members': True,
}

# mock imports
autodoc_mock_imports = ["lib601, lib601.util, lib601.sm, lib601.gfx, soar.io"]

MOCK_MODULES = ['lib601', 'lib601.util', 'lib601.sm', 'lib601.gfx', 'soar.io', 'smBrain', 'lib601.io']
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.Mock()

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

sys.path.insert(0, os.path.abspath('../..'))
# sys.path.insert(0, os.path.abspath('../../Unit 1 Software Engineering/swLab02'))
sys.path.insert(0, os.path.abspath('../../Unit 1 Software Engineering/designLab01'))
sys.path.insert(0, os.path.abspath('../../Unit 1 Software Engineering/designLab02'))
sys.path.insert(0, os.path.abspath('../../Unit 1 Software Engineering/homework01'))
sys.path.insert(0, os.path.abspath('../../Unit 2 Signals and Systems/designLab03'))
sys.path.insert(0, os.path.abspath('../../Unit 2 Signals and Systems/quiz03'))
# sys.path.insert(0, os.path.abspath('../../Unit 2 Signals and Systems/'))