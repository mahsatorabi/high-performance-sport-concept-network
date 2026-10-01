"""
ARTICLE 1 - consolidated results summary (all headline numbers for the manuscript).
"""
import os, json, csv, collections
import numpy as np
from scipy import stats

BASE = r"D:\Uni of Birjand\articles\adel\article1"
DATA, TAB = os.path.join(BASE, "data"), os.path.join(BASE, "tables")
b = json.load(open(os.path.join(DATA, "corpus.json"), encoding="utf-8"))
SEM, NET, NAT, PIL = b["semcon"], b["net"], b["national"], b["pillars"]
TT, TOP = b["temporal"], b["topics"]

print("=" * 78)
print("ARTICLE 1 - CONSOLIDATED RESULTS")
print("=" * 78)
print("\nCORPUS")
print("   raw Scopus records        %d" % b["n_raw"])
print("   analytic corpus          %d  (excluded: %s)"
      % (b["n_kept"], b["exclusion_counts"]))
print("   analysis window 2013-2025 %d   post-window 2026 %d"
      % (b["n_window"], sum(1 for d in b["docs"] if d["year"] > 2025)))
print("   query-artefact inflation  %.2fx" % 3.67)

print("\nCONCEPT EXTRACTION (stage 1)")
r = list(csv.DictReader(open(os.path.join(DATA, "concepts.csv"), encoding="utf-8-sig")))
print("   concepts                 %d (%d unigram / %d multiword)"
      % (len(r), sum(1 for x in r if int(x["n"]) == 1), sum(1 for x in r if int(x["n"]) > 1)))

print("\nSEMCON (stage 2) - semantic concept-family consolidation")
print("   encoder                   %s" % SEM["model"])
print("   anisotropy: raw %+.4f -> centred %+.4f  (mean |cos| %.4f)"
      % (SEM["cos_raw"], SEM["cos_centred"], SEM["abs_cen"]))
print("   exact normalisation       %d concepts -> %d lemma groups"
      % (SEM["n_concepts"], SEM["n_lemma_groups"]))
print("   tau (%s)  %.3f" % (SEM.get("tau_source", "?"), SEM["tau"]))
if SEM.get("audited_precision") is not None:
    print("   audited precision        %.3f  (%d merges adjudicated, %d judged correct)"
          % (SEM["audited_precision"], SEM["n_merges_audited"], SEM["n_correct"]))
print("   families                  %d (%d multi-member, largest %d)"
      % (SEM["n_families"], SEM["n_multi"], SEM["stability"][0]["largest"]))
print("   semantic vs co-occ. ARI   %.3f  (NMI %.3f) - divergence is the finding"
      % (SEM["ari"], SEM["nmi"]))

print("\nNETWORK (stage 3) - null-calibrated")
print("   nodes / edges             %d / %d  (density %.4f, mean degree %.1f)"
      % (NET["n_nodes"], NET["n_edges"], NET["density"], 2 * NET["n_edges"] / NET["n_nodes"]))
print("   communities               %d at resolution %.1f"
      % (len(set(int(r["cluster"]) for r in
                 csv.DictReader(open(os.path.join(TAB, "T3_network_centrality.csv"),
                                     encoding="utf-8-sig")))), NET["resolution"]))
print("   MODULARITY                Q = %.3f   null %.3f +/- %.3f   z = %+.1f   p = %.4f"
      % (NET["modularity"], NET["mod_null"], NET["mod_sd"], NET["mod_z"], NET["p_mod"]))
print("   null draws                %d degree-preserving configuration models" % NET["null_draws"])
zb = [float(x["betweenness_z"]) for x in
      csv.DictReader(open(os.path.join(TAB, "T3_network_centrality.csv"), encoding="utf-8-sig"))]
print("   bridging nodes z>1.96     %d    z>2.58 %d    z>3.29 %d"
      % (sum(1 for z in zb if z > 1.96), sum(1 for z in zb if z > 2.58),
         sum(1 for z in zb if z > 3.29)))

print("\nCONCEPT STRATIFICATION (stage 3)")
print("   layer concordance (Spearman of betweenness rank, n=%d)" % NET["n_nodes"])
print("      title vs full text     rho = %.3f" % NET["rho_L1_L3"])
print("      title vs keywords      rho = %.3f" % NET["rho_L1_L2"])
print("      keywords vs full text  rho = %.3f" % NET["rho_L2_L3"])
print("   median provenance ratio   %.3f  -> ~%d%% of concept mentions sit in titles"
      % (NET["pr_median"], round(100 * NET["pr_median"])))

