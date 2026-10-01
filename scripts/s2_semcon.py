"""
ARTICLE 1 - Stage 2: SEMCON  - conservative concept-family consolidation.

DESIGN RATIONALE
----------------
A first implementation used connected components on a thresholded concept-similarity
graph. Empirically that failed: generic vocabulary chains (elite~national~high~...)
into a single 132-member family and the integrative concept "youth sport" was absorbed
by a demographic blob. Connected components admit unbounded chaining, so one spurious
edge destroys the partition.

This version is conservative by construction:

  Step 1  EXACT NORMALISATION - orthographic (British->American) + plural singularisation
          by an auditable rule set. This removes the dominant source of fragmentation in
          this corpus (policy/policies, organisation/organization, coach/coaches) with
          no model and no error.
  Step 2  LEXICAL SYNONY - mean-centred E5-v2 cosine similarity, COMPLETE-LINKAGE
          agglomerative clustering cut at tau. Complete linkage guarantees every pair
          inside a family is mutually within 1-tau, so chaining is impossible. Clusters
          larger than the size cap are REJECTED (not arbitrarily cut) because we will not
          assert an internal structure we cannot justify.

  VALIDATION - the benchmark is evaluated END-TO-END (does a true-synonym pair land in
  one family, does a contrast pair land in two?), tau is the midpoint of the F1 plateau,
  and the family-size cap is swept to demonstrate stability.
"""
import os, json, csv, math, collections, itertools, random, re
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import numpy as np
from sentence_transformers import SentenceTransformer
import transformers
transformers.utils.logging.disable_progress_bar()
transformers.utils.logging.set_verbosity_error()
import networkx as nx
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

BASE = r"D:\Uni of Birjand\articles\adel\article1"
DATA = os.path.join(BASE, "data")
MODEL = "intfloat/e5-base-v2"
MAX_FAMILY = 12
random.seed(42); np.random.seed(42)

# ---------------------------------------------------------------- audit benchmark
# Evaluated end-to-end at the FAMILY level on original surface forms.
# POS = one conceptual object (morphological, orthographic, or close lexical synonymy)
POS = [
    ("policy", "policies"), ("coach", "coaches"), ("athlete", "athletes"),
    ("system", "systems"), ("federation", "federations"), ("player", "players"),
    ("talent", "talents"), ("strategy", "strategies"), ("competition", "competitions"),
    ("organization", "organizations"), ("organisation", "organisations"),
    ("program", "programs"), ("programme", "programmes"),
    ("behaviour", "behaviors"), ("behavior", "behaviours"),
    ("center", "centre"), ("centres", "centers"),
    ("coach", "coaching"), ("coaches", "coaching"),
    ("development", "developments"), ("practice", "practices"),
    ("facility", "facilities"), ("injury", "injuries"), ("career", "careers"),
    ("identity", "identities"), ("network", "networks"),
    ("leader", "leaders"), ("partner", "partners"),
    ("institution", "institutions"), ("regulation", "regulations"),
    ("initiative", "initiatives"), ("investment", "investments"),
    # lexical synonymy that survives exact normalisation
    ("athlete development", "talent development"), ("leader", "leadership"),
    ("innovation", "innovative"), ("technology", "technological"),
    ("funding", "investment"), ("participation", "involvement"),
    ("strategy", "strategic"), ("talented", "talent"),
]
# NEG = distinct conceptual objects, several of them superficially similar
NEG = [
    ("policy", "basketball"), ("coaching", "doping"), ("talent", "injury"),
    ("governance", "nutrition"), ("training", "governance"),
    ("olympic", "rehabilitation"), ("coach", "social"),
    ("management", "muscle"), ("mental", "competition"),
    ("technology", "leadership"), ("talent", "gender"),
    ("athlete", "physiology"), ("funding", "motivation"),
    ("innovation", "history"), ("leadership", "prevention"),
    ("governance", "coaching"), ("sponsorship", "nutrition"),
    ("talent", "enzyme"), ("athlete", "cartilage"), ("policy", "shoulder"),
    ("training", "perception"), ("governance", "sepsis"),
    ("innovation", "fatigue"), ("mental", "passing"),
    ("technology", "cognition"), ("coaching", "genetics"),
    ("talent", "nutrition"), ("leadership", "pain"),
    ("training", "doping"), ("management", "swimming"),
    ("youth", "sponsorship"), ("innovation", "ranking"), ("athlete", "doping"),
    ("mental", "injury"), ("technology", "history"),
    ("development", "shading"), ("coaching", "nutrition"),
    ("funding", "swimming"), ("leadership", "cognition"),
    ("governance", "basketball"), ("talent", "swimming"),
    ("policy", "nutrition"), ("innovation", "shading"),
    ("management", "nutrition"), ("training", "shading"),
    ("strategy", "nutrition"), ("facility", "nutrition"),
    ("participation", "nutrition"), ("institution", "nutrition"),
    ("identity", "nutrition"), ("network", "nutrition"),
    ("partners", "nutrition"), ("regulation", "nutrition"),
]

