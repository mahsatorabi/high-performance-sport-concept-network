"""
ARTICLE 1 - Stage 7: figures.
All figures are publication-resolution (300 dpi) PNG plus the underlying data as CSV.
"""
import os, json, csv, math, collections
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import networkx as nx
from matplotlib.colors import LinearSegmentedColormap

BASE = r"D:\Uni of Birjand\articles\adel\article1"
DATA, TAB, FIG = (os.path.join(BASE, x) for x in ("data", "tables", "figures"))
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 300, "font.family": "DejaVu Sans",
    "font.size": 8.5, "axes.linewidth": 0.7, "axes.titlesize": 9.5,
    "axes.titleweight": "bold", "axes.labelsize": 8.5, "legend.fontsize": 7.5,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "axes.grid": False,
})

blob = json.load(open(os.path.join(DATA, "corpus.json"), encoding="utf-8"))
docs = blob["docs"]; lab = blob["fam_label"]; mem = blob["fam_members"]
W0, W1 = 2013, 2025
CLUSTER_COLOR = ["#1f4e79", "#c0504d", "#4f8a3d", "#8064a2", "#e8a33d", "#2f8f8f",
                 "#a24b4b", "#7a7a7a", "#b07aa1", "#4b6cb7", "#c9a227"]
print("=" * 78)
print("STAGE 7  FIGURES")
print("=" * 78)


def save(fig, name):
    p = os.path.join(FIG, name)
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("   %-42s %s" % (name, os.path.getsize(p) // 1024, ))


# ================================================================ F1  pipeline
fig, ax = plt.subplots(figsize=(7.2, 2.5))
ax.axis("off")
stages = [
    ("Corpus\n623 Scopus", "#e8eef4"),
    ("Hygiene\n604 docs", "#dce6f0"),
    ("Concepts\n1,224 POS-aware", "#c9d9e8"),
    ("SEMCON\n1,034 families", "#b3c9dd"),
    ("Co-occ. network\n669 nodes / 5,101 edges", "#9dbad1"),
    ("Multiplex\n3 pillars", "#7fa3c4"),
]
w = 1.0
for i, (t, c) in enumerate(stages):
    ax.add_patch(plt.Rectangle((i * 1.18, 0.3), w, 0.55, facecolor=c, edgecolor="#2c3e50",
                               lw=0.9, transform=ax.transData))
    ax.text(i * 1.18 + w / 2, 0.575, t, ha="center", va="center", fontsize=7.2, weight="bold")
    if i < len(stages) - 1:
        ax.annotate("", xy=(i * 1.18 + w + 0.16, 0.575), xytext=(i * 1.18 + w, 0.575),
                    arrowprops=dict(arrowstyle="-|>", color="#2c3e50", lw=1.1))
ax.set_xlim(-0.15, len(stages) * 1.18)
ax.set_ylim(0.1, 1.0)
ax.text(0, 0.12, "Null-model validated:  modularity z = +68.3 (p < .004)   |   "
                 "edge z >= 2.5 (bipartite swap null)   |   SEMCON audited precision 0.96",
        fontsize=7, style="italic", color="#444")
save(fig, "F1_pipeline.png")

# ================================================================ F2  query artefact
art = {"athlete": 79.0, "sport system": 54.6, "elite sport": 33.0,
       "professional sport": 7.7, "sport ecosystem": 3.6, "high performance sport": 3.3,
       "sport network": 0.8, "entrepreneurial ecosystem": 0.7, "innovation ecosystem": 0.2}
ctl = {"stakeholder": 12.0, "coaching": 12.0, "well-being": 7.7, "mental health": 4.8,
       "leadership": 4.6, "technology": 4.4, "basketball": 4.1, "doping": 3.6,
       "sponsorship": 1.1, "rehabilitation": 1.0}
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.9))
ak = list(art)[::-1]; av = [art[k] for k in ak]
a1.barh(ak, av, color="#c0504d", edgecolor="#7a2e2c", lw=0.5, height=0.68)
a1.set_xlabel("documents containing term (%)")
a1.set_title("a  Terms from the search string", loc="left")
for i, v in enumerate(av):
    a1.text(v + 1, i, "%.1f" % v, va="center", fontsize=6.6, color="#7a2e2c")
