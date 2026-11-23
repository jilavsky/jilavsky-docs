# Where we are and what is next

*Restart point. Updated 2026-11-23. Read this first, then `PLAN.md` for the design.
Delete items as they are done; finished work goes to `CHANGELOG.md`.*

## State

Phases 1–5 and the first release of every package are done (see `CHANGELOG.md`). Released:
pyIrena 1.3.1, Bernardyn 1.2.0, AIDA 1.1.2 (PyPI distribution `aida-workbench`). All four sites
build; `stable` exists for the three packages; every Help-button target resolves on `stable`.

Health check of 2026-11-23: 109 pages crawled, no broken internal link.

## Next, in order

1. **Christmas walk-through (Jan).**
   - Every `CHECK(Jan)` note: `grep -rn "CHECK(Jan)" docs/` in each package (63 / 5 / 43 lines
     for pyIrena / Bernardyn / AIDA); lists are in `planning/status-*-phase5.md`.
   - Manual shots, 17 `todo` rows in total, in each package's
     `planning/docs-screenshots/SHOTLIST.md`: pyIrena 13, AIDA 3 (two Add-server confirmations, the MCP Tools tab), Bernardyn 1 (3-D
     waterfall). Each has a `% SCREENSHOT` comment next to the page text.
2. **Code issues found in phase 5 (not fixed)**: pyIrena 13 groups, AIDA 7, Bernardyn 8, in the
   status files. Triage into issues or small PRs. (Open code-review issues that already exist:
   Bernardyn #1, AIDA #2; pyIrena has none for these.)

## Small loose ends

- AIDA `CHANGELOG.md` links to `compare/v0.1.0b5...v0.1.0b6` and `b6...b7`; those tags were
  never pushed, so the links 404. Drop them or tag.
- Some AIDA screenshots are not reproducible run to run (timings, sidebar/import dialogs). Make
  them deterministic before relying on "regenerate and diff" there.
- Bernardyn can replace its own `refuse()` and `flush_deletes(ctx)` with the template's
  `refuse_message_boxes()` and `flush_deletes(app)` in `_common.py`. Optional.
- Do **not** call `flush_deletes` from the clean-up loop: doing so crashed PySide6.

## Later

- Phase 6: Anisa and pyNika (PLAN.md §7). Neither has a `docs/conf.py` yet (Anisa has only
  `docs/parameters.md`; pyNika has four loose pages). Add each to `intersphinx_mapping` and the
  navbar only after its RTD site is live.
- Igor manuals modernization (PLAN.md §8), separate branch in `SAXS_IgorCodeDocs`.

## Restarting

Open Claude Code in `~/GitHub/jilavsky-docs` and say: "Read NEXT.md and continue."
