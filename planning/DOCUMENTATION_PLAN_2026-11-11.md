# Documentation restructure plan — Irena family on Read the Docs

*Status: DRAFT for Jan's review — 2026-11-11. Nothing here has been implemented yet.*
*Branch: `docs-restructure-2026` (SAXS_IgorCodeDocs).*

## 1. Goals

1. One documentation home for the whole family: **Irena / Nika / Indra (Igor Pro)**, **pyIrena**,
   **Bernardyn**, **Matilda**, **AIDA**, **Anisa**, with room for later additions (e.g. **pyNika**).
2. Every GUI can deep-link to its own page. For example, pyIrena's *Unified Fit* Help button opens the
   pyIrena Unified Fit page, while AIDA's Help button opens the AIDA top page.
3. **No existing link breaks.** Released Igor code, old papers and emails all point at
   `saxs-igorcodedocs.readthedocs.io/...`.
4. A modern, pinned, maintainable toolchain that RTD stops complaining about.
5. A page structure an agent can draft from code and the existing Markdown, so that over the
   Christmas break Jan mainly captures screenshots and corrects the text, rather than writing pages.

## 2. What exists today (inventory)

### 2.1 SAXS_IgorCodeDocs (this repo)

| Item | Finding | Consequence |
|---|---|---|
| Started | March 2017 (`sphinx-quickstart`), 241 commits, tags `1.0` … `1.7.0` | Long version history on RTD |
| Size | ~177 MB git pack; media: Irena 130 MB, Nika 25 MB, Indra 19 MB | Don't merge this history into anything else |
| Source | 65 `.rst` files, ~570 png/jpg, 3 `.wmf` + 2 `.emf` | Browsers can't show wmf/emf; convert those 5 |
| `readthedocs.yaml` | No leading dot, so the path must be set in the RTD admin. ubuntu-24.04, Python 3.12, `formats: all` | Rename to `.readthedocs.yaml` and clear the admin override at the same time |
| `requirements.txt` | `sphinx>=5.0` (unpinned, so RTD currently builds Sphinx 9.1), `readthedocs-sphinx-search`, `setuptools` | The search extension is obsolete (RTD now does server-side search). Unpinned Sphinx means a new release can break a build without any change on our side |
| `conf.py` | 2017 boilerplate, `agogo` theme, `master_doc`, `u''` strings, only `mathjax` | Rewrite in about 60 lines |
| Built output | `docs/source/_build` (181 MB) is in the working tree but correctly git-ignored | OK |
| `PyIrena.rst` | Inside the Irena manual; points to GitHub Markdown | Becomes a short pointer to the new pyIrena docs. Keep its label `irena-pyirena` |

### 2.2 How Igor links into the docs (critical constraint)

`IN2_GeneralProcedures.ipf` builds URLs as
`http://saxs-igorcodedocs.readthedocs.io/` + `ManualVersionString` + page,
with `ManualVersionString = "en/1.7.0/"` (earlier releases used `en/1.4/` and `en/1.5.1/`).
There are **49 `IN2G_OpenWebManual(...)` calls**, some with anchors, e.g.
`Irena/DataManipulation.html#data-manipulation-2` or `Irena/bioSAXS.html#biosaxs-pddf`.

This means:

- The project `saxs-igorcodedocs` and its **old versions (1.4, 1.5.1, 1.7.0, …) must stay online indefinitely.** Never deactivate them.
- Page file names and the section titles that generate anchors are a **frozen contract** for Irena/Nika/Indra.
- `Irena/CylinderModels.html` is referenced from Igor but **no such page exists**, so that link is already broken. Fix it with a redirect or a page.
- Do not rebuild old versions. RTD removed the ubuntu-20.04 image in June 2026, so old tags might not build any more. Their already-built HTML is still served.

### 2.3 The Python packages