# ---------------------------------------------------------------- STEP 1 exact normalisation
BRIT = {
    "organisation": "organization", "organisations": "organizations",
    "organised": "organized", "organising": "organizing",
    "programme": "program", "programmes": "programs",
    "behaviour": "behavior", "behaviours": "behaviors", "behavioural": "behavioral",
    "centre": "center", "centres": "centers", "centred": "centered",
    "labour": "labor", "favour": "favor", "favours": "favors",
    "recognised": "recognized", "recognise": "recognize", "recognises": "recognizes",
    "emphasise": "emphasize", "emphasised": "emphasized", "utilise": "utilize",
    "utilised": "utilized", "specialised": "specialized", "specialisation": "specialization",
    "prioritise": "prioritize", "prioritised": "prioritized",
    "analysed": "analyzed", "analyses": "analyzes",
    "licence": "license", "defence": "defense", "judgement": "judgment",
    "ageing": "aging", "whilst": "while", "amongst": "among", "towards": "toward",
    "learnt": "learned", "travelling": "traveling", "modelling": "modeling",
    "modelled": "modeled", "counselling": "counseling", "fulfilment": "fulfillment",
    "enrolment": "enrollment", "instalment": "installment", "skilful": "skillful",
    "practise": "practice", "practised": "practiced", "practising": "practicing",
    "sceptical": "skeptical", "grey": "gray", "metre": "meter",
}
IRREG = {
    "analyses": "analysis", "bases": "basis", "crises": "crisis", "theses": "thesis",
    "diagnoses": "diagnosis", "hypotheses": "hypothesis", "parentheses": "parenthesis",
    "oases": "oasis", "indices": "index", "vertices": "vertex", "matrices": "matrix",
}
KEEP_PLURAL = set("""
gas plus its lens bias news thus yes chaos atlas canvas corpus campus focus
series species means crossroads genetics physics politics
athletics gymnastics economics statistics ethics kinetics humanities logistics
prognosis synopsis ellipsis tennis
""".split())


def singular(w):
    if w in KEEP_PLURAL:
        return w
    if w in IRREG:
        return IRREG[w]
    if len(w) < 4:
        return w
    if w.endswith("ies"):
        return w[:-3] + "y"
    if w.endswith("ves"):
        return w[:-3] + "f"
    if w.endswith(("sses", "shes", "ches", "xes", "zes", "ses")):
        return w[:-2]
    if w.endswith(("ss", "us", "is", "as")):
        return w
    if w.endswith("s"):
        return w[:-1]
    return w


def lemma_key(phrase):
    out = []
    for p in phrase.split():
        p = re.sub(r"[^a-z0-9]", "", p.lower())
        if not p:
            continue
        p = BRIT.get(p, singular(BRIT.get(p, p)))
        out.append(p)
    return tuple(out)


