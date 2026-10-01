"""
ARTICLE 1 - master runner. Executes the full pipeline in order.
Usage:  python run_all.py
"""
import subprocess, sys, os, time

HERE = os.path.dirname(os.path.abspath(__file__))
STAGES = [
    ("s0_corpus.py", "corpus construction + query-artefact diagnostics"),
    ("s1_concepts.py", "POS-aware concept extraction"),
    ("s2_semcon.py", "SEMCON concept-family consolidation"),
    ("s2c_verdicts.py", "manual audit -> tau decision"),
    ("s3_network.py", "co-occurrence network + null models"),
    ("s4_topics.py", "UMAP + HDBSCAN topic model"),
    ("s5_multiplex.py", "three-pillar multiplex + supra centrality"),
    ("s6_temporal.py", "temporal + cross-national"),
    ("s7_figures.py", "figures"),
]

PY = sys.executable
t_all = time.time()
for script, desc in STAGES:
    p = os.path.join(HERE, script)
    t0 = time.time()
    print("\n" + "#" * 78)
    print("# %-22s  %s" % (script, desc))
    print("#" * 78, flush=True)
    r = subprocess.run([PY, p], capture_output=True, text=True, cwd=HERE)
    if r.returncode != 0:
        print(r.stdout[-4000:])
        print(r.stderr[-4000:])
        print("\nFAILED at %s (exit %d)" % (script, r.returncode))
        sys.exit(1)
    tail = [l for l in r.stdout.splitlines()
            if l.strip() and not l.startswith("   draw")]
    print("\n".join(tail[-14:]))
    print("   [ok %.0fs]" % (time.time() - t0), flush=True)
print("\n" + "=" * 78)
print("PIPELINE COMPLETE in %.0f s" % (time.time() - t_all))
print("=" * 78)
