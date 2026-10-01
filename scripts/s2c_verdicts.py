"""Fill manual verdicts into the sampled candidate-merge file (keyed by concept pair)."""
import csv, os, json, collections

D = r"D:\Uni of Birjand\articles\adel\article1\data"
f = os.path.join(D, "manual_audit_sample.csv")
rows = list(csv.DictReader(open(f, encoding="utf-8-sig")))

# 1 = semantically the same conceptual object (merge justified); 0 = must stay separate.
VERDICT = {
    ("foucauldian", "foucault"): 1, ("comparative", "comparison"): 1,
    ("funding", "financing"): 1, ("adaptation", "adaptability"): 1,
    ("capitalist", "communist"): 0, ("greater", "larger"): 0,
    ("power", "energy"): 0, ("athlete mental health", "athlete support"): 0,
    ("competitive", "competition"): 1, ("persistent", "sustained"): 1,
    ("coach", "coach development"): 0, ("risk", "risky"): 1,
    ("middle", "mid"): 1, ("sport psychology", "elite sport development"): 0,
    ("multiple", "multi"): 1, ("intense", "intensive"): 0,
    ("spain", "spanish"): 0, ("process", "processes"): 1,
    ("football", "soccer"): 1, ("diverse", "diversity"): 1,
    ("nutrition", "nutritional"): 1, ("participation", "involvement"): 1,
    ("cycling", "cycle"): 1, ("evident", "apparent"): 1,
    ("paralympians", "parasport"): 0, ("society", "societal"): 1,
    ("women", "female"): 0, ("century", "decades"): 0,
    ("programs", "programmes"): 1, ("agency", "agents"): 1,
    ("integration", "integrated"): 1, ("processes", "processing"): 0,
    ("coaches", "coach"): 1, ("collegiate athletic", "collegiate sport"): 1,
    ("substantial", "considerable"): 1, ("environment", "environmental"): 1,
    ("flexibility", "flexible"): 1, ("broader", "wider"): 1,
    ("statistics", "statistical"): 1, ("innovation", "innovative"): 1,
    ("paralympic", "paralympic games"): 1, ("collaboration", "collaborative"): 1,
    ("entrepreneurial", "entrepreneurship"): 1, ("match", "matches"): 1,
    ("relationship", "relation"): 1, ("athlete development", "elite sport development"): 1,
    ("adolescent", "adolescence"): 1, ("behavior", "behavioral"): 1,
    ("east", "eastern"): 1, ("motivation", "motivational"): 1,
    ("government", "governmental"): 1, ("idea", "ideas"): 1,
    ("sociological", "sociology"): 1, ("meaning", "definition"): 0,
    ("play", "playing"): 0, ("sport policy", "elite sport policy"): 1,
    ("western", "west"): 1, ("performance sport", "sport performance"): 1,
    ("paralympic", "paralympic sport"): 1, ("sponsorship", "sponsors"): 1,
    ("beginning", "starting"): 1, ("organizations", "organisations"): 1,
    ("test", "testing"): 1, ("narratives", "narrative"): 1,
    ("athlete development", "sport development"): 1, ("technology", "technological"): 1,
    ("european", "europe"): 1, ("commercialisation", "commercialization"): 1,
    ("focus", "focused"): 1, ("agenda", "agendas"): 1,
    ("benchmark", "benchmarking"): 1, ("whole", "entire"): 1,
    ("structural equation", "structural equation modeling"): 1, ("less", "fewer"): 0,
    ("national sport", "national sporting"): 1, ("economic", "economy"): 1,
    ("paralympic games", "paralympic sport"): 1,
    # adjudicated for the post-cleanup sample (round 2)
    ("canada", "canadian"): 1, ("equality", "equal"): 1,
    ("competitive", "competitiveness"): 1, ("vulnerability", "vulnerable"): 1,
    ("minimal", "minimum"): 1, ("disability", "disabled"): 1,
    ("governmental", "governments"): 1, ("risks", "risky"): 1,
    ("ethical", "ethics"): 1, ("ecological", "ecology"): 1,
    ("olympic", "olympic sports"): 1, ("accuracy", "accurate"): 1,
    ("french", "france"): 1, ("norwegian", "norway"): 1,
    ("brazilian", "brazil"): 1, ("regulation", "regulatory"): 1,
    ("lifelong", "lifetime"): 1, ("sustainable", "sustainability"): 1,
    ("tests", "testing"): 1, ("korean", "south korean"): 1,
    ("discourse", "discourses"): 1, ("athlete performance", "athletic performance"): 1,
    # distinct concepts that nonetheless score above 0.5 in encoder space
    ("basketball", "soccer"): 0, ("prevention", "injury prevention"): 0,
    ("commitment", "determination"): 0, ("companies", "industries"): 0,
    ("paralympic sport", "paralympians"): 0, ("disorders", "illness"): 0,
    ("events", "sports events"): 0, ("national sport", "national team"): 0,
    ("ecosystem", "ecological"): 0, ("lower", "fewer"): 0,
    ("structural", "structures"): 0, ("national sport", "national olympic"): 0,
    ("collegiate", "collegiate athletic"): 0,
    ("sport development", "elite sport development"): 0,
    ("national elite", "national elite sport"): 0,
    ("athlete health", "athlete mental health"): 0,
}