| Package | Repo | Version | Existing docs (`docs/`) | Current Help-button target |
|---|---|---|---|---|
| pyIrena | jilavsky/pyirena | 1.2.1 | ~40 `.md` files, ~19k lines (GUI guides, methods, API, developer) | GitHub `blob/main/docs/<tool>.md`, one URL per panel (~13 panels) |
| Bernardyn | jilavsky/bernardyn | 1.1.0 | 8 `.md` (user guide, workflow, MCP, recipes) | Local `docs/` folder if editable install, otherwise GitHub |
| Matilda | **APS-USAXS**/Matilda | 0.3.0b1 | 11 `.md` + figures | GitHub `docs/matilda-gui.md` |
| AIDA | jilavsky/aida | 1.0.1 | 20 `.md` + figures (already a task-oriented guide set) | GitHub docs |
| Anisa | jilavsky/anisa | 0.0.1b1 | 1 `.md` (parameters) | — |
| pyNika *(not in your list)* | jilavsky/pynika | 1.0.0 | md guides | — |

All the Python documentation is already **Markdown**, which decides the format choice below. The docs are
not shipped in the wheels (pyIrena packages only `pyirena*`), so screenshots stored in the repo do not
bloat what users install.

## 3. Recommended architecture

### 3.1 One RTD *parent* project, with each package as a *subproject*

```
https://<parent>.readthedocs.io/en/latest/                         ← family home page (new repo)
https://<parent>.readthedocs.io/projects/pyirena/en/stable/...     ← docs from jilavsky/pyirena
https://<parent>.readthedocs.io/projects/bernardyn/en/stable/...
https://<parent>.readthedocs.io/projects/matilda/en/stable/...
https://<parent>.readthedocs.io/projects/aida/en/stable/...
https://<parent>.readthedocs.io/projects/anisa/en/stable/...
https://saxs-igorcodedocs.readthedocs.io/en/stable/...             ← unchanged (see 3.4)
```

Why subprojects:

- **Independent versions.** Each subproject keeps its own versions, releases and flyout menu. pyIrena
  can release monthly and Igor yearly, without coupling.
- **Joint search.** A search on the parent includes subproject results, with a per-project filter.
- **Short names are scoped to the parent.** The global RTD slugs `aida` and `matilda` are already taken
  by unrelated projects, but the subproject *alias* can still be `aida` or `matilda`.
- Each subproject is a normal RTD project, so it can be detached or moved later.

Alternative considered: separate top-level projects (`pyirena.readthedocs.io`, …). That gives shorter
URLs but no shared search or domain, and two of the names are unavailable. Not recommended.

Alternative considered: a single monorepo and single Sphinx build containing everything. That gives one
version number for all packages and makes per-package versioned docs impossible. Not recommended.

### 3.2 Where each package's docs live: in the package's own repo

Each package keeps its docs in `docs/` of its own repo, and its RTD subproject builds from there.

- Docs are versioned with the code automatically. Tag `v1.3.0` produces docs version `v1.3.0`.
- An agent changing a GUI updates its page in the **same PR**, and a test can enforce this (see 4.3).
- The API reference can be generated from the docstrings.
- The existing Markdown files become pages with minimal changes.

### 3.3 New repo for the family home page (the "parent")

Proposed: a new repo, e.g. `jilavsky/irena-family-docs` (name to decide, D1). It is small and text-only, and holds:

- **Home**: what each package is for, with one card per package and links.
- **Which tool do I need?** A decision table (reduce at 12-ID: Matilda; analyze: pyIrena or Irena;
  publication figures: Bernardyn; anisotropic samples: Anisa; AI-assisted work: AIDA).
- **Installing the family** into one Python environment (they are designed to share one).
- **Data formats shared by everyone**: NXcanSAS/HDF5 layout and the results groups each package writes.
- **End-to-end workflows** across packages (measure → Matilda → pyIrena → Bernardyn → AIDA).
- **Irena ↔ pyIrena tool map** (see §6), for users migrating from Igor.
- **How to cite**, papers, release news.
- Link to the Igor manuals.

Cross-package material lives here and nowhere else, so it is not duplicated in five places.

### 3.4 Igor manuals: keep the project and repo, modernize in place

Moving them into the new repo would drag 177 MB of history along and gain nothing. Instead:

- Keep `saxs-igorcodedocs` exactly where it is. Modernize the toolchain on this branch (§5).
- Rename only the **display name**, e.g. "Igor Pro packages: Irena, Nika, Indra". The slug and URLs stay as they are.
- Link it from the parent home page and the navbar of every subproject.
- **Optional, later:** attach it as a subproject (`/projects/igor/`). RTD then redirects the old
  subdomain to the parent. It's **not yet verified** whether the redirect keeps the full path and anchor
  (`/en/1.7.0/Irena/UnifiedFit.html#…`). Test this on a throwaway project before trying it. Until it's
  proven, keep Igor stand-alone. Nothing is lost, because the navbar links make it look like one site
  anyway.

