"""Unit tests for each Normaliser, calling ``normalise`` directly.

These are characterisation tests: they pin down what the normalisers do
*today* so that later refactors (see plan.md) are caught, quirks included.
"""

import warnings

import pytest

from sphinx_toml import (
    HTML,
    IntersphinxMappingNormaliser,
    IntersphinxRegistry,
    SphinxNormalizer,
)


class TestIntersphinxMappingNormaliser:
    def test_url_and_fallback_become_a_tuple(self):
        data = {"numpy": {"url": "https://numpy.org/doc/", "fallback": "/local"}}
        out = IntersphinxMappingNormaliser().normalise(data)
        assert out == {"numpy": ("https://numpy.org/doc/", "/local")}

    def test_empty_fallback_becomes_none(self):
        data = {"numpy": {"url": "https://numpy.org/doc/", "fallback": ""}}
        out = IntersphinxMappingNormaliser().normalise(data)
        assert out == {"numpy": ("https://numpy.org/doc/", None)}

    def test_keys_are_the_package_names(self):
        # Note: the normaliser returns {pkg: tuple}, not {"intersphinx_mapping": ...}.
        data = {
            "python": {"url": "https://docs.python.org/3/", "fallback": ""},
            "numpy": {"url": "https://numpy.org/doc/", "fallback": ""},
        }
        out = IntersphinxMappingNormaliser().normalise(data)
        assert set(out) == {"python", "numpy"}


class TestIntersphinxRegistry:
    def test_resolves_packages_from_registry(self):
        out = IntersphinxRegistry().normalise({"packages": ["python"]}, current_conf={})
        assert out == {
            "intersphinx_mapping": {"python": ("https://docs.python.org/3/", None)}
        }

    def test_merges_explicit_mapping_from_current_conf(self):
        current_conf = {
            "intersphinx_mapping": {"mylib": ("https://example.com/", None)}
        }
        out = IntersphinxRegistry().normalise(
            {"packages": ["python"]}, current_conf=current_conf
        )
        mapping = out["intersphinx_mapping"]
        assert mapping["python"] == ("https://docs.python.org/3/", None)
        assert mapping["mylib"] == ("https://example.com/", None)

    def test_explicit_mapping_wins_over_registry(self):
        current_conf = {
            "intersphinx_mapping": {"python": ("https://override/", "/fallback")}
        }
        out = IntersphinxRegistry().normalise(
            {"packages": ["python"]}, current_conf=current_conf
        )
        assert out["intersphinx_mapping"]["python"] == ("https://override/", "/fallback")


class TestHTML:
    def test_additional_pages_list_of_pairs_becomes_dict(self):
        data = {
            "html_theme": "default",
            "html_additional_pages": [["index", "index.html"], ["about", "about.html"]],
        }
        out = HTML().normalise(data)
        assert out["html_additional_pages"] == {
            "index": "index.html",
            "about": "about.html",
        }

    def test_other_keys_pass_through_untouched(self):
        data = {"html_theme": "furo", "html_static_path": ["_static"]}
        out = HTML().normalise(data)
        assert out["html_theme"] == "furo"
        assert out["html_static_path"] == ["_static"]

    def test_no_additional_pages_is_a_noop(self):
        data = {"html_theme": "default"}
        out = HTML().normalise(data)
        assert out == {"html_theme": "default"}


class TestSphinxNormalizer:
    def test_plain_section_passes_through(self):
        data = {"project": "demo", "copyright": "2026"}
        out = SphinxNormalizer().normalise(data)
        assert out == {"project": "demo", "copyright": "2026"}

    def test_string_source_suffix_warns_and_is_wrapped(self):
        with pytest.warns(UserWarning, match="source_suffix"):
            out = SphinxNormalizer().normalise({"source_suffix": ".rst"})
        assert out["source_suffix"] == {".rst": "restructuredtext"}

    def test_dict_source_suffix_is_left_alone_without_warning(self):
        mapping = {".rst": "restructuredtext", ".md": "markdown"}
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            out = SphinxNormalizer().normalise({"source_suffix": dict(mapping)})
        assert out["source_suffix"] == mapping

    def test_autodoc_keys_are_hoisted_up_one_level(self):
        data = {
            "project": "demo",
            "ext": {"autodoc": {"autodoc_type_aliases": {"x": "y"}}},
        }
        out = SphinxNormalizer().normalise(data)
        # hoisted to the top level ...
        assert out["autodoc_type_aliases"] == {"x": "y"}
        # ... and removed from ext.
        assert out["ext"] == {}

    def test_non_dict_raises(self):
        with pytest.raises(AssertionError):
            SphinxNormalizer().normalise(["not", "a", "dict"])
