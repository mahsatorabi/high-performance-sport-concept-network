# -*- coding: utf-8 -*-
"""Part 6: Discussion, limitations, conclusion, references."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docbuild import *
from docx import Document

d = Document(DOC)

h1(d, "5. Discussion")

h2(d, "5.1 What the intellectual structure of high-performance sport actually looks like")
para(d, "High-performance sport research is a genuine community structure rather than an "
        "integrated discourse or a diffuse field. Modularity of 0.446 against a degree-preserving "
        "null of 0.220 (z = +64.3) cannot be explained by corpus composition, and the ten "
        "communities that emerge map recognisably onto the field's established divisions: "
        "competition and national systems (C0), performance measurement and intervention (C1), "
        "athlete experience and inclusion (C2), talent and participation (C3), strategy and "
        "implementation (C4), governance and organisation (C5).")

para(d, "This bears directly on how the ecosystem question should be posed. If the field were "
        "integrated, we would expect weak community structure and a high boundary-crossing "
        "rate. We observe the opposite on both counts. The appropriate formulation is therefore "
        "not whether high-performance sport is an ecosystem, but at what level integration "
        "operates - and the evidence indicates that it operates within communities rather than "
        "between them.")

h2(d, "5.2 The field's structural concepts are invisible in its own framing")
para(d, "The second conclusion concerns a dissociation between where a field concentrates its "
        "communicative effort and where its structure resides. Only 8.3% of concept mentions "
        "occur in titles, and title-level betweenness correlates with full-text betweenness at "
        "rho = 0.39. Titles and author keywords agree closely with each other (rho = 0.71) but "
        "neither agrees with the full text.")

para(d, "Title-level and keyword-level metadata function as signalling devices, and the "
        "concepts carrying structural weight - \u201cframework\u201d, \u201cecosystem\u201d, "
        "\u201cimplementation\u201d, \u201cstructural\u201d - are systematically "
        "under-signalled relative to their structural importance. This has practical "
        "consequences: reviewers and editors allocate attention on the basis of titles and "
        "keywords, so if integrative concepts are less visible there, integrative work is less "
        "likely to be funded, published centrally or recognised. Conversely, concepts "
        "appearing frequently in titles without structural weight consume attention without "
        "doing structural work.")

para(d, "This dissociation also explains the field's slow progress on systems thinking. The "
        "ecosystem framing is genuinely integrative in the network - \u201cecosystem\u201d has "
        "betweenness 0.024 and z = +16.5 - but it is largely buried rather than structural. A "
        "concept can be integrative within a body of work without that work being organised "
        "around it.")

h2(d, "5.3 Segregation of the pillars: the ecosystem framing is aspirational")
para(d, "The most consequential conclusion concerns how the thesis motivating this research "
        "should be stated. The governance, innovation and talent-development pillars are "
        "statistically segregated: conceptual traffic between them is significantly below "
        "chance (z = -4.16). The ecosystem framing is thus a prescription for how "
        "high-performance sport systems should be organised, not a description of how the "
        "scholarship has developed.")

para(d, "This does not show that the pillars are substantively independent in practice, nor "
        "that integration is theoretically incoherent. It shows that the research literature does "
        "not currently articulate the relationships between them: if it did, the associated "
        "concepts would co-occur and cross-pillar shortest paths would not be depleted relative "
        "to chance. The test converts an assumption into an open question, and in doing so "
        "identifies integration as a research gap.")

para(d, "A plausible mechanism explains the segregation. Each pillar has its own dominant "
        "methodological community and outlet: governance research draws on policy analysis and "
        "comparative case study, talent research on longitudinal design and qualitative "
        "interview, innovation research on instrumentation and computational methods. Innovation "
        "is the most distinctive case, since AI and wearable research is frequently reported as "
        "an instrument for governance decisions or talent selection rather than as a distinct "
        "institutional domain (Li, 2023; Taheri et al., 2025), suggesting it is conceptually "
        "subsumed within the other two. The corpus supports this: the innovation pillar contains "
        "no top-twenty bridging concepts.")

h2(d, "5.4 Bridging belongs to the system, not to any single pillar")
para(d, "An initial reading of our own results suggested that bridging concepts concentrated in "
        "governance vocabulary, which would have implied that governance is the field's "
        "integrative core. We tested this and it did not hold: the rate of significant bridging "
        "does not differ across pillars (chi-square = 2.40, p = .30). We report this because the "
        "result is more interesting than the one it replaced. If bridging is distributed evenly "
        "across the pillars rather than concentrated in one, then integration is a property of "
        "the system rather than of any constituent, and it should be modelled at the system "
        "level. This has a direct consequence for the conceptual modelling pursued in the "
        "companion paper: a model that treats governance, innovation and talent development as "
        "three parallel sub-systems would misdescribe the bridging structure we observe.")

h2(d, "5.5 National systems as differentiated research cultures")
para(d, "Cross-national differences are substantial (chi-square = 180.6, V = 0.267) and are "
        "substantively interpretable. The Norwegian profile is talent-centric: \u201ctalent "
        "identification\u201d appears at lift 13.4, and \u201celite\u201d occurs in 86.4% of "
        "Norwegian documents against 42.7% corpus-wide. This accords with its distinctive "
        "high-performance governance tradition and long-standing investment in a unified "
        "national pathway. Canada emphasises \u201csport psychology\u201d and "
        "\u201cpractitioners\u201d, indicating a stronger professional-practice orientation. "
        "Australia over-represents \u201cperformance sport\u201d (lift 3.74).")

para(d, "This matters for policy transfer. If national systems emphasise different concepts, "
        "then evidence about high-performance sport governance does not generalise "
        "automatically across them, and comparative benchmarking requires conceptual alignment "
        "that is currently absent. It also suggests that concept-level analysis can contribute "
        "to the policy-transfer literature by identifying where systems are conceptually "
        "aligned and where they are not.")

h2(d, "5.6 Contribution to knowledge mapping methodology")
para(d, "The methodological contribution is independent of the substantive findings and is the "
        "more transferable. Four elements merit adoption. First, the query-artefact diagnosis: "
        "a single-query retrieval inflates its own vocabulary 3.67-fold relative to matched "
        "controls, and the inflation is predictable from query logic, since terms appearing in "
        "many disjuncts are most inflated. Any co-word analysis of a bounded domain retrieved "
        "with a structured query is subject to this, and it determines the identity of the "
        "resulting network's hubs.")

para(d, "Second, the anisotropy correction: mean cosine between semantically unrelated concept "
        "pairs was +0.808 under raw neural embeddings, falling to -0.001 after mean-centring. "
        "This is not a subtle degradation - it renders the similarity matrix uninformative, and "
        "anyone applying embedding-based consolidation without it will obtain results determined "
        "by the encoder's geometry rather than by the domain. Third, the failure of connected "
        "components, where a single spurious edge merged 132 concepts and destroyed an "
        "integrative concept; complete linkage makes chaining structurally impossible.")

para(d, "Fourth, and most generally useful, the principle that structural claims require stated "
        "nulls. Roughly half the raw modularity value in this network (0.220 of 0.446) is "
        "generated by degree heterogeneity alone. Any bibliometric study reporting modularity "
        "or centralities without a degree-preserving null is reporting a quantity whose "
        "substantive interpretation is undetermined.")

h2(d, "5.7 Implications for practice")
para(d, "For sport policy organisations, the segregation finding suggests that integrative "
        "frameworks require deliberate construction rather than emergence. If the research and "
        "practice literatures do not connect governance, innovation and talent development, "
        "then policy frameworks asserting their interdependence are imposing an integration "
        "that the knowledge base does not yet support, and should specify the mechanisms by "
        "which integration is expected to occur. The national differentiation finding "
        "additionally suggests that frameworks should not be transferred across systems without "
        "conceptual alignment.")

para(d, "For research design, the bridging results identify where intervention is most "
        "plausible. Concepts connecting the competition community (C0) to the governance "
        "community (C5) - 'countries', 'governance', 'structural', 'global' - and those "
        "connecting C0 to implementation (C4) - 'framework', 'ecosystem', 'strategies', "
        "'implementation' - are where cross-community work would most change the structure of "
        "the field. The absence of innovation vocabulary from this list suggests that "
        "technology-focused research currently reaches governance and talent literatures "
        "through practice settings rather than through scholarly channels.")

h2(d, "5.8 Limitations")
para(d, "Six limitations are material.")

h2(d, "5.8.1 Single database, single query, small corpus")
para(d, "The corpus derives from one query against one database (Scopus). Single-query retrieval "
        "is the source of the artefact we correct for, and correcting it does not recover the "
        "documents the query missed. At 604 documents (448 in the window), the corpus is small by "
        "bibliometric standards, where studies commonly analyse 1,500-4,000 documents. Four "
        "consequences follow: community structure rests on 669 nodes, so boundary membership is "
        "unstable and the ten-community solution should not be treated as canonical; expected "
        "cell counts fall below 5 in nine of thirty-six topic-by-period cells, which is why we "
        "report effect size and treat the temporal test as indicative; cross-national tests rest "
        "on ten countries, with Norway (22 documents) and Switzerland (13) contributing few, so "
        "national profiles are fragile even where significant; and topic stability of ARI 0.751 "
        "supports qualitative interpretation but not fine-grained boundary claims. We regard the "
        "methodological contributions as portable to larger corpora and the substantive findings "
        "as appropriately preliminary.")

h2(d, "5.8.2 Language and document-type composition")
para(d, "Sixty-one records (10.1%) are indexed as non-English, principally Russian-language "
        "journals. Scopus supplies English-language abstracts for most of these, so they were "
        "retained; titles and keywords for some are not in English, and residual non-English "
        "tokens were filtered as cross-lingual noise. The concentration of Routledge (116) and "
        "Taylor & Francis (87) titles orients the corpus toward policy and sociology "
        "scholarship relative to performance science, which likely understates the innovation "
        "pillar.")

h2(d, "5.8.3 Pillar assignment")
para(d, "The three-pillar partition rests on cosine similarity to 15 textual prototypes, with "
        "31.2% of concepts unassigned and a median assignment margin of only 0.034. The "
        "segmentation result is robust in the sense that bridging rates do not differ across "
        "pillars, but individual assignments should not be treated as definitive. A supervised "
        "classifier trained on expert-labelled concepts would be required for stronger claims.")

h2(d, "5.8.4 Association is not causation; no outcome variable")
para(d, "Co-occurrence establishes that concepts appear in the same documents. It does not "
        "establish that research on one concept influences research on another, nor that either "
        "reflects properties of real-world sport systems. All structural findings here are claims "
        "about a literature, not about sport systems as such. Further, the corpus contains no "
        "performance outcome, so we make no claims about whether governance arrangements, "
        "innovation or talent development affect sporting success; none of the analyses here "
        "could support such claims. This is stated explicitly because the framing that motivates "
        "such extrapolation is precisely what our results caution against.")

h2(d, "5.9 Future research")
para(d, "Three directions follow. First, replication on a larger corpus and a second database "
        "would establish whether the modularity and segregation findings hold. Second, the "
        "query-artefact correction and null-calibration procedures should be applied to existing "
        "sport bibliometric analyses, several of which report centrality without a null; the "
        "degree to which their conclusions survive is an empirical question in itself. Third, "
        "the relationship between conceptual structure and substantive outcomes requires data "
        "this design cannot provide, and remains the central open question about whether the "
        "ecosystem framing describes or prescribes.")

h1(d, "6. Conclusion")
para(d, "We constructed and validated a concept network for high-performance sport research and "
        "tested three claims implicit in its characterisation as an ecosystem. The field is "
        "modular beyond chance (Q = 0.446, z = +64.3), confirming it as a genuine community "
        "structure. Its integrative concepts are largely invisible in its own framing: only 8.3% "
        "of concept mentions occur in titles and title-level centrality correlates weakly with "
        "full-text centrality (rho = 0.39). And its three commonly asserted pillars are "
        "statistically segregated, with cross-pillar conceptual traffic below chance (z = -4.16), "
        "while bridging is distributed evenly across them rather than concentrated in any one. "
        "The ecosystem framing is therefore best understood as a prescription rather than a "
        "description of the current literature, and integration is better characterised as a "
        "research gap than as an established property.")
para(d, "Methodologically, the pipeline addresses four problems affecting concept-network "
        "analysis generally: single-query retrieval inflating its own vocabulary 3.67-fold; "
        "neural embeddings too anisotropic (+0.808 mean random-pair cosine) to support semantic "
        "consolidation; connected components chaining semantically incoherent families; and "
        "structural claims reported without degree-preserving nulls, against which roughly half "
        "the observed modularity in a typical concept network is attributable to degree "
        "heterogeneity alone. The procedure is validated by hand adjudication and released as a "
        "reproducible nine-stage pipeline. We consider the methodological contribution the more "
        "durable result, since the substantive findings are bounded by a corpus of 604 "
        "documents.")

page_break(d)
d.save(DOC)
print("part6 ok")