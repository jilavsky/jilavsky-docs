# Changelog

## Unreleased

- 2026-11-23: Health check after the first releases. pyIrena 1.3.1, Bernardyn 1.2.0 and AIDA 1.1.2
  are on PyPI with their Help buttons on Read the Docs. `stable` exists for all three; all 19 Help
  targets (including anchors) resolve on it; a crawl of the four sites (109 pages) found no broken
  internal link. Docs CI green in all four repos. NEXT.md reduced to the walk-through, the
  phase-5 code issues and Phase 6.
- 2026-11-23: RTD setup finished: parent `jilavsky-docs` with subprojects `pyirena`, `bernardyn`,
  `aida`; tag automation; pull-request builds. pyIrena and AIDA default to `stable`.
- 2026-11-17: GitHub Actions on checkout v7 / setup-python v7 (repo and template). Phase 5 done
  in all three packages: tool pages, shot lists, automated screenshots; reports in
  `planning/status-*-phase5.md`.
- 2026-11-16: Template: family screenshot machinery (`scripts/make_doc_screenshots.py`,
  `scripts/doc_shots/`, `tests/test_doc_screenshots.py`, `SHOTLIST.md`); page sources hidden;
  tool-page section labels; `refuse_message_boxes()` and `flush_deletes(app)` helpers.
- 2026-11-13: Template: docs CI workflow and Dependabot for packages; `ruff format`-clean
  `conf.py`; NumPy docstrings on; optional sections; per-package accent colours with dark
  theme. pyIrena, Bernardyn and AIDA moved to the template (branches `docs-rtd`).
- 2026-11-13: Repo created. Family home page (which tool, installation, data formats, workflows,
  Igor manuals, Irena ↔ pyIrena map, citing), package docs template, RTD config, CI.
