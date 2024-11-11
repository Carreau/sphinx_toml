from __future__ import annotations
from typing import List

from pydantic import BaseModel, Field, Extra
from typing import List, Dict, Tuple, Optional, Any


class Autodoc(BaseModel):
    autodoc_type_aliases: Optional[Dict[str, str]] = None


class Ext(BaseModel):
    autodoc: Autodoc

class Sphinx(BaseModel):
    copyright: str
    default_role: Optional[str] = None
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
    todo_include_todos: Optional[bool] = None  # sphinx.ext.todo  ?
    ext: Ext

    class Config:
        extra = Extra.forbid


class IntersphinxRegistry(BaseModel):
    packages: List[str]

    class ConfigDict:
        extra = "forbid"


class Latex(BaseModel):
    latex_documents: Optional[List[Tuple[str, str, str, str, str, str]]] = None
    latex_use_modindex: bool
    texinfo_documents: Optional[
        List[Tuple[str, str, str, str, str, str, str, int]]
    ] = None
    latex_font_size: Optional[str] = None

    class ConfigDict:
        extra = "forbid"


class Html(BaseModel):
    html_theme: str
    html_static_path: Optional[List[str]] = None
    html_favicon: Optional[str] = None
    html_last_updated_fmt: Optional[str] = None
    htmlhelp_basename: str
    html_additional_pages: Optional[List[Tuple[str, str]]] = None
    html_theme_options: Optional[Dict[str, Any]] = None

    class ConfigDict:
        extra = "forbid"


class Numpydoc(BaseModel):
    numpydoc_show_class_members: bool
    numpydoc_class_members_toctree: bool
    warning_is_error: bool

    class ConfigDict:
        extra = "forbid"


class InnerModel(BaseModel):
    url: str
    fallback: str


class Config(BaseModel):
    sphinx: Sphinx
    latex: Optional[Latex] = None
    intersphinx_registry: Optional[IntersphinxRegistry] = None
    html: Optional[Html] = None
    numpydoc: Optional[Numpydoc] = None
    intersphinx_mapping: Optional[Dict[str, InnerModel]] = None

    class ConfigDict:
        extra = "forbid"
