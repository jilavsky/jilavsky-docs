# Package docs template

Copy this into a family package repo to give it the standard docs layout (PLAN.md §3).

## Apply to a package

1. Copy `.readthedocs.yaml`, `.github/workflows/docs.yml`, `.github/dependabot.yml` and `docs/`
   to the repo root (screenshot machinery: see "Screenshots" below). Do not copy this README. If the repo already has a `dependabot.yml`, merge
   the entry into it.
2. In `docs/conf.py`, edit only the `PER-PACKAGE` block (`PACKAGE`, `DIST`, `project`,
   `GITHUB_REPO`, `SRC_DIR`, `autodoc_mock_imports`, `LEGACY_GITHUB_STUBS`).
3. In `docs/_static/family.css`, set the two accent values from the table at its top.
4. In `docs/index.md` and `docs/reference/api.md`, replace `pyIrena` / `pyirena`.
5. Copy `pkg/_docs.py` to `<package>/_docs.py` (AIDA: `src/aida/_docs.py`); set `DIST` and
   `SUBPROJECT`.
6. Copy `tests/test_help_targets.py`; fix its import line.
7. Move the existing Markdown into the sections (see PLAN.md §4). List each page in its
   section's `index.md`.
8. Build: `pip install -r docs/requirements.txt && sphinx-build -W --keep-going -b html docs docs/_build/html`.
9. Add `docs/_build/` to `.gitignore`. Make sure `docs/` is not packaged into the wheel.
10. Switch the GUI Help buttons to
    `QDesktopServices.openUrl(QUrl(docs_url("<target>")))`.

## Tool pages

Start from `docs/tools/_template.md` (excluded from the build). Every section gets a label
`(<page>-<section>)=` with these suffixes: `window`, `workflow`, `controls`, `results`,
`scripting`, `method`, `references` (add others freely, e.g. `unified-fit-slit-smearing`). Help
buttons that jump into a page (`HELP_ANCHORS`) use these labels. Labels are a contract once
released: add, never rename or remove.

## Working notes in pages

Two kinds of MyST comment (`% ...`), invisible on the rendered site:

- `% SCREENSHOT <id>: <what it must show>` marks an image still to be taken. When the image
  exists, replace the comment with a `figure` with alt text and caption.
- `% CHECK(Jan): <doubt>` marks text that may be wrong and needs the author's decision.

`html_copy_source = False` in `conf.py` keeps them out of the published `_sources/`. They are
still visible in the public GitHub repository.

## Screenshots

Copy `scripts/make_doc_screenshots.py`, `scripts/doc_shots/` (all of it),
`tests/test_doc_screenshots.py` and `planning/docs-screenshots/SHOTLIST.md`.

- **Only `scripts/doc_shots/_package.py` differs per package**: data folder, callout colour,
  `isolate_settings()` (point every settings/state location of the package at a scratch folder:
  environment variables, `HOME`, `QSettings`, `QStandardPaths`, keychain) and `make_app()`
  (offscreen app as the real one sets it up: names, light theme or Fusion, default font,
  `refuse_message_boxes()`). Package-specific helpers (e.g. waiting for a fit job, a lock if
  shots rebuild a fixed `/tmp/<pkg>-docs` folder) go there too. Everything else stays identical
  to the template.
- A shot ID is `<page>-<nn>-<what>`; the image lives next to the page:
  `<page dir>/img/<page>/<id>.png`. Page file names must be unique across `docs/`, except
  `index`: `index-<nn>-…` shots belong to the home page `docs/index.md`.
- One module per page, `scripts/doc_shots/<page>.py`, registering shots with `@shot("<id>")`
  (pattern in `_example.py`). Shots that need judgment stay as `% SCREENSHOT` comments.
- Inputs are always scratch copies (`ctx.dataset(...)`); fixed window sizes; light theme;
  < 300 KB per PNG. Numbered callouts come from widget geometry (`draw_callouts`). The scratch
  folder is deleted after the run (`--keep` keeps it).
- `tests/test_doc_screenshots.py` (no Qt) keeps pages, shot list, images and `@shot` functions
  in step. If tests live inside the package (pyIrena: `pyirena/tests/`), it still finds the repo
  root by `pyproject.toml`.
- pyIrena's copy predates the template (images only under `tools/`); it can switch over when
  convenient.

## Sections

`getting-started/`, `guides/`, `reference/` and `changelog.md` are expected in every package.
`tools/`, `methods/` and `developer/` are optional: **leave a section out (folder and toctree
entry) until it has a page.** Never build empty placeholder pages. When you add a section, use the
name from this template.

## One source for text that also lives elsewhere

Include it instead of copying it. For a part of `README.md`, mark it and include that part:

````markdown
<!-- docs-install-start -->
...install text...
<!-- docs-install-end -->
````

````markdown
```{include} ../../README.md
:start-after: <!-- docs-install-start -->
:end-before: <!-- docs-install-end -->
```
````

Whole files (`CHANGELOG.md`, a schema `.md` inside the package) are included without markers.

## Links from README.md and CHANGELOG.md into docs/

Both are included in the site or shown on PyPI, where a relative link to `docs/...` cannot work.
Links from them into the docs use absolute RTD URLs (`.../en/latest/...`).

## Keep the copies in sync

Everything outside the `PER-PACKAGE` block is meant to stay identical to this template, including
the `FAMILY` navbar and `requirements.txt` pins. When the template changes, diff each package's copy
against it.

A tool page starts from `docs/tools/_template.md` (excluded from the build).
