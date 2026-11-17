# Status after phase 5 (Bernardyn screenshots and page review)

*Written 2026-11-16 by the agent that carried out `handoff-aida-bernardyn-phase5.md` in
`/Users/ilavsky/GitHub/Bernardyn`. For Jan, ahead of the Christmas walk-through.*

## Summary

The work is on branch **`docs-phase5`** in Bernardyn: 6 commits on top of `main` (69a4567).
**Not pushed, no PR.** Pushing and opening a draft PR (for the Read the Docs preview) waits for
your go-ahead.

- **Window tour is the pattern.** Commit `41a5641` holds the machinery and the window tour on
  their own; review that one first.
- **Screenshots:**
  - 13 automated and committed.
  - 1 left for you (the 3-D waterfall).
  - Every PNG is under 300 KB; the largest is 249 KB.
- **New pages:** `getting-started/window-tour.md` and `getting-started/quickstart.md`.
- **Checks:**
  - `sphinx-build -W --keep-going` gives zero warnings.
  - Full test suite: 329 passed, 4 skipped.
  - `ruff check bernardyn tests scripts` is clean.
  - Every Python and CLI block on `guides/headless-recipes.md` was run as written.
  - No CHECK text appears in the built HTML, and `_sources/` is empty.
- **No package code changed.** No hook was needed: the shot functions call the window's
  existing methods (see "Hooks" below).
- **Before starting:** the working tree had an uncommitted `docs/conf.py` change that added a
  second `html_copy_source = False` line. That is the duplicate the template removed in
  19eee36, so I reverted it rather than committing it.

## Commits

| Commit | What |
|---|---|
| 41a5641 | Machinery copied from the template, `_package.py`, window tour, user-guide moves and labels |
| f18cb9b | Quickstart (5 shots) |
| 375669f | User guide (5 shots plus 1 placeholder) and workflow (1 shot) |
| 5c496c6 | Headless recipes: the PNG its first example writes |
| 3fe55e3 | Two images regenerated after their last code change |
| ae9f0bb | CHECK notes; developer note on regenerating the screenshots |

## Per page

