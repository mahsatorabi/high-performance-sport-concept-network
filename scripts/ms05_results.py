# -*- coding: utf-8 -*-
"""Part 5: Results."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docbuild import *
from docx import Document

d = Document(DOC)

h1(d, "4. Results")

h2(d, "4.1 Corpus characteristics")
para(d, "The analytic corpus comprises 604 documents (Table 1), of which 448 fall within the "
        "2013-2025 analysis window used for all inference. The corpus is dominated by articles "
        "(447) and book chapters (95). Ten journals account for the largest shares: "
        "International Journal of Sport Policy and Politics (23), Teoriya i Praktika "
        "Fizicheskoy Kultury (23), Frontiers in Sports and Active Living (21), International "
        "Journal of the History of Sport (19), International Review for the Sociology of Sport "
        "(18) and Sport in Society (13). Routledge accounts for 116 documents and Taylor & Francis "
        "for 87, orienting the corpus toward the sport policy and sociology traditions rather "
        "than the performance-science literature. Authorship involves 1,514 unique authors across "
        "8,024 citations, with a median of 3 citations per document and 184 uncited documents.")

h2(d, "4.2 The query string dominates frequency")
para(d, "The query-artefact diagnosis is confirmed. Query-string terms average 20.4% document "
        "frequency against 5.5% for matched control terms, an inflation ratio of 3.67 (Figure "
        "1). 'Athlete' occurs in 79.0% of documents, 'sport system' in 54.6%, 'elite sport' in "
        "33.0% and 'sport ecosystem' in only 3.6%. The ordering is instructive: terms appearing "
        "in many query disjuncts are heavily inflated, while a term appearing in one disjunct "
        "'sport ecosystem' is at corpus-typical frequency. This pattern confirms that the "
        "inflation is a property of query logic rather than of the field, and validates the "
        "necessary-condition argument for excluding 'sport' outright rather than empirically.")

h2(d, "4.3 Mined concept inventory")
para(d, "The filter cascade reduces 24,749 candidate nominal n-grams to 1,208 concepts, of "
        "which 1,120 are unigrams and 88 multiword (Table 2). C1 (minimum support) removes the "
        "large majority; the substantive filters C2-C7 remove a further 744 candidates. The "
        "surviving inventory is dominated by substantive domain vocabulary (Table 3). The "
        "multiword concepts surviving the collocation and adjacenting criteria are genuine "
        "domain expressions: \u201cathlete development\u201d (56 documents), \u201cperformance "
        "sport\u201d (54), \u201csport policy\u201d (53), \u201cnational sport\u201d (41), "
        "\u201cyouth sport\u201d (41), \u201ctalent identification\u201d (31), \u201cmental "
        "health\u201d (28), \u201csport development\u201d (27) and \u201cartificial "
        "intelligence\u201d (14).")

h2(d, "4.4 SEMCON validation")

h2(d, "4.4 SEMCON validation")
para(d, "The encoder is severely anisotropic in this application: mean cosine between "
        "randomly sampled concept pairs is +0.808 under raw embeddings and -0.001 after "
        "mean-centring, with mean absolute similarity 0.066 (Figure 2). On the raw space "
        "essentially every concept pair would exceed any plausible merge threshold. This single "
        "correction is what makes the remainder of the procedure well defined.")
para(d, "Consolidation outcomes are correspondingly conservative. Stage 1 reduces 1,208 concepts "
        "to 1,098 groups, merging 110 morphological and orthographic variants; Stage 2 yields "
        "1,041 families, of which 56 are multi-member and the largest contains three members. At "
        "the rejected threshold of 0.42, complete linkage produced 453 multi-member families with "
        "members up to six. Retained consolidations are semantically defensible, including "
        "“athlete performance” with “athletic performance”, “ethical” "
        "with “ethics”, “olympic” with “olympic sports”, "
        "“regulation” with “regulatory”, “sustainable” with "
        "“sustainability” and “korean” with “south korean”.")

para(d, "The safety benchmark is saturated and cannot discriminate thresholds, confirming the "
        "necessity of the manual audit. Audited precision rises monotonically with similarity: "
        "0.00 below approximately 0.55, 0.40 at 0.60, 0.86 at 0.70, 0.92 at 0.80 and 1.00 in every "
        "band at 0.85 and above. The pre-registered rule yields tau = 0.730 with cumulative "
        "precision 0.957 over 70 adjudicated merges (Figure 3). The independent automatic screen "
        "flags none of the 56 multi-member families, giving an upper bound on "
        "family-construction error of 1.000; the screen is not vacuous, since at the rejected "
        "threshold it flags 18 of 453 families including genuine antonym errors. The partition "
        "is identical across family-size caps from 3 to 12 members.")

para(d, "Agreement between semantic families and independently computed co-occurrence "
        "communities is very low: adjusted Rand 0.002, NMI 0.477. This near-orthogonality is not "
        "a failure. The two partitions answer different questions: semantic families group "
        "concepts that mean the same thing, co-occurrence communities group concepts used "
        "together. The divergence is the informative quantity, because concepts that bridge "
        "meaning groups without co-usage ties are precisely the integrative concepts of interest.")

h2(d, "4.5 The field is a genuine community structure")
para(d, "The concept network contains 669 nodes and 5,061 edges, with density 0.0226 and mean "
        "degree 15.1; two nodes are isolated. Louvain community detection over the resolution "
        "sweep yields maximum modularity at resolution 1.1 with ten communities (Figure 5).")

para(d, "The substantive finding is that this modularity is not an artefact. Observed modularity "
        "is Q = 0.446 against a degree-preserving configuration-model null of 0.220 ± 0.004 "
        "over 300 randomisations, giving z = +64.3 and a one-sided p of .003 (the minimum "
        "attainable with 300 draws). The null is essential to this claim: a random graph with "
        "the same degree sequence reaches Q = 0.220, so roughly half of the raw modularity "
        "value is explained by degree heterogeneity alone. The field's community structure "
        "exceeds chance by a factor of approximately two.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F5_network.png", 6.6)
figure_caption(d, "Figure 4. The concept co-occurrence network (backbone shown for "
                  "legibility). (a) Communities; (b) bridging concepts labelled by betweenness, "
                  "sized by degree. Ten communities at resolution 1.1, Q = 0.446, z = +64.3 "
                  "against the configuration-model null.")

table_caption(d, "Table 5. Communities and their defining concepts.")
table(d,
      ["Comm.", "n", "Sum df", "Defining concepts"],
      [["C0", "103", "2,429", "olympic, sporting, competitive, countries, games, policies, resources, global"],
       ["C1", "103", "2,159", "performance sport, programs, outcomes, models, interventions, psychological"],
       ["C2", "90", "1,714", "teams, players, women, values, gender, systemic, inclusion, status"],
       ["C3", "88", "2,168", "coaches, athlete development, youth, participation, talent, coaching"],
       ["C4", "83", "1,824", "framework, challenges, strategies, stakeholders, ecosystem, implementation"],
       ["C5", "79", "1,755", "organizations, sport policy, activity, governance, institutional, structural"],
       ["C6", "53", "1,073", "athletic, experiences, association, transitions, relationships, perceptions"],
       ["C7", "37", "675", "educational, academic, university, managers, barriers, institutions"],
       ["C8-9", "33", "614", "organisational conditions; paralympic, disability, crisis, covid"]],
      widths=[0.45, 0.3, 0.55, 5.0])
figure_caption(d, "Note: C8 and C9 are combined for space; see Appendix E for the full "
                  "partition.")

para(d, "The community structure is substantive rather than lexical: three communities map "
        "closely onto the field's established divisions - C0 on competition and national "
        "systems, C3 on talent and participation, C5 on governance and organisation (Table 5). "
        "The remaining communities are more heterogeneous, addressing performance measurement, "
        "athlete experience and inclusion, strategy and implementation, transitions, and "
        "education. This has a direct implication for how the ecosystem question should be "
        "posed: if the field were integrated, we would expect weak community structure and a "
        "high boundary-crossing rate, and we observe the opposite on both counts.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F6_nullmodel.png", 6.6)
figure_caption(d, "Figure 5. Null-model validation. (a) Modularity across the Louvain "
                  "resolution sweep against the configuration-model null band (2 SD); selected "
                  "resolution marked. (b) Betweenness z-score against degree, showing that "
                  "large z-scores concentrate at low degree where null variance is small. "
                  "(c) Distribution of observed betweenness, demonstrating that integrative "
                  "positions are rare.")

h2(d, "4.6 Concept stratification: framing versus intellectual infrastructure")
para(d, "The layered corpus design yields the study's most practically consequential finding. "
        "The median provenance ratio, defined as the share of a concept family's documents in "
        "which it appears in the title relative to all documents in which it appears, is 0.083. "
        "That is, only 8.3% of concept mentions occur in titles. The remainder are buried in "
        "abstracts, where they do the intellectual work but do not signal membership of a "
        "research front.")

para(d, "Layer concordance confirms that this is consequential rather than cosmetic. Spearman "
        "correlation of betweenness ranks is 0.713 between the title layer and the author-"
        "keyword layer, but only 0.391 between titles and full text, and 0.439 between "
        "keywords and full text (Figure 6). Titles and author keywords agree closely with each "
        "other, because both are short, self-selected and written for signalling. Neither "
        "agrees well with the full text, where the concepts that carry structural weight "
        "concentrate.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F7_layers.png", 6.6)
figure_caption(d, "Figure 6. Concept stratification. (a) Title-layer betweenness against "
                  "full-text betweenness (Spearman rho = 0.39); points below the diagonal are "
                  "structurally important but unadvertised in titles. (b) Betweenness against "
                  "provenance ratio, separating buried intellectual infrastructure from "
                  "framing-driven concepts.")

para(d, "The two measures together define four quadrants. Structurally important and "
        "high-provenance concepts are those the field advertises as its core, including "
        "“coaches”, “athlete development” and “participation”. "
        "Structurally important and low-provenance concepts are the field’s load-bearing "
        "infrastructure: they hold the network together while appearing in few titles. "
        "“Framework” is the clearest case, with full-text betweenness of 0.027 against "
        "title-layer betweenness an order of magnitude lower, and “ecosystem” behaves "
        "similarly. High-provenance, low-structural concepts are framing devices that consume "
        "attention without doing structural work.")

h2(d, "4.7 Bridging concepts")
para(d, "Betweenness in the observed network reaches 0.038 against a null mean of 0.0018, a "
        "factor of approximately 21. Of 669 nodes, 212 exceed betweenness z of 1.96, 195 exceed "
        "2.58 and 166 exceed 3.29. The ranked bridging concepts are substantive.")

table_caption(d, "Table 6. Leading bridging concepts with null-calibrated significance.")
table(d,
      ["Concept", "df", "Betweenness", "z", "Community"],
      [["athletic", "76", "0.0382", "+11.0", "C6"],
       ["coaches", "131", "0.0345", "+35.0", "C3"],
       ["countries", "84", "0.0325", "+7.3", "C0"],
       ["participation", "78", "0.0272", "+8.9", "C3"],
       ["framework", "121", "0.0270", "+17.1", "C4"],
       ["ecosystem", "71", "0.0238", "+16.5", "C4"],
       ["governance", "55", "0.0231", "+16.3", "C5"],
       ["injury", "48", "0.0228", "+9.9", "C4"],
       ["olympic", "143", "0.0214", "+4.6", "C0"],
       ["athlete development", "89", "0.0211", "+4.0", "C3"],
       ["structural", "45", "0.0204", "+5.5", "C5"],
       ["challenges", "100", "0.0203", "+2.7", "C4"],
       ["strategies", "99", "0.0199", "+6.5", "C4"],
       ["outcomes", "65", "0.0197", "+6.2", "C1"],
       ["experiences", "67", "0.0193", "+10.5", "C6"],
       ["performance sport", "85", "0.0180", "+10.8", "C1"],
       ["global", "58", "0.0168", "+16.6", "C0"]],
      widths=[1.5, 0.5, 0.9, 0.6, 0.8])
figure_caption(d, "Note: betweenness computed on the weighted network. Low-degree nodes can "
                  "attain high z-scores because null variance is small; z indicates "
                  "unusualness for the degree, betweenness is the effect size.")

para(d, "A qualification is necessary. The z-score tests unusualness relative to degree, not "
        "absolute importance, and for low-degree nodes null variance is small enough that z "
        "becomes large mechanically. We therefore rank by observed betweenness and treat z as a "
        "significance test; very low-frequency concepts (\u201cdirectors\u201d, df = 9; "
        "\u201cinequities\u201d, df = 9) attain z above 100 on negligible absolute betweenness "
        "and are excluded from substantive interpretation.")

para(d, "The substantive bridges cluster in two groups. The first is organisational and "
        "systemic vocabulary connecting the competition community to the governance community: "
        "\u201ccountries\u201d, \u201cgovernance\u201d, \u201cstructural\u201d and "
        "\u201cglobal\u201d. The second connects the competition community to implementation "
        "and strategy: \u201cframework\u201d, \u201cecosystem\u201d, "
        "\u201cstrategies\u201d, \u201cchallenges\u201d and \u201cimplementation\u201d. "
        "Notably, \u201cecosystem\u201d is among the strongest bridges, indicating that the "
        "concept does real work in the literature rather than functioning only as rhetoric. "
        "Conversely, innovation vocabulary is almost absent from the bridging list.")

h2(d, "4.8 Thematic structure")

h2(d, "4.8.1 Topic inventory")
para(d, "The topic model yields eight topics plus a noise cluster covering 16.3% of the windowed "
        "corpus (73 of 448 documents), with silhouette 0.484 on the clustered subset and "
        "bootstrap co-assignment ARI of 0.751 (SD 0.145, range 0.437-0.882) over twelve "
        "replicates. The stability estimate indicates that topic boundaries are reproducible at "
        "roughly three-quarters accuracy, which supports qualitative interpretation while "
        "arguing against fine-grained boundary claims.")

table_caption(d, "Table 7. Topic profiles: prevalence, direction and labels. Class-based TF-IDF "
                 "labels are truncated to four concepts; contrastive labels use "
                 "log-odds with an informative Dirichlet prior.")
table(d,
      ["Topic", "n", "Share", "Mean yr", "Direction", "c-TF-IDF label"],
      [["Socio / mental / limitations", "33", "7.4%", "2022.0", "Emerging", "socio / mental / limitations / achievements"],
       ["Physical activity / ecosystem", "50", "11.2%", "2021.7", "Emerging", "physical activity / ecosystem / clusters"],
       ["Organisational / systematic", "47", "10.5%", "2021.7", "Emerging", "organizational / systematic / highest / german"],
       ["Dual / alternative / landscape", "40", "8.9%", "2021.8", "Emerging", "dual / alternative / landscape / limitations"],
       ["Capacity / specialisation", "21", "4.7%", "2020.7", "Stable", "capacity / combination / specialization"],
       ["Networks / talent / psychology", "29", "6.5%", "2020.8", "Stable", "networks / talent / germany / psychology"],
       ["Prevention / primary / gender", "19", "4.2%", "2020.8", "Declining", "prevention / primary / gender / core"],
       ["Problems / criteria / governance", "136", "30.4%", "2019.8", "Declining", "problems / making / criteria / governance"],
       ["Noise (unclustered)", "73", "16.3%", "2021.1", "-", "-"]],
      widths=[1.55, 0.35, 0.45, 0.55, 0.6, 2.1])
figure_caption(d, "Note: share of the 448-document windowed corpus. Direction derives from the "
                  "emergence score in Table 8. Topic assignment is by embedding distance; "
                  "labels are by term importance.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F8_topics.png", 6.6)
figure_caption(d, "Figure 7. Topic structure. (a) UMAP projection of document embeddings with "
                  "HDBSCAN partition; unclustered documents shown in grey. (b) Topic prevalence "
                  "colour-coded by direction, where red denotes emerging and blue declining.")

h2(d, "4.8.2 The noise cluster as substantive heterogeneity")
para(d, "The 16.3% noise share merits comment rather than dismissal. These documents are not "
        "errors; HDBSCAN assigns to noise precisely those documents lying in low-density regions "
        "of the manifold. In a corpus assembled by a Boolean query spanning governance, "
        "innovation and talent development, a noise share approaching one sixth indicates real "
        "thematic heterogeneity at the boundary between the query's conceptual blocks - "
        "including book chapters on comparative elite sport systems and conference proceedings on "
        "sport history and sociology that share vocabulary with none of the eight coherent "
        "themes. We report it rather than tuning it away.")

h2(d, "4.9 Thematic evolution (RQ2)")
para(d, "Topic composition differs across periods, but modestly. The topic-by-period "
        "contingency table yields chi-square = 47.18 with 24 degrees of freedom, p = .003, "
        "Cramér's V = 0.187 (Figure 8). Nine of thirty-six cells have expected frequency below "
        "5, which limits the weight the test can bear and is the reason for reporting effect "
        "size rather than significance alone. The effect is real but not large: roughly 19% of "
        "the variance in topic membership is associated with period.")

para(d, "Four topics are emerging and two declining (Tables 7-8). The clearest emerging theme "
        "concerns socio-cultural and mental-health themes (emergence +0.148, mean year 2022.0), "
        "followed by themes combining physical activity with ecosystem concepts (+0.131), "
        "organisational themes with a notable German concentration (+0.114), and dual/alternative "
        "pathways (+0.091). The largest topic in absolute terms, at 30.4% of the windowed "
        "corpus, is the clearest decliner (-0.153), as is the pandemic-influenced prevention "
        "theme (-0.083).")

table_caption(d, "Table 8. Temporal structure: topic emergence and decline.")
table(d,
      ["Topic", "n", "Mean year", "Share since 2021", "Emergence", "Direction"],
      [["Socio / mental / limitations", "33", "2022.0", "0.76", "+0.148", "Emerging"],
       ["Physical activity / ecosystem", "50", "2021.7", "0.74", "+0.131", "Emerging"],
       ["Organizational / systematic", "47", "2021.7", "0.72", "+0.114", "Emerging"],
       ["Dual / alternative / landscape", "40", "2021.8", "0.70", "+0.091", "Emerging"],
       ["Capacity / specialization", "21", "2020.7", "0.67", "+0.057", "Stable"],
       ["Networks / talent / psychology", "29", "2020.8", "0.66", "+0.046", "Stable"],
       ["Noise", "73", "2021.1", "0.60", "-0.007", "Stable"],
       ["Covid / committee / psychology", "19", "2020.8", "0.53", "-0.083", "Declining"],
       ["Problems / criteria / governance", "136", "2019.8", "0.46", "-0.153", "Declining"]],
      widths=[1.9, 0.35, 0.7, 0.9, 0.7, 0.7])
figure_caption(d, "Note: corpus baseline share since 2021 is 0.609. Emergence is the topic's "
                  "share minus this baseline; thresholds of +/-0.08 separate directions.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F10_temporal.png", 6.6)
figure_caption(d, "Figure 8. Thematic evolution. (a) Topic prevalence across four periods "
                  "against the corpus total; chi-square = 47.18, V = 0.187. (b) Concept "
                  "frontier, plotting mean publication year against the share of mentions since "
                  "2021.")

h2(d, "4.9.1 The concept frontier")
para(d, "At the concept level, the frontier is dominated by digital and methodological "
        "vocabulary. The concepts with the highest mean publication year are “actionable” "
        "(2024.6), “digital” (2024.2), “reflexive” (2024.1), “algorithm” "
        "(2024.1), “maltreatment” (2024.1), “transformation” (2024.0) and "
        "“equitable” (2024.0). Two observations follow. The frontier is methodologically "
        "marked, indicating an ongoing turn towards methodological and critical reflexivity; and "
        "“maltreatment” and “equitable” indicate that safeguarding and equity "
        "concerns have become frontier issues within the window, consistent with the emerging "
        "socio-cultural theme in Table 8. The most established concepts - “willingness” "
        "(2016.6), “qualities” (2016.8), “specialist” (2017.0), “officials” "
        "(2017.3) and “modern elite” (2017.6) - are predominantly descriptive or "
        "person-centred terms characteristic of earlier qualitative work, whose relative decline "
        "is consistent with the observed shift toward policy and methodological framing.")

h2(d, "4.10 The three pillars are segregated (RQ3)")
para(d, "Pillar assignment assigns 669 network concepts as follows: 140 to governance, 159 to "
        "innovation, 158 to talent development and 212 unassigned because the margin over the "
        "runner-up prototype fell below threshold. The median assignment margin is 0.034 "
        "(interquartile range 0.015-0.074), indicating that many assignments are close calls and "
        "should be interpreted with corresponding caution.")

para(d, "The integration test is unambiguous. The observed share of shortest paths between "
        "concepts that cross a pillar boundary is 0.950. Under degree-preserving randomisation of "
        "pillar labels the expected share is 0.963 ± 0.003, giving z = -4.16 (Figure 9). "
        "Conceptual traffic between pillars is therefore significantly lower than chance: the "
        "three pillars behave as segregated literatures, and shortest paths between concepts "
        "routinely route around pillar boundaries rather than through them.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F9_pillars.png", 6.6)
figure_caption(d, "Figure 9. Three-pillar multiplex structure. (a) Pillar assignment counts. "
                  "(b) Supra-centrality distributions by pillar. (c) Leading cross-pillar "
                  "bridges within each pillar.")

table_caption(d, "Table 9. Pillar assignment, coupling and leading bridges.")
table(d,
      ["Pillar", "n", "Leading bridges by supra-centrality"],
      [["Governance", "140", "governance, countries, issues, policies, contexts, national olympic, organizations, institutional"],
       ["Innovation", "159", "ecosystem, sustainable, sustained, opportunities, unique, ecological, grassroots, gap"],
       ["Talent", "158", "coaches, psychological, higher, confidence, educational, ability, psychology, identification"],
       ["Unassigned", "212", "structural, mental, athletic, insights, participation, dynamics, gender, olympic"]],
      widths=[0.9, 0.35, 5.1])
figure_caption(d, "Note: boundary-crossing load observed 0.950 against null 0.963 +/- 0.003, "
                  "z = -4.16. Bridges are ranked by supra-centrality, the sum of within-layer "
                  "betweenness across inhabited layers, weighted by intra-layer degree.")

para(d, "The substantive reading requires care. “Governance” and “countries” "
        "bridge within governance; “coaches” and “identification” within talent; "
        "“ecosystem” and “sustainable” within innovation. These are internal "
        "integrators of their own pillars rather than connectors between them. The cross-pillar "
        "evidence is negative: the concept vocabulary of governance, innovation and talent "
        "research does not substantially interpenetrate.")

para(d, "One qualification matters. Thirty-one percent of concepts are unassigned and the "
        "median assignment margin is low, so true integration could in principle fall between "
        "prototypes. We tested this directly: bridging is not pillar-specific (chi-square = 2.40, "
        "p = .30; INNOVATION 30.8%, TALENT 27.8%, GOVERNANCE 22.9% of concepts exceed z = 2.58). "
        "Bridging belongs to the system rather than to any constituent.")

h2(d, "4.11 National research systems (RQ4)")
para(d, "Ten countries meet the minimum support threshold. Canada (50 documents), the United "
        "States (41), Germany (40), Australia (36), the United Kingdom (35), China (34), the "
        "Russian Federation (28), Norway (22), Spain (18) and Switzerland (13) account for 348 "
        "of 448 windowed documents. Topic mix differs significantly across these systems: "
        "chi-square = 180.63, 72 degrees of freedom, p < .001, Cramér's V = 0.267.")

para(d, "Topic-level over-representation is detected in 4 of 69 tested cells (lift > 1.3, "
        "FDR-corrected q < .05): Norway over-represents the talent and identification theme "
        "(lift 6.16), Australia the managerial and technical theme (4.29), China the "
        "systematic and methodological theme (3.43), and the Russian Federation the "
        "governance theme (2.00).")

para(d, "Concept-level analysis is more informative, yielding 27 significant cells from 929 "
        "tested after removing 16 circular demonymic cells (Table 10). Two national profiles "
        "are notably distinctive. Norway, at only 22 documents, is markedly talent-centric: "
        "\u201ctalent identification\u201d at lift 13.41, \u201cidentification\u201d 7.58, "
        "\u201ctalent\u201d 6.46 and \u201cathlete development\u201d 3.87, with "
        "\u201celite\u201d appearing in 86.4% of its documents against 42.7% corpus-wide - "
        "consistent with its distinctive high-performance sport governance tradition. Canada "
        "shows a different profile emphasising \u201csport psychology\u201d (lift 6.12) and "
        "\u201cpractitioners\u201d (4.14), indicating a stronger professional-practice "
        "orientation.")

table_caption(d, "Table 10. National conceptual emphases (lift > 1.3, q < .05; circular "
                 "demonyms excluded).")
table(d,
      ["Country", "n", "Concept", "Share", "Rest", "Lift", "q"],
      [["Norway", "22", "talent identification", "0.409", "0.030", "13.41", "0.003"],
       ["Norway", "22", "identification", "0.409", "0.054", "7.58", "0.007"],
       ["Norway", "22", "talent", "0.545", "0.085", "6.46", "0.001"],
       ["Norway", "22", "athlete development", "0.545", "0.141", "3.87", "0.006"],
       ["Norway", "22", "elite", "0.864", "0.427", "2.02", "0.002"],
       ["Canada", "50", "sport psychology", "0.180", "0.033", "6.12", "0.021"],
       ["Canada", "50", "practitioners", "0.260", "0.063", "4.14", "0.017"],
       ["Australia", "36", "performance sport", "0.444", "0.119", "3.74", "0.002"],
       ["United States", "41", "collegiate", "0.171", "0.010", "17.37", "0.028"],
       ["United Kingdom", "35", "elite", "0.714", "0.426", "1.68", "0.035"]],
      widths=[1.0, 0.3, 1.5, 0.55, 0.5, 0.5, 0.5])
figure_caption(d, "Note: q-values are Benjamini-Hochberg FDR-corrected across the full family "
                  "of 929 tests. Displayed cells are those with lift > 1.3; lifts for "
                  "United States 'collegiate' and the Russian Federation 'standards' reflect "
                  "small denominators.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F11_national.png", 6.6)
figure_caption(d, "Figure 10. National research emphises. (a) Concept families significantly "
                  "over-represented in each national system. (b) Distribution of effect sizes "
                  "across all tested country-by-concept cells, separating significant from "
                  "non-significant cells.")

page_break(d)
d.save(DOC)
print("part5 ok")