"""End-to-end tests for ``load_into_locals`` driven by real ``sphinx.toml`` files.

Uses the ``run_loader`` fixture (see conftest.py), which writes the TOML to an
isolated tmp dir, chdirs into it, and returns the resulting ``loc`` mapping.
"""

import os


def test_sphinx_section_is_loaded(run_loader):
    loc = run_loader(
        """
        [sphinx]
        project = "demo"
        copyright = "2026, me"
        """
    )
    assert loc["project"] == "demo"
    assert loc["copyright"] == "2026, me"


def test_html_additional_pages_becomes_dict(run_loader):
    loc = run_loader(
        """
        [html]
        html_theme = "default"
        html_additional_pages = [["index", "index.html"]]
        """
    )
    assert loc["html_additional_pages"] == {"index": "index.html"}


def test_intersphinx_registry_resolves_packages(run_loader):
    loc = run_loader(
        """
        [intersphinx_registry]
        packages = ["python"]
        """
    )
    assert loc["intersphinx_mapping"]["python"] == ("https://docs.python.org/3/", None)


def test_registry_merges_mapping_already_in_conf(run_loader):
    # A conf.py may define intersphinx_mapping before calling load_into_locals.
    loc = run_loader(
        """
        [intersphinx_registry]
        packages = ["python"]
        """,
        initial={"intersphinx_mapping": {"mylib": ("https://example.com/", None)}},
    )
    assert loc["intersphinx_mapping"]["python"] == ("https://docs.python.org/3/", None)
    assert loc["intersphinx_mapping"]["mylib"] == ("https://example.com/", None)


def test_unknown_sections_are_copied_verbatim(run_loader):
    loc = run_loader(
        """
        [numpydoc]
        numpydoc_show_class_members = false
        warning_is_error = true
        """
    )
    # numpydoc has no normaliser, so its keys land in loc unchanged.
    assert loc["numpydoc_show_class_members"] is False
    assert loc["warning_is_error"] is True


def test_environ_side_effect_sets_os_environ(run_loader, monkeypatch):
    monkeypatch.delenv("SPHINX_TOML_TEST_VAR", raising=False)
    run_loader(
        """
        [sphinx_toml.environ]
        SPHINX_TOML_TEST_VAR = "hello"

        [sphinx]
        project = "demo"
        """
    )
    assert os.environ["SPHINX_TOML_TEST_VAR"] == "hello"


def test_sphinx_toml_section_is_not_leaked_into_loc(run_loader):
    loc = run_loader(
        """
        [sphinx_toml.environ]
        FOO = "bar"

        [sphinx]
        project = "demo"
        """
    )
    # The sphinx_toml meta-section is popped, not copied into conf.
    assert "sphinx_toml" not in loc
    assert "environ" not in loc


def test_autodoc_keys_are_hoisted(run_loader):
    loc = run_loader(
        """
        [sphinx]
        project = "demo"

        [sphinx.ext.autodoc]
        autodoc_type_aliases = {x = "y"}
        """
    )
    assert loc["autodoc_type_aliases"] == {"x": "y"}


def test_missing_file_raises(tmp_path, monkeypatch):
    from sphinx_toml import load_into_locals

    monkeypatch.chdir(tmp_path)
    try:
        load_into_locals({})
    except FileNotFoundError:
        pass
    else:  # pragma: no cover
        raise AssertionError("expected FileNotFoundError when sphinx.toml is absent")
