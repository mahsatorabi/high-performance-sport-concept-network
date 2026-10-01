"""Diagnostic: scan the manuscript for formulaic / AI-tell prose patterns."""
import re, sys, collections
from docx import Document

p = r"D:\Uni of Birjand\articles\adel\article1\Article1_manuscript.docx"
d = Document(p)
texts = [x.text for x in d.paragraphs if x.text.strip()]
body = "\n".join(texts)

PATTERNS = {
    "em dash (—)": r"—",
    "semicolon-heavy 'not X but Y'": r"\bnot\b[^.]{0,40}\bbut\b",
    "triadic list (a, b, and c)": r"\b\w+,\s+\w+,?\s+and\s+\w+\b",
    "'It is worth noting'": r"[Ii]t is worth noting",
    "'Importantly/N Notably/ Crucially'": r"\b(Importantly|Notably|Crucially|Importantly)\b",
    "'This has a direct implication'": r"[Tt]his has a (direct|clear|practical) ",
    "'It should be noted'": r"It should be noted",
    "'However,' at sentence start": r"(?m)(?:^|(?<=\. ))However,",
    "'Moreover/Furthermore/Therefore'": r"\b(MMoreover|Furthermore|Therefore|Nevertheless)\b",
    "'In conclusion'": r"[Ii]n conclusion",
    "'plays a (key|crucial|central) role'": r"plays a (key|crucial|central|vital) role",
    "'delve/underscore/realm/tapestry'": r"\b(delve|underscore|realm|tapestry|testament|landscape of)\b",
    "'stands as'": r"stands as\b",
    "'it is important to note'": r"it is important to note",
    "colon-then-list": r":\s+[a-z]+\s+[a-z]+,\s+[a-z]+",
    "parenthetical gloss in body": r"\s\([a-z][^)]{15,}\)",
}

print("=" * 72)
print("PROSE PATTERN SCAN")
print("=" * 72)
for name, pat in PATTERNS.items():
    hits = re.findall(pat, body)
    print("%-38s %4d" % (name, len(hits)))

# sentence length distribution
sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", body) if len(s.strip()) > 25]
lens = sorted(len(s.split()) for s in sents)
import statistics
print("\nsentences: %d   mean %.1f words   sd %.1f" % (
    len(lens), statistics.mean(lens), statistics.pstdev(lens)))
print("  quartiles: %d / %d / %d / %d" % (
    lens[len(lens)//4], lens[len(lens)//2], lens[3*len(lens)//4], lens[-1]))
short = sum(1 for x in lens if x <= 12)
mid = sum(1 for x in lens if 13 <= x <= 24)
lng = sum(1 for x in lens if x >= 25)
print("  short (<=12w): %d   medium: %d   long (>=25w): %d" % (short, mid, lng))

# paragraph openings
print("\nmost common paragraph openings (4-word stems):")
op = collections.Counter(" ".join(t.split()[:4]) for t in texts if len(t.split()) > 12)
for k, v in op.most_common(10):
    if v > 2:
        print("   %-34s %d" % (k, v))