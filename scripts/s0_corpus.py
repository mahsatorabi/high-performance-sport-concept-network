"""
ARTICLE 1 - Stage 0: Corpus construction, layered design, and query-artifact diagnostics.

Design decisions implemented here (these are the methodological claims of the paper):
  D1  Layered corpus (Evidence Ladder): L1=title, L2=title+author keywords, L3=title+kw+abstract.
      Every downstream concept statistic is computed on all three layers, enabling the
      Concept Stratification Stability (CSS) statistic defined in stage 2.
  D2  Query-artifact suppression. The corpus was retrieved with a single Boolean query whose
      terms ("sport", "elite sport", "athlete", ...) are therefore present in a degenerate
      share of documents. Terms from the query string are flagged and EXCLUDED from candidate
      concept mining, but retained as a "domain core" set for document normalisation.
  D3  Analysis window. Scopus indexing of 2026 is incomplete (retrieved 30.09.2026), so all
      temporal inference is restricted to 2013-2025. Pre-2013 records are retained for
      descriptive purposes only.
  D4  Document hygiene. Retracted/erratum/editorial/note records are excluded; the exclusion
      count is reported rather than silently applied.
"""
import csv, json, re, os, sys, collections, hashlib

csv.field_size_limit(10**9)

BASE = r"D:\Uni of Birjand\articles\adel\article1"
SRC = r"D:\Uni of Birjand\articles\adel\data.csv"
OUT = os.path.join(BASE, "data")
os.makedirs(OUT, exist_ok=True)

QUERY = (
    '( "sport ecosystem" OR "sport system" OR "sport network" OR "sport value chain" '
    'OR "innovation ecosystem" OR "entrepreneurial ecosystem" ) AND '
    '( "elite sport" OR "high performance sport" OR "professional sport" OR "athlete*" )'
)
QUERY_TERMS = [
    "sport ecosystem", "sport system", "sport network", "sport value chain",
    "innovation ecosystem", "entrepreneurial ecosystem",
    "elite sport", "high performance sport", "professional sport", "athlete",
]

KEEP_TYPES = {"Article", "Review", "Conference paper", "Book chapter", "Book"}
EXCL_TYPES = {"Retracted", "Erratum", "Editorial", "Note"}

WINDOW_START, WINDOW_END = 2013, 2025


def clean(s):
    if s is None:
        return ""
    s = s.replace("\xa0", " ")
    if "�" in s:  # mojibake replacement char introduced by the CSV export
        s = s.replace("�", "'")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# Scopus appends publisher licence/copyright notices to a large share of abstracts. These
# strings are lexical noise that would otherwise become high-frequency "concepts"
# (e.g. "taylor francis", "rights reserved"). Strip them before any text mining.
BOILER = [
    r"[©�]\s*((?:19|20)\d{2}\b|The Author)",
    r"All rights reserved",
    r"This article is downloaded by",
    r"under exclusive license to",
    r"Distributed under the terms of the Creative Commons",
    r"Creative Commons Attribution",
    r"Article (?:copy|available) under (?:the )?terms",
    r"See discussions, stats, and other related tools",
    r"Reviews: \d+",
]
BOILER_RE = re.compile("|".join(BOILER), re.I)
TITLE_TRANSL_RE = re.compile(r"\s*\[(?:DIRITTI|AN|ALYSIS|An|SCHWITZUNG|BARRESTUDY|COMUNICACI)[\s\S]{0,400}?\]\s*")


def strip_boiler(abstract):
    m = BOILER_RE.search(abstract)
    if m:
        abstract = abstract[:m.start()]
    return re.sub(r"\s+", " ", abstract).strip()


def norm_country(a):
    a = a.strip()
    if "," not in a:
        return None
    c = a.split(",")[-1].strip()
    c = re.sub(r"\s*\d+\s*$", "", c).strip()
    return c or None


rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig", newline="")))
n_raw = len(rows)

# ---------------------------------------------------------------- D4 hygiene
excl_type = collections.Counter()
kept = []
for r in rows:
    dt = clean(r.get("Document Type"))
    if dt in EXCL_TYPES or dt not in KEEP_TYPES:
        excl_type[dt or "(blank)"] += 1
        continue
    kept.append(r)

# year filter: keep pre-window records flagged, do not drop (used descriptively)
docs = []
for r in kept:
    yr = clean(r.get("Year"))
    try:
        yr = int(yr)
    except ValueError:
        yr = 0
    title = clean(r.get("Title"))
    abstr = strip_boiler(clean(r.get("Abstract")))
    title = clean(TITLE_TRANSL_RE.sub("", title)) or title
    if not title or len(abstr) < 80:
        excl_type["(missing or degenerate title/abstract)"] += 1
        continue
    ak = [clean(x) for x in re.split(r"[;|]", r.get("Author Keywords") or "") if clean(x)]
    affs = [clean(x) for x in (r.get("Affiliations") or "").split(";") if clean(x)]
    countries, lead = [], None
    for a in affs:
        c = norm_country(a)
        if c and c not in countries:
            countries.append(c)
    if countries:
        lead = countries[0]
    try:
        cites = int(clean(r.get("Cited by")) or 0)
    except ValueError:
        cites = 0
    doctype = clean(r.get("Document Type"))
    docs.append(dict(
        eid=clean(r.get("EID")),
        doi=clean(r.get("DOI")),
        title=title,
        abstract=abstr,
        author_keywords=ak,
        year=yr,
        doctype=doctype,
        source=clean(r.get("Source title")),
        publisher=clean(r.get("Publisher")),
        language=clean(r.get("Language of Original Document")),
        cited_by=cites,
        countries=countries,
        lead_country=lead,
        authors=len([a for a in (r.get("Author(s) ID") or "").split(";") if a.strip()]),
    ))

