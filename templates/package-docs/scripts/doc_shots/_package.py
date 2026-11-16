"""Per-package part of the documentation screenshot machinery.

Copied from jilavsky-docs/templates/package-docs; **this is the only file in
scripts/doc_shots/ that differs between packages** (like the PER-PACKAGE
block of docs/conf.py). The example values are pyIrena's.

``isolate_settings`` runs before anything imports Qt or the package, and
again before every shot, so each shot starts from the coded defaults and
nothing is written to the user's real settings.
"""

from __future__ import annotations

import os
from pathlib import Path

from ._common import REPO

#: Default folder for Context.dataset(): tracked input files for the shots.
DATA_ROOT: Path = REPO / "validationData"

#: Callout circles: an orange that reads on white and on plots.
CALLOUT_FILL = "#c2410c"
CALLOUT_RADIUS = 12


def isolate_settings(scratch: Path) -> None:
    """Point every settings/state location of the package into *scratch*.

    pyIrena: ``PYIRENA_STATE_DIR``. AIDA: its config/data directories.
    Bernardyn: its QSettings / workspace location. Find them in the package's
    config code; a shot must never read or write the developer's real ones.
    """
    os.environ["PYIRENA_STATE_DIR"] = str(scratch / "state")


def make_app():
    """Create the offscreen QApplication with the package's light theme."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.pop("PYIRENA_NATIVE_THEME", None)
    from pyirena.gui import window_state

    window_state.GEOMETRY_PERSISTENCE_ENABLED = False
    from pyirena.gui._qt import QApplication
    from pyirena.gui.theme import apply_theme

    app = QApplication.instance() or QApplication(["make_doc_screenshots"])
    apply_theme(app)
    return app
