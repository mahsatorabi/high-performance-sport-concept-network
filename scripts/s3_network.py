"""
ARTICLE 1 - Stage 3: concept-family co-occurrence network, centrality, community
structure, and NULL-MODEL VALIDATION.

Two departures from a conventional co-word analysis:

  1. Edges are admitted by STATISTICAL SIGNIFICANCE of the co-occurrence (Fisher exact
     test on the 2x2 document table, FDR-corrected), not by an arbitrary similarity cut.
  2. Every structural claim is tested against a DEGREE-PRESERVING NULL MODEL
     (configuration model). Observed modularity and node centrality are converted to
     z-scores against the null distribution, so "this field is modular" and "this
     concept is integrative" become falsifiable statements rather than eyeballed ones.

Layered centralities (L1 titles / L2 author keywords / L3 full text) additionally yield
the Concept Stratification diagnostic: which concepts are advertised in titles versus
which carry the field's structure invisibly.
"""
import os, json, csv, math, collections, itertools, random, sys
import numpy as np
import networkx as nx
from scipy import stats


BASE = r"D:\Uni of Birjand\articles\adel\article1"
DATA, TAB = os.path.join(BASE, "data"), os.path.join(BASE, "tables")
os.makedirs(TAB, exist_ok=True)
random.seed(7); np.random.seed(7)

MIN_NODE_DF = 8           # lower specificity cutoff: family must occur in >= 8 documents
NODE_SHARE_MAX = 0.30     # upper specificity cutoff: drop families in >30% of documents
MIN_COOC = 3              # minimum raw co-occurrence for an admissible edge
EDGE_Z = 2.5              # per-edge z-score against the bipartite null
NULL_DRAWS = 30           # bipartite swap draws for the edge null
CENT_NULL_DRAWS = 300     # configuration-model draws for the structural null

blob = json.load(open(os.path.join(DATA, "corpus.json"), encoding="utf-8"))
docs = blob["docs"]; N = len(docs)
lab = blob["fam_label"]; mem = blob["fam_members"]
f1m, f2m, f3m = blob["fams_L1"], blob["fams_L2"], blob["fams_L3"]

print("=" * 78)
print("STAGE 3  CO-OCCURRENCE NETWORK + NULL-MODEL VALIDATION")
print("=" * 78)
print("families: %d   documents: %d   MIN_NODE_DF=%d" % (len(lab), N, MIN_NODE_DF))


def matrix(present, nf):
    M = np.zeros((N, nf), dtype=np.float32)
    for d, row in enumerate(present):
        for f in row:
            M[d, f] = 1.0
    return M


df3 = M3 = None
df1 = np.array([sum(1 for r in f1m if f in r) for f in range(len(lab))], dtype=float)
df2 = np.array([sum(1 for r in f2m if f in r) for f in range(len(lab))], dtype=float)
df3 = np.array([sum(1 for r in f3m if f in r) for f in range(len(lab))], dtype=float)
M3 = matrix(f3m, len(lab))

nodes_all = [f for f in range(len(lab)) if df3[f] >= MIN_NODE_DF]
nodes_hi = [f for f in nodes_all if df3[f] / N > NODE_SHARE_MAX]
nodes = [f for f in nodes_all if f not in set(nodes_hi)]
print("specificity window: df >= %d and df/N <= %.2f" % (MIN_NODE_DF, NODE_SHARE_MAX))
print("   eligible families (df>=%d)          : %d" % (MIN_NODE_DF, len(nodes_all)))
print("   excluded as too ubiquitous (df/N>%.2f): %d  -> %s"
      % (NODE_SHARE_MAX, len(nodes_hi), ", ".join(lab[f] for f in sorted(
          nodes_hi, key=lambda f: -df3[f])[:14])))
print("   NODES RETAINED                     : %d" % len(nodes))

X = M3[:, nodes]
C = (X.T @ X).astype(float)                 # co-occurrence counts
k = df3[nodes]
both = C.copy()
np.fill_diagonal(both, 0)

