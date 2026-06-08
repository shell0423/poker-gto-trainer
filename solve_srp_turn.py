#!/usr/bin/env python3
"""BTN vs BB SRP — TWO-STREET solver (flop + turn), river collapsed to equity.
This includes the turn barrel, so flop c-bet frequencies become realistic
(unlike the single-street solve_srp.py which understates betting).

Tree (per flop, pot P0):
  FLOP: BB checks -> BTN {check, bet F=2/3 pot}
        bet -> BB {fold, call}
        check / bet-call -> TURN (chance over 49 cards, card removal)
  TURN (4-card board): BB checks -> BTN {check, bet 2/3 pot} -> BB {fold, call}
        terminals valued by RIVER equity on the 4-card board.
Simplifications: one bet size per street, no donk/check-raise on the turn,
no flop check-raise. River = full equity (so river chance is exact; the only
approximation is the turn betting abstraction). Outputs data/srp_turn.json."""
import json, os, sys
import numpy as np
from itertools import combinations
from build_equity import evaluate, CLASSES, COMBOS

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
R = "23456789TJQKA"; SU = {'s': 0, 'h': 1, 'd': 2, 'c': 3}
def cd(t): return R.index(t[0]) * 4 + SU[t[1]]

charts = json.load(open(os.path.join(D, "charts_100bb.json")))
def chart(title): return next(c for c in charts if c["title"] == title)
def weighted_combos(ch, field):
    hands = {h["hand"]: h for h in ch["hands"]}; out = []
    for name in CLASSES:
        h = hands.get(name)
        if not h: continue
        f = (h.get("aggroPct", 0) if field == "aggro" else h.get("callPct", 0)) / 100.0
        if f <= 0: continue
        for (a, b) in COMBOS[name]:
            out.append((a, b, f, name))
    return out
BTN_C = weighted_combos(chart("BTN RFI"), "aggro")
BB_C = weighted_combos(chart("BB vs BTN open"), "call")

def turn_equities(flop, Bi, Oi):
    """For each turn card t: river-equity matrix E[t] (nB x nO) and validity masks."""
    nB, nO = len(Bi), len(Oi)
    compat = np.ones((nB, nO), dtype=bool)
    for k in range(2):
        for l in range(2):
            compat &= (Bi[:, k][:, None] != Oi[:, l][None, :])
    deck = [c for c in range(52) if c not in flop]
    Et, vB, vO = {}, {}, {}
    for t in deck:
        mB = ~((Bi[:, 0] == t) | (Bi[:, 1] == t)); mO = ~((Oi[:, 0] == t) | (Oi[:, 1] == t))
        vB[t] = mB; vO[t] = mO
        wins = np.zeros((nB, nO)); ties = np.zeros((nB, nO)); cnt = np.zeros((nB, nO))
        for r in deck:
            if r == t: continue
            board = [flop[0], flop[1], flop[2], t, r]
            rvB = mB & (Bi[:, 0] != r) & (Bi[:, 1] != r)
            rvO = mO & (Oi[:, 0] != r) & (Oi[:, 1] != r)
            sB = evaluate(np.concatenate([Bi, np.tile(board, (nB, 1))], axis=1))
            sO = evaluate(np.concatenate([Oi, np.tile(board, (nO, 1))], axis=1))
            valid = compat & rvB[:, None] & rvO[None, :]
            wins += (sB[:, None] > sO[None, :]) & valid
            ties += (sB[:, None] == sO[None, :]) & valid
            cnt += valid
        Et[t] = np.where(cnt > 0, (wins + 0.5 * ties) / np.maximum(cnt, 1), 0.5)
    return Et, vB, vO, compat, deck

