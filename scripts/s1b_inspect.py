import csv, os, collections
B = r"D:\Uni of Birjand\articles\adel\article1"
rows = list(csv.DictReader(open(os.path.join(B, "data", "concepts.csv"), encoding="utf-8-sig")))
print("TOTAL", len(rows))
print("\n--- ALL MULTIWORD CONCEPTS ---")
for r in rows:
    if int(r["n"]) > 1:
        print("  %4s  %-42s  L1=%3s L2=%3s  llr=%s" % (r["df"], r["concept"], r["df_L1"], r["df_L2"], r["llr"]))
print("\n--- UNIGRAMS df 5-19 (the long tail that will be consolidated/filtered) ---")
tail = [r for r in rows if int(r["n"]) == 1 and int(r["df"]) <= 19]
print("count:", len(tail))
print("  " + ", ".join(r["concept"] for r in tail))
print("\n--- UNIGRAMS df 20-60 ---")
mid = [r for r in rows if int(r["n"]) == 1 and 20 <= int(r["df"]) <= 60]
print("count:", len(mid))
print("  " + ", ".join(r["concept"] for r in mid))
