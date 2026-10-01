"""
ARTICLE 1 - Stage 6: TEMPORAL and CROSS-NATIONAL analysis.

RQ2  How has the thematic composition of the field evolved, and what is the frontier?
RQ3  Which national systems and communities dominate, and does the intellectual centre of
     gravity differ between national contexts?

Statistical approach: all topic x period and topic x country tests are chi-square on the
full contingency table (not a per-cell test, which would inflate error rates), p-values are
Benjamini-Hochberg FDR-corrected across the whole family of tests, and effect sizes
(Cramér's V) are reported alongside p-values because with small expected counts a
significant chi-square can be a trivial effect.
"""
import os, json, csv, math, collections
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
import networkx as nx

BASE = r"D:\Uni of Birjand\articles\adel\article1"
DATA, TAB = os.path.join(BASE, "data"), os.path.join(BASE, "tables")
W0, W1 = 2013, 2025
PERIODS = [(2013, 2016), (2017, 2019), (2020, 2021), (2022, 2025)]
MIN_CELL = 5
MIN_COUNTRY = 12

blob = json.load(open(os.path.join(DATA, "corpus.json"), encoding="utf-8"))
docs = blob["docs"]; lab = blob["fam_label"]
topics_meta = blob["topics"]
assign = {int(k): v for k, v in topics_meta["assignment"].items()}
sel = sorted(assign)
T = np.array([assign[i] for i in sel])
YR = np.array([docs[i]["year"] for i in sel])
COUNTRY = [docs[i]["lead_country"] for i in sel]
tlabels = {p["topic"]: p["label"] for p in topics_meta["profiles"]}
tl = lambda t: ("NOISE" if t == -1 else tlabels.get(t, str(t)))
ntop = max(tlabels) + 1
print("=" * 78)
print("STAGE 6  TEMPORAL AND CROSS-NATIONAL ANALYSIS")
print("=" * 78)
print("documents %d-%d: %d   topics %d (+noise %.1f%%)"
      % (W0, W1, len(sel), ntop, 100 * (T == -1).mean()))

# ---------------------------------------------------------------- RQ2 temporal
print("\nRQ2  TEMPORAL STRUCTURE")
print("   period distribution: %s" % ", ".join(
    "%d-%d n=%d" % (a, b, int(((YR >= a) & (YR <= b)).sum())) for a, b in PERIODS))

def topic_period_table():
    rows = []
    for t in range(-1, ntop):
        r = [int(((T == t) & (YR >= a) & (YR <= b)).sum()) for a, b in PERIODS]
        rows.append((t, r))
    return rows

tpt = topic_period_table()
print("\n   %-6s %-38s %s" % ("topic", "label", "  ".join("%d-%d" % p for p in PERIODS)))
for t, r in tpt:
    print("   %-6s %-38s %s" % (tl(t)[:38], tl(t)[:38], "  ".join("%4d" % x for x in r)))

# chi-square on the full topic x period table
cnt = np.array([[int(((T == t) & (YR >= a) & (YR <= b)).sum()) for a, b in PERIODS]
                for t in range(-1, ntop)], dtype=float)
keep = (cnt.sum(1) >= MIN_CELL)
chi2, p_chi, dof, exp = stats.chi2_contingency(cnt[keep])
n = cnt[keep].sum()
V = math.sqrt(chi2 / (n * (min(cnt.shape) - 1)))
print("\n   TOPIC x PERIOD chi-square: chi2=%.1f  dof=%d  p=%.3e  Cramer's V=%.3f"
      % (chi2, dof, p_chi, V))
# expected counts warn us where the test is untrustworthy
print("   cells with expected count < 5: %d of %d" % (int((exp < 5).sum()), exp.size))