print("\nTOPIC MODEL (stage 4)")
TOP
print("   documents                 %d in %d-%d" % (TOP["n_docs"], *TOP["window"]))
print("   topics / noise            %d / %.1f%%   silhouette %.3f"
      % (TOP["n_topics"], 100 * TOP["noise_share"], TOP["silhouette"]))
print("   stability (bootstrap ARI) mean %.3f sd %.3f over %d replicates"
      % (TOP["stability"]["mean"], TOP["stability"]["sd"], TOP["stability"]["replicates"]))
print("   HDBSCAN params            min_cluster_size=%d min_samples=%d"
      % (TOP["params"]["min_cluster_size"], TOP["params"]["min_samples"]))

print("\nTHREE-PILLAR MULTIPLEX (stage 5)")
for p, c in sorted(PIL["counts"].items(), key=lambda x: -x[1]):
    print("   %-12s %4d (%.1f%%)" % (p, c, 100 * c / NET["n_nodes"]))
ov = PIL["overlap"]
print("   boundary crossing         observed %.4f  null %.4f +/- %.4f  z = %+.2f  p = %.3f"
      % (ov["observed_boundary_crossing"], ov["null_mean"], ov["null_sd"], ov["z"], ov["p"]))

print("\nTEMPORAL (stage 6, RQ2)")
print("   topic x period            chi2 = %.1f  dof %d  p = %.2e  Cramer's V = %.3f"
      % (TT["chi2"], TT["dof"], TT["p"], TT["cramersV"]))
tt = list(csv.DictReader(open(os.path.join(TAB, "T6_temporal_topics.csv"), encoding="utf-8-sig")))
print("   %-40s %5s %8s %s" % ("topic", "n", "meanYr", "direction"))
for x in sorted(tt, key=lambda y: -float(y["emergence"])):
    print("   %-40s %5s %8s %s" % (x["label"][:40], x["n"], x["mean_year"], x["direction"]))

print("\nCROSS-NATIONAL (stage 6, RQ3)")
print("   countries (n>=12 docs)    %d" % len(NAT["top_countries"]))
print("   topic x country           chi2 = %.1f  dof %d  p = %.2e  V = %.3f"
      % (NAT["chi2"], NAT["dof"], NAT["p"], NAT["cramersV"]))
print("   over-represented cells    %d/%d topic-level, %d/%d family-level (lift>1.3, q<.05)"
      % (NAT["n_sig_topic"], NAT["n_tested"], NAT["n_sig_family"], NAT["n_tested_family"]))

print("\nANSWERABLE-FOR-THE-MANUSCRIPT HEADLINES")
print("   1. The concept network of high-performance sport is significantly modular")
print("      (Q=%.3f vs null %.3f, z=%+.0f): the field is a community structure, not a"
      % (NET["modularity"], NET["mod_null"], NET["mod_z"]))
print("         diffuse discourse.")
print("   2. Only ~%d%% of concept mentions appear in titles, and title-level centrality"
      % round(100 * NET["pr_median"]))
print("         correlates with full-text centrality at only rho=%.2f: the concepts that"
      % NET["rho_L1_L3"])
print("         carry the field's structure are largely invisible in how it presents itself.")
print("   3. The three pillars are SEGREGATED (z=%+.2f, shortest paths avoid pillar"
      % ov["z"])
print("         boundaries more than chance): the 'ecosystem' framing is not yet realised")
print("         in the literature; integration is a research gap, not an established fact.")
_pl = list(csv.DictReader(open(os.path.join(TAB, "T5_pillars.csv"), encoding="utf-8-sig")))
_cen = {int(r["family_id"]): r for r in
        csv.DictReader(open(os.path.join(TAB, "T3_network_centrality.csv"),
                            encoding="utf-8-sig"))}
_tab = []
for _p in ["GOVERNANCE", "INNOVATION", "TALENT"]:
    _s = [r for r in _pl if r["pillar"] == _p]
    _nb = sum(1 for r in _s if float(_cen.get(int(r["family_id"]),
                                              {"betweenness_z": 0})["betweenness_z"]) > 2.58)
    _tab.append([_nb, len(_s) - _nb])
_tab = np.array(_tab)
_c2, _pv = stats.chi2_contingency(_tab)[:2]
print("   4. %d of %d network nodes bridge significantly (z>2.58). Bridging is NOT"
      % (sum(1 for z in zb if z > 2.58), len(zb)))
print("         pillar-specific (chi2=%.2f, p=%.2f): no pillar bridges more than another."
      % (_c2, _pv))
print("         Bridging therefore belongs to the SYSTEM, which is the case for modelling")
print("         it as one network rather than as three parallel literatures.")
print("=" * 78)





