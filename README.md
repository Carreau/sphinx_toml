# SPHINX_TOML

Partially load sphinx configuration from `sphinx.toml` situated in the same dir as conf.py.


## usage

in your `conf.py` file:

```python
from sphinx_toml import  load_into_locals

load_into_locals(locals())
```

