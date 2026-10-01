"""
ARTICLE 1 - Stage 4: embedding-based topic model (UMAP + HDBSCAN) with c-TF-IDF labels.

Recent-technique choices and why they matter for a 604-document corpus:
  * Document embeddings from a contrastive sentence encoder rather than a bag of words,
    so that near-synonymous phrasing is not split across topics.
  * UMAP to a low-dimensional manifold, then density-based HDBSCAN rather than k-means.
    HDBSCAN discovers an appropriate number of topics and, crucially, EMITS A NOISE CLUSTER.
    In a bibliometric corpus the noise cluster is not a nuisance: documents that belong to
    no coherent theme are evidence of genuine heterogeneity, and reporting the share is
    more honest than forcing every document into a topic.
  * Topics are described with c-TF-IDF over the SEMCON concept families (not raw tokens),
    so topic labels are expressed in the same vocabulary as the co-occurrence network, and
    by a log-odds-ratio contrastive score with an informative Dirichlet prior, which is
    better behaved than raw frequency for small clusters.
  * STABILITY is measured: HDBSCAN is re-fitted on bootstrap resamples and the adjusted
    Rand index of the co-assignment matrices is reported. Topic models that are unstable
    should not be interpreted, and saying so with a number is the point.
"""
import os, json, csv, math, collections, random, sys
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import numpy as np
from sentence_transformers import SentenceTransformer
import transformers
transformers.utils.logging.disable_progress_bar()
transformers.utils.logging.set_verbosity_error()
import umap
from sklearn.cluster import HDBSCAN
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.feature_extraction.text import CountVectorizer
from statsmodels.stats.multitest import multipletests

BASE = r"D:\Uni of Birjand\articles\adel\article1"
DATA, TAB = os.path.join(BASE, "data"), os.path.join(BASE, "tables")
MODEL = "intfloat/e5-base-v2"
W0, W1 = 2013, 2025
MIN_CLUSTER = 12
N_COMPONENTS = 5
random.seed(11); np.random.seed(11)

blob = json.load(open(os.path.join(DATA, "corpus.json"), encoding="utf-8"))
docs = blob["docs"]; lab = blob["fam_label"]; f3m = blob["fams_L3"]
fam_of = {int(k): v for k, v in blob["fam_of_concept"].items()}

sel = [i for i, d in enumerate(docs) if W0 <= d["year"] <= W1]
print("=" * 78)
print("STAGE 4  EMBEDDING TOPIC MODEL  (UMAP + HDBSCAN + c-TF-IDF)")
print("=" * 78)
print("documents in %d-%d : %d" % (W0, W1, len(sel)))
texts = [docs[i]["title"] + ". " + " ; ".join(docs[i]["author_keywords"]) + ". " +
         docs[i]["abstract"] for i in sel]
fam_sets = [sorted({fam_of[c] for c in f3m[i]}) for i in sel]

# ---------------------------------------------------------------- embeddings
model = SentenceTransformer(MODEL)
E = model.encode(["passage: " + t for t in texts], batch_size=32, convert_to_numpy=True,
                 normalize_embeddings=True, show_progress_bar=False)
E = np.asarray(E, dtype=np.float32)
E = E - E.mean(0, keepdims=True)
E /= np.maximum(np.linalg.norm(E, axis=1, keepdims=True), 1e-9)
print("document embeddings: %s (mean-centred)" % (E.shape,))

# ---------------------------------------------------------------- UMAP
red = umap.UMAP(n_components=N_COMPONENTS, n_neighbors=15, min_dist=0.0,
                metric="cosine", random_state=11, verbose=False)
Eu = red.fit_transform(E)
print("UMAP manifold: %s" % (Eu.shape,))

# ---------------------------------------------------------------- HDBSCAN + parameter selection
grid = [(m, mcs) for m in (5, 8, 10) for mcs in (12, 15, 20)]
cand = []
for m, mcs in grid:
    hc = HDBSCAN(min_cluster_size=mcs, min_samples=m, metric="euclidean",
                 cluster_selection_method="eom").fit(Eu)
    lb = hc.labels_
    k = len(set(lb)) - (1 if -1 in lb else 0)
    noise = (lb == -1).mean()
    sizes = collections.Counter(lb[lb >= 0])
    ok = (k >= 4 and k <= 20 and noise < 0.45 and (min(sizes.values()) if sizes else 0) >= 8)
    sil = -1.0
    if k >= 2 and noise < 0.6:
        try:
            sil = float(silhouette_score(Eu[lb >= 0], lb[lb >= 0]))
        except Exception:
            pass
    cand.append(dict(min_samples=m, min_cluster_size=mcs, n_topics=k,
                     noise=round(float(noise), 4), silhouette=round(sil, 4),
                     min_size=min(sizes.values()) if sizes else 0, valid=ok))
