# Status after phase 5 (pyIrena tool pages and screenshots)

*Written 2026-11-16 by the agent that carried out `handoff-pyirena-phase5.md` in
`/Users/ilavsky/GitHub/pyirena`. For Jan, ahead of the Christmas walk-through.*

## Summary

The work is on branch **`docs-phase5`** in pyirena: 17 commits on top of `main` (e84d63a), not
pushed, no PR.

- **Unified Fit is the pattern.** It is done end to end in commit `c91a194`, on its own; review
  that one first.
- **All 14 tool pages** now follow the template structure, in this order:
  1. At a glance
  2. Purpose
  3. The window (annotated screenshot and numbered legend)
  4. Typical workflow (on a named dataset)
  5. Controls (tables)
  6. Results and outputs
  7. From Python or AIDA
  8. Method notes
  9. References

  Leftovers go in extra sections at the end.
- **Screenshots:**
  - 42 are automated and committed.
  - 13 are left for you, as invisible `% SCREENSHOT` comments in the pages and `automated: no`
    rows in the shot list.
  - Every image is under 300 KB.
- **The four phase-3 stale-content items are fixed** (commit `398d34e`).
- **Checks:**
  - `sphinx-build -W --keep-going` gives zero warnings.
  - Full test suite: 2202 passed, 8 skipped.
  - `ruff check pyirena/ scripts/doc_shots scripts/make_doc_screenshots.py` is clean.
  - Every Python snippet on the tool pages was run as written.
  - `validationData/`, `testData/` and `~/.pyirena` were not modified by any of this.
- **How the work was done:** the 13 pages after Unified Fit were written by four parallel agents
  from the Unified Fit pattern. I cherry-picked their commits (no conflicts) and re-ran every
  check on the merged branch.

**Things that look wrong are kept and marked, not fixed.** Each page keeps the text it had and
marks doubtful statements with invisible `% CHECK(Jan): …` comments. These never appear on the
published site. To find them all:

```bash
grep -rn "CHECK(Jan)" docs/
```

**No code hooks were added.** No package code changed. The screenshot functions drive the panels'
existing methods.

## Regenerating the screenshots

From the pyirena repository root, with the GUI extras installed:

```bash
python scripts/make_doc_screenshots.py                    # all 42 images, about 80 s on this Mac
python scripts/make_doc_screenshots.py --only unified-fit # one page
python scripts/make_doc_screenshots.py --only unified-fit-03-guinier-fit   # one image
python scripts/make_doc_screenshots.py --list
```

The same is documented in `docs/developer/testing.md`, section "Updating documentation
screenshots".

How the script is laid out:

- `scripts/make_doc_screenshots.py` is the entry point.
- `scripts/doc_shots/_common.py` holds the shared helpers: the throw-away settings folder, the
  copies of the data, the callouts, and the PNG saving.
- Each page has its own module, `scripts/doc_shots/<page>.py`.
- `planning/docs-screenshots/SHOTLIST.md` lists every shot.
- `pyirena/tests/test_doc_screenshots.py` checks, without Qt, that the pages, the shot list, the
  images and the `@shot` registrations agree.

Reproducibility: 40 of 42 images come out byte-identical on every run. The two exceptions:

- `saxs-morph-01-window`: the status bar prints the elapsed time.
- `data-explorer-01-window`: a few pixels in the folder label change.

Both look the same to the eye.

## Per page

| Page | Status | Automated shots | Left for Jan | Commit |
|---|---|---|---|---|
| unified-fit | done | 01 window, 02 Porod tab, 03 local Guinier, 04 fit result, 05 slit smeared | 06 real data | c91a194 |
| size-distribution | done | 01 window, 02 background tab, 03 fit result | 04 real data | 7a291d5 |
| modeling | done | 01 window, 02 population tab, 03 fit result | 04 real data | 182ae9c |
| simple-fits | done | 01 window, 02 sphere, 03 invariant | 04 real data (linearization) | 65eacd7 |
| fractals | done | 01 window, 02 Monte-Carlo I(Q), 03 optimizer | 04 3D viewer, 05 targets | b0806a7 |
| waxs-peak-fit | done | 01 window, 02 find peaks, 03 fit result, 04 diffraction lines | 05 phase identification | 43c0848 |
| carbon-fit | done | 01 window, 02 WAXS zoom, 03 results | 04 real carbon | d7a7b24 |
| saxs-morph | done | 01 window, 02 calculated, 03 slice | 04 3D view | 4a9e3b4 |
| data-merge | done | 01 window, 02 loaded | 03 Porod view, real pair | ebfd215 |
| data-manipulation | done | 01 window, 02 scale result, 03 subtract | 04 similarity, real series | 6025200 |
| scattering-contrast | done | 01 window, 02 energy scan | 03 import dialog | 5592c9c |
| data-explorer | done | 01 window, 02 graph, 03 collect | none | 4c1e844 |
| data-selector | done | 01 window, 02 graph, 03 tabulate | 04 export context menu | 68a769b |
| feature-identifier | done | 01 window (the dialog), 02 markers on the Unified graph | none | bf84067 |

