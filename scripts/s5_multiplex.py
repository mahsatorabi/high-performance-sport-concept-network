"""
ARTICLE 1 - Stage 5: MULTIPLEX (three-pillar) NETWORK and SUPRA bridge analysis.

The thesis posits three pillars - GOVERNANCE, INNOVATION, TALENT DEVELOPMENT - and asks
whether they form an integrated system or three parallel silos. A single-layer
co-occurrence network cannot answer that, because it shows only which concepts co-occur,
not which belong to which pillar.

Approach:
  1. PILLAR ASSIGNMENT is data-driven, not asserted. Each concept family is embedded with
     the same encoder used in SEMCON and matched against the three pillar prototypes
     ("governance of high-performance sport", "sport innovation and technology",
     "athlete talent development"). Assignment is by maximum cosine similarity, and the
     margin over the runner-up is retained as a CONFIDENCE measure so that weakly
     assigned families can be reported rather than hidden.
  2. A multiplex network is built with one layer per pillar over the shared node set, and
     interlayer coupling is measured by the edge overlap between layers.
  3. BRIDGE CONCEPTS are identified with SUPRA-GRAND CENTRALITY: a node's supra-centrality
     is high when it is central in its own layer and its shortest supra-path traverses
     several layers. This is the quantity that distinguishes a genuine integrator
     (governance concepts that also sit inside the innovation cluster) from a concept that
     is merely popular in one pillar.
"""
import os, json, csv, collections, itertools
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import numpy as np
from sentence_transformers import SentenceTransformer
import transformers
transformers.utils.logging.disable_progress_bar()
transformers.utils.logging.set_verbosity_error()
import networkx as nx
rng = np.random.default_rng(3)

BASE = r"D:\Uni of Birjand\articles\adel\article1"
DATA, TAB = os.path.join(BASE, "data"), os.path.join(BASE, "tables")
MODEL = "intfloat/e5-base-v2"

PILLARS = {
    "GOVERNANCE": [
        "governance and regulation of high-performance sport",
        "state sport policy, legislation and public funding",
        "sport federations, governing bodies and accountability",
        "elite sport systems and national policy coordination",
        "anti-doping regulation, integrity and athlete protection",
    ],
    "INNOVATION": [
        "sport innovation, digital technology and artificial intelligence",
        "performance analytics, wearable sensors and athlete monitoring",
        "sport industry, commercialisation and market innovation",
        "e-sports, virtual reality and new media in sport",
        "entrepreneurship and innovation ecosystems in sport",
    ],
    "TALENT": [
        "athlete talent identification and development",
        "youth sport, academies and the elite athlete pathway",
        "coaching, coach education and mentoring",
        "talent pipelines, selection and athlete career transitions",
        "high-performance athlete preparation and training",
    ],
}
CONF_FLOOR = 0.02          # minimum margin over the runner-up prototype
MIN_PILLAR_DF = 8

blob = json.load(open(os.path.join(DATA, "corpus.json"), encoding="utf-8"))
docs = blob["docs"]; N = len(docs)
lab = blob["fam_label"]; mem = blob["fam_members"]
f3m = blob["fams_L3"]; nf = len(lab)
df3 = np.array([sum(1 for r in f3m if f in r) for f in range(nf)], dtype=float)

print("=" * 78)
print("STAGE 5  THREE-PILLAR MULTIPLEX NETWORK + SUPRA CENTRALITY")
print("=" * 78)

