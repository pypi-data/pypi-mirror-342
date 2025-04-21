extensions: list[str] = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

autosummary_generate: bool = True
autodoc_default_options: dict[str, bool] = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

templates_path: list[str] = ["_templates"]

html_theme: str = "pydata_sphinx_theme"
html_show_sourcelink: bool = False
html_theme_options: dict = {
    "logo": {
        "text": "pyquations",
    },
    "navbar_start": ["navbar-logo"],
    "navbar_end": ["navbar-icon-links"],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/mitchell-gottlieb/pyquations",
            "icon": "fab fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/pyquations/",
            "icon": "fab fa-python",
        },
        {
            "name": "Sponsor",
            "url": "https://github.com/sponsors/mitchell-gottlieb",
            "icon": "fas fa-heart",
            "type": "fontawesome",
        },
    ],
    "footer_start": ["copyright"],
    "footer_end": [],
}


source_suffix: list[str] = [".rst"]

master_doc: str = "index"

project: str = "pyquations"
author: str = "Mitchell Gottlieb"