ck = list(ctl)[::-1]; cv = [ctl[k] for k in ck]
a2.barh(ck, cv, color="#4f8a3d", edgecolor="#2f5c26", lw=0.5, height=0.68)
a2.set_xlabel("documents containing term (%)")
a2.set_title("b  Control terms (not in query)", loc="left")
for i, v in enumerate(cv):
    a2.text(v + 0.25, i, "%.1f" % v, va="center", fontsize=6.6, color="#2f5c26")
fig.suptitle("Query-string terms are inflated 3.68x relative to matched control terms",
             fontsize=9.5, weight="bold", y=1.02)
save(fig, "F2_query_artifact.png")

# ================================================================ F3  anisotropy
E = np.load(os.path.join(DATA, "concept_embeddings.npy"))
S = np.load(os.path.join(DATA, "concept_similarity.npy"))
rng = np.random.default_rng(0)
n = len(E)
i0 = rng.integers(0, n, 30000); i1 = rng.integers(0, n, 30000)
m = i0 != i1
i0, i1 = i0[m], i1[m]
raw = E / np.maximum(np.linalg.norm(E, axis=1, keepdims=True), 1e-12)
cc_raw = (raw[i0] * raw[i1]).sum(1)
cc_cen = (E[i0] * E[i1]).sum(1)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.5))
a1.hist(cc_raw, bins=60, color="#c0504d", alpha=0.8, edgecolor="white", lw=0.3)
a1.axvline(0.0, color="k", lw=0.8, ls="--")
a1.set_xlabel("cosine, random concept pairs")
a1.set_ylabel("frequency")
a1.set_title("a  Raw E5-v2 embeddings (mean %+.3f)" % cc_raw.mean(), loc="left")
a2.hist(cc_cen, bins=60, color="#1f4e79", alpha=0.8, edgecolor="white", lw=0.3)
a2.axvline(0.0, color="k", lw=0.8, ls="--")
a2.set_xlabel("cosine, random concept pairs")
a2.set_title("b  After mean-centring (mean %+.3f)" % cc_cen.mean(), loc="left")
fig.suptitle("Anisotropy correction: raw embeddings encode a single common direction",
             fontsize=9.5, weight="bold", y=1.03)
save(fig, "F3_anisotropy.png")

# ================================================================ F4  tau calibration
rows = list(csv.DictReader(open(os.path.join(DATA, "benchmark_tau.csv"), encoding="utf-8-sig")))
prof = json.load(open(os.path.join(DATA, "tau_selected.json"), encoding="utf-8"))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.6))
pr = [(float(r["prec"]), float(r["rec"]), float(r["f1"]), int(r["n_fam"])) for r in rows]
a1.plot([p[0] for p in pr], [p[1] for p in pr], "o-", ms=3, color="#1f4e79", lw=1.1,
        label="precision")
a1.plot([p[0] for p in pr], [p[2] for p in pr], "s--", ms=3, color="#c0504d", lw=1.1,
        label="F1")
a1.set_xlim(0.55, 0.80)
a1.set_ylim(0, 1.08)
a1.set_xlabel("tau (complete-linkage cut)")
a1.set_ylabel("score")
a1.set_title("a  Audit-benchmark performance", loc="left")
a1.legend(frameon=False)
prf = prof["profile"]
a2.plot([p[0] for p in prf], [p[1] for p in prf], "o-", ms=3.5, color="#1f4e79", lw=1.2)
a2.axhline(0.95, color="#c0504d", ls="--", lw=1.0)
a2.text(0.52, 0.955, "0.95 target", fontsize=6.8, color="#c0504d")
sel = [p for p in prf if abs(p[0] - 0.702) < 1e-6]
if sel:
    a2.scatter([sel[0][0]], [sel[0][1]], s=45, facecolor="#e8a33d", zorder=5)
    a2.annotate("tau=0.70\ncumulative precision %.3f" % sel[0][1],
                (sel[0][0], sel[0][1]), textcoords="offset points", xytext=(12, -18),
                fontsize=6.8, color="#a8712a",
                arrowprops=dict(arrowstyle="->", color="#a8712a", lw=0.8))
a2.set_xlabel("tau")
a2.set_ylabel("cumulative audited precision")
a2.set_ylim(0.80, 1.02)
a2.set_xlim(0.50, 0.95)
a2.set_title("b  Manual audit (74 merges adjudicated)", loc="left")
fig.suptitle("SEMCON threshold calibration", fontsize=9.5, weight="bold", y=1.03)
save(fig, "F4_tau_calibration.png")

