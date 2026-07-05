# Project Review & Improvement Plan — `sphinx_toml`

A prioritized plan to take `sphinx_toml` from a working-but-rough prototype to a
maintainable, tested package. Ordered by impact; each item is independently
shippable.

## Summary of current state

The package works for its author's own docs builds but carries several latent
bugs, dead code, and no safety net.

---

## P0 — Correctness bugs (fix first)

1. **`Normaliser.normalise` missing `self`.** The base class method signature is
   `def normalise(data)`. Give it `self` and a consistent
   `normalise(self, data, *, current_conf=None)` signature across all
   normalisers (two of them currently differ on whether `current_conf` is
   keyword-only).

**Verification:** `python -c "import sphinx_toml"` succeeds; exercise each
normaliser via a minimal `sphinx.toml`. Test under 3.10 and 3.11 if possible.

> Note: `if sys.version_info > (3, 11)` in `__init__.py` is **not** a bug —
> `version_info` for any 3.11.x compares greater than the 2-tuple `(3, 11)`, so
> `tomllib` is correctly selected on 3.11. It is only stylistically confusing;
> changing it to `>= (3, 11)` is a readability cleanup, not a fix.

---

## P1 — Wire up validation & modernize Pydantic

2. **Actually use the `models.Config`.** Today the Pydantic models are dead
   code. In `load_into_locals`, parse the loaded TOML through `Config` (e.g.
   `Config.model_validate(config)`) to get early, clear errors instead of
   silent misconfiguration. Decide whether validation is strict (fail the build)
   or advisory (warn) — likely warn first, then tighten.

3. **Migrate to Pydantic v2 idioms.** Replace `class Config: extra = Extra.forbid`
   with `model_config = ConfigDict(extra="forbid")` and drop the
   `from pydantic import ... Extra` import (`Extra` is deprecated in v2). Remove
   the unused `Field` import. Pin `pydantic>=2` in `pyproject.toml`.

4. **Reconcile schema with normaliser output.** The models describe the *input*
   TOML, but some normalisers reshape data (e.g. `intersphinx_mapping` tuples,
   `html_additional_pages` dict, autodoc hoisting). Document which model
   describes input vs. output, and make sure every supported section has a model.

---

## P2 — Robustness & UX

5. **Replace `print(...)` with `logging`.** The loader prints on every build.
   Route diagnostics through the standard `logging` module (or Sphinx's logger)
   at `debug`/`info` level so builds are quiet by default.

6. **Make the `sphinx.toml` path configurable / robust.** It is hard-coded to
   `./sphinx.toml` relative to the process cwd. Accept an optional path argument,
   or resolve relative to the caller's `conf.py`. Raise a clear error when the
   file is missing.

7. **Guard the environ side effect.** `[sphinx_toml.environ]` mutates
   `os.environ` unconditionally and prints each key. Keep it, but log at debug
   level and document the behavior prominently (it is surprising).

---

## P3 — Project hygiene

8. **Add a test suite.** Create `tests/` with:
    - an import smoke test,
    - fixture `sphinx.toml` files exercising each normaliser,
    - a test that `load_into_locals({})` produces the expected dict.
    Use `pytest`; add a `[project.optional-dependencies] test = ["pytest"]`.

9. **Add CI.** A GitHub Actions workflow running the test suite on Python
    3.10 / 3.11 / 3.12.

10. **Add linting/formatting.** `ruff` (lint + format) with a minimal config;
    it flags the unused imports and the missing `self`.

11. **Expand the README.** Document every supported `sphinx.toml` section with a
    complete example file, and describe the environ and intersphinx-registry
    features. Add a `CHANGELOG`.

12. **Metadata polish.** The `pyproject.toml` MIT classifier and `LICENSE`
    should match; consider adding `Documentation` / `Source` URLs and a
    `Bug Tracker` entry.

---

## Suggested sequencing

- **Milestone 1 (bugs):** P0 #1 + a smoke test (P3 #8 partial) + CI (P3 #9).
  This makes the package correct and keeps it correct.
- **Milestone 2 (validation):** P1 #2–#4, modernizing to Pydantic v2 and turning
  the models into a real schema check.
- **Milestone 3 (polish):** P2 #5–#7 and remaining P3 items.

Each milestone is a self-contained PR-sized unit of work.