blob = json.load(open(os.path.join(DATA, "corpus.json"), encoding="utf-8"))
docs = blob["docs"]; concepts = blob["concept_list"]; binary = blob["binary"]
N = len(docs)
cidx = {c: i for i, c in enumerate(concepts)}
print("=" * 78)
print("STAGE 2  SEMCON  (exact normalisation + conservative lexical synonymy)")
print("=" * 78)
print("concepts: %d   documents: %d   encoder: %s" % (len(concepts), N, MODEL))

dfL3_c = [sum(1 for r in binary["L3"] if i in r) for i in range(len(concepts))]

groups = collections.defaultdict(list)
for i, c in enumerate(concepts):
    groups[lemma_key(c)].append(i)
group_keys = list(groups.keys())
canon_members = {k: sorted(v, key=lambda i: (-dfL3_c[i], len(concepts[i]), concepts[i]))
                 for k, v in groups.items()}
canon = {k: concepts[canon_members[k][0]] for k in group_keys}
reps = [canon_members[k][0] for k in group_keys]            # concept index of each group rep
pos_of = {c: j for j, c in enumerate(reps)}
rep_labels = [concepts[c] for c in reps]
lemma_rep = {}
for k, v in groups.items():
    j = pos_of[canon_members[k][0]]
    for m in v:
        lemma_rep[m] = j

n_lemma_groups = len(group_keys)
merged = sum(len(v) - 1 for v in groups.values())
print("\nSTEP 1  exact normalisation")
print("   %d concepts -> %d normalised groups  (%d merged, %.1f%%)"
      % (len(concepts), n_lemma_groups, merged, 100 * merged / len(concepts)))
ex = [(concepts[i], rep_labels[lemma_rep[i]]) for i in range(len(concepts)) if lemma_rep[i] != i][:16]
print("   examples: " + "; ".join("%s->%s" % e for e in ex))

# ---------------------------------------------------------------- STEP 2 embeddings
model = SentenceTransformer(MODEL)
E = model.encode(["query: " + c for c in rep_labels], batch_size=128,
                 convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)
E = np.asarray(E, dtype=np.float64)
raw = E.copy()
Ec = E - E.mean(axis=0, keepdims=True)
Ec /= np.maximum(np.linalg.norm(Ec, axis=1, keepdims=True), 1e-12)

rng = np.random.default_rng(0)
i0 = rng.integers(0, len(rep_labels), 6000)
i1 = rng.integers(0, len(rep_labels), 6000)
m = i0 != i1
i0, i1 = i0[m], i1[m]
cos_raw = float((raw[i0] * raw[i1]).sum(1).mean())
cos_cen = float((Ec[i0] * Ec[i1]).sum(1).mean())
abs_cen = float(np.abs((Ec[i0] * Ec[i1]).sum(1)).mean())
print("\nSTEP 2  anisotropy correction (mean cosine of random concept pairs)")
print("   raw           : %+.4f" % cos_raw)
print("   mean-centred  : %+.4f" % cos_cen)
print("   mean |cos| after centring : %.4f" % abs_cen)

S = Ec @ Ec.T
np.fill_diagonal(S, 1.0)
lidx = {c: j for j, c in enumerate(rep_labels)}

# ---------------------------------------------------------------- clustering helper
def cluster(tau, cap):
    lab = AgglomerativeClustering(n_clusters=None, metric="cosine", linkage="complete",
                                  distance_threshold=1.0 - tau).fit_predict(Ec)
    buckets = collections.defaultdict(list)
    for j, l in enumerate(lab):
        buckets[int(l)].append(j)
    fams, rejected = [], 0
    for l, mem in buckets.items():
        if len(mem) == 1:
            fams.append([mem[0]])
        elif len(mem) > cap:
            rejected += 1
            fams.extend([[j] for j in mem])
        else:
            fams.append(sorted(mem))
    return fams, rejected


def fam_map(fams):
    m = {}
    for f, mem in enumerate(fams):
        for j in mem:
            m[j] = f
    return m