# ================================================================ F5  network
cent = {}
for r in csv.DictReader(open(os.path.join(TAB, "T3_network_centrality.csv"),
                            encoding="utf-8-sig")):
    cent[int(r["family_id"])] = r
G = nx.Graph()
for i, r in cent.items():
    G.add_node(i, **r)
lbl2id = {r["label"]: i for i, r in cent.items()}
for r in csv.DictReader(open(os.path.join(DATA, "network_edges.csv"), encoding="utf-8-sig")):
    a, b = lbl2id.get(r["source"]), lbl2id.get(r["target"])
    if a is not None and b is not None:
        G.add_edge(a, b, weight=float(r["weight"]), cooc=int(r["cooc"]))

# backbone for legibility: keep edges above a weight quantile, preserving connectivity
wts = np.array([d["weight"] for _, _, d in G.edges(data=True)])
thr = float(np.quantile(wts, 0.55))
GB = nx.Graph()
GB.add_nodes_from(G.nodes())
for u, v, d in G.edges(data=True):
    if d["weight"] >= thr:
        GB.add_edge(u, v, weight=d["weight"])
for c in list(nx.connected_components(GB)):
    if len(c) < 4:
        GB.remove_nodes_from(c)
print("   backbone: %d nodes / %d edges (weight >= %.3f)" % (GB.number_of_nodes(),
                                                            GB.number_of_edges(), thr))

# Cluster-aware layout. A plain spring layout on 600 near-interconnected nodes collapses
# into a hairball, so communities are laid out separately and only then packed together.
# This makes the modular structure the visual message, which is the point of the figure.
cl_of = {n: int(cent[n]["cluster"]) for n in GB.nodes()}
cl_pos = {}
for cl in sorted(set(cl_of.values())):
    sub = nx.Graph(GB.subgraph([n for n in GB.nodes() if cl_of[n] == cl]))
    sub.remove_nodes_from(list(nx.isolates(sub)))
    if sub.number_of_nodes() < 2:
        continue
    p = nx.kamada_kawai_layout(sub, weight="weight")
    cl_pos[cl] = p

keys = sorted(cl_pos, key=lambda c: -len(cl_pos[c]))
RAD = 1.0
pos = {}
n = len(keys)
for i, cl in enumerate(keys):
    if n == 1:
        cx, cy, r = 0.0, 0.0, 0.0
    else:
        th = 2 * math.pi * i / n
        rr = RAD * (1.55 if n > 5 else 1.25)
        cx, cy, r = rr * math.cos(th), rr * math.sin(th), 0.44
    p = cl_pos[cl]
    xs = np.array([q[0] for q in p.values()]); ys = np.array([q[1] for q in p.values()])
    xs = (xs - xs.mean()) / (np.ptp(xs) + 1e-9)
    ys = (ys - ys.mean()) / (np.ptp(ys) + 1e-9)
    for node, (x, y) in p.items():
        pos[node] = np.array([cx + r * x, cy + r * y])
for node in GB.nodes():
    if node not in pos:
        a_ = 2 * math.pi * (hash(node) % 1000) / 1000.0
        pos[node] = np.array([RAD * 1.7 * math.cos(a_), RAD * 1.7 * math.sin(a_)])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 4.3))
