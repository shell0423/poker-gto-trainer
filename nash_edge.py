#!/usr/bin/env python3
"""EDGE POKER tournament push/fold Nash (chip-EV) with a 1bb big-blind ante.
EDGE structure: 12 players in 4-max tables -> single final table at <=6 -> down to HU.
So the table sizes that actually occur are 4-max (early) and 6->HU (final), all with a
1bb BB-ante (flat dead money in every pot). Reuses the generalized solver in
nash_multiway.py. Outputs data/pushfold_edge.json (jam + SB/BB call ranges, with EV)."""
import json, os
import numpy as np
from nash_multiway import precompute, solve, pct
from build_equity import CLASSES

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
ANTE = 1.0   # EDGE: 1bb big-blind ante (flat dead money per pot)

# (label, action-order seat list, first-in jam positions to output)
FORMATS = [
    ("4-max", ["UTG", "BTN", "SB", "BB"], ["UTG", "BTN"]),               # early game
    ("6-max", ["UTG", "HJ", "CO", "BTN", "SB", "BB"], ["UTG", "HJ", "CO", "BTN"]),  # final table start
    ("HU",    ["SB", "BB"], ["SB"]),                                     # final two
]
STACKS = {"4-max": [8, 10, 12, 15, 20], "6-max": [8, 10, 12, 15, 20], "HU": [5, 8, 10, 12, 15, 20]}
CONFIG = "EDGE Push/Fold (Nash, +1bb ante)"

rng = np.random.default_rng(424242)
charts = []
summ = []
for fmt, seats, positions in FORMATS:
    for pos in positions:
        pre = precompute(pos, 1500, rng, seats=seats)
        behind = pre["behind"]
        for S in STACKS[fmt]:
            P, C, evp = solve(pre, S, ante=ANTE)
            jp = pct(P)
            summ.append((fmt, pos, S, jp))
            title_pos = "SB" if fmt == "HU" else pos
            charts.append({
                "config": CONFIG, "cat": f"{fmt} — {title_pos} jam",
                "key": f"edge_{fmt}_{pos}_jam_{S}", "title": f"{fmt} {title_pos} Jam — {S}bb",
                "sizing": f"jam {S}bb (+ante)", "rangePct": f"jam {jp}%", "aggroLabel": "Jam", "exact": True,
                "notes": f"EDGE POKER {fmt} first-in (unopened) jam from {title_pos} at {S}bb, with the 1bb BB-ante. Chip-EV Nash via fictitious play. The ante adds dead money every pot, so jam ranges are WIDER than ante-free push/fold. EDGE's fast 40bb turbo structure means most of the tournament is played here. Jams {jp}% of hands. (Independent-caller + tie approximations; chip-EV, no ICM — fine for a win-the-tournament objective, loosen toward survival only at the top-6 points bubble.)",
                "hands": [{"hand": CLASSES[i], "aggroPct": round(float(P[i]) * 100), "callPct": 0, "foldPct": 100 - round(float(P[i]) * 100)} for i in range(169)],
                "ev": {CLASSES[i]: round(float(evp[i]), 3) for i in range(169)}, "evFold": -pre["b_actor"], "evUnit": "bb",
            })
            for t, s in enumerate(behind):
                if s not in ("SB", "BB"):
                    continue
                cr = {CLASSES[i]: round(float(C[t][i]) * 100) for i in range(169)}
                cp = pct(C[t])
                charts.append({
                    "config": CONFIG, "cat": f"{fmt} — call vs {title_pos} jam",
                    "key": f"edge_{fmt}_{pos}_{s}call_{S}", "title": f"{fmt} {s} call vs {title_pos} jam — {S}bb",
                    "sizing": f"vs {S}bb jam (+ante)", "rangePct": f"call {cp}%", "aggroLabel": "Call", "exact": True,
                    "notes": f"EDGE POKER {fmt}: {s} calling a {S}bb first-in jam from {title_pos}, 1bb BB-ante. Chip-EV Nash. The ante improves the pot odds to call, so calling ranges are a bit wider than ante-free. Calls {cp}%.",
                    "hands": [{"hand": CLASSES[i], "aggroPct": 0, "callPct": cr[CLASSES[i]], "foldPct": 100 - cr[CLASSES[i]]} for i in range(169)],
                })

json.dump({"charts": charts}, open(os.path.join(D, "pushfold_edge.json"), "w"), indent=0)

print("=== EDGE push/fold (+1bb ante) jam % ===")
for fmt, seats, positions in FORMATS:
    print(f"[{fmt}]")
    for pos in positions:
        row = [f"{j:4.1f}" for (f, p, s, j) in summ if f == fmt and p == pos]
        st = STACKS[fmt]
        print(f"  {('SB' if fmt=='HU' else pos):>4}: " + " ".join(f"{s}bb={j}" for ((f, p, ss, j), s) in zip([x for x in summ if x[0]==fmt and x[1]==pos], st)))
print(f"charts: {len(charts)} | saved data/pushfold_edge.json")
# sanity: ante should widen jam vs the no-ante 6-max baseline (BTN 10bb no-ante was ~36%)
b = {(f, p, s): j for f, p, s, j in summ}
print("4-max BTN 10bb jam% (+ante):", b.get(("4-max", "BTN", 10)), "(expect wider than 6-max no-ante ~36%)")
print("HU SB 10bb jam% (+ante):", b.get(("HU", "SB", 10)), "(expect wider than no-ante ~58%)")
