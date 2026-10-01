# -*- coding: utf-8 -*-
"""Part A: title, abstract, highlights, Introduction, Literature review.
Rewritten for a more natural academic voice and a tighter word budget."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docbuild import *

d = new_doc()

title(d, "Mapping the Intellectual Structure of High-Performance Sport Ecosystem "
         "Research: A Null-Calibrated Co-Word and Thematic-Evolution Analysis of "
         "Governance, Innovation and Talent Development, 2013-2025")

para(d, "[Author names and affiliations]", indent=False, align=WD_ALIGN_PARAGRAPH.CENTER,
     size=11, italic=True)

# ---------------------------------------------------------------- ABSTRACT
h1(d, "Abstract")
para(d, "High-performance sport is routinely described as an ecosystem in which governance, "
        "innovation and talent development reinforce one another. Whether the research "
        "literature actually works that way is a separate question, and one that has not been "
        "asked, because the concepts that would define such a system have never been measured "
        "as a structure. This study builds such a measurement for the field and uses it to test "
        "the claim.", indent=False)
para(d, "A Scopus corpus of 604 records (448 published between 2013 and 2025) was turned into a "
        "concept network in three steps: a part-of-speech-constrained term-mining cascade; a new "
        "consolidation procedure, SEMCON, which merges morphological variants deterministically "
        "and then clusters the remaining lexical synonymy by complete linkage over "
        "anisotropy-corrected neural embeddings; and a degree-preserving bipartite null model "
        "that decides which co-occurrences count as edges. Every structural claim is then "
        "checked against a configuration-model null over 300 randomisations. Thematic change is "
        "measured with UMAP and HDBSCAN topic modelling; national differences with "
        "false-discovery-rate-corrected proportion tests.", indent=False)
para(d, "Three results stand out. The network is markedly modular (Q = 0.446, against a null of "
        "0.220 with SD 0.004; z = +64.3, p < .004), so the field is a genuine community "
        "structure. Yet the concepts holding that structure together are largely missing from "
        "how the field describes itself: only 8.3% of concept mentions occur in titles, and "
        "title-level betweenness tracks full-text betweenness at just rho = 0.39. Third, the "
        "three pillars are segregated. Shortest paths between concepts cross pillar boundaries "
        "less often than chance would predict (0.950 observed, 0.963 null, z = -4.16). The "
        "ecosystem framing turns out to be prescriptive rather than descriptive. Cross-national "
        "differences are real (topic by country chi-square = 180.6, V = 0.267, p < .001).",
     indent=False)
para(d, "The methods matter as much as the findings. A single-query search inflates its own "
        "vocabulary 3.67-fold relative to matched controls. Connected components over a "
        "thresholded similarity graph chain nonsense. Raw neural embeddings are too anisotropic "
        "(+0.81 mean cosine between unrelated concepts) to consolidate anything without "
        "mean-centring. SEMCON addresses all three and is calibrated by hand adjudication of 95 "
        "sampled merges (audited precision 0.957).", indent=False)

p = d.add_paragraph()
p.paragraph_format.line_spacing = 2.0
p.paragraph_format.first_line_indent = Cm(1.27)
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r = p.add_run("Keywords: ")
r.bold = True; r.font.size = Pt(12)
r2 = p.add_run("high-performance sport; sport policy; science mapping; co-word analysis; "
               "concept networks; null models; text mining; talent development; sport "
               "innovation")
r2.font.size = Pt(12)

h1(d, "Highlights")
bullet(d, "The high-performance sport concept network is significantly modular "
          "(z = +64.3 against a degree-preserving null).")
bullet(d, "Governance, innovation and talent development are segregated literatures, not an "
          "integrated ecosystem.")
bullet(d, "Only 8.3% of concept mentions appear in titles; integrative concepts are "
          "structurally invisible in the field's framing.")
bullet(d, "Single-query retrieval inflates search-string vocabulary 3.67-fold and distorts "
          "conventional co-word networks.")
bullet(d, "SEMCON, validated by hand adjudication, is released as a reproducible standard for "
          "concept networks in bounded corpora.")

page_break(d)

# ================================================================ 1 INTRODUCTION
h1(d, "1. Introduction")

para(d, "High-performance sport is usually studied as a system. The SPLISS project reduced "
        "forty years of comparative case literature to nine interacting policy pillars, from "
        "public funding and governance through talent identification, coaching and facilities to "
        "competition and scientific research (De Bosscher et al., 2006), and the model has "
        "since been applied in more than twenty national systems (Houlihan & Green, 2008). "
        "Organisational researchers reach for much the same picture from a different direction, "
        "placing performance where macro-level political economy, meso-level policy capacity and "
        "micro-level athlete development meet (Sotiriadou et al., 2008). More recently, "
        "innovation studies have lent sport their ecosystem vocabulary, and the analogy has "
        "spread (cf. Adner, 2017). The premise running through all of it is that outcomes come "
        "from interaction.")

para(d, "That premise has a testable implication, and nobody has tested it. If the three "
        "domains really are one system, the scholarship should show it. Concepts from different "
        "pillars ought to be strongly associated with one another, and a handful of integrative "
        "concepts ought to bind them into something whole. If instead we find three parallel "
        "literatures, each internally coherent and only lightly connected, then ecosystem "
        "language is a prescription about how sport systems should be run rather than a "
        "description of how the field has grown. The distinction matters, because it decides "
        "whether the next step is theoretical integration or an attempt to build the connections "
        "that are missing.")

para(d, "The obvious reason nobody has done this is that the relevant concepts have never been "
        "operationalised as a measurable structure. Sport policy scholarship has mapped national "
        "systems carefully, above all through SPLISS. Athlete development has been reviewed "
        "repeatedly, most recently an umbrella review of sixty systematic reviews (Johnston et "
        "al., 2017; Descheemaeker et al., 2025). Those are reviews of substantive claims, though, "
        "not of the literature's own organisation. What is missing is a representation of the "
        "conceptual structure that is explicit, reproducible and comparable against what the "
        "ecosystem model predicts.")

para(d, "Science mapping is the obvious tool. Co-word analysis reconstructs a field's concepts "
        "from the terms that co-occur across its documents (Callon et al., 1986; He, 1999), and "
        "it has been applied to sport before (Wollny et al., 2023; Liu et al., 2024). It suits "
        "this question because what we want to know about is conceptual rather than citational. "
        "Applied to a bounded domain, though, it runs into a specific difficulty, and we want to "
        "name it here because it shapes much of what follows.")

para(d, "A domain literature is nearly always found with one structured query, which means the "
        "query's own vocabulary sits inside a large and unrandom share of the results. In our "
        "corpus, terms lifted straight from the search string run about 3.67 times as frequent as "
        "matched control terms, and the phrase “sport system” on its own appears in 54.6% of "
        "documents. Conventional co-word analysis takes the most frequent terms as the field's "
        "core concepts. Run naively here, it hands back the search string dressed up as a "
        "finding.")

para(d, "Synonymy compounds the problem. Co-word networks built on surface strings fragment: "
        "“talent development”, “athlete development” and “talent pipeline” mean much the "
        "same thing but occupy separate nodes, which both breaks the network apart and spreads "
        "the centrality of integrative concepts thinly across near-duplicates. The usual fix is a "
        "hand-built synonym dictionary, which does not scale and does not transfer across "
        "domains. We use a two-stage procedure instead (SEMCON). The first stage handles "
        "morphological and orthographic variation with rules, so it cannot make mistakes. The "
        "second handles the rest by cosine similarity between neural sentence embeddings under "
        "complete linkage. Section 3.6 gives the validation, including two approaches that failed "
        "before this one worked, since both failures look likely to recur in anyone else's data.")

para(d, "A third difficulty has to do with what claims are licensed. Sports science reports "
        "centralities and clusterings fairly often without saying whether the structure is any "
        "different from chance. But every co-occurrence network shows some modularity and has "
        "some hubs, simply because the documents came from a partitioned field in the first "
        "place. Saying a field is modular, or a concept integrative, only means something "
        "against a stated null. Here every structural claim is tested against a degree-preserving "
        "null: a bipartite swap model for edges, a configuration model for modularity and "
        "centrality.")

para(d, "The study asks four questions. Two concern structure:", indent=False)
para(d, "RQ1. What is the conceptual structure of high-performance sport research as a concept "
        "network, and which concepts are integrative? Is the network modular relative to a "
        "degree-preserving null, and which concepts occupy significantly bridging positions?",
     indent=False)
para(d, "RQ2. How does the thematic composition of the field evolve across the governance, "
        "innovation and talent-development pillars, and which concepts sit at its frontier?",
     indent=False)
para(d, "Two concern integration and difference:", indent=False)
para(d, "RQ3. Do the three pillars form an integrated conceptual system, or parallel literatures "
        "with limited interconnection?", indent=False)
para(d, "RQ4. How do national research systems differ in the concepts and topics they "
        "over-represent?", indent=False)

para(d, "Three contributions follow. On methods, we show that co-word analysis of a "
        "single-query bounded corpus is materially distorted by its own retrieval instrument, "
        "measure the distortion, and supply a corrected procedure that has been validated. On "
        "substance, we establish that the literature is modular while its three commonly "
        "asserted pillars are statistically segregated, which turns ecosystem integration "
        "from a settled fact into an open question. On practice, we identify which concepts "
        "actually carry cross-pillar associations, giving the conceptual modelling in the "
        "companion paper something firmer than intuition to work from.")

page_break(d)

# ================================================================ 2 LITERATURE REVIEW
h1(d, "2. Literature review")

h2(d, "2.1 The high-performance sport system as an object of study")
para(d, "The SPLISS model remains the most systematic attempt to specify what a functioning "
        "national elite sport system requires. Its value for present purposes lies in "
        "decomposing a system into interdependent policy domains; its limitation lies in having "
        "been built for benchmarking rather than for inference. SPLISS posits interdependence "
        "and does not measure it.")

para(d, "The organisational-developmental literature argues for something similar from the "
        "other end, stressing that macro conditions, meso capacity and micro development are "
        "closely intertwined rather than separable (Sotiriadou et al., 2008). This establishes "
        "why a systemic view is reasonable. Whether the scholarship needed to sustain that view "
        "exists as a connected structure is left open.")

h2(d, "2.2 Governance and policy")
para(d, "Sport governance research is a mature subfield with real conceptual apparatus. "
        "Houlihan and Mallinson (2013) sort governance into state, market, civil society and "
        "sport movement, and argue that the state's role in elite sport is neither dominant nor "
        "withdrawing. A review of sport policy research from 2000 to 2020 found that close to "
        "half of all studies worked at the meso level, with governance theory and the SPLISS "
        "model the most-used frameworks (Chien, 2022). Of the three pillars we examine, "
        "governance is the one most likely to hold together internally.")

h2(d, "2.3 Innovation, technology and analytics")
para(d, "Technological innovation in sport has grown fast, driven by wearables, machine learning "
        "and commercial platforms. Recent reviews cover biomechanics, injury-risk prediction, "
        "workload management and talent identification, and several note that the data these "
        "systems need confine them to elite settings (Li, 2023; Taheri et al., 2025). What "
        "matters for our argument is that this work is usually reported as an instrument for "
        "governance decisions or for talent selection, not as a domain of its own. The "
        "innovation pillar may be folded inside the other two rather than standing alongside "
        "them, and the multiplex analysis in Section 4.10 is built to find out.")

h2(d, "2.4 Talent development and the athlete pathway")
para(d, "The talent literature is the most developed and the most contested of the three. "
        "Reviews have settled on a vocabulary of stages, detection, identification, "
        "development, selection (Johnston et al., 2017; Zhao et al., 2024), and they keep "
        "arriving at the same uncomfortable place: evidence for predictive validity is weak, "
        "especially at young ages (Vaeyens et al., 2008; Till & Baker, 2020). The recent "
        "umbrella review pulled out eight overarching and forty-four phase-specific determinants "
        "of youth development (Descheemaeker et al., 2025). A literature this dense and this "
        "explicitly aimed at policy design should be internally coherent, and should be tightly "
        "coupled to governance through the pathway concept.")

h2(d, "2.5 Prior knowledge mapping in sport")
para(d, "Co-word analyses have mapped sport management journals (Wollny et al., 2023) and "
        "digital sport research (Liu et al., 2024). Three problems recur, and this study takes "
        "on all three.")

para(d, "The first is the retrieval instrument. Single-query retrieval partly determines the "
        "frequency profile of the corpus, so the most frequent terms may be query terms rather "
        "than field concepts. The second is synonymy, handled by manual curation or left alone, "
        "which fragments networks and disperses centrality. The third is inference: modularity "
        "and centralities get reported without any randomisation null, leaving open how much of "
        "the structure is simply the clustering of any document set drawn from a partitioned "
        "field.")

para(d, "All three are methodological rather than substantive, so none requires new data. "
        "Fixing them takes care, though, because the standard remedies themselves break in ways "
        "that go unwritten. Section 3.6 reports two such failures from our own development "
        "work, and the validation design that came out of them.")

page_break(d)
d.save(DOC)
print("partA ok")