# Installing the family

The Python packages are designed to work in **one shared Python environment**. Their Qt (PySide6)
version limits are chosen so that installing one never forces a Qt change that breaks another.

You need **Python 3.11, 3.12 or 3.13** to install all of them (3.12 is recommended). pyIrena,
Bernardyn and Anisa also run on 3.10; AIDA needs 3.11 or newer. Python 3.14 is not supported yet.

## With conda

```bash
conda create -n sas python=3.12
conda activate sas
pip install "pyirena[gui]" bernardyn "aida-workbench[gui]"
```

## With venv

```bash
python3.12 -m venv sas-env
source sas-env/bin/activate        # Windows: sas-env\Scripts\activate
pip install "pyirena[gui]" bernardyn "aida-workbench[gui]"
```

On macOS with zsh, keep the quotes around names with square brackets.

## Starting the programs

| Package | Command |
|---|---|
| pyIrena | `pyirena-gui` |
| Bernardyn | `bernardyn` |
| AIDA | `aida-gui` |

Each package's manual has a full installation page, including optional extras (MCP servers,
development installs) and platform notes.
