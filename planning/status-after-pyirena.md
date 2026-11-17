# Status after phase 3 (pyIrena): open decisions and undone work

*Written 2026-11-13 by the agent that carried out `handoff-pyirena.md` in
`/Users/ilavsky/GitHub/pyirena`. For Jan and for the agent that continues with AIDA and
Bernardyn. Read this before reusing the brief.*

## Where pyIrena stands

- Branch `docs-rtd` in pyirena, two commits, **not pushed, no PR**:
  - `00b573e`: only `git mv` renames, so `git log --follow` keeps history. Tests fail at this
    commit on its own; they pass after the next one.
  - `d4435a1`: everything else (template files, link fixes, `pyirena/_docs.py`, 13 Help buttons,
    13 stubs, tests, pointer updates, CHANGELOG entry).
- Checks: `sphinx-build -W --keep-going` gives zero warnings; full suite 2195 passed, 8 skipped;
  `ruff` clean; `docs/` is not in the wheel.
- I changed nothing in the template except the PER-PACKAGE block of `conf.py`.
- The mapping actually used is PLAN.md §4.1, with these differences:
  - `unified_fit_features.md` was **deleted, not merged**. It is a February 2026 v0.x
    development log, and its useful parts were already in the GUI page.
  - `distribution.md` went to `developer/`: it is the PyPI/conda release guide, not a method.
  - `CHANGELOG_archive.md` became its own page, `changelog-archive.md`.
  - `QUICK_START.md` became `getting-started/python-quickstart.md`, and `usage_guide.md` became
    `guides/scripting-unified-fit.md`.

## Decided 2026-11-13

- **Decision 1 → (c), accepted.** Dev installs of `main` open `stable` and 404 until the next
  release. Only Jan is affected. `docs_version()` stays as it is. PLAN.md §6 is updated.
- **Decision 2 → `latest`.** pyIrena's 13 stubs and the CHANGELOG doc links point at `latest`
  (pyirena commit `5957cb3`). PLAN.md §4.4 and the brief are updated. The PyPI `Documentation`
  URL in `pyproject.toml` stays at `stable`: PyPI shows it only from the next release, when
  `stable` exists.
- **Decision 3 → NumPy style on.** `napoleon_numpy_docstring = True` in the template and in
  pyIrena's `conf.py`. The pyIrena build still gives zero warnings, and NumPy `Parameters`
  sections now render as field lists. AIDA and Bernardyn get it from the template.

The original text of decisions 1–3 is kept below for the record.

## Decisions Jan needs to make

### Template-level (1–3 decided, see above)

1. **Dev installs open `stable`, not `latest`.** `docs_version()` returns `latest` only for
   version strings with `dev`, `+`, `a`, `b` or `rc`. All three packages keep the release number
   in `pyproject.toml` between releases; pyirena `main` says `1.2.1`. So an editable checkout of
   `main` opens `stable`, which contradicts PLAN.md §6 step 6 ("dev installs open `latest`").
   Until the first release after the move, that is a 404. Options:
   - **(a)** Bump to a `.devN` version right after each release. This changes the release
     routine of all three packages.
   - **(b)** Make `docs_version()` also return `latest` for an editable or source install, by
     checking `direct_url.json` from `importlib.metadata`. This is a template change, and it
     works without changing the release routine.
   - **(c)** Accept it. Only developers are affected, and only until the next release.
2. **Where the transition stubs point.** The brief says `stable`. But `stable` does not exist
   until the next release, so v1.2.1 users who click Help land on the stub and then get a 404
   (once `docs-rtd` is merged to `main`). Pointing the stubs at `latest` works immediately. The
   catch is that `latest` follows `main`, which may describe features not yet released. Only
   pyIrena needs stubs. Decide before merging pyirena `docs-rtd`.
3. **NumPy-style docstrings.** The template turns on napoleon for Google style only. Many
   pyIrena docstrings are NumPy style, so they render as plain text blocks on the API page; they
   build without warnings, but not nicely. Turning on `napoleon_numpy_docstring` alone did not
   fix the warnings I had. The choices:
   - turn on both styles in the template;
   - or convert docstrings to Google style over time (the house standard says Google).

   I converted one docstring, `write_iq_data`, because a parameter named `error:` was being shown
   as an "Error" warning box.