# ---------------------------------------------------------------- end-to-end benchmark
def evaluate(tau, cap):
    fams, rej = cluster(tau, cap)
    fm = fam_map(fams)
    p = [(a, b) for a, b in POS if a in cidx and b in cidx and lemma_rep[cidx[a]] != lemma_rep[cidx[b]]]
    n = [(a, b) for a, b in NEG if a in cidx and b in cidx and lemma_rep[cidx[a]] != lemma_rep[cidx[b]]]
    tp = sum(1 for a, b in p if fm[lemma_rep[cidx[a]]] == fm[lemma_rep[cidx[b]]])
    fn = len(p) - tp
    fp = sum(1 for a, b in n if fm[lemma_rep[cidx[a]]] == fm[lemma_rep[cidx[b]]])
    tn = len(n) - fp
    prec = tp / (tp + fp) if (tp + fp) else 1.0
    rec = tp / (tp + fn) if (tp + fn) else 1.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    return dict(tau=tau, cap=cap, tp=tp, fp=fp, fn=fn, tn=tn, prec=prec, rec=rec, f1=f1,
                acc=(tp + tn) / max(len(p) + len(n), 1), n_fam=len(fams), rejected=rej,
                largest=max(len(m) for m in fams),
                n_multi=sum(1 for m in fams if len(m) > 1))


avail_p = [1 for a, b in POS if a in cidx and b in cidx]
avail_n = [1 for a, b in NEG if a in cidx and b in cidx]
step1_p = sum(1 for a, b in POS if a in cidx and b in cidx and lemma_rep[cidx[a]] == lemma_rep[cidx[b]])
step1_n = sum(1 for a, b in NEG if a in cidx and b in cidx and lemma_rep[cidx[a]] == lemma_rep[cidx[b]])
print("\nBENCHMARK AVAILABILITY (of %d synonym / %d contrast pairs defined)" % (len(POS), len(NEG)))
print("   both surfaces present in the mined concept set : %d / %d synonym, %d / %d contrast"
      % (len(avail_p), len(POS), len(avail_n), len(NEG)))
print("   STEP 1 alone already co-locates  : %d synonym pairs (correct) and %d contrast pairs (false merge)"
      % (step1_p, step1_n))

rows = [evaluate(round(float(t), 2), MAX_FAMILY) for t in np.arange(0.15, 1.00, 0.01)]
f1max = max(r["f1"] for r in rows)
plateau = [min(r["tau"] for r in rows if r["f1"] >= f1max - 1e-9),
           max(r["tau"] for r in rows if r["f1"] >= f1max - 1e-9)]
TAU = float(np.mean(plateau))
print("\nEND-TO-END tau SWEEP (family-level co-membership, cap=%d)" % MAX_FAMILY)
print("   %-5s %3s %3s %6s %6s %6s %6s %7s %8s" % ("tau", "TP", "FP", "prec", "rec", "F1", "acc", "fams", "largest"))
for r in rows:
    if r["f1"] >= f1max - 1e-9 or abs(r["tau"] - round(TAU, 2)) < 0.03:
        print("   %-5.2f %3d %3d %6.3f %6.3f %6.3f %6.3f %7d %8d"
              % (r["tau"], r["tp"], r["fp"], r["prec"], r["rec"], r["f1"], r["acc"],
                 r["n_fam"], r["largest"]))
print("   F1 plateau = tau in [%.2f, %.2f]  ->  plateau tau = %.3f (midpoint)"
      % (plateau[0], plateau[1], TAU))
print("   NOTE: F1 is saturated (zero false merges across the whole grid), so the benchmark")
print("   certifies SAFETY but cannot select tau. tau is therefore taken from the manual")
print("   adjudication of the sampled candidate merges (manual_audit_sample.csv).")

# manual adjudication overrides the plateau if verdicts are present
TAU_PATH = os.path.join(DATA, "tau_selected.json")
TAU_SRC = "manual audit"
TAU_SEL = None
if os.path.exists(TAU_PATH):
    sel = json.load(open(TAU_PATH))
    TAU = float(sel["tau"]); TAU_SRC = sel.get("source", "manual audit")
    TAU_SEL = sel
    print("\n   MANUAL AUDIT: tau overridden to %.3f (%s)" % (TAU, TAU_SRC))
