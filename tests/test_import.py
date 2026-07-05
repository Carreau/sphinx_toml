"""Smoke tests: the package and its public surface import cleanly."""


def test_import_package():
    import sphinx_toml  # noqa: F401


def test_public_surface():
    import sphinx_toml

    assert callable(sphinx_toml.load_into_locals)
    # load_into_locals is the bound method of the module-level loader.
    assert sphinx_toml.load_into_locals == sphinx_toml.loader.load_into_locals


def test_version_is_a_string():
    import sphinx_toml

    assert isinstance(sphinx_toml.__version__, str)
