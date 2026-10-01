# -*- coding: utf-8 -*-
"""Part D: Discussion, limitations, conclusion, references, declarations."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docbuild import *
from docx import Document

d = Document(DOC)

h1(d, "5. Discussion")

h2(d, "5.1 The shape of the field")
para(d, "High-performance sport research is a real community structure, not an integrated "
        "discourse and not a diffuse field. Modularity of 0.446 against a null of 0.220 "
        "(z = +64.3) cannot be put down to how the corpus was assembled, and the ten communities "
        "map onto recognisable divisions: competition and national systems, performance "
        "measurement, athlete experience and inclusion, talent and participation, strategy and "
        "implementation, governance and organisation.")

para(d, "That settles how the ecosystem question should be put. An integrated field would show "
        "weak community structure and frequent boundary crossing. We see the reverse on both "
        "counts. The useful question is not whether high-performance sport is an ecosystem but "
        "at what level integration operates, and the evidence puts it inside communities rather "
        "than between them.")

h2(d, "5.2 Where the field is structurally invisible")
para(d, "Only 8.3% of concept mentions appear in titles, and title-level betweenness "
        "correlates with full-text betweenness at rho = 0.39. Titles and keywords agree closely "
        "with each other (0.71) because both are short, self-selected and written to signal; "
        "neither tracks the full text.")

para(d, "Titles and keywords function as signalling devices, and the concepts carrying "
        "structural weight, “framework”, “ecosystem”, “implementation”, "
        "“structural”, are under-signalled against their structural importance. Editors and "
        "reviewers allocate attention on titles and keywords, so integrative work is less likely "
        "to be funded, published centrally or noticed. The reverse also happens: concepts that "
        "show up in titles without matching structural weight take up attention without earning "
        "it.")

para(d, "This also goes some way towards explaining why systems thinking has advanced slowly. "
        "The ecosystem framing is genuinely integrative in the network, with betweenness 0.024 "
        "and z = +16.5, but it sits buried rather than structural. A concept can be integrative "
        "within a body of work without that work being organised around it.")

h2(d, "5.3 Segregation: the framing is aspirational")
para(d, "The most consequential result concerns how the thesis motivating this work should be "
        "stated. Governance, innovation and talent development are statistically segregated: "
        "traffic between them runs below chance (z = -4.16). Ecosystem language is a "
        "prescription about how sport systems should be organised, not a description of how the "
        "scholarship developed.")

para(d, "This does not show the pillars are independent in practice, nor that integration is "
        "incoherent. It shows the literature does not currently articulate the relationships "
        "between them. Had it done so, the concepts would co-occur and cross-pillar shortest "
        "paths would not be depleted relative to chance. The test converts an assumption into an "
        "open question and, in doing so, locates a research gap.")

para(d, "The mechanism is not hard to guess. Each pillar has its own dominant methodological "
        "community and outlet: governance draws on policy analysis and comparative case study, "
        "talent on longitudinal design and qualitative interview, innovation on instrumentation "
        "and computation. Innovation is the most distinctive case, since AI and wearable "
        "research is usually reported as an instrument for governance or for talent selection "
        "rather than as a domain in its own right (Li, 2023; Taheri et al., 2025). The corpus "
        "fits: the innovation pillar holds no top-twenty bridging concepts.")

h2(d, "5.4 Bridging belongs to the system")
para(d, "An early reading of our own results suggested bridges concentrated in governance "
        "vocabulary, which would have made governance the integrative core. Testing it, the "
        "claim failed: bridging rates do not differ across pillars (chi-square = 2.40, p = .30). "
        "The surviving result is more useful than the one it replaced. If bridging is spread "
        "evenly across pillars rather than concentrated in one, integration belongs to the "
        "system rather than to any constituent, and should be modelled at that level. The "
        "conceptual model in the companion paper follows this: a design with three parallel "
        "sub-systems would misdescribe the bridging we observe.")

h2(d, "5.5 National cultures")
para(d, "Cross-national differences are substantial (chi-square = 180.6, V = 0.267) and "
        "interpretable. Norway's talent-centric profile, with “talent identification” at lift "
        "13.4 and “elite” in 86.4% of its documents, fits its high-performance governance "
        "tradition and long investment in a unified pathway. Canada emphasises “sport "
        "psychology” and “practitioners”, suggesting a stronger professional-practice "
        "orientation. The United States over-represents “collegiate”, reflecting an "
        "institutional model with no counterpart elsewhere. These are differentiated research "
        "cultures answering to different arrangements, not copies of one agenda.")

para(d, "That matters for policy transfer. If systems emphasise different concepts, evidence "
        "about high-performance governance does not carry across them automatically, and "
        "comparative benchmarking needs conceptual alignment that does not currently exist. It "
        "also suggests concept-level analysis can help the policy-transfer literature by showing "
        "where systems line up and where they do not.")

h2(d, "5.6 What the method adds")
para(d, "The methodological contribution stands apart from the findings and travels better. "
        "Four elements are worth adopting.")

para(d, "The query-artefact diagnosis comes first. Single-query retrieval inflates its own "
        "vocabulary 3.67-fold against matched controls, and the inflation is predictable from "
        "query logic, since terms spread across many disjuncts inflate hardest. Every co-word "
        "analysis of a bounded domain retrieved this way is affected, and it determines who ends "
        "up at the centre of the network.")

para(d, "Second, the anisotropy correction. Mean cosine between unrelated concepts was +0.808 "
        "raw and -0.001 after mean-centring. This is not a subtle degradation; it renders the "
        "similarity matrix uninformative, and anyone consolidating embeddings without it will be "
        "reading the encoder's geometry rather than the domain. Third, connected components "
        "chain: one spurious edge merged 132 concepts and destroyed an integrative concept. "
        "Complete linkage makes that impossible.")

para(d, "Fourth, structural claims need stated nulls. Roughly half the raw modularity here, "
        "0.220 out of 0.446, comes from degree heterogeneity alone. Reporting modularity or "
        "centralities without a degree-preserving null leaves the substantive interpretation "
        "undetermined.")

h2(d, "5.7 For practice")
para(d, "If the literatures do not connect, policy frameworks asserting that governance, "
        "innovation and talent development are interdependent are imposing an integration the "
        "knowledge base does not yet support, and should say how the integration is supposed to "
        "happen. The national differentiation result adds that such frameworks should not be "
        "transferred across systems without checking conceptual alignment. On the research "
        "side, the bridges that do exist point to where intervention would change the field's "
        "structure: vocabulary joining competition (C0) to governance (C5), and competition to "
        "implementation (C4). The absence of innovation vocabulary from that list suggests "
        "technology research reaches the other two through practice settings rather than "
        "scholarly channels.")

h2(d, "5.8 Limitations")
h2(d, "5.8.1 Single query, single database, small corpus")
para(d, "The corpus comes from one query against one database. Single-query retrieval is the "
        "source of the artefact we correct for, and correcting it does not recover what the "
        "query missed. At 604 documents, 448 in the window, it is small by bibliometric "
        "standards, where 1,500 to 4,000 is typical, and four things follow. Community structure "
        "rests on 669 nodes, so boundary membership is unstable and the ten-community solution "
        "should not be treated as canonical. Expected cell counts fall below 5 in nine of "
        "thirty-six topic-by-period cells, which is why effect size is reported and the temporal "
        "test treated as indicative. Cross-national work covers ten countries, with Norway (22) "
        "and Switzerland (13) thin, so national profiles stay fragile even where significant. "
        "Topic stability of ARI 0.751 supports qualitative reading, not boundary claims. The "
        "methodological contributions should transfer to larger corpora; the substantive findings "
        "are preliminary.")

h2(d, "5.8.2 Language and document-type composition")
para(d, "Sixty-one records (10.1%) are non-English, mostly Russian-language journals. Scopus "
        "supplies English abstracts for most, so they were kept; titles and keywords for some "
        "are not English and residual tokens were filtered as cross-lingual noise. Routledge "
        "(116) and Taylor & Francis (87) titles lean the corpus towards policy and sociology, "
        "which probably understates the innovation pillar.")

h2(d, "5.8.3 Pillar assignment")
para(d, "The partition rests on cosine similarity to fifteen prototypes, with 31.2% unassigned "
        "and a median margin of 0.034. Segregation is robust in the sense that bridging rates do "
        "not differ across pillars, but individual assignments are not definitive. A supervised "
        "classifier trained on expert-labelled concepts would be needed for stronger claims.")

h2(d, "5.8.4 Association is not causation, and there is no outcome variable")
para(d, "Co-occurrence shows that concepts appear in the same documents. It does not show that "
        "research on one shapes research on another, nor that either reflects properties of real "
        "sport systems. Every structural claim here is about a literature, not about sport "
        "systems as such. The corpus also contains no performance outcome, so we make no claims "
        "about whether governance, innovation or talent development affect sporting success, and "
        "nothing here could support such claims. That is worth stating plainly, because the "
        "framing that invites the extrapolation is exactly what these results warn against.")

h2(d, "5.9 Future research")
para(d, "Three directions. Replicating on a larger corpus and a second database would show "
        "whether the modularity and segregation findings hold. Applying the query-artefact "
        "correction and null calibration to existing sport bibliometric studies, several of which "
        "report centrality without a null, would establish how much of their interpretation "
        "survives. Linking conceptual structure to outcome data, which this design cannot do, "
        "remains the central open question about whether the ecosystem framing describes or "
        "prescribes.")

h1(d, "6. Conclusion")
para(d, "We built and validated a concept network for high-performance sport research and used "
        "it to test three claims embedded in its description as an ecosystem. The field is "
        "modular beyond chance (Q = 0.446, z = +64.3). Its integrative concepts are largely "
        "missing from its own framing: 8.3% of mentions occur in titles, and title-level "
        "centrality tracks full-text centrality at rho = 0.39. And its three commonly asserted "
        "pillars are segregated, with cross-pillar traffic below chance (z = -4.16) while "
        "bridging sits evenly across them rather than in any one. The ecosystem framing is best "
        "read as a prescription rather than a description, and integration is a research gap "
        "rather than an established property.")
para(d, "Methodologically, the pipeline addresses four problems affecting concept-network "
        "analysis generally: single-query retrieval inflating its own vocabulary 3.67-fold; "
        "embeddings too anisotropic (+0.808 mean random-pair cosine) to consolidate anything "
        "without mean-centring; connected components chaining incoherent families; and "
        "structural claims reported without nulls, against which roughly half the apparent "
        "modularity in a typical network is degree heterogeneity. It is validated by hand "
        "adjudication and released as a nine-stage pipeline. The methodological result is the "
        "more durable of the two, since the findings are bounded by 604 documents.")

page_break(d)
d.save(DOC)
print("partD ok")