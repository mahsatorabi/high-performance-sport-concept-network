"""
Build the Article 1 manuscript outline (.docx) for a Q1 sport-management journal.
Headings only - no prose.
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

BASE = r"D:\Uni of Birjand\articles\adel\article1"
OUT = os.path.join(BASE, "Article1_manuscript_outline.docx")

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(10.5)
for s in doc.sections:
    s.top_margin = s.bottom_margin = Inches(0.8)
    s.left_margin = s.right_margin = Inches(0.9)


def h(text, level):
    p = doc.add_heading(text, level=level)
    for r in p.runs:
        r.font.color.rgb = RGBColor(0x1F, 0x3B, 0x57)
        r.font.name = "Calibri"
        r.font.size = Pt({1: 14, 2: 12, 3: 11, 4: 10.5}[level])
    return p


def meta(text, italic=True):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic = italic
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    p.paragraph_format.space_after = Pt(4)
    return p


# ------------------------------------------------------------------ front matter
t = doc.add_heading("Mapping the Intellectual Structure of High-Performance Sport "
                    "Ecosystem Research", level=0)
for r in t.runs:
    r.font.size = Pt(17)
    r.font.color.rgb = RGBColor(0x1F, 0x3B, 0x57)
meta("Full paper title: Mapping the Intellectual Structure of High-Performance Sport "
     "Ecosystem Research: A Null-Calibrated Co-Word and Thematic-Evolution Analysis of "
     "Governance, Innovation and Talent Development, 2013-2025")
meta("Target journal: International Journal of Sport Policy and Politics (primary); "
     "alternatives: European Sport Management Quarterly / Sport Management Review / "
     "International Review for the Sociology of Sport")

h("Manuscript front matter", 1)
h("Title page", 2)
h("Abstract (structured: Background / Purpose / Method / Results / Conclusions)", 2)
h("Keywords (6-8)", 2)
h("Highlights (3-5 bullets, Elsevier format)", 2)
h("Graphical abstract", 2)

# ------------------------------------------------------------------ 1 Introduction
h("1. Introduction", 1)
h("1.1 High-performance sport as an ecosystem: promise and empirical gap", 2)
h("1.2 Governance, innovation and talent development as interdependent pillars", 2)
h("1.3 The measurement problem: why the literature cannot yet be modelled as a system", 2)
h("1.4 Aim and research questions", 2)
h("1.5 Contributions of the study", 2)
h("1.6 Position of the paper", 2)

# ------------------------------------------------------------------ 2 Literature
h("2. Literature review", 1)
h("2.1 The high-performance sport system tradition", 2)
h("2.2 Sport policy and governance scholarship", 2)
h("2.3 Sport innovation, technology and digital analytics", 2)
h("2.4 Athlete talent development, identification and the pathway literature", 2)
h("2.5 Athlete well-being, dual careers and welfare", 2)
h("2.6 Prior knowledge-mapping studies of sport: contributions and limitations", 2)
h("2.7 Gaps addressed by this study", 2)

# ------------------------------------------------------------------ 3 Method
h("3. Method", 1)
h("3.1 Study design and reporting transparency", 2)
h("3.2 Literature search and corpus construction", 2)
h("3.2.1 Database, search strategy and retrieval date", 3)
h("3.2.2 Inclusion and exclusion criteria", 3)
h("3.2.3 Document hygiene and licence-boilerplate removal", 3)
h("3.2.4 Analysis window and treatment of incomplete 2026 indexing", 3)
h("3.3 Query-artefact problem and its empirical diagnosis", 2)
h("3.3.1 Single-query inflation of search-string vocabulary", 3)
h("3.3.2 Necessary-condition tokens", 3)
h("3.3.3 Query-artefact suppression rule", 3)
h("3.4 Layered corpus design (L1 titles / L2 author keywords / L3 full text)", 2)
h("3.5 POS-aware concept extraction", 2)
h("3.5.1 Nominal-run constraint and dependency-free parsing", 3)
h("3.5.2 Filter cascade C1-C7 (support, non-ubiquity, artefact exclusion, maximality, "
  "collocation, adjacenting)", 3)
h("3.5.3 Dunning log-likelihood collocation test", 3)
h("3.5.4 Left/right adjacency entropy for conceptual atomicity", 3)
h("3.6 SEMCON: semantic concept-family consolidation", 2)
h("3.6.1 Motivation: synonym fragmentation in surface-string co-word analysis", 3)
h("3.6.2 Exact normalisation (orthographic and plural)", 3)
h("3.6.3 Encoder choice and anisotropy correction", 3)
h("3.6.4 Why connected components fail and complete linkage is required", 3)
h("3.6.5 Family-size cap as a precision constraint", 3)
h("3.6.6 Threshold calibration by hand-adjudicated audit", 3)
h("3.6.7 Automatic over-merge screen (antonym and low-similarity flags)", 3)
h("3.7 Co-occurrence network construction", 2)
h("3.7.1 Specificity window for node selection", 3)
h("3.7.2 Edge null model: degree-preserving bipartite randomisation", 3)
h("3.7.3 Edge weight: association strength", 3)
h("3.8 Centrality measures and community detection", 2)
h("3.9 Structural null model and hypothesis testing", 2)
h("3.9.1 Configuration model for modularity and betweenness", 3)
h("3.9.2 Approximation strategy and its justification", 3)
h("3.10 Embedding-based topic modelling", 2)
h("3.10.1 UMAP dimensionality reduction", 3)
h("3.10.2 HDBSCAN density-based clustering and the noise cluster", 3)
h("3.10.3 Parameter grid, silhouette and cluster-validity criteria", 3)
h("3.10.4 c-TF-IDF labelling over concept families", 3)
h("3.10.5 Contrastive log-odds with informative Dirichlet prior", 3)
h("3.10.6 Topic stability via bootstrap co-assignment", 3)
h("3.11 Temporal and cross-national inference", 2)
h("3.11.1 Periodisation", 3)
h("3.11.2 Chi-square with Cramér's V and expected-count diagnostics", 3)
h("3.11.3 Emergence and decline scoring", 3)
h("3.11.4 Two-proportion tests with Benjamini-Hochberg FDR", 3)
h("3.11.5 Exclusion of circular demonymic tests", 3)
h("3.12 Multiplex construction and pillar assignment", 2)
h("3.13 Software, reproducibility and robustness", 2)
h("3.14 Ethics and reporting statement", 2)

# ------------------------------------------------------------------ 4 Results
h("4. Results", 1)
h("4.1 Corpus characteristics", 2)
h("4.2 The query string is a stronger predictor of frequency than the field", 2)
h("4.3 Mined concept inventory", 2)
h("4.4 SEMCON validation and consolidation outcomes", 2)
h("4.4.1 Anisotropy correction and encoder behaviour", 3)
h("4.4.2 Exact-normalisation gains", 3)
h("4.4.3 Audited precision and threshold selection", 3)
h("4.4.4 Over-merge screen results", 3)
h("4.4.5 Semantic families versus co-occurrence communities: divergence as a finding", 3)
h("4.5 The field is a genuine community structure", 2)
h("4.5.1 Network topology and resolution profile", 3)
h("4.5.2 Modularity against the configuration-model null", 3)
h("4.5.3 Community profiles", 3)
h("4.6 Concept stratification: framing versus intellectual infrastructure", 2)
h("4.6.1 Provenance ratios", 3)
h("4.6.2 Layer concordance", 3)
h("4.6.3 Buried and promoted concepts", 3)
h("4.7 Bridging concepts and the null-tested significance of integration", 2)
h("4.8 Thematic structure of 2013-2025", 2)
h("4.8.1 Topic inventory and labels", 3)
h("4.8.2 Noise cluster as genuine heterogeneity", 3)
h("4.8.3 Topic stability", 3)
h("4.9 Thematic evolution (RQ2)", 2)
h("4.9.1 Topic-by-period contingency structure", 3)
h("4.9.2 Emerging, stable and declining themes", 3)
h("4.9.3 The concept frontier", 3)
h("4.10 Governance, innovation and talent development as segregated pillars", 2)
h("4.10.1 Pillar assignment and assignment confidence", 3)
h("4.10.2 Boundary-crossing load against the null", 3)
h("4.10.3 Supra-centrality and cross-pillar bridges", 3)
h("4.11 National systems and communities (RQ3)", 2)
h("4.11.1 Which countries dominate the field", 3)
h("4.11.2 Topic-mix differences across national systems", 3)
h("4.11.3 Conceptual emphasis: what each system over-represents", 3)

# ------------------------------------------------------------------ 5 Discussion
h("5. Discussion", 1)
h("5.1 What the intellectual structure of high-performance sport actually looks like", 2)
h("5.2 The field's structural concepts are invisible in its own framing", 2)
h("5.3 Segregation of the three pillars: the ecosystem framing is aspirational, not "
  "empirical", 2)
h("5.4 Bridging belongs to the system, not to any single pillar", 2)
h("5.5 National systems as differentiated research cultures rather than replicas", 2)
h("5.6 Why intellectual infrastructure and framing diverge: mechanisms and implications", 2)
h("5.7 Implications for sport policy practice", 2)
h("5.8 Implications for research design and theory building", 2)
h("5.9 Contribution to knowledge mapping methodology", 2)
h("5.10 Limitations", 2)
h("5.10.1 Single database and single-query retrieval", 3)
h("5.10.2 Corpus size", 3)
h("5.10.3 English-language dominance and translation of abstracts", 3)
h("5.10.4 Pillar assignment rests on prototype similarity", 3)
h("5.10.5 Co-occurrence implies association, not causal structure", 3)
h("5.10.6 Absence of an outcome variable prevents claims about performance effects", 3)
h("5.11 Future research", 2)

# ------------------------------------------------------------------ back matter
h("6. Conclusion", 1)
h("Declarations", 1)
h("Funding", 2)
h("Conflict of interest", 2)
h("Ethics approval", 2)
h("Data availability and code reproducibility", 2)
h("Author contributions (CRediT)", 2)
h("References", 1)
h("Tables", 1)
h("Table 1. Corpus construction and exclusion audit", 2)
h("Table 2. Concept-extraction filter cascade with drop counts", 2)
h("Table 3. SEMCON validation: benchmark, manual audit and over-merge screen", 2)
h("Table 4. Network topology and null-model comparison", 2)
h("Table 5. Communities with defining concepts", 2)
h("Table 6. Top bridging concepts with null-calibrated significance", 2)
h("Table 7. Topic profiles with c-TF-IDF and contrastive labels", 2)
h("Table 8. Temporal structure: topic-by-period counts, emergence and decline scores", 2)
h("Table 9. Three-pillar assignment, boundary crossing and supra-centrality", 2)
h("Table 10. National emphases (over-represented concept families, FDR-corrected)", 2)
h("Figures", 1)
h("Figure 1. Analysis pipeline with null-model validation points", 2)
h("Figure 2. Query-string inflation against matched control terms", 2)
h("Figure 3. Encoder anisotropy before and after mean-centring", 2)
h("Figure 4. SEMCON threshold calibration: benchmark and manual audit", 2)
h("Figure 5. Concept co-occurrence network: communities and bridging concepts", 2)
h("Figure 6. Null-model validation of modularity and centrality", 2)
h("Figure 7. Concept stratification: title-layer versus full-text centrality", 2)
h("Figure 8. UMAP and HDBSCAN topic model with topic prevalence", 2)
h("Figure 9. Three-pillar multiplex and supra-centrality", 2)
h("Figure 10. Thematic evolution and the concept frontier", 2)
h("Figure 11. National research emphases and effect-size distribution", 2)
h("Appendices", 1)
h("Appendix A. Full search string and Scopus query syntax", 2)
h("Appendix B. Complete concept-extraction filter cascade log", 2)
h("Appendix C. SEMCON audit benchmark: all adjudicated pairs and verdicts", 2)
h("Appendix D. Size-cap stability sweep", 2)
h("Appendix E. Louvain resolution sweep", 2)
h("Appendix F. Complete cross-national test results (topic and family level)", 2)

doc.save(OUT)
print("Wrote %s" % OUT)
print("headings: %d" % len(doc.paragraphs))