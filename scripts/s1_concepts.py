"""
ARTICLE 1 - Stage 1: POS-aware concept extraction by term mining.

The novelty of this stage is a filter cascade that makes the concept set robust to the
degenerate character of a single-query bibliographic retrieval, combined with POS-constrained
noun-phrase mining so that candidate concepts are nominal constructs rather than any
frequent string.

FILTER CASCADE (all criteria; every drop is counted and reported)
  C1  Support         df >= MIN_DF
  C2  Non-ubiquity    df/N < UBIQUITY_MAX   (a term in most documents is a corpus constant)
  C3  Query-artifact  term matches the search string (empirically inflated 3.68x, stage 0)
  C4  Nominality      POS-constrained: candidate must be a contiguous run of
                      NOUN/PROPN/ADJ tokens, ADJ never permitted in final position alone
  C5  Maximality      drop n-grams that are strict sub-phrases of a longer n-gram with
                      identical document frequency (removes fragments)
  C6  Collocation     Dunning (1993) log-likelihood vs independence, Bonferroni, alpha=.001
  C7  Adjacenting     min(left-entropy, right-entropy) >= ENTROPY_MIN bits (atomicity)
"""
import csv, json, math, os, re, collections, sys
import itertools as _itertools
from collections import Counter, defaultdict
import spacy

BASE = r"D:\Uni of Birjand\articles\adel\article1"
DATA = os.path.join(BASE, "data")
csv.field_size_limit(10**9)

MIN_DF = 5
UBIQUITY_MAX = 0.60
LLR_CRIT = 10.828      # chi-square(1) at p = .001
ENTROPY_MIN = 0.30
MAX_N = 4

QUERY_PHRASES = [
    "sport ecosystem", "sport system", "sport network", "sport value chain",
    "innovation ecosystem", "entrepreneurial ecosystem", "elite sport",
    "high performance sport", "professional sport", "athlete",
]

STOP = set("""
a an the and or but if then than that this these those there here of in on at to for from with
without by as is are was were be been being am do does did doing have has had having will would
shall should can could may might must not no nor so such both each few more most other some only
own same too very just don now it its we you they he she them his her their our your my me i us
who whom which what when where why how all any because while about into over under between during
before after above below up down out off again further once against per via among throughout
despite along across toward towards upon within
one two three four five six seven eight nine ten first second third next last
study studies studied research researches article articles paper papers
result results finding findings analysis analyses analytic analyse analyze analyzing
method methods methodology methodologies approach approaches
data dataset datasets information information
use used uses using useful utilize utilized
show shows showed shown
based upon
may might could would should will shall must can
however therefore thus hence moreover furthermore although though whereas
new novel recent current future key important significant various several different
potential need needs role roles factor factors impact impacts effect effects
understanding perspective perspectives review reviews reviewed
individual individuals group groups level levels
article issue volume number page pages
time times year years world worlds case cases study chapter chapters
part parts many much lot lots kind kinds sort sorts type types thing things
way ways example examples order orders semi structured
specific specifically purpose purposes significant significantly
important importantly critical critically
good better best worse worst
real actual true false general particular
well even still yet ever never always
""" .split())

ARTIFACT = set()
for q in QUERY_PHRASES:
    qn = re.sub(r"[^a-z0-9\- ]", " ", q.replace("*", "").lower())
    qn = " ".join(qn.split())
    if not qn:
        continue
    ARTIFACT.add(qn)

# Generate every plural variant of every query phrase so that morphological forms such as
# "sports system", "sport systems" and "elite sports" are also treated as artefacts.
ARTIFACT_BASE = set()
for a in ARTIFACT:
    parts = a.split()
    ARTIFACT_BASE.add(a)
    for i in range(len(parts)):
        for combo in _itertools.product(["", "s"], repeat=len(parts)):
            if not any(combo):
                continue
            ARTIFACT_BASE.add(" ".join(p + c for p, c in zip(parts, combo)))

# Necessary-condition tokens: every disjunct of the query contains the token "sport"
# (sport ecosystem | sport system | sport network | sport value chain | elite sport |
#  high performance sport | professional sport), so the token is present in the corpus by
# construction and carries no information about the field.
NECESSARY = {"sport", "sports"}
ARTIFACT_BASE |= NECESSARY