### 3.5 Optional: a custom domain

RTD Community supports custom domains. Something like `docs.usaxs.xray.aps.anl.gov` (APS IT would need
to add a CNAME) or a personal domain makes the URLs independent of the RTD slug and of RTD itself.
Not needed to start; it can be added later without breaking the `readthedocs.io` URLs (RTD redirects them).

## 4. Deep linking from the applications

### 4.1 One helper per package

```python
# pyirena/_docs.py  (same pattern in each package)
from importlib.metadata import version

_BASE = "https://<parent>.readthedocs.io/projects/pyirena/en/{ver}/"

HELP_TARGETS = {            # GUI id  → page (path relative to the docs root, without .html)
    "home":          "",
    "unified_fit":   "tools/unified-fit",
    "size_dist":     "tools/size-distribution",
    "modeling":      "tools/modeling",
    "simple_fits":   "tools/simple-fits",
    "fractals":      "tools/fractals",
    "waxs_peakfit":  "tools/waxs-peak-fit",
    "carbon_fit":    "tools/carbon-fit",
    "saxs_morph":    "tools/saxs-morph",
    "data_merge":    "tools/data-merge",
    "data_manip":    "tools/data-manipulation",
    "contrast":      "tools/scattering-contrast",
    "hdf5_viewer":   "tools/data-explorer",
    "data_selector": "tools/data-selector",
}

def docs_url(target: str = "home", anchor: str = "") -> str:
    v = version("pyirena")
    ver = "latest" if ("dev" in v or "+" in v) else "stable"      # see decision D3
    page = HELP_TARGETS[target]
    url = _BASE.format(ver=ver) + (page + ".html" if page else "")
    return url + (f"#{anchor}" if anchor else "")
```

The panels then call `QDesktopServices.openUrl(QUrl(docs_url("unified_fit")))`. AIDA and Bernardyn call
`docs_url()`, which opens the top page. Bernardyn's existing "local docs for an editable checkout"
fallback can stay.

### 4.2 Stable page names are a contract

- A file under `tools/` is **never renamed** once released. If a rename is unavoidable, add a redirect
  with `sphinx-reredirects` in `conf.py`, so the redirect is version-controlled and reviewable.
- Use explicit MyST labels, e.g. `(unified-fit-levels)=`, for anchors the GUI links to. Don't rely on
  auto-generated heading anchors (the Igor manuals depend on those, and that is fragile).

### 4.3 A test that guards the contract (in each package's test suite)

`tests/test_help_targets.py` checks that every `HELP_TARGETS` value has a matching `docs/<page>.md` file,
and that every anchor used in the code exists as a label. It costs nothing and catches the "renamed the
page, broke the Help button" class of bugs at PR time.

For the **Igor** manuals, the equivalent is a script (`tools/check_igor_links.py` in this repo) that pulls
the 49 `IN2G_OpenWebManual` targets out of SAXS_IgorCode and checks them against the built HTML, page and
anchor. Run it before every Igor docs release.

### 4.4 Transition from the current GitHub links

Released versions of pyIrena, Matilda and AIDA open `github.com/.../blob/main/docs/<file>.md`. If those
files move or disappear, the Help buttons in already-installed copies break. Two ways to handle this:

- Keep the existing `docs/*.md` file names where they make sense as page names, or
- Leave a one-line stub at each old path ("Moved to <RTD URL>") for about a year.

## 5. Modernized toolchain (same for every project)

