#!/usr/bin/env python3
"""Multiway first-in (unopened) push/fold Nash for 6-max, chip-EV.
Actor jams or folds; each player behind independently calls/folds (Nash via
fictitious play). Equal effective stacks => single pot, winner-take-all (ties
approximated as no-win for both, ~<2% of deals). Uses the validated numpy
7-card evaluator. Outputs data/pushfold_multiway.json (jam + SB/BB call ranges,
with per-hand jam EV for the EV display)."""
import json, os
import numpy as np
from build_equity import evaluate, CLASSES, COMBOS

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
IDX = {n: i for i, n in enumerate(CLASSES)}

# card-pair -> class index, and representative combo per class
CLASS_OF = np.full((52, 52), -1, dtype=np.int64)
for i, n in enumerate(CLASSES):
    for (a, b) in COMBOS[n]:
        CLASS_OF[a, b] = i; CLASS_OF[b, a] = i
REP = np.array([COMBOS[CLASSES[i]][0] for i in range(169)], dtype=np.int64)  # (169,2)

# 6-max seats in action order; blinds in bb
SEATS = ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']
BLIND = {'SB': 0.5, 'BB': 1.0}
def seat_blind(s): return BLIND.get(s, 0.0)

def sample_deals(actor2, m, N, rng):
    """N deals of m opponent hands + 5 board, all distinct from actor2.
    Returns opp_classes (N,m), opp_ge_actor (N,m) bool (opp_score >= actor_score)."""
    keys = rng.random((N, 52)); keys[:, actor2[0]] = 2.0; keys[:, actor2[1]] = 2.0
    order = np.argsort(keys, axis=1)
    picks = order[:, :2 * m + 5]
    opp = picks[:, :2 * m].reshape(N, m, 2)
    board = picks[:, 2 * m:2 * m + 5]
    a7 = np.concatenate([np.tile(actor2, (N, 1)), board], axis=1)
    a_score = evaluate(a7)
    ocl = np.empty((N, m), dtype=np.int64); oge = np.empty((N, m), dtype=bool)
    for i in range(m):
        o7 = np.concatenate([opp[:, i, :], board], axis=1)
        oge[:, i] = evaluate(o7) >= a_score
        ocl[:, i] = CLASS_OF[opp[:, i, 0], opp[:, i, 1]]
    return ocl, oge

def precompute(position, N, rng, seats=SEATS):
    """Per position: pusher deals (vs k behind) and caller deals (per behind seat,
    opp[0]=pusher, opp[1:]=other behind). `seats` = action-order seat list (any size)."""
    a = seats.index(position); behind = seats[a + 1:]; k = len(behind)
    bb = np.array([seat_blind(s) for s in behind])           # blinds of behind seats
    # pusher: opp columns = behind seats in order
    P_oc = np.empty((169, N, k), dtype=np.int64); P_ge = np.empty((169, N, k), dtype=bool)
    for p in range(169):
        oc, ge = sample_deals(REP[p], k, N, rng)
        P_oc[p] = oc; P_ge[p] = ge
    # callers: for each behind seat t, opp0=pusher then other behind
    C_data = []
    for t in range(k):
        others = [i for i in range(k) if i != t]
        ob = bb[others] if others else np.zeros(0)
        pcl = np.empty((169, N), dtype=np.int64); pge = np.empty((169, N), dtype=bool)
        ocl = np.empty((169, N, k - 1), dtype=np.int64); oge = np.empty((169, N, k - 1), dtype=bool)
        for g in range(169):
            oc, ge = sample_deals(REP[g], k, N, rng)   # opp0=pusher, opp1..=other behind
            pcl[g] = oc[:, 0]; pge[g] = ge[:, 0]
            ocl[g] = oc[:, 1:]; oge[g] = ge[:, 1:]
        C_data.append(dict(t=t, others=others, ob=ob, pcl=pcl, pge=pge, ocl=ocl, oge=oge))
    return dict(behind=behind, k=k, bb=bb, b_actor=seat_blind(position),
                tot=float(bb.sum()), P_oc=P_oc, P_ge=P_ge, C=C_data)

def solve(pre, S, T=70, ante=0.0):
    k = pre['k']; bb = pre['bb']; tot = pre['tot'] + ante; b_actor = pre['b_actor']
    P_oc, P_ge = pre['P_oc'], pre['P_ge']
    P = np.ones(169); C = [np.ones(169) for _ in range(k)]
    Ps = np.zeros(169); Cs = [np.zeros(169) for _ in range(k)]
    ev_p = np.zeros(169)
    for it in range(1, T + 1):
        # ---- pusher best response vs caller ranges C ----
        c_all = np.stack([C[i][P_oc[:, :, i]] for i in range(k)], axis=2)   # (169,N,k)
        nonA = ~P_ge
        Sc = (nonA * c_all).sum(2)
        Scb = (nonA * c_all * bb[None, None, :]).sum(2)
        prodNoA = np.prod(np.where(P_ge, 1 - c_all, 1.0), axis=2)
        share = prodNoA * (S * (1 + Sc) + tot - Scb)
        ev_p = (share - S).mean(1)
        pbr = (ev_p > -b_actor).astype(float)
        # ---- caller best responses ----
        cbr = []
        for d in pre['C']:
            t = d['t']; others = d['others']; ob = d['ob']
            if k - 1 > 0:
                cw = np.stack([C[others[q]][d['ocl'][:, :, q]] for q in range(k - 1)], axis=2)
                nonAo = ~d['oge']
                Sco = (nonAo * cw).sum(2)
                Scbo = (nonAo * cw * ob[None, None, :]).sum(2)
                prodNoAo = np.prod(np.where(d['oge'], 1 - cw, 1.0), axis=2)
            else:
                Sco = np.zeros((169, P.shape[0] if False else d['pcl'].shape[1]))
                Scbo = 0.0; prodNoAo = 1.0
            w = P[d['pcl']]                       # (169,N) importance weight by jam range
            canWin = (~d['pge']).astype(float)
            pot = S * (2 + Sco) + tot - bb[t] - Scbo
            net = canWin * prodNoAo * pot - S
            sw = w.sum(1)
            ev_c = (w * net).sum(1) / np.where(sw > 0, sw, 1.0)
            cbr.append((ev_c > -bb[t]).astype(float))
        # ---- fictitious-play averaging ----
        Ps += pbr; P = Ps / it
        for t in range(k):
            Cs[t] += cbr[t]; C[t] = Cs[t] / it
    return P, C, ev_p

