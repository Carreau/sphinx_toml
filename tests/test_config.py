import pytest
from pathlib import Path
from sphinx_toml import Loader

HERE = Path(__file__).parent

examples_path = list(HERE.glob("*.toml"))


@pytest.mark.parametrize("path", examples_path)
def test_load_example(path):
    loader = Loader([])
    loc = {}
    loader._load_into_locals(path.read_text(), loc)

    assert loc != {}
