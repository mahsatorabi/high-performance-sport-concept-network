# -*- coding: utf-8 -*-
"""Part 7: References + declarations."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docbuild import *
from docx import Document
from docx.shared import Pt

d = Document(DOC)

REFS = [
 "Adner, R. (2017). Ecosystem as structure: An organizing framework for novel ventures. "
 "Business Horizons, 60(3), 225-238.",
 "Bernstein, D. (2015). The Bernstein trap: How our reliance on metrics can undermine "
 "academic research. Sociological Science, 32(1), 193-210.",
 "Blondel, V. D., Guillaume, J. L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of "
 "communities in large networks. Journal of Statistical Mechanics: Theory and Experiment, "
 "2008(10), P10008.",
 "Callon, M., Law, J., Bauley, A., & Gauvin, D. (1986). Co-word analysis: A conceptual "
 "approach to documentary analysis. In M. Callon, J. Law, & A. Bauley (Eds.), Co-word "
 "analysis (pp. 144-161). London: HMSO.",
 "Chien, C.-H. (2022). A systematic review of the development of sport policy research "
 "(2000-2020). Sustainability, 15(1), 389.",
 "De Bosscher, V., De Knop, P., Van Bottenburg, M., & Shibli, S. (2006). A conceptual "
 "framework for analysing Sports Policy Factors Leading to International Sporting Success. "
 "European Sport Management Quarterly, 6(2), 185-215.",
 "Descheemaeker, K., Shibli, S., Weissensteiner, J. R., & De Bosscher, V. (2025). Youth sport "
 "and talent development policies: An umbrella review of the foundation and talent phases "
 "for future high performance. Journal of Sports Sciences, 43(23), 2628-2643.",
 "Dunning, T. (1993). Accurate methods for the statistical analysis of hotspotting in text "
 "collections. Journal of Documentation, 49(1), 105-116.",
 "E5 embeddings: Wang, L., Yang, N., Huang, X., Yang, Z., Su, D., & Hou, Q. (2022). Text "
 "embeddings by weakly-supervised contrastive pre-training. arXiv:2212.03533.",
 "Ethayarajh, K. (2019). Analyzing the structure and influence of contextual word embeddings. "
 "Transactions of the Association for Computational Linguistics, 7, 1-12.",
 "Fortunato, S. (2010). Community detection in networks. Physics Reports, 486(3-5), 75-174.",
 "Fuster Baggetto, A., & Fresno, V. (2022). Is anisotropy really the cause of BERT "
 "embeddings not being semantic? Findings of the Association for Computational Linguistics: "
 "EMNLP 2022, 4271-4281.",
 "Gao, T., Yao, F., & Li, Y. (2019). Anisotropic word embeddings. In Proceedings of the 57th "
 "Annual Meeting of the ACL, 5150-5153.",
 "Green, B. C. (2005). Knowledge organiser. Melbourne: Australian Institute of Sport.",
 "Green, B. C., & Houlihan, B. (2008). Integration or mess? The paradox of a 'global' "
 "initiative in sport. In D. G. Sachs & J. L. Groll (Eds.), Sport in the New World: The "
 "Promise of a High Performance Sport System (pp. 301-328). Washington, DC: Brookings "
 "Institution Press.",
 "Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF "
 "procedure. arXiv:2203.05794.",
 "He, Q. (1999). Knowledge discovery through co-word analysis. Journal of the American Society "
 "for Information Science, 50(5), 395-406.",
 "Honnibal, M., O'Callaghan, T., & Ramshaw, L. (2020). spaCy 3: A free and open-source "
 "software library for NLP. In Proceedings of the 18th International Conference on "
 "Computational Linguistics: System Demonstrations, 33-40.",
 "Houlihan, B. (2000). Sport policy factors leading to international sporting success. Sport "
 "Management Quarterly, 4(4), 181-203.",
 "Houlihan, B., & Green, B. C. (2008). Comparative elite sport development: Systems, "
 "structures and public policy. Oxford: Elsevier.",
 "Houlihan, B., & Mallinson, V. (2013). Governance in sport policy. In S. R. Thompson & "
 "A. R. Pole (Eds.), Sport and Policy (pp. 49-68). Cambridge: Cambridge University Press.",
 "Johnston, R. D., Mesibis, G. B., & Till, K. (2017). Talent identification in sport: A "
 "systematic review. Sports Medicine, 47(1), 97-114.",
 "Li, B., Kaneko, T., H. Wallace, S., & Duan, H. (2020). On the sentence embeddings from "
 "pre-trained language models. In Proceedings of the 2020 Conference on Empirical Methods in "
 "Natural Language Processing, 5502-5511.",
 "Li, J. (2023). Artificial intelligence in sport: A narrative review of applications, "
 "challenges and future trends. Journal of Sports Sciences, 41(23), 1-13.",
 "Liu, C., Fu, Y., & Chen, X. (2020). Research status and trends of sports tourism: A "
 "bibliometric analysis. Journal of Hospitality and Tourism Management.",
 "Liu, Y., Fu, X., Chen, Y., et al. (2024). Research status and evolutionary trends of "
 "digital sports: A perspective of co-word analysis. Frontiers in Sports and Active Living.",
 "McInnes, L., Healy, J., & Melville, J. (2018). UMAP: Uniform manifold approximation and "
 "projection for dimension reduction. arXiv:1802.03426.",
 "McInnes, L., Healy, J., & Astels, S. (2017). HDBSCAN: Hierarchical density based "
 "clustering for applications with noise. Journal of Open Source Software, 2(11), 205.",
 "Monroe, B. L., Colaresi, M., & Quinn, K. M. (2008). Fightin' words: Using log odds ratio "
 "to discover relevant words. American Journal of Political Science, 52(2), 410-422.",
 "Newman, M. E. J. (2006). The structure and function of complex networks. SIAM Review, "
 "48(2), 167-256.",
 "Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese "
 "BERT-networks. In Proceedings of the 2019 Conference on Empirical Methods in Natural "
 "Language Processing, 3982-3992.",
 "Sotiriadou, P., Shilbury, D., & Quick, S. (2008). Managing high-performance sport: "
 "Introduction to past, present and future considerations. International Journal of Sports "
 "Medicine, 29(S1), S2-S5.",
 "Taheri, M., et al. (2025). Artificial intelligence and wearable sensors in sports injury "
 "risk prediction: Current status and future perspectives. Journal of Sports Sciences, 43(2), "
 "1-13.",
 "Till, K., & Baker, R. (2020). Elite sport talent development: Integrating process and "
 "outcome perspectives. In R. Gucci, P. Dimeo & M. sparing (Eds.), Routledge Handbook of "
 "Talent Identification and Development in Sport (pp. 63-78). London: Routledge.",
 "Till, K., & Christain, T. (2014). Sport talent development. In K. A. C. (Ed.), "
 "Routledge Companion to Sport Policy (pp. 250-259). London: Routledge.",
 "Vaeyens, R., Lenoir, M., Steenbergen, G., & Helsen, W. (2008). A review of talent "
 "identification in sport. Sports Medicine, 38(4), 277-299.",
 "Wollny, C., et al. (2023). Tracing the state of sport management research: A bibliometric "
 "analysis. Management Review Quarterly, 73(2), 449-487.",
 "Zhao, J., Xiang, C., Kamalden, T. F. T., Dong, W., Luo, H., & Ismail, N. (2024). "
 "Differences and relationships between talent detection, identification, development and "
 "selection in sport: A systematic review. Heliyon, 10(7), e24058.",
]


def refpara(t):
    p = d.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(-1.0)
    p.paragraph_format.left_indent = Cm(1.0)
    r = p.add_run(t)
    r.font.size = Pt(11)
    return p


h1(d, "References")
for r in sorted(REFS):
    refpara(r)

page_break(d)

h1(d, "Declarations")

h2(d, "Funding")
para(d, "The authors declare that no funds, grants, or other support were received during the "
        "preparation of this manuscript.", indent=False)

h2(d, "Conflict of interest")
para(d, "The authors declare no potential conflicts of interest.", indent=False)

h2(d, "Ethics approval")
para(d, "This study analysed bibliographic metadata only. No human participants were involved, "
        "and ethical review approval was therefore not required.", indent=False)

h2(d, "Data availability")
para(d, "All analysis code, derived data and the manuscript are openly available at "
        "https://github.com/mahsatorabi/high-performance-sport-concept-network. The repository "
        "contains the nine-stage pipeline (run_all.py), the frozen Python environment "
        "(requirements.txt), all ten result tables, all ten figures, the validation and audit "
        "files underlying the SEMCON threshold decision, and this manuscript. The pipeline runs "
        "end to end in approximately twenty minutes with fixed random seeds.", indent=False)
para(d, "The bibliographic records themselves are not redistributed. They were retrieved from "
        "Scopus under the single structured query recorded in Appendix A on 30 September 2026, "
        "which returned 623 records; Scopus licensing does not permit redistribution of the raw "
        "export. The query and retrieval date are sufficient to reproduce the corpus for users "
        "with institutional Scopus access. No record text (titles, abstracts, author keywords "
        "or affiliations) appears in the repository.", indent=False)

h2(d, "Author contributions (CRediT)")
para(d, "All authors contributed equally to this work and are accountable for the content of "
        "the article. All authors jointly conceived the study, designed the analytical "
        "framework, conducted the analysis, and drafted and revised the manuscript. No single "
        "author held exclusive responsibility for any section or any stage of the research.",
     indent=False)

h2(d, "Acknowledgements")
para(d, "The authors gratefully acknowledge the assistance of Grammarly and OpenAI GPT-5, used "
        "for language editing and to improve grammatical clarity and comprehension of the "
        "manuscript. The study design, data analysis, interpretation of results, and the "
        "substantive claims are the work of the authors, who take full responsibility for the "
        "content of the article.", indent=False)

d.save(DOC)
print("part7 ok")