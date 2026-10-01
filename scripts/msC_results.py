# -*- coding: utf-8 -*-
"""Part C: Results."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docbuild import *
from docx import Document

d = Document(DOC)

h1(d, "4. Results")

h2(d, "4.1 The corpus")
para(d, "604 documents, of which 448 fall in the 2013-2025 analysis window (Table 1). Articles "
        "(447) and book chapters (95) dominate. Six journals supply the largest shares: "
        "International Journal of Sport Policy and Politics (23), Teoriya i Praktika "
        "Fizicheskoy Kultury (23), Frontiers in Sports and Active Living (21), International "
        "Journal of the History of Sport (19), International Review for the Sociology of Sport "
        "(18), Sport in Society (13). Routledge accounts for 116 documents and Taylor & Francis "
        "for 87, so the corpus leans towards policy and sociology rather than performance "
        "science. There are 1,514 unique authors across 8,024 citations, a median of three "
        "citations per document, and 184 uncited documents.")

h2(d, "4.2 The search string drives frequency")
para(d, "The diagnosis holds. Query terms average 20.4% document frequency against 5.5% for "
        "controls, a ratio of 3.67 (Figure 1). “Athlete” appears in 79.0% of documents, “sport "
        "system” in 54.6%, “elite sport” in 33.0%, while “sport ecosystem” sits at a "
        "corpus-typical 3.6%. The ordering is what identifies the cause: terms appearing across "
        "many disjuncts are inflated hardest, which is a property of query logic rather than of "
        "the field. It also justifies excluding “sport” on logical grounds rather than "
        "empirically.")

h2(d, "4.3 The mined inventory")
para(d, "24,749 candidate nominal n-grams reduce to 1,208 concepts, 1,120 unigrams and 88 "
        "multiwords (Table 2). C1 absorbs the bulk; C2 to C7 remove another 744. What survives "
        "is substantive domain vocabulary (Table 3). The multiword survivors are real domain "
        "expressions: “athlete development” (56 documents), “performance sport” (54), “sport "
        "policy” (53), “national sport” (41), “youth sport” (41), “talent identification” "
        "(31), “mental health” (28), “sport development” (27) and “artificial intelligence” "
        "(14).")

h2(d, "4.4 SEMCON validation")
para(d, "The encoder is severely anisotropic here: mean cosine between random concept pairs is "
        "+0.808 raw, falling to -0.001 after centring, with mean absolute similarity 0.066 "
        "(Figure 2). Uncorrected, every pair would clear any plausible threshold. That one "
        "correction is what makes the rest of the procedure well defined.")

para(d, "Consolidation is correspondingly conservative. Stage 1 takes 1,208 concepts to 1,098 "
        "groups, merging 110 variants; Stage 2 yields 1,041 families, 56 of them multi-member, "
        "the largest holding three. At the rejected threshold of 0.42 complete linkage produced "
        "453 multi-member families with members up to six. Retained merges are defensible: "
        "“athlete performance” with “athletic performance”, “ethical” with “ethics”, "
        "“olympic” with “olympic sports”, “regulation” with “regulatory”, “sustainable” "
        "with “sustainability”, “korean” with “south korean”.")

para(d, "The safety benchmark is saturated and cannot discriminate thresholds, which is why the "
        "audit was needed. Audited precision is erratic below about 0.80 (0.00 at 0.50, 0.40 at "
        "0.60, 0.29 at 0.65, 0.86 at 0.70, 0.71 at 0.75) and perfect at every band from 0.85 up, "
        "where all 45 judged merges were correct. The pre-registered rule gives tau = 0.729 at "
        "cumulative precision 0.957 (Figure 3). The automatic screen flags none of the 56 "
        "multi-member families, so family-construction error is at or below 1.000. It is not "
        "vacuous: at the rejected 0.42 it flags 18 of 453 families, real antonym errors "
        "included. Sweeping the family-size cap from 3 to 12 changes nothing, since no family "
        "exceeds three members.")

para(d, "Agreement between semantic families and independently computed co-occurrence "
        "communities is very low: adjusted Rand 0.002, NMI 0.477. That is not a failure. "
        "Families group concepts meaning the same thing; communities group concepts used "
        "together. The divergence is the useful part, because concepts bridging meaning groups "
        "without co-usage ties are exactly the integrative concepts we are after.")

h2(d, "4.5 A genuine community structure")
para(d, "669 nodes, 5,061 edges, density 0.0226, mean degree 15.1, two isolated nodes. Louvain "
        "peaks at resolution 1.1 with ten communities (Figure 4).")

para(d, "The modularity is not an artefact of the corpus. Observed Q = 0.446 against a "
        "configuration-model null of 0.220 (SD 0.004) over 300 randomisations: z = +64.3, "
        "one-sided p = .003, the smallest attainable with 300 draws. The null is what makes this "
        "claim worth making, since a random graph with the same degrees already reaches 0.220. "
        "Roughly half the raw modularity is degree heterogeneity. The field's community "
        "structure exceeds chance by about a factor of two.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F5_network.png", 6.6)
figure_caption(d, "Figure 4. The concept co-occurrence network, backbone shown for "
                  "legibility. (a) Communities. (b) Bridging concepts labelled by betweenness, "
                  "sized by degree. Ten communities at resolution 1.1; Q = 0.446, z = +64.3.")

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
figure_caption(d, "C8 and C9 are combined for space; the full partition is in Appendix E.")

para(d, "The structure is substantive rather than lexical. Three communities track the field's "
        "established divisions closely: C0 on competition and national systems, C3 on talent and "
        "participation, C5 on governance and organisation. The rest cover performance "
        "measurement, athlete experience and inclusion, strategy and implementation, "
        "transitions, and education.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F6_nullmodel.png", 6.6)
figure_caption(d, "Figure 5. Null-model validation. (a) Modularity across the resolution sweep "
                  "against the configuration-model null band at 2 SD; selected resolution "
                  "marked. (b) Betweenness z against degree, showing large z concentrating at "
                  "low degree where null variance is small. (c) Distribution of observed "
                  "betweenness: integrative positions are rare.")

h2(d, "4.6 Framing versus intellectual infrastructure")
para(d, "The median provenance ratio, a family's title-level share divided by its full-document "
        "share, is 0.083. Only 8.3% of concept mentions appear in titles. The rest sit in "
        "abstracts, doing the intellectual work without signalling front membership.")

para(d, "That is not cosmetic. Spearman correlation of betweenness ranks is 0.713 between titles "
        "and author keywords, but only 0.391 between titles and full text, and 0.439 between "
        "keywords and full text (Figure 6). Titles and keywords agree with each other, being "
        "short, self-selected and written to signal. Neither tracks the full text, where "
        "structural weight concentrates.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F7_layers.png", 6.6)
figure_caption(d, "Figure 6. Concept stratification. (a) Title-layer against full-text "
                  "betweenness (Spearman rho = 0.39); points below the diagonal are "
                  "structurally important but unadvertised. (b) Betweenness against provenance "
                  "ratio, separating buried infrastructure from framing-driven concepts.")

para(d, "Together the two measures give four quadrants. Structurally important and "
        "high-provenance concepts are the ones the field advertises: “coaches”, “athlete "
        "development”, “participation”. Structurally important and low-provenance concepts are "
        "its load-bearing infrastructure, holding the network together while appearing in few "
        "titles. “Framework” is the clearest case, full-text betweenness 0.027 against "
        "title-layer betweenness an order of magnitude lower, and “ecosystem” behaves the same "
        "way. High-provenance, low-structural concepts are framing devices that take up "
        "attention without doing structural work.")

h2(d, "4.7 Bridging concepts")
para(d, "Observed betweenness reaches 0.038 against a null mean of 0.0018, a factor of about "
        "21. Of 669 nodes, 212 exceed z = 1.96, 195 exceed 2.58 and 166 exceed 3.29.")

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
figure_caption(d, "Betweenness is computed on the weighted network. z measures unusualness for "
                  "the degree; because null variance is small at low degree, z can run high "
                  "there, so betweenness rather than z is the effect size.")

para(d, "That caveat matters. Some very low-frequency concepts (“directors”, “inequities”, "
        "both df = 9) reach z above 100 on negligible absolute betweenness, and are excluded "
        "from interpretation.")

para(d, "The real bridges fall into two groups. The first is organisational and systemic "
        "vocabulary joining the competition community to the governance community: "
        "“countries”, “governance”, “structural”, “global”. The second joins "
        "competition to implementation and strategy: “framework”, “ecosystem”, “strategies”, "
        "“challenges”, “implementation”. “Ecosystem” itself is among the strongest, which "
        "says the concept does real work in the literature rather than functioning as rhetoric. "
        "Innovation vocabulary, by contrast, is almost absent from the list.")

h2(d, "4.8 Thematic structure")
para(d, "Eight topics plus a noise cluster covering 16.3% of the windowed corpus (73 of 448 "
        "documents), silhouette 0.484 on the clustered subset, bootstrap co-assignment ARI 0.751 "
        "(SD 0.145, range 0.437-0.882) over twelve replicates. Stability at that level supports "
        "qualitative interpretation but not fine claims about boundaries.")

table_caption(d, "Table 7. Topic prevalence, direction and labels.")
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
figure_caption(d, "Share of the 448-document windowed corpus. Direction derives from the "
                  "emergence scores in Table 8.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F8_topics.png", 6.6)
figure_caption(d, "Figure 7. Topic structure. (a) UMAP projection of document embeddings with "
                  "HDBSCAN partition; unclustered documents in grey. (b) Topic prevalence, "
                  "red for emerging and blue for declining.")

para(d, "The noise share is worth a sentence. These are not failures: HDBSCAN sends documents to "
        "noise precisely because they lie in low-density regions of the manifold. In a corpus "
        "assembled by a Boolean query spanning three conceptual blocks, noise approaching one "
        "sixth points to real heterogeneity at the boundaries, including book chapters on "
        "comparative elite sport systems and conference proceedings sharing vocabulary with "
        "none of the eight themes.")

h2(d, "4.9 Thematic evolution")
para(d, "Composition shifts across periods, though modestly. The topic-by-period table gives "
        "chi-square = 47.18 on 24 degrees of freedom, p = .003, Cramér's V = 0.187 (Figure 8). "
        "Nine of thirty-six cells have expected frequency below 5, which limits what the test "
        "can carry and is why effect size is reported alongside. The effect is real but not "
        "large: around 19% of the variance in topic membership tracks period.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F10_temporal.png", 6.6)
figure_caption(d, "Figure 8. Thematic evolution. (a) Topic prevalence across four periods "
                  "against the corpus total; chi-square = 47.18, V = 0.187. (b) Concept "
                  "frontier: mean publication year against share of mentions since 2021.")

table_caption(d, "Table 8. Emergence and decline scores.")
table(d,
      ["Topic", "n", "Mean year", "Share since 2021", "Emergence", "Direction"],
      [["Socio / mental / limitations", "33", "2022.0", "0.76", "+0.148", "Emerging"],
       ["Physical activity / ecosystem", "50", "2021.7", "0.74", "+0.131", "Emerging"],
       ["Organisational / systematic", "47", "2021.7", "0.72", "+0.114", "Emerging"],
       ["Dual / alternative / landscape", "40", "2021.8", "0.70", "+0.091", "Emerging"],
       ["Capacity / specialization", "21", "2020.7", "0.67", "+0.057", "Stable"],
       ["Networks / talent / psychology", "29", "2020.8", "0.66", "+0.046", "Stable"],
       ["Noise", "73", "2021.1", "0.60", "-0.007", "Stable"],
       ["Covid / committee / psychology", "19", "2020.8", "0.53", "-0.083", "Declining"],
       ["Problems / criteria / governance", "136", "2019.8", "0.46", "-0.153", "Declining"]],
      widths=[1.9, 0.35, 0.7, 0.9, 0.7, 0.7])
figure_caption(d, "Corpus baseline share since 2021 is 0.609. Emergence is the topic's share "
                  "minus that baseline.")

para(d, "Four topics are emerging and two declining. The strongest is socio-cultural and "
        "mental health, mean year 2022.0, emergence +0.148. Then physical activity with "
        "ecosystem concepts (+0.131), organisational themes with a German concentration "
        "(+0.114), and dual or alternative pathways (+0.091). The largest topic in absolute "
        "terms, at 30.4% of the windowed corpus, is the sharpest decliner (-0.153), as is the "
        "pandemic-influenced prevention theme (-0.083).")

para(d, "At concept level the frontier is digital and methodological: “actionable” (2024.6), "
        "“digital” (2024.2), “reflexive” (2024.1), “algorithm” (2024.1), “maltreatment” "
        "(2024.1), “transformation” (2024.0), “equitable” (2024.0). The frontier is "
        "methodologically marked, and the presence of “maltreatment” and “equitable” suggests "
        "safeguarding and equity have become frontier concerns, consistent with the emerging "
        "socio-cultural theme. The most established concepts are “willingness” (2016.6), "
        "“qualities” (2016.8), “specialist” (2017.0), “officials” (2017.3) and “modern "
        "elite” (2017.6), all descriptive or person-centred terms typical of earlier "
        "qualitative work.")

h2(d, "4.10 The pillars are segregated")
para(d, "Assignment places 140 concepts in governance, 159 in innovation, 158 in talent "
        "development and 212 unassigned on the margin rule. The median assignment margin is "
        "0.034 (IQR 0.015-0.074), so many assignments are close calls and should be read as "
        "such.")

para(d, "The integration test is unambiguous. The observed share of shortest paths crossing a "
        "pillar boundary is 0.950, against 0.963 (SD 0.003) under degree-preserving "
        "randomisation of pillar labels: z = -4.16 (Figure 9). Conceptual traffic between "
        "pillars runs significantly below chance, and shortest paths route around boundaries "
        "rather than through them.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F9_pillars.png", 6.6)
figure_caption(d, "Figure 9. Three-pillar multiplex. (a) Assignment counts. (b) Supra-centrality "
                  "by pillar. (c) Leading bridges within each pillar.")

table_caption(d, "Table 9. Pillar assignment and leading bridges.")
table(d,
      ["Pillar", "n", "Leading bridges by supra-centrality"],
      [["Governance", "140", "governance, countries, issues, policies, contexts, national olympic, organizations, institutional"],
       ["Innovation", "159", "ecosystem, sustainable, sustained, opportunities, unique, ecological, grassroots, gap"],
       ["Talent", "158", "coaches, psychological, higher, confidence, educational, ability, psychology, identification"],
       ["Unassigned", "212", "structural, mental, athletic, insights, participation, dynamics, gender, olympic"]],
      widths=[0.9, 0.35, 5.1])
figure_caption(d, "Boundary-crossing load observed 0.950, null 0.963 (SD 0.003), z = -4.16. "
                  "Bridges ranked by supra-centrality.")

para(d, "Read carefully, these are internal integrators. “Governance” and “countries” bridge "
        "within governance, “coaches” and “identification” within talent, “ecosystem” and "
        "“sustainable” within innovation. The cross-pillar evidence is negative: the concept "
        "vocabulary of the three literatures does not substantially interpenetrate.")

para(d, "One caveat deserves weight. With 31% unassigned and a thin median margin, real "
        "integration could in principle sit between prototypes. We tested that: bridging is not "
        "pillar-specific (chi-square = 2.40, p = .30; innovation 30.8%, talent 27.8%, governance "
        "22.9% of concepts above z = 2.58). Bridging belongs to the system rather than to any "
        "one constituent.")

h2(d, "4.11 National systems")
para(d, "Ten countries clear the support threshold: Canada (50), United States (41), Germany "
        "(40), Australia (36), United Kingdom (35), China (34), Russian Federation (28), "
        "Norway (22), Spain (18), Switzerland (13), accounting for 348 of 448 windowed "
        "documents. Topic mix differs significantly: chi-square = 180.63, 72 degrees of "
        "freedom, p < .001, V = 0.267.")

para(d, "At topic level, 4 of 69 tested cells show over-representation (lift > 1.3, q < .05). "
        "Norway runs high on talent and identification (6.16), Australia on managerial and "
        "technical themes (4.29), China on systematic and methodological themes (3.43), Russia "
        "on governance themes (2.00).")

para(d, "Concept level says more, with 27 significant cells from 929 tested once 16 circular "
        "demonymic cells are removed (Table 10). Two profiles stand out. Norway, on 22 "
        "documents, is markedly talent-centric: “talent identification” lift 13.41, "
        "“identification” 7.58, “talent” 6.46, “athlete development” 3.87, with “elite” "
        "in 86.4% of its documents against 42.7% corpus-wide, matching its distinctive "
        "high-performance governance tradition. Canada leans different, with “sport psychology” "
        "(6.12) and “practitioners” (4.14), pointing to a stronger professional-practice "
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
figure_caption(d, "q-values are Benjamini-Hochberg corrected across all 929 tests. Displayed "
                  "cells have lift > 1.3. The large lifts for “collegiate” and Russia’s "
                  "“standards” reflect small denominators.")

figure(d, r"D:\Uni of Birjand\articles\adel\article1\figures\F11_national.png", 6.6)
figure_caption(d, "Figure 10. National emphases. (a) Concept families significantly "
                  "over-represented in each system. (b) Effect-size distribution across all "
                  "tested country-by-concept cells, significant against not.")

page_break(d)
d.save(DOC)
print("partC ok")