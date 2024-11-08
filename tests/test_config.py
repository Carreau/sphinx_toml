import pytest
from pathlib import Path
from sphinx_toml import Loader

examples_path = list(Path(".").glob("*.toml"))


@pytest.mark.parametrize("path", examples_path)
def test_load_example(path):
    loader = Loader([])
    loader._load_into_locals(path.read_text(), {})
