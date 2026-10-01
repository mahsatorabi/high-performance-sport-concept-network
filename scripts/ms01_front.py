# -*- coding: utf-8 -*-
"""Part 1: title, abstract, keywords, highlights, Introduction."""
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
        "innovation and talent development are mutually reinforcing. Whether the research "
        "literature behaves as such a system has not been established, because the concepts "
        "that would define it have never been measured as a structure. This study constructs "
        "and validates a concept network for the field and tests that implicit claim.", indent=False)

para(d, "A Scopus corpus of 604 records (2013-2025: n = 448) was converted into a concept network "
        "through a POS-constrained term-mining cascade, a new semantic concept-family "
        "consolidation procedure (SEMCON) combining deterministic normalisation with "
        "complete-linkage clustering of anisotropy-corrected neural embeddings, and a "
        "degree-preserving bipartite null model for edge admission. Structural claims were "
        "tested against a configuration-model null over 300 randomisations. Thematic evolution "
        "was assessed by embedding-based topic modelling (UMAP + HDBSCAN with class-based "
        "TF-IDF); cross-national differences by FDR-corrected proportion tests.", indent=False)

para(d, "Three findings follow. First, the network is significantly modular (Q = 0.446 against a "
        "null of 0.220 ± 0.004, z = +64.3, p < .004): high-performance sport research "
        "constitutes a genuine community structure, not an integrated discourse. Second, its "
        "integrative concepts are largely invisible in its own framing - only 8.3% of concept "
        "mentions occur in titles, and title-level betweenness correlates with full-text "
        "betweenness at only rho = 0.39. Third, the governance, innovation and talent-development "
        "pillars are statistically segregated: shortest paths between concepts cross pillar "
        "boundaries less often than under degree-preserving randomisation (0.950 versus 0.963 ± "
        "0.003, z = -4.16). The ecosystem framing is therefore aspirational rather than "
        "empirical, and bridging is distributed evenly across pillars (chi-square = 2.40, "
        "p = .30). Cross-national variation is substantial (topic × country chi-square = 180.6, "
        "V = 0.267, p < .001), indicating differentiated national cultures rather than a shared "
        "agenda.", indent=False)

para(d, "The methodological contribution is equally consequential. Single-query retrieval "
        "inflates its own search vocabulary 3.67-fold relative to matched controls; connected "
        "components over a thresholded similarity graph chain semantically incoherent families; "
        "and raw neural embeddings are too anisotropic (+0.81 mean random-pair cosine) to "
        "support consolidation without mean-centring. SEMCON, calibrated by hand adjudication of "
        "95 sampled merges (audited precision 0.957), is released as a reproducible standard for "
        "concept-network analysis in bounded corpora.", indent=False)

p = d.add_paragraph()
p.paragraph_format.line_spacing = 2.0
p.paragraph_format.first_line_indent = Cm(1.27)
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r = p.add_run("Keywords: ")
r.bold = True
r.font.size = Pt(12)
r2 = p.add_run("high-performance sport; sport policy; science mapping; co-word analysis; "
               "semantic concept networks; null models; text mining; talent development; "
               "sport innovation")
r2.font.size = Pt(12)

# ---------------------------------------------------------------- HIGHLIGHTS
h1(d, "Highlights")
bullet(d, "The high-performance sport concept network is significantly modular "
          "(z = +64.3 against a degree-preserving null).")
bullet(d, "Governance, innovation and talent development are statistically segregated "
          "literatures, not an integrated ecosystem.")
bullet(d, "Only 8.3% of concept mentions appear in titles; integrative concepts are "
          "structurally invisible in the field's own framing.")
bullet(d, "Single-query retrieval inflates search-string vocabulary 3.67-fold, distorting "
          "conventional co-word networks.")
bullet(d, "SEMCON, a validated semantic concept-family consolidation procedure, is released "
          "as a reproducible standard for bounded corpora.")

page_break(d)

# ================================================================ 1. INTRODUCTION
h1(d, "1. Introduction")

para(d, "High-performance sport is conventionally analysed as a system. The SPLISS project "
        "models national elite sport performance as a function of nine interacting policy "
        "pillars spanning finance, governance, participation, talent identification, athletic "
        "and post-career support, coaching, facilities, competition and scientific research "
        "(De Bosscher et al., 2006). The organisational-developmental literature likewise "
        "locates performance at the intersection of macro-level political economy, meso-level "
        "policy design and micro-level athlete development (Sotiriadou et al., 2008), and "
        "ecological theorising borrowed from innovation studies has encouraged analysts to "
        "treat sport as an ecosystem of interdependent actors (cf. Adner, 2017). Across these "
        "traditions the organising premise is that outcomes emerge from interaction rather "
        "than from isolated determinants.", indent=False)