### Datasets and checks

Each fit shown in a screenshot was checked against the dataset's known answer
(`validationData/README.md`):

- **Unified Fit**, `unified_two_level`: Rg 120.1 / 1202 Å against 120 / 1200; reduced χ² 1.06.
- **Unified Fit**, slit-smeared file: G 99.8, Rg 200, B 3.05e-7 against 100, 200, 3.045e-7.
- **Size Distribution**:
  - `sizes_sphere_lognormal`: Vf 0.009996 against 0.01;
  - `sizes_sphere_flat_background`: Vf 0.005997 against 0.006.
- **Modeling**: Vf 0.00504, Rg 4001 against 0.005, 4000.
- **Simple Fits**:
  - Guinier: Rg 45.97 against 45;
  - Sphere: 7.999 / 119.97 against 8 / 120;
  - Invariant: φ 0.00579 against 0.006.
- **WAXS**, `waxs_three_gauss`: Q₀ 1.850 / 2.550 / 3.049, matching the ground truth.
- **Data Merge**: DS2 scale 0.8719 against 1/1.15 = 0.8696.
- **Data Manipulation**: scale 0.4 with background 0.12 reproduces the reference to 3×10⁻¹³.

Three pages had no suitable validation set:

- **Carbon** uses a curve synthesised the same way `test_carbon_fit` does (S_macro 3e4, φ 0.20,
  r 7 Å, seed 7). The fit recovers φ 0.199 and r 6.99 Å.
- **SAXS Morph** uses `simple_fits/simple_debye_bueche.h5`, a random two-phase curve. The
  dilute-spheres files give a useless model there (reduced χ² 6461).
- **Fractals** builds its reference file in scratch from a Unified fit of
  `modeling_mass_fractal.h5`.

### Diffraction Lines

There is no page. `diffraction_lines_panel.py` is a tab inside the WAXS Peak Fit window: it has
no window, Help button or `main()` of its own. It is documented in its own section of
`waxs-peak-fit.md`, which has the label `diffraction-lines-tab`.

### Where moved content went

The pattern is the same on every page:

- the introduction → Purpose;
- launching instructions → At a glance;
- per-control prose → Controls tables, using the label shown in the GUI, the old meaning text,
  the default from the code, and the tooltip as the tip;
- saving → Results and outputs;
- scripting → the Python tab;
- theory, fit quality and slit smearing → Method notes;
- everything else → extra sections at the end.

No new `methods/` or `guides/` pages were created. Page-specific moves:

- **unified-fit:**
  - The three fitting strategies → a new section, "Fitting strategy".
  - Tips and Common issues → "Tips and troubleshooting".
- **modeling:**
  - Populations 4.1–4.6, Distributions, Form factors and Structure factors stay on the page in
    an end section, "Model reference".
  - They stay because `developer/adding-{form,structure}-factors.md` point to
    `tools/modeling.md`. Moving them to `methods/` together with those pointers is a good
    follow-up.
  - MC Uncertainty stays in an end section, so the CHANGELOG link `#mc-uncertainty` still
    resolves.
- **size-distribution:** the Method-parameters table links to labelled sections of
  `methods/size-distribution-methods.md`; those labels are new.
- **data-merge:** Batch run, Config file format, CLI reference and Python API reference → end
  sections.
- **fractals:** Algorithm details, Performance, and Notes and limitations → end sections.
- **feature-identifier:** Tuning guidance, Limitations, and Technical notes → end sections.
- **data-selector:** Installation, Requirements, Troubleshooting, Development, Future features
  and similar → end sections.
  - "Getting graphs and tables out of pyIrena" is kept word for word, with a new label,
    `getting-graphs-and-tables-out`.
  - The page title changed from "pyIrena GUI Module" (the old README title) to "Data Selector".

