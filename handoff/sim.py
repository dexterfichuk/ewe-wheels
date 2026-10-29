import ewe, pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_columns',30)
m = ewe.open("broughton_herring_1975.eiixml")
m.ecopath()
H = ["Herring adult", "Herring juvenile"]
def run(label, **kw):
    s = m.ecosim(**kw)
    r = s.relative_biomass
    y = r.groupby(r.index.astype(int)).mean()
    print(f"{label:38s}", " ".join(f"{g.split()[1][:3]}={y[g].iloc[-1]:.2f}" for g in H),
          f"seals={y['Seals and sea lions'].iloc[-1]:.2f} salmonA={y['Adult salmon'].iloc[-1]:.2f}")
    return y
res = {}
P0 = {"Seal control": 0, "Whaling": 0}
res["baseline"] = run("baseline (1975 effort)")
res["roe x4"] = run("roe herring effort x4", effort={"Roe herring": 4})
res["predators recover"] = run("seal control + whaling stop", effort=P0)
res["recover v x2"] = run("  ... vulnerabilities x2", effort=P0, vulnerability_multiplier=2)
res["recover v x2 roe x2"] = run("  ... and roe effort x2", effort={**P0, "Roe herring": 2}, vulnerability_multiplier=2)
res["recover v x2 roe 0"] = run("  ... and roe closed", effort={**P0, "Roe herring": 0}, vulnerability_multiplier=2)
pd.concat({k: v["Herring adult"] for k, v in res.items()}, axis=1).to_csv("ecosim_herring_adult.csv")
m.close()
