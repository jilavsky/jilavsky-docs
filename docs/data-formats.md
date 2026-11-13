# Shared data formats

The family exchanges data as **NXcanSAS HDF5** files. Units: Q in Å⁻¹, intensity in cm⁻¹ where
the data are absolutely calibrated.

## Where the data are in a file

| What | HDF5 path |
|---|---|
| Name of the default sample | attribute `entry/@default` |
| Q | `entry/<sample>/sasdata/Q` |
| Intensity | `entry/<sample>/sasdata/I` |
| Uncertainty | `entry/<sample>/sasdata/Idev` (may be missing) |
| Slit-smeared USAXS data | `entry/<sample>_SMR/sasdata/...` |

`entry/@default` points to the desmeared data when both variants are present.

```python
import h5py

with h5py.File("file.h5", "r") as f:
    sample = f["entry"].attrs["default"]
    sd = f[f"entry/{sample}/sasdata"]
    Q = sd["Q"][:]
    I = sd["I"][:]
    dI = sd["Idev"][:] if "Idev" in sd else None
```

## Results written by each package

| Package | What it writes | Details |
|---|---|---|
| pyIrena | `entry/<tool>_results` groups next to the data, plus the panel setup as JSON | pyIrena manual, *HDF5 layout* reference page |
| Bernardyn | Its own graph packages, `*.bernardyn.h5` (data, styles, previews) | Bernardyn manual, *Data flow and formats* |
| AIDA | Does not write SAS data; it calls the tools above | |

Each package documents its own groups in full. This page lists only what you need to move data
between packages.

% TODO: replace the "Details" text with links once the subprojects are live.
