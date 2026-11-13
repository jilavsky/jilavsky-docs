# PLAN: family documentation on Read the Docs

*Revised 2026-11-13 from the 2026-11-11 draft (kept unchanged in
`planning/DOCUMENTATION_PLAN_2026-11-11.md`), with Jan's decisions applied.*

## 1. Decisions (settled)

| # | Decision |
|---|---|
| D1 | Parent RTD project and repo: **`jilavsky-docs`** (`github.com/jilavsky/jilavsky-docs`). The slug was free on 2026-11-13; register it soon. |
| D2 | All in one place eventually, built in small steps. **First wave: pyIrena, Bernardyn, AIDA.** Anisa and pyNika added later as subprojects. The Igor manuals stay a stand-alone project for now (their URLs are hard-coded in released Igor code); attach them as a subproject only after a redirect test (§6). |
| D3 | Help buttons open **`stable`** for releases, **`latest`** for dev and pre-release installs. |
| D4 | Theme: **PyData Sphinx Theme** (NumPy, SciPy, pandas, Jupyter use it; works on every platform and in dark mode). |
| D5 | Custom domain: later. |
| D6 | **Matilda: not part of this site** (different org, mostly internal). |
| D7 | **pyNika: later**. A navbar slot is added when its docs exist. |
| D8 | Accept EthicalAds (RTD Community). |

## 2. Architecture

```
https://jilavsky-docs.readthedocs.io/en/stable/                      ← this repo (home page)
https://jilavsky-docs.readthedocs.io/projects/pyirena/en/stable/     ← jilavsky/pyirena  docs/
https://jilavsky-docs.readthedocs.io/projects/bernardyn/en/stable/   ← jilavsky/bernardyn docs/
https://jilavsky-docs.readthedocs.io/projects/aida/en/stable/        ← jilavsky/aida     docs/
https://saxs-igorcodedocs.readthedocs.io/en/stable/                  ← unchanged, stand-alone
```

- Each package's docs live in **its own repo**, in `docs/`, and are versioned with its code.
- This repo holds only what is shared: home page, which-tool table, installing several packages
  into one environment, shared file formats, cross-package workflows, the Irena ↔ pyIrena map,
  citations, and the package template.
- Every site shows the same top navbar (the `FAMILY` block in each `conf.py`), so the family reads
  as one site even though each package has its own versions.

## 3. One layout for every package (harmonization)

Now is the time to make all packages the same; later each rename costs a redirect. The rule is
simple: **every package's `docs/` looks like `templates/package-docs/docs/`**.

```
<repo>/
  .readthedocs.yaml                  identical in every repo
  docs/
    conf.py                          identical except the PER-PACKAGE block
    requirements.txt                 identical pins in every repo
    _static/family.css               identical except the accent colour
    index.md                         what it is, who it is for, one screenshot
    getting-started/                 installation.md, quickstart.md
    tools/                           ONE PAGE PER WINDOW = Help-button targets (optional)
    guides/                          task-oriented how-tos
    methods/                         theory and algorithms (optional)
    reference/                       api.md (autodoc), file formats, CLI, MCP tools
    developer/                       testing, releasing, extending (optional)
    changelog.md                     includes ../CHANGELOG.md
  <package>/_docs.py                 HELP_TARGETS + docs_url(); no Qt imports
  tests/test_help_targets.py         every Help target exists as a page
```

Conventions, all packages:

- **File names: lowercase, kebab-case** (`unified-fit.md`, not `unified_fit_gui.md`). No
  `_gui` suffix: the folder (`tools/`) already says it is a window.
- **Images next to the page**: `<section>/img/<page>/<page>-<nn>-<what>.png`. Source files that
  generate figures (`make_figures.py`, `.svg` masters) live in the same folder.
- **Only user-facing pages in `docs/`.** Planning notes, TODO lists, talk slides and
  agent-instruction files belong elsewhere (`planning/`, repo root, or the AI skill folder).
- **No `docs/README.md`.** `index.md` is the table of contents. (GitHub shows a folder listing
  instead, which is fine because readers use RTD.)
- **Anchors the code links to** are explicit MyST labels (`(unified-fit-levels)=`), never
  auto-generated heading anchors.
- **Optional sections are left out** (folder and toctree entry) until they have a page; no empty
  placeholder pages (decided 2026-11-13 after AIDA and Bernardyn).
- **Text that lives elsewhere is included, not copied** (`{include}`, with `start-after`/`end-before`
  markers for part of `README.md`).
- **Sections are listed by hand** in each `<section>/index.md` (no globbing), so the order is
  chosen and an empty section still builds without warnings.
- **Page names under `tools/` never change after release.** If one must, add a redirect.

Not documentation, but noticed while surveying (leave alone unless you want them harmonized):
AIDA uses a `src/` layout, `hatchling` and Python `>=3.11`, while the house standard is a flat
layout, `setuptools` and `>=3.10`. The template copes with both (`SRC_DIR` in `conf.py`).

