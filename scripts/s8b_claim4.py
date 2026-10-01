"""Verify headline claim 4 (bridge concentration by pillar) before it goes in the paper."""
import os, csv, collections
import numpy as np
from scipy import stats

BASE = r"D:\Uni of Birjand\articles\adel\article1"
TAB = os.path.join(BASE, "tables")
pl = list(csv.DictReader(open(os.path.join(TAB, "T5_pillars.csv"), encoding="utf-8-sig")))

print("CLAIM-4 CHECK: are significantly-bridging concepts concentrated in governance?")
print("\n%-12s %6s %10s %10s %9s" % ("pillar", "n", "n_bridge", "%bridge", "mean df"))
tot_n = tot_b = 0
for p in ["GOVERNANCE", "INNOVATION", "TALENT", "UNASSIGNED"]:
    s = [r for r in pl if r["pillar"] == p]
    b = [r for r in s if float(r["betweenness_z"] if "betweenness_z" in r else 0) > 2.58]
    print("%-12s %6d %10d %9.1f%% %9.1f"
          % (p, len(s), len(b), 100 * len(b) / max(len(s), 1),
             np.mean([float(r["df"]) for r in s])))
    tot_n += len(s); tot_b += len(b)

# T5 does not carry betweenness_z, so recompute the test from the stage-3 table joined on id
cent = {int(r["family_id"]): r for r in
        csv.DictReader(open(os.path.join(TAB, "T3_network_centrality.csv"),
                            encoding="utf-8-sig"))}
print("\n(with betweenness z from stage 3, joined by family_id)")
print("%-12s %6s %10s %10s %9s %9s" % ("pillar", "n", "n_bridge", "%bridge", "mean df", "med df"))
tabs = {}
for p in ["GOVERNANCE", "INNOVATION", "TALENT", "UNASSIGNED"]:
    s = [r for r in pl if r["pillar"] == p]
    nb = 0
    dfs_b, dfs_all = [], []
    for r in s:
        c = cent.get(int(r["family_id"]))
        z = float(c["betweenness_z"]) if c else 0.0
        dfs_all.append(float(r["df"]))
        if z > 2.58:
            nb += 1
            dfs_b.append(float(r["df"]))
    print("%-12s %6d %10d %9.1f%% %9.1f %9.1f"
          % (p, len(s), nb, 100 * nb / max(len(s), 1), np.mean(dfs_all),
             np.median(dfs_b) if dfs_b else float("nan")))
    tabs[p] = (len(s), nb)

# 3x2 chi-square: pillar x is-bridge
tab = np.array([[tabs[p][1], tabs[p][0] - tabs[p][1]] for p in
                ["GOVERNANCE", "INNOVATION", "TALENT"]])
chi2, pv, dof, exp = stats.chi2_contingency(tab)
n = tab.sum()
V = (chi2 / (n * 1)) ** 0.5
print("\nPILLAR x BRIDGE chi-square (3 pillars, df=2)")
print("   table (bridge, non-bridge): %s" % tab.tolist())
print("   chi2 = %.2f  p = %.4f  Cramer's V = %.3f" % (chi2, pv, V))

# and the df confound: bridging nodes are low-df, so compare within df band
print("\nCONTROL for degree (the honest version of the claim):")
print("   %-12s %5s %5s %8s" % ("pillar", "n", "brg", "%bridge"))
for lo, hi in [(8, 15), (16, 40), (41, 999)]:
    print("   df %d-%d" % (lo, hi))
    for p in ["GOVERNANCE", "INNOVATION", "TALENT"]:
        s = [r for r in pl if r["pillar"] == p and lo <= float(r["df"]) <= hi]
        nb = sum(1 for r in s
                 if float(cent.get(int(r["family_id"]), {"betweenness_z": 0})["betweenness_z"]) > 2.58)
        print("   %-12s %5d %5d %7.1f%%" % (p, len(s), nb, 100 * nb / max(len(s), 1)))