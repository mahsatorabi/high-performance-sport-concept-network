import json, os
B = r"D:\Uni of Birjand\articles\adel\article1"
d = json.load(open(os.path.join(B, "data", "corpus.json"), encoding="utf-8"))
docs = d["docs"]
ne = [x for x in docs if x["language"] not in ("English", "")]
print("non-English:", len(ne))
inwin = [x for x in docs if 2013 <= x["year"] <= 2025 and x["language"] not in ("English", "")]
print("non-English within 2013-2025:", len(inwin))
import re
lat = sum(1 for x in inwin if re.search(r"[a-z]", x["abstract"]))
print("non-English w/ ascii-letter abstracts:", lat)
for x in inwin[:6]:
    print("\n---", x["language"], x["year"], "|", x["source"][:60])
    print("T:", x["title"][:150])
    print("A:", x["abstract"][:280])
