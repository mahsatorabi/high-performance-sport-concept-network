# Scopus retrieval record

## Query (verbatim)

```
TITLE-ABS-KEY(
  ( "sport ecosystem" OR "sport system" OR "sport network" OR "sport value chain"
    OR "innovation ecosystem" OR "entrepreneurial ecosystem" )
  AND
  ( "elite sport" OR "high performance sport" OR "professional sport" OR "athlete*" )
)
```

## Retrieval

| Field | Value |
|---|---|
| Database | Scopus |
| Field searched | TITLE-ABS-KEY (title, abstract, author keywords) |
| Retrieval date | 30 September 2026 |
| Records returned | **623** |

## Pre-filtering

**None applied by the researcher.** All 623 records were exported unfiltered from Scopus.
Every exclusion reported in the manuscript (Table 1) is an *analytical* decision made
within the pipeline, not a step applied before data collection.

## Analytical exclusions (applied in `s0_corpus.py`)

| Exclusion | n | Reason |
|---|---|---|
| Retracted | 3 | Withdrawn during data processing |
| Note | 7 | Not peer-reviewed articles |
| Editorial | 2 | Non-empirical |
| Erratum | 1 | Correction notice |
| Degenerate title/abstract | 6 | Empty or < 80 characters after boilerplate stripping |
| **Analytic corpus** | **604** | |
| of which in analysis window 2013–2025 | 448 | Retained for all inference |
| of which pre-2013 | 50 | Descriptive reporting only |
| of which 2026 (partial indexing) | 106 | Excluded from all inference |

## Note on the 2026 records

2026 contributed 106 records — more than any single year after 2021 — because Scopus indexing
for 2026 was incomplete at the retrieval date. Including these in temporal inference would
produce a spurious recent-topic surge, so all temporal analysis is restricted to 2013–2025.

## Note on Scopus Index Keywords

Scopus Index Keywords (MeSH-derived) are excluded from concept mining entirely. They are
clinical taxonomy terms and produce a physiology cluster in this corpus
(`human` 107 documents, `female` 61, `male` 60, `adult` 48) unrelated to the research object.

## Licence

Scopus records are **not redistributed** in this repository. The query and retrieval date
above are sufficient to reproduce the corpus for users with institutional Scopus access.