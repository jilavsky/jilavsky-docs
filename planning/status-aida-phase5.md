# Status after phase 5 (AIDA screenshots and page review)

*Written 2026-11-16 by the agent that carried out `handoff-aida-bernardyn-phase5.md` in
`/Users/ilavsky/GitHub/Aida`. For Jan, ahead of the Christmas walk-through.*

## Summary

The work is on branch **`docs-phase5`** in Aida, on top of `main` (3c850a3). It is **not
pushed** and there is no PR yet: push and open a draft PR when you want the Read the Docs
preview.

- **Review the pattern first:** commit `964d7f2` holds the copied machinery, AIDA's
  `_package.py` and the window tour (`getting-started/gui-overview.md`), on its own.
- **Screenshots:** 29 automated and committed, 3 left for you (`% SCREENSHOT` comments in the
  pages, `automated: no` rows in the shot list). Every screenshot is under 300 KB (the largest is
  the window tour, 213 KB). The only PNGs over 300 KB are two hand-made concept figures that were
  already there (`fig-a`, `fig-c`).
- **Pages:** 17 of 18 reviewed and changed (labels, shots, CHECK notes). `index.md` is
  unchanged: the template cannot give it a shot (see "Template changes suggested").
- **Checks on the final branch:**
  - `sphinx-build -W --keep-going`: zero warnings.
  - `ruff check .` and `ruff format --check .`: clean.
  - `pytest --ignore=tests/ui`: 1836 passed.
  - `pytest tests/ui` (run separately, offscreen): 750 passed.
- **No package code changed** and no hook was added: every shot drives existing widgets and
  dialogs.
- **How it was done:** I did the machinery and the window tour. Three forks in separate
  worktrees then did the other pages in groups (guides A, guides B, getting-started and
  reference). I cherry-picked their commits (only the shot list conflicted, append-only) and
  re-ran every check on the merged branch.

Text that looks wrong is kept and marked with invisible `% CHECK(Jan): …` comments (43 of them);
`grep -rn "CHECK(Jan)" docs/` lists them all.

## Regenerating the screenshots

From the Aida repo root, in the `aida` conda env (`gui` extra installed):

```bash
python scripts/make_doc_screenshots.py                       # all 29, about 17 s on this Mac
python scripts/make_doc_screenshots.py --only gui-overview   # one page
python scripts/make_doc_screenshots.py --only gui-overview-01-window
python scripts/make_doc_screenshots.py --list
```

The same is now in `CONTRIBUTING.md`, section "Documentation screenshots".

- 26 of 29 images are byte-identical between runs. The three exceptions show a time:
  `moving-and-sharing-02`/`-03` (bundle creation time) and `coding-and-scripting-02` (run
  duration).
- A single `--only` run gives the same image as a full run.
- The script takes a lock on `/tmp/aida-docs.lock`, so two runs (e.g. two worktrees) never
  rebuild `/tmp/aida-docs` at the same time.

How the shots are made:

- AIDA's real `MainWindow` and dialogs, offscreen, at fixed sizes. The main window is 1600×940.
- **No model, no network, no key:** `aida.core.session.build_provider` is replaced with AIDA's
  own `MockProvider` for the run.
- **Conversations are seeded** into the scratch database through `ConversationStore` /
  `ArtifactStore` (`_package.seed_conversation`), from JSON files in `scripts/doc_shots/data/`.
  The pyIrena exchange is a question, `pyirena__pyirena_list_files`,
  `pyirena__pyirena_plot_iq`, the returned PNG and an answer.
- **The PNG** is pyIrena's tracked `data-explorer-02-graph.png` (three `validationData/unified/`
  files with their Unified models), cropped to the graph.
- **Neutral names:** profiles `local-ollama` (`http://localhost:11434/v1`) and `claude-direct`
  (a `secret_ref` only), workspace `saxs-analysis`, user `usaxs-team`, folders under
  `/tmp/aida-docs/`.
- **The running "pyirena" server in the MCP panel is a stand-in:** AIDA's own
  `tests/mock_mcp_server.py` registered under that name, so the panel shows it ticked without
  pyIrena installed. No shot calls its tools. The MCP dialog shots use a page-local `mcp.json`
  with the neutral command `/opt/conda/envs/pyirena/bin/pyirena-mcp`, which is never started.

## Settings isolation (proof)

`_package.isolate_settings(scratch)` runs before Qt or AIDA is imported, and again before every
shot. It does four things:

- sets `AIDA_HOME` to scratch, which holds config, conversations DB, artifacts, logs, skills and
  workflows;
- sets `HOME` to scratch, which covers the default records folder `~/Documents/Aida`; each shot
  also writes `records_dir` and `scratch_dir` under `/tmp/aida-docs` into the scratch
  `config.yaml`;
