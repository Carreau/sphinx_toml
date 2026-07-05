"""Shared pytest fixtures for the sphinx_toml test suite."""

import pytest

from sphinx_toml import Loader, load_into_locals


@pytest.fixture
def run_loader(tmp_path, monkeypatch):
    """Write a ``sphinx.toml`` and run ``load_into_locals`` from that directory.

    ``load_into_locals`` reads ``./sphinx.toml`` relative to the process cwd, so
    the fixture chdirs into an isolated ``tmp_path`` before loading.

    Returns a callable ``run(toml_text, initial=None) -> dict`` giving the
    ``loc`` mapping after loading (``initial`` seeds it, mirroring a ``conf.py``
    that has already defined some names).
    """

    def run(toml_text, initial=None):
        (tmp_path / "sphinx.toml").write_text(toml_text)
        monkeypatch.chdir(tmp_path)
        loc = dict(initial or {})
        load_into_locals(loc)
        return loc

    return run
