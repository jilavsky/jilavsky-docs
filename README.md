# jilavsky-docs

Home page of the documentation for Jan Ilavsky's small-angle scattering software, published at
**<https://jilavsky-docs.readthedocs.io>**.

This repo holds the **shared** pages only. Each package builds its own manual from its own repo as
a Read the Docs subproject:

| Package | Docs source | Published at |
|---|---|---|
| Family home page | this repo, `docs/` | `jilavsky-docs.readthedocs.io/en/stable/` |
| pyIrena | `jilavsky/pyirena`, `docs/` | `.../projects/pyirena/en/stable/` |
| Bernardyn | `jilavsky/bernardyn`, `docs/` | `.../projects/bernardyn/en/stable/` |
| AIDA | `jilavsky/aida`, `docs/` | `.../projects/aida/en/stable/` |
| Irena, Nika, Indra (Igor Pro) | `jilavsky/SAXS_IgorCodeDocs` | `saxs-igorcodedocs.readthedocs.io` (separate) |

`templates/package-docs/` is the starting point copied into each package. `PLAN.md` describes the
design, the decisions and the remaining steps.

## Build locally

```bash
conda env create -f environment.yml
conda activate jilavsky-docs
sphinx-build -W --keep-going -b html docs docs/_build/html
open docs/_build/html/index.html
```

or with a venv: `pip install -r docs/requirements.txt`, then the same `sphinx-build` command.
