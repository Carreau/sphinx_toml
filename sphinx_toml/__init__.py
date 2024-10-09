"""
Minimal package to load data from a sphinx.toml file next to a conf.py file.

This is not dissimilar to https://pypi.org/project/sphinx-pyproject/ but
currently extends to a few more keys until those are standardized and moved into
a proper sphinx declarative configuration or into pyproject.toml.
"""

__version__ = "0.0.2"

import sys
from intersphinx_registry import get_intersphinx_mapping
from .models import Config

from typing import Any, List

if sys.version_info > (3, 11):
    import tomllib
else:
    import tomli as tomllib

with open("./sphinx.toml", "rb") as f:
    config = tomllib.load(f)
    # basic validation for now. What does not match
    c = Config(**config)


class Normaliser:
    key: str

    def normalise(data: Any) -> Any:
        pass


class IntersphinxMappingNormaliser:
    key = "intersphinx_mapping"

    def normalise(self, data, *, current_conf=None):
        mapping = {}
        for k, v in data.items():
            fallback = data[k]["fallback"]
            mapping[k] = tuple([data[k]["url"], None if fallback == "" else fallback])
        return mapping


class IntersphinxRegistry:
    key = "intersphinx_registry"

    def normalise(self, data, current_conf=None):
        mapping = get_intersphinx_mapping(packages=data["packages"])
        if "intersphinx_mapping" in current_conf:
            mapping.update(current_conf["intersphinx_mapping"])
        return {"intersphinx_mapping": mapping}


class HTML:
    key = "html"

    def normalise(self, data, current_conf=None):
        if "html_additional_pages" in data:
            data_toml = data["html_additional_pages"]
            data["html_additional_pages"] = {}
            for item in data_toml:
                data["html_additional_pages"][item[0]] = item[1]
        return data


class Loader:
    normalisers: List[Normaliser]

    def __init__(self, normalisers):
        self.normalisers = normalisers

    def load_into_locals(self, loc):
        with open("./sphinx.toml", "rb") as f:
            config = tomllib.load(f)
        sections = set(config.keys())

        for norm in self.normalisers:
            if norm.key in config:
                normalized = norm.normalise(config[norm.key], current_conf=loc)
                loc.update(normalized)
                sections.remove(norm.key)

        for s in sections:
            loc.update(config[s])


loader = Loader([IntersphinxMappingNormaliser(), IntersphinxRegistry(), HTML()])

load_into_locals = loader.load_into_locals
