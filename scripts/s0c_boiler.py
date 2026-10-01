import json, re, os, collections
B = r"D:\Uni of Birjand\articles\adel\article1"
d = json.load(open(os.path.join(B, "data", "corpus.json"), encoding="utf-8"))
docs = d["docs"]
PATS = [
 r"downloaded by", r"Taylor\s*&\s*Francis", r"under exclusive license", r"All rights reserved",
 r"Copyright\s+20\d\d", r"\u00a9", r"Elsevier", r"Springer Nature", r"Wiley", r"SAGE Publications",
 r"Cambridge University Press", r"Taylor and Francis", r"permission of", r"Republic of all rights",
 r"open access article", r"This article is", r"See discussions", r"reviews:",
]
for p in PATS:
    c = sum(1 for x in docs if re.search(p, x["abstract"], re.I))
    if c:
        print("%-40s %4d docs" % (p, c))
print()
# print tail of 6 abstracts from T&F and Springer-heavy publishers
for p in ["Taylor and Francis", "Springer", "Routledge", "SAGE"]:
    sel = [x for x in docs if p.lower() in (x["publisher"] or "").lower()][:2]
    for x in sel:
        print("\n### %s | %s" % (p, x["source"][:50]))
        print("TAIL:", x["abstract"][-420:])
