# Brief: move pyIrena's docs onto Read the Docs (phase 3)

*For an agent working in `/Users/ilavsky/GitHub/pyirena`. Written 2026-11-13 from
`/Users/ilavsky/GitHub/jilavsky-docs`. Reusable for AIDA and Bernardyn with the changes in the
last section.*

## Goal

Turn pyIrena's flat `docs/*.md` into a Sphinx/MyST site that builds on Read the Docs as the
subproject `pyirena` of `jilavsky-docs`, using the family template. Switch the GUI Help buttons to
it. **This phase moves and restructures; it does not rewrite content.** Text stays as it is apart
from fixing links, headings and the merges listed below. New tool-page drafts and screenshots are
a later phase.

Final URL: `https://jilavsky-docs.readthedocs.io/projects/pyirena/en/{stable|latest}/`.

## Read first

1. `/Users/ilavsky/GitHub/jilavsky-docs/PLAN.md`, §3 (layout and conventions) and §4.1 (the
   pyIrena move table) and §4.4 (transition stubs).
2. `/Users/ilavsky/GitHub/jilavsky-docs/templates/package-docs/README.md`, then the template files.
3. pyIrena's own `AGENTS.md`.

## Steps

Work on a new branch `docs-rtd` from `main`.

1. **Copy the template.** `.readthedocs.yaml` and `docs/conf.py`, `docs/requirements.txt`,
   `docs/_static/family.css` from `templates/package-docs/` into the repo, plus the section
   `index.md` files. Edit only the `PER-PACKAGE` block of `conf.py`. Keep everything else
   identical to the template; if something in the template has to change, stop and say so, so the
   template is fixed for every package.
2. **Move the files** per PLAN.md §4.1 with `git mv` (history is kept). Rename to lowercase
   kebab-case. List every page explicitly in its section's `index.md` (no globbing).
   Merges in the table (`unified_fit_gui.md` + `unified_fit_features.md`; the theory part of
   `sizes_methods.md` into `methods/`) are the only content edits beyond link fixes. Where the
   table looks wrong once you read a file, choose sensibly and list your choice in the PR text.
3. **Fix links.** Relative `.md` links between moved files, image paths, and links into the repo
   (`../pyirena/...`, `planning/...`): point those at GitHub URLs, because they are outside the
   docs site. Headings must form a valid hierarchy (one `#` per page) or MyST warns.
4. **Help-link helper.** Copy `templates/package-docs/pkg/_docs.py` to `pyirena/_docs.py`
   (`DIST = SUBPROJECT = "pyirena"`). Fill `HELP_TARGETS` for the 13 panels that open GitHub
   today, plus `"home": ""`. Find them with
   `grep -rn "blob/main/docs" pyirena/gui`.
5. **Switch the Help buttons** to `QDesktopServices.openUrl(QUrl(docs_url("<target>")))`. Keep
   `_docs.py` free of Qt.
6. **Tests.** pyIrena's tests live in `pyirena/tests/`, not top-level `tests/`:
   - Add `pyirena/tests/test_help_targets.py` from the template; its docs path is
     `Path(__file__).resolve().parents[2] / "docs"`.
   - `test_tool_registration.py::test_every_tool_has_a_gui_panel_and_docs` expects a flat
     `docs/<tool>_gui.md`. Change it to the new `docs/tools/<page>.md` names, ideally by checking
     against `HELP_TARGETS` so there is one source of truth.
   - `test_text_encoding_contract.py` scans only `docs/*.md`; make it `rglob("*.md")`.
   - `test_config_contract.py` reads `docs/batch_api.md`; update the path.
   - Run the full suite, not just these.
7. **Update every pointer to old doc paths**: `AGENTS.md` (the tool map and the "start here"
   table), `README.md`, and docstrings/comments (`grep -rn "docs/[A-Za-z_]*\.md" pyirena`).
   AGENTS.md must stay accurate: other agents navigate by it.
8. **Transition stubs.** For each of the 13 old GitHub Help paths (e.g. `docs/unified_fit_gui.md`),
   leave a one-line stub: `Moved to <https://jilavsky-docs.readthedocs.io/projects/pyirena/en/latest/tools/unified-fit.html>`.
   Add them to `LEGACY_GITHUB_STUBS` in `conf.py`. Released v1.2.1 opens these paths on `main`.
   Make sure the tests from step 6 don't count stubs as real pages.
9. **API reference.** `docs/reference/api.md`: autodoc only for the stable public API (look for
   what README/`batch_api.md`/`scattering_io_api.md` present as public, e.g. `pyirena.batch`,
   `pyirena.io`). Do not autodoc the GUI. Mock anything RTD cannot import.
10. **Build clean:** `pip install -r docs/requirements.txt && pip install -e . &&
    sphinx-build -W --keep-going -b html docs docs/_build/html`. Zero warnings. Add `docs/_build/`
    to `.gitignore`. Confirm `docs/` is still not in the wheel.
11. **CHANGELOG.md**: one entry (docs moved to Read the Docs; Help buttons open RTD).
12. Commit on `docs-rtd`. Do not push or open a PR until Jan says so. In the final report, give
    the mapping actually used (old file → new page), every judgment call, and anything left
    undone.

## Constraints

- No numerical or behavioural code changes beyond the Help-button URLs.
- No new runtime dependencies. Docs dependencies live only in `docs/requirements.txt`.
- Never bind the name `version` at module level in `conf.py` (Sphinx reads it as a setting).
- Do not add intersphinx entries for family projects that are not live yet. `igor` is live, and
  tool pages may link to the Irena manual with `` {doc}`igor:Irena/UnifiedFit` ``.
- Page names under `docs/tools/` become a frozen contract once released; choose them carefully now.

## What Jan does afterwards (not the agent)

On RTD: import pyirena as project `jilavsky-pyirena`, add it to `jilavsky-docs` as subproject
alias `pyirena`, default version `stable`, automation rule for tags `^v\d+\.\d+\.\d+$`, PR builds
on. Do **not** activate v1.2.1 or older tags (no Sphinx config). `stable` appears with the next
release.

## Reusing this brief for AIDA and Bernardyn

- Move table: PLAN.md §4.2 (AIDA) or §4.3 (Bernardyn) instead of §4.1.
- One Help button each (top page): `HELP_TARGETS = {"home": ""}`.
- AIDA: `src/` layout (`SRC_DIR = "../src"`, helper at `src/aida/_docs.py`), `DIST = "aida-workbench"`,
  `SUBPROJECT = "aida"`, tests in `tests/`; replace `DOCUMENTATION_URL` in
  `src/aida/ui/qt/main_window.py`. No stubs needed (it links the `docs/` folder, which remains).
- Bernardyn: `DIST = SUBPROJECT = "bernardyn"`; decide with Jan whether to keep the "open local
  docs for an editable checkout" fallback in `_documentation_url()`. Include
  `bernardyn/schemas/graph-package-v3.md` into `reference/` with `{include}`.
- Each repo's own tests may read `docs/` paths too: grep for them first.
