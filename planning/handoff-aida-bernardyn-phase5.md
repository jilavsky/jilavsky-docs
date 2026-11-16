# Brief: AIDA and Bernardyn screenshots and page review (phase 5)

*For an agent working in `/Users/ilavsky/GitHub/Aida` or `/Users/ilavsky/GitHub/Bernardyn`.
Written 2026-11-16 after pyIrena phase 5 was merged (pyirena PR #42). One session per repo; the
two can run at the same time.*

## Goal

Same aim as pyIrena's phase 5: over the Christmas break Jan mostly **checks text and takes the
few screenshots that need judgment**. AIDA and Bernardyn are each one main window used through
task guides, not a set of tool windows, so:

- **no `tools/` section**; the "window" pattern goes into one **window tour** page;
- **screenshots go into the existing pages** where they help (getting-started, guides);
- the same screenshot machinery, shot list, hidden placeholders and test as pyIrena, from the
  family template.

**Reorganize and illustrate; do not rewrite.** Do not change any statement about behaviour,
defaults or results unless it is a plain mismatch with the code (a renamed button), and list
every such change. Doubtful text is kept and marked `% CHECK(Jan): …`.

## Read first

1. `/Users/ilavsky/GitHub/jilavsky-docs/PLAN.md` §3 (layout, conventions, labels, working notes)
   and §9 (screenshots).
2. `/Users/ilavsky/GitHub/jilavsky-docs/templates/package-docs/README.md`, sections "Tool pages",
   "Working notes in pages", "Screenshots"; then `templates/package-docs/scripts/` and
   `tests/test_doc_screenshots.py`.
3. `/Users/ilavsky/GitHub/jilavsky-docs/planning/status-pyirena-phase5.md`: how pyIrena did it,
   what went wrong, the "Notes for Jan's walk-through".
4. pyIrena's merged pages as the model, e.g.
   <https://jilavsky-docs.readthedocs.io/projects/pyirena/en/latest/tools/unified-fit.html>
   (source: `/Users/ilavsky/GitHub/pyirena/docs/tools/unified-fit.md`).
5. The repo's own `AGENTS.md` / `CLAUDE.md`.

## Work

Branch `docs-phase5` from an up-to-date `main`.

### 1. Copy the screenshot machinery from the template

`scripts/make_doc_screenshots.py`, `scripts/doc_shots/` (`__init__.py`, `_common.py`,
`_example.py`, `_package.py`), `tests/test_doc_screenshots.py`,
`planning/docs-screenshots/SHOTLIST.md`. Edit **only** `scripts/doc_shots/_package.py`:

- `DATA_ROOT`: where the tracked inputs are (Bernardyn: `testData/`; AIDA: see below).
- `CALLOUT_FILL`: keep the orange unless it clashes with the window.
- `isolate_settings(scratch)`: every place the package reads or writes user state must point
  into `scratch`. The developer's real settings, workspaces, conversations, keychain and
  `~/.pyirena` are never read or written. Prove it in the report (e.g. compare modification times
  before and after a run).
- `make_app()`: offscreen `QApplication`, light theme, window-geometry persistence off, as the
  real app sets them up (organisation/application names, theme).

If the template needs a change, describe it in the report rather than editing it, so all three
packages change together.

### 2. Window tour page

- **AIDA:** `getting-started/gui-overview.md` becomes the tour: one annotated full-window shot
  (numbered callouts from widget geometry) and a numbered legend, then the existing text
  arranged under it. Keep the file name (no Help button points at it, but links do).
- **Bernardyn:** add `getting-started/window-tour.md` (the window parts, with an annotated shot
  and legend). Move into it the window-description parts of `guides/user-guide.md`, leaving a
  link behind. Also add `getting-started/quickstart.md`: a first figure in about 10 minutes from
  a file in `testData/` (open, add the data and a pyIrena fit, style, export PNG), with a shot per
  step where it helps. List it in `getting-started/index.md`.
- Section labels follow the convention `(<page>-<section>)=`.

### 3. Screenshots in the other pages

Go through every page and add shots where a reader would otherwise have to guess what to look
at (a dialog, a menu, the state after an action). A typical guide gets 1–3; reference pages
usually none. Automate what can be automated; leave the rest as `% SCREENSHOT` comments with an
`automated: no` row explaining what to set up.

### 4. Runnable examples

Every code block a user would copy must run as written, or be fenced as `text` with a note why
not. Run each and say so in the report.
- **Bernardyn:** `guides/headless-recipes.md` and the API on `reference/api.md`, on scratch
  copies of `testData/` files.
- **AIDA:** CLI commands that need no model (`aida doctor`, config, workspace, skills, kb
  commands, …) against a scratch `AIDA_HOME`. Commands that need a live model are not run; mark
  them `% CHECK(Jan): not run, needs a model`.

### 5. Review notes

Mark text that has drifted from the code with `% CHECK(Jan): …` (renamed buttons, menus that
moved, missing options, stale paths), as pyIrena did. Scientific or behavioural doubts get
**[behaviour]** at the start of the comment.

### 6. Code issues

Do not fix package code on `docs-phase5`. If you find a bug, list it in the report; if Jan asks
for a fix, it goes on its own branch and PR (lesson from pyIrena, where a fix that changed a
saved-file name rode along with the docs PR). A tiny hook that a window needs to be driven by
the script is allowed; list it.

## Package specifics

### AIDA

- All state lives under `AIDA_HOME` (`src/aida/config/paths.py`): config, conversations
  database, artifacts, logs, skills, workflows. `isolate_settings` sets `AIDA_HOME` to the
  scratch folder. Check that the keychain is not touched (providers with `secret_ref` only, or
  the `AIDA_SECRET_<PROFILE>` environment variable with a dummy value).
- **No live model, no network, no real key in any shot.** Show conversations by **seeding them
  into the scratch database through AIDA's own persistence API** (the tests in `tests/` show how
  conversations, messages, tool calls and images are created). Use a realistic exchange with
  pyIrena: a user question, a tool call, a returned PNG plot, an answer. Take any PNG from a
  tracked file (e.g. a pyIrena docs image) rather than generating one.