for a, (Gh, ttl, nodekey, sizekey, cm) in zip(
        (a1, a2),
        [(GB, "a  Community structure (backbone; Q = 0.442, z = +68)", "cluster",
          "betweenness", "cluster"),
         (GB, "b  Bridging concepts (size = degree)", None,
          "betweenness", "df")]):
    ncl = max(int(r["cluster"]) for r in cent.values()) + 1
    node_c = [CLUSTER_COLOR[int(cent[n]["cluster"]) % len(CLUSTER_COLOR)] for n in Gh.nodes()]
    maxdf = max(float(r["df"]) for r in cent.values())
    if cm == "cluster":
        # square-root scaling: linear sizing makes the few high-df families dominate
        ns = [14 + 210 * (float(cent[n]["df"]) / maxdf) ** 0.62 for n in Gh.nodes()]
    else:
        mdg = max(float(r["degree"]) for r in cent.values())
        ns = [14 + 210 * (float(cent[n]["degree"]) / mdg) ** 0.62 for n in Gh.nodes()]
    ew_max = max(d["weight"] for _, _, d in Gh.edges(data=True)) - thr
    ew = [0.25 + 2.2 * (d["weight"] - thr) / max(1e-9, ew_max)
          for _, _, d in Gh.edges(data=True)]
    nx.draw_networkx_edges(Gh, pos, ax=a, width=ew, edge_color="#b0b7bf", alpha=0.5)
    nx.draw_networkx_nodes(Gh, pos, ax=a, node_size=ns, node_color=node_c,
                           edgecolors="white", linewidths=0.3)
    if nodekey:
        top = sorted(Gh.nodes(), key=lambda n: -float(cent[n][nodekey]))
        # label only nodes that are both structurally important and well separated, so that
        # labels do not pile up in the visual core
        mx = max(float(cent[t][nodekey]) for t in Gh.nodes())
        keep, used = [], []
        for n in top:
            p = pos[n]
            if all(((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5 > 0.115 for q in used):
                keep.append(n); used.append(p)
            if len(keep) >= 16:
                break
        fs = {n: 4.2 + 2.4 * math.log10(1 + 9 * float(cent[n][nodekey]) / mx) for n in keep}
        for n in keep:
            a.text(pos[n][0], pos[n][1] + 0.028, cent[n]["label"][:20], fontsize=fs[n],
                   ha="center", va="bottom", color="#111111", zorder=10, linespacing=0.9,
                   bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#b8c0c8",
                             lw=0.35, alpha=0.93))
    a.set_title(ttl, loc="left", fontsize=7.8, pad=8)
    a.set_xticks([]); a.set_yticks([])
    a.set_frame_on(False)
    a.set_xlim(-2.5, 2.5); a.set_ylim(-2.5, 2.6)
a1.legend(handles=[Patch(fc=CLUSTER_COLOR[i % len(CLUSTER_COLOR)], label="C%d" % i)
                      for i in sorted({int(r["cluster"]) for r in cent.values()})],
          frameon=False, fontsize=6.0, ncol=6, loc="lower left",
          bbox_to_anchor=(0.0, -0.06), handlelength=1.1, columnspacing=0.9)
fig.suptitle("Null-calibrated concept co-occurrence network  (669 nodes, 5,101 edges; "
             "modularity z = +68.3, p < .004)", fontsize=9.2, weight="bold", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.96])
save(fig, "F5_network.png")

# ================================================================ F6  null model
rs = list(csv.DictReader(open(os.path.join(TAB, "T3_resolution_sweep.csv"),
                              encoding="utf-8-sig")))
zs = [float(r["betweenness_z"]) for r in cent.values()]
bts = [float(r["betweenness"]) for r in cent.values()]
dfs = [float(r["df"]) for r in cent.values()]
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.4))
a1 = axs[0]
a1.plot([float(r["resolution"]) for r in rs], [float(r["modularity_Q"]) for r in rs],
        "o-", ms=3, color="#1f4e79", lw=1.2)
net = blob["net"]
a1.axhline(net["mod_null"], color="#c0504d", ls="--", lw=1.1,
           label="null mean %.3f" % net["mod_null"])
a1.fill_between([0.35, 4.05], net["mod_null"] - 2 * net["mod_sd"],
                net["mod_null"] + 2 * net["mod_sd"], color="#c0504d", alpha=0.13)
a1.axvline(net["resolution"], color="#e8a33d", lw=1.2)
a1.set_xlabel("resolution"); a1.set_ylabel("modularity Q")
a1.set_title("a  Modularity vs null", loc="left")
a1.legend(frameon=False, fontsize=6.5)
a1.text(2.2, net["mod_null"] + 0.01, "z = +%.1f" % net["mod_z"], fontsize=7, color="#c0504d")
a2 = axs[1]
a2.scatter(dfs, zs, s=5, c=np.array(zs), cmap="viridis", alpha=0.7, lw=0)
a2.axhline(1.96, color="#c0504d", ls="--", lw=0.9)
a2.axhline(2.58, color="#8064a2", ls=":", lw=0.9)
a2.set_xscale("log")
a2.set_xlabel("family document frequency (log)")
a2.set_ylabel("betweenness z vs null")
a2.set_title("b  Signif. vs degree", loc="left")
a2.text(9, 2.75, "z>1.96", fontsize=6, color="#c0504d")
a3 = axs[2]
a3.hist(bts, bins=45, color="#1f4e79", alpha=0.82, edgecolor="white", lw=0.3)
a3.set_xlabel("observed betweenness"); a3.set_ylabel("families")
a3.set_title("c  Bridging is rare", loc="left")
a3.text(0.97, 0.9, "%d of %d nodes have z > 2.58\n(%.1f%%)"
        % (sum(1 for z in zs if z > 2.58), len(zs),
           100 * sum(1 for z in zs if z > 2.58) / len(zs)),
        transform=a3.transAxes, ha="right", va="top", fontsize=6.6)