# ---------------------------------------------------------------- layered corpora
def layer(d, lvl):
    if lvl == 1:
        return d["title"]
    if lvl == 2:
        return d["title"] + " " + " ; ".join(d["author_keywords"])
    return d["title"] + " ; " + " ; ".join(d["author_keywords"]) + " . " + d["abstract"]

for d in docs:
    for lvl in (1, 2, 3):
        d["L%d" % lvl] = layer(d, lvl)

in_window = [d for d in docs if WINDOW_START <= d["year"] <= WINDOW_END]
out_window = [d for d in docs if d["year"] > WINDOW_END]
pre_window = [d for d in docs if 0 < d["year"] < WINDOW_START]

# ---------------------------------------------------------------- D2 diagnostics
def term_doc_freq(dl, terms):
    c = collections.Counter()
    for d in dl:
        t = " " + re.sub(r"[^a-z0-9\- ]+", " ", d["L3"].lower()) + " "
        for q in terms:
            if (" " + q.lower() + " ") in t or (q.lower() + "s ") in t:
                c[q] += 1
    return c

artifact = term_doc_freq(docs, QUERY_TERMS)

# domain-generic control terms (NOT in the query) for contrast
control_terms = ["coaching", "mental health", "sponsorship", "basketball", "rehabilitation",
                 "doping", "leadership", "technology", "well-being", "stakeholder"]
control = term_doc_freq(docs, control_terms)

# ---------------------------------------------------------------- write corpus
ids = {}
for i, d in enumerate(docs):
    d["doc_id"] = i
    d["eid_hash"] = hashlib.md5((d["eid"] or d["title"]).encode("utf-8")).hexdigest()[:12]

with open(os.path.join(OUT, "corpus.json"), "w", encoding="utf-8") as f:
    json.dump(dict(
        query=QUERY, window=[WINDOW_START, WINDOW_END],
        n_raw=n_raw, n_kept=len(docs), n_window=len(in_window),
        exclusion_counts=dict(excl_type),
        docs=docs,
    ), f, ensure_ascii=False)

with open(os.path.join(OUT, "corpus_meta.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["doc_id", "year", "doctype", "source", "cited_by", "lead_country",
                "n_countries", "authors", "language", "title"])
    for d in docs:
        w.writerow([d["doc_id"], d["year"], d["doctype"], d["source"], d["cited_by"],
                    d["lead_country"] or "", len(d["countries"]), d["authors"],
                    d["language"], d["title"]])

# ---------------------------------------------------------------- report
print("=" * 78)
print("STAGE 0  CORPUS CONSTRUCTION")
print("=" * 78)
print("Raw Scopus records              : %d" % n_raw)
print("Excluded by type/quality        : %d  %s" % (sum(excl_type.values()), dict(excl_type)))
print("Analytic corpus                 : %d" % len(docs))
print("  analysis window %d-%d      : %d" % (WINDOW_START, WINDOW_END, len(in_window)))
print("  post-window (2026, partial)   : %d" % len(out_window))
print("  pre-2013 (descriptive only)   : %d" % len(pre_window))
print()
print("DOC TYPE (analytic corpus)")
for k, v in collections.Counter(d["doctype"] for d in docs).most_common():
    print("   %4d  %s" % (v, k))
print()
print("LANGUAGE (analytic corpus)")
for k, v in collections.Counter(d["language"] for d in docs).most_common(12):
    print("   %4d  %s" % (v, k or "(blank)"))
print()
print("=" * 78)
print("D2  QUERY-ARTIFACT DIAGNOSTIC  (terms taken verbatim from the search string)")
print("=" * 78)
print("%-30s %7s %9s" % ("query term", "docs", "share"))
for k, v in artifact.most_common():
    print("%-30s %7d %8.1f%%" % (k, v, 100 * v / len(docs)))
print()
print("%-30s %7s %9s" % ("control term (not in query)", "docs", "share"))
for k, v in control.most_common():
    print("%-30s %7d %8.1f%%" % (k, v, 100 * v / len(docs)))
print()
art_mean = sum(artifact.values()) / len(artifact)
ctl_mean = sum(control.values()) / len(control)
print("mean share, query terms  : %.1f%%" % (100 * art_mean / len(docs)))
print("mean share, control terms: %.1f%%" % (100 * ctl_mean / len(docs)))
print("inflation ratio          : %.2fx" % (art_mean / ctl_mean))
print()
print("Wrote %s" % os.path.join(OUT, "corpus.json"))
print("Wrote %s" % os.path.join(OUT, "corpus_meta.csv"))
