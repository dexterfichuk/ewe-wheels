# ewe wheels

Prebuilt wheels of `ewe`, the Python SDK for Ecopath with Ecosim (prototype). Each wheel bundles the
EwE engine, the .NET runtime and the model library, so nothing else needs installing.

```bash
pip install https://github.com/dexterfichuk/ewe-wheels/releases/download/v0.1.0/ewe-0.1.0-py3-none-manylinux_2_28_x86_64.whl
```

Wheels for Linux (x86-64, arm64), macOS (arm64, x86-64) and Windows (x64) are on the
[v0.1.0 release](https://github.com/dexterfichuk/ewe-wheels/releases/tag/v0.1.0).

```python
import ewe, ewe.library
m = ewe.library.load("anchovy-bay")
m.ecopath().diagnostics
m.ecosim().biomass
```

EwE is licensed under the EUPL-1.2. Source: https://github.com/Official-EwE/Eii.Ecopath