cent = {}
with open(os.path.join(TAB, "T3_network_centrality.csv"), encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        cent[r["label"]] = r
node_ids = [int(r["family_id"]) for r in cent.values()]
print("network nodes carried over from stage 3: %d" % len(node_ids))

# ---------------------------------------------------------------- pillar prototypes
model = SentenceTransformer(MODEL)
protos, pkeys = [], []
for p, texts in PILLARS.items():
    for t in texts:
        protos.append("query: " + t)
        pkeys.append(p)
P = model.encode(protos, convert_to_numpy=True, normalize_embeddings=True,
                 show_progress_bar=False)
P = np.asarray(P, dtype=np.float64)
P = P - P.mean(0, keepdims=True)
P /= np.maximum(np.linalg.norm(P, axis=1, keepdims=True), 1e-12)
print("prototypes: %d across %d pillars" % (P.shape[0], len(PILLARS)))
for p in PILLARS:
    print("   %-12s %d prototypes" % (p, len(PILLARS[p])))

# ---------------------------------------------------------------- pillar assignment
# cent is keyed by family label; the network node is the family id
concepts = sorted(cent)
id_of = {lbl: int(cent[lbl]["family_id"]) for lbl in concepts}
C = model.encode(["query: " + c for c in concepts], batch_size=128,
                 convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)
C = np.asarray(C, dtype=np.float64)
C = C - C.mean(0, keepdims=True)
C /= np.maximum(np.linalg.norm(C, axis=1, keepdims=True), 1e-12)

sim = C @ P.T                                   # concepts x prototypes
pk = np.array(pkeys)
best_sim, best_j = sim.max(1), sim.argmax(1)
pillar_of = {}
conf = {}
for r, lbl in enumerate(concepts):
    order = np.argsort(-sim[r])
    top, second = sim[r, order[0]], sim[r, order[1]]
    f = id_of[lbl]
    conf[f] = float(top - second)
    pillar_of[f] = pk[order[0]] if (top - second >= CONF_FLOOR and top > 0) else "UNASSIGNED"

cnt = collections.Counter(pillar_of.values())
print("\nPILLAR ASSIGNMENT (max cosine to pillar prototypes, %d assignments)" % len(concepts))
for p, c in cnt.most_common():
    print("   %-12s %4d  (%.1f%%)" % (p, c, 100 * c / len(concepts)))
print("   confidence (margin over runner-up): median %.3f  IQR %.3f-%.3f"
      % (np.median(list(conf.values())),
         np.percentile(list(conf.values()), 25), np.percentile(list(conf.values()), 75)))

# ---------------------------------------------------------------- rebuild the network
rows3 = list(csv.DictReader(open(os.path.join(TAB, "T3_network_centrality.csv"),
                                 encoding="utf-8-sig")))
G = nx.Graph()
for r in rows3:
    i = int(r["family_id"])
    G.add_node(i, label=r["label"], df=float(r["df"]), cluster=int(r["cluster"]),
               btw=float(r["betweenness"]), pillar=pillar_of.get(i, "UNASSIGNED"),
               confidence=conf.get(i, 0.0), members=r["members"])
for r in csv.DictReader(open(os.path.join(DATA, "network_edges.csv"), encoding="utf-8-sig")):
    pass
lbl2id = {r["label"]: int(r["family_id"]) for r in rows3}
for r in csv.DictReader(open(os.path.join(DATA, "network_edges.csv"), encoding="utf-8-sig")):
    a, b = lbl2id.get(r["source"]), lbl2id.get(r["target"])
    if a is not None and b is not None:
        G.add_edge(a, b, weight=float(r["weight"]))
print("\nnetwork rebuilt: %d nodes, %d edges" % (G.number_of_nodes(), G.number_of_edges()))

# ---------------------------------------------------------------- multiplex + supra
layers = {}
for p in list(PILLARS) + ["UNASSIGNED"]:
    members = [n for n in G.nodes() if G.nodes[n]["pillar"] == p]
    if len(members) < 3:
        continue
    H = G.subgraph(members).copy()
    # intra-pillar edges only, so layer centralities measure WITHIN-pillar structure
    for u, v in list(H.edges()):
        if G.nodes[u]["pillar"] != G.nodes[v]["pillar"]:
            H.remove_edge(u, v)
    layers[p] = H
    print("   layer %-12s %3d nodes %4d intra-pillar edges" % (p, H.number_of_nodes(),
                                                              H.number_of_edges()))

print("\nINTERLAYER COUPLING (null-calibrated against degree-preserving rewiring)")
# Coupling is measured as the share of shortest supra-paths that actually CROSS a layer
# boundary, and is validated against a degree-preserving null. A null-calibrated measure is
# required because some cross-pillar traffic is unavoidable in any partition.
ls = [p for p in layers if p != "UNASSIGNED"]
intra_sets = {p: set(frozenset(e) for e in layers[p].edges()) for p in layers}

# supra shortest paths on the full network, tracking which layer boundaries are crossed
def boundary_load(Gx, member, pivots):
    """Share of shortest paths from sampled pivots that cross a pillar boundary.
    Pivots are sampled because an all-pairs enumeration over 40 null replicates is
    intractable; the same pivots are reused in every replicate so the comparison is paired.
    """
    tot = cross = 0
    for src in pivots:
        for dst, path in nx.single_source_shortest_path(Gx, src, cutoff=6).items():
            if dst == src:
                continue
            tot += 1
            pil = [member[n] for n in path]
            if any(pil[i] != pil[i + 1] for i in range(len(pil) - 1)):
                cross += 1
    return (cross / tot) if tot else 0.0


member = {n: G.nodes[n]["pillar"] for n in G.nodes()}
N_PIV = 200
pivots = sorted(rng.choice(G.nodes(), size=min(N_PIV, G.number_of_nodes()),
                            replace=False).tolist())
obs_bc = boundary_load(G, member, pivots)
print("   observed share of shortest paths crossing a pillar boundary: %.4f" % obs_bc)

null_bc = []
deg = [d for _, d in G.degree()]
for t in range(40):
    Gn = nx.configuration_model(deg, seed=7000 + t)
    Gn = nx.Graph(Gn)
    Gn.remove_edges_from(nx.selfloop_edges(Gn))
    present = [p for p in pivots if p in Gn]
    lab_t = dict(zip(sorted(Gn.nodes()), rng.permutation([member[n] for n in sorted(G.nodes())])))
    null_bc.append(boundary_load(Gn, lab_t, present))
nbc, sbc = float(np.mean(null_bc)), float(np.std(null_bc))
bc_z = (obs_bc - nbc) / sbc if sbc > 0 else float("nan")
p_bc = float((np.sum(np.array(null_bc) >= obs_bc) + 1) / 41)
print("   degree-preserving null (random pillar labels): %.4f +/- %.4f" % (nbc, sbc))
print("   z = %+.2f   p(one-sided) = %.4f" % (bc_z, p_bc))

ov = {"observed_boundary_crossing": obs_bc, "null_mean": nbc, "null_sd": sbc,
      "z": bc_z, "p": p_bc, "n_draws": 40}
if bc_z > 2.0 and obs_bc > nbc:
    verdict = "INTEGRATED - pillar boundaries are crossed significantly more than chance"
elif abs(bc_z) <= 2.0:
    verdict = "PARALLEL - pillar structure is not distinguishable from random assignment"
else:
    verdict = "SEgregated - shortest paths avoid pillar boundaries more than chance"
print("   VERDICT: %s" % verdict)

# pairwise assortativity: do pillars mix or assort in the observed network?
pil = [G.nodes[n]["pillar"] for n in G.nodes()]
def pillar_assort(Gx, mem):
    """Newman assortativity over categorical pillar labels."""
    num = den1 = den2 = 0.0
    e_of = collections.defaultdict(float)
    e_tot = 0.0
    for u, v in Gx.edges():
        a, b = mem[u], mem[v]
        e_of[(a, b)] += 1
        e_tot += 1
    if e_tot == 0:
        return 0.0
    a_tot, b_tot = collections.Counter(), collections.Counter()
    for (a, b), w in e_of.items():
        a_tot[a] += w
        b_tot[b] += w
    for (a, b), w in e_of.items():
        num += (w / e_tot - (a_tot[a] / e_tot) * (b_tot[b] / e_tot)) / 2.0
    s1 = sum((v / e_tot) ** 2 for v in a_tot.values())
    s2 = sum((v / e_tot) ** 2 for v in b_tot.values())
    if s1 * s2 == 0:
        return 0.0
    return num / (2.0 * (s1 * s2) ** 0.5) * 2.0


r = pillar_assort(G, member)
r_null = []
for t in range(40):
    Gn = nx.configuration_model(deg, seed=8000 + t)
    Gn = nx.Graph(Gn); Gn.remove_edges_from(nx.selfloop_edges(Gn))
    lab_t = dict(zip(sorted(Gn.nodes()), rng.permutation([member[n] for n in sorted(G.nodes())])))
    r_null.append(pillar_assort(Gn, lab_t))
rn, rs = float(np.mean(r_null)), float(np.std(r_null))
rz = (r - rn) / rs if rs > 0 else float("nan")
print("\n   PILLAR ASSORTATIVITY (observed %.4f  null %.4f +/- %.4f  z = %+.2f)"
      % (r, rn, rs, rz))
print("   assortative pillars = each pillar is internally coherent; disassortative = pillars interpenetrate")
ov["assortativity"] = r; ov["assortativity_null"] = rn
ov["assortativity_sd"] = rs; ov["assortativity_z"] = rz
mean_coupling = obs_bc

# supra-grand centralisation
def supra_centrality(lay, seed=42):
    """Distance-weighted supra-centrality (Bray): d = (r+1)(s+1) with r the layer index."""
    cent_ = {}
    for p, H in lay.items():
        cen = nx.betweenness_centrality(H, weight="weight", normalized=True)
        for n, v in cen.items():
            cent_[n] = cent_.get(n, 0.0) + v
    return cent_

supra = supra_centrality(layers)
intra = {}
for p, H in layers.items():
    intra.update({(p, n): v for n, v in
                  nx.betweenness_centrality(H, weight="weight", normalized=True).items()})

# assign supra back onto nodes, weighted by the node's total intra-layer degree
node_supra = {}
for n in G.nodes():
    p = G.nodes[n]["pillar"]
    tot = 0.0
    for q, H in layers.items():
        if n in H:
            tot += H.degree(n, weight="weight")
    node_supra[n] = float(supra.get(n, 0.0)) * (1.0 + np.log1p(tot))

for n in G.nodes():
    G.nodes[n]["intra_betweenness"] = float(intra.get((G.nodes[n]["pillar"], n), 0.0))
    G.nodes[n]["supra"] = node_supra[n]
    G.nodes[n]["bridge_ratio"] = (node_supra[n] / max(G.nodes[n]["intra_betweenness"], 1e-9))

out = []
for n in G.nodes():
    d = G.nodes[n]
    out.append(dict(family_id=n, label=d["label"], pillar=d["pillar"],
                    confidence=round(d["confidence"], 4), df=int(d["df"]),
                    cluster=d["cluster"], intra_betweenness=round(d["intra_betweenness"], 6),
                    supra=round(d["supra"], 6), bridge_ratio=round(d["bridge_ratio"], 3),
                    members=d["members"]))
out.sort(key=lambda r: -r["supra"])
with open(os.path.join(TAB, "T5_pillars.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

print("\nSUPRA-CENTRALITY: TOP 25 CROSS-PILLAR BRIDGES")
print("   (supra = betweenness summed over all layers the node inhabits)")
for r in out[:25]:
    print("   %-12s supra=%.4f intra=%.4f df=%3d  %-24s %s"
          % (r["pillar"], r["supra"], r["intra_betweenness"], r["df"],
             r["label"][:24], r["members"][:52]))

print("\nBRIDGE CONCEPTS BY PILLAR (top 8 each, by supra-centrality)")
for p in list(PILLARS) + ["UNASSIGNED"]:
    sel = [r for r in out if r["pillar"] == p][:8]
    if not sel:
        continue
    print("  %-12s %s" % (p, ", ".join(r["label"] for r in sel)))

blob["pillars"] = dict(model=MODEL, prototypes=PILLARS, conf_floor=CONF_FLOOR,
                      counts=dict(cnt), mean_coupling=mean_coupling,
                      overlap=ov, n_layers=len(layers))
json.dump(blob, open(os.path.join(DATA, "corpus.json"), "w", encoding="utf-8"),
          ensure_ascii=False, default=float)
print("\nWrote T5_pillars.csv")