- Provider profiles in shots: neutral names (`local-ollama`, `claude-direct`), endpoints like
  `http://localhost:11434`, no ANL-internal hostnames, no real user names or home paths. Use
  `/tmp/aida-docs/...` style folders so paths read the same on every run.
- `DATA_ROOT`: AIDA has no data folder. Put the few small inputs the shots need (a seed
  conversation as JSON, a sample folder) under `scripts/doc_shots/data/` and point `DATA_ROOT`
  there.
- `guides/axis-camera.md` (1115 lines) and `reference/` pages: screenshots only where the page
  describes a window; skip the rest.
- AIDA's CI runs `ruff format --check .`: new Python files must pass it.

### Bernardyn

- Settings: `bernardyn/app.py` sets organisation and application name "Bernardyn" and uses
  `QSettings`. There is no environment variable for the settings location, so
  `isolate_settings`/`make_app` must redirect QSettings to the scratch folder, e.g.
  `QSettings.setDefaultFormat(QSettings.Format.IniFormat)` plus
  `QSettings.setPath(IniFormat, UserScope, scratch)`, and set different organisation or
  application names for the run. Check that nothing appears in the real
  `~/Library/Preferences` (macOS) or registry entry. Workspace and recent-files lists must come
  from the scratch folder too. `BERNARDYN_DATA_ROOT` / `BERNARDYN_OUTPUT_ROOT` (MCP paths) should
  point at scratch if the MCP code is used.
- Inputs: the 7 tracked files in `testData/`, including saved pyIrena results
  (`pyirena_1_2_*`), are ideal: data with fits and size distributions, as users see them.
- 3D views: PyVista/OpenGL may not render offscreen (pyIrena saw a VTK segfault). If so, leave
  those shots manual and say why.
- Graph packages: if a shot shows a saved `*.bernardyn.h5`, build it in scratch from `testData/`
  in the shot function; do not commit generated packages.

## Order and checks

1. Copy the machinery, write `_package.py`, make the **window tour shot** work end to end
   (shot, page, shot list, test). Commit it on its own: it is the pattern Jan reviews.
2. Then the rest, one commit per page or two.
3. Zero warnings with `sphinx-build -W --keep-going -b html docs docs/_build/html`; full test
   suite; `ruff check` (and `ruff format --check` for AIDA). PNGs < 300 KB.
4. Commit on `docs-phase5`. **Ask Jan before pushing**; once pushed, a draft PR gives him the
   Read the Docs preview he reviews from.

## Report

Write `/Users/ilavsky/GitHub/jilavsky-docs/planning/status-<aida|bernardyn>-phase5.md` (one file
per package, so the two sessions don't collide):
- per page: what changed, shots automated vs left for Jan;
- the settings-isolation proof;
- every `CHECK(Jan)` item, grouped by page, **[behaviour]** items first;
- code issues found (not fixed) and any hook added;
- template changes suggested;
- the command to regenerate the screenshots and how long it takes.
