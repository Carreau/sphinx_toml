from typing import List

from pydantic import BaseModel, Field, Extra
from typing import List, Dict, Tuple


class Sphinx(BaseModel):
    autodoc_type_aliases: Dict[str, str]
    copyright: str
    default_role: str
    exclude_patterns: List[str]
    extensions: List[str]
    github_project_url: str
    master_doc: str
    modindex_common_prefix: List[str]
    pygments_style: str
    project: str
    source_suffix: str
    templates_path: List[str]
    today_fmt: str

    # class Config:
    #    extra = Extra.forbid


class IntersphinxRegistry(BaseModel):
    packages: List[str]

    class Config:
        extra = Extra.forbid


class Latex(BaseModel):
    latex_documents: List[Tuple[str, str, str, str, str, int]]
    latex_use_modindex: bool
    texinfo_documents: List[Tuple[str, str, str, str, str, str, str, int]]
    latex_font_size: str

    class Config:
        extra = Extra.forbid


class Html(BaseModel):
    html_theme: str
    html_static_path: List[str]
    html_favicon: str
    html_last_updated_fmt: str
    htmlhelp_basename: str
    html_additional_pages: List[Tuple[str, str]]

    class Config:
        extra = Extra.forbid


class Numpydoc(BaseModel):
    numpydoc_show_class_members: bool
    numpydoc_class_members_toctree: bool
    warning_is_error: bool

    class Config:
        extra = Extra.forbid


class Config(BaseModel):
    sphinx: Sphinx
    latex: Latex
    intersphinx_registry: IntersphinxRegistry
    html: Html
    numpydoc: Numpydoc

    class Config:
        extra = Extra.forbid
