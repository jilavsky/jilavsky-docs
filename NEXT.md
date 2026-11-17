# Where we are and what is next

*Restart point. Updated 2026-11-17. Read this first, then `PLAN.md` for the design.
Delete items as they are done.*

## State

| Repo | Branch | State |
|---|---|---|
| jilavsky-docs | main | Workflow and template on checkout v7 / setup-python v7 |
| pyirena | main | Phase 5 and template machinery merged. Draft PR #44: actions v7 |
| Bernardyn | main | Phase 5 and template machinery merged. Draft PR #6: actions v7 |
| Aida | main | Phase 5 and template machinery merged. Draft PR #9: actions v7 |

All three packages run identical screenshot machinery (only `_package.py` differs).

Phase 5 reports, with every `CHECK(Jan)` item, the code issues and the manual shots:
`planning/status-pyirena-phase5.md`, `planning/status-aida-phase5.md`,
`planning/status-bernardyn-phase5.md`.

## Next, in order

1. **Actions v7 PRs** (pyIrena #44, AIDA #9, Bernardyn #6): `actions/checkout` v4 → v7 and
   `actions/setup-python` v5 → v7 in every workflow. Merge when CI is green.
   Note: jilavsky-docs's own `docs.yml` had lost the setup-python bump. The merge commit
   `1332b04` (main into Dependabot #1) took the v5 line. It is restored in jilavsky-docs main.
2. Then the Christmas walk-through items, or **Later** (below).

## Template notes (change of 2026-11-16)

- `index-<nn>-…` shots belong to `docs/index.md`; `--keep` keeps the scratch folder.
- New helpers `refuse_message_boxes()` and `flush_deletes(app)` in `_common.py`. Bernardyn can
  replace its own `refuse()` and `flush_deletes(ctx)` with them; optional.
- Do **not** call `flush_deletes` from the clean-up loop: doing so crashed PySide6.
- Some AIDA shots are not reproducible run to run (timings, sidebar/import dialogs). Worth making
  them deterministic before relying on "regenerate and diff" there.

## For the Christmas walk-through (Jan)

- Every `CHECK(Jan)` note: `grep -rn "CHECK(Jan)" docs/` in each package; lists are in the
  status files.
- Manual shots: AIDA 3 (two Add-server confirmations, the MCP Tools tab), Bernardyn 1 (3-D
  waterfall), pyIrena's from its report. Each has a `% SCREENSHOT` comment and a `todo` row in
  `planning/docs-screenshots/SHOTLIST.md`.
- Code issues found during phase 5 (not fixed): pyIrena 13 groups, AIDA 7, Bernardyn 8, in the
  status files. Triage into issues or small PRs.

## Later

- Releases: pyIrena 1.3.0 (after validation, it changes results), Bernardyn 1.2.0. After each,
  set that RTD subproject's default version to `stable` (AIDA already can be).
- Phase 6: Anisa, pyNika (PLAN.md §7).

## Restarting

Open Claude Code in `~/GitHub/jilavsky-docs` and say: "Read NEXT.md and continue."