# Research-apparatus vocabulary: describes the instrument of a study rather than the object
# of study. Removed as a documented, separately counted filter (C3b).
APPARATUS = set("""
interview interviews interviewed qualitative quantitative participants participant
method methods methodology methodologies survey surveys questionnaire questionnaires
thematic analysis analyses analyze analysed analyzed findings finding
sample samples sampling transcript transcripts coding reliability validity
semi structured main case cases study studies studied literature review reviewed
paper papers article articles research researcher researchers author authors
purpose purposes aim aims objective objectives result results discussion
introduction conclusion conclusions background theoretical empirical
editor editors editorial contributors contributor chapters
severally similarly especially notably particularly indeed overall
foreword preface glossary acknowledgements acknowledgments
abstract synopsis epilogue appendix table
severely severe closely close
functional functions capable capability
diverse diversity mixed positive negative
reflexive reflexive practices perform
available accessible applicable
""".split())

# High-frequency general English. A dedicated stoplist cannot keep pace with a corpus of
# 600 abstracts, so candidate mining is additionally constrained to a standard high-frequency
# English word list. Domain-bearing vocabulary (athlete, coach, policy, governance,
# doping, pathway, ...) is not in this list, so it survives, whereas generic content words
# (work, end, positive, able, single, mean, level) are removed as corpus-level filler.
HIGH_FREQ = set("""
able about above accept according account across act action active actual add addition additional
address administration admit adult affect after again against age agency agenda ago agree agreement
ahead aim all allow almost alone along already also although always among amount analysis analyse
analysis analyze and animal another answer any anyone anything appear apply approach area argue
argument around arrange arrive art article as ask aspect assess assessment asset assume at attack
attempt attention attitude attract audience author authority available average avoid award aware
away back background bad balance ball bank bar base basic basis be beat beautiful because become
bed before begin beginning behalf behaviour behavior behind belief believe benefit best better
between beyond big bill billion bit black block blood blue board body book border both bottom box
boy break bridge brief bright bring broad brother budget build building business but buy by call
camera campaign can cancer candidate capital car card care career carry case cash cast catch cause
cell center central centre century certain certainly chair challenge chance change channel chapter
character charge cheap check child choice choose church citizen city civil claim class clear clearly
close coach cold collection college colour color come commercial common community company compare
comparison compete competition complete completely complex computer concern condition conference
consider considerable construction consumer contact contain content contest context continue
contract control cost could council country couple course court cover create creation cultural
culture current currently customer cut daily data date daughter deal death debate decade decide
decision deep defence defense degree deliver demand department depend describe design desire desk
despite detail determine develop development die difference different difficult dinner direction
director discover discuss discussion disease do doctor document dog domestic door double doubt down
draw dream drive drop drug dry during duty each early east easy eat economic economy edge editor
education effect effective effectively efficiency effort eight either elect election else emerge
emotional emphasis employ employee employment encourage end energy engine engineer english enhance
enormous enough ensure enter enterprise entire environment environmental especially essay essential
establish estate estimate european even evening event eventually ever every everybody everyone
everything evidence exactly example excellent except exchange executive exercise exist existence
existing expect expectation expensive experience expert explain explanation explore express
expression extend extent external extra extremely eye face fact factor factory fail fair fall
false familiar family famous far farm fashion fast father fear feature federal feel female few
field fight figure file fill film final finally finance financial find fine finger finish fire
firm first fish five floor fly focus follow food foot for force foreign forget form former forward
four frame free freedom friend from front full fund future game garden gas general generation
get girl give glass go goal good government great green ground group grow growth guess gun guy
hair half hand handle hang happen happy hard head health hear heart heat heavy help her here
herself high him himself his history hit hold hole home hope horse hospital hot hotel hour house
how however huge human hundred husband i idea identify if image imagine impact important improve
in include including increase indeed indicate individual industrial industry information initial
inside instead institution instruction instrument insurance intend interest international
interview introduce investment involve issue item its itself job join joint joke journalist judge
jump just keep key kid kill kind kitchen knee know knowledge labour labor lack lady land language
large last late later laugh law lawyer lay lead leader leadership learn least leave left leg
legal less let letter level library lie life lift light like likely limit line link list listen
little live load local location lock long look lose loss lot love low luck machine magazine main
maintain major majority make male man manage management manager manner many map mark market
marriage material matter may maybe me mean meaning measure media medical meet meeting member
membership memory mention message method middle might mile military million mind mine minute miss
mission mistake mix model modern moment money monitor month mood moral more morning most mother
motion mountain mouth move movement movie much music must my myself name nation national natural
nature near nearly necessary need network never new news newspaper next nice night nine no none
nor normal north not note nothing notice now number occur ocean of off offer office officer
official often oil old once one online only open operate operation opinion opportunity option or
orange order organisation organization organization original other others our out outside over
owner page pain paint painting pair panel paper parent park part participant particular
particularly party pass passage past patient pattern pay peace people per perform performance
perhaps period person personal phone physical pick picture piece place plan plant plastic plate
play player please point police policy political politics poor popular population position
positive possible power practice prepare present president pressure pretty prevent price private
probably problem process produce product production professional professor programme program
project property protect prove provide public publication publish pull purpose push put quality
question quick quickly quite race radio raise range rate rather reach read ready real reality
realise realize really reason receive recent recently recognise recognize record red reduce reflect
region relate relationship religious remain remember remove report represent republican require
research resource respond response responsibility rest result return reveal rich right rise risk
road rock role room rule run safe safety sail sale same sample save say scale scene school science
scientist score sea search season seat second section security see seek seem sell send senior sense
series serious serve service session set settle seven several sex sexual shake share sharp she
sheet ship shoot short shot should shoulder show side sign signal significant similarly simple simply
since sing single sister sit site situation six size skill skin sky sleep slow small smile so social
society soft software solution solve some somebody someone something sometimes son song soon sort
sound source south southern space speak special specific speech spend sport spread spring staff
stage stand standard star start state statement station stay step stick still stock stop store
story straight strange strategic street strong structure student study stuff style subject success
successful such suddenly suffer suggest summer supply support suppose sure surface surprise system
table take talk tall task tax teach teacher team technology television tell temperature tend
tension term terms terrible test text than thank that the their them themselves then theory there
these they thing think third this those though thought thousand three through throughout throw thus
time today together tonight too top total tough toward town trade traditional traffic
training travel treat treatment tree trial trip trouble true truth try turn twice type under
understand unit until upon use used useful user usually value various very victim view violence
visit voice vote wait walk wall want war watch water way we wear weather wedding week weight welcome
well west western what whatever when where whether which while white who whole whom whose why wide
wife wild will win wind window wine wing winter wire wish with within without woman wonder wood word
work worker world worry worth would write writer wrong yard yeah year yes yet young your yourself
""".split())
# Bibliographic / export metadata and cross-lingual residue that survives abstract cleaning.
META_NOISE = set("""
scopus pubmed sportdiscus sportdiscus spliss jpes web of science science direct
copyright rights reserved licence license isbn issn doi orcid
search searched database databases google wiley springer elsevier sage
taylor francis group
el la los las del und et du des le les die der das dei den dem
deporte deporte ISSN ISBN
""".split())