- sets `PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring`, so any keychain call raises
  `NoKeyringError`, which AIDA treats as "no secret";
- removes `AIDA_USER` and every `AIDA_SECRET_*` variable.

What I checked:

- **Files:** I recorded the size and modification time of every file in `~/.aida` and
  `~/Documents/Aida` (103 files) at 12:19. At 12:32 I compared again, after all three forks'
  runs and CLI tests and a full regeneration. `diff`: no changes, and
  `find ~/.aida ~/Documents/Aida -newer marker` is empty.
- **Preferences:** no `~/Library/Preferences` file matching aida or python was modified.
- **Keychain:** none of the 12 keychain items with service `aida` has a modification date of
  today (`security dump-keychain`, metadata only).
- **Forks:** each CLI example ran with its own `mktemp` `AIDA_HOME` and `HOME` and the fail
  backend.

## Per page

| Page | Automated shots | Left for Jan |
|---|---|---|
| getting-started/gui-overview | 01 window (12 callouts and a legend) | none |
| getting-started/installation | 01 onboarding (first-run dialog) | none |
| getting-started/concepts | none (hand-made figures kept) | none |
| guides/workspaces | 01 management, 02 edit form | none |
| guides/organizing-conversations | 01 sidebar, 02 manage users, 03 move to user | none |
| guides/workflows | 01 dialog, 02 repeating step, 03 schedules | none |
| guides/skills | 01 panel | none |
| guides/knowledge-bases | 01 dialog, 02 add form, 03 retrieval row | none |
| guides/documents | 01 attached, 02 settings OCR | none |
| guides/coding-and-scripting | 01 open in editor, 02 code editor, 03 scripting group | none |
| guides/moving-and-sharing | 01 export, 02 import contents, 03 import paths | none |
| guides/pyirena | 01 inline plot | 02 Add pyIrena confirmation |
| guides/bernardyn | none | 01 Add Bernardyn confirmation |
| guides/axis-camera | none (no AIDA window on the page) | none |
| reference/providers-and-secrets | 01 providers dialog, 02 profile form | none |
| reference/mcp-servers | 01 dialog, 02 server form | 03 Tools tab |
| reference/safety-and-permissions | 01 confirm dialog | none |
| reference/context-and-limits | 01 status bar (crop) | none |
| index | none | none (template limitation) |

Notes:

- **The three manual shots:**
  - The two Add confirmations are modal `QMessageBox.question` boxes and need a real install.
    Crop the PATH value; it shows home folders (see code issues).
  - The Tools tab needs a started real pyirena-mcp.
- **Section labels:** every touched section has a `(<page>-<section>)=` label, e.g.
  `gui-overview-sidebar`.
- **The window tour** keeps the existing text under a new "The window" section: the figure, then
  a numbered legend that links to the sections below it. File name unchanged.
- **Main-window shots** use a 530 px session column. At the app's default proportions the
  Folders section clips its buttons (see code issues).
- **Extra test data:** `organizing-conversations` adds `conversation-short-4.json` (user
  `saxs-student`). `knowledge-bases` uses an embedding profile `ollama-embed` (localhost, never
  contacted) and a never-built KB `usaxs-notes`. `workflows-03` writes one ok and one failed
  run into the scratch database, with fixed timestamps.

### Plain mismatches fixed (the only text changes)

- **mcp-servers:**
  - `aida mcp server test pyirena-mcp` → `aida mcp test pyirena-mcp` (twice).
  - `--arg --config` → `--arg=--config`, which argparse requires. One sentence added saying why.
- **concepts:**
  - `aida mcp server test pyirena-mcp` → `aida mcp test pyirena`.
  - "Providers… → Add" → "Configure → Providers… → Add…".
  - "Supports vision" → "Vision".
- **providers-and-secrets:** "(Settings → Providers)" → "(Configure → Providers…)".
- **context-and-limits:** "(trimming disabled)" → "Context: trimming disabled".
- **coding-and-scripting:**
  - The interpreter field is in "the session column's **Folders** section", not "the toolbar's
    Folders panel".
  - "</> Open in Editor" sits at the top right of a message, not under it.

## CHECK(Jan) items

### [behaviour]

