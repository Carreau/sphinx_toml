from __future__ import annotations
from typing import List

from pydantic import BaseModel, Field
from typing import List, Dict, Tuple, Optional, Any, _UnionGenericAlias


class SphinxModel(BaseModel):
    @classmethod
    def _flatten(cls, config):
        for key, value in config.items():
            field = cls.model_fields[key]
            field_a = field.annotation
            if type(field_a) is _UnionGenericAlias:
                field_a, the_none = field_a.__args__
                assert the_none is type(None), the_none
            if isinstance(field_a, type) and issubclass(field_a, SphinxModel):
                yield from field_a._flatten(value)
            else:
                yield key, value


class Autodoc(SphinxModel):
    autodoc_type_aliases: Optional[Dict[str, str]] = None

class Intersphinx(SphinxModel):
    intersphinx_mapping: Optional[Dict[str, InnerModel]] = None


class Ext(SphinxModel):
    autodoc: Autodoc
    intersphinx: Intersphinx


class Misc(SphinxModel):
    github_project_url: str


class Sphinx(SphinxModel):
    # -- Project information --
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-project

    project: str
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-copyright
    copyright: str

    # -- markup --
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-default_role
    default_role: Optional[str] = None

    # -- source-files --
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-source-files
    exclude_patterns: List[str]
    master_doc: str
    source_suffix: str

    # -- General Conf ––
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-extensions
    extensions: List[str]

    # -- Options for the Javascript domain --
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-modindex_common_prefix
    modindex_common_prefix: List[str] = None

    # -- Highlightning ––
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-pygments_styl
    pygments_style: str

    # TODO
    templates_path: Optional[List[str]] = None
    today_fmt: Optional[str] = None
    todo_include_todos: Optional[bool] = None  # sphinx.ext.todo  ?
    ext: Ext

    # Builder, html
    html: Optional[Html] = None

    class ConfigDic:
        extra = "forbid"


class IntersphinxRegistry(SphinxModel):
    packages: List[str]

    class ConfigDict:
        extra = "forbid"


class Latex(SphinxModel):
    latex_documents: Optional[List[Tuple[str, str, str, str, str, str]]] = None
    latex_use_modindex: bool
    texinfo_documents: Optional[
        List[Tuple[str, str, str, str, str, str, str, int]]
    ] = None
    latex_font_size: Optional[str] = None

    class ConfigDict:
        extra = "forbid"

    @classmethod
    def _flatten(cls, config):
        for k, v in super()._flatten(config):
            yield k, v


class Html(SphinxModel):
    html_theme: str
    html_static_path: Optional[List[str]] = None
    html_favicon: Optional[str] = None
    html_last_updated_fmt: Optional[str] = None
    htmlhelp_basename: str
    html_additional_pages: Optional[List[Tuple[str, str]]] = None
    html_theme_options: Optional[Dict[str, Any]] = None

    class ConfigDict:
        extra = "forbid"


class Numpydoc(SphinxModel):
    numpydoc_show_class_members: bool
    numpydoc_class_members_toctree: bool
    warning_is_error: bool

    class ConfigDict:
        extra = "forbid"


class InnerModel(BaseModel):
    url: str
    fallback: str


class Config(SphinxModel):
    sphinx: Sphinx
    latex: Optional[Latex] = None
    intersphinx_registry: Optional[IntersphinxRegistry] = None
    numpydoc: Optional[Numpydoc] = None
    # not in sphinx
    misc: Misc

    class ConfigDict:
        extra = "forbid"
