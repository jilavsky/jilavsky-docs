# Which tool do I need?

| I want to ... | Use | Notes |
|---|---|---|
| Fit or model reduced 1D SAS data (I vs Q) | **pyIrena** | Unified Fit, size distributions, modeling, simple fits, fractals, WAXS peaks |
| Do the same in Igor Pro | **Irena** | See {doc}`irena-pyirena-map` for the matching pyIrena tool |
| Reduce 2D detector images | **Nika** (Igor Pro) | pyNika will be documented here later |
| Reduce USAXS data | **Indra** (Igor Pro) | |
| Make figures for a paper or talk | **Bernardyn** | Reads NXcanSAS data and saved pyIrena results |
| Model anisotropic particle populations from several 1D cuts | **Anisa** | Beta; see its [GitHub page](https://github.com/jilavsky/anisa) |
| Ask an AI model to run these tools on my data | **AIDA** | Uses the pyIrena and Bernardyn MCP servers |

All the Python packages read and write the same NXcanSAS HDF5 files (see {doc}`data-formats`), so
a result saved by one can be opened by the next. A typical chain is described in {doc}`workflows`.