4. **CHANGELOG links into `docs/`.** `docs/changelog.md` includes the root `CHANGELOG.md`.
   Relative links in that file cannot work both on GitHub and in the site, so I changed
   pyIrena's to absolute RTD `stable` URLs. Alternatives:
   - the `:relative-docs:` option on the MyST include, untested;
   - or a rule in the template README: "CHANGELOG links to docs use absolute URLs".

   This matters only for packages whose CHANGELOG links into `docs/`.

### pyIrena-specific

5. **Approve the judgment calls** listed above, plus three more:
   - **The Sizes page split.** The tool page has the controls, the fit window, how to read the
     plot, fit quality and slit smearing. The methods page has the four methods, the comparison
     and the references.
   - **The API page** autodocs only `pyirena.batch` and `pyirena.io`.
   - **Dead links** to files that never existed were pointed at the right page, or the link was
     removed and the text kept.
6. **When to push and merge `docs-rtd`.** Merging puts the stubs on `main`, and that interacts
   with decision 2.
7. **`family.css` accent colour.** I left the template default. Pick a per-package colour now,
   or never.

## Undone / known gaps

- **No live RTD build yet.** RTD setup is Jan's phase 2. The build was verified locally only, in
  `/tmp/pyirena-docs-venv`.
- **Help buttons:** I clicked 7 of the 13 offscreen and each gave the correct URL. The other 6
  panels need constructor arguments my offscreen check did not supply; they import fine and got
  the same mechanical edit.
- **Stale content, left untouched** because this phase does not rewrite text. It belongs to phase
  5 (drafts):
  - `developer/testing.md`, `getting-started/python-quickstart.md` and
    `guides/scripting-unified-fit.md` refer to demos and files that no longer exist;
  - the intro of `methods/size-distribution-methods.md` says "three methods" and then describes
    four.
- **No CI workflow added to pyirena.** PLAN.md §5 lists a GitHub Action that runs
  `sphinx-build -W` on PRs, but neither the brief nor the template includes one. Add it to the
  template, then copy it to each package.
- **No Dependabot config** for the `docs/requirements.txt` pins (PLAN.md §5). Same as above:
  template first.
- No screenshots, no `tools/_template.md` drafts: phase 5, as planned.

## Notes for reusing the brief (AIDA, Bernardyn)

- Run `grep -rn "docs/" <pkg> tests` early. In pyIrena, four tests and many comments read
  `docs/` paths.
- On macOS, the file system is case-insensitive, so a link to `../CHANGELOG.md` from
  `docs/changelog.md` looks valid locally but is not. Check links against `git ls-files`, not
  with `os.path.exists`.
- Fix links in two passes:
  1. links between moved pages, resolved against the new folders;
  2. links into the repo (`../pyirena/...`), resolved against the **old** flat `docs/` folder,
     then turned into GitHub URLs.
- Docstrings that look fine in an IDE can still produce Sphinx warnings with `-W`: RST example
  blocks need `::`, and a `name:` line that matches a napoleon section word (Error, Note,
  Example…) becomes a box. Fix these in the docstring itself. Don't loosen the template to hide
  them.
- Keep the rename commit separate. It is worth it for `git log --follow`.
- Decision 1 affects AIDA and Bernardyn exactly as it affects pyIrena.

## Readiness to continue

Yes. The template decisions (1 and 3) are settled, and the template is updated, so AIDA and
Bernardyn can start from it now. Decisions 4–7 can wait for the review after all three packages
are done; that is also when pyirena `docs-rtd` should be pushed.

## Bernardyn (done 2026-11-13)

*By the agent that carried out `handoff-aida-bernardyn.md` in `/Users/ilavsky/GitHub/Bernardyn`.*

- Branch `docs-rtd` from `main`, two commits, **not pushed**: `35796a1` (renames only) and
  `ac0abe7` (everything else). Note: before starting, Jan merged `fix/issue-1-code-review` into
  `main` (fast-forward, pushed), so `docs-rtd` contains that fix commit too.
