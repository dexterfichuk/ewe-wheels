# ewe: Ecopath with Ecosim for Python and R

Prebuilt packages of `ewe`, which runs [Ecopath with Ecosim](https://ecopath.org) models from Python
and R on macOS, Linux and Windows. Each wheel bundles the EwE engine, the Access converter, the .NET
runtime and a model library, so nothing else needs installing.

**Documentation: https://dexterfichuk.github.io/ewe-wheels/**

```bash
pip install https://github.com/dexterfichuk/ewe-wheels/releases/download/v0.1.0/ewe-0.1.0-py3-none-manylinux_2_28_x86_64.whl
```

```python
import ewe
m = ewe.library.load("anchovy-bay")
m.ecopath().diagnostics
m.ecosim().biomass
m.save("anchovy_bay.ewemdb")     # opens in EwE on Windows
```

Wheels for Linux (x86-64, arm64), macOS (Apple silicon, Intel) and Windows (x64), the R package and
R engine bundles are on the [v0.1.0 release](https://github.com/dexterfichuk/ewe-wheels/releases/tag/v0.1.0);
see [Install](https://dexterfichuk.github.io/ewe-wheels/install/). Try it in Google Colab:
[examples/ewe_colab_quickstart.ipynb](https://colab.research.google.com/github/dexterfichuk/ewe-wheels/blob/main/examples/ewe_colab_quickstart.ipynb).

Prototype: the API can change before 1.0.

EwE is licensed under the EUPL-1.2. Source: https://github.com/Official-EwE/Eii.Ecopath
