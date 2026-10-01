# -*- coding: utf-8 -*-
"""Part 3: Method - corpus, query artefacts, concept extraction."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docbuild import *
from docx import Document

d = Document(DOC)

h1(d, "3. Method")

h2(d, "3.1 Design and transparency")
para(d, "This is a retrospective bibliometric and text-mining study of a single bibliographic "
        "corpus. Analyses were performed in Python 3.11 using spaCy 3.8 for parsing, "
        "sentence-transformers with intfloat/e5-base-v2, scikit-learn for clustering and topic "
        "modelling, umap-learn for dimensionality reduction, NetworkX for network analysis, and "
        "SciPy and statsmodels for inference. The pipeline executes end-to-end in approximately "
        "20 minutes as a nine-stage script sequence with every parameter in a single "
        "configuration block per stage. Random seeds are fixed throughout, so all reported "
        "quantities are reproducible.")

h2(d, "3.2 Literature search and corpus construction")
para(d, "Data were retrieved from Scopus on 30 September 2026 using the structured query "
        "reported in Appendix A, combining a concept block on sport ecosystems, systems, "
        "networks and value chains with a context block on elite and high-performance sport. "
        "The query returned 623 records.")

table_caption(d, "Table 1. Corpus construction and exclusion audit.")
table(d,
      ["Stage", "n", "Note"],
      [["Scopus records retrieved", "623", "Single structured query, 30.09.2026"],
       ["Excluded: Retracted", "3", "Withdrawn during data processing"],
       ["Excluded: Note", "7", "Not peer-reviewed articles"],
       ["Excluded: Editorial", "2", "Non-empirical"],
       ["Excluded: Erratum", "1", "Correction notice"],
       ["Excluded: degenerate title/abstract", "6", "Empty or < 80 characters after cleaning"],
       ["Analytic corpus", "604", "Retained for structural analysis"],
       ["  of which in analysis window 2013-2025", "448", "Retained for all inference"],
       ["  of which pre-2013", "50", "Descriptive reporting only"],
       ["  of which 2026 (partial indexing)", "106", "Excluded from all inference"]],
      widths=[3.3, 0.7, 2.5])
figure_caption(d, "Document types retained: articles (447), book chapters (95), reviews (26), "
                  "conference papers (24), books (12). Retaining book chapters is deliberate: "
                  "sport policy and elite sport systems scholarship is disproportionately "
                  "published in edited volumes, and excluding them would systematically "
                  "disadvantage governance research.")

para(d, "Two corpus decisions require justification. First, Scopus indexing of 2026 was "
        "incomplete at the retrieval date, with 2026 already contributing 106 records - more "
        "than any other single year after 2021. Including these in temporal inference would "
        "produce a spurious recent-topic surge, so all temporal analysis is restricted to the "
        "2013-2025 window. Second, Scopus Index Keywords are excluded from concept mining "
        "entirely. These are MeSH-derived clinical terms and produce, in this corpus, a "
        "physiology cluster ('human', 107 documents; 'female', 61; 'male', 60; 'adult', 48) "
        "that has no relation to the research object. Concept mining draws on titles, author "
        "keywords and abstracts.")

h2(d, "3.3 The query-artefact problem")
para(d, "Retrieval with a single structured query guarantees that the query's vocabulary is "
        "over-represented in the result set relative to the underlying literature. We treat "
        "this as a measurement problem with a measurable magnitude and a correctable bias.")

para(d, "Diagnostically, we compared document frequency for nine phrases taken verbatim from "
        "the search string against ten control terms selected to be plausible in the domain "
        "but absent from the query. Figure 2 reports the result.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F2_query_artifact.png", 6.3)
figure_caption(d, "Figure 1. Query-string terms versus matched control terms. Query terms "
                  "average 20.4% document frequency against 5.5% for controls, an inflation "
                  "ratio of 3.67. The phrase 'sport system' alone, an alternative in the query, "
                  "occurs in 54.6% of documents.")

para(d, "Two classes of suppression follow. The first is direct: any candidate term matching "
        "the search string, including morphological variants, is excluded from concept mining. "
        "The second follows from the logical structure of the query. Every disjunct of the "
        "concept block contains the token 'sport' (sport ecosystem, sport system, sport "
        "network, sport value chain, elite sport, high performance sport, professional sport), "
        "so that token is present in the corpus by construction and carries no information "
        "about the field. 'Sport' and 'sports' are therefore excluded as necessary-condition "
        "tokens. By contrast, 'athlete', 'elite' and 'performance' appear in only one disjunct "
        "each and are not guaranteed; they are retained on their merits, subject to the "
        "specificity criteria of Section 3.5.")

h2(d, "3.4 Layered corpus design")
para(d, "Every structural statistic is computed on three nested layers of the same documents: "
        "L1 (titles), L2 (titles plus author keywords), and L3 (titles, author keywords and "
        "abstracts). This design supports the concept stratification analysis in Section 4.6, "
        "which compares where concepts are mentioned against where they are structurally "
        "important. It also provides a robustness check: conclusions that hold across layers "
        "are unlikely to depend on the abstract-mining step.")

h2(d, "3.5 POS-aware concept extraction")
para(d, "Concepts are mined from the L3 layer as noun-phrase-constrained n-grams of length one "
        "to four. Candidates are generated only from maximal runs of contiguous tokens tagged "
        "NOUN, PROPN or ADJ, with adjectives permitted only in non-final position. Because "
        "adjacency is evaluated on the filtered nominal stream, a deleted verb between two "
        "nouns does not generate a spurious bigram - a failure mode of naive n-gram mining over "
        "raw text. Candidates then pass through a seven-stage filter cascade, with every drop "
        "count reported so that the surviving inventory is fully auditable.")

table_caption(d, "Table 2. Concept-extraction filter cascade.")
table(d,
      ["Criterion", "Rule", "Dropped"],
      [["C1 Support", "df >= 5", "22,768"],
       ["C2 Non-ubiquity", "df/N < 0.60", "4"],
       ["C3 Query-artefact exclusion", "matches search string or necessary-condition token",
        "16"],
       ["C3b Research apparatus", "methodological vocabulary describing the instrument",
        "37"],
       ["C3c Metadata and cross-lingual", "export residue and non-English residue", "24"],
       ["C3d Single-character token", "n-gram contains a 1-character token", "10"],
       ["C3e Definitional construction", "'the term X', 'the notion of X'", "7"],
       ["C3f High-frequency English", "unigram in a standard high-frequency list", "373"],
       ["C4 Stopword inside", "contains a stopword", "42"],
       ["C5 Maximality", "strict sub-phrase of a longer n-gram with identical df", "19"],
       ["C6 Collocation (Dunning LLR)", "chi-square(1) >= 10.828 for multiword terms", "108"],
       ["C7 Adjacenting", "min(left, right entropy) >= 0.30 bits", "121"],
       ["Retained", "1,208 concepts (1,120 unigram, 88 multiword)", "-"]],
      widths=[1.5, 3.4, 0.8])
figure_caption(d, "C1 dominates because the length-four n-gram space is combinatorially large; "
                  "the substantive filters are C2-C7, which together removed 744 further "
                  "candidates.")

para(d, "Three criteria warrant elaboration. C5 (maximality) removes fragments: if \u201ctalent "
        "development programme\u201d and \u201ctalent development\u201d occur in exactly the "
        "same documents, the latter is not an independent concept. C6 uses Dunning's (1993) "
        "log-likelihood ratio for the 2x2 contingency table of the two constituent words "
        "against an independence null, at p = .001. For longer n-grams, where a single 2x2 "
        "table is undefined, every contiguous bigram within the phrase must itself be a "
        "significant collocation. C7 applies adjacency entropy - the Shannon entropy of tokens "
        "immediately left and right of each occurrence - so that only \u201catomic\u201d "
        "concepts with variable contextual slots survive, preventing phrases such as "
        "\u201cdevelopment\u201d from absorbing unrelated neighbours.")

para(d, "C3f requires a comment. A hand-built stoplist cannot keep pace with 604 abstracts, and "
        "without a high-frequency filter the inventory is dominated by generic English. We "
        "therefore apply a standard high-frequency English word list to unigrams only. This "
        "restriction is deliberate: multiword expressions assembled from generic words are "
        "frequently genuine domain concepts - \u201cnational team\u201d, \u201csocial "
        "support\u201d, \u201cyouth sport\u201d - and a blanket component-wise rule would "
        "discard them. The full list is provided in Appendix B.")

table_caption(d, "Table 3. Twelve most frequent retained concepts (document frequency, after "
                 "SEMCON consolidation).")
table(d,
      ["Concept", "df", "Concept", "df", "Concept", "df", "Concept", "df"],
      [["elite", "274", "national sport", "41", "athlete development", "41", "governance",
        "55"],
       ["development", "263", "youth sport", "41", "mental health", "28", "regulatory", "48"],
       ["performance", "251", "talent identification", "31", "implementation", "43",
        "federal", "46"],
       ["systems", "248", "coach", "54", "stakeholders", "58", "sport policy", "44"],
       ["national", "212", "policy", "48", "club", "45", "performance environment", "41"],
       ["coaching", "149", "olympic", "48", "resources", "43", "leadership", "43"]],
      widths=[1.15, 0.4, 1.15, 0.4, 1.15, 0.4, 1.15, 0.4])
figure_caption(d, "Note: no research-apparatus, cross-lingual or export-residue vocabulary "
                  "survives the cascade.")

page_break(d)
d.save(DOC)
print("part3 ok")