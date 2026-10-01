import json, os, numpy as np
B = r"D:\Uni of Birjand\articles\adel\article1"
D = os.path.join(B, "data")
blob = json.load(open(os.path.join(D, "corpus.json"), encoding="utf-8"))
S = np.load(os.path.join(D, "concept_similarity.npy"))
cons = blob["concept_list"]
nf = len(blob["fam_label"])
fam_of = {int(k): v for k, v in blob["fam_of_concept"].items()}
# representative labels of families (one per family) -> sample in FAMILY space
labels = blob["fam_label"]
print("families:", nf)

rng = np.random.default_rng(2024)
pairs = []
# stratified sample across the similarity range
edges = [(i, j) for i in range(nf) for j in range(i + 1, nf)]
print("total possible pairs:", len(edges))
idx = rng.choice(len(edges), size=4000, replace=False)
cand = [edges[t] for t in idx]
sims = np.array([S[i, j] for i, j in cand])
bands = [(0.20, 0.40), (0.40, 0.55), (0.55, 0.65), (0.65, 0.75), (0.75, 0.85), (0.85, 1.01)]
take = []
for lo, hi in bands:
    k = np.where((sims >= lo) & (sims < hi))[0]
    k = rng.permutation(k)[:20]
    take.extend(k.tolist())
take = sorted(set(take))
print("sampled %d pairs across %d similarity bands" % (len(take), len(bands)))
rows = []
for t in take:
    i, j = cand[t]
    rows.append((round(float(sims[t]), 3), labels[i], labels[j]))
for s, a, b in rows:
    print("%6.3f  %-34s %-34s" % (s, a[:34], b[:34]))
json.dump([list(r) for r in rows], open(os.path.join(D, "manual_audit_sample.json"), "w"), indent=0)