| Piece | Choice | Notes |
|---|---|---|
| Generator | **Sphinx 9.x**, pinned | RTD already builds 9.1 for us, just unpinned |
| Markdown | **MyST-Parser** | Python docs stay `.md`; Igor stays `.rst`; both work in one project |
| Theme | **PyData Sphinx Theme** | Maintained, used by NumPy/SciPy. Shared top navbar with links to every family member, plus a version switcher. (Furo is the simpler alternative, but it has no family navbar.) |
| Layout helpers | `sphinx-design` | Cards on the home page; **tabs on tool pages: "GUI / Python script / MCP (AIDA)"** |
| Others | `sphinx-copybutton`, `sphinx-reredirects`, `sphinx.ext.intersphinx`, `autodoc` + `napoleon` | Intersphinx gives typed cross-links between projects (pyIrena page → Irena page, and back) |
| API reference | `autodoc` with `autodoc_mock_imports = ["PySide6", "pyqtgraph", …]` | Keeps the RTD build light |
| Removed | `readthedocs-sphinx-search`, `setuptools`, `agogo` | |
| RTD config | `.readthedocs.yaml`: ubuntu-24.04, Python 3.13, `formats: [pdf, epub]` | RTD natively supports `uv` since April 2026 (optional) |
| Pinning | `docs/requirements.txt` with exact versions, updated by Dependabot | Builds only change when we decide |
| `conf.py` | ~60 lines; `html_baseurl` from `READTHEDOCS_CANONICAL_URL` | |
| Quality gate | GitHub Action: `sphinx-build -W --keep-going` + linkcheck on PRs; RTD PR previews on | |
| Branding | One small family logo + per-package accent colour | Same `conf.py` template copied into each repo. A shared mini-package is only worth it if the copies drift |

Igor-specific clean-up on this branch: convert the 5 wmf/emf images to PNG/SVG, fix `CylinderModels`,
switch the theme, and run the link check from §4.3. **Don't rename any page or any section heading
that Igor links to.**

## 6. Content structure

### 6.1 Per-package layout (Python packages)

```
docs/
  conf.py
  requirements.txt
  index.md                    ← what it is, who it's for, screenshot, "start here"
  getting-started/
    installation.md
    quickstart.md             ← 10-minute first result with bundled test data
  tools/                      ← ONE PAGE PER GUI TOOL = Help-button targets (stable names)
    unified-fit.md
    img/unified-fit/*.png
  guides/                     ← task-oriented how-tos (batch fitting, scripting, Jupyter, AIDA use)
  methods/                    ← theory and algorithms (sizes methods, slit smearing, fit metrics)
  reference/                  ← API (autodoc), file format/HDF5 layout, CLI, MCP tool list
  developer/                  ← adding form factors, testing, releasing
  changelog.md                ← includes ../CHANGELOG.md
```

This follows the Diátaxis split (tutorial / how-to / explanation / reference) that most scientific
Python projects use. The point is to keep **"what does this button do"** (`tools/`) apart from **"why does
the math work"** (`methods/`).

### 6.2 Standard tool page template (for agent drafting)

```markdown
(unified-fit)=
# Unified Fit

:::{admonition} At a glance
Launch: `pyirena-gui` → Unified Fit · Script: `pyirena.unified.fit(...)` ·
MCP tool: `unified_fit` · Igor equivalent: {doc}`Irena Unified Fit <igor:Irena/UnifiedFit>`
:::

One-paragraph purpose and when to use it (and when not to).

## The window            ← annotated full-window screenshot, numbered callouts
## Typical workflow      ← 5–8 numbered steps with one screenshot each, using bundled test data
## Controls              ← table: control · meaning · default · tips
## Results and outputs   ← what is saved, where in the HDF5 file, how to reuse it
## Doing it from Python / from AIDA   ← sphinx-design tabs
## Method notes          ← short; link to methods/ for the theory
## References
```

Every tool page has the same structure, so users learn it once, an agent can fill it consistently,
and a gap is easy to spot.

### 6.3 Irena ↔ pyIrena map (first pass, to verify)

| pyIrena tool | Irena page |
|---|---|
| Unified Fit | UnifiedFit |
| Size Distribution | SizeDistribution |
| Modeling | Modeling / ModelingModels |
| Simple Fits | SimpleFits |
| Fractals | Fractals |
| WAXS Peak Fit | WAXS |
| Data Merge, Data Manipulation | DataManipulation |
| Scattering Contrast | ScatteringContrastCalculator |
| Data Explorer (HDF5 viewer) | HDF5Browser |
| SAXS Morph | TwoPhaseSolid (?) |
| Carbon Fit, Feature Identifier, Diffraction Lines | — (new in pyIrena) |

Each pair links both ways: a "Python version" note on the Irena page, and "Igor equivalent" on the pyIrena page.

## 7. Screenshots: making Christmas efficient

1. **Shot lists first.** For each tool page, the agent writes `docs/tools/SHOTLIST.md`: shot id,
   window, dataset (from `testData/`), state to set up, and what the shot must show. Jan works down the list.