print("\nHDBSCAN PARAMETER GRID")
print("   %-4s %-5s %-5s %-8s %-8s %-8s %s" % ("ms", "mcs", "K", "noise", "silhou", "minsize", "ok"))
for c in cand:
    print("   %-4d %-5d %-5d %-8.3f %-8.3f %-8d %s"
          % (c["min_samples"], c["min_cluster_size"], c["n_topics"], c["noise"],
             c["silhouette"], c["min_size"], "YES" if c["valid"] else ""))
val = [c for c in cand if c["valid"]]
pick = max(val, key=lambda c: (c["silhouette"], -abs(c["n_topics"] - 9))) if val else \
    max(cand, key=lambda c: c["silhouette"])
print("   SELECTED min_samples=%d min_cluster_size=%d -> %d topics, noise %.1f%%, silhouette %.3f"
      % (pick["min_samples"], pick["min_cluster_size"], pick["n_topics"],
         100 * pick["noise"], pick["silhouette"]))

hc = HDBSCAN(min_cluster_size=pick["min_cluster_size"], min_samples=pick["min_samples"],
             metric="euclidean", cluster_selection_method="eom").fit(Eu)
T = hc.labels_
topics = sorted(set(int(x) for x in T if x != -1))
print("   realised %d topics + noise cluster (%.1f%% of documents, n=%d)"
      % (len(topics), 100 * (T == -1).mean(), (T == -1).sum()))

# ---------------------------------------------------------------- c-TF-IDF over families
nf = len(lab)
rows_tf = np.zeros((len(topics), nf))
for t_i, t in enumerate(topics):
    m = T == t
    for i in np.nonzero(m)[0]:
        for f in fam_sets[i]:
            rows_tf[t_i, f] += 1
df_fam = np.zeros(nf)
for fs in fam_sets:
    for f in fs:
        df_fam[f] += 1
A = len(topics)
c_tfidf = np.zeros_like(rows_tf)
for t_i in range(A):
    tot = rows_tf[t_i].sum()
    if tot == 0:
        continue
    c_tfidf[t_i] = (rows_tf[t_i] / tot) * np.log(1 + A / np.maximum(df_fam, 1))

# ---------------------------------------------------------------- label masking
# Topic labels are only interpretable if the labelling vocabulary is itself specific.
# The same specificity window used for the co-occurrence network (frequent enough to be
# real, rare enough to be informative) is applied here, so ubiquitous filler such as
# "end", "great", "certain" cannot win a c-TF-IDF argument merely by being everywhere.
df_arr = df_fam
LABEL_MIN_DF = 10
LABEL_MAX_SHARE = 0.30
label_mask = (df_arr >= LABEL_MIN_DF) & (df_arr / len(sel) <= LABEL_MAX_SHARE)
print("\nlabel vocabulary restricted to specificity window: df>=%d and df/N<=%.2f  -> %d of %d families"
      % (LABEL_MIN_DF, LABEL_MAX_SHARE, int(label_mask.sum()), nf))
c_lab = np.where(label_mask[None, :], c_tfidf, -np.inf)
k_lab = np.where(label_mask[None, :], contrast[t], -np.inf) if False else None

# ---------------------------------------------------------------- contrastive log-odds
# Monroe et al. (2008) z-scored log-odds ratio with an informative Dirichlet prior.
PRIOR = 50.0
alpha0 = PRIOR * np.maximum(df_fam, 1) / max(df_fam.sum(), 1) * 1.0
alpha0 = np.maximum(alpha0, 1e-6)
contrast = {}
for t_i, t in enumerate(topics):
    a = rows_tf[t_i] + alpha0
    b = (rows_tf.sum(0) - rows_tf[t_i]) + alpha0
    la = np.log(a / a.sum())
    lb = np.log(b / b.sum())
    contrast[t] = np.where(label_mask, la - lb, -np.inf)

members_of = {t: collections.Counter() for t in topics}
for t in topics:
    for i in np.nonzero(T == t)[0]:
        for f in fam_sets[i]:
            members_of[t][f] += 1

