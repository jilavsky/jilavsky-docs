# Where we are and what is next

*Restart point. Updated 2026-11-17. Read this first, then `PLAN.md` for the design.
Delete items as they are done.*

## State

| Repo | Branch | State |
|---|---|---|
| jilavsky-docs | main | Template `_common.py` has the `scene_item_rect` fix (628676d) |
| pyirena | main | Phase 5 (#42) and template machinery (#43) merged |
| Bernardyn | main | #3, #4 merged. Draft PR #5: `scene_item_rect` fix |
| Aida | main | #5, #6, #7 merged. Draft PR #8: `scene_item_rect` fix |

All three packages now run the same screenshot machinery. After #5 and #8, `_common.py` is
identical everywhere.

Phase 5 reports, with every `CHECK(Jan)` item, the code issues and the manual shots:
`planning/status-pyirena-phase5.md`, `planning/status-aida-phase5.md`,
`planning/status-bernardyn-phase5.md`.

## Next, in order

1. **Bernardyn PR #5 and AIDA PR #8:** one-file copy of the template `_common.py`. Neither
   package calls `scene_item_rect`, so no image changes. Review and merge.
2. **pyIrena fork worktrees** (Jan; Claude was not permitted to delete them). Checked
   2026-11-17: all four have every commit on main (same patches). One holds an untracked
   `.scratch/` folder; its notes are now in `status-pyirena-phase5.md` item 13. So `--force` is
   needed for that one:
   `cd ~/GitHub/pyirena && for w in .claude/worktrees/agent-*; do git worktree remove --force "$w"; done && git branch -D $(git branch --list 'worktree-agent-*' --format='%(refname:short)')`
   Also listed: a locked worktree `/tmp/pyirena-head` (lock reason "initializing", at an old
   commit `67e0747`). It is probably stale: `git worktree unlock /tmp/pyirena-head && git
   worktree remove /tmp/pyirena-head` if nothing is using it.
3. Optional: regenerate pyIrena's out-of-date `data-explorer-01` image on purpose
   (`python scripts/make_doc_screenshots.py --only data-explorer-01-window`).
4. Then move on to the Christmas walk-through items or **Later** (below).

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