### Deleted content

Only these were removed:

- the ASCII window sketches on unified-fit, modeling, simple-fits, saxs-morph,
  data-manipulation, scattering-contrast and data-explorer (replaced by the annotated
  screenshots; data-explorer keeps the panel widths as a sentence);
- the hand-written "Contents" lists, which duplicate the page's table of contents;
- exact duplicates (the Export ASCII bullet in the Unified workflow; Data Explorer's repeated
  X-axis table);
- data-selector's empty "Screenshots (add when available)" section.

Everything can be restored from git history.

### Snippets that had to change to run

Each of these was a broken or non-runnable example, now a working one on `validationData`:

- **unified-fit:** new control-API example.
- **modeling:** the old examples used `dist_params` keys `median`/`sigma`/`shift`; the code uses
  `min_size`/`mean_size`/`sdeviation`. They also read `result['result'].populations`; the code
  has `.config.populations`. The example also sets `q_min = 5e-5`, because the default 0.001
  cuts off the Guinier region.
- **simple-fits:** the example runs on copies, because `fit_simple` saves into the data file by
  default. The old example used `load_result(…, "simple_fits")`, which raises `ValueError`; it
  now uses `load_simple_fit_results`.
- **saxs-morph:** the example writes its own config and uses `save_to_nexus=False`.
- **data-merge, data-manipulation:** the examples write to an `output_folder` in the current
  directory. Manipulation's example values are now the inverses of the known constants, so the
  result can be checked against the reference.
- **waxs-peak-fit, carbon-fit:** the old batch examples referenced files that don't exist. They
  are now shown as `text` blocks, and a runnable control-API example was added.

Signature and schema listings that are not code are now fenced as `text`.

## Text that looks wrong or out of date, kept as is

Each item below is also a `% CHECK(Jan)` comment in the page. Items marked **[physics]** are
scientific statements and need your judgement; the others are GUI labels or behaviour that have
drifted from the text.

**unified-fit**
- **[physics]** "working from largest structure (Level 1) to smallest", "Rg values should be
  ordered (Level 1 largest)", and "For Level 1 Guinier: A at low-Q flat region onset".
  - The code's convention is the opposite: Link RgCutoff ties level N's RgCO to the Rg of level
    N−1, so level 1 is the smallest, high-Q structure, as in Irena.
  - The validation file agrees: level 1 is Rg 120 Å, level 2 is 1200 Å.
  - `getting-started/python-quickstart.md` also agrees ("Level 1: Small primary particles").
- "Store local fits" and "Export ASCII" are not in the current panel.
- "Display local (Porod & Guinier) fits?" is now "Show selected level?". Its tooltip says it
  overlays the selected level's contribution.
- Renamed buttons: "Store in Data Folder" → "Store in File", and "Reset Unified" → "Reset to
  Defaults".
- "Fix limits? — Lock current low/high values", but its tooltip says it sets all limits to ±5×.
- Residuals are described as "(Data − Fit)/σ", but the plot axis says "r' (rescaled)".
- "a Slit smeared control row appears": the row is always visible.

**size-distribution**
- **[physics]** "volume fraction = ∫P(r)dr / contrast". Under the G-matrix convention (and in
  `validationData/README.md`), ∫P_V dr is the volume fraction itself.
- The plot is described as "D(r) = dV/dr (volume fraction per Å)", but the axis reads
  "P(r) (a.u.)".

**modeling**
- "Derived Results panel (below the graph)": no such panel exists.
- The HDF5 `@pop_type` list names three types, leaving out guinier_porod, mass_fractal and
  surface_fractal.
- Log-Normal parameters are given as "Median, σ, Shift"; the GUI and code use Min Size, Mean
  Size and Sdeviation.
- Global-fit timings disagree: "~60 s → ~17 s on 6 cores" in the text, 130 s → 21 s in the
  table.
- The References section was added from citations in the text (Hammouda 2010, Teixeira 1988,
  Ardell 1966); please check it.

**simple-fits**
- "N MC runs (default 50)": the GUI says "Passes", default 10. 50 is the batch default.
- "Export/Import Parameters": the buttons are "Save/Load params to/from JSON".
- "the linearization panel shows 'No linearization available…'": for the Sphere model the panel
  is hidden instead.
- References were added (Debye 1947 and the Irena modules). Papers for Teubner-Strey,
  Debye-Bueche, Benedetti-Ciccariello and Hermans are still missing.