## 4. Per-package migration (first wave)

Each package: branch `docs-rtd`, copy the template, move the existing Markdown into the layout
(contents mostly unchanged in the first pass), add `_docs.py` and the test, switch Help buttons
in the next release.

### 4.1 pyIrena (first; sets the pattern)

Today 13 panels open `github.com/jilavsky/pyirena/blob/main/docs/<file>.md`.

| Now (`docs/`) | New |
|---|---|
| `unified_fit_gui.md`, `unified_fit_features.md` | `tools/unified-fit.md` (merge) |
| `sizes_methods.md` | `tools/size-distribution.md` + `methods/size-distribution-methods.md` |
| `modeling_gui.md` | `tools/modeling.md` |
| `simple_fits_gui.md` | `tools/simple-fits.md` |
| `fractals_gui.md` | `tools/fractals.md` |
| `waxs_peakfit_gui.md` | `tools/waxs-peak-fit.md` |
| `carbon_fit_gui.md` | `tools/carbon-fit.md` |
| `saxs_morph_gui.md` | `tools/saxs-morph.md` |
| `data_merge_gui.md` | `tools/data-merge.md` |
| `data_manipulation_gui.md` | `tools/data-manipulation.md` |
| `scattering_contrast_gui.md` | `tools/scattering-contrast.md` |
| `hdf5_viewer_gui.md` | `tools/data-explorer.md` |
| `GUI_README.md` | `tools/data-selector.md` |
| `feature_identifier.md` | `tools/feature-identifier.md` |
| `installation.md`, `QUICK_START.md`, `gui_quickstart.md` | `getting-started/` |
| `usage_guide.md`, `batch_api.md`, `data_import_and_cleaning.md`, `igor_pxp_import.md`, `ai_integration.md` | `guides/` |
| `sizes_methods.md` (theory part), `slit_smearing.md`, `fit_quality_metrics.md`, `saxs_morph_method_comparison.md`, `distribution.md` | `methods/` |
| `HDF5_NxcanSAS_structure.md`, `scattering_io_api.md`, `ai_tools_reference.md`, `zmq_service.md` | `reference/` |
| `developer_*.md`, `testing.md`, `zmq_service_testing.md`, `module_map.md`, `validation.md` | `developer/` |
| `CHANGELOG_archive.md` | `changelog.md` (append) or leave out of the site |

(Mapping to be confirmed while doing it; a few files may split or merge.)

### 4.2 AIDA

Already task-oriented; mostly moves. One Help button (top page).

- `installation.md` → `getting-started/`; `gui-overview.md`, `concepts.md` → `getting-started/`
  (or keep `concepts.md` in `guides/`).
- `workspaces.md`, `organizing-conversations.md`, `documents.md`, `knowledge-bases.md`, `skills.md`,
  `workflows.md`, `coding-and-scripting.md`, `moving-and-sharing.md`, `pyirena.md`, `bernardyn.md`,
  `axis-camera.md` → `guides/`.
- `providers-and-secrets.md`, `mcp-servers.md`, `safety-and-permissions.md`,
  `context-and-limits.md` → `reference/`.
- `figures/` → `getting-started/img/concepts/` (with `make_figures.py`).
- `talk-intro-slide.md`, `docs/README.md` → out of `docs/` (talk material is not a manual page).
- `main_window.py`: replace `DOCUMENTATION_URL` (GitHub tree) with `docs_url()`.

### 4.3 Bernardyn

Small; mostly moves. One Help button (top page).

- `user-guide.md`, `workflow.md` → `guides/` (or split `user-guide.md` into `getting-started/`
  quickstart + guides).
- `data-flow-and-formats.md`, `mcp.md`, `headless-recipes.md` → `reference/` / `guides/`.
- `releasing.md` → `developer/`. `TODO.md`, `docs/README.md` → out of `docs/`.
- `bernardyn/schemas/graph-package-v3.md` → include it in `reference/` with `{include}` so the
  schema has one source.
- `_documentation_url()` today opens the local `docs/` folder for an editable checkout. Keep that
  fallback if you like it; otherwise use `docs_url()` always (simpler, and local `.md` files are
  less readable than the built site).

### 4.4 Transition: released Help buttons that point to GitHub

pyIrena 1.2.1 and AIDA 1.1.0 open GitHub URLs on `main`. When files move, those break. For about a
year, leave a one-line stub at each old pyIrena path, e.g. `docs/unified_fit_gui.md`:

```markdown
Moved to <https://jilavsky-docs.readthedocs.io/projects/pyirena/en/latest/tools/unified-fit.html>
```

Stubs point at `latest`, not `stable` (decided 2026-11-13): `stable` exists only from the next
release, and the tool pages change little between releases.

List the stubs in `LEGACY_GITHUB_STUBS` in `conf.py` so Sphinx skips them. AIDA's link is to the
`docs/` folder itself, which still exists, so it needs no stub.