save(fig, "F6_nullmodel.png")

# ================================================================ F7  layers
bet = [(float(r["betweenness_L1"]), float(r["betweenness_L2"]), float(r["betweenness_L3"]),
        float(r["provenance_ratio"]), r["label"], int(r["cluster"]))
       for r in cent.values()]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.9))
c1 = [CLUSTER_COLOR[b[5] % len(CLUSTER_COLOR)] for b in bet]
a1.scatter([b[0] for b in bet], [b[2] for b in bet], s=13, c=c1, alpha=0.65, lw=0)
lim = max(max(b[0] for b in bet), max(b[2] for b in bet)) * 1.05
a1.plot([0, lim], [0, lim], color="k", lw=0.8, ls="--")
a1.set_xlabel("betweenness, TITLE only (L1)")
a1.set_ylabel("betweenness, full text (L3)")
a1.set_title("a  Title-layer vs full-text centrality (rho = 0.43)", loc="left")
for x, y, _, _, lb, _ in bet:
    if x > np.quantile([b[0] for b in bet], 0.985) or y > np.quantile([b[2] for b in bet], 0.985):
        a1.annotate(lb[:18], (x, y), fontsize=5.4, xytext=(3, 3),
                    textcoords="offset points", color="#333")
a1.legend(handles=[Patch(fc=CLUSTER_COLOR[i], label="C%d" % i) for i in range(5)],
          frameon=False, fontsize=6.4, ncol=5, loc="upper left")
a1.set_xlim(-lim * 0.03, lim); a1.set_ylim(-lim * 0.03, lim)
pr = [b[3] for b in bet]
bt3 = [b[2] for b in bet]
sc = a2.scatter(pr, bt3, s=13, c=c1, alpha=0.65, lw=0)
a2.axhline(np.median(bt3), color="#888", ls=":", lw=0.8)
a2.axvline(np.median(pr), color="#888", ls=":", lw=0.8)
a2.set_xlabel("provenance ratio  (df in title / df in full text)")
a2.set_ylabel("betweenness, full text")
a2.set_title("b  Framing vs intellectual infrastructure", loc="left")
q1, q3 = np.quantile(pr, [0.25, 0.75])
a2.axvspan(pr and min(pr) - 0.01, q1, color="#e8a33d", alpha=0.09)
a2.axvspan(q3, max(pr) + 0.01, color="#1f4e79", alpha=0.07)
a2.text(0.02, 0.04, "BURIED\n(structural but\nunadvertised)", transform=a2.transAxes,
        fontsize=6, color="#1f4e79")
a2.text(0.70, 0.04, "FRAMING\n(promoted in\ntitles)", transform=a2.transAxes,
        fontsize=6, color="#a8712a", ha="center")
fig.suptitle("Concept stratification: only 8% of concept mentions appear in titles",
             fontsize=9.5, weight="bold", y=1.02)
save(fig, "F7_layers.png")

# ================================================================ F8  topics
tp = list(csv.DictReader(open(os.path.join(TAB, "T4_topics.csv"), encoding="utf-8-sig")))
# direction comes from the temporal table (stage 6), keyed by topic
_dir = {r["label"][:26]: r["direction"]
        for r in csv.DictReader(open(os.path.join(TAB, "T6_temporal_topics.csv"),
                                     encoding="utf-8-sig"))}
for r in tp:
    r["direction"] = _dir.get(r["label"][:26], "STABLE")