**fractals**
- "GUI-only; no batch / scripting / headless API": `core.fractals` exposes `grow_aggregate`,
  `intensity_unified` and `optimize_growth`, and `pyirena_read_fractals` exists.
- **[physics]** The Monte-Carlo description is stale: "voxelize… 20×-oversampled… random pairs
  of solid voxels", "~40 MB", "1e7 pair samples / 20 s". The code places uniform points in each
  sphere and histograms all pair distances, with optional 10 % polydispersity.
- "The best is bolded": the best trial actually gets a "★ BEST" suffix.
- "Click Grow One": the button is "Grow", on the "Grow One" tab.

**waxs-peak-fit**
- The peak-shape list leaves out Voigt.
- The "Add Peak Manually" button is gone; adding and removing peaks is on the graph's right-click
  menu.
- Button names: "Revert" is now "Revert back"; "Export/Import Parameters" is now "Save/Load
  params to JSON"; there is no "Save State" button.
- The cursors are described as "cyan dashed" but are blue and red. The "Q-min/Q-max display
  boxes" are a label.

**carbon-fit**
- "In the Data Browser": the tool is called the Data Selector everywhere else.
- The physics text was moved word for word, including both corrections against the source
  paper: the eq. 3 roughness 1/5, and the graphite d100 / ρ_struc correction.

**saxs-morph**
- **[physics]** "refines parameters … by fitting back to the data" contradicts its own Method
  notes, which say it is "not an iterative fit".
- **[physics]** The power-law pre-fit is described as "a low-Q window … dominated by the Q⁻⁴
  Porod slope". The Porod tail is at high Q.
- "Each term has its own Fit / limits row": there are none for B, P or the background.
- "Runs … synchronously … blocks the GUI": the calculation runs in a worker thread.
- "black data − background trace": it is green.
- Button names: "Save Result to HDF5…" is now "Save/Append to HDF5…"; "SAXS Morph (GUI)
  (purple button, row 8)" is now "3D saxsMorph (GUI)".
- The Performance table and the cube-side tooltip disagree at 256³ (3 s and 16 MB, against 15 s
  and 125 MB). The measured time was about 4 s.
- "Berk (1991) Phys. Rev. E 51, 4141": the year and the journal don't match.
- The Igor equivalent, TwoPhaseSolid, is uncertain. It was already marked (?) in
  `irena-pyirena-map.md`.

**data-merge**
- "Algorithm: Nelder-Mead simplex": with Scale = DS2 the engine reports "Analytical WLS"
  (closed form).
- The Scale menu in the panel defaults to DS1, while the config default is `scale_dataset` 2 and
  the Concepts section treats DS1 as the absolute reference.
- "Split OFF: DS1 Q ≤ cursor B, DS2 Q ≥ cursor A", but the tooltip says "include all data".
- "Save JSON Config" is said to save the Q range and optimisation settings; it also saves the
  folders.

**data-manipulation**
- "Lower threshold = stricter (fewer rejections)": a lower threshold rejects fewer frames, so it
  is looser. The threshold guide's "0.001 (strict)" has the same problem.
- The core slit guard (Method notes) and "the api adds guards the panel relies on the user for"
  (AIDA tab) contradict each other.
- The Franke 2015 reference was written from memory by an agent; please check the authors and
  title.

**scattering-contrast**
- The page said to click "Scattering Contrast (GUI)" in the "Support Tools section". The button
  is "Scattering Contrast Calculator", in "Data Processing & Reference". At a glance now uses the
  GUI label.
- The "Neutron Isotope Selection table (collapsible)" is not collapsible.
- The μ axis on the graph is labelled "kcm⁻¹" (a pyqtgraph SI prefix), while the table uses
  cm⁻¹.

**data-explorer**
- The introduction lists "Data Merge" results, but there is no Merge preset or Collect type.
- Undocumented features:
  - "Plot Modeling model" in the Group menu;
  - five presets (Size Dist. surf. S(r), cumul. surf., Modeling model, and Modeling vol./num.
    P(r));
  - the "Modeling" and "Carbon model" Collect types;
  - the "Export to Igor" tab;
  - the "Save ITX" button in the Collect window.
- Renamed: the "WAXS Peak Fit" preset is "WAXS model", and the Multi-Collect buttons are "+ Add",
  "Remove sel." and "Collect from all selected files".
