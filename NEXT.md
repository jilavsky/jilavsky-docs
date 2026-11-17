# Where we are and what is next

*Restart point. Updated 2026-11-17. Read this first, then `PLAN.md` for the design.
Delete items as they are done.*

## State

| Repo | Branch | State |
|---|---|---|
| jilavsky-docs | main | Template `_common.py`: `scene_item_rect` fix of 2026-11-17 (see below) |
| pyirena | main | Phase 5 merged (#42). Draft PR #43 switches it to the template machinery |
| Bernardyn | main | Phase 5 (#3) and template sync (#4) merged |
| Aida | main | Phase 5 merged (#5). Draft PRs #6 and #7 open; Jan handles them |

Phase 5 reports, with every `CHECK(Jan)` item, the code issues and the manual shots:
`planning/status-pyirena-phase5.md`, `planning/status-aida-phase5.md`,
`planning/status-bernardyn-phase5.md`.

## Next, in order

1. **AIDA PRs #6 (tool count 28, axis-camera decision) and #7 (template sync):** Jan.
2. **pyIrena PR #43** (`docs-template-sync`): check CI, review, merge. The shared files are now
   identical to the template. pyIrena's own parts are in `scripts/doc_shots/_package.py`
   (`VALIDATION`, `TEST_DATA`, `wait_jobs(ctx, panel)`). 40/42 shots byte-identical.
   `data-explorer-01` is just out of date (identical to an old-scripts run): regenerate it on
   purpose if wanted. `saxs-morph-01` varies run to run (3-D view).
3. **Carry the `scene_item_rect` fix** to Bernardyn and AIDA: copy
   `templates/package-docs/scripts/doc_shots/_common.py` over theirs (AIDA after #7 is merged).
   The template version raised `AttributeError: QSize.toSize`. Neither package calls it, so
   this only keeps `_common.py` identical.
4. **pyIrena leftover fork worktrees:** four `.claude/worktrees/agent-*` exist. Check, as was
   done for AIDA, that their commits are on main before removing them and deleting their
   branches.

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
- Code issues found during phase 5 (not fixed): AIDA 7, Bernardyn 8, in the status files.
  Triage into issues or small PRs.

## Later

- Releases: pyIrena 1.3.0 (after validation, it changes results), Bernardyn 1.2.0. After each,
  set that RTD subproject's default version to `stable` (AIDA already can be).
- pyIrena Windows test `test_h5open.py::test_open_h5_opens_a_same_identity_file_independently`
  has failed on main since 2026-11-06 (PermissionError); separate fix.
- jilavsky-docs Dependabot PRs #1 (checkout v7) and #2 (setup-python v7): merge, then carry the
  versions into `templates/package-docs/.github/workflows/docs.yml` and the packages.
- Phase 6: Anisa, pyNika (PLAN.md §7).

## Restarting

Open Claude Code in `~/GitHub/jilavsky-docs` and say: "Read NEXT.md and continue."
