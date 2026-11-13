# CLAUDE.md — jilavsky-docs

Parent Read the Docs project for the documentation family (pyIrena, Bernardyn, AIDA; later Anisa,
pyNika). Design and decisions: `PLAN.md`. Read it before changing structure.

## Map

- `docs/`: the family home page (shared material only). Built by RTD from `.readthedocs.yaml`.
- `templates/package-docs/`: the layout copied into every package repo. A change here must be
  carried over to each package's copy. Instructions are in its `README.md`.
- `planning/`: superseded drafts, kept for history.

## Rules

- Content specific to one package belongs in that package's repo, not here.
- The build runs with `-W`; keep it warning-free:
  `sphinx-build -W --keep-going -b html docs docs/_build/html`.
- Pins in `docs/requirements.txt` and `templates/package-docs/docs/requirements.txt` stay identical.
- The `FAMILY` navbar block is identical in `docs/conf.py` and the template's `conf.py`.
- Never bind the name `version` at module level in a `conf.py` (Sphinx reads it as a setting).
- Add a project to `intersphinx_mapping` only after its RTD site is live.
- Help-button page names (`tools/*.md` in packages) and the Igor manual URLs are frozen contracts.
- Matilda is deliberately not part of this site.
