import ewe, pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_columns',30)

from stanza import split
AREA = 350.0   # km2 of marine water within ~15 km of Echo Bay (Salmon Coast Field Station)
# DFO spawn index within 15 km of Echo Bay, mean 1969-1976 = 583 t; the index is a minimum
# (spawners only, survey q <= 1), so adult herring in the area are taken as 2x that.
B_HERRING = 2 * 583 / AREA
JUV = split(B_HERRING, 6.3, 0.48, [(0, 1.5), (24, 0.7)])[0]
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
G("Herring juvenile", biomass_area=JUV[0], pb=1.5, qb=JUV[1], vbk=0.48)  # the SDK has no stanza calculation, so done in stanza.py
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
               wmat_winf=0.35, rec_power=1, leading_stage=2)

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
D("Herring adult", {"Euphausiids": 0.3, "Small zooplankton": 0.3})   # 40% eaten offshore in summer
doc.set_group("Herring adult", diet_import=0.4)
D("Herring juvenile", {"Euphausiids": 0.25, "Small zooplankton": 0.65, "Phytoplankton": 0.1})
D("Other forage fish", {"Euphausiids": 0.4, "Small zooplankton": 0.6})
D("Demersal fishes", {"Benthic invertebrates": 0.6, "Euphausiids": 0.2, "Other forage fish": 0.05,
                      "Herring juvenile": 0.01, "Small zooplankton": 0.14})
D("Jellyfish", {"Small zooplankton": 0.845, "Euphausiids": 0.1, "Herring juvenile": 0.005, "Phytoplankton": 0.05})
D("Euphausiids", {"Phytoplankton": 0.7, "Small zooplankton": 0.2, "Detritus": 0.1})
D("Small zooplankton", {"Phytoplankton": 0.8, "Detritus": 0.2})
D("Benthic invertebrates", {"Phytoplankton": 0.38, "Kelp and eelgrass": 0.02, "Detritus": 0.6})

doc.add_fleet("Roe herring")
doc.add_fleet("Salmon")
doc.add_fleet("Groundfish hook and line")
# Predator removals that held seals and humpbacks down before the 1970s (seal culls and bounties,
# coastal whaling). Kept as fleets so an Ecosim run can switch them off and let predators recover.
doc.add_fleet("Seal control")
doc.add_fleet("Whaling")
doc.set_catch("Seal control", "Seals and sea lions", landings=0.036)
doc.set_catch("Whaling", "Humpback whales", landings=0.0012)
doc.set_catch("Roe herring", "Herring adult", landings=0.35)
doc.set_catch("Salmon", "Adult salmon", landings=0.3)
doc.set_catch("Groundfish hook and line", "Lingcod and rockfish", landings=0.05)
doc.set_catch("Groundfish hook and line", "Spiny dogfish", landings=0.1)
doc.add_ecosim_scenario("1975-2025", years=50)

v = doc.validate(); print(v)
doc.to_json("broughton.json")
with doc.open() as m:
    p = m.ecopath()
    print("balanced:", p.balanced, p.unbalanced_groups)
    print(p.diagnostics.round(3))

out = doc.save("broughton_herring_1975.eiixml"); print("saved", out)
