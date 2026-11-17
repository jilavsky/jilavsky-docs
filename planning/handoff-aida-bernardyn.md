# Brief: move AIDA's or Bernardyn's docs onto Read the Docs (phase 3)

*For an agent working in `/Users/ilavsky/GitHub/Aida` or `/Users/ilavsky/GitHub/Bernardyn`.
Written 2026-11-13 after pyIrena was done. One session per repo; the two can run at the same
time.*

## Read first, in this order

1. `/Users/ilavsky/GitHub/jilavsky-docs/planning/handoff-pyirena.md`: the full step list. Follow
   it, with the differences below. Its section "Reusing this brief" applies.
2. `/Users/ilavsky/GitHub/jilavsky-docs/planning/status-after-pyirena.md`: decisions already made
   and the lessons from pyIrena (especially "Notes for reusing the brief").
3. `/Users/ilavsky/GitHub/jilavsky-docs/PLAN.md` §3 and your package's section: §4.2 (AIDA) or
   §4.3 (Bernardyn).
4. `/Users/ilavsky/GitHub/jilavsky-docs/templates/package-docs/README.md` and the template files.
   The template now also has `.github/workflows/docs.yml` and `.github/dependabot.yml`: copy them.
5. The repo's own `AGENTS.md` / `CLAUDE.md`.

## Differences from the pyIrena brief

- **One Help button, to the home page.** `HELP_TARGETS = {"home": ""}`, no `HELP_ANCHORS`.
- **No transition stubs** unless you find a released link to a specific `docs/*.md` file
  (grep first; AIDA links the `docs/` folder, Bernardyn a docs folder or GitHub).
- **Decisions already made apply as-is:** stubs and CHANGELOG links use `latest`; NumPy-style
  docstrings are on in the template; dev installs of `main` opening `stable` is accepted.
- **CHANGELOG links into `docs/`**: absolute RTD `latest` URLs (template README, "CHANGELOG links").
- Same commit structure as pyIrena: one commit with renames only (`git mv`), then the rest.

### AIDA

- `src/` layout: `SRC_DIR = "../src"`, helper at `src/aida/_docs.py`, tests in `tests/`.
- `DIST = "aida-workbench"`, `SUBPROJECT = "aida"`, `project = "AIDA"`, `GITHUB_REPO = "aida"`.
- Replace `DOCUMENTATION_URL` (GitHub tree) in `src/aida/ui/qt/main_window.py` with `docs_url()`;
  the tooltip that shows the URL must show the new one.
- `docs/figures/` with `make_figures.py` moves together; the script must still write to where the
  pages read from.
- `docs/talk-intro-slide.md` and `docs/README.md` leave `docs/`. Put the slide in `planning/` or
  wherever AIDA keeps talk material; don't delete it.
- AIDA is built with hatchling: check the wheel/sdist config so `docs/` stays out of the wheel.

### Bernardyn

- **Branch from `main`.** The local checkout is on `fix/issue-1-code-review` (one commit not on
  `main`). Switch to `main` before creating `docs-rtd`, and leave that branch untouched.
- `DIST = SUBPROJECT = GITHUB_REPO = "bernardyn"`, `project = "Bernardyn"`.
- `_documentation_url()` in `bernardyn/gui/main_window.py` opens the local `docs/` folder for an
  editable checkout. **Replace it with `docs_url()` always** (decided: the built site is more
  readable than raw `.md` files, and one code path is simpler). Keep the warning dialog for when
  the browser cannot be opened.
- Include `bernardyn/schemas/graph-package-v3.md` in `reference/` with `{include}`; do not copy it.
- `docs/TODO.md` and `docs/README.md` leave `docs/` (TODO to the repo root or `planning/`).

## When done

Commit on `docs-rtd`, do not push. Append a short section for your package to
`/Users/ilavsky/GitHub/jilavsky-docs/planning/status-after-pyirena.md` (judgment calls, gaps,
anything the template should change). If the template needs a change, describe it there rather
than editing it, so pyIrena's copy can be updated in the same pass.