# per-topic temporal trend: mean publication year, and early-vs-late share
print("\n   %-38s %6s %8s %8s %9s" % ("topic", "n", "meanYr", "lateSh", "trend"))
tem = []
for t in range(-1, ntop):
    m = T == t
    if m.sum() < MIN_CELL:
        continue
    yy = YR[m]
    late = float((yy >= 2021).mean())
    early = float((yy <= 2019).mean())
    # emergence score: late share normalised against the corpus baseline
    base_late = float((YR >= 2021).mean())
    emerge = late - base_late
    decr = early - float((YR <= 2019).mean())
    tem.append(dict(topic=int(t), label=tl(t), n=int(m.sum()),
                    mean_year=round(float(yy.mean()), 2), share_late=round(late, 4),
                    emergence=round(emerge, 4), decline=round(decr, 4),
                    direction=("EMERGING" if emerge > 0.08 else
                               "DECLINING" if decr > 0.08 else "STABLE")))
for r in sorted(tem, key=lambda x: -x["emergence"]):
    print("   %-38s %6d %8.1f %8.2f %9s %s"
          % (r["label"][:38], r["n"], r["mean_year"], r["share_late"],
             "%+.3f" % r["emergence"], r["direction"]))
print("   corpus baseline: share >=2021 = %.3f ; share <=2019 = %.3f"
      % (float((YR >= 2021).mean()), float((YR <= 2019).mean())))

# concept-level emergence: mean publication year of each family
fdf3 = None
with open(os.path.join(DATA, "families.csv"), encoding="utf-8-sig") as f:
    fams = list(csv.DictReader(f))
fam_of = {int(k): v for k, v in blob["fam_of_concept"].items()}
docs_fams = blob["fams_L3"]
# document -> families, restricted to the analysis window
rows_y = collections.defaultdict(list)
for i in sel:
    for fx in blob["fams_L3"][docs[i]["doc_id"]]:
        rows_y[fx].append(docs[i]["year"])

rank_by_year = []
for fx, ys in rows_y.items():
    if len(ys) < MIN_CELL:
        continue
    rank_by_year.append((fx, float(np.mean(ys)), len(ys), float(np.mean(np.array(ys) >= 2021))))
rank_by_year.sort(key=lambda x: x[1])
print("\n   CONCEPT EMERGENCE (frontier = highest mean publication year)")
print("   %-34s %8s %6s %8s" % ("family", "meanYr", "n", "lateSh"))
for fx, my, n_, ls in rank_by_year[-15:][::-1]:
    print("   %-34s %8.1f %6d %8.2f" % (lab[fx][:34], my, n_, ls))
print("   --- most established (lowest mean year) ---")
for fx, my, n_, ls in rank_by_year[:8]:
    print("   %-34s %8.1f %6d %8.2f" % (lab[fx][:34], my, n_, ls))

# ---------------------------------------------------------------- RQ3 national
print("\nRQ3  CROSS-NATIONAL STRUCTURE")
ccount = collections.Counter(c for c in COUNTRY if c)
top_c = [c for c, n_ in ccount.most_common() if n_ >= MIN_COUNTRY]
print("   countries with >= %d documents: %d of %d" % (MIN_COUNTRY, len(top_c), len(ccount)))
print("   %-26s %6s %8s" % ("country", "n", "meanYr"))
for c in top_c:
    yy = [YR[i] for i in range(len(sel)) if COUNTRY[i] == c]
    print("   %-26s %6d %8.1f" % (c, len(yy), float(np.mean(yy))))

print("\n   TOPIC x COUNTRY chi-square")
cc = np.array([[int(((T == t) & np.array([COUNTRY[i] == c for i in range(len(sel))])).sum())
                for c in top_c] for t in range(-1, ntop)], dtype=float)
# Drop any country column that itself has too little support, so the two masks align.
col_ok = cc.sum(0) >= MIN_CELL
if not col_ok.all():
    cc = cc[:, col_ok]
    top_c = [c for c, ok in zip(top_c, col_ok) if ok]
    print("   (dropped %d country columns with fewer than %d documents)"
          % ((~col_ok).sum(), MIN_CELL))
row_ok = cc.sum(1) >= MIN_CELL
col_ok2 = cc.sum(0) >= 1
sub = cc[np.ix_(row_ok, col_ok2)]
chi2c, pc, dofc, expc = stats.chi2_contingency(sub)
nc = sub.sum()
Vc = math.sqrt(chi2c / (nc * (min(cc.shape) - 1)))
print("   chi2=%.1f dof=%d p=%.3e Cramer's V=%.3f  (cells exp<5: %d/%d)"
      % (chi2c, dofc, pc, Vc, int((expc < 5).sum()), expc.size))