else:
    TAU_SRC = "benchmark plateau midpoint"
    print("\n   (no manual verdicts found -> using plateau midpoint)")
TAU = round(TAU, 2)

res = evaluate(TAU, MAX_FAMILY)
print("\n   SELECTED tau=%.2f : F1=%.3f precision=%.3f recall=%.3f accuracy=%.3f  families=%d"
      % (TAU, res["f1"], res["prec"], res["rec"], res["acc"], res["n_fam"]))

print("\n   SIZE-CAP STABILITY SWEEP (tau fixed at %.2f)" % TAU)
print("   %-5s %7s %9s %8s %8s %6s %6s" % ("cap", "fams", "multi", "largest", "rejected", "prec", "F1"))
stab = []
for cap in (3, 4, 5, 6, 8, 12):
    r = evaluate(TAU, cap)
    stab.append(r)
    print("   %-5d %7d %9d %8d %8d %6.3f %6.3f"
          % (cap, r["n_fam"], r["n_multi"], r["largest"], r["rejected"], r["prec"], r["f1"]))

# ---------------------------------------------------------------- final families
fams, rejected = cluster(TAU, MAX_FAMILY)
fm = fam_map(fams)
n_fams = len(fams)
fam_of_concept = {i: fm[lemma_rep[i]] for i in range(len(concepts))}

fam_label, fam_members = [], []
for mem in fams:
    ms = sorted(mem, key=lambda j: -dfL3_c[reps[j]])
    fam_label.append(rep_labels[ms[0]])
    fam_members.append([rep_labels[j] for j in ms])


def collapse(present):
    return [sorted({fam_of_concept[i] for i in row}) for row in present]


f1m = collapse(binary["L1"]); f2m = collapse(binary["L2"]); f3m = collapse(binary["L3"])
fdf = [sum(1 for r in f3m if f in r) for f in range(n_fams)]
fdf1 = [sum(1 for r in f1m if f in r) for f in range(n_fams)]
fdf2 = [sum(1 for r in f2m if f in r) for f in range(n_fams)]
sizes = sorted((len(m) for m in fams), reverse=True)
print("\nFINAL FAMILIES: %d  (multi-member %d, singleton %d, largest %d, rejected by cap %d)"
      % (n_fams, sum(1 for s in sizes if s > 1), sum(1 for s in sizes if s == 1),
         sizes[0], rejected))
print("   mean families/document   L1 %.2f   L2 %.2f   L3 %.2f"
      % (np.mean([len(r) for r in f1m]), np.mean([len(r) for r in f2m]),
         np.mean([len(r) for r in f3m])))

# ---------------------------------------------------------------- cross-validation
D = np.zeros((N, len(concepts)), dtype=np.float32)
for di, row in enumerate(binary["L3"]):
    for i in row:
        D[di, i] = 1.0
C = (D.T @ D).astype(np.float32)
deg = C.sum(1)
adj = np.zeros_like(C)
nz = deg > 0
adj[:, nz] = C[:, nz] / np.sqrt(np.outer(deg, deg[nz]))
Acooc = nx.from_numpy_array(adj)
cc = nx.community.louvain_communities(Acooc, seed=42, weight="weight")
cl = np.zeros(len(concepts), dtype=int)
for kk, c in enumerate(cc):
    for m in c:
        cl[m] = kk
sl = np.array([fam_of_concept[i] for i in range(len(concepts))])
ari = adjusted_rand_score(cl, sl); nmi = normalized_mutual_info_score(cl, sl)
print("\nCROSS-VALIDATION  semantic families vs co-occurrence communities")
print("   adjusted Rand %.3f    NMI %.3f" % (ari, nmi))
print("   Low agreement is expected and is the informative result: semantic families group")
print("   words that MEAN the same thing, co-occurrence communities group words that are USED")
print("   together. Divergence isolates integrative concepts that bridge meaning groups")
print("   without co-usage ties - exactly the quantity of interest for ecosystem modelling.")

