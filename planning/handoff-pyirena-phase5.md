# Brief: pyIrena tool pages and screenshots (phase 5)

*For an agent working in `/Users/ilavsky/GitHub/pyirena`. Written 2026-11-16 from
`/Users/ilavsky/GitHub/jilavsky-docs`. Phase 3 (moving the docs onto Read the Docs) is done and
live at <https://jilavsky-docs.readthedocs.io/projects/pyirena/en/latest/>.*

## Goal

Prepare pyIrena's tool pages so that over the Christmas break Jan mostly **checks text and takes
the few screenshots that need judgment**, instead of writing. Concretely:

1. Every page in `docs/tools/` follows the standard tool-page structure.
2. Every screenshot a page needs has an ID, a place in the page, and a line in a shot list.
3. A script produces all screenshots that can be automated, reproducibly, from tracked data.

**Scientific content is reorganized, not rewritten.** Do not change any numerical claim, default,
equation or recommendation. Where text looks wrong or stale, keep it and list it for Jan (see
"Report"). Results are validated against Igor Irena; the docs must describe the code as it is.

## Read first

1. `/Users/ilavsky/GitHub/jilavsky-docs/PLAN.md`, §3 (layout), §9 (screenshots).
2. `/Users/ilavsky/GitHub/jilavsky-docs/templates/package-docs/docs/tools/_template.md`: the
   tool-page structure.
3. `/Users/ilavsky/GitHub/jilavsky-docs/planning/status-after-pyirena.md`, including the
   "Stale content" list from phase 3.
4. `/Users/ilavsky/GitHub/jilavsky-docs/docs/irena-pyirena-map.md`: Igor equivalents.
5. pyIrena's `AGENTS.md`; `validationData/README.md`.

## What exists today

- 14 tool pages in `docs/tools/`, 100–800 lines each, written as GUI guides with their own
  structures (e.g. `unified-fit.md`: Overview, Launching, GUI Layout, Left Panel, Right Panel,
  Model, Workflow…). **No screenshots anywhere in `docs/`.**
- 13 of them are Help-button targets (`pyirena/_docs.py`, `HELP_TARGETS`). Their file names are
  frozen: do not rename or move them.
- Panels are `QWidget`s with `set_data(...)` (e.g. `UnifiedFitPanel`, `SizesFitPanel`), and the
  code already grabs widgets (`gui/ai_advisor.py`, `gui/plot_export.py`).
- `validationData/`: synthetic datasets with exactly known parameters, tracked in git, also fitted
  in Igor Irena. Use these for screenshots: they are reproducible and their "correct answer" is
  known. `testData/` (40 MB) is the fallback where a tool needs real data (e.g. WAXS, PXP import).

## Work

Branch `docs-phase5` from `main`.

### 1. Tool-page structure

Restructure each page in `docs/tools/` into the template's sections, in this order:

| Section | Content |
|---|---|
| `(label)=` + `# Tool name` | Keep the existing label/title wording; drop "GUI Guide" from titles |
| **At a glance** admonition | Launch (menu path and console command), Python entry point, MCP tool name(s), Igor equivalent as `` {doc}`Irena … <igor:Irena/Page>` `` (or "none, new in pyIrena") |
| Purpose | One paragraph: what for, when to use, when not to |
| **The window** | Annotated full-window screenshot (callout numbers), then a short legend keyed to the numbers |
| **Typical workflow** | 5–8 numbered steps on a named validation dataset, a screenshot where it helps |
| **Controls** | Table: control · meaning · default · tips. Move the existing per-control prose here |
| **Results and outputs** | What is saved, where in the HDF5 file (link `reference/hdf5-nxcansas-structure`), how to reuse |
| **From Python or AIDA** | `tab-set`: Python (`pyirena.batch` / api) and AIDA/MCP |
| **Method notes** | Short; theory stays in or moves to `methods/` and is linked |
| **References** | Papers |