- The supported-files table leaves out `.h5xp`.
- "via the HDF5 Viewer" uses the tool's old name.

**data-selector**
- "Text Files (Future)": text import already exists.
- Troubleshooting says "matplotlib Qt backend", but the graphs use pyqtgraph.
- The Development section names `data_selector.py` and an `__init__.py` that does Qt detection.
  These are now `data_selector/panel.py` and `gui/_qt.py`.
- Nearly all of the "Future Features" list is implemented.

**feature-identifier**
- **[physics]** The default "Min segment width (dec)" is given as 0.10; the code uses 0.2.
- Knee keys `slope_low_q`, `slope_high_q` and `delta_slope` are now `P_low_q`, `P_high_q` and
  `delta_P`.
- `pyirena_ctrl_detect_features(...)` is now `pyirena_call("detect_features", …)`.
- The knee label "GK Δ=" is shown as "GK ΔP=" in the GUI.

**Phase-3 stale content (fixed, commit 398d34e)**
- `developer/testing.md`: references to the generator scripts and `data_selector.py` that no
  longer exist; the test files are tracked in `testData/`.
- `guides/scripting-unified-fit.md`: `unified_demo.py` and `README_unified.md` now point to
  `python -m pyirena.examples.unified_fit_demo` and the Unified Fit page. The demo runs one fit,
  not four.
- `getting-started/python-quickstart.md`: "Learn the theory" now links to the Unified method
  notes; the FAQ bullet (no such page) is removed.
- `methods/size-distribution-methods.md`: "three methods" is now "four" (three places), matching
  the four methods in `core/sizes.py`.

Left as is in `testing.md`: "Should show: ['entry1']", the Qt5Agg remark, and the
expected-performance table.

## Code observations (not fixed; no code was changed)

Most important first:

1. **The Fractals target detection never fires for files written by current pyIrena.**
   - Cause: `FractalsPanel._derive_targets_from_levels` reads `level["RgCutoff"]`, but
     `load_unified_fit_results` returns `"RgCO"`.
   - Verified: a stored fit with RgCO₂ = Rg₁ still shows "No targets", so the documented
     "with a reference Unified fit" workflow does not work. This is why `fractals-05-targets` is
     a manual shot.
2. **Unified Fit says "Level not feasible" for level 1 at the ground-truth parameters** of
   `unified_two_level` and `unified_one_level_slitsmeared`. It is visible in shots 01, 03 and 05.
   The likely cause, from the group D agent: the validation generator defines B with the
   smooth-join formula, and the feasibility check judges B differently. Decide whether the check
   or the data is right, and whether the shots are acceptable as they are.
3. **The Feature Identifier suggests 5 levels for `unified_two_level.h5`**, which has 2 levels
   and a flat background of 0.02. It labels the background "PLS P=0.6". This is visible in its
   two shots.
4. **Unified Fit:**
   - The "Results to graphs" annotation shows level-2 "RgCO = 100" after a fit in which RgCO is
     linked to Rg₁ = 120, so the field looks stale.
   - The "Results to graphs" tooltip says it plots results for all files selected in the Data
     Selector; it actually annotates the current graph.
5. **Default methods differ** between the GUI and the API:
   - Size Distribution: the GUI default is regularization, while
     `api.control.select_sizes_model` defaults to and recommends maxent.
   - Data Merge: the panel's Scale default is DS1, the config default is DS2.
6. **Monte Carlo runs are unseeded in the GUI:** Size Distribution MC passes no seed, and the
   Fractals MC worker gets none. Fine for users, but not reproducible.
7. **`api.inspect_file()`** returns `reduced_data_present=False` and no Q range for
   `unified_two_level.h5`, while `api.read_reduced_data()` reads the same file.
8. **The compound library ignores `PYIRENA_STATE_DIR`:** `io/contrast_io.DEFAULT_LIBRARY_PATH`
   is fixed at `~/.pyirena`. The screenshot module overrides it.
9. **`ai-tools-reference.md`** says SAXS Morph χ² appears only in files written before 1.2.0;
   the current panel computes it.
10. **PyVista/VTK segfaults** under `QT_QPA_PLATFORM=offscreen`. The script turns PyVista off,
    and the window shots show the "not installed" placeholder in the 3D pane (the captions
    explain this).