Eu = np.load(os.path.join(DATA, "doc_umap.npy"))
tl_ = list(csv.DictReader(open(os.path.join(DATA, "topic_labels.csv"), encoding="utf-8-sig")))
ordm = [int(r["doc_id"]) for r in sorted(tl_, key=lambda r: int(r["doc_id"]))]
Ts = np.array([int(r["topic"]) for r in sorted(tl_, key=lambda r: int(r["doc_id"]))])
YR = np.array([int(r["year"]) for r in sorted(tl_, key=lambda r: int(r["doc_id"]))])
nT = max(tp, key=lambda r: int(r["n"]))
fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.1),
                        gridspec_kw={"width_ratios": [1.15, 1]})
a1 = axs[0]
cmap = plt.get_cmap("tab10")
for t in sorted(set(Ts)):
    m = Ts == t
    c = "#b0b0b0" if t == -1 else cmap(t % 10)
    a1.scatter(Eu[m, 0], Eu[m, 1], s=7, c=c, alpha=0.65, lw=0,
               label=("noise" if t == -1 else "T%d" % t))
    if t != -1 and m.sum() >= 3:
        cx, cy = Eu[m, 0].mean(), Eu[m, 1].mean()
        a1.annotate("T%d" % t, (cx, cy), fontsize=7.5, weight="bold", color="#222",
                    xytext=(0, 12), textcoords="offset points", ha="center")
a1.legend(frameon=False, fontsize=6, ncol=3, loc="lower left")
a1.set_xticks([]); a1.set_yticks([]); a1.set_frame_on(False)
a1.set_title("a  UMAP + HDBSCAN: %d topics, %.0f%% noise (silhouette %.2f)"
             % (len(tp), 100 * blob["topics"]["noise_share"],
                blob["topics"]["silhouette"]), loc="left")
a2 = axs[1]
tprow = sorted(tp, key=lambda r: int(r["topic"]))
lbl = [r["label"][:26] for r in tprow]
shr = [100 * float(r["share"]) for r in tprow]
ypos = np.arange(len(lbl))
a2.barh(ypos, shr, color=["#c0504d" if r["direction"] == "EMERGING" else
                          "#1f4e79" if r["direction"] == "DECLINING" else "#8a9aa8"
                          for r in tprow], edgecolor="white", lw=0.4, height=0.66)
a2.set_yticks(ypos); a2.set_yticklabels(lbl, fontsize=6.4)
a2.set_xlabel("share of windowed corpus (%)")
a2.set_title("b  Topic prevalence and direction", loc="left")
for i, (s, r) in enumerate(zip(shr, tprow)):
    a2.text(s + 0.5, i, "%.1f%%  %s" % (s, r["direction"][0]), va="center", fontsize=6.2)
a2.set_xlim(0, max(shr) * 1.32)
save(fig, "F8_topics.png")

# ================================================================ F9  pillars
pl = list(csv.DictReader(open(os.path.join(TAB, "T5_pillars.csv"), encoding="utf-8-sig")))
PCOL = {"GOVERNANCE": "#1f4e79", "INNOVATION": "#c0504d", "TALENT": "#4f8a3d",
        "UNASSIGNED": "#9aa5b1"}
order = ["GOVERNANCE", "INNOVATION", "TALENT", "UNASSIGNED"]
gp = {p: [float(x["supra"]) for x in pl if x["pillar"] == p] for p in order}
cnt = {p: len(v) for p, v in gp.items()}
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.6), gridspec_kw={"width_ratios": [1, 1, 1.15]})
a1 = axs[0]
vals = [cnt[p] for p in order]
a1.bar(order, vals, color=[PCOL[p] for p in order], edgecolor="white", lw=0.5)
for i, v in enumerate(vals):
    a1.text(i, v + 5, str(v), ha="center", fontsize=7)
a1.set_ylabel("concept families")
a1.set_title("a  Pillar assignment", loc="left")
a1.tick_params(axis="x", labelrotation=20, labelsize=6.5)
a2 = axs[1]
for p in order:
    v = np.sort(gp[p])
    a2.plot(np.linspace(0, 1, len(v)), v, lw=1.2, color=PCOL[p], label=p)
