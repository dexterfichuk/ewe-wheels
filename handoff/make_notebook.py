"""Write broughton_herring_colab.ipynb: build the Broughton herring 1975 EwE model from code in Colab."""
import csv, json, sys
from pathlib import Path

HERE = Path(__file__).parent
rows = list(csv.DictReader(open(HERE / "broughton_spawn_index.csv")))
spawn = ", ".join(f"{r['year']}: {r['spawn_index_t']}" for r in rows)

cells = []
md = lambda s: cells.append(("markdown", s.strip("\n")))
code = lambda s: cells.append(("code", s.strip("\n")))

md("""
# Broughton Archipelago herring, 1975: an Ecopath with Ecosim model in Colab

Pacific herring used to spawn every spring around Echo Bay in the Broughton Archipelago (BC), near the
Salmon Coast Field Station. The DFO spawn index within 15 km of the station averaged about 580 t from 1969 to 1976,
then fell to almost nothing after 1980 and has stayed there apart from a one-off spawn in 1992.

This notebook builds a small food-web model of the area as it was in 1975, entirely from Python with the `ewe` package,
then asks Ecosim a few "what if" questions about the herring decline:

1. Install `ewe` (the engine, .NET and the model library are bundled)
2. Look at the spawn index record
3. Build the model: 19 groups, a two-stanza herring group, diets, five fleets
4. Balance it with Ecopath and look at the food web
5. Run Ecosim scenarios: heavier roe fishing, predator recovery (the end of seal culls and whaling), both
6. Save the model as `.eiixml` and as an Access `.ewemdb` that opens in the EwE desktop app

It is a teaching model, not an assessment: herring biomass comes from the spawn index and every other group is
adapted from the Strait of Georgia model. Each step takes a few seconds.
""")
md("""
## 1. Install

`WHEEL_URL` points at the Linux x86-64 wheel (about 70 MB); the `[plot]` extra adds matplotlib. On your own machine,
install the wheel for your platform instead and skip this cell. If the URL is empty, the cell asks you to upload the `.whl`.
""")
code("""
WHEEL_URL = "https://github.com/dexterfichuk/ewe-wheels/releases/download/v0.1.1/ewe-0.1.1-py3-none-manylinux_2_28_x86_64.whl"

import importlib.util, os, subprocess, sys

if importlib.util.find_spec("ewe") is None:
    if WHEEL_URL:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", f"ewe[plot] @ {WHEEL_URL}"], check=True)
    else:
        from google.colab import files  # upload the .whl from your computer
        wheel = next(iter(files.upload()))
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", f"ewe[plot] @ file://{os.path.abspath(wheel)}"], check=True)
""")
code("""
import ewe
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option("display.precision", 3)
print("ewe", ewe.__version__)
""")
md("""
## 2. The spawn index

Total spawn index (t) of DFO herring spawn surveys within 15 km of Echo Bay (50.751 N, 126.497 W), summed by year
(surface + Macrocystis + understory spawn). The index counts spawners only and assumes survey catchability <= 1, so it is a minimum.
""")
code(f"""
spawn = pd.Series({{{spawn}}}, name="spawn index (t)")
spawn.index.name = "year"

ax = spawn.plot.bar(figsize=(11, 3), width=0.8, color="#3b6fb6")
ax.set_xticks(range(0, len(spawn), 5), spawn.index[::5])
ax.set_ylabel("spawn index (t)")
ax.set_title("Herring spawn within 15 km of Echo Bay")
plt.show()

print("mean 1969-1976:", round(spawn.loc[1969:1976].mean()), "t")
""")
md("""
## 3. Build the model

Area: about 350 km² of water within 15 km of the station. Adult herring biomass is taken as twice the 1969-1976 spawn
index (a minimum, so doubled) divided by the area. Groups with `ee=` instead of a biomass get their biomass from
mass balance.

Herring has two life stages (juveniles 0-2 years, adults 2+). Only the adult biomass and Q/B are entered;
`calculate_stanzas()` (run once the diets are in, since it loads the model) runs EwE's multi-stanza calculation to fill in the juvenile biomass and Q/B from the stage
mortalities and the von Bertalanffy K, as the desktop app does.
""")
code("""
AREA = 350.0                    # km²
B_HERRING = 2 * 583 / AREA      # t/km²

doc = ewe.new_model("Broughton herring 1975", area=AREA, first_year=1975,
                    unit_currency=5, unit_time=1, country="Canada",
                    ecosystem_type="Fjord / archipelago",
                    min_lon=-126.75, max_lon=-126.25, min_lat=50.6, max_lat=50.9,
                    description="Broughton Archipelago around Salmon Coast Field Station, when herring still spawned there. "
                                "Herring biomass from the DFO spawn index within 15 km (mean 1969-1976 = 583 t). "
                                "Other groups adapted from the Strait of Georgia model.")
G = doc.add_group
G("Transient orcas", biomass_area=0.002, pb=0.02, qb=7.4)
G("Humpback whales", biomass_area=0.02, pb=0.08, qb=9.0)
G("Seals and sea lions", biomass_area=0.3, pb=0.2, qb=8.1)
G("Seabirds", biomass_area=0.02, pb=0.3, qb=80)
G("Lingcod and rockfish", biomass_area=3.0, pb=0.4, qb=1.5)
G("Spiny dogfish", biomass_area=4.0, pb=0.1, qb=2.5)
G("Adult salmon", biomass_area=0.4, pb=1.3, qb=4.5)
G("Juvenile salmon", biomass_area=0.5, pb=3.0, qb=15)
G("Herring adult", biomass_area=B_HERRING, pb=0.7, qb=6.3, vbk=0.48)
G("Herring juvenile", pb=1.5, vbk=0.48)          # B and Q/B from calculate_stanzas() after the diets
G("Other forage fish", pb=2.0, qb=18, ee=0.95)
G("Demersal fishes", biomass_area=10, pb=0.5, qb=2.5)
G("Jellyfish", biomass_area=10, pb=3.0, qb=12)
G("Euphausiids", pb=12, qb=40, ee=0.95)
G("Small zooplankton", pb=25, qb=183, ee=0.95)
G("Benthic invertebrates", biomass_area=300, pb=2.0, qb=12)
G("Kelp and eelgrass", "producer", biomass_area=50, pb=4.4)
G("Phytoplankton", "producer", pb=200, ee=0.6)
G("Detritus", "detritus", biomass_area=1)

doc.add_stanza("Pacific herring", [("Herring juvenile", 0, 1.5), ("Herring adult", 24, 0.7)],
               wmat_winf=0.35, rec_power=1, leading_stage=2);
""")
md("""
Diets (fraction of each predator's consumption). Adult herring feed offshore for part of the year, so 40% of their
diet is an import from outside the area.
""")
code("""
D = doc.set_diet
D("Transient orcas", {"Seals and sea lions": 1.0})
D("Humpback whales", {"Herring adult": 0.3, "Herring juvenile": 0.1, "Other forage fish": 0.1, "Euphausiids": 0.5})
D("Seals and sea lions", {"Herring adult": 0.2, "Herring juvenile": 0.05, "Adult salmon": 0.05, "Juvenile salmon": 0.05,
                          "Other forage fish": 0.2, "Demersal fishes": 0.35, "Lingcod and rockfish": 0.05, "Benthic invertebrates": 0.05})
D("Seabirds", {"Herring adult": 0.05, "Herring juvenile": 0.15, "Other forage fish": 0.3, "Juvenile salmon": 0.05,
               "Benthic invertebrates": 0.3, "Euphausiids": 0.1, "Demersal fishes": 0.05})
D("Lingcod and rockfish", {"Herring adult": 0.08, "Herring juvenile": 0.1, "Other forage fish": 0.1, "Demersal fishes": 0.42,
                           "Benthic invertebrates": 0.25, "Juvenile salmon": 0.05})
D("Spiny dogfish", {"Herring adult": 0.04, "Herring juvenile": 0.05, "Other forage fish": 0.05, "Demersal fishes": 0.15,
                    "Juvenile salmon": 0.05, "Euphausiids": 0.46, "Benthic invertebrates": 0.1, "Jellyfish": 0.1})
D("Adult salmon", {"Herring adult": 0.2, "Herring juvenile": 0.2, "Other forage fish": 0.4, "Euphausiids": 0.2})
D("Juvenile salmon", {"Euphausiids": 0.3, "Small zooplankton": 0.6, "Jellyfish": 0.1})
D("Herring adult", {"Euphausiids": 0.3, "Small zooplankton": 0.3})
doc.set_group("Herring adult", diet_import=0.4)
D("Herring juvenile", {"Euphausiids": 0.25, "Small zooplankton": 0.65, "Phytoplankton": 0.1})
D("Other forage fish", {"Euphausiids": 0.4, "Small zooplankton": 0.6})
D("Demersal fishes", {"Benthic invertebrates": 0.6, "Euphausiids": 0.2, "Other forage fish": 0.05,
                      "Herring juvenile": 0.01, "Small zooplankton": 0.14})
D("Jellyfish", {"Small zooplankton": 0.845, "Euphausiids": 0.1, "Herring juvenile": 0.005, "Phytoplankton": 0.05})
D("Euphausiids", {"Phytoplankton": 0.7, "Small zooplankton": 0.2, "Detritus": 0.1})
D("Small zooplankton", {"Phytoplankton": 0.8, "Detritus": 0.2})
D("Benthic invertebrates", {"Phytoplankton": 0.38, "Kelp and eelgrass": 0.02, "Detritus": 0.6})

doc.calculate_stanzas()   # juvenile herring B and Q/B from the adult stage
""")
md("""
Fleets and 1975 landings (t/km²/year). Seal control (culls and bounties) and coastal whaling had held seals and
humpbacks down before the 1970s; they are kept as fleets so Ecosim can switch them off and let the predators recover.
""")
code("""
for fleet in ["Roe herring", "Salmon", "Groundfish hook and line", "Seal control", "Whaling"]:
    doc.add_fleet(fleet)
doc.set_catch("Roe herring", "Herring adult", landings=0.35)
doc.set_catch("Salmon", "Adult salmon", landings=0.3)
doc.set_catch("Groundfish hook and line", "Lingcod and rockfish", landings=0.05)
doc.set_catch("Groundfish hook and line", "Spiny dogfish", landings=0.1)
doc.set_catch("Seal control", "Seals and sea lions", landings=0.036)
doc.set_catch("Whaling", "Humpback whales", landings=0.0012)

doc.add_ecosim_scenario("1975-2025", years=50)
print(doc.validate())
doc.groups.set_index("name").loc[["Herring adult", "Herring juvenile"], ["biomass_area", "pb", "qb", "vbk"]]
""")
md("""
## 4. Ecopath: mass balance

`doc.open()` loads the document in the engine. A model is balanced when every group's ecotrophic efficiency (EE)
is at most 1, that is, no group loses more to predators and fishing than it produces.
""")
code("""
m = doc.open()
path = m.ecopath()
print("balanced:", path.balanced, "| unbalanced groups:", path.unbalanced_groups)
path.diagnostics[["biomass", "pb", "qb", "ee", "tl", "f", "m2"]]
""")
code("""
path.plot();   # biomass against trophic level
""")
code("""
m.plot.foodweb();   # trophic level up, node size = biomass, links = consumption
""")
md("""
## 5. Ecosim: what could have driven the decline?

Each run starts from the 1975 balance and goes 50 years with constant fleet effort (1 = the 1975 effort) unless
changed. `vulnerability_multiplier=2` doubles every predator-prey vulnerability, i.e. stronger top-down control.
""")
code("""
H = ["Herring adult", "Herring juvenile", "Seals and sea lions", "Humpback whales", "Adult salmon"]
P0 = {"Seal control": 0, "Whaling": 0}   # predator removals stop
runs = {
    "baseline (1975 effort)": m.ecosim(),
    "roe herring effort x4": m.ecosim(effort={"Roe herring": 4}),
    "predators recover": m.ecosim(effort=P0),
    "predators recover, vulnerability x2": m.ecosim(effort=P0, vulnerability_multiplier=2),
    "  ... and roe effort x2": m.ecosim(effort={**P0, "Roe herring": 2}, vulnerability_multiplier=2),
    "  ... and roe fishery closed": m.ecosim(effort={**P0, "Roe herring": 0}, vulnerability_multiplier=2),
}
end = pd.DataFrame({k: r.biomass.iloc[-1] / r.biomass.iloc[0] for k, r in runs.items()}).T[H]
end.round(2)   # biomass after 50 years relative to 1975
""")
code("""
base, *_ = runs.values()
base.plot.compare({k: v for k, v in list(runs.items())[1:4]}, label="baseline", groups=H[:4]);
""")
md("""
Model against the record: the Ecosim adult herring biomass of each run (relative to 1975) next to the spawn
index relative to its 1969-1976 mean.
""")
code("""
fig, ax = plt.subplots(figsize=(10, 4))
obs = spawn.loc[1969:] / spawn.loc[1969:1976].mean()
ax.bar(obs.index, obs.values, color="#c9c9c9", label="spawn index / 1969-76 mean")
for k, r in runs.items():
    b = r.biomass["Herring adult"]
    y = (b / b.iloc[0]).groupby(b.index.astype(int)).mean()
    ax.plot(y.index, y.values, label=k.strip(" ."))
ax.set_ylabel("relative to 1975")
ax.set_title("Adult herring: Ecosim runs vs the spawn index")
ax.legend(fontsize=8, ncol=2)
plt.show()
""")
md("""
None of these runs reproduces a near-total loss after 1980 on its own: the model says local spawning collapse needs
more than the predator and fishing changes here (spawning moving elsewhere, a recruitment failure, or much higher
mortality than these parameters allow). Predator recovery hits adult salmon far harder than herring: with
seals at 3-7 times their 1975 biomass, adult salmon disappear from the area in the vulnerability x2 runs. Try your own: change `effort`, `vulnerability_multiplier`, or edit the
document with `doc.set_group(...)` and reopen it.

## 6. Save

`.eiixml` is EwE's XML format; `.ewemdb` is the Access database the EwE 6 desktop app opens.
""")
code("""
saved = m.save("broughton_herring_1975.eiixml")
access = m.save("broughton_herring_1975.ewemdb")
doc.to_json("broughton_herring_1975.json")   # the editable ewe-model document
for p in (saved, access):
    print(p, p.stat().st_size // 1024, "kB")
m.close()

try:
    from google.colab import files
    # files.download(str(access))   # uncomment to download
except ImportError:
    pass
""")

nb = {"cells": [], "metadata": {"colab": {"name": "broughton_herring_colab.ipynb", "provenance": []},
      "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
      "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 0}
for kind, src in cells:
    c = {"cell_type": kind, "metadata": {}, "source": src.splitlines(keepends=True)}
    if kind == "code":
        c.update(execution_count=None, outputs=[])
    nb["cells"].append(c)
out = HERE / "broughton_herring_colab.ipynb"
out.write_text(json.dumps(nb, indent=1) + "\n")
print("wrote", out)