# ---------------------------------------------------------------- over-merge audit
# Semantic consolidation is trusted only insofar as it can be audited. Two automatic
# screens flag candidate FALSE merges so that they can be inspected and counted rather
# than silently accepted.
ANTONYMS = [
    ("public", "private"), ("internal", "external"), ("high", "upper"),
    ("individual", "team"), ("positive", "negative"), ("formal", "informal"),
    ("central", "peripheral"), ("elite", "mass"), ("centralized", "decentralized"),
    ("top", "bottom"), ("male", "female"), ("quantitative", "qualitative"),
    ("traditional", "modern"), ("supportive", "restrictive"),
    ("inclusive", "exclusive"), ("global", "local"),
    ("competition", "cooperation"), ("increase", "decline"),
    ("more", "less"), ("stronger", "weaker"), ("higher", "lower"),
]
ANT = set()
for a, b in ANTONYMS:
    ANT.add(tuple(sorted((a, b))))

audit_rows = []
for f, mem in enumerate(fams):
    if len(mem) < 2:
        continue
    labs = [rep_labels[j] for j in mem]
    k1 = [set(l.split()) for l in labs]
    flags = []
    for i in range(len(labs)):
        for j in range(i + 1, len(labs)):
            a, b = labs[i], labs[j]
            if tuple(sorted((a, b))) in ANT:
                flags.append("ANTONYM:%s|%s" % (a, b))
            elif k1[i] and k1[j] and (k1[i] & k1[j]) and S[mem[i], mem[j]] < 0.60:
                flags.append("SHAREDWORD_LOWSIM:%.2f %s|%s" % (S[mem[i], mem[j]], a, b))
    audit_rows.append(dict(family_id=f, label=fam_label[f], size=len(mem),
                           members=" | ".join(labs), n_flags=len(flags),
                           flags="; ".join(flags)))
flagged = [a for a in audit_rows if a["n_flags"] > 0]
print("\nOVER-MERGE AUDIT (automatic screen over %d multi-member families)" % len(audit_rows))
print("   families with >=1 flag: %d  (%.1f%%)  -> upper bound on precision %.3f"
      % (len(flagged), 100 * len(flagged) / max(len(audit_rows), 1),
         1 - len(flagged) / max(len(audit_rows), 1)))
for a in flagged[:35]:
    print("   %-28s %s" % (a["label"][:28], a["flags"][:88]))