# ---- edge null model: DEGREE-PRESERVING BIPARTITE RANDOMISATION --------------
# A p-value per edge wastes power and leaves most of the network isolated. Instead each
# edge is scored against a null that preserves BOTH document and concept degrees, so the
# null preserves the overall opportunity structure while destroying topical association.
# A double-edge swap between two documents preserves both marginals exactly.
print("\nEDGE NULL MODEL  (bipartite swap, %d draws, degrees preserved)" % NULL_DRAWS)
inv = [[] for _ in range(N)]
for d in range(N):
    for c in np.nonzero(X[d])[0]:
        inv[d].append(int(c))

rng = np.random.default_rng(11)
Snull = np.zeros((NULL_DRAWS, len(nodes), len(nodes)), dtype=np.float32)
for t in range(NULL_DRAWS):
    Mx = X.copy()
    cur = [list(inv[d]) for d in range(N)]
    for _ in range(40 * N):                      # 40 swap proposals per document
        a, b = rng.integers(0, N, 2)
        if a == b or not cur[a] or not cur[b]:
            continue
        ia = int(rng.integers(0, len(cur[a])))
        ca = cur[a][ia]
        if ca in cur[b]:
            continue
        cb = int(cur[b][int(rng.integers(0, len(cur[b])))])
        cur[a][ia] = cb
        cur[b][cur[b].index(cb)] = ca
    Mn = np.zeros_like(Mx)
    for d in range(N):
        for c in cur[d]:
            Mn[d, c] = 1.0
    Cn = (Mn.T @ Mn).astype(np.float32)
    np.fill_diagonal(Cn, 0)
    Sn = Cn / np.maximum(k[:, None] + k[None, :] - Cn, 1e-9)
    Snull[t] = Sn
    if (t + 1) % 10 == 0:
        print("   draw %d/%d" % (t + 1, NULL_DRAWS))

m_null = Snull.mean(0)
s_null = Snull.std(0) + 1e-9
AS = both / np.maximum(k[:, None] + k[None, :] - both, 1e-9)
np.fill_diagonal(AS, 0)
Z = (AS - m_null) / s_null

