# -*- coding: utf-8 -*-
"""Part 2: Literature review."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docbuild import *
from docx import Document

d = Document(DOC)

h1(d, "2. Literature review")

h2(d, "2.1 The high-performance sport system as an object of study")
para(d, "Comparative analysis of national elite sport systems developed through the SPLISS "
        "project remains the field's most systematic attempt to specify what a functioning "
        "high-performance sport system requires. De Bosscher et al. (2006) distilled four "
        "decades of case literature into nine pillars and approximately one hundred critical "
        "success factors, later extended to a wider national sample (Houlihan & Green, 2008). "
        "The model's analytic value lies in decomposing a purported system into interdependent "
        "policy domains; its limitation lies in being designed for benchmarking rather than "
        "structural inference. SPLISS posits interdependence; it does not measure it.")

para(d, "The organisational-developmental literature supplies a complementary level of "
        "analysis, locating performance at the intersection of macro-level political and "
        "economic conditions, meso-level policy and organisational capacity, and micro-level "
        "athlete development, and stressing that these levels are closely intertwined rather "
        "than separable (Sotiriadou et al., 2008). This work establishes why a systemic "
        "conceptualisation is plausible; it leaves open whether the scholarship required to "
        "sustain that conception exists as a connected structure.")

h2(d, "2.2 Governance and policy")
para(d, "Sport governance research has matured substantially since the turn of the century. "
        "Houlihan and Mallinson (2013) distinguish governance within the state, the market, "
        "civil society and the sport movement, and argue that the state's role in elite sport "
        "is neither uniformly dominant nor withdrawing. A systematic review of sport policy "
        "research between 2000 and 2020 found that nearly half of included studies focused on "
        "meso-level organisational analysis, and that governance theory and the SPLISS model "
        "were the most frequently applied frameworks (Chien, 2022). This is a mature subfield "
        "with substantial conceptual apparatus, which makes it the most likely of the three "
        "pillars to possess internal coherence.")

h2(d, "2.3 Innovation, technology and analytics")
para(d, "Technological innovation in sport has attracted rapidly growing attention, driven by "
        "the diffusion of wearable sensing, machine learning and commercial platforms. Recent "
        "reviews characterise the field across biomechanical analysis, injury-risk prediction, "
        "workload management and talent identification, while noting that the data requirements "
        "of many proposed systems confine them to elite settings (Li, 2023; Taheri et al., 2025). "
        "Crucially, AI and wearable research in sport is often reported as an instrument for "
        "improving governance decisions and talent selection rather than as a distinct "
        "institutional domain. This raises the possibility that the innovation pillar is "
        "conceptually subsumed within the other two rather than standing alongside them, a "
        "possibility the multiplex analysis in Section 4.10 is designed to detect.")

h2(d, "2.4 Talent development and the athlete pathway")
para(d, "The talent literature is the most theoretically elaborated and most internally "
        "contested of the three pillars. Systematic reviews have established a vocabulary of "
        "successive stages - detection, identification, development, selection (Johnston et al., "
        "2017; Zhao et al., 2024) - and have repeatedly found that empirical evidence for "
        "predictive validity remains weak, particularly for early-age identification (Vaeyens "
        "et al., 2008; Till & Baker, 2020). A recent umbrella review of 60 systematic reviews "
        "identified eight overarching and 44 phase-specific determinants of youth athlete "
        "development (Descheemaeker et al., 2025). The density of this literature, and its "
        "explicit orientation toward policy design, suggest an internally coherent pillar "
        "strongly coupled to governance concerns through the pathway construct.")

h2(d, "2.5 Athlete well-being, dual careers and safeguarding")
para(d, "A fourth strand addresses athlete welfare, mental health, dual careers and "
        "safeguarding. Although not one of the three pillars specified in this study, it appears "
        "in the network analysis and is retained as a substantive subfield rather than excluded "
        "a priori. Its conceptual position within the network indicates whether its historical "
        "stance as a corrective to performance-focused policy agendas has been accommodated or "
        "persists.")

h2(d, "2.6 Prior knowledge mapping in sport and the gaps addressed")
para(d, "Co-word analyses have mapped thematic development across leading sport management "
        "journals (Wollny et al., 2023) and digital sport research (Liu et al., 2024). These "
        "establish the descriptive value of concept mapping for sport scholarship. Three "
        "methodological limitations recur across them, each addressed directly in this study. "
        "First, none controls for the retrieval instrument: because domain-focused mapping "
        "relies on a single structured query, the frequency profile of the corpus is partly "
        "determined by the query's wording, so the most frequent terms may be query terms rather "
        "than field concepts. Second, synonymy is handled by manual curation or accepted, which "
        "fragments concept networks and disperses measured centrality. Third, structural claims "
        "are descriptive - modularity and centralities are reported without comparison to a "
        "randomisation null, leaving open how much apparent structure is attributable to the "
        "clustering inherent in any document set drawn from a partitioned knowledge domain.")

para(d, "These gaps are methodological rather than substantive, and therefore addressable "
        "without new data. Correcting them requires care, however, because the standard remedies "
        "adopted in general bibliometric practice - manual synonym merging and threshold-based "
        "graph construction - are themselves unreliable in ways rarely documented. Section 3.6 "
        "reports two such failures encountered during development of this study and the "
        "validation design adopted in response.")

page_break(d)
d.save(DOC)
print("part2 ok")