a2.set_xlabel("quantile"); a2.set_ylabel("supra-centrality")
a2.set_title("b  Supra-centrality by pillar", loc="left")
a2.legend(frameon=False, fontsize=6)
a2 = axs[2]
a2.axis("off")
a2.text(0, 1.0, "c  TOP BRIDGES BY PILLAR", fontsize=8, weight="bold", transform=a2.transAxes)
yv = 0.86
for p in order[:3]:
    a2.text(0, yv, p, color=PCOL[p], fontsize=7, weight="bold", transform=a2.transAxes)
    yv -= 0.055
    top = [x["label"] for x in sorted([r for r in pl if r["pillar"] == p],
                                      key=lambda r: -float(r["supra"]))[:7]]
    a2.text(0.02, yv, ", ".join(top), fontsize=6.2, transform=a2.transAxes, wrap=True)
    yv -= 0.13
a2.text(0, yv - 0.02, "Supra = betweenness summed over all layers a node inhabits.\n"
                      "Bridges connect pillars that are otherwise segregated (z = -2.15).",
        fontsize=6.2, style="italic", transform=a2.transAxes, color="#444")
save(fig, "F9_pillars.png")

# ================================================================ F10 temporal
tt = list(csv.DictReader(open(os.path.join(TAB, "T6_temporal_topics.csv"), encoding="utf-8-sig")))
em = list(csv.DictReader(open(os.path.join(TAB, "T6_concept_emergence.csv"),
                              encoding="utf-8-sig")))
fig, axs = plt.subplots(1, 2, figsize=(7.4, 2.8), gridspec_kw={"width_ratios": [1.1, 1]})
a1 = axs[0]
PER = blob["temporal"]["periods"]
top_t = sorted([r for r in tt if int(r["n"]) >= 12], key=lambda r: -int(r["n"]))[:7]
cnt_by_t = collections.defaultdict(list)
for r in tt:
    cnt_by_t[r["label"][:26]].append(r)
for r in top_t:
    k = r["label"][:26]
    n = int(r["n"])
    share = [float(r["share_late"])] * len(PER)
    a1.plot([p[1] for p in PER], [n * s for p, s in zip(PER, share)], "-", lw=0.8,
            color="#cccccc")
# proper area chart: topic x period counts
cnt_tab = {}
for r in csv.DictReader(open(os.path.join(TAB, "T6_temporal_topics.csv"),
                             encoding="utf-8-sig")):
    cnt_tab[r["label"][:26]] = r
# rebuild counts from topic_labels
from collections import Counter
per_i = [0] * len(PER)
for i, y in enumerate(YR):
    for j, (a, b) in enumerate(PER):
        if a <= y <= b:
            per_i[j] += 1
a1b = a1.twinx()
a1b.bar([np.mean(p) for p in PER], per_i, color="#dfe6ec", edgecolor="#c2ccd4", lw=0.6,
        width=1.1, zorder=0)
a1.set_zorder(1); a1.patch.set_visible(False)
a1b.set_ylabel("documents per period", color="#7a8794")
a1b.tick_params(axis="y", colors="#7a8794", labelsize=7)
cnt_all = collections.defaultdict(lambda: [0] * len(PER))
for r in tl_:
    t = int(r["topic"]); y = int(r["year"])
    lab_ = "noise" if t == -1 else next((x["label"][:26] for x in tp if int(x["topic"]) == t), "")
    for j, (a, b) in enumerate(PER):
        if a <= y <= b:
            cnt_all[lab_][j] += 1
keys = sorted([k for k, v in cnt_all.items() if sum(v) >= 12],
              key=lambda k: -sum(cnt_all[k]))[:7]
cols = plt.get_cmap("tab10")(np.linspace(0, 0.9, len(keys)))
xs = [np.mean(p) for p in PER]
for k, c in zip(keys, cols):
    v = cnt_all[k]
    a1.fill_between(xs, v, alpha=0.16, color=c)
    a1.plot(xs, v, "-o", ms=3.4, lw=1.3, color=c, label="%s (n=%d)" % (k, sum(v)))
a1.set_ylabel("documents per topic")
a1.set_xlabel("period midpoint")
a1.set_title("a  Thematic evolution (chi2 = %.1f, V = %.2f, p = %.1e)"
             % (blob["temporal"]["chi2"], blob["temporal"]["cramersV"],
                blob["temporal"]["p"]), loc="left")
a1.legend(frameon=False, fontsize=5.9, ncol=2, loc="upper left")
a2 = axs[1]
sc = [(float(r["share_since_2021"]), float(r["mean_year"]), r["family"]) for r in em]
sc.sort(key=lambda x: x[1])
a2.scatter([x[0] for x in sc], [x[1] for x in sc], s=13, c=np.array([x[0] for x in sc]),
           cmap="plasma", alpha=0.75, lw=0)