- Existing content that does not fit a section (e.g. Modeling's long form-factor notes) goes to
  `methods/` or `guides/` with a link, or stays under an extra `##` section at the end. **Nothing
  is deleted** except exact duplicates; say where each moved block went in the report.
- Every Python snippet must **run as written** against a file in `validationData/` (or
  `testData/`). Run each one; don't present untested code.
- MCP tool names come from `pyirena/api` / `docs/reference/ai-tools-reference.md`, not memory.
- Pages without a window of their own (`data-selector` is shared by tools) keep the structure
  where it makes sense; use judgment and say what you did.
- `gui/diffraction_lines_panel.py` has no page. If it is a user-facing window, add
  `tools/diffraction-lines.md` (not a Help target, so not in `HELP_TARGETS` unless a button
  exists).

### 2. Screenshot IDs, placeholders and the shot list

- ID format: `<page>-<nn>-<what>`, e.g. `unified-fit-01-window`. Image path:
  `docs/tools/img/<page>/<id>.png`.
- Where an image does not exist yet, put an **invisible placeholder** (a MyST comment, so the
  published site stays clean even if a release happens before Christmas):

  ```markdown
  % SCREENSHOT unified-fit-03-guinier-fit: Level 1 tab after "Fit" on validationData/unified/unified_two_level.h5,
  % Guinier and Porod regions both fitted, residuals visible.
  ```

  When the image exists, replace the comment with a MyST `figure` with alt text and a caption.
- Shot list: `planning/docs-screenshots/SHOTLIST.md` (outside `docs/`, so Sphinx ignores it):
  one table row per ID with columns `ID · page · dataset · state to set up · must show ·
  automated? · status`. Group by page, in page order.
- Add `pyirena/tests/test_doc_screenshots.py` (no Qt, no network): every `SCREENSHOT` ID in
  `docs/` is in `SHOTLIST.md` and vice versa; IDs are unique; every image in `docs/tools/img/` is
  referenced by a page. (Sphinx `-W` already fails on a referenced image that is missing.)

### 3. Automated screenshots

`scripts/make_doc_screenshots.py`:

- Opens each panel offscreen (`QT_QPA_PLATFORM=offscreen` should work; if a panel renders
  differently offscreen, say so) with a validation dataset, sets a fixed window size, sets the
  state (run the fit, select a tab), grabs with `QWidget.grab()`, saves to the image path.
- A registry maps shot ID → setup function, so `--only unified-fit-03-guinier-fit` re-shoots one
  image and the default re-shoots all. Deterministic: fixed seeds, fixed sizes, light theme.
- **Callouts for "The window" shots are drawn by the script** (numbered circles placed from the
  widgets' own geometry, via `QPainter`), so they stay right when the layout changes. The legend
  under the image uses the same numbers.
- PNG, light theme, < 300 KB each where possible (choose the window size and scale for that;
  use `oxipng`/`pngquant` only if already installed, and add no dependencies).
- Not part of the test suite. GUI extras required. Document the command in
  `docs/developer/` (a short "Updating documentation screenshots" section).
- Commit the generated PNGs. Leave as placeholders only the shots that need judgment (a good
  fit on real data, a tricky state, OS dialogs) and mark them `automated: no` in the shot list.

### 4. Known stale content (from phase 3)

Fix only these, as they are factual mismatches with the current tree, not scientific changes:
- `developer/testing.md`, `getting-started/python-quickstart.md`, `guides/scripting-unified-fit.md`
  refer to demos and files that no longer exist: point them at what exists now, or remove the
  reference, and list each change.
- `methods/size-distribution-methods.md` says "three methods" then describes four: make the count
  match the methods actually described (check the code for how many exist).

### 5. Order of work

1. **Unified Fit first, end to end** (page, shots, shot list, test, script registry). Commit it
   on its own: it is the pattern Jan reviews.
2. Then the other tool pages, one commit per page (or per two small pages), in the order of the
   Help-button list.
3. Build clean (`sphinx-build -W --keep-going -b html docs docs/_build/html`), full test suite,
   `ruff`. Don't push.

## Constraints

- Tool page file names and existing `(label)=` targets are a contract. Add labels freely; never
  remove or rename one.
- No new runtime or docs dependencies. Do not edit `docs/conf.py` outside its PER-PACKAGE block or
  `docs/_static/family.css`; if the template needs a change, describe it in the report.
- No code changes beyond the screenshot script, the new test and, if unavoidable, a small hook a
  panel needs to be driven by the script (e.g. a public way to select a tab). List any such hook.
- Keep Irena terminology and parameter names users already know.

## Report

Write `/Users/ilavsky/GitHub/jilavsky-docs/planning/status-pyirena-phase5.md`:
- per page: done / partial, where moved content went, screenshots automated vs left for Jan;
- every place where the text looked wrong or out of date but was left as is (page, quote, why);
- code hooks added, if any; template changes suggested;
- the exact command Jan runs to regenerate screenshots, and how long it takes.