years = [docs[i]["year"] for i in sel]
noise_idx = [i for i in np.nonzero(T == -1)[0]]
print("\nTOPIC PROFILES")
topic_rows = []
for t in topics:
    n_t = int((T == t).sum())
    top_c = np.argsort(-c_lab[t])[:8]
    names = [lab[f] for f in top_c]
    con = contrast[t]
    top_k = np.argsort(-con)[:8]
    con_names = [lab[f] for f in top_k]
    my = [years[i] for i in np.nonzero(T == t)[0]]
    mpy = float(np.mean(my))
    lead = collections.Counter()
    for i in np.nonzero(T == t)[0]:
        c = docs[i]["lead_country"]
        if c:
            lead[c] += 1
    lc = ", ".join("%s(%d)" % (c, n) for c, n in lead.most_common(3))
    print("\n  TOPIC %d  n=%3d  (%.1f%% of corpus)  mean year %.1f"
          % (t, n_t, 100 * n_t / len(T), mpy))
    print("     c-TF-IDF      : %s" % ", ".join(names))
    print("     contrastive   : %s" % ", ".join(con_names))
    print("     lead countries: %s" % lc)
    topic_rows.append(dict(
        topic=t, n=n_t, share=round(n_t / len(T), 4), mean_year=round(mpy, 2),
        label=" / ".join(names[:4]), contrastive=" / ".join(con_names[:5]),
        ctfidf=" | ".join(names), contrast=" | ".join(con_names),
        lead_countries=lc,
        members="; ".join(docs[sel[i]]["title"][:90] for i in np.nonzero(T == t)[0][:4])))

# ---------------------------------------------------------------- stability
print("\nTOPIC STABILITY  (bootstrap resampling, %d replicates)" % 12)
aris = []
for b in range(12):
    idx = np.random.default_rng(500 + b).choice(len(T), size=len(T), replace=True)
    if len(set(T[idx])) - (1 if -1 in T[idx] else 0) < 2:
        continue
    sub = HDBSCAN(min_cluster_size=pick["min_cluster_size"], min_samples=pick["min_samples"],
                  metric="euclidean", cluster_selection_method="eom").fit(Eu[idx])
    lb = sub.labels_
    a_mask = (T != -1) & (lb != -1)
    if len(set(T[idx][a_mask])) < 2 or len(set(lb[a_mask])) < 2:
        continue
    aris.append(adjusted_rand_score(T[idx][a_mask], lb[a_mask]))
print("   co-assignment ARI across %d replicates: mean %.3f  sd %.3f  min %.3f  max %.3f"
      % (len(aris), np.mean(aris), np.std(aris), min(aris), max(aris)))
stab = dict(mean=float(np.mean(aris)), sd=float(np.std(aris)), min=float(min(aris)),
            max=float(max(aris)), replicates=len(aris))

with open(os.path.join(TAB, "T4_topics.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(topic_rows[0].keys())); w.writeheader(); w.writerows(topic_rows)
with open(os.path.join(DATA, "topic_labels.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["doc_id", "year", "topic", "topic_label", "lead_country", "title"])
    for i, gi in enumerate(sel):
        w.writerow([gi, docs[gi]["year"], int(T[i]),
                    "NOISE" if T[i] == -1 else topic_rows[[r["topic"] for r in topic_rows].index(T[i])]["label"],
                    docs[gi]["lead_country"] or "", docs[gi]["title"][:200]])

blob["topics"] = dict(
    model=MODEL, window=[W0, W1], n_docs=len(sel), n_topics=len(topics),
    noise_share=round(float((T == -1).mean()), 4),
    params=dict(min_samples=pick["min_samples"], min_cluster_size=pick["min_cluster_size"],
                n_components=N_COMPONENTS, n_neighbors=15),
    silhouette=pick["silhouette"], stability=stab,
    profiles=[dict(topic=r["topic"], n=r["n"], label=r["label"]) for r in topic_rows],
    assignment={str(sel[i]): int(T[i]) for i in range(len(sel))})
json.dump(blob, open(os.path.join(DATA, "corpus.json"), "w", encoding="utf-8"),
          ensure_ascii=False, default=float)
np.save(os.path.join(DATA, "doc_embeddings.npy"), E)
np.save(os.path.join(DATA, "doc_umap.npy"), Eu)
print("\nWrote T4_topics.csv, topic_labels.csv, doc_embeddings.npy, doc_umap.npy")