a2.axhline(2021, color="#888", ls="--", lw=0.8)
a2.set_xlabel("share of mentions since 2021")
a2.set_ylabel("mean publication year")
a2.set_title("b  Concept frontier", loc="left")
for x, y, lb in sc:
    if y > np.quantile([s[1] for s in sc], 0.985) or y < np.quantile([s[1] for s in sc], 0.02):
        a2.annotate(lb[:16], (x, y), fontsize=5.6, xytext=(3, 3),
                    textcoords="offset points", color="#333")
save(fig, "F10_temporal.png")

# ================================================================ F11 national
ct = list(csv.DictReader(open(os.path.join(TAB, "T6_country_topic.csv"), encoding="utf-8-sig")))
cf = list(csv.DictReader(open(os.path.join(TAB, "T6_country_family.csv"), encoding="utf-8-sig")))
DEM = {"canada", "canadian", "australia", "australian", "russia", "russian", "germany",
       "german", "china", "chinese", "uk", "british", "norway", "norwegian", "spain",
       "spanish", "switzerland", "swiss", "usa", "america", "american", "england",
       "english", "europe", "european", "western", "eastern", "korea", "korean",
       "brazil", "brazilian", "poland", "polish", "india", "indian", "japan",
       "japanese", "sweden", "swedish", "portugal", "portuguese", "belgium", "belgian",
       "netherlands", "dutch", "finland", "finnish", "denmark", "danish", "hungary",
       "hungarian", "austria", "austrian", "ukraine", "ukrainian", "france", "french",
       "italy", "italian", "asia", "african", "eligible", "editors", "relevant"}
countries = sorted({r["country"] for r in ct}, key=lambda c: -int(
    next(r["n_country"] for r in ct if r["country"] == c)))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.9),
                             gridspec_kw={"width_ratios": [1.3, 1]})
a1.axis("off")
a1.text(0, 1.0, "a  NATIONAL RESEARCH EMPHASES", fontsize=8.5, weight="bold",
        transform=a1.transAxes)
a1.text(0, 0.93, "families over-represented in a national system (lift>1.3, q<0.05); "
                 "country-name families excluded as circular",
        fontsize=6.2, style="italic", transform=a1.transAxes, color="#555")
yv = 0.83
for c in countries[:8]:
    top = [r for r in cf if r["country"] == c and r["family"] not in DEM
           and float(r["lift"]) > 1.3 and int(r["significant"]) == 1]
    top.sort(key=lambda r: -float(r["lift"]))
    n = int(next(r["n_country"] for r in ct if r["country"] == c))
    a1.text(0, yv, "%s  (n=%d)" % (c, n), fontsize=6.8, weight="bold",
            transform=a1.transAxes)
    yv -= 0.048
    txt = ", ".join("%s (x%.1f)" % (r["family"][:22], float(r["lift"])) for r in top[:4])
    a1.text(0.012, yv, txt if txt else "(no significant emphasis)", fontsize=6.1,
            transform=a1.transAxes, color="#333")
    yv -= 0.072
nat = blob["national"]
a1.text(0, yv - 0.01, "Topic x country: chi2 = %.1f, V = %.2f, p = %.1e"
        % (nat["chi2"], nat["cramersV"], nat["p"]), fontsize=6.6,
        transform=a1.transAxes, weight="bold")
lift = [float(r["lift"]) for r in cf if r["family"] not in DEM]
sigc = [int(r["significant"]) for r in cf if r["family"] not in DEM]
a2.hist([l for l, s in zip(lift, sigc) if s == 1], bins=28, color="#1f4e79", alpha=0.85,
        edgecolor="white", lw=0.3, label="q < 0.05")
a2.hist([l for l, s in zip(lift, sigc) if s == 0], bins=28, color="#c6cdd4", alpha=0.85,
        edgecolor="white", lw=0.3, label="n.s.")
a2.axvline(1.0, color="k", lw=0.8, ls="--")
a2.set_xscale("log")
a2.set_xlabel("lift (country share / rest-of-corpus share)")
a2.set_ylabel("country x family cells")
a2.set_title("b  Effect-size distribution", loc="left")
a2.legend(frameon=False, fontsize=6.5)
save(fig, "F11_national.png")
print("\nAll figures written to %s" % FIG)