## 5. Toolchain

| Piece | Choice |
|---|---|
| Generator | Sphinx 9.2.0, pinned exactly |
| Markdown | MyST-Parser 5.2.0 (Igor manuals stay reStructuredText) |
| Theme | PyData Sphinx Theme 0.24.0 |
| Extras | sphinx-design 0.8.0 (cards, tabs), sphinx-copybutton 0.5.2 |
| API | `autodoc` + `napoleon` (Google style); GUI libraries mocked |
| Versions menu | RTD's own flyout (RTD Addons). No PyData switcher JSON to maintain |
| RTD config | `.readthedocs.yaml`, ubuntu-24.04, Python 3.13, `fail_on_warning: true` |
| Search | RTD server-side search, which covers subprojects from the parent |
| CI | GitHub Action: `sphinx-build -W --keep-going` on PRs; RTD PR previews |
| Pin updates | Dependabot, monthly |

Changed from the draft:

- **No PDF/ePub at first** (`formats: []`). LaTeX chokes on some Unicode (Å⁻¹) and on
  sphinx-design layouts, and a failed PDF fails the whole build. Switch on per package later.
- **`sphinx-reredirects` only when the first redirect is needed**, not by default.
- **No version-switcher JSON**; RTD's flyout already lists versions.
- **Intersphinx to a family member only after it is live**, because the build treats an
  unreachable inventory as an error.
- **Sphinx gotcha found while testing:** a module-level name `version` in `conf.py` is read as a
  Sphinx setting, so the template uses `importlib.metadata.version(...)` without importing the
  bare name.

## 6. RTD admin steps (Jan)

1. Create GitHub repo `jilavsky/jilavsky-docs`; push this folder.
2. On RTD, import it as project **`jilavsky-docs`**.
3. For each package, import the repo as its own RTD project. The project slug must be unique on
   all of RTD (`aida` is taken), so use **`jilavsky-pyirena`, `jilavsky-bernardyn`,
   `jilavsky-aida`** for consistency. The slug never appears in links: readers see the alias.
4. In `jilavsky-docs` → Settings → Subprojects, add each with alias **`pyirena`, `bernardyn`,
   `aida`**.
5. Per project: default version `stable`; automation rule "activate version" for tags matching
   `^v\d+\.\d+\.\d+$` (all three packages already tag as `vX.Y.Z`); turn on pull-request builds.
6. `stable` exists only once a release tag is active. **Do not activate tags released before the
   package had Sphinx docs** (pyIrena ≤ v1.2.1, Bernardyn ≤ v1.1.0, AIDA ≤ v1.1.0): they have no
   `docs/conf.py` and their builds fail. Until the next release, only `latest` (built from `main`)
   exists. That is fine, because released copies still open GitHub (via the stubs, which point at
   `latest`). Dev installs of `main` report the release number and so open `stable`, which 404s
   until the next release; accepted on 2026-11-13 (only Jan is affected).
   Import each package on RTD after its `docs-rtd` branch is merged (or activate the branch on RTD
   to preview it before merging).
7. Igor manuals: no change. Optionally later, on a throwaway project, test whether attaching a
   project as a subproject keeps old deep links (`/en/1.7.0/Irena/UnifiedFit.html#…`) working.
   Only if it does, attach `saxs-igorcodedocs`.

## 7. Phases

| Phase | When | Output |
|---|---|---|
| 1. This repo | done (2026-11-13) | Home page, template, CI. Builds clean with `-W` |
| 2. RTD setup | late Nov, Jan | §6 steps 1–6 |
| 3. pyIrena | Dec | `docs-rtd` branch per §4.1; `_docs.py`; Help buttons switched; stubs |
| 4. AIDA, Bernardyn | Dec | same, per §4.2 and §4.3 |
| 5. Drafts and shot lists | Dec | Tool pages per `tools/_template.md`; `SHOTLIST.md`; automated screenshots (`QWidget.grab()`) where possible |
| 6. Walk-through | Christmas break, Jan | Screenshots and corrections |
| 7. Release | January | Next release of each package switches its Help buttons to RTD |
| Later | 2027 | Anisa, pyNika; Igor modernization (separate branch in SAXS_IgorCodeDocs) |

## 8. Igor manuals (unchanged from the draft, deferred)

Modernize `SAXS_IgorCodeDocs` in place on its `docs-restructure-2026` branch: new `conf.py`,
PyData theme, pinned requirements, wmf/emf → PNG, fix the missing `Irena/CylinderModels` page that
Igor links to, a link checker for the 49 `IN2G_OpenWebManual` targets. Never rename a page or a
heading Igor links to; never deactivate old versions.

## 9. Screenshots

As in the draft §7: shot lists first, automate with `QWidget.grab()`, PNG, light theme, fixed
window size, `<page>-<nn>-<what>.png`, < 300 KB, alt text required.
