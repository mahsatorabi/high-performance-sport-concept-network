# -*- coding: utf-8 -*-
"""Part 4: Method - SEMCON, network, nulls, topics, temporal."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docbuild import *
from docx import Document

d = Document(DOC)

h2(d, "3.6 SEMCON: semantic concept-family consolidation")

h3 = h2
para(d, "A co-word network built on surface strings is fragmented by synonymy. Several "
        "conceptually identical objects appear here under multiple names - \u201ccoaches\u201d, "
        "\u201ccoach\u201d, \u201ccoaching\u201d and \u201csports coaching\u201d are the same "
        "category; \u201cathlete development\u201d and \u201csport development\u201d overlap "
        "substantially. This fragmentation disperses the centrality of integrative concepts "
        "across near-duplicate nodes and inflates the apparent number of themes. SEMCON "
        "addresses this in two stages designed to be conservative by construction.")

h2(d, "3.6.1 Stage 1: deterministic exact normalisation")
para(d, "Morphological and orthographic variation is the dominant source of fragmentation in "
        "this corpus and admits exact treatment. A rule-based normaliser applies British-to-"
        "American orthographic mapping (organisation/organization, programme/program, "
        "behaviour/behavior, centre/center, defence/defense, and approximately sixty further "
        "mappings, which matter materially in a sport-science literature split between British "
        "and American systems) followed by conservative plural singularisation with an explicit "
        "irregular-form list. No model is involved and no error is possible. In this corpus "
        "this stage reduces 1,208 concepts to 1,098 normalised groups, merging 110 surface "
        "variants.")

h2(d, "3.6.2 Stage 2: lexical synonymy under complete linkage")
para(d, "Residual synonymy is not morphological and requires semantic judgement. We encode "
        "each normalised concept with intfloat/e5-base-v2 (Wang et al., 2022), a recent "
        "contrastive sentence encoder, computing cosine similarity between mean-centred "
        "embeddings. Cosine similarity under this encoder is not interpretable without a "
        "correction step, for reasons documented below.")

para(d, "Concepts are then grouped by complete-linkage agglomerative clustering with the "
        "distance threshold set to 1 - tau. Complete linkage guarantees that every pair within "
        "a family is mutually within threshold, so no concept can be linked to another only "
        "transitively. A hard cap of 12 members is imposed on family size; clusters exceeding "
        "the cap are rejected and their members retained as singletons rather than arbitrarily "
        "subdivided, because we decline to assert an internal structure we cannot justify.")

h2(d, "3.6.3 Anisotropy correction")
para(d, "Neural sentence embeddings occupy a narrow region of representation space, so that "
        "unrelated items appear highly similar. This anisotropy has been extensively "
        "documented in the natural language processing literature (Ethayarajh, 2019; Li et "
        "al., 2020) and is severe in our setting.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F3_anisotropy.png", 6.3)
figure_caption(d, "Figure 2. Distribution of cosine similarity between randomly sampled concept "
                  "pairs, before and after mean-centring. Raw embeddings place unrelated "
                  "concepts at mean cosine +0.808; after mean-centring the mean is -0.001 with "
                  "mean absolute similarity 0.066. Without this correction every pair of "
                  "concepts appears similar and the similarity matrix is uninformative.")

para(d, "Empirical magnitude in this corpus: mean cosine between randomly sampled, "
        "semantically unrelated concept pairs is +0.808 under raw embeddings, falling to "
        "-0.001 after subtracting the mean embedding and renormalising. Any similarity "
        "threshold applied to the raw space would therefore merge substantially all concepts. "
        "All subsequent similarity computation uses mean-centred embeddings. We note for "
        "completeness that recent work questions whether anisotropy is the sole cause of poor "
        "downstream performance (Fuster Baggetto & Fresno, 2022); that debate concerns "
        "anisotropy's causal role in embedding quality, and does not bear on our narrower "
        "requirement, which is that cosine similarities be usable as a discriminative measure "
        "in the first place.")

h2(d, "3.6.4 Two failures, and the resulting design")
para(d, "Two methodological failures during development shaped the final design. Both are "
        "reported because they generalise, and because a reader evaluating SEMCON needs to "
        "know where its parameterisation came from.")

para(d, "Failure one: connected components over a thresholded similarity graph. Our initial "
        "implementation built a concept-similarity graph and extracted families as connected "
        "components. This produced a single family of 132 members containing \u201celite\u201d, "
        "\u201cdevelopment\u201d, \u201cperformance\u201d, \u201cnational\u201d and "
        "\u201cpolicy\u201d, and separately absorbed the integrative concept \u201cyouth "
        "sport\u201d into a 72-member demographic family. The mechanism is chaining: "
        "connected components admit arbitrarily long transitive chains, so one spurious edge "
        "between two generic words merges an entire region of concept space. Complete linkage "
        "replaces connected components and makes chaining structurally impossible.")

para(d, "Failure two: threshold selection by benchmark performance alone. We first calibrated "
        "tau on a hand-built benchmark of synonymous and contrastive concept pairs. This "
        "benchmark turned out to be saturated - zero false merges across the entire range of "
        "tau from 0.15 to 0.98 - so it could certify safety but could not discriminate between "
        "thresholds. Selecting tau by benchmark F1 would have been arbitrary. The validation "
        "design was changed in response.")

h2(d, "3.6.5 Threshold calibration by hand adjudication")
para(d, "The revised design samples the pairs that complete-linkage would actually merge at each "
        "of eight candidate thresholds, presents them for manual adjudication, and derives the "
        "threshold from the audited outcome. The sampled population is the union of "
        "within-cluster pairs across the threshold grid - exactly the decisions the procedure "
        "makes. Verdicts were recorded on a binary scale: same conceptual object, or must "
        "remain separate. Ninety-five merges were adjudicated.")

para(d, "The decision rule was fixed before examining the audited precision profile: select the "
        "smallest tau whose cumulative audited precision over all merges at or above that "
        "threshold is at least 0.95. This yields tau = 0.730 with cumulative precision 0.957 "
        "(70 merges, 67 judged correct). A pre-registered conservative criterion was preferred "
        "to argmax selection because the argmax within a flat optimum is arbitrary.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F4_tau_calibration.png", 6.3)
figure_caption(d, "Figure 3. SEMCON threshold calibration. (a) Performance on the "
                  "saturated safety benchmark, which cannot discriminate tau. (b) Cumulative "
                  "precision from manual adjudication of 95 sampled merges; the selected "
                  "operating point is the smallest tau meeting the 0.95 criterion.")

para(d, "An independent automatic screen cross-checks the result. Every multi-member family is "
        "screened for antonym pairs from a curated list (public/private, elite/mass, "
        "competitive/cooperation, traditional/modern, global/local, and others) and for pairs "
        "sharing a word but scoring below 0.60 similarity. At the selected tau, 56 multi-member "
        "families were retained and none triggered either criterion, giving an upper bound on "
        "family-construction error of 1.000. The screen is not vacuous: at a rejected threshold "
        "of 0.42 it flags 18 of 453 multi-member families, including genuine antonym errors. A "
        "stability sweep over the family-size cap from 3 to 12 members shows identical "
        "partitioning across all values, because no family exceeds three members at the "
        "selected threshold.")

h2(d, "3.7 Co-occurrence network construction")
para(d, "The document-by-concept-family matrix is binary. Nodes are selected within a "
        "specificity window: a family must appear in at least 8 documents to be informative, "
        "and in no more than 30% of documents to be more than a corpus constant. The upper "
        "bound excludes two families ('elite', 'systems'); the lower bound retains 669 of 1,041 "
        "families.")

para(d, "Edge admission is by null-calibrated significance rather than by a similarity "
        "threshold. For each concept pair we compute association strength (the Jaccard-style "
        "overlap of the two document sets) and compare it against a degree-preserving bipartite "
        "randomisation null. The null is generated by edge-swap: a candidate family is "
        "exchanged between two documents, which preserves both document and concept degrees "
        "exactly while destroying topical association. Thirty draws suffice for a per-pair "
        "null distribution of association strength. An edge is retained when raw co-occurrence "
        "is at least 3 and the null-calibrated z-score is at least 2.5, yielding 5,061 edges.")

table_caption(d, "Table 4. Edge-admission sensitivity to the null-calibrated threshold.")
table(d,
      ["z threshold", "1.0", "1.5", "2.0", "2.5", "3.0", "4.0"],
      [["Edges retained", "27,694", "19,851", "13,478", "8,846", "5,906", "2,562"],
       ["Mean degree", "64.1", "46.0", "31.2", "20.5", "13.7", "5.9"]],
      widths=[1.7, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85])
figure_caption(d, "Note: computed on the specificity-windowed node set before finalising "
                  "parameters; the selected operating point (z >= 2.5) is shown in bold in the "
                  "source table. The qualitative structure of the network is stable across "
                  "this range, which is examined further in the sensitivity analysis.")

h2(d, "3.8 Centrality, community detection and the structural null")
para(d, "Centrality is measured in the weighted network by strength, closeness, betweenness, "
        "eigenvector centrality and PageRank. Eigenvector centrality is undefined for "
        "disconnected graphs and is therefore computed per connected component and rescaled by "
        "component size. Communities are detected by the Louvain algorithm over a resolution "
        "sweep from 0.4 to 4.0 in steps of 0.1; modularity is evaluated for each resolution and "
        "the maximum retained.")

para(d, "Structural claims are tested against a configuration-model null. For 300 "
        "randomisations preserving the observed degree sequence, we compute the modularity of "
        "the Louvain partition and the betweenness of each node, and convert observed values "
        "into z-scores. Betweenness in the null is computed by pivot sampling (k = 200) for "
        "computational tractability; the same sampled pivots are used for observed and null "
        "estimates so that the comparison is internally consistent. This null is the "
        "appropriate benchmark because it asks whether the observed degree sequence alone "
        "would generate apparent modularity. The answer is emphatically yes: a random graph "
        "with this degree sequence achieves Q = 0.220.")

h2(d, "3.9 Embedding-based topic modelling")
para(d, "Thematic structure is assessed independently of the concept network. Documents in the "
        "2013-2025 window are encoded with the same E5 encoder, mean-centred, reduced to five "
        "dimensions by UMAP (McInnes et al., 2018) and clustered by HDBSCAN (McInnes & Healy, "
        "2017). Density-based clustering is preferred to k-means because it determines the "
        "number of clusters from the data and assigns unclustered documents to a noise category "
        "rather than forcing every document into a topic. In a heterogeneous literature this is "
        "informative: the noise share measures the degree to which the corpus decomposes into "
        "coherent themes.")

para(d, "HDBSCAN parameters are selected from a nine-point grid over min_samples (5, 8, 10) and "
        "min_cluster_size (12, 15, 20) by joint criteria: between 4 and 20 topics, noise share "
        "below 45%, smallest cluster at least 8 documents, and maximum silhouette score on the "
        "clustered subset. The selected configuration (min_samples = 8, min_cluster_size = 15) "
        "yields eight topics, 16.3% noise and silhouette 0.484.")

para(d, "Topics are labelled twice. Primary labels use class-based TF-IDF (Grootendorst, 2022), "
        "which treats each topic as a class and computes term importance for the topic "
        "relative to the corpus. Secondary labels use the z-scored log-odds ratio with an "
        "informative Dirichlet prior (Monroe et al., 2008), which discriminates terms by "
        "whether they are more frequent in the topic than elsewhere, and is better behaved than "
        "raw frequency for small topics. Both are computed over the SEMCON concept families "
        "rather than raw tokens, so that topic labels are expressed in the same vocabulary as "
        "the concept network and the two analyses can be compared directly. Topic labels are "
        "additionally constrained to the specificity window so that ubiquitous generic "
        "vocabulary cannot win a label argument by mere frequency.")

para(d, "Topic stability is assessed by refitting HDBSCAN on twelve bootstrap resamples and "
        "computing the adjusted Rand index of co-assignment between each replicate and the "
        "full-sample partition, so that the reader can judge whether topic boundaries are "
        "reproducible.")

h2(d, "3.10 Temporal and cross-national inference")
para(d, "Temporal analysis uses four periods chosen to isolate structural breaks in the corpus: "
        "2013-2016, 2017-2019, 2020-2021 and 2022-2025, the third separating the pandemic surge "
        "and its distinct literature. Association between topic and period is assessed by "
        "chi-square on the full contingency table, not per-cell tests, which would inflate the "
        "error rate. Because significant chi-square statistics can arise from negligible effects "
        "at this corpus size, Cramer's V is reported alongside, as is the count of cells with "
        "expected frequency below 5. Topic direction is scored as an emergence parameter - the "
        "topic's share of documents from 2021 onward minus the corpus baseline - with declines "
        "scored symmetrically on the pre-2020 share and thresholds of ±0.08 separating "
        "directions.")

para(d, "Cross-national analysis assigns each document to its lead-affiliation country. "
        "Countries with at least 12 documents form the comparison set (10 of 54). "
        "Over-representation is tested by two-proportion z-tests of each country's topic or "
        "concept share against the rest of the corpus, with Benjamini-Hochberg false discovery "
        "rate correction across each family of tests. One exclusion requires explicit statement: "
        "demonymic and geographic concept families ('canada', 'norwegian', 'russia' and similar; "
        "70 in total) are trivially over-represented in their own national corpus because the "
        "country variable derives from them. Testing them would be circular, so their results are "
        "excluded from reporting while remaining in the multiplicity correction.")

h2(d, "3.11 Multiplex construction and pillar assignment")
para(d, "To test integration (RQ3), the network is decomposed into a multiplex with one layer "
        "per pillar. Pillar assignment is data-driven rather than asserted: each concept family "
        "is embedded with the same encoder and matched against 15 pillar prototypes, five per "
        "pillar, describing governance and regulation, sport innovation and technology, and "
        "athlete talent development. Assignment is by maximum cosine similarity after "
        "mean-centring, with families whose margin over the runner-up prototype falls below "
        "0.02 recorded as unassigned. This procedure retains assignment confidence as an "
        "explicit quantity rather than presenting a hard partition.")

para(d, "Integration is then assessed by the share of shortest paths between concepts that "
        "cross a pillar boundary, compared against a degree-preserving null in which pillar "
        "labels are randomly permuted. This null-calibrated formulation is essential: some "
        "cross-pillar traffic is unavoidable under any partition, so an uncalibrated overlap "
        "count is uninterpretable. Bridge concepts are identified by supra-centrality, the "
        "sum of a node's within-layer betweenness across the layers it inhabits, weighted by "
        "its total intra-layer degree.")

h2(d, "3.12 Robustness and reproducibility")
para(d, "Four stability checks are reported: sensitivity of edge admission across the "
        "null-calibrated threshold (Table 4); stability of the community partition across the "
        "Louvain resolution sweep (Appendix E); stability of SEMCON across the family-size cap "
        "(Section 3.6.5); and topic stability by bootstrap (Section 3.9). Layer concordance "
        "between title-level and full-text structure provides an additional internal check: "
        "conclusions that survive all three evidence layers are unlikely to depend on any "
        "single processing decision.")

page_break(d)
d.save(DOC)
print("part4 ok")