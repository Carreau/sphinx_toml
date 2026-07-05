"""Tests for the Pydantic schema in ``sphinx_toml.models``.

The models are not yet wired into loading (see plan.md), but they document the
intended ``sphinx.toml`` schema. These tests guard that they at least build and
validate a realistic config, so wiring them up later is a small step.
"""

import pytest
from pydantic import ValidationError

from sphinx_toml.models import Config, Html, IntersphinxRegistry

VALID_SPHINX = {
    "copyright": "2026, me",
    "exclude_patterns": ["_build"],
    "extensions": ["sphinx.ext.autodoc"],
    "github_project_url": "https://github.com/example/demo",
    "master_doc": "index",
    "pygments_style": "default",
    "project": "demo",
    "source_suffix": ".rst",
}


def test_models_rebuild():
    # Forward references (SphinxExt, ...) must resolve. This is what regressed
    # with the old ``Optinal`` typo.
    Config.model_rebuild()


def test_config_validates_a_minimal_config():
    cfg = Config.model_validate({"sphinx": dict(VALID_SPHINX)})
    assert cfg.sphinx.project == "demo"


def test_config_rejects_unknown_top_level_section():
    with pytest.raises(ValidationError):
        Config.model_validate({"sphinx": dict(VALID_SPHINX), "bogus": {}})


def test_html_model_forbids_extra_keys():
    with pytest.raises(ValidationError):
        Html.model_validate(
            {"html_theme": "furo", "htmlhelp_basename": "demo", "nope": 1}
        )


def test_intersphinx_registry_model_requires_packages():
    with pytest.raises(ValidationError):
        IntersphinxRegistry.model_validate({})
    assert IntersphinxRegistry.model_validate({"packages": ["python"]}).packages == [
        "python"
    ]