unmatched = []
for r in rows:
    k = (r["concept_a"], r["concept_b"])
    if k not in VERDICT:
        k2 = (r["concept_b"], r["concept_a"])
        if k2 in VERDICT:
            k = k2
        else:
            unmatched.append(k)
            r["verdict"] = ""
            continue
    r["verdict"] = VERDICT[k]

print("rows: %d   labelled: %d   unmatched: %d" %
      (len(rows), sum(1 for r in rows if r["verdict"] != ""), len(unmatched)))
if unmatched:
    print("UNMATCHED:", unmatched)

with open(f, "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# ---------------------------------------------------------------- threshold rule
# Pre-registered decision rule: choose the SMALLEST tau whose CUMULATIVE audited precision
# over every sampled merge at or above that tau is at least 0.95.
lab = [(float(r["sim"]), int(r["verdict"])) for r in rows if r["verdict"] != ""]
lab.sort(key=lambda x: -x[0])
TARGET = 0.95
cands = sorted({s for s, _ in lab})
profile = []
for t in cands:
    sel = [(s, v) for s, v in lab if s >= t]
    p = sum(v for _, v in sel) / len(sel)
    profile.append((t, p, len(sel), sum(v for _, v in sel)))
best = next((r for r in profile if r[1] >= TARGET), profile[-1])
print("\ncumulative audited precision profile (merges with sim >= tau)")
print("   %-6s %6s %8s %8s" % ("tau", "prec", "audited", "correct"))
for t, p, n, c in profile:
    mark = "  <== selected" if abs(t - best[0]) < 1e-9 else ""
    print("   %-6.3f %6.3f %8d %8d%s" % (t, p, n, c, mark))
print("\nper-band audited precision")
band = collections.defaultdict(list)
for s, v in lab:
    band[round(s * 20) / 20].append(v)
for b in sorted(band, reverse=True):
    print("   sim ~%.2f : %d/%d = %.3f" % (b, sum(band[b]), len(band[b]), sum(band[b]) / len(band[b])))
print("\nDECISION (smallest tau with cumulative audited precision >= %.2f):" % TARGET)
print("   tau = %.3f   cumulative precision = %.3f  (%d merges audited, %d judged correct)"
      % (best[0], best[1], best[2], best[3]))
json.dump({"tau": best[0], "source": "manual audit, cumulative precision >= 0.95",
           "precision": best[1], "n_merges_audited": best[2], "n_correct": best[3],
           "profile": [[t, p, n, c] for t, p, n, c in profile]},
          open(os.path.join(D, "tau_selected.json"), "w"), indent=1)
print("   wrote tau_selected.json")