admissible = (both >= MIN_COOC)
print("   pairs with co-occurrence >= %d : %d" % (MIN_COOC, admissible.sum() // 2))
for zt in (4.0, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5):
    keep = admissible & (Z >= zt)
    np.fill_diagonal(keep, False)
    print("   z >= %-4.1f -> %5d edges" % (zt, keep.sum() // 2))
keep = admissible & (Z >= EDGE_Z)
np.fill_diagonal(keep, False)
SIG = keep
print("   SELECTED edge rule: co-occurrence >= %d AND null z >= %.1f -> %d edges"
      % (MIN_COOC, EDGE_Z, SIG.sum() // 2))

# association strength of the surviving edges, also expressed as a null z-score
qmat = np.zeros_like(both)
iu = np.triu_indices(len(nodes), 1)
ii, jj = iu
qmat[iu] = Z[iu]
qmat[jj, ii] = Z[iu]

G = nx.Graph()
for i, fi in enumerate(nodes):
    G.add_node(fi, label=lab[fi], df=float(k[i]), size=len(mem[fi]),
               members=" | ".join(mem[fi][:10]))
for i, j in zip(*np.nonzero(np.triu(SIG, 1))):
    u, v = nodes[i], nodes[j]
    G.add_edge(u, v, weight=float(AS[i, j]), cooc=float(both[i, j]), z=float(Z[i, j]))

G.remove_nodes_from([n for n in G if G.degree(n) == 0])
print("network: %d nodes, %d edges (mean degree %.2f, density %.4f)"
      % (G.number_of_nodes(), G.number_of_edges(),
         2 * G.number_of_edges() / max(G.number_of_nodes(), 1),
         nx.density(G)))
iso = [n for n in nodes if n not in G]
print("isolated families (df>=%d but no significant partner): %d" % (MIN_NODE_DF, len(iso)))

# ---- centrality ---------------------------------------------------------------
cen = {}
cen["degree"] = dict(G.degree())
cen["strength"] = {n: d for n, d in G.degree(weight="weight")}
cen["closeness"] = nx.closeness_centrality(G)
cen["betweenness"] = nx.betweenness_centrality(G, weight="weight", normalized=True)
cen["eigenvector"] = {n: 0.0 for n in G.nodes()}
# eigenvector centrality is undefined for disconnected graphs, so it is computed on each
# connected component separately and rescaled by component size (standard treatment).
for comp in nx.connected_components(G):
    H = G.subgraph(comp)
    if H.number_of_nodes() < 3:
        continue
    try:
        ev = nx.eigenvector_centrality_numpy(H, weight="weight", max_iter=3000, tol=1e-9)
    except Exception:
        ev = nx.eigenvector_centrality(H, weight="weight", max_iter=3000, tol=1e-9)
    f = H.number_of_nodes() / G.number_of_nodes()
    for n, v in ev.items():
        cen["eigenvector"][n] = v * f
cen["pagerank"] = nx.pagerank(G, weight="weight")
cen["clustering"] = nx.clustering(G)
cen["core_number"] = dict(nx.core_number(G))

# ---- community structure + resolution sweep ---------------------------------
def modularity_of(Gu, part):
    return nx.algorithms.community.quality.modularity(Gu, part, weight="weight")


res_sweep = []
best = (None, -1)
for r in np.arange(0.4, 4.01, 0.1):
    part = nx.community.louvain_communities(G, seed=7, weight="weight", resolution=r)
    q = modularity_of(G, part)
    res_sweep.append((round(float(r), 2), len(part), q))
    if q > best[1]:
        best = (r, q, part)
RES, Q, comms = best[0], best[1], best[2]
print("\nCOMMUNITY STRUCTURE (Louvain, resolution sweep 0.4-4.0)")
for r, k_, q_ in res_sweep:
    if abs(r - RES) < 0.11 or r in (0.4, 1.0, 2.0, 3.0, 4.0):
        print("   resolution %.1f -> %2d clusters, Q = %.3f%s" % (r, k_, q_, "  <== selected" if r == RES else ""))
comms = sorted(comms, key=len, reverse=True)
clab = {}
for ci, c in enumerate(comms):
    for n in c:
        clab[n] = ci
print("   selected resolution %.1f : %d clusters, modularity Q = %.3f" % (RES, len(comms), Q))
print("   cluster sizes: %s" % ", ".join(str(len(c)) for c in comms))

# ---- NULL MODEL: degree-preserving configuration model ------------------------
deg = [d for _, d in G.degree()]
print("\nNULL MODEL  (configuration model, degree sequence preserved, %d draws)" % CENT_NULL_DRAWS)
# Exact betweenness is affordable once, but not 500 times over; the null uses the
# standard pivot-sampling approximation with the same seed for every draw.
null_btw = collections.defaultdict(list)
null_mod = []
for t in range(CENT_NULL_DRAWS):
    Gn = nx.configuration_model(deg, seed=1000 + t)
    Gn = nx.Graph(Gn)
    Gn.remove_edges_from(nx.selfloop_edges(Gn))
    b = nx.betweenness_centrality(Gn, k=200, seed=1000 + t, weight="weight", normalized=True)
    for n, v in b.items():
        null_btw[n].append(v)
    # Closeness is not null-tested: an all-pairs distance distribution over 300 draws is
    # not affordable, and closeness is not a primary quantity here. Betweenness and
    # modularity are the two structural claims that are tested.
    part = nx.community.louvain_communities(Gn, seed=1000 + t, weight="weight")
    null_mod.append(modularity_of(Gn, part))
    if (t + 1) % 50 == 0:
        print("   draw %d/%d" % (t + 1, CENT_NULL_DRAWS)); sys.stdout.flush()
null_btw = {n: v for n, v in null_btw.items()}
mod_obs, mod_null = Q, float(np.mean(null_mod))
mod_sd = float(np.std(null_mod))
mod_z = (mod_obs - mod_null) / mod_sd if mod_sd > 0 else float("nan")
p_mod = float((np.sum(np.array(null_mod) >= mod_obs) + 1) / (CENT_NULL_DRAWS + 1))
print("   modularity    observed %.3f  null %.3f +/- %.3f   z = %+.2f   p(one-sided) = %.4f"
      % (mod_obs, mod_null, mod_sd, mod_z, p_mod))

rows = []
for n in G.nodes():
    bt = cen["betweenness"][n]
    bnull = np.array(null_btw.get(n, [0.0]))
    rows.append(dict(
        family_id=n, label=G.nodes[n]["label"], df=G.nodes[n]["df"],
        family_size=G.nodes[n]["size"], cluster=clab[n],
        members=G.nodes[n]["members"],
        degree=cen["degree"][n], strength=round(cen["strength"][n], 4),
        betweenness=bt,
        betweenness_null_mean=round(float(bnull.mean()), 6),
        betweenness_z=(round(float((bt - bnull.mean()) / bnull.std()), 3)
                       if bnull.std() > 0 else 0.0),
        closeness=cen["closeness"][n],
        eigenvector=cen["eigenvector"][n], pagerank=cen["pagerank"][n],
        clustering=cen["clustering"][n], core_number=cen["core_number"][n],
        df_L1=int(df1[n]), df_L2=int(df2[n]), df_L3=int(df3[n]),
    ))

zb = np.array([r["betweenness_z"] for r in rows])
print("   betweenness   observed max %.5f   null mean %.5f"
      % (max(r["betweenness"] for r in rows),
         float(np.mean([np.mean(null_btw.get(n, [0.0])) for n in G.nodes()]))))
print("   nodes with betweenness z > 1.96 : %d   z > 2.58 : %d   z > 3.29 : %d"
      % ((zb > 1.96).sum(), (zb > 2.58).sum(), (zb > 3.29).sum()))

# ---- Layer stratification ----------------------------------------------------
print("\nCONCEPT STRATIFICATION  (provenance of each family across evidence layers)")


def cent_layer(present):
    """Betweenness on the same node set but a different evidence layer."""
    M = matrix(present, len(lab))
    sub = [f for f in range(len(lab))
           if MIN_NODE_DF <= df3[f] and df3[f] / N <= NODE_SHARE_MAX]
    Xs = M[:, sub]
    degs = Xs.sum(0)
    Ws = (Xs.T @ Xs).astype(float)
    np.fill_diagonal(Ws, 0.0)
    Ws = Ws / np.maximum(np.sqrt(np.outer(degs, degs)), 1e-9)
    Gs = nx.from_numpy_array(Ws)
    Gs = nx.relabel_nodes(Gs, dict(enumerate(sub)))
    b = nx.betweenness_centrality(Gs, weight="weight", normalized=True)
    return {sub[i]: v for i, v in enumerate(b.values())}


bt1 = cent_layer(f1m); bt2 = cent_layer(f2m); bt3 = cent_layer(f3m)
common = [n for n in G.nodes() if n in bt1 and n in bt2]
r13 = stats.spearmanr([bt1[n] for n in common], [bt3[n] for n in common])
r12 = stats.spearmanr([bt1[n] for n in common], [bt2[n] for n in common])
r23 = stats.spearmanr([bt2[n] for n in common], [bt3[n] for n in common])
print("   layer concordance (Spearman of betweenness rank, n=%d)" % len(common))
print("      L1 title   vs L3 full    rho = %.3f  (p = %.2e)" % (r13.statistic, r13.pvalue))
print("      L1 title   vs L2 keywords rho = %.3f  (p = %.2e)" % (r12.statistic, r12.pvalue))
print("      L2 keywords vs L3 full   rho = %.3f  (p = %.2e)" % (r23.statistic, r23.pvalue))

pr_median = float(np.median([r_["df_L1"] / max(r_["df_L3"], 1) for r_ in rows]))
for r_ in rows:
    r_["provenance_ratio"] = round(r_["df_L1"] / max(r_["df_L3"], 1), 4)
    r_["keyword_ratio"] = round(r_["df_L2"] / max(r_["df_L3"], 1), 4)
    r_["betweenness_L1"] = round(bt1.get(r_["family_id"], 0.0), 6)
    r_["betweenness_L2"] = round(bt2.get(r_["family_id"], 0.0), 6)
    r_["betweenness_L3"] = round(bt3.get(r_["family_id"], 0.0), 6)
print("   median provenance ratio (df_L1 / df_L3) = %.3f" % pr_median)

rows.sort(key=lambda r: -r["betweenness"])
with open(os.path.join(TAB, "T3_network_centrality.csv"), "w", encoding="utf-8-sig",
          newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open(os.path.join(TAB, "T3_resolution_sweep.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["resolution", "n_clusters", "modularity_Q"])
    w.writerows(res_sweep)

print("\nTOP 30 BY BETWEENNESS (bridging concepts, ranked by observed betweenness)")
print("   z = null-model significance test; low-df nodes have small null variance so")
print("   their z is inflated - read z as 'unusual for this degree', btw as the effect size")
for r_ in rows[:30]:
    print("  z=%+6.2f  btw=%.4f  df=%3d  C%-2d  %-26s  %s"
          % (r_["betweenness_z"], r_["betweenness"], r_["df"], r_["cluster"],
             r_["label"][:26], r_["members"][:56]))

sig_bridge = [r_ for r_ in rows if r_["betweenness_z"] > 2.58]
print("\nBRIDGE CONCEPTS (betweenness z > 2.58): %d of %d nodes (%.1f%%)"
      % (len(sig_bridge), len(rows), 100 * len(sig_bridge) / len(rows)))
for r_ in sorted(sig_bridge, key=lambda r_: -r_["betweenness"])[:22]:
    print("  z=%+6.2f  btw=%.4f  df=%3d  C%-2d  %-28s  %s"
          % (r_["betweenness_z"], r_["betweenness"], r_["df"], r_["cluster"],
             r_["label"][:28], r_["members"][:44]))

print("\nTOP 12 BY PROXIMITY / EIGENVECTOR (intellectual core)")
for r_ in sorted(rows, key=lambda x: -x["eigenvector"])[:12]:
    print("  eig=%.4f  str=%.2f  df=%3d  C%d  %-26s" %
          (r_["eigenvector"], r_["strength"], r_["df"], r_["cluster"], r_["label"][:26]))

print("\nCLUSTER PROFILES")
for ci, c in enumerate(comms):
    ids = sorted(c, key=lambda n: -df3[n])
    top = [lab[n] for n in ids[:9]]
    print("  C%d  n=%-3d df_sum=%-5d  %s" % (ci, len(c), int(df3[ids].sum()), ", ".join(top)))

blob["net"] = dict(min_node_df=MIN_NODE_DF, n_nodes=G.number_of_nodes(),
                   n_edges=G.number_of_edges(), density=nx.density(G),
                   resolution=RES, modularity=Q, mod_null=mod_null, mod_sd=mod_sd,
                   mod_z=mod_z, p_mod=p_mod, null_draws=CENT_NULL_DRAWS,
                   rho_L1_L3=r13.statistic, rho_L1_L2=r12.statistic, rho_L2_L3=r23.statistic,
                   pr_median=pr_median, nodes=[int(x) for x in G.nodes()],
                   n_isolated=len(iso))
json.dump(blob, open(os.path.join(DATA, "corpus.json"), "w", encoding="utf-8"),
          ensure_ascii=False, default=float)

# edge list for figures
with open(os.path.join(DATA, "network_edges.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["source", "target", "weight", "cooc", "z"])
    for u, v, d in G.edges(data=True):
        w.writerow([lab[u], lab[v], round(d["weight"], 5), int(d["cooc"]), "%.3e" % d["z"]])
print("\nWrote T3_network_centrality.csv, T3_resolution_sweep.csv, network_edges.csv")


