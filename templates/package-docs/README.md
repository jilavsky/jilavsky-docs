# Package docs template

Copy this into a family package repo to give it the standard docs layout (PLAN.md §3).

## Apply to a package

1. Copy `.readthedocs.yaml` and `docs/` to the repo root. Do not copy this README.
2. In `docs/conf.py`, edit only the `PER-PACKAGE` block (`PACKAGE`, `DIST`, `project`,
   `GITHUB_REPO`, `SRC_DIR`, `autodoc_mock_imports`, `LEGACY_GITHUB_STUBS`).
3. In `docs/_static/family.css`, set `--family-accent`.
4. In `docs/index.md` and `docs/reference/api.md`, replace `pyIrena` / `pyirena`.
5. Copy `pkg/_docs.py` to `<package>/_docs.py` (AIDA: `src/aida/_docs.py`); set `DIST` and
   `SUBPROJECT`.
6. Copy `tests/test_help_targets.py`; fix its import line.
7. Move the existing Markdown into the sections (see PLAN.md §4). List each page in its
   section's `index.md`.
8. Build: `pip install -r docs/requirements.txt && sphinx-build -W --keep-going -b html docs docs/_build/html`.
9. Add `docs/_build/` to `.gitignore`. Make sure `docs/` is not packaged into the wheel.
10. Switch the GUI Help buttons to
    `QDesktopServices.openUrl(QUrl(docs_url("<target>")))`.

## Keep the copies in sync

Everything outside the `PER-PACKAGE` block is meant to stay identical to this template, including
the `FAMILY` navbar and `requirements.txt` pins. When the template changes, diff each package's copy
against it.

A tool page starts from `docs/tools/_template.md` (excluded from the build).