# per-country topic profile with FDR
prow = []
for c in top_c:
    m = np.array([COUNTRY[i] == c for i in range(len(sel))])
    n_c = int(m.sum())
    for t in range(-1, ntop):
        k = int(((T == t) & m).sum())
        if k == 0:
            continue
        rest = int(((T == t) & ~m).sum())
        # two-proportion z test of this country's topic share vs the rest of the corpus
        p1, p2 = k / n_c, rest / (len(sel) - n_c)
        p0 = (p1 + p2) / 2
        se = math.sqrt(max(p0 * (1 - p0) * (1 / n_c + 1 / (len(sel) - n_c)), 1e-12))
        z = (p1 - p2) / se
        pv = 2 * (1 - stats.norm.cdf(abs(z)))
        prow.append(dict(country=c, n_country=n_c, topic=int(t), label=tl(t), k=k,
                         share=round(p1, 4), rest_share=round(p2, 4),
                         lift=round(p1 / p2, 3) if p2 > 0 else 0.0,
                         z=round(z, 2), p=pv))
if prow:
    _, qv, _, _ = multipletests([r["p"] for r in prow], method="fdr_bh")
    for r, q in zip(prow, qv):
        r["q"] = float(q)
        r["significant"] = int(q < 0.05)
print("   %-22s %-30s %6s %7s %7s %6s %s" % ("country", "topic", "k/n", "share", "rest", "lift", "q"))
sig = [r for r in prow if r["significant"] and r["lift"] > 1.3]
sig.sort(key=lambda r: (-r["lift"], -r["k"]))
seen = set()
shown = 0
for r in sig:
    key = (r["country"], r["topic"])
    if key in seen:
        continue
    seen.add(key)
    if shown >= 30:
        break
    print("   %-22s %-30s %3d/%-3d %7.3f %7.3f %6.2f %.3f"
          % (r["country"][:22], r["label"][:30], r["k"], r["n_country"], r["share"],
             r["rest_share"], r["lift"], r["q"]))
    shown += 1
print("   over-represented country-topic cells (lift>1.3, q<0.05): %d of %d tested"
      % (len([r for r in prow if r["significant"] and r["lift"] > 1.3]), len(prow)))

# ---------------------------------------------------------------- concept-position
# Does the CONCEPTUAL emphasis of a country differ, or only the topic mix?
# Demonymic and pure-geographic families ("canada", "norwegian", "russia", ...) are
# over-represented trivially because the country label is derived FROM them. Reporting
# them as national research emphases would be circular, so they are excluded here and the
# exclusion is stated rather than left implicit.
DEMONYMS = {"canada", "canadian", "australia", "australian", "russia", "russian",
            "germany", "german", "china", "chinese", "uk", "british", "norway", "norwegian",
            "spain", "spanish", "switzerland", "swiss", "usa", "america", "american",
            "canadians", "australians", "germans", "chinese", "england", "english",
            "europe", "european", "western", "eastern", "asia", "african", "france",
            "french", "italy", "italian", "brazil", "brazilian", "korea", "korean",
            "poland", "polish", "india", "indian", "japan", "japanese", "finland",
            "finnish", "denmark", "danish", "sweden", "swedish", "portugal", "portuguese",
            "belgium", "belgian", "netherlands", "dutch", "hungary", "hungarian",
            "austria", "austrian", "ukraine", "ukrainian", "israel", "israeli",
            "canadian sport", "australian sport", "german sport", "chinese sport"}

print("\n   CONCEPT EMPHASIS BY COUNTRY (top over-represented families, q<0.05)")
print("   [excludes %d demonymic/geographic families that are circular for this test]"
      % len(DEMONYMS))
frow = []
for c in top_c:
    m = np.array([COUNTRY[i] == c for i in range(len(sel))])
    n_c = int(m.sum())
    for fx, ys in rows_y.items():
        tot = len(ys)
        if tot < MIN_CELL:
            continue
        # rebuild the per-document membership for this family inside the window
        pass