- Checks: `sphinx-build -W --keep-going` zero warnings (venv `/tmp/bernardyn-docs-venv`); full
  suite 322 passed, 4 skipped; `ruff` clean; `docs/` not in the wheel. Template files are
  identical to the template apart from the PER-PACKAGE blocks.
- Mapping used:
  - `user-guide.md`, `workflow.md`, `headless-recipes.md` → `guides/` (user guide not split).
  - `data-flow-and-formats.md`, `mcp.md` → `reference/`; `releasing.md` → `developer/`.
  - `TODO.md` → repo root; `docs/README.md` deleted (its maintenance rule moved to
    `developer/index.md`).
  - `reference/graph-package-v3.md` `{include}`s `bernardyn/schemas/graph-package-v3.md`, with a
    short "Earlier versions" note linking v1/v2 on GitHub.
- Judgment calls:
  - **Sections without content are left out** of the toctree and the folder (no `tools/`,
    `methods/`, no `quickstart.md`), instead of building empty placeholder pages.
  - `getting-started/installation.md` `{include}`s README's "Install and run" section
    (`start-after`/`end-before`), so the install text has one source.
  - `developer/extending.md` `{include}`s `bernardyn/EXTENDING.md` (not in the brief; one
    source, no edits).
  - API page: `automodule:: bernardyn` with `:members:`, which follows `__all__` (recipe facade +
    document model). Added a one-line docstring to `list_recipes` so it appears.
  - `HELP_ANCHORS` kept as an empty dict so `_docs.py` and the test stay identical to the
    template; the anchor test therefore shows one "empty parameter set" skip.
  - User guide sentence about the Documentation button updated to match the new behaviour (the
    only content edit beyond links). No transition stubs: no released link to a specific
    `docs/*.md` file (released 1.1.0 opens the GitHub `docs/` tree, which still exists).
- Gaps: `family.css` accent left at the default (decision 7); no live RTD build yet.
- Template suggestions: (1) say in the README that empty sections may be omitted, or decide
  that every package keeps all six; (2) document the `{include}` + `start-after` pattern for
  reusing README install text; (3) the anchor test's empty-parameter skip could use
  `pytest.mark.skipif(not HELP_ANCHORS, ...)` for a clearer message.

## AIDA (done 2026-11-13)

*By the agent that carried out `handoff-aida-bernardyn.md` in `/Users/ilavsky/GitHub/Aida`.*

- Branch `docs-rtd` from `main`, two commits, **not pushed**: `4cdd341` (renames only) and
  `6f3b984` (everything else).
- Checks: `sphinx-build -W --keep-going` zero warnings (venv `/tmp/aida-docs-venv`); non-GUI
  suite 1751 passed, 27 skipped; GUI suite 750 passed (offscreen); `ruff check` and
  `ruff format --check` clean; `docs/` not in the wheel (wheel has only `src/aida` + `skills`).
  Template files identical apart from the PER-PACKAGE blocks.
- Mapping used: PLAN.md §4.2 as written. `concepts.md` went to `getting-started/` (with
  `installation.md`, `gui-overview.md`). `docs/figures/` (PNG, SVG and `make_figures.py`) →
  `getting-started/img/concepts/`, file names unchanged; the script writes next to itself, so it
  still writes where the page reads. `talk-intro-slide.md` → `planning/`.
  `docs/README.md` → `docs/index.md` (`git mv`), rewritten as the home page: same status
  banner, page table (now `{doc}` links, plus the two pages it was missing) and "Not
  implemented yet" section, with the toctree.