para(d, "The framing carries an empirical implication rarely tested. If governance, innovation "
        "and talent development constitute an integrated system, the research literature "
        "should display the corresponding signature: strong and frequent associations between "
        "pillars, and integrative concepts binding them together. If instead the three "
        "literatures are parallel, each with its own internal logic and few conceptual "
        "bridges, then ecosystem thinking prescribes how sport systems should be organised "
        "rather than describing how scholarship has developed. Distinguishing these matters: a "
        "genuinely integrated literature would justify theoretical integration, a segregated one "
        "would justify treating the pillars as substantively distinct and concentrating effort "
        "on missing connections.", indent=False)

para(d, "This is hard to answer for a straightforward reason: the concepts that would "
        "instantiate an ecosystem have never been operationalised as a measurable structure. "
        "Sport policy scholarship has mapped individual national systems systematically, most "
        "comprehensively through the SPLISS benchmarking series (Houlihan & Green, 2008), and "
        "athlete development has been the subject of multiple systematic reviews (Johnston et "
        "al., 2017; Descheemaeker et al., 2025). But these review substantive claims. What is "
        "missing is a representation of the field's conceptual organisation that is explicit, "
        "reproducible, testable, and comparable against what the ecosystem model predicts.",
     indent=False)

para(d, "Science mapping supplies the relevant apparatus. Co-word analysis reconstructs a "
        "field's conceptual structure from the co-occurrence of terms across documents (Callon "
        "et al., 1986; He, 1999) and has been applied across sport (Wollny et al., 2023; Liu et "
        "al., 2024). It is attractive here because the construct of interest is conceptual "
        "rather than citational. Yet applied to a bounded domain such as high-performance "
        "sport, standard practice encounters a problem we term the query-artefact problem.",
     indent=False)

para(d, "A domain literature is almost always retrieved with a single structured query, so "
        "that the query's vocabulary is present in a large, non-random share of the retrieved "
        "documents. In our corpus, terms drawn verbatim from the search string appear with mean "
        "frequency 3.67 times that of matched control terms, and the phrase \u201csport "
        "system\u201d alone occurs in 54.6% of documents. Since conventional co-word analysis "
        "treats the most frequent terms as the field's core concepts, an uncorrected analysis "
        "returns the search string as a finding. This is not a second-order concern: it "
        "determines the identity of the network's hubs.", indent=False)

para(d, "A second problem compounds it. Co-word networks built on surface strings fragment "
        "under synonymy. \u201cTalent development\u201d, \u201cathlete development\u201d and "
        "\u201ctalent pipeline\u201d denote substantially the same object but occupy separate "
        "nodes, fragmenting the network and dispersing the centrality of integrative concepts. "
        "Standard remedies are manual synonym dictionaries, which do not scale. We instead "
        "propose a two-stage consolidation procedure (SEMCON) applying deterministic "
        "normalisation for morphological and orthographic variation, then clustering residual "
        "lexical synonymy by cosine similarity between anisotropy-corrected neural embeddings "
        "under complete linkage. Section 3.6 reports the validation, including two failures "
        "encountered and corrected during development, because these are instructive about the "
        "reliability of embedding-based consolidation in general.", indent=False)

para(d, "A third concern is inference. Applied sports science frequently reports centralities "
        "and clusterings without indicating whether the structure departs from what chance "
        "would produce. Any co-occurrence network will exhibit some modularity and some "
        "apparent hubs, because the underlying document set is itself clustered by topic. "
        "Claims that a field is \u201cmodular\u201d or a concept \u201cintegrative\u201d are "
        "therefore meaningful only against a stated null. This study places every structural "
        "claim against a degree-preserving null: a bipartite swap model for edges and a "
        "configuration model for modularity and centrality.", indent=False)

para(d, "Against this background the study asks four questions. Two concern structure:",
     indent=False)
para(d, "RQ1. What is the conceptual structure of high-performance sport research as a concept "
        "network, and which concepts are structurally integrative? Specifically, is the network "
        "modular relative to a degree-preserving null, and which concepts occupy significantly "
        "bridging positions?", indent=False)
para(d, "RQ2. How does the thematic composition of the field evolve across the governance, "
        "innovation and talent-development pillars, and which concepts constitute its "
        "frontier?", indent=False)
para(d, "Two concern integration and difference:", indent=False)
para(d, "RQ3. Do the three pillars form an integrated conceptual system, or parallel literatures "
        "with limited interconnection?", indent=False)
para(d, "RQ4. How do national research systems differ in the concepts and topics they "
        "over-represent?", indent=False)

para(d, "The study makes three contributions. Methodologically, it demonstrates that "
        "conventional co-word analysis of a single-query bounded corpus is materially biased by "
        "the retrieval instrument, quantifies the bias, and supplies a validated correction. "
        "Substantively, it establishes that the literature is modular but that its three "
        "asserted pillars are statistically segregated, reclassifying ecosystem integration "
        "from established fact to open empirical question. Practically, it identifies which "
        "concepts carry cross-pillar associations, providing a defensible basis for integrative "
        "interventions and for the conceptual modelling reported in the companion paper.",
     indent=False)

page_break(d)
d.save(DOC)
print("part1 ok")