def pct(fr): return round(float((fr * W).sum() / W.sum() * 100), 1)
def wclass(n): return 6 if len(n) == 2 else (4 if n[2] == 's' else 12)
W = np.array([wclass(n) for n in CLASSES], dtype=float)

if __name__ == "__main__":
    rng = np.random.default_rng(20260601)
    POSITIONS = ['UTG', 'HJ', 'CO', 'BTN']
    STACKS = [8, 10, 12, 15, 20]
    charts = []; summ = []
    for pos in POSITIONS:
        print(f"precompute {pos} …", flush=True)
        pre = precompute(pos, N=1500, rng=rng)
        behind = pre['behind']
        for S in STACKS:
            P, C, evp = solve(pre, S)
            jp = pct(P)
            summ.append((pos, S, jp))
            jam = {CLASSES[i]: round(float(P[i]) * 100) for i in range(169)}
            ev = {CLASSES[i]: round(float(evp[i]), 3) for i in range(169)}
            charts.append({
                "config": "First-in Push/Fold (6-max, Nash)", "cat": f"First-in Jam — {pos}",
                "key": f"fi_jam_{pos}_{S}", "title": f"{pos} first-in Jam — {S}bb",
                "sizing": f"jam {S}bb", "rangePct": f"jam {jp}%", "aggroLabel": "Jam", "exact": True,
                "notes": f"6-max first-in (unopened) jam from {pos} at {S}bb effective, {len(behind)} players behind. Chip-EV Nash (no ICM) via fictitious play: actor jams or folds, each player behind calls a Nash range. Equal stacks => single pot. Jams {jp}% of hands. Later positions jam wider (fewer players behind); ranges shrink as stack grows. Independent-caller + tie approximations (study-grade).",
                "hands": [{"hand": CLASSES[i], "aggroPct": jam[CLASSES[i]], "callPct": 0, "foldPct": 100 - jam[CLASSES[i]]} for i in range(169)],
                "ev": ev, "evFold": -pre['b_actor'], "evUnit": "bb",
            })
            # caller charts for the blinds (SB, BB) where present
            for t, s in enumerate(behind):
                if s not in ('SB', 'BB'):
                    continue
                cr = {CLASSES[i]: round(float(C[t][i]) * 100) for i in range(169)}
                cp = pct(C[t])
                charts.append({
                    "config": "First-in Push/Fold (6-max, Nash)", "cat": f"Call vs {pos} jam",
                    "key": f"fi_call_{pos}_{s}_{S}", "title": f"{s} call vs {pos} jam — {S}bb",
                    "sizing": f"vs {pos} {S}bb jam", "rangePct": f"call {cp}%", "aggroLabel": "Call", "exact": True,
                    "notes": f"{s} calling a {S}bb first-in jam from {pos} (6-max, chip-EV Nash). Calls {cp}% — tighter when other players are still behind (overcall risk) and as the jam stack grows.",
                    "hands": [{"hand": CLASSES[i], "aggroPct": 0, "callPct": cr[CLASSES[i]], "foldPct": 100 - cr[CLASSES[i]]} for i in range(169)],
                })
    json.dump({"charts": charts}, open(os.path.join(D, "pushfold_multiway.json"), "w"), indent=0)

    print("\n=== first-in jam % (6-max, chip-EV Nash) ===")
    print(f"{'pos':>5} " + " ".join(f"{s}bb" for s in STACKS))
    for pos in POSITIONS:
        row = [f"{j:5.1f}" for (p, s, j) in summ if p == pos]
        print(f"{pos:>5} " + " ".join(row))
    aa = all(c['hands'][IDX['AA']]['aggroPct'] == 100 for c in charts if c['aggroLabel'] == 'Jam')
    print("AA always jam:", aa)
    # later position jams wider than earlier at same stack?
    by = {}
    for p, s, j in summ: by[(p, s)] = j
    mono = all(by[('UTG', s)] <= by[('HJ', s)] <= by[('CO', s)] <= by[('BTN', s)] for s in STACKS)
    print("jam% widens UTG<=HJ<=CO<=BTN at each stack:", mono)
    print("charts:", len(charts), "| saved data/pushfold_multiway.json")