def solve_flop(flop, P0=5.5, Fr=0.66, Tr=0.66, IT=500):
    Bc = [x for x in BTN_C if x[0] not in flop and x[1] not in flop]
    Oc = [x for x in BB_C if x[0] not in flop and x[1] not in flop]
    nB, nO = len(Bc), len(Oc)
    wB = np.array([x[2] for x in Bc]); wO = np.array([x[2] for x in Oc])
    Bi = np.array([[x[0], x[1]] for x in Bc], dtype=np.int64)
    Oi = np.array([[x[0], x[1]] for x in Oc], dtype=np.int64)
    Et, vBm, vOm, compat, deck = turn_equities(flop, Bi, Oi)
    Nturn = len(deck); F = Fr * P0
    regret, stratsum = {}, {}
    def strat(key, n, nA):
        rg = regret.get(key)
        if rg is None: return np.full((n, nA), 1.0 / nA)
        pos = np.maximum(rg, 0); s = pos.sum(1, keepdims=True)
        return np.where(s > 0, pos / s, 1.0 / nA)
    def acc(key, n, nA, reg_delta, ss_delta):
        regret[key] = regret.get(key, np.zeros((n, nA))) + reg_delta
        stratsum[key] = stratsum.get(key, np.zeros((n, nA))) + ss_delta

    def turn_cfr(t, path, pB, pO):
        E = Et[t]; m = 0.0 if path == 'x' else F; potT = P0 + 2 * m; T = Tr * potT
        PB_cc = (E * potT - m) * compat; PO_cc = ((1 - E) * potT - m) * compat
        PB_bf = (P0 + m) * compat;       PO_bf = (-m) * compat
        PB_bc = (E * (potT + 2 * T) - (m + T)) * compat
        PO_bc = ((1 - E) * (potT + 2 * T) - (m + T)) * compat
        stB = strat(('bt', t, path), nB, 2)        # [check, bet]
        pB_chk = pB * stB[:, 0]; pB_bet = pB * stB[:, 1]
        stO = strat(('bbt', t, path), nO, 2)        # [fold, call]
        uB_check = (PB_cc * pO[None, :]).sum(1)
        uB_betff = (PB_bf * pO[None, :])            # BTN val if BB folds (per j weighted later)
        uB_bet = ((stO[:, 0][None, :] * PB_bf + stO[:, 1][None, :] * PB_bc) * pO[None, :]).sum(1)
        uB = stB[:, 0] * uB_check + stB[:, 1] * uB_bet
        acc(('bt', t, path), nB, 2, np.stack([uB_check - uB, uB_bet - uB], 1), pB[:, None] * stB)
        uO_fold = (PO_bf * pB_bet[:, None]).sum(0)
        uO_call = (PO_bc * pB_bet[:, None]).sum(0)
        uO_betnode = stO[:, 0] * uO_fold + stO[:, 1] * uO_call
        acc(('bbt', t, path), nO, 2, np.stack([uO_fold - uO_betnode, uO_call - uO_betnode], 1), pO[:, None] * stO)
        uO_check = (PO_cc * pB_chk[:, None]).sum(0)
        uO = uO_check + uO_betnode
        return uB, uO

    def chance(path, pB, pO):
        uB = np.zeros(nB); uO = np.zeros(nO)
        for t in deck:
            vB = vBm[t]; vO = vOm[t]
            cb, co = turn_cfr(t, path, pB * vB, pO * vO)
            uB += vB * cb; uO += vO * co
        return uB / Nturn, uO / Nturn

    def flop_cfr(pB, pO):
        stFB = strat('fb', nB, 2)                   # [check, bet]
        uB_chk, uO_chk = chance('x', pB * stFB[:, 0], pO)
        pB_bet = pB * stFB[:, 1]
        stFO = strat('fbb', nO, 2)                   # [fold, call]
        # fold terminal: BTN wins P0, BB 0
        PB_ff = P0 * compat
        uB_ff = (PB_ff * (pO * stFO[:, 0])[None, :]).sum(1)
        uB_callbr, uO_callbr = chance('bc', pB_bet, pO * stFO[:, 1])
        uB_bet = uB_ff + uB_callbr
        # BB node (vs flop bet)
        uO_fold = np.zeros(nO)                        # PO_ff = 0
        uO_call = uO_callbr
        uO_betnode = stFO[:, 0] * uO_fold + stFO[:, 1] * uO_call
        acc('fbb', nO, 2, np.stack([uO_fold - uO_betnode, uO_call - uO_betnode], 1), pO[:, None] * stFO)
        uB = stFB[:, 0] * uB_chk + stFB[:, 1] * uB_bet
        uO = uO_chk + uO_betnode
        acc('fb', nB, 2, np.stack([uB_chk - uB, uB_bet - uB], 1), pB[:, None] * stFB)
        return uB, uO

    for _ in range(IT):
        flop_cfr(wB.copy(), wO.copy())
    def avg(key):
        ss = stratsum[key]; s = ss.sum(1, keepdims=True)
        return np.where(s > 0, ss / s, 0.0)
    sFB = avg('fb')                                  # nB x [check, bet]
    sFO = avg('fbb')                                 # nO x [fold, call]
    def agg(combos, vec, w):
        accm = {}
        for k, (a, b, wt, name) in enumerate(combos):
            d = accm.setdefault(name, [np.zeros(vec.shape[1]), 0.0])
            d[0] += w[k] * vec[k]; d[1] += w[k]
        return {n: v[0] / v[1] for n, v in accm.items() if v[1] > 0}
    btn = agg(Bc, sFB, wB); bb = agg(Oc, sFO, wB if False else wO)
    cbet = {n: round(v[1] * 100) for n, v in btn.items()}
    bb_call = {n: round(v[1] * 100) for n, v in bb.items()}
    cbet_overall = float((wB * sFB[:, 1]).sum() / wB.sum() * 100)
    call_overall = float((wO * sFO[:, 1]).sum() / wO.sum() * 100)
    return dict(cbet=cbet, bb_call=bb_call,
                cbet_overall=round(cbet_overall, 1), call_overall=round(call_overall, 1))