# vectorised version using the document x family matrix
d_fam = {}
for pos, i in enumerate(sel):
    d_fam[i] = set(blob["fams_L3"][docs[i]["doc_id"]])
fids = [fx for fx, ys in rows_y.items() if len(ys) >= MIN_CELL]
M = np.zeros((len(sel), len(fids)))
for pos, i in enumerate(sel):
    s = d_fam[i]
    for j, fx in enumerate(fids):
        if fx in s:
            M[pos, j] = 1.0
for c in top_c:
    m = np.array([COUNTRY[i] == c for i in range(len(sel))])
    n_c = int(m.sum())
    for j, fx in enumerate(fids):
        k = int((M[m, j]).sum())
        if k < 3:
            continue
        rest = int((M[~m, j]).sum())
        p1, p2 = k / n_c, rest / (len(sel) - n_c)
        p0 = (p1 + p2) / 2
        se = math.sqrt(max(p0 * (1 - p0) * (1 / n_c + 1 / (len(sel) - n_c)), 1e-12))
        z = (p1 - p2) / se
        pv = 2 * (1 - stats.norm.cdf(abs(z)))
        frow.append(dict(country=c, n_country=n_c, family=lab[fx], k=k,
                         share=round(p1, 4), rest_share=round(p2, 4),
                         lift=round(p1 / p2, 3) if p2 > 0 else 0.0, z=round(z, 2), p=pv))
if frow:
    _, qv, _, _ = multipletests([r["p"] for r in frow], method="fdr_bh")
    for r, q in zip(frow, qv):
        r["q"] = float(q)
        r["significant"] = int(q < 0.05)
    n_circ = sum(1 for r in frow if r["family"] in DEMONYMS)
    sigf = [r for r in frow
            if r["significant"] and r["lift"] > 1.3 and r["family"] not in DEMONYMS]
    sigf.sort(key=lambda r: (-r["lift"], -r["k"]))
    print("   over-represented country-family cells (lift>1.3, q<0.05): %d of %d tested"
          % (len(sigf), len(frow) - n_circ))
    print("   (%d circular cells removed: country name/demonym families)" % n_circ)
    for r in sigf[:24]:
        print("   %-22s %-28s %3d/%-3d share=%.3f rest=%.3f lift=%5.2f q=%.3f"
              % (r["country"][:22], r["family"][:28], r["k"], r["n_country"], r["share"],
                 r["rest_share"], r["lift"], r["q"]))

# ---------------------------------------------------------------- export
with open(os.path.join(TAB, "T6_temporal_topics.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(tem[0].keys())); w.writeheader(); w.writerows(tem)
with open(os.path.join(TAB, "T6_country_topic.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(prow[0].keys())); w.writeheader(); w.writerows(prow)
if frow:
    with open(os.path.join(TAB, "T6_country_family.csv"), "w", encoding="utf-8-sig",
              newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(frow[0].keys())); w.writeheader(); w.writerows(frow)
with open(os.path.join(TAB, "T6_concept_emergence.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["family", "mean_year", "n", "share_since_2021"])
    w.writerows([[lab[fx], round(my, 3), n_, round(ls, 4)] for fx, my, n_, ls in rank_by_year])

blob["temporal"] = dict(periods=PERIODS, chi2=float(chi2), dof=int(dof), p=float(p_chi),
                        cramersV=float(V), n_cells_exp_lt5=int((exp < 5).sum()), n_cells=int(exp.size))
blob["national"] = dict(top_countries=top_c, n_countries=len(top_c), chi2=float(chi2c),
                        dof=int(dofc), p=float(pc), cramersV=float(Vc),
                        n_sig_topic=int(len([r for r in prow if r["significant"] and r["lift"] > 1.3])),
                        n_tested=len(prow),
                        n_sig_family=len([r for r in frow if r["significant"] and r["lift"] > 1.3]) if frow else 0,
                        n_tested_family=len(frow))
json.dump(blob, open(os.path.join(DATA, "corpus.json"), "w", encoding="utf-8"),
          ensure_ascii=False, default=float)
print("\nWrote T6_temporal_topics.csv, T6_country_topic.csv, T6_country_family.csv, T6_concept_emergence.csv")
