# Workflows across packages

## From reduced data to a figure

1. **Reduce** the measurement: Nika (2D) or Indra (USAXS) in Igor Pro, or the beamline's own
   reduction. The result is an NXcanSAS HDF5 file.
2. **Analyze** it in **pyIrena**: for example, a Unified Fit or a size distribution. The results
   are saved into the same HDF5 file.
3. **Plot** the data, the fit and the size distribution in **Bernardyn**, and export PNG/SVG for the
   paper. Save the graph as a `*.bernardyn.h5` package so it can be edited later.

## The same chain, with AIDA

AIDA can run steps 2 and 3 for you: it calls pyIrena and Bernardyn through their MCP servers on
the files in your workspace, and shows the plots they return. You check the result and decide.

% TODO(Jan): add a worked example with bundled test data once the package manuals have one.
