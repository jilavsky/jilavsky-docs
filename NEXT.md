# Where we are and what is next

*Restart point. Updated 2026-11-16, end of day. Read this first, then `PLAN.md` for the design.
Delete items as they are done.*

## State

| Repo | Branch | State |
|---|---|---|
| jilavsky-docs | main | Template has today's screenshot-machinery fixes (see "Template sync") |
| pyirena | main | Phase 5 merged (#42). Has its own older copy of the screenshot machinery |
| Bernardyn | main | Phase 5 merged (#3) |
| Aida | main | Windows fix `ffac4ef` on main. **Phase 5 PR #5 still an open draft**: main is merged into it, CI was rerunning with the fix |

Phase 5 reports, with every `CHECK(Jan)` item, the code issues and the manual shots:
`planning/status-pyirena-phase5.md`, `planning/status-aida-phase5.md`,
`planning/status-bernardyn-phase5.md`.

## Next, in order

1. **AIDA PR #5:** if CI is green, mark it ready and merge.
2. **AIDA `guides/axis-camera.md` privacy:** already live on `latest` and `stable`. It shows a real
   home path, `/home/beams/USAXS`, the IP `10.54.122.46` and a stray working note. Decide what
   to replace them with, then fix in a small AIDA docs PR.
3. **AIDA [behaviour]:** the pages say "~70 tools" / "~10,200 tokens" for pyIrena's MCP server;
   the measured count against pyIrena 1.2.1 is 28. Jan decides the numbers.
4. **Template sync** (below) into Bernardyn and AIDA, then switch pyIrena to the template copy.
5. Remove AIDA's leftover fork worktrees:
   `git -C ~/GitHub/Aida worktree list`, then `git worktree remove` each `.claude/worktrees/agent-*`
   and delete the `worktree-agent-*` branches.

## Template sync (template change of 2026-11-16)

Copy these unchanged from `templates/package-docs/` into each package (AIDA after #5 is merged):
`scripts/make_doc_screenshots.py`, `scripts/doc_shots/_common.py`,
`scripts/doc_shots/_example.py`. `_package.py` is not copied; its new docstrings are guidance.

What changed:
- `index-<nn>-…` shots belong to `docs/index.md`.
- `--keep`; the scratch folder is otherwise deleted after the run.
- One failing `close()` in clean-up no longer ends the run.
- New helpers `refuse_message_boxes()` and `flush_deletes(app)` in `_common.py`.
  - Bernardyn can replace its own `refuse()` and `flush_deletes(ctx)` with them; optional.
  - Do **not** call `flush_deletes` from the clean-up loop: doing so crashed PySide6.

Checked: Bernardyn's 13 shots with the new files gave byte-identical images and the test passes.

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
