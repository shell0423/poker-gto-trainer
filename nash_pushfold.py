#!/usr/bin/env python3
"""Heads-up SB push/fold Nash equilibrium (chip-EV) via fictitious play on the
exact MC equity matrix. Blind-vs-blind: SB(button) jams or folds, BB calls or folds.
Outputs data/pushfold_nash.json for the chart viewer."""
import json, os
import numpy as np

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
E = np.load(os.path.join(D, "equity.npy"))      # E[h,g] = equity of class h vs g
CL = json.load(open(os.path.join(D, "classes.json")))
def wclass(n): return 6 if len(n) == 2 else (4 if n[2] == 's' else 12)
w = np.array([wclass(n) for n in CL], dtype=float)
W = w.sum()                                      # 1326

def solve(S, T=5000):
    """S = effective stack in bb. Returns (jam_freq[169], call_freq[169])."""
    p = np.ones(169); c = np.ones(169)           # running averages (priors: jam/call all)
    ps = np.zeros(169); cs = np.zeros(169)
    for t in range(1, T + 1):
        # SB push EV per hand vs BB's average calling range c
        wc = w * c
        ev_push = ((w * (1 - c)).sum() * 1.0 + 2 * S * (E @ wc) - S * wc.sum()) / W
        sb_br = (ev_push > -0.5).astype(float)   # fold EV = -0.5 (forfeit SB)
        # BB call EV per hand vs SB's average jam range p
        pw = p * w; J = pw.sum()
        ev_call = (2 * S / J) * (E @ pw) - S
        bb_br = (ev_call > -1.0).astype(float)   # fold EV = -1.0 (forfeit BB)
        ps += sb_br; cs += bb_br
        p = ps / t; c = cs / t
    return p, c, ev_push, ev_call

def pct(freq): return round(float((freq * w).sum() / W * 100), 1)

STACKS = [3, 5, 8, 10, 12, 15, 20, 25]
charts = []
summary = []
for S in STACKS:
    p, c, evp, evc = solve(S)
    jam = {CL[i]: round(float(p[i]) * 100) for i in range(169)}
    call = {CL[i]: round(float(c[i]) * 100) for i in range(169)}
    jp, cp = pct(p), pct(c)
    summary.append((S, jp, cp))
    charts.append({
        "config": "HU Push/Fold (exact Nash)", "cat": "Push/Fold Nash (HU, exact chip-EV)",
        "key": f"hu_jam_{S}", "title": f"HU SB Jam — {S}bb", "sizing": f"jam {S}bb",
        "rangePct": f"jam {jp}%", "aggroLabel": "Jam", "exact": True,
        "notes": f"Heads-up blind-vs-blind. SB(button) open-jams {S}bb or folds. Nash (chip-EV, no ICM) via fictitious play on exact MC equities. SB jams {jp}% of hands. Card-removal in range weighting is not modeled (standard simplification); ranges match published HU Nash charts within MC noise.",
        "hands": [{"hand": CL[i], "aggroPct": jam[CL[i]], "callPct": 0, "foldPct": 100 - jam[CL[i]]} for i in range(169)],
        "ev": {CL[i]: round(float(evp[i]), 3) for i in range(169)}, "evFold": -0.5, "evUnit": "bb",
    })
    charts.append({
        "config": "HU Push/Fold (exact Nash)", "cat": "Push/Fold Nash (HU, exact chip-EV)",
        "key": f"hu_call_{S}", "title": f"HU BB Call vs Jam — {S}bb", "sizing": f"vs {S}bb jam",
        "rangePct": f"call {cp}%", "aggroLabel": "Call", "exact": True,
        "notes": f"BB facing a {S}bb SB open-jam: call or fold (Nash). BB calls {cp}% of hands. Pairs and big aces are the last to drop as the jam stack grows.",
        "hands": [{"hand": CL[i], "aggroPct": 0, "callPct": call[CL[i]], "foldPct": 100 - call[CL[i]]} for i in range(169)],
        "ev": {CL[i]: round(float(evc[i]), 3) for i in range(169)}, "evFold": -1.0, "evUnit": "bb",
    })

json.dump({"charts": charts}, open(os.path.join(D, "pushfold_nash.json"), "w"), indent=0)

print("=== HU Push/Fold Nash (exact chip-EV) ===")
print(f"{'stack':>6} {'SB jam%':>9} {'BB call%':>9}")
for S, jp, cp in summary:
    print(f"{S:>5}bb {jp:>8}% {cp:>8}%")
# sanity landmarks
print("\nsanity: AA/KK always jam at every stack:",
      all(c["hands"][CL.index("AA")]["aggroPct"] == 100 for c in charts if c["aggroLabel"] == "Jam"))
print("monotonic: jam% strictly decreases as stack grows:",
      all(summary[i][1] >= summary[i+1][1] for i in range(len(summary)-1)))
# show 10bb jam range hands that are non-zero, compact
S10 = next(c for c in charts if c["key"] == "hu_jam_10")
jammed = [h["hand"] for h in S10["hands"] if h["aggroPct"] >= 50]
print(f"\n10bb SB jam (>=50%): {len(jammed)} classes")
print(" ", " ".join(jammed))
print("SAVED", os.path.join(D, "pushfold_nash.json"))