FLOPS = [
    ("As7d2c","A高ドライ"),("AsKd5c","A高2ブロードウェイ"),("AhAd9c","Aペア"),("Ks8h3c","K高ドライ"),
    ("KsKd4h","Kペア"),("QhJsTd","ブロードウェイ連結"),("Qh7c2d","Q高ドライ"),("Jh9d4c","J高ギャップ"),
    ("Th9h2c","中位二色"),("Ts8d5c","中位ギャップ"),("9s8s5h","ウェット二色連結"),("9h6c3d","中低バラ"),
    ("8c7d6h","連結ミドル"),("8s8d3c","8ペア"),("7s6h2d","低めバラ"),("6s5s4d","ロー連結二色"),
    ("5h4d3c","ロー連結"),("4s4h2d","低ペア"),("AhKhQh","モノトーンブロードウェイ"),("9d6d3d","モノトーン中低"),
    ("Ks9s4s","モノトーンK"),("AsQh7h","A高フラドロ"),("KhQd2c","KQバラ"),("JsTs6d","JT二色"),
    ("Td7c3h","T高バラ"),("9s9h4c","9ペア"),("7h7d2s","7ペア"),("As5s3h","Aホイール二色"),
    ("KhJh5c","KJフラドロ"),("Qc9c4h","Q9フラドロ"),("Jd8d5s","J8二色"),("Th6h2c","T6二色"),
    ("8h5h3d","低フラドロ"),("6c4c2h","超ロー二色"),("AsAhKd","AAK"),
    ("Ks7d7h","K77ツーペア盤"),("QsJd9c","QJ9連結バラ"),("Th9c8d","T98連結バラ"),
]

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    out = []
    for s, label in FLOPS:
        if only and s != only: continue
        flop = [cd(s[i:i+2]) for i in range(0, 6, 2)]
        res = solve_flop(flop)
        print(f"[{s}] {label}: c-bet {res['cbet_overall']}% | BB call {res['call_overall']}%", flush=True)
        res["flop"] = s; res["label"] = label
        out.append(res)
        json.dump({"flops": out}, open(os.path.join(D, "srp_turn.json"), "w"))
    print("SAVED data/srp_turn.json |", len(out), "flops")
