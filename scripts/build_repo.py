"""Assemble the public repository, excluding all Scopus-derived content."""
import os, shutil, glob, sys

SRC = r"D:\Uni of Birjand\articles\adel"
A1 = os.path.join(SRC, "article1")
DST = os.path.join(SRC, "repo_build")

# Scopus-derived content that must NEVER be committed
FORBIDDEN_NAMES = {"data.csv", "corpus.json", "corpus_meta.csv", "tau_selected.json",
                   "concepts.csv", "families.csv", "concept_family_map.csv",
                   "network_edges.csv", "concept_embeddings.npy", "concept_similarity.npy",
                   "doc_embeddings.npy", "doc_umap.npy", "concepts.csv"}
FORBIDDEN_EXT = {".npy"}

copied, skipped = [], []


def copy_file(src, dst):
    base = os.path.basename(src)
    ext = os.path.splitext(base)[1].lower()
    if base in FORBIDDEN_NAMES or ext in FORBIDDEN_EXT:
        skipped.append(base)
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    copied.append(os.path.relpath(dst, DST))


# 1. analysis pipeline
for f in sorted(glob.glob(os.path.join(A1, "scripts", "*.py"))):
    copy_file(f, os.path.join(DST, "scripts", os.path.basename(f)))

# 2. tables (result outputs)
for f in sorted(glob.glob(os.path.join(A1, "tables", "*.csv"))):
    copy_file(f, os.path.join(DST, "tables", os.path.basename(f)))

# 3. figures
for f in sorted(glob.glob(os.path.join(A1, "figures", "*.png"))):
    copy_file(f, os.path.join(DST, "figures", os.path.basename(f)))

# 4. manuscript
for f in ["Article1_manuscript.docx", "Article1_manuscript_outline.docx"]:
    p = os.path.join(A1, f)
    if os.path.exists(p):
        copy_file(p, os.path.join(DST, "manuscript", f))

# 5. verification / audit files that support validation claims
VER = os.path.join(DST, "verification")
for f in sorted(glob.glob(os.path.join(A1, "data", "*"))):
    b = os.path.basename(f)
    if b in FORBIDDEN_NAMES or os.path.splitext(b)[1].lower() in FORBIDDEN_EXT:
        continue
    # manual audit: contains concept pairs + verdicts (no bibliographic records)
    if b == "manual_audit_sample.csv":
        copy_file(f, os.path.join(VER, b))

# 6. consolidated results summary
copy_file(os.path.join(A1, "scripts", "s8_summary.py"),
          os.path.join(DST, "scripts", "s8_summary.py"))

print("=" * 70)
print("REPOSITORY ASSEMBLY")
print("=" * 70)
print("copied %d files" % len(copied))
for c in sorted(copied):
    print("   %s" % c)
print()
print("EXCLUDED (Scopus-licence / derived-from-record-text): %d" % len(skipped))
for s in sorted(set(skipped)):
    print("   %s" % s)

# final safety sweep: fail loudly if anything forbidden survived
leaked = []
for root, _, files in os.walk(DST):
    if ".git" in root:
        continue
    for f in files:
        if f in FORBIDDEN_NAMES or os.path.splitext(f)[1].lower() in FORBIDDEN_EXT:
            leaked.append(os.path.join(root, f))
if leaked:
    print("\n*** LEAK CHECK FAILED ***")
    for l in leaked:
        print("   %s" % l)
    sys.exit(1)
print("\nleak check: clean (no Scopus records or record-derived binaries present)")