# CLAUDE.md

Guidance for working in the `sphinx_toml` repository.

## What this project is

`sphinx_toml` is a small Python package that lets a Sphinx documentation build
load part of its configuration from a `sphinx.toml` file living next to
`conf.py`, instead of writing everything as Python in `conf.py`.

Usage, from a project's `conf.py`:

```python
from sphinx_toml import load_into_locals

load_into_locals(locals())
```

`load_into_locals` reads `./sphinx.toml`, transforms ("normalises") a handful of
sections into the shapes Sphinx expects, and injects the resulting names into the
mapping it is handed (normally `conf.py`'s `locals()`).

It is conceptually similar to [`sphinx-pyproject`](https://pypi.org/project/sphinx-pyproject/)
but covers a few extra keys that are not yet standardized into a declarative
Sphinx config or `pyproject.toml`.

## Layout

```
sphinx_toml/
  __init__.py    # Loader + Normaliser classes, module-level `loader` and `load_into_locals`
  models.py      # Pydantic models describing the sphinx.toml schema (currently NOT wired into loading)
pyproject.toml   # flit-based build, version/description are dynamic (read from __init__.py)
README.md
LICENSE          # MIT
```

There is currently **no unit-test suite and no linter configuration**. CI does
exist: `.github/workflows/ipython-docs.yml` is an integration guard that builds
[IPython](https://github.com/ipython/ipython)'s real documentation against the
`sphinx_toml` in the checkout (IPython's `docs/source/conf.py` calls
`load_into_locals`, and `sphinx_toml` is listed in its `docs/requirements.txt`),
so a change here that breaks IPython's doc build fails CI.

## Architecture

- **`Loader`** (`__init__.py`) holds an ordered list of `Normaliser` instances.
  `load_into_locals(loc)`:
  1. opens `./sphinx.toml` (relative to the cwd of the Sphinx build) with
     `tomllib`/`tomli`,
  2. pops the `sphinx_toml` section and applies any `[sphinx_toml.environ]`
     values to `os.environ`,
  3. runs each normaliser whose `key` matches a top-level TOML section,
     updating `loc` with the normalised output,
  4. copies any remaining (un-normalised) sections into `loc` verbatim.

- **Normalisers** each declare a `key` (the TOML section name) and a
  `normalise(self, data, *, current_conf=None)` method:
  - `IntersphinxMappingNormaliser` — turns `[intersphinx_mapping.<pkg>]` tables
    (`url` + `fallback`) into the `(url, fallback-or-None)` tuples Sphinx wants.
  - `IntersphinxRegistry` — resolves a package list through
    `intersphinx_registry.get_intersphinx_mapping`, merging any explicit mapping.
  - `HTML` — converts `html_additional_pages` from a list of pairs into a dict.
  - `SphinxNormalizer` — copies the `[sphinx]` section through, warns on a string
    `source_suffix`, and hoists `[sphinx.ext.autodoc]` keys up a level.

- **`models.py`** defines Pydantic models (`Config`, `Sphinx`, `Html`, `Latex`,
  `Numpydoc`, …) that describe the intended `sphinx.toml` schema. **These models
  are not currently used by the loader** — loading does no validation.

## Known rough edges (read before editing)

Treat these as landmines, not settled design:

- `Config` / `Extra` use Pydantic **v1** idioms while `pydantic` (v2) is the
  declared and installed dependency; they still work via v2's deprecation shim
  but should be migrated.
- `__init__.py` uses `if sys.version_info > (3, 11)` to choose `tomllib` vs
  `tomli`. This happens to be correct (`version_info` for 3.11.x compares
  greater than the 2-tuple `(3, 11)` because it carries extra elements), but it
  reads as if it means "> 3.11". Prefer the clearer `>= (3, 11)`.
- The base `Normaliser.normalise(data)` is missing `self`, and the two
  intersphinx normalisers have inconsistent `current_conf` signatures
  (keyword-only in some, positional in others).
- The loader is full of `print(...)` debug statements and writes to stdout during
  every build.
- Paths are hard-coded to `./sphinx.toml` relative to the process cwd.

## Conventions

- Python ≥ 3.10. Build backend is **flit_core**; version and description are
  `dynamic` and pulled from `sphinx_toml/__init__.py` (`__version__` and the
  module docstring). Bump the version there, not in `pyproject.toml`.
- Keep the public surface small: `load_into_locals` is the entry point users
  call. Adding a new supported TOML section usually means adding a `Normaliser`
  subclass and registering it in the module-level `loader` list.
- When adding a normaliser, also extend the Pydantic models in `models.py` so the
  schema stays documented, even while validation is not yet enforced.

## Verifying changes

There is no test harness yet, so verify manually:

```bash
python -c "import sphinx_toml"                       # import smoke test
python -c "from sphinx_toml.models import Config; Config.model_rebuild()"  # surfaces the Optinal typo
```

Ideally, create a throwaway dir with a minimal `sphinx.toml`, then run
`load_into_locals({})` from that dir and inspect the resulting dict.