- **guides/pyirena:** "~70 tools", "68 tool(s)" and "~10,200 tokens" (also used on bernardyn and
  in concepts, and "100+ tools" on mcp-servers). `aida mcp test pyirena` against pyIrena 1.2.1
  reports **28** tools. The context-cost argument for MCP groups rests on these numbers.
  *Resolved 2026-11-17 (AIDA PR #6): 28 tools, ~5,500 tokens.*

### Privacy, decide before the PR goes public

- **guides/axis-camera:**
  - The page is already published, and it shows a real home path (`/Users/ilavsky/...`),
    `/home/beams/USAXS` and the IP `10.54.122.46`.
  - A stray working note is published as written: "*NOTE* for axisserver withotu credentials…".
  - *Resolved 2026-11-17 (Jan): the IPs and paths stay. The cameras are behind the lab firewall,
    password-protected, and their addresses are already public. The stray note is still open.*

### By page

**getting-started/gui-overview**
- The File menu has "Export Setup…" and "Import Setup…"; the page doesn't list them.
- The session column has five sections: Folders, MCP Servers, Skills, Quick Tasks and Workspace
  Notes. Skills and Workspace Notes are not described, and the order differs.
- "labeled 'Workspace permissions' in the UI": the header says "Folders". The group-box title
  is cleared by `CollapsibleSection`.
- "Dialogs reachable from the Configure menu": the list includes the Code Editor (it opens from
  the toolbar) and leaves out Workflows… and Schedules….
- Status bar: the "Context: Nk / Mk (P%)" label is not mentioned here (it is in
  context-and-limits).

**getting-started/installation**
- With several pyirena-mcp installs, `add-pyirena` stops and asks for `--first` or
  `--command`. Same on concepts, pyirena and bernardyn, where it also breaks the
  Troubleshooting fixes `--force` and `--output-root`.
- `doctor` runs six checks the list leaves out.
- The `~/.aida` tree leaves out `schedules.yaml`, `*.lock`, `workflows/`, `knowledge/` and
  `tmp/`.

**getting-started/concepts**
- `make_figures.py --png` needs `cairosvg`, which is not declared anywhere.
- The Test button gives a "Profile OK" message box, not "green".
- The tool count and `--first` (above).

**guides/workspaces**
- The Fields table has no row for `use_ocr` (the Document OCR checkbox) or `notes` (Workspace
  Notes).

**guides/knowledge-bases**
- "Linking a KB to a workspace is CLI/config-file only": the Workspaces form now has a
  Knowledge bases tick list.
- `kb build`, `kb update` and `kb query`: not run, they need an embedding model.

**guides/workflows**
- `aida run` (both examples), `workflow run`, `schedule run` and `schedule watch`: not run,
  need a model.
- The `aida run` flag list leaves out `--user USER`.
- Not described: `schedule add --reuse-chat`, `--rollover-hours`, and the Schedules dialog's
  "Forget Pinned Chat" button and "chat reuse" line.

**guides/organizing-conversations**
- `aida chat --user`: not run, needs a model.
- `aida run my-workflow --user "…"` fails as written (exit 2): `aida run` needs `--workspace` and
  a prompt, and `aida workflow run` has no `--user`. Was
  `aida run --workspace W "prompt" --user …` meant?

**guides/coding-and-scripting**
- The Code Editor also opens from its own Open… button and from a file artifact's "Open in
  Code Editor"; the page lists two ways in.

**guides/pyirena** (besides the tool count)
- `add-pyirena` also writes a `PATH` env var, which is missing from the "configures" table.
- "Where it looks" leaves out `/opt/miniconda3/envs`, `/opt/anaconda3/envs` and the Windows
  `%LOCALAPPDATA%` / `%PROGRAMDATA%` folders.

**guides/bernardyn**
- `--first` (above); the token comparison depends on the pyIrena tool count.

**guides/axis-camera** (besides the privacy items)
- The printed source may lag the repo: the page says 10 tests pass, `~/GitHub/axis-cam-mcp`
  has 23.
- A10: `aida mcp server list` and `aida doctor` don't start the server, so they can't show it
  "came up"; `aida mcp test axis-cam` would.
- Not run, needs the camera: A8, A9, B3, B6. Not run: A7, which creates a conda environment.

**reference/providers-and-secrets**
- "All six are optional", but the table has ten rows.
- "opnerouter" looks like a typo.
- The form's "Secret value" field does store secrets in the keychain, which contradicts the
  paragraph saying the GUI cannot set them.

**reference/mcp-servers**
- `timeout_seconds` (the form's Timeout row) is not in the fields table.
- "100+ tools" (see the tool count above).

**reference/safety-and-permissions**
- The third button, and the CLI's `a` answer, appear only when the request can be remembered;
  otherwise the prompt is `[y/N]`.
- "FolderDisplay panel" is the Folders section; the class name appears nowhere in the window.

**reference/context-and-limits**
- `/compact` and Compact Conversation: not run, need a model.

## Runnable examples (step 4)

Every CLI example ran against a scratch `AIDA_HOME`/`HOME` with the fail keyring backend:

- **Ran as written (or after the plain fixes above):**
  - **Config:** `aida doctor`, `config export/import` (all forms), `config secret
    get/delete`.
  - **Workspaces and conversations:** `workspace new/edit/show/list` (every flag on the
    pages), `conversations list/export/gc`.
  - **Workflows and knowledge bases:** `workflow list/show/validate`, `schedule
    add/list/enable/disable/remove`, `kb add/list/show/edit/remove`.
  - **MCP:** `mcp server add/list/show/edit/remove --yes`, `mcp test` (mock server and real
    pyIrena/Bernardyn installs), `mcp group …`, the tool-permission commands, `mcp import`,
    `find-/add-pyirena`, `find-/add-bernardyn` with `--command` or `--first`.
  - **Other:** `documents figures`, `axis-cam-mcp --help`.
- **Failed as written:**
  - Fixed: `mcp server test`, `--arg --config`.
  - Marked CHECK: `aida run my-workflow --user`, and `add-pyirena`/`add-bernardyn` without
    `--first` when several installs exist.
- **Expected failures:**
  - `kb build/update/query` (no embedding profile).
  - `documents verify-ocr` (no key).
  - `config secret set` (keychain disabled on purpose).
  - `aida doctor` exits 1 with `[FAIL] provider:local-ollama: not reachable`.
- **Not run:**
  - Anything that needs a model (marked `% CHECK(Jan): not run, needs a model`).
  - pip/conda installs.
  - Camera and ssh steps.
  - `aida-gui` (covered by the shots).

## Code issues found (not fixed)

1. **`aida doctor` reports "keyring backend available" when no keychain is usable.**
   `secrets.keyring_available()` looks for "fail" in the class name, but keyring's fail backend
   class is just `Keyring` (module `keyring.backends.fail`). Found by two forks independently.
2. **Add pyIrena / Add Bernardyn write the full inherited `PATH` into `mcp.json`** and show it in
   the confirmation, home-folder entries included.
3. **`aida workspace edit --knowledge-bases` accepts unknown KB names** and reports "no
   warnings".
4. **Prompts crash without a TTY:** `aida config secret set PROFILE` (no value) and
   `aida mcp server remove NAME` (no `--yes`) end in an uncaught `EOFError` traceback when stdin
   is not a TTY.
5. **`aida conversations export` on an untitled conversation** writes a file name that repeats
   the id (`c269d046-c269d046.md`).
6. **`make_figures.py --png` needs `cairosvg`**, which is in no extra.
7. **Cosmetic:**
   - The session column's Folders section needs about 503 px, so at the default column
     proportions its buttons are clipped ("Save to Wor…", "MCP Serv…").
   - The Manage Users dialog's explanation label doesn't wrap, forcing the dialog to about
     980 px.
   - `aida config export` prints "1 workspaces".

No hooks were added to the package.

## Template changes suggested (not made)

- **`index.md` cannot carry a shot.** `_common.page_file("index")` matches every section's
  `index.md`, so the lookup is ambiguous. The template wants one screenshot on `index.md`.
  Either give the top-level page its own ID prefix (e.g. `home-01-…` mapped to `docs/index.md`)
  or let `page_file` prefer `docs/<page>.md`.
- **Default font size in `make_app()`.** Dialog shots inherited whatever font size an earlier
  shot had set, so images depended on run order. AIDA's `_package.make_app()` now applies the
  default once. Worth a line in the template's `_package.py` docstring ("set the app's default
  font in `make_app`").
- **A run lock.** AIDA's `_package` holds a lock while it rebuilds its shown folder
  (`/tmp/aida-docs`). Bernardyn will want the same if it uses a fixed folder.
- **Keeping a window alive:** a shot that returns only a child widget's grab (e.g.
  `window.sidebar`) can lose the window to garbage collection mid-shot. A note in `_example.py`
  ("keep a reference to the top-level window until you grab") would help.

## Notes for the walk-through

- **Start with `964d7f2`** (machinery and the window tour). If the tour's pattern is wrong
  (legend style, callout placement, which conversation is shown), the other main-window shots
  (pyirena, skills, sidebar, status bar) use the same setup.
- **Doing a manual shot:**
  1. Save it as `<page dir>/img/<page>/<id>.png`.
  2. Replace the `% SCREENSHOT` comment with a `figure` that has alt text and a caption.
  3. Set the row to `done` in `planning/docs-screenshots/SHOTLIST.md`.

  `pytest tests/test_doc_screenshots.py` catches anything out of step.
- **Leftovers:**
  - The forks' worktrees are in `Aida/.claude/worktrees/agent-*`, on branches
    `worktree-agent-*`; everything in them is cherry-picked. Delete them when convenient.
  - `/tmp/aida-sphinx-venv` is a throwaway Python 3.13 venv for the docs build. The `aida`
    env is 3.11, and `sphinx==9.2.0` needs 3.12 or newer.
- **Unrelated:** the uncommitted duplicate `html_copy_source = False` line in `docs/conf.py`
  on `main` was dropped before branching; the committed line is still there.
