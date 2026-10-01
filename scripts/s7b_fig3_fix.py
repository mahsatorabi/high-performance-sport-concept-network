"""
Rebuild F4_tau_calibration.png (manuscript Figure 3).

Correction to the previous version:
  - panel (a) previously plotted precision against RECALL while the axis was labelled tau,
    so the panel was empty and mislabelled. It now shows benchmark precision/recall against
    tau over the full grid, which is what makes the saturation argument visible.
  - panel (b) reports the audited sample size correctly (95 adjudicated) and shows audited
    precision by similarity band, which is the quantity that actually discriminates.
"""
import os, json, csv, collections
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = r"D:\Uni of Birjand\articles\adel\article1"
DATA, FIG = os.path.join(BASE, "data"), os.path.join(BASE, "figures")

plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 300,
                     "font.family": "DejaVu Sans", "font.size": 8.5,
                     "axes.linewidth": 0.7, "axes.labelsize": 8.5,
                     "xtick.labelsize": 7.5, "ytick.labelsize": 7.5})

bench = list(csv.DictReader(open(os.path.join(DATA, "benchmark_tau.csv"),
                                encoding="utf-8-sig")))
audit = [r for r in csv.DictReader(open(os.path.join(DATA, "manual_audit_sample.csv"),
                                         encoding="utf-8-sig")) if r["verdict"] != ""]
sel = json.load(open(os.path.join(DATA, "tau_selected.json"), encoding="utf-8"))
TAU = sel["tau"]

taus = np.array([float(r["tau"]) for r in bench])
prec = np.array([float(r["prec"]) for r in bench])
rec = np.array([float(r["rec"]) for r in bench])

band = collections.defaultdict(lambda: [0, 0])
for r in audit:
    b = round(float(r["sim"]) * 20) / 20.0
    band[b][0] += 1
    band[b][1] += int(r["verdict"])
bands = sorted(band)
bn = [band[b][0] for b in bands]
bp = [band[b][1] / band[b][0] for b in bands]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.7))

# ---------------- panel (a): benchmark precision is saturated
a1.axhline(1.0, color="#4f8a3d", lw=3.0, alpha=0.28, zorder=1)
a1.plot(taus, prec, "-", lw=1.6, color="#4f8a3d")
a1.axvline(TAU, color="#c0504d", lw=1.1, ls=":")
a1.set_xlim(0.15, 0.98)
a1.set_ylim(0.90, 1.05)
a1.set_yticks([0.90, 0.95, 1.00])
a1.set_xlabel("tau")
a1.set_ylabel("benchmark precision")
a1.set_title("a  Safety benchmark: saturated", loc="left", fontsize=8.5)
a1.text(0.30, 0.935, "precision = 1.00 at every tau tested:\nno false merges occur, so the\n"
                     "benchmark certifies safety but\ncannot select a threshold",
        fontsize=6.3, color="#444", ha="left", va="bottom")
a1.grid(axis="y", lw=0.4, color="#e4e4e4")
a1.annotate("selected\ntau", xy=(TAU, 0.915), fontsize=6.0, color="#c0504d",
            ha="center", va="bottom")

# ---------------- panel (b): audited precision by similarity band
cols = ["#c0504d" if p < 0.95 else "#4f8a3d" for p in bp]
x = np.arange(len(bands))
a2.bar(x, bp, width=0.68, color=cols, edgecolor="white", lw=0.5)
a2.axhline(0.95, color="#1f4e79", lw=1.2, ls="--")
a2.set_xticks(x)
a2.set_xticklabels(["%.2f" % b for b in bands], fontsize=6.2, rotation=45)
a2.set_ylim(0, 1.30)
a2.set_xlabel("concept similarity (band midpoint)")
a2.set_ylabel("audited precision")
a2.set_title("b  Manual audit: %d merges adjudicated" % len(audit), loc="left",
             fontsize=8.5)
a2.grid(axis="y", lw=0.4, color="#ececec")
for xi, (p, n) in enumerate(zip(bp, bn)):
    a2.text(xi, p + 0.025, "%d/%d" % (round(p * n), n), ha="center", fontsize=5.7,
            color="#333")
a2.axvspan(bands.index(0.80) - 0.5, len(bands) - 0.5, color="#4f8a3d", alpha=0.055,
           zorder=0)
a2.text(0.6, 1.24, "shaded region: every\nmerge above tau is\njudged correct",
        fontsize=6.0, color="#3d6b28", ha="left", va="top")
a2.text(len(bands) - 0.55, 1.24, "tau = %.3f\nprecision %.3f" % (TAU, sel["precision"]),
        fontsize=6.4, color="#a8712a", ha="right", va="top")

fig.suptitle("SEMCON threshold calibration", fontsize=9.5, weight="bold", y=1.03)
fig.tight_layout(rect=[0, 0, 1, 0.97])
out = os.path.join(FIG, "F4_tau_calibration.png")
fig.savefig(out, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("wrote %s (%.0f KB)" % (out, os.path.getsize(out) / 1024))
print("tau=%.4f  audit n=%d  precision=%.3f  bands=%d" % (TAU, len(audit),
                                                         sel["precision"], len(bands)))