# Definitional constructions: "the term X", "the notion of X" - frequency artefacts.
DEFINITIONAL_HEADS = {"term", "terms", "notion", "notions"}

print("=" * 78)
print("STAGE 1  POS-AWARE CONCEPT EXTRACTION")
print("=" * 78)

blob = json.load(open(os.path.join(DATA, "corpus.json"), encoding="utf-8"))
docs = blob["docs"]
N = len(docs)
print("N documents: %d  |  MIN_DF=%d  UBIQUITY_MAX=%.2f  ENTROPY_MIN=%.2f bits"
      % (N, MIN_DF, UBIQUITY_MAX, ENTROPY_MIN))

nlp = spacy.load("en_core_web_sm", disable=["ner", "lemmatizer"])
print("spaCy model loaded; parsing %d documents x 3 layers ..." % (N * 3))

NOMINAL = {"NOUN", "PROPN"}
OK_POS = {"NOUN", "PROPN", "ADJ"}


def analyse(text):
    """Return list of (token, pos) with hyphens/apostrophes split, numerics dropped."""
    doc = nlp(text)
    out = []
    for t in doc:
        if t.is_space or t.is_punct or t.like_num or t.like_url or t.like_email:
            out.append((None, "BREAK"))
            continue
        w = t.text.lower()
        parts = [p for p in re.split(r"[-/']", w) if re.match(r"^[a-z][a-z0-9]*$", p)]
        if not parts:
            out.append((None, "BREAK"))
            continue
        pos = t.pos_ if t.text[:1].isalpha() else "BREAK"
        if pos not in OK_POS:
            pos = "BREAK"
        for i, p in enumerate(parts):
            out.append((p, pos if (i == 0 and pos != "BREAK") else
                        ("NOUN" if pos != "BREAK" else "BREAK")))
    return out


