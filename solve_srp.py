#!/usr/bin/env python3
"""BTN vs BB single-raised-pot FLOP solver (CFR / fictitious play).
Tree: BB checks -> BTN c-bets (one size) or checks -> BB call/fold vs the bet.
Terminals valued by full-board (river) equity (single bet-round model; exact at low
SPR, an approximation deep). A true Nash of THIS abstracted flop game.
Ranges: BTN = open range, BB = flat-call range, from data/charts_100bb.json.
Outputs data/srp_flop.json (per-class BTN c-bet% and BB call/fold% per flop)."""
import json, os
import numpy as np
from itertools import combinations
from build_equity import evaluate, CLASSES, COMBOS

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
R = "23456789TJQKA"; SU = {'s': 0, 'h': 1, 'd': 2, 'c': 3}
def cd(t): return R.index(t[0]) * 4 + SU[t[1]]
def cstr(c): return R[c // 4] + "shdc"[c % 4]

charts = json.load(open(os.path.join(D, "charts_100bb.json")))
def chart(title): return next(c for c in charts if c["title"] == title)
BTN = chart("BTN RFI")            # aggroPct = open frequency
BBD = chart("BB vs BTN open")     # callPct = BB flat (defend by calling)

def weighted_combos(ch, field):
    hands = {h["hand"]: h for h in ch["hands"]}
    out = []
    for name in CLASSES:
        h = hands.get(name)
        if not h: continue
        f = (h.get("aggroPct", 0) if field == "aggro" else h.get("callPct", 0)) / 100.0
        if f <= 0: continue
        for (a, b) in COMBOS[name]:
            out.append((a, b, f, name))
    return out

BTN_C = weighted_combos(BTN, "aggro")
BB_C = weighted_combos(BBD, "call")

def equity_matrix(flop, Bc, Oc):
    """E[i,j] = BTN combo i equity vs BB combo j on this flop (turn+river enumerated)."""
    nB, nO = len(Bc), len(Oc)
    Bi = np.array([[a, b] for (a, b, w, n) in Bc], dtype=np.int64)
    Oi = np.array([[a, b] for (a, b, w, n) in Oc], dtype=np.int64)
    compat = np.ones((nB, nO), dtype=bool)
    for k in range(2):
        for l in range(2):
            compat &= (Bi[:, k][:, None] != Oi[:, l][None, :])
    fset = set(flop)
    deck = [c for c in range(52) if c not in fset]
    wins = np.zeros((nB, nO)); ties = np.zeros((nB, nO)); cnt = np.zeros((nB, nO))
    for (t, r) in combinations(deck, 2):
        board = [flop[0], flop[1], flop[2], t, r]
        vB = (Bi[:, 0] != t) & (Bi[:, 1] != t) & (Bi[:, 0] != r) & (Bi[:, 1] != r)
        vO = (Oi[:, 0] != t) & (Oi[:, 1] != t) & (Oi[:, 0] != r) & (Oi[:, 1] != r)
        sB = evaluate(np.concatenate([Bi, np.tile(board, (nB, 1))], axis=1))
        sO = evaluate(np.concatenate([Oi, np.tile(board, (nO, 1))], axis=1))
        valid = compat & vB[:, None] & vO[None, :]
        wins += (sB[:, None] > sO[None, :]) & valid
        ties += (sB[:, None] == sO[None, :]) & valid
        cnt += valid
    E = np.where(cnt > 0, (wins + 0.5 * ties) / np.maximum(cnt, 1), 0.5)
    return E, compat

def solve_flop(flop, P=5.5, bet_frac=0.66, T=800):
    Bc = [x for x in BTN_C if x[0] not in flop and x[1] not in flop]
    Oc = [x for x in BB_C if x[0] not in flop and x[1] not in flop]
    nB, nO = len(Bc), len(Oc)
    wB = np.array([x[2] for x in Bc]); wO = np.array([x[2] for x in Oc])
    E, compat = equity_matrix(flop, Bc, Oc)
    b = bet_frac * P
    Wc = wO[None, :] * compat                      # BB weights seen by each BTN hand
    den = np.maximum(Wc.sum(1), 1e-9)
    termO = (1 - E) * (P + 2 * b) - b
    sigB = np.full(nB, 0.5); sigO = np.full(nO, 0.5)
    sBsum = np.zeros(nB); sOsum = np.zeros(nO)
    for it in range(1, T + 1):
        # BTN best-responds to BB's avg calling strategy
        term = (1 - sigO)[None, :] * P + sigO[None, :] * (E * (P + 2 * b) - b)
        EV_bet = (Wc * term).sum(1) / den
        EV_check = (Wc * (E * P)).sum(1) / den
        btn_br = (EV_bet > EV_check).astype(float)
        # BB best-responds to BTN's avg betting range
        Bw = (wB * sigB)[:, None] * compat
        denO = np.maximum(Bw.sum(0), 1e-9)
        EV_call = (Bw * termO).sum(0) / denO
        bb_br = (EV_call > 0).astype(float)
        sBsum += btn_br; sOsum += bb_br
        sigB = sBsum / it; sigO = sOsum / it
    # aggregate per class (reach-weighted)
    def agg(combos, sig, w):
        acc = {}
        for k, (a, b2, wt, name) in enumerate(combos):
            d = acc.setdefault(name, [0.0, 0.0])
            d[0] += w[k] * sig[k]; d[1] += w[k]
        return {n: (v[0] / v[1] if v[1] > 0 else 0.0) for n, v in acc.items()}
    cbet = agg(Bc, sigB, wB)
    bbcall = agg(Oc, sigO, wO)
    # overall frequencies (range-weighted)
    cbet_overall = float((wB * sigB).sum() / wB.sum() * 100)
    bbcall_overall = float((wO * sigO).sum() / wO.sum() * 100)
    return cbet, bbcall, cbet_overall, bbcall_overall

FLOPS = [
    ("As7d2c", "ドライ A-high レインボー"),
    ("KsKd4h", "ペアボード K"),
    ("9s8s5h", "ウェット 二色 コネクト"),
    ("Th9h2c", "中位 二色"),
    ("Qh7c2d", "Q-high レインボー"),
    ("6s5s4d", "ロー コネクト 二色"),
]

if __name__ == "__main__":
    out = []
    for s, label in FLOPS:
        flop = [cd(s[i:i+2]) for i in range(0, 6, 2)]
        cbet, bbcall, co, bo = solve_flop(flop)
        print(f"[{s}] {label}: BTN c-bet {co:.1f}% | BB call-vs-cbet {bo:.1f}%")
        # a few sanity classes
        for cl in ["AA", "AKs", "A2s", "72o", "KK", "QJs", "55"]:
            if cl in cbet:
                print(f"    {cl}: cbet {cbet[cl]*100:.0f}%", end="")
        print()
        out.append({"flop": s, "label": label, "cbet_overall": round(co, 1),
                    "bbcall_overall": round(bo, 1),
                    "cbet": {k: round(v * 100) for k, v in cbet.items()},
                    "bbcall": {k: round(v * 100) for k, v in bbcall.items()}})
    json.dump({"flops": out}, open(os.path.join(D, "srp_flop.json"), "w"))
    print("SAVED data/srp_flop.json |", len(out), "flops")
