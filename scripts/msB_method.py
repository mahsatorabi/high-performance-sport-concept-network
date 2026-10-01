# -*- coding: utf-8 -*-
"""Part B: Method."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docbuild import *
from docx import Document

d = Document(DOC)

h1(d, "3. Method")

h2(d, "3.1 Design and software")
para(d, "This is a retrospective bibliometric study of one bibliographic corpus. Analysis was "
        "done in Python 3.11 with spaCy 3.8 for parsing, sentence-transformers "
        "(intfloat/e5-base-v2) for embeddings, scikit-learn for clustering and topic modelling, "
        "umap-learn, NetworkX, SciPy and statsmodels. The pipeline is nine scripts that run "
        "end to end in about twenty minutes, with every parameter in one configuration block "
        "per stage. Seeds are fixed throughout.")

h2(d, "3.2 Search and corpus construction")
para(d, "Records came from Scopus on 30 September 2026 under the structured query given in "
        "Appendix A. It returned 623 records. No filtering was applied before collection.")

table_caption(d, "Table 1. Corpus construction and exclusion audit.")
table(d,
      ["Stage", "n", "Note"],
      [["Scopus records retrieved", "623", "Single structured query, 30.09.2026"],
       ["Excluded: Retracted", "3", "Withdrawn during data processing"],
       ["Excluded: Note", "7", "Not peer-reviewed articles"],
       ["Excluded: Editorial", "2", "Non-empirical"],
       ["Excluded: Erratum", "1", "Correction notice"],
       ["Excluded: degenerate title/abstract", "6", "Empty or under 80 characters after cleaning"],
       ["Analytic corpus", "604", "Used for structural analysis"],
       ["   within analysis window 2013-2025", "448", "Used for all inference"],
       ["   pre-2013", "50", "Descriptive reporting only"],
       ["   2026 (partial indexing)", "106", "Excluded from all inference"]],
      widths=[3.3, 0.7, 2.5])
figure_caption(d, "Retained document types: articles (447), book chapters (95), reviews (26), "
                  "conference papers (24), books (12). Book chapters are kept deliberately. "
                  "Elite sport systems scholarship appears disproportionately in edited "
                  "volumes, and dropping them would quietly penalise governance research.")

para(d, "Two corpus decisions need justifying. Scopus indexing of 2026 was incomplete at "
        "retrieval, and 2026 had already contributed 106 records, more than any year since 2021. "
        "Leaving them in would manufacture a surge in recent topics, so all temporal work uses "
        "2013-2025. Separately, Scopus Index Keywords are excluded outright. They are "
        "MeSH-derived clinical terms, and here they produce a physiology cluster with no "
        "bearing on the research object: “human” in 107 documents, “female” 61, “male” 60, "
        "“adult” 48. Mining draws on titles, author keywords and abstracts.")

h2(d, "3.3 The query-artefact problem")
para(d, "One structured query guarantees its own vocabulary is over-represented in the results. "
        "We treat that as a measurement problem with a measurable size and a correctable bias. "
        "To size it, we compared document frequency for nine phrases taken verbatim from the "
        "search string against ten control terms plausible for the domain but absent from the "
        "query.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F2_query_artifact.png", 6.3)
figure_caption(d, "Figure 1. Query-string terms against matched controls. Query terms average "
                  "20.4% document frequency, controls 5.5%, an inflation ratio of 3.67. The "
                  "phrase “sport system”, a single alternative in the query, occurs in 54.6% "
                  "of documents.")

para(d, "Two kinds of suppression follow. Direct suppression first: anything matching the "
        "search string, morphological variants included, is barred from concept mining. Second, "
        "and less obviously, every disjunct in the concept block contains the token “sport”, "
        "so that token is in the corpus by construction and says nothing about the field. "
        "“Sport” and “sports” are therefore dropped on logical grounds. The same does not "
        "hold for “athlete”, “elite” or “performance”: each appears in only one disjunct, "
        "so none is guaranteed, and all three stay subject to the specificity criteria below.")

h2(d, "3.4 A layered corpus")
para(d, "Every structural statistic is computed three times, on titles, on titles plus author "
        "keywords, and on the full record. This is what the stratification analysis in Section "
        "4.6 uses, and it doubles as a robustness check, since conclusions that hold across all "
        "three layers are unlikely to hinge on abstract mining.")

h2(d, "3.5 Concept extraction")
para(d, "Concepts are noun-phrase-constrained n-grams, one to four tokens long. Candidates come "
        "only from runs of adjacent NOUN, PROPN or ADJ tokens, with adjectives barred from final "
        "position. Running adjacency off the filtered stream matters: it stops a deleted verb "
        "between two nouns from generating a spurious bigram, a common failure in naive n-gram "
        "mining. Candidates then pass seven filters, each with its drop count reported so the "
        "surviving set can be audited.")

table_caption(d, "Table 2. Concept-extraction filter cascade.")
table(d,
      ["Criterion", "Rule", "Dropped"],
      [["C1 Support", "df >= 5", "22,768"],
       ["C2 Non-ubiquity", "df/N < 0.60", "4"],
       ["C3 Query-artefact exclusion", "matches search string or necessary-condition token",
        "16"],
       ["C3b Research apparatus", "methodological vocabulary describing the instrument", "37"],
       ["C3c Metadata and cross-lingual", "export residue, non-English residue", "24"],
       ["C3d Single-character token", "contains a 1-character token", "10"],
       ["C3e Definitional construction", "“the term X”, “the notion of X”", "7"],
       ["C3f High-frequency English", "unigram in a high-frequency word list", "373"],
       ["C4 Stopword inside", "contains a stopword", "42"],
       ["C5 Maximality", "sub-phrase of a longer n-gram with identical df", "19"],
       ["C6 Collocation (Dunning LLR)", "chi-square(1) >= 10.828, multiword terms", "108"],
       ["C7 Adjacenting", "min(left, right entropy) >= 0.30 bits", "121"],
       ["Retained", "1,208 concepts (1,120 unigram, 88 multiword)", "-"]],
      widths=[1.5, 3.4, 0.8])
figure_caption(d, "C1 does most of the work, because the length-four n-gram space is "
                  "combinatorially enormous. The filters that actually decide what counts as a "
                  "concept are C2 to C7, which remove a further 744 candidates.")

para(d, "Three of these deserve comment. C5 removes fragments: where “talent development "
        "programme” and “talent development” occur in exactly the same documents, the latter "
        "is not a separate concept. C6 uses Dunning's (1993) log-likelihood ratio on the 2x2 "
        "table of the two constituent words, at p = .001. Longer phrases have no single 2x2 "
        "table, so there we require every internal bigram to be a significant collocation in "
        "its own right. C7 applies adjacency entropy, the Shannon entropy of the tokens either "
        "side of each occurrence, which keeps only atomic concepts and stops something like "
        "“development” from quietly swallowing unrelated neighbours.")

para(d, "C3f needs a word. A hand-written stoplist cannot keep pace with 604 abstracts, and "
        "without a high-frequency filter the inventory fills up with generic English. We use a "
        "standard high-frequency word list, on unigrams only. That restriction is a choice: "
        "multiword phrases built from ordinary words are often real domain concepts, and a "
        "blanket component-wise rule would throw away “national team”, “social support” and "
        "“youth sport”. The list is in Appendix B.")

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
figure_caption(d, "No research-apparatus, cross-lingual or export-residue vocabulary survives "
                  "the cascade.")

h2(d, "3.6 SEMCON: consolidating concept families")
para(d, "Surface-string networks fragment under synonymy. In this corpus the same object turns "
        "up as “coaches”, “coach”, “coaching” and “sports coaching”; “athlete "
        "development” and “sport development” overlap heavily. That fragmentation spreads "
        "centrality across near-duplicates and inflates the apparent number of themes. SEMCON "
        "runs in two stages, both built to err towards not merging.")

h2(d, "3.6.1 Deterministic normalisation")
para(d, "Morphological and orthographic variation is the biggest source of fragmentation here, "
        "and it can be handled exactly. A rule-based normaliser maps British to American spelling "
        "(organisation/organization, programme/program, behaviour/behavior, centre/center, "
        "defence/defense and about sixty more, which matter in a sport-science literature split "
        "between British and American systems), then singularises plurals with an explicit "
        "irregular list. No model is involved, so nothing can go wrong. This stage takes 1,208 "
        "concepts down to 1,098 groups.")

h2(d, "3.6.2 Lexical synonymy under complete linkage")
para(d, "What remains is not morphological and needs judgement. We encode each normalised "
        "concept with E5-base-v2 (Wang et al., 2022) and take cosine similarity between mean-"
        "centred embeddings. Why centring matters is the next subsection. Concepts are then "
        "grouped by complete-linkage agglomerative clustering at distance 1 minus tau. Complete "
        "linkage guarantees every pair inside a family sits within threshold, so nothing can be "
        "linked only transitively. A cap of twelve members applies; anything larger is rejected "
        "and its members kept as singletons, since we would rather decline to assert a structure "
        "we cannot defend than invent one.")

h2(d, "3.6.3 Anisotropy")
para(d, "Neural sentence embeddings crowd into a narrow region, so unrelated items look alike "
        "(Ethayarajh, 2019; Li et al., 2020). Here the effect is severe. Mean cosine between "
        "randomly sampled unrelated concept pairs is +0.808 on raw embeddings and -0.001 after "
        "subtracting the mean vector and renormalising.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F3_anisotropy.png", 6.3)
figure_caption(d, "Figure 2. Cosine similarity between randomly sampled concept pairs, before "
                  "and after mean-centring. On the raw space almost every pair clears any "
                  "plausible merge threshold. Everything downstream uses centred embeddings.")

para(d, "Recent work argues that anisotropy is not the sole cause of poor downstream "
        "performance (Fuster Baggetto & Fresno, 2022). That debate is about causation in "
        "embedding quality and does not bear on our narrower requirement, which is that cosine "
        "similarity discriminate at all.")

h2(d, "3.6.4 Two approaches that failed")
para(d, "Two failures during development set the final design. Both are worth reporting because "
        "both are likely to recur.")

para(d, "Connected components over a thresholded similarity graph was the first attempt. It "
        "produced one family of 132 members containing “elite”, “development”, "
        "“performance”, “national” and “policy”, and folded “youth sport” into a "
        "72-member demographic group with “youth”, “age”, “women” and “people”. The mechanism "
        "is chaining. Connected components allow arbitrarily long transitive paths, so a single "
        "spurious edge between two common words swallows a whole region. Complete linkage "
        "replaces them and makes chaining impossible.")

para(d, "Calibrating tau on benchmark performance alone was the second. The benchmark of "
        "known synonym and contrast pairs turned out to be saturated: zero false merges anywhere "
        "between tau = 0.15 and 0.98. It could certify safety but could not pick a threshold, "
        "and taking an argmax on a flat optimum would have been arbitrary. The validation design "
        "was rebuilt in response.")

h2(d, "3.6.5 Calibrating by hand adjudication")
para(d, "The replacement samples the pairs complete linkage would actually merge at eight "
        "candidate thresholds, has them adjudicated by hand, and derives tau from the result. "
        "The sampled population is the union of within-cluster pairs across the grid, so it is "
        "exactly the set of decisions the procedure faces. Verdicts are binary: same conceptual "
        "object, or keep separate. Ninety-five merges were judged.")

para(d, "The rule was fixed before the audited profile was examined: take the smallest tau whose "
        "cumulative audited precision over merges at or above it reaches 0.95. A conservative "
        "criterion beat argmax here for the reason given above. The rule returns tau = 0.729 with "
        "cumulative precision 0.957, from 70 merges of which 67 were correct.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F4_tau_calibration.png", 6.3)
figure_caption(d, "Figure 3. Threshold calibration. (a) Benchmark precision sits at 1.00 across "
                  "the whole grid, which is why the benchmark certifies safety without "
                  "selecting anything. (b) Audited precision by similarity band, bar labels "
                  "giving correct judgments over total adjudicated. Precision is erratic below "
                  "roughly 0.80 and perfect at every band from 0.85 up.")

para(d, "An automatic screen checks this independently. Every multi-member family is screened "
        "for antonyms from a curated list (public/private, elite/mass, competitive/cooperation, "
        "traditional/modern, global/local and others) and for pairs sharing a word but scoring "
        "below 0.60. At the chosen tau, none of the 56 multi-member families trips either "
        "criterion, putting family-construction error at or below 1.000. The screen is not "
        "vacuous: at the rejected threshold of 0.42 it flags 18 of 453 families, genuine antonym "
        "errors included. Sweeping the family-size cap from 3 to 12 leaves the partition "
        "unchanged, since no family exceeds three members.")

h2(d, "3.7 Network construction")
para(d, "The document-by-concept matrix is binary. Nodes fall inside a specificity window: at "
        "least 8 documents so the concept is informative, and no more than 30% of documents so "
        "it is not a corpus constant. The upper bound removes two families (“elite”, "
        "“systems”); the lower keeps 669 of 1,041.")

para(d, "Edges are admitted against a null rather than a threshold. For each pair we compute "
        "association strength, the overlap of the two document sets, and compare it to a "
        "degree-preserving bipartite null built by edge swap: a concept is exchanged between two "
        "documents, which preserves document and concept degrees exactly while destroying "
        "topical association. Thirty draws give a usable null per pair. An edge is kept when raw "
        "co-occurrence is at least 3 and the null z-score is at least 2.5, which yields 5,061 "
        "edges.")

table_caption(d, "Table 4. Edge-admission sensitivity to the null-calibrated threshold.")
table(d,
      ["z threshold", "1.0", "1.5", "2.0", "2.5", "3.0", "4.0"],
      [["Edges retained", "27,694", "19,851", "13,478", "8,846", "5,906", "2,562"],
       ["Mean degree", "64.1", "46.0", "31.2", "20.5", "13.7", "5.9"]],
      widths=[1.7, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85])
figure_caption(d, "Computed on the specificity-windowed node set before parameters were "
                  "finalised; the chosen operating point is z >= 2.5.")

h2(d, "3.8 Centrality, communities and the structural null")
para(d, "Centrality is measured on the weighted network: strength, closeness, betweenness, "
        "eigenvector and PageRank. Eigenvector centrality is undefined on disconnected graphs, "
        "so it is computed per component and rescaled by component size. Communities use "
        "Louvain over a resolution sweep from 0.4 to 4.0 in steps of 0.1, keeping the "
        "resolution with highest modularity.")

para(d, "Structure is tested against a configuration model. Over 300 randomisations preserving "
        "the observed degree sequence we recompute the modularity of the Louvain partition and "
        "the betweenness of each node, and convert observations to z-scores. Null betweenness "
        "uses pivot sampling with k = 200 for tractability, and observed and null estimates use "
        "the same pivots so the comparison is like for like. This is the right benchmark "
        "because it asks whether the degree sequence alone would produce apparent modularity. It "
        "would: a random graph with these degrees reaches Q = 0.220.")

h2(d, "3.9 Topic modelling")
para(d, "Thematic structure is assessed separately from the concept network. Window documents "
        "are encoded with the same E5 encoder, mean-centred, reduced to five dimensions by UMAP "
        "(McInnes et al., 2018) and clustered by HDBSCAN (McInnes & Healy, 2017). Density-based "
        "clustering suits this corpus because it fixes the number of clusters from the data and "
        "assigns unclustered documents to noise rather than forcing them into a topic. In a "
        "heterogeneous literature the noise share is itself informative: it measures how far the "
        "corpus decomposes into coherent themes.")

para(d, "Parameters come from a nine-point grid over min_samples (5, 8, 10) and min_cluster_size "
        "(12, 15, 20), scored on joint criteria: 4 to 20 topics, noise below 45%, smallest "
        "cluster at least 8 documents, and best silhouette score on the clustered subset. The "
        "chosen configuration (min_samples = 8, min_cluster_size = 15) gives eight topics, "
        "16.3% noise and silhouette 0.484.")

para(d, "Topics are labelled twice, and both label sets are computed over SEMCON families rather "
        "than raw tokens so they use the same vocabulary as the network. Primary labels use "
        "class-based TF-IDF (Grootendorst, 2022). Secondary labels use the log-odds ratio with "
        "an informative Dirichlet prior (Monroe et al., 2008), which separates terms that are "
        "over-represented in a topic from those that are merely frequent, and behaves better "
        "than raw counts on small topics. Labels are also confined to the specificity window, "
        "which stops ubiquitous filler winning a label by sheer frequency. Stability comes from "
        "refitting HDBSCAN on twelve bootstrap resamples and taking the adjusted Rand index of "
        "co-assignment against the full-sample partition.")

h2(d, "3.10 Temporal and cross-national inference")
para(d, "Periods are 2013-2016, 2017-2019, 2020-2021 and 2022-2025, the third isolating the "
        "pandemic surge and the distinct literature around it. Topic-by-period association uses "
        "chi-square on the full contingency table rather than per-cell tests, which would inflate "
        "the error rate. Cramér's V is reported alongside, because a significant chi-square at "
        "this corpus size can sit on a negligible effect, as is the count of cells with expected "
        "frequency below 5. Direction is an emergence parameter: the topic's share from 2021 "
        "onward minus the corpus baseline, declines scored the same way on the pre-2020 share, "
        "with 0.08 separating the categories.")

para(d, "Documents are assigned to their lead-affiliation country, and countries with at least "
        "12 documents form the comparison set (10 of 54). Over-representation uses two-proportion "
        "z-tests against the rest of the corpus with Benjamini-Hochberg correction across each "
        "family of tests. One exclusion needs stating: demonymic and geographic families "
        "(“canada”, “norwegian”, “russia” and similar, 70 in all) are trivially "
        "over-represented in their own national corpus, since the country variable derives from "
        "them. Testing them is circular, so they are dropped from reporting while staying in the "
        "multiplicity correction.")

h2(d, "3.11 Multiplex construction")
para(d, "To test integration, the network is split into a multiplex with one layer per pillar. "
        "Assignment is data-driven rather than assumed. Each family is embedded with the same "
        "encoder and matched against fifteen prototypes, five per pillar, covering governance "
        "and regulation, sport innovation and technology, and athlete talent development. "
        "Assignment takes the maximum cosine similarity after mean-centring; families whose "
        "margin over the runner-up falls below 0.02 are recorded as unassigned, so confidence "
        "stays visible rather than being hidden inside a hard partition.")

para(d, "Integration is then the share of shortest paths between concepts that cross a pillar "
        "boundary, compared against a degree-preserving null with pillar labels randomly "
        "permuted. The null is not optional: some cross-pillar traffic is unavoidable under any "
        "partition, so a raw overlap count means nothing. Bridge concepts are ranked by "
        "supra-centrality, a node's within-layer betweenness summed across the layers it "
        "inhabits and weighted by its total intra-layer degree.")

page_break(d)
d.save(DOC)
print("partB ok")