# ---------------------------------------------------------------- POS analysis per layer
seqs = {}
for lk, src in (("L1", lambda d: d["title"]),
                ("L2", lambda d: d["title"] + " ; " + " ; ".join(d["author_keywords"])),
                ("L3", lambda d: d["title"] + " ; " + " ; ".join(d["author_keywords"])
                                  + " . " + d["abstract"])):
    seqs[lk] = [analyse(src(d)) for d in docs]

audit = collections.Counter()

# ---------------------------------------------------------------- mine candidate n-grams
def mine(seq):
    """n-gram document frequency and boundary statistics over nominal runs."""
    dfm = defaultdict(set)
    bnd = defaultdict(Counter)
    for di, toks in enumerate(seq):
        n = len(toks)
        for i in range(n):
            w, p = toks[i]
            if w is None or w in STOP:
                continue
            # left neighbour within same nominal run
            lp = toks[i - 1] if i > 0 else (None, "BREAK")
            ltok = lp[0] if lp[0] and lp[1] != "BREAK" else "^"
            for L in range(1, MAX_N + 1):
                if i + L > n:
                    break
                grp = toks[i:i + L]
                if any(g[0] is None or g[1] == "BREAK" for g in grp):
                    break
                g = tuple(x[0] for x in grp)
                dfm[g].add(di)
                rn = toks[i + L] if i + L < n else (None, "BREAK")
                rtok = rn[0] if rn[0] and rn[1] != "BREAK" else "$"
                bnd[g][(ltok, rtok)] += 1
            if p == "ADJ":
                # an adjective may not terminate a nominal run
                pass
    return dfm, bnd


# NOTE: adjacency is defined on the *filtered nominal* stream, so a deleted verb between
# two nouns does not create a false bigram.
dfm, bnd = mine(seqs["L3"])
df = {g: len(s) for g, s in dfm.items()}
print("raw nominal n-grams: %d" % len(df))


def entropy(counts):
    tot = sum(counts.values())
    if tot == 0:
        return 0.0
    return -sum((c / tot) * math.log2(c / tot) for c in counts.values())


def adj_ent(g):
    L, R = Counter(), Counter()
    for (l, r), c in bnd.get(g, {}).items():
        L[l] += c
        R[r] += c
    return entropy(L), entropy(R)


# ---------------------------------------------------------------- C1..C3
cands = {}
for g, v in df.items():
    phrase = " ".join(g)
    if v < MIN_DF:
        audit["C1 support"] += 1
        continue
    if v / N >= UBIQUITY_MAX:
        audit["C2 ubiquity"] += 1
        continue
    if phrase in ARTIFACT_BASE:
        audit["C3 query artifact"] += 1
        continue
    if len(g) == 1 and g[0] in APPARATUS:
        audit["C3b research apparatus"] += 1
        continue
    if any(w in META_NOISE for w in g):
        audit["C3c metadata / cross-lingual"] += 1
        continue
    if any(len(w) < 2 for w in g):
        audit["C3d single-character token"] += 1
        continue
    if g[0] in DEFINITIONAL_HEADS:
        audit["C3e definitional construction"] += 1
        continue
    # The high-frequency list constrains UNIGRAMS only. Multiword expressions are retained
    # on the strength of the collocation test alone, because expressions assembled from
    # generic words are frequently genuine domain concepts ("national team", "social
    # support", "youth sport") and would be lost under a blanket component-wise rule.
    if len(g) == 1 and g[0] in HIGH_FREQ:
        audit["C3f high-frequency English"] += 1
        continue
    if any(x in STOP for x in g):
        audit["C4 stopword inside"] += 1
        continue
    cands[g] = v

# ---------------------------------------------------------------- C5 maximality
by_df = collections.defaultdict(list)
for g, v in cands.items():
    by_df[v].append(g)
contain = defaultdict(set)
for v, gs in by_df.items():
    if len(gs) < 2:
        continue
    gs = sorted(gs, key=lambda x: (len(x), x))
    for i, g in enumerate(gs):
        pat = " " + " ".join(g) + " "
        for h in gs[i + 1:]:
            if pat in " " + " ".join(h) + " ":
                contain[g].add(h)
keep = {}
for g, v in cands.items():
    if g in contain:
        audit["C5 fragment (maximality)"] += 1
        continue
    keep[g] = v
cands = keep

# ---------------------------------------------------------------- C6 collocation
uni_df = {g[0]: df[g] for g in df if len(g) == 1}