11. **Cosmetic:**
    - `&` read as a menu shortcut: "Fit Cmplx. Bckg. & Sizes" and "Data Processing & Reference"
      lose the `&` (it needs `&&`).
    - Clipped labels: "Identify Features…", "Parameters", "Open NeXus…", "Parse ▸", "Del".
    - Overlapping log-axis tick labels in several panels.
    - The WAXS "Half-width" label overprints `bg0` after switching away from SNIP.
    - Carbon (100) header text overprints.
    - Simple Fits y-axis label has no units.
    - Merge error bars draw as wide grey bars.
    - Merge's minimum width is about 1884 px.
    - Panels whose coded sizes clip their controls: Modeling at 1300×900, Simple Fits at
      1200×700, Contrast at 1120×740. The shots use larger sizes.
    - The Data Selector graph legend font is very large; this may be offscreen-only.
12. Size Distribution and Simple Fits have no `__main__`, so neither can be launched standalone.

## Template changes suggested (not made)

- **`tools/_template.md`, Typical workflow:** it says "one screenshot each", while the brief
  says "a screenshot where it helps". Every page here followed the brief (2–4 workflow shots).
  Align the template.
- **`tools/_template.md`, At a glance:** a single line separated by `·` gets hard to read with
  four long items. The pages use one item per line, ending lines with `\`, and `:class: tip`.
  Worth adopting in the template.
- **Labels:** the pages use `(<page>-<section>)=` on every section, e.g. `unified-fit-controls`.
  Worth stating as a family convention, because Help-button anchors (`HELP_ANCHORS`) will want
  them.
- **Screenshot machinery:** `scripts/doc_shots/_common.py`, `make_doc_screenshots.py` and
  `test_doc_screenshots.py` are generic apart from the pyIrena imports. They could become a
  family template for AIDA and Bernardyn: the same ID scheme, shot list and test.
- **conf.py:** images, figures with alt text, `tab-set` and `{doc}` links to `igor:` all work
  with the current settings. One thing to decide: the `% CHECK(Jan)` and `% SCREENSHOT` comments
  are hidden on the rendered pages, but Sphinx copies the page sources to `_sources/*.txt`, which
  the "Show source" link serves. If that matters before the comments are resolved, set
  `html_copy_source = False` (or `html_show_sourcelink = False`) in the template.

## Notes for Jan's walk-through

- **Start with Unified Fit** (`c91a194`). If the pattern or the decisions there are wrong, the
  other 13 pages will need the same change.
- **Doing the 13 manual shots:** take the shot, save it as
  `docs/tools/img/<page>/<id>.png`, then:
  1. replace the `% SCREENSHOT` comment with a `figure` that has alt text and a caption;
  2. set the status in `SHOTLIST.md` to `done`.

  `pytest pyirena/tests/test_doc_screenshots.py` catches anything that gets out of step.
- **Fonts come from the operating system.** Regenerate a page's automated shots on one machine,
  and check `git diff --stat docs/tools/img` before committing.
- **Scratch files the script leaves:**
  - Data Selector and Data Explorer shots use a fixed folder, `/tmp/pyirena-docs/unified` (the
    system temp folder on Windows), so the path shown in the image is the same on every run. It
    is rebuilt each run.
  - The agents' worktrees are still in `pyirena/.claude/worktrees/`, with their branches
    `worktree-agent-*`. Everything in them has been cherry-picked onto `docs-phase5`; delete
    them when convenient.

## Template changes applied (2026-11-16, jilavsky-docs session)

All four suggestions above were accepted and are now in `templates/package-docs/`:

1. `conf.py`: `html_copy_source = False` (outside the PER-PACKAGE block), so `% CHECK(Jan)` and
   `% SCREENSHOT` comments are not published in `_sources/`. Already synced into AIDA and
   Bernardyn.
2. `tools/_template.md`: "At a glance" with one item per line (`\` line ends, `:class: tip`);
   "a screenshot where it helps".
3. Section labels `(<page>-<section>)=` with suffixes `window`, `workflow`, `controls`,
   `results`, `scripting`, `method`, `references`, as on the pyIrena pages (template README,
   PLAN.md §3).
4. The screenshot machinery becomes a family template later, with AIDA/Bernardyn phase 5.

**For pyIrena, still to do on `docs-phase5`:** copy the template's `docs/conf.py` keeping
pyIrena's PER-PACKAGE block (the only change is the three `html_copy_source` lines), rebuild with
`-W`, and commit **before** the branch is merged, so the CHECK comments never reach `_sources/`
on `latest`.