2. **Automate what can be automated.** Most Qt panels can capture themselves (`QWidget.grab()`).
   `scripts/make_doc_screenshots.py` opens each tool on bundled test data, sets a fixed window size, runs
   the fit and saves the PNGs. When the GUI changes, re-run the script and the screenshots are updated.
   Jan then only takes the shots that need judgment (a good fit, a tricky state).
3. **Conventions.** PNG; light theme; fixed window size; filename `<tool>-<nn>-<what>.png` in
   `tools/img/<tool>/`; optimized (oxipng/pngquant, aim for < 300 KB); alt text required; callout numbers
   added in the image, not in the text.
4. **Placeholders.** Agent drafts use `{figure-placeholder} unified-fit-03` blocks, so the build stays
   green and missing shots are listed automatically.

## 8. Phases and timeline

| Phase | When | Who | Output |
|---|---|---|---|
| 0. Decisions | by ~Nov 25 | Jan | Answers to §9 |
| 1. RTD setup | late Nov | Jan (RTD admin), agent (files) | Parent repo and RTD project; subprojects created; PR builds; tag automation rules |
| 2. Igor modernization | Dec, on this branch | agent | New `conf.py`/theme/requirements, wmf→png, link checker green, `PyIrena.rst` → pointer |
| 3. Package skeletons | Dec, branch `docs-rtd` in each repo | agent | `docs/` restructured per §6.1, existing md ingested, `_docs.py` + help-target test, builds green on RTD |
| 4. Drafts and shot lists | Dec | agent | Tool pages per template with placeholders; SHOTLIST.md; automated screenshots where possible |
| 5. Walk-through | Christmas break | Jan | Screenshots, corrections, gaps noted |
| 6. Switch-over | January | agent + Jan | Merge; next release of each package switches its Help buttons to RTD; stubs at old GitHub paths; home page live |

Suggested order of packages: **pyIrena** (largest, most Help buttons; sets the pattern) → **AIDA**
(already well structured, mostly moving files) → **Bernardyn** → **Matilda** → **Anisa** (skeleton only
until it is validated).

### RTD admin tasks only Jan can do

Create the parent project and import each repo; add the subprojects with aliases; set the default version
to `stable`; add an automation rule "activate new tags matching `^v\d+\.\d+\.\d+$`" per subproject;
enable pull-request builds; decide on ads (EthicalAds on Community; Gold membership removes them);
optionally add a custom domain. For **Matilda**, the RTD GitHub app needs access to the APS-USAXS org.

## 9. Decisions for Jan

| # | Question | Options | Recommendation |
|---|---|---|---|
| D1 | Parent slug and repo name | e.g. `irena-family`, `usaxs-software`, `ilavsky-sas`, `aps-sas-tools` (check availability on RTD) | A name that is about the software family, not the beamline, since pyIrena/AIDA users are everywhere |
| D2 | Igor docs: stand-alone or subproject? | stand-alone + navbar links / subproject after a redirect test | Stand-alone for now |
| D3 | Help links: `stable` or the installed version? | `stable` (always newest docs) / `v{installed}` (exact match, as Igor does) | `stable` for releases, `latest` for dev installs; revisit if docs start drifting from older releases |
| D4 | Theme | PyData / Furo / Book | PyData (family navbar) |
| D5 | Custom domain now or later? | now / later / never | Later |
| D6 | Matilda in the family docs? | yes / separate (it is an APS-USAXS org repo, beamline-specific) | Yes, as a subproject; its beamline-staff pages (daemon, service) go under a "Beamline staff" section |
| D7 | Include pyNika? | now / later | Reserve a slot; add when ready |
| D8 | Ads | accept EthicalAds / Gold membership | Your call; doesn't affect the structure |

## 10. Risks

- **Breaking Igor links.** Mitigated by the §2.2 rules and the link checker. Old versions are never deactivated.
- **Docs drifting from the GUI.** Mitigated by the help-target test, the same-PR rule, and automated screenshots.
- **Repo growth from screenshots.** Docs stay out of the wheels; images are optimized; a re-shoot
  overwrites files in place instead of adding new ones.
- **RTD changes terms.** All content is plain Sphinx/Markdown in git. It can be moved to GitHub Pages in
  about a day per project (losing only the hosted versioning and search).