| Page | What changed | Automated shots | Left for Jan |
|---|---|---|---|
| getting-started/window-tour *(new)* | Annotated full window with a 12-item legend. Then Panels, Graph area and Documentation/version, moved from the user guide | 01 window | none |
| getting-started/quickstart *(new)* | Five steps: File browser, Unified Fit data + fit, title and box axes, a visible fit line, preview and PNG export | 01 choose, 02 added, 03 styled, 04 datasets, 05 preview | none |
| getting-started/index | Lists quickstart and window-tour | none | none |
| index | "Start here" now also points to the quickstart | none | none |
| guides/user-guide | Section labels `user-guide-<section>`. Window-description text moved to the tour, with links left behind | 01 data selector, 02 File-browser preview, 03 distribution graph, 04 power-law dialog, 05 power-law guide | 06 3-D waterfall |
| guides/workflow | Page label, File-menu shot, one CHECK | 01 File menu | none |
| guides/headless-recipes | Page label; the example's own PNG shown after it | 01 Porod PNG | none |
| reference/* | One CHECK in data-flow-and-formats. No shots: reference pages | none | none |
| developer/index | New section "Documentation screenshots" (how to regenerate) | none | none |
| developer/releasing | One CHECK | none | none |

### What moved from the user guide to the window tour

Moved word for word:

- the Documentation-button and version paragraphs;
- "Both primary panels may be floated…";
- the Datasets-tab paragraph;
- the Display-badge paragraph.

Changed while moving:

- **The File browser's dock paragraph** ("drag its title…, float it…, × button, View → Open File
  Browser, Reset panel layout, remembered on this computer") now says that **all three panels**
  dock, float and stay visible on macOS, and that **Reset panel layout puts every panel back**.
  - Checked in the code: `WA_MacAlwaysShowToolWindow` is set on all three docks, and
    `_reset_all_panels` resets all three.
  - This is the only statement I widened. Revert it if you prefer the File-browser-only wording.

What the user guide keeps:

- one-line links at each place where text left;
- the paragraph "The interactive 2-D graph is fitted to the available window…", because it
  explains Preview output.

### Statements changed

- **Quickstart:** I first wrote "It opens a new, unsaved workspace". I changed it to the
  behaviour in the code and the user guide: a new workspace on the first start, the last saved
  workspace after that.
- No other statement about behaviour, defaults or results was changed.

### Runnable examples (headless-recipes)

Each was run on scratch copies of `testData/Al_Mg_Si__40C_0min_0498.h5` (named `sample.h5` and
`saved-result.h5`) and `Rh1_0085.h5`. All worked; none had to change.

- **Python:**
  - the Porod example;
  - the Size Distribution volume example;
  - the `Presentation(...)` block;
  - the `results=(…)` comparison from the prose;
  - `label=`, `list_recipes()` and `inspect_data()`.
- **CLI:**
  - `bernardyn-plot list-recipes`;
  - `create --recipe porod …`;
  - `create --recipe unified_fit_residuals …`;
  - `--label`, `--series-preset`, `--no-legend`, `--x-range` and `--y-range`;
  - the refusal to overwrite an existing output.
- **Python without `QT_QPA_PLATFORM`:** the Porod example also runs with the variable unset; the
  API goes offscreen by itself.
- **Recipe list:** the "Current recipe set" list matches `list_recipes()` (31 IDs).
- **`reference/api.md`:** autodoc only, with no code blocks or docstring examples, so there was
  nothing to run. All 18 public names render. `SERIES_PRESETS` (a constant) is not shown, which
  is normal for autodoc data without a docstring.
- **`reference/mcp.md`:** the five tool names and the `bernardyn_create_plot` options match
  `bernardyn/mcp/server.py`. The JSON block is a configuration template with placeholder paths;
  it was left as is.

## Settings isolation (proof)

**Where Bernardyn keeps user state.** It is not where the brief assumed:

- **No `QSettings`.** Bernardyn does not use `QSettings`, so the `setPath(IniFormat, …)` idea
  in the brief does not apply.
- **`UserState`:** `~/.bernardyn/state.json`, found through `Path.home()`. It holds the last
  folder, recent workspaces, the last workspace, and the data-selector and File-browser choices.
- **Graph templates:** `QStandardPaths.AppDataLocation/templates`. On macOS Qt ignores `HOME`
  for this location (checked: it still returned `~/Library/Application Support/Bernardyn/…`).
- **Logs:** `~/.bernardyn/logs`, written only by `bernardyn.app.main()`, which the script never
  calls.
- **Locks:** workspace `.lock` files sit beside the package, so in scratch.

**What `scripts/doc_shots/_package.py` does:**

- `isolate_settings()` sets `HOME` and `USERPROFILE` to `<scratch>/shot-*/home`, and
  `BERNARDYN_DATA_ROOT` / `BERNARDYN_OUTPUT_ROOT` to scratch.
- `make_app()` replaces `MainWindow._template_folder` with a scratch folder.
- It sets the organisation and application name to `Bernardyn-docshots`.
- It makes `QMessageBox.warning/information/critical/question` raise an error, so a run fails
  instead of hanging on a modal box.

**Evidence:**

- Before the first run and after all runs (three full runs plus partial ones):
  - `~/.bernardyn/state.json`, `logs/bernardyn.log`, `templates/` and
    `~/Library/Application Support/Bernardyn/*` have identical modification times
    (`state.json`: 2026-11-11 13:50).
  - Nothing named Bernardyn or docshots appeared in `~/Library/Preferences` or Application
    Support.
- Each shot's state was written to `$TMPDIR/docshots-*/shot-*/home/.bernardyn/state.json`;
  29 such files were found, with the expected content (`"folder":
  "/private/tmp/bernardyn-docs/testData"`, and so on).
- `git status testData` is clean.
- **The full test suite does not touch the real `state.json` either** (same modification time
  before and after `pytest`).

## Working notes (`% CHECK(Jan)`) by page

Find them with `grep -rn "CHECK(Jan)" docs/`. `docs/conf.py` also matches, but only because its
comment explains these notes.

**guides/workflow**
- **[behaviour]** Step 1 says "Start Bernardyn. It opens a new, unsaved workspace with one graph
  tab". The user guide ("Save and export") and the code (`MainWindow.restore_last_workspace`)
  reopen the last saved workspace at launch, so step 1 is true only on the first start or after
  File → New workspace.

**getting-started/quickstart**
- `testData/` is not installed with the package. The page points users to the GitHub folder;
  is that the intended source of the example files?

**reference/data-flow-and-formats**
- The input-format table leaves out `.hdf`, which the data selector, the File browser and the
  Add data… filter accept (`testData/LnG_0103.hdf` loads). The user guide lists it.

**developer/releasing**
- The one-time setup and the "bump the version" example still name `0.0.1b6`; the package is at
  1.1.0. Keep them as history, or use a placeholder?

**Checked and found correct.** Every control the user guide names, as spelled in the GUI:

- buttons: Add selected, Select all visible, Places, Copy selected to / Move selected to,
  Create new 2D graph, Check / Uncheck selected, Break lock, Update graph, Add / Edit / Delete,
  Caps, Match output, Apply to, Copy image, Print…;
- shortcuts: Ctrl+Shift+B, Ctrl+Shift+N, Ctrl+E, Ctrl+R, and Refresh = F5;
- the subfolder limit of 50, the 10 recent workspaces, the 0.5 % cap size, the 5 % uncertainty,
  and P = 4 for the power-law guide.

## Code issues found (not fixed; no package code changed)

Most useful first.

1. **The Documentation button's tooltip is stale.** It says "Open local documentation (or
   GitHub documentation after PyPI installation)", but the button opens Read the Docs
   (`_docs.docs_url("home")`).
2. **The first-launch layout is cramped.** With the default `MainWindow.resize(1500, 900)` and
   three docks, the graph gets about 240 × 165 px, and the Display badge sits over the graph
   title. The shots use 1800 × 1000 with fixed dock widths.
3. **The Display badge covers a long title** even at the shot size: "Size Distribution volume
   distribution" in `user-guide-03-distribution`.
4. **Annotation dialog:**
   - The default X/Y are shown with 16–17 significant digits (`0.005251863565392395`).
   - Extra dialog height goes to the explanatory label at the top, not to the form, which
     keeps scrolling.
5. **Tick labels on linear axes** print as `5.000e+03` and `6.000e-05` on the size-distribution
   graph (`user-guide-03`). Readable, but not publication style.
6. **The data selector shows the desmeared and slit-smeared entries under the same name**
   (`…0498.h5: sasdata`). Only the path column, often cut off, tells them apart.
7. **Headless Porod default:** the legend's top-right default sits over the highest-q points
   (`headless-recipes-01-porod`).
8. **Python wrappers can go stale.** `menuBar().actions()[0].menu()` returned a QMenu whose C++
   object was already deleted on the Python side; `findChildren(QMenu)` works. This only
   matters to scripts, not to users.

### Hooks

No hook was added to the package. The shot functions use private `MainWindow` and `Inspector`
methods and attributes:

- `_open_data_paths`, `_import_result_selection`, `_preview_output`, `_output_previews`;
- `_annotation_defaults`, `_upsert_annotation`;
- `files_panel.*`, `GraphPage.canvas._renderer`.

A refactor that renames these breaks the script, not the tests. The tests already use
`_import_result_selection` the same way.

## Template changes suggested (not made)

1. **Clean-up loop in `make_doc_screenshots.py`:**
   - The 2-D renderer closes a temporary pyqtgraph `PlotWidget` and calls `deleteLater()`.
     `processEvents()` outside an event loop never runs deferred deletes, so the widget stays a
     top-level widget.
   - The loop then calls `close()` on it a second time and pyqtgraph raises `AttributeError`,
     which aborts the whole run.
   - Bernardyn works around it in `_package.flush_deletes()`.
   - Suggestion: in the `finally:` block, call
     `QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)` before the loop, and
     wrap each `close()` in `try`.
2. **Modal-dialog guard:** any `QMessageBox` hangs an offscreen run with no output. The
   `refuse()` patch in Bernardyn's `make_app` is generic and could move to `_common.py`.
3. **Scratch folders are never removed.** `$TMPDIR/docshots-*` builds up with every run. Delete
   it at exit, with a `--keep` flag for debugging.
4. **`_package.py` docstring:** for Bernardyn, the template's hint ("its QSettings / workspace
   location") is wrong; there are no QSettings. A neutral wording would help: "every place the
   package reads or writes user state; check `Path.home()`, `QStandardPaths` and `QSettings`
   uses".
5. **`make_app` "light theme":** Bernardyn has no theme, and the offscreen platform already
   defaults to Fusion. `_package.make_app` sets Fusion explicitly so runs on Windows or Linux
   look the same. Worth one sentence in the template README.
6. **Helpers worth sharing,** if AIDA or pyIrena want them:
   - `graph_strip()`: crops the empty space around an aspect-locked pyqtgraph canvas;
   - `fixed_data_folder()`: a fixed `/tmp/<pkg>-docs/…` copy, so paths read the same on every
     run;
   - rooting a folder tree at that folder, so the shot does not list other folders in `/tmp`.

## Regenerating the screenshots

From the Bernardyn repository root, in the `bernardyn` conda environment:

```bash
python scripts/make_doc_screenshots.py                    # all 13, about 37 s on this Mac
python scripts/make_doc_screenshots.py --only quickstart  # one page
python scripts/make_doc_screenshots.py --only window-tour-01-window
python scripts/make_doc_screenshots.py --list
```

- **Reproducible:** two consecutive full runs gave byte-identical images for all 13.
- **Fixed folder:** the shots that show a folder use `/tmp/bernardyn-docs/testData`, which is
  rebuilt on each run.
- **Docs build:** the `docs-env` conda environment has no `myst_parser`. I built in a throwaway
  venv instead (`/tmp/bern-docs-venv`, made from the bernardyn environment plus
  `docs/requirements.txt`).
- **The same instructions** are in `docs/developer/index.md`, section "Documentation
  screenshots".

## Notes for Jan's walk-through

- **Start with `41a5641`** (window tour and `_package.py`). If the callout placement, the
  1800 × 1000 window size or the moved text is wrong there, the other pages will need the same
  change.
- **The one manual shot, `user-guide-06-waterfall`:**
  1. Take it on a real display.
  2. Save it as `docs/guides/img/user-guide/user-guide-06-waterfall.png`.
  3. Replace the `% SCREENSHOT` comment with a `figure`, with alt text and a caption.
  4. Set its row in `planning/docs-screenshots/SHOTLIST.md` to `done`.

  `pytest tests/test_doc_screenshots.py` catches anything out of step.
- **Shortcuts:** the File-menu shot shows macOS glyphs (⌘). The caption says "Ctrl on Windows and
  Linux".
- **Next step:** say the word to push `docs-phase5` and open a draft PR for the RTD preview.