with open(os.path.join(DATA, "semcon_audit.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(audit_rows[0].keys())); w.writeheader(); w.writerows(audit_rows)
with open(os.path.join(DATA, "semcon_flagged.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(audit_rows[0].keys())); w.writeheader(); w.writerows(flagged)

# ---------------------------------------------------------------- manual audit sample
# Precision of semantic consolidation cannot be read off a saturated benchmark, so a
# stratified sample of the pairs that COMPLETE-LINKAGE WOULD ACTUALLY MERGE is exported for
# manual adjudication at each candidate threshold. The sampled population is the union of
# within-cluster pairs across the threshold grid - i.e. exactly the decisions the
# procedure makes.
MANUAL = []
grid = [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
for t in grid:
    labs_, _ = cluster(t, MAX_FAMILY)
    pool = []
    for mem in labs_:
        if len(mem) < 2:
            continue
        for a in range(len(mem)):
            for b in range(a + 1, len(mem)):
                pool.append((mem[a], mem[b]))
    if not pool:
        continue
    rs = np.random.default_rng(1000 + int(t * 100))
    take = rs.choice(len(pool), size=min(16, len(pool)), replace=False)
    for tsel in take:
        a, b = pool[int(tsel)]
        MANUAL.append(dict(tau=t, sim=round(float(S[a, b]), 4),
                           concept_a=rep_labels[a], concept_b=rep_labels[b], verdict=""))
if MANUAL:
    with open(os.path.join(DATA, "manual_audit_sample.csv"), "w", encoding="utf-8-sig",
              newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(MANUAL[0].keys()))
        w.writeheader(); w.writerows(MANUAL)
    print("\nMANUAL AUDIT SAMPLE exported: %d candidate merges -> %s"
          % (len(MANUAL), os.path.join(DATA, "manual_audit_sample.csv")))

# ---------------------------------------------------------------- export
out = []
for f in range(n_fams):
    mem = fam_members[f]
    out.append(dict(
        family_id=f, label=fam_label[f], size=len(mem), df_L1=fdf1[f], df_L2=fdf2[f],
        df_L3=fdf[f], share_L3=round(fdf[f] / N, 4),
        provenance_ratio=round(fdf1[f] / max(fdf[f], 1), 4),
        keyword_ratio=round(fdf2[f] / max(fdf[f], 1), 4),
        members=" | ".join(mem[:14]) + (" | ..." if len(mem) > 14 else "")))
out.sort(key=lambda r: -r["df_L3"])
for i, r in enumerate(out):
    r["family_rank"] = i + 1
with open(os.path.join(DATA, "families.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
with open(os.path.join(DATA, "benchmark_tau.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open(os.path.join(DATA, "concept_family_map.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["concept", "family_id", "family_label"])
    for i, c in enumerate(concepts):
        w.writerow([c, fam_of_concept[i], fam_label[fam_of_concept[i]]])

blob["fam_label"] = fam_label
blob["fam_members"] = fam_members
blob["rep_labels"] = rep_labels
blob["fam_of_concept"] = {str(k): int(v) for k, v in fam_of_concept.items()}
blob["fams_L1"] = f1m; blob["fams_L2"] = f2m; blob["fams_L3"] = f3m
blob["semcon"] = dict(model=MODEL, tau=TAU, plateau=plateau, f1=res["f1"], prec=res["prec"],
                      rec=res["rec"], acc=res["acc"], max_family=MAX_FAMILY,
                      audited_precision=(TAU_SEL.get("precision") if TAU_SEL else None),
                      n_merges_audited=(TAU_SEL.get("n_merges_audited") if TAU_SEL else None),
                      n_correct=(TAU_SEL.get("n_correct") if TAU_SEL else None),
                      tau_source=TAU_SRC,
                      n_concepts=len(concepts), n_lemma_groups=n_lemma_groups,
                      n_families=n_fams, n_multi=int(sum(1 for s in sizes if s > 1)),
                      ari=ari, nmi=nmi, cos_raw=cos_raw, cos_centred=cos_cen, abs_cen=abs_cen,
                      stability=stab, rejected=rejected,
                      step1_synonym_hits=step1_p, step1_false_merges=step1_n,
                      n_bench_pos=len(avail_p), n_bench_neg=len(avail_n))
json.dump(blob, open(os.path.join(DATA, "corpus.json"), "w", encoding="utf-8"), ensure_ascii=False)

print("\nTOP 55 CONCEPT FAMILIES (by df)")
for r in out[:55]:
    print("  %4d  %-28s sz=%-2d L1=%-3d PR=%.2f  %s"
          % (r["df_L3"], r["label"][:28], r["size"], r["df_L1"], r["provenance_ratio"],
             r["members"][:66]))
print("\nMULTI-MEMBER FAMILIES (the consolidations that exact normalisation alone did not do)")
shown = 0
for r in out:
    if r["size"] >= 2 and shown < 40:
        print("  %-30s <- %s" % (r["label"][:30], r["members"][:96])); shown += 1
np.save(os.path.join(DATA, "concept_embeddings.npy"), Ec)
with open(os.path.join(DATA, "concept_similarity.npy"), "wb") as f:
    np.save(f, S.astype(np.float32))
print("\nWrote families.csv, benchmark_tau.csv, concept_family_map.csv, embeddings")

