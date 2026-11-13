"""Sphinx configuration for the jilavsky-docs family home page.

This is the RTD *parent* project. Each package (pyIrena, Bernardyn, AIDA, ...)
builds its own docs from its own repo as an RTD *subproject*; see PLAN.md.
The family navbar (FAMILY below) is copied verbatim into every package's
conf.py so the whole site looks like one; keep the copies in sync.
"""

import os

project = "jilavsky-docs"
html_title = "SAS software by Jan Ilavsky"
author = "Jan Ilavsky"
copyright = "2026, Jan Ilavsky"  # noqa: A001  (Sphinx name)

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx.ext.intersphinx",
]

myst_enable_extensions = ["colon_fence", "deflist", "dollarmath", "substitution"]
myst_heading_anchors = 3

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# ---- Family navbar: identical block in every family conf.py ---------------
_RTD = "https://jilavsky-docs.readthedocs.io"
_IGOR = "https://saxs-igorcodedocs.readthedocs.io/en/stable/"
FAMILY = [
    {"name": "Home", "url": f"{_RTD}/en/stable/"},
    {"name": "pyIrena", "url": f"{_RTD}/projects/pyirena/en/stable/"},
    {"name": "Bernardyn", "url": f"{_RTD}/projects/bernardyn/en/stable/"},
    {"name": "AIDA", "url": f"{_RTD}/projects/aida/en/stable/"},
    {"name": "Igor: Irena/Nika/Indra", "url": _IGOR},
]
# ---------------------------------------------------------------------------

# Cross-project links. Add a family member here only once its RTD project is
# live: an unreachable inventory is a warning, and the build runs with -W.
intersphinx_mapping = {
    "igor": (_IGOR, None),
    # "pyirena": (f"{_RTD}/projects/pyirena/en/stable/", None),
    # "bernardyn": (f"{_RTD}/projects/bernardyn/en/stable/", None),
    # "aida": (f"{_RTD}/projects/aida/en/stable/", None),
}
intersphinx_disabled_reftypes = ["std:doc"]  # cross-project pages need an explicit prefix

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["family.css"]
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")
html_theme_options = {
    "external_links": [link for link in FAMILY if link["name"] != "Home"],
    "header_links_before_dropdown": 6,
    "navbar_align": "left",
    "show_toc_level": 2,
    "use_edit_page_button": True,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/jilavsky/jilavsky-docs",
            "icon": "fa-brands fa-github",
        },
    ],
}
html_context = {
    "github_user": "jilavsky",
    "github_repo": "jilavsky-docs",
    "github_version": "main",
    "doc_path": "docs",
}
