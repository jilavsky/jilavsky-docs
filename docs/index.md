# SAS software by Jan Ilavsky

Software for small-angle and wide-angle X-ray scattering (SAXS, USAXS, WAXS, and SANS):
data reduction, analysis, figures, and AI-assisted work. The tools are developed at the Advanced
Photon Source (Argonne National Laboratory) and are used at many other facilities.

Each package has its own manual, with its own versions. This site links them together and holds
the material they share: installation, file formats, and workflows that use more than one package.

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} pyIrena
:link: https://jilavsky-docs.readthedocs.io/projects/pyirena/

Analysis of SAS data in Python: Unified Fit, size distributions, modeling, simple fits, WAXS
peak fitting, data merging. A port of Igor Pro Irena, with GUI, scripting and MCP interfaces.
:::

:::{grid-item-card} Bernardyn
:link: https://jilavsky-docs.readthedocs.io/projects/bernardyn/

Publication-quality plots of scattering and diffraction curves, including saved pyIrena
results. Graphs are saved as portable HDF5 packages.
:::

:::{grid-item-card} AIDA
:link: https://jilavsky-docs.readthedocs.io/projects/aida/

AI Data Assistant: a desktop workbench for using local or cloud language models with
pyIrena, Bernardyn and other scientific tools, in your own data folders.
:::

:::{grid-item-card} Irena, Nika, Indra (Igor Pro)
:link: https://saxs-igorcodedocs.readthedocs.io/en/stable/

The original Igor Pro packages: Irena (analysis), Nika (2D reduction) and Indra (USAXS
reduction).
:::

::::

Coming later: **Anisa** (anisotropic particle populations) and **pyNika** (2D data reduction in
Python). Until their manuals are here, see their GitHub pages:
[Anisa](https://github.com/jilavsky/anisa), [pyNika](https://github.com/jilavsky/pynika).

```{toctree}
:maxdepth: 1
:caption: Using the family

which-tool
installation
data-formats
workflows
```

```{toctree}
:maxdepth: 1
:caption: Coming from Igor Pro

igor-manuals
irena-pyirena-map
```

```{toctree}
:maxdepth: 1
:caption: About

citing
```
