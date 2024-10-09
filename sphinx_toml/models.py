from typing import List

from pydantic import BaseModel, Field, Extra
from typing import List, Dict, Tuple, Optional


class Sphinx(BaseModel):
    autodoc_type_aliases: Optional[Dict[str, str]] = None
    copyright: str
    default_role: str
    exclude_patterns: List[str]
    extensions: List[str]
    github_project_url: str
    master_doc: str
    modindex_common_prefix: List[str] = None
    pygments_style: str
    project: str
    source_suffix: str
    templates_path: Optional[List[str]] = None
    today_fmt: Optional[str] = None

    # class Config:
    #    extra = Extra.forbid


class IntersphinxRegistry(BaseModel):
    packages: List[str]

    class Config:
        extra = Extra.forbid


class Latex(BaseModel):
    latex_documents: Optional[List[Tuple[str, str, str, str, str, str]]] = None
    latex_use_modindex: bool
    texinfo_documents: Optional[
        List[Tuple[str, str, str, str, str, str, str, int]]
    ] = None
    latex_font_size: Optional[str] = None

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


class InnerModel(BaseModel):
    url: str
    fallback: str


class Config(BaseModel):
    sphinx: Sphinx
    latex: Latex
    intersphinx_registry: Optional[IntersphinxRegistry] = None
    html: Html
    numpydoc: Numpydoc
    intersphinx_mapping: Dict[str, InnerModel]

    class Config:
        extra = Extra.forbid
