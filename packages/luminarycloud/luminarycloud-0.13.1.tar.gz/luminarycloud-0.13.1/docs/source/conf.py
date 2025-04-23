# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.

# mypy: ignore-errors

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Luminary API - Python SDK Documentation"
# this copyright text is copied directly from the luminarycloud.com website and should be kept in sync
copyright = "2019-2024 Luminary Cloud, Inc. All rights reserved. Luminary Cloud, Luminary CFD, Realtime Engineering, and Luminary logos/marks are trademarks of Luminary Cloud, Inc., a Delaware corporation"
author = "Luminary Cloud"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "autoapi.extension",
    "numpydoc",
    "sphinx_autodoc_typehints",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",  # lots of good stuff (might want to use more features in the future): https://sphinx-design.readthedocs.io/en/latest/index.html
]

autoapi_dirs = [
    "../../luminarycloud",
    "../../luminarycloud/params/param_wrappers",
]
autoapi_type = "python"
autoapi_root = (
    "reference"  # generated docs will be in this sub dir, which becomes part of the url path
)
autoapi_file_patterns = ["*.pyi", "*.py"]
autoapi_ignore = ["test_*", "*_pb2*"]  # ignore test, private, and proto files
autoapi_options = [
    "members",
    "show-inheritance",
    "inherited-members",
    "undoc-members",
    "show-module-summary",
    "imported-members",
]
autoapi_member_order = "groupwise"

myst_enable_extensions = ["colon_fence"]
numpydoc_show_inherited_class_members = True
templates_path = ["_templates"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
# LATEST_VERSION is a template and will get replaced when generating the docs with `docker compose run --build docs`
html_title = "Luminary Cloud SDK (vLATEST_VERSION)"
# NOTE: rather than use the html_logo config option, we're embedding the logo
# directly in our custom _templates/sidebar/brand.html
# NOTE: rather than use html_favicon to set a favicon for the docs site, we
# purposefully omit it so that browsers will reuse the favicon from
# app.luminarycloud.com.
html_show_sphinx = False
html_static_path = ["assets"]

# Set the color/style for code blocks
# (https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-pygments_style).
# Eventually, we may want to define our own style using Luminary colors
# (https://pygments.org/docs/styledevelopment/,
# https://stackoverflow.com/questions/48615629/how-to-include-pygments-styles-in-a-sphinx-project),
# but for now just we just use a built-in theme (https://pygments.org/styles/).
# pygments_style = "TODO"
# pygments_dark_style = "TODO"

# https://pradyunsg.me/furo/customisation/colors/
html_theme_options = {
    "default_mode": "dark",
    "sidebar_hide_name": True,
    # hide the "View source" buttons at the top of the page
    # https://pradyunsg.me/furo/customisation/#top-of-page-buttons
    "top_of_page_buttons": [],
    # Color values are from
    # https://www.figma.com/file/jgngRpKr9HPeHuI8hKQfbS/Luminary-Component-Library-V2
    "dark_css_variables": {
        # set links to be the primary link purple
        "color-brand-primary": "#9F8EFB",
        "color-brand-content": "#9F8EFB",
        # api names, seen in the generated api reference
        "color-api-pre-name": "#FDC9A0",
        "color-api-name": "#FDC9A0",
        # Reference: https://github.com/pradyunsg/furo/blob/main/src/furo/assets/styles/variables/_admonitions.scss
        # all admonition backgrounds will be the same
        "color-admonition-title-background--caution": "#222134",
        "color-admonition-title-background--warning": "#222134",
        "color-admonition-title-background--danger": "#222134",
        "color-admonition-title-background--attention": "#222134",
        "color-admonition-title-background--error": "#222134",
        "color-admonition-title-background--hint": "#222134",
        "color-admonition-title-background--tip": "#222134",
        "color-admonition-title-background--important": "#222134",
        "color-admonition-title-background--note": "#222134",
        "color-admonition-title-background--seealso": "#222134",
        "color-admonition-title-background--admonition-todo": "#222134",
        # each admonition type will get either a orange or green highlight
        "color-admonition-title--caution": "#FDC9A0",
        "color-admonition-title--warning": "#FDC9A0",
        "color-admonition-title--danger": "#FDC9A0",
        "color-admonition-title--attention": "#FDC9A0",
        "color-admonition-title--error": "#FDC9A0",
        "color-admonition-title--hint": "#5EC298",
        "color-admonition-title--tip": "#5EC298",
        "color-admonition-title--important": "#FDC9A0",
        "color-admonition-title--note": "#5EC298",
        "color-admonition-title--seealso": "#5EC298",
        "color-admonition-title--admonition-todo": "#FDC9A0",
    },
    "light_css_variables": {
        # Reference: https://pradyunsg.me/furo/customisation/fonts/#
        # Note: custom fonts are loaded remotely, see:  _templates/sidebar/brand.html
        # Gesture Headline is overridden for <h1> in brand.html, but all other text
        # will use the font-stack below
        "font-stack": "Inter, Helvetica, Arial, sans-serif",
        "font-stack--monospace": "Inconsolata, monospace",
    },
}

# -- Custom options -------------------------------------------------

autoapi_skip_packages = []
autoapi_skip_classes = [
    "luminarycloud.SimulationParam",
]
autoapi_skip_methods = []

# -------------------------------------------------------------------


def skip_member(app, what, name, obj, skip, options):
    if what == "module":
        return True
    if what == "package" and name in autoapi_skip_packages:
        return True
    if what == "method" and name in autoapi_skip_methods:
        return True

    # Skip most of the params package until it's stable.
    if (
        what == "package"
        and name.startswith("luminarycloud.params.")
        and name != "luminarycloud.params.geometry"
    ):
        return True

    return skip


def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_member)