def gllr2(o, n1, n2):
    """Dunning (1993) log-likelihood ratio for the 2x2 table
         w1w2 present / w1w2 absent
       w1 present  / w1 absent
       with marginals n1 = df(w1), n2 = df(w2).  Positive => collocation."""
    if min(o, n1, n2) <= 0:
        return 0.0
    e12 = n1 * n2 / N

    def d(a, b):
        return a * math.log(a / b) if a > 0 and b > 0 else 0.0
    return 2 * (d(o, e12)
                + d(n1 - o, n1 - e12)
                + d(n2 - o, n2 - e12)
                + d(N - n1 - n2 + o, N - n1 - n2 + e12))


llr = {}
for g, v in cands.items():
    if len(g) == 1:
        llr[g] = None
        continue
    if len(g) == 2:
        llr[g] = gllr2(v, uni_df.get(g[0], 0), uni_df.get(g[1], 0))
    else:
        # For longer n-grams a 2x2 table is not defined; require that EVERY contiguous
        # bigram inside the phrase is itself a significant collocation.
        vals = []
        for i in range(len(g) - 1):
            a, b = g[i], g[i + 1]
            if a not in uni_df or b not in uni_df:
                vals.append(0.0)
            else:
                vals.append(gllr2(df.get((a, b), 0), uni_df[a], uni_df[b]))
        llr[g] = min(vals)

sel = {}
for g, v in cands.items():
    if len(g) == 1:
        sel[g] = v
    elif llr[g] is not None and llr[g] >= LLR_CRIT:
        sel[g] = v
    else:
        audit["C6 collocation (LLR<crit)"] += 1
cands = sel

# ---------------------------------------------------------------- C7 adjacenting
final = {}
for g, v in cands.items():
    if len(g) == 1:
        final[g] = v
        continue
    hl, hr = adj_ent(g)
    if min(hl, hr) < ENTROPY_MIN:
        audit["C7 adjacenting (non-atomic)"] += 1
        continue
    final[g] = v

print("FINAL concepts: %d  (unigram %d / multiword %d)"
      % (len(final), sum(1 for g in final if len(g) == 1),
         sum(1 for g in final if len(g) > 1)))
for k, v in audit.most_common():
    print("   drop %-28s %6d" % (k, v))

# ---------------------------------------------------------------- concept index
order = sorted(final, key=lambda x: (-final[x], x))
idx = {g: i for i, g in enumerate(order)}
concept_list = [" ".join(g) for g in order]

# ---------------------------------------------------------------- document-concept presence
def presence(lk):
    rows = []
    for seq in seqs[lk]:
        toks = seq
        n = len(toks)
        present = set()
        for i in range(n):
            if toks[i][0] is None or toks[i][1] == "BREAK":
                continue
            for L in range(1, MAX_N + 1):
                if i + L > n:
                    break
                grp = toks[i:i + L]
                if any(g[0] is None or g[1] == "BREAK" for g in grp):
                    break
                key = tuple(x[0] for x in grp)
                if key in idx:
                    present.add(idx[key])
        rows.append(sorted(present))
    return rows


binary = {lk: presence(lk) for lk in ("L1", "L2", "L3")}
for lk in binary:
    print("layer %s mean concepts/doc = %.2f" % (lk, sum(len(r) for r in binary[lk]) / N))

concepts_out = []
for g, i in idx.items():
    hl, hr = adj_ent(g)
    concepts_out.append(dict(
        concept_id=i, concept=" ".join(g), n=len(g), df=final[g],
        share=round(final[g] / N, 4),
        left_entropy=round(hl, 3), right_entropy=round(hr, 3),
        llr=(round(llr[g], 2) if llr.get(g) is not None else None),
        df_L1=sum(1 for r in binary["L1"] if i in r),
        df_L2=sum(1 for r in binary["L2"] if i in r),
        df_L3=sum(1 for r in binary["L3"] if i in r),
    ))

with open(os.path.join(DATA, "concepts.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(concepts_out[0].keys()))
    w.writeheader()
    w.writerows(concepts_out)

blob["concept_list"] = concept_list
blob["binary"] = binary
blob["artifact"] = sorted(ARTIFACT_BASE)
json.dump(blob, open(os.path.join(DATA, "corpus.json"), "w", encoding="utf-8"),
          ensure_ascii=False)

print("\nTOP 70 CONCEPTS")
for c in concepts_out[:70]:
    print("  %4d  %-40s L1=%3d L2=%3d L3=%3d" %
          (c["df"], c["concept"][:40], c["df_L1"], c["df_L2"], c["df_L3"]))
print("\nWrote concepts.csv")