- Judgment calls:
  - **Sections without content left out**, same as Bernardyn: no `tools/`, `methods/`,
    `developer/`, no `quickstart.md`.
  - **No API page.** AIDA is an application; nothing in README or `docs/` presents a public
    Python API, so there is nothing stable to autodoc. `autodoc_mock_imports = ["PySide6"]`.
  - `MainWindow.DOCUMENTATION_URL` removed; button, Help menu, tooltip and About box call
    `docs_url()`. GUI tests compare against `docs_url()`.
  - **README links into `docs/` → absolute RTD `latest` URLs** (as for the CHANGELOG). README is
    also the PyPI page, where relative links never worked.
  - User-visible messages that name a doc path (`aida doctor`, the keychain error, the PySide6
    import diagnosis) now name the **new repo path** (`docs/getting-started/installation.md#…`),
    not an RTD URL. That keeps this phase free of behaviour changes, but a pip user has no
    `docs/` folder: pointing these at the site would be better. Open follow-up.
  - Links in the historical planning notes (`planning/COMPLETED.md`, `planning/completed/`)
    fixed so they resolve; their prose was left alone.
  - One code fence in `reference/mcp-servers.md` changed `bash` → `text`: Pygments failed on an
    apostrophe inside a `<placeholder>` (`misc.highlighting_failure` is a warning under `-W`).
  - **`docs/conf.py` excluded from `ruff format`** in `pyproject.toml` (reason written there).
    AIDA's CI runs `ruff format --check .`, and the template does not pass it (column-aligned
    comments in PER-PACKAGE, one long `FAMILY` line). See template suggestion 1.
  - No transition stubs: the released 1.1.0 opens the GitHub `docs/` tree, which still exists.
    Nothing released links a specific `docs/*.md` file (the in-app messages print paths as text).
- Content left as it is (phase 5): `concepts.md` still says "Status: draft for review" and ends
  with "Notes for the talk"; `index.md` lists remote HTTP MCP servers as "parked" although
  `reference/mcp-servers.md` documents them.
- Gaps: `family.css` accent left at the default (decision 7); no live RTD build yet. Help
  button checked through the GUI tests (offscreen), not clicked by hand.
- Template suggestions:
  1. **Make `docs/conf.py` pass `ruff format`** (single space before the PER-PACKAGE comments,
     wrap the Igor `FAMILY` entry). Then any repo can format-check it, and AIDA can drop its
     exclude.
  2. Same as Bernardyn: say that empty sections may be omitted.
  3. The README could say that README links into `docs/` should also be absolute RTD URLs
     (the README is the PyPI page).

## Review and template sync after all three (2026-11-13)

*From the jilavsky-docs session, after the pyIrena, Bernardyn and AIDA reports.*

Decided by Jan:

- **Judgment calls in all three reports: approved** (nothing reverted).
- **Accent colours: one per package.** Light / dark pairs, all ≥ 4.5:1 as link text:
  home `#2f4b66`/`#9bb8d3`, pyIrena `#1f6fb2`/`#6cb4f0`, Bernardyn `#0b7a66`/`#4cc7ae`,
  AIDA `#6a44b0`/`#b29af0`. `family.css` now sets the dark theme too.
- **CHANGELOG and README links into `docs/`: absolute RTD `latest` URLs** (template README).
- **Bernardyn Help always opens the site** (no local-folder fallback).
- **AIDA's user-visible messages point at the site**, not repo paths: `aida doctor`, the keychain
  error and the PySide6 import help use `docs_url()`, with explicit labels guarded by
  `HELP_ANCHORS` (`secrets`, `gui-fails-to-import-on-headless-linux`).
- **Push and merge: Jan, after reviewing the sync commits.**

Template changes from the package suggestions, all applied:

1. `conf.py` passes `ruff format` (Igor URL named once as `_IGOR`); AIDA's format exclude removed.
2. Optional sections (`tools/`, `methods/`, `developer/`) are left out until they have a page.
3. `{include}` with `start-after`/`end-before` documented for reusing README text.
4. Anchor test skips with "no HELP_ANCHORS defined" instead of an empty parameter set.
5. README links into `docs/` use absolute RTD URLs, like CHANGELOG links.

Synced into each `docs-rtd` branch as one extra commit: `conf.py` (template + own PER-PACKAGE
block), `test_help_targets.py`, `family.css`; pyIrena also got `.github/workflows/docs.yml`,
`.github/dependabot.yml` and the corrected `_docs.py` docstring.
