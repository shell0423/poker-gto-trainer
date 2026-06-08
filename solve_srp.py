#!/usr/bin/env python3
"""BTN vs BB single-raised-pot FLOP solver — vector CFR.
Tree: BB checks -> BTN {check, bet 33%, bet 75%} -> BB {fold, call, check-raise 3.5x}
      -> BTN {fold, call}. Terminals valued by full-board (river) equity
      (single bet-round model: exact at low SPR, an approximation deep). A true Nash
      of THIS abstracted flop game (multi-size + check-raise).
Ranges from data/charts_100bb.json (BTN open / BB flat). Outputs data/srp_flop.json."""
import json, os, sys
import numpy as np
from itertools import combinations
from build_equity import evaluate, CLASSES, COMBOS

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
R = "23456789TJQKA"; SU = {'s': 0, 'h': 1, 'd': 2, 'c': 3}
def cd(t): return R.index(t[0]) * 4 + SU[t[1]]

charts = json.load(open(os.path.join(D, "charts_100bb.json")))
def chart(title): return next(c for c in charts if c["title"] == title)
BTN_C = None; BB_C = None
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
BTN_C = weighted_combos(chart("BTN RFI"), "aggro")
BB_C = weighted_combos(chart("BB vs BTN open"), "call")

def equity_matrix(flop, Bi, Oi):
    nB, nO = len(Bi), len(Oi)
    compat = np.ones((nB, nO), dtype=bool)
    for k in range(2):
        for l in range(2):
            compat &= (Bi[:, k][:, None] != Oi[:, l][None, :])
    deck = [c for c in range(52) if c not in flop]
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

def solve_flop(flop, P=5.5, T=1500):
    Bc = [x for x in BTN_C if x[0] not in flop and x[1] not in flop]
    Oc = [x for x in BB_C if x[0] not in flop and x[1] not in flop]
    nB, nO = len(Bc), len(Oc)
    wB = np.array([x[2] for x in Bc]); wO = np.array([x[2] for x in Oc])
    Bi = np.array([[x[0], x[1]] for x in Bc], dtype=np.int64)
    Oi = np.array([[x[0], x[1]] for x in Oc], dtype=np.int64)
    E, compat = equity_matrix(flop, Bi, Oi)
    b1, b2 = 0.33 * P, 0.75 * P
    def SD(Q, iB, iO): return {'t': 'term', 'PB': (E * Q - iB) * compat, 'PO': ((1 - E) * Q - iO) * compat}
    def Ffold(): return {'t': 'term', 'PB': P * compat, 'PO': 0.0 * compat}     # BB folds, BTN wins P
    def Bfold(iB): return {'t': 'term', 'PB': (-iB) * compat, 'PO': (P + iB) * compat}  # BTN folds to raise
    def betbranch(b, tag):
        r = 3.5 * b
        return {'t': 'O', 'is': 'bbvs' + tag, 'a': ['fold', 'call', 'raise'],
                'ch': [Ffold(), SD(P + 2 * b, b, b),
                       {'t': 'B', 'is': 'btnvr' + tag, 'a': ['fold', 'call'],
                        'ch': [Bfold(b), SD(P + 2 * r, r, r)]}]}
    root = {'t': 'B', 'is': 'flop', 'a': ['check', 'bet1', 'bet2'],
            'ch': [SD(P, 0, 0), betbranch(b1, '1'), betbranch(b2, '2')]}
    regret, stratsum = {}, {}
    def strat(infoset, n, nA):
        rg = regret.get(infoset)
        if rg is None: return np.full((n, nA), 1.0 / nA)
        pos = np.maximum(rg, 0); s = pos.sum(1, keepdims=True)
        return np.where(s > 0, pos / s, 1.0 / nA)
    def cfr(node, pB, pO):
        if node['t'] == 'term':
            return (node['PB'] * pO[None, :]).sum(1), (node['PO'] * pB[:, None]).sum(0)
        nA = len(node['a'])
        if node['t'] == 'B':
            st = strat(node['is'], nB, nA); cu = np.zeros((nB, nA)); uO = np.zeros(nO)
            for a, ch in enumerate(node['ch']):
                cb, co = cfr(ch, pB * st[:, a], pO); cu[:, a] = cb; uO += co
            uB = (st * cu).sum(1)
            regret[node['is']] = regret.get(node['is'], np.zeros((nB, nA))) + (cu - uB[:, None])
            stratsum[node['is']] = stratsum.get(node['is'], np.zeros((nB, nA))) + pB[:, None] * st
            return uB, uO
        else:
            st = strat(node['is'], nO, nA); cu = np.zeros((nO, nA)); uB = np.zeros(nB)
            for a, ch in enumerate(node['ch']):
                cb, co = cfr(ch, pB, pO * st[:, a]); cu[:, a] = co; uB += cb
            uO = (st * cu).sum(1)
            regret[node['is']] = regret.get(node['is'], np.zeros((nO, nA))) + (cu - uO[:, None])
            stratsum[node['is']] = stratsum.get(node['is'], np.zeros((nO, nA))) + pO[:, None] * st
            return uB, uO
    for _ in range(T):
        cfr(root, wB.copy(), wO.copy())
    def avg(infoset):
        ss = stratsum[infoset]; s = ss.sum(1, keepdims=True)
        return np.where(s > 0, ss / s, 0.0)
    sB = avg('flop')                     # nB x [check,bet1,bet2]
    bbv1 = avg('bbvs1'); bbv2 = avg('bbvs2')  # nO x [fold,call,raise]
    # BTN sizing reach for weighting BB defense
    W1 = float((wB * sB[:, 1]).sum()); W2 = float((wB * sB[:, 2]).sum())
    Wt = max(W1 + W2, 1e-9)
    bbdef = (W1 * bbv1 + W2 * bbv2) / Wt  # nO x [fold,call,raise]
    def agg(combos, vec, w):
        acc = {}
        for k, (a, b2, wt, name) in enumerate(combos):
            d = acc.setdefault(name, [np.zeros(vec.shape[1]), 0.0])
            d[0] += w[k] * vec[k]; d[1] += w[k]
        return {n: (v[0] / v[1]) for n, v in acc.items() if v[1] > 0}
    btn = agg(Bc, sB, wB)        # name -> [check,bet1,bet2]
    bb = agg(Oc, bbdef, wO)      # name -> [fold,call,raise]
    cbet_overall = float((wB * (sB[:, 1] + sB[:, 2])).sum() / wB.sum() * 100)
    raise_overall = float((wO * bbdef[:, 2]).sum() / wO.sum() * 100)
    call_overall = float((wO * bbdef[:, 1]).sum() / wO.sum() * 100)
    cbet = {n: round((v[1] + v[2]) * 100) for n, v in btn.items()}
    cbet_small = {n: round(v[1] * 100) for n, v in btn.items()}
    cbet_big = {n: round(v[2] * 100) for n, v in btn.items()}
    bb_call = {n: round(v[1] * 100) for n, v in bb.items()}
    bb_raise = {n: round(v[2] * 100) for n, v in bb.items()}
    return dict(cbet=cbet, cbet_small=cbet_small, cbet_big=cbet_big, bb_call=bb_call, bb_raise=bb_raise,
                cbet_overall=round(cbet_overall, 1), call_overall=round(call_overall, 1), raise_overall=round(raise_overall, 1))

# representative flops across textures
FLOPS = [
    ("As7d2c","A高ドライ"),("AsKd5c","A高2ブロードウェイ"),("AhAd9c","Aペア"),("Ks8h3c","K高ドライ"),
    ("KsKd4h","Kペア"),("QhJsTd","ブロードウェイ連結"),("Qh7c2d","Q高ドライ"),("Jh9d4c","J高ギャップ"),
    ("Th9h2c","中位二色"),("Ts8d5c","中位ギャップ"),("9s8s5h","ウェット二色連結"),("9h6c3d","中低バラ"),
    ("8c7d6h","連結ミドル"),("8s8d3c","8ペア"),("7s6h2d","低めバラ"),("6s5s4d","ロー連結二色"),
    ("5h4d3c","ロー連結"),("4s4h2d","低ペア"),("AhKhQh","モノトーンブロードウェイ"),("9d6d3d","モノトーン中低"),
    ("Ks9s4s","モノトーンK"),("AsQh7h","A高フラドロ"),("KhQd2c","KQバラ"),("JsTs6d","JT二色"),
    ("Td7c3h","T高バラ"),("9s9h4c","9ペア"),("7h7d2s","7ペア"),("As5s3h","Aホイール二色"),
    ("KhJh5c","KJフラドロ"),("Qc9c4h","Q9フラドロ"),("Jd8d5s","J8二色"),("Th6h2c","T6二色"),
    ("8h5h3d","低フラドロ"),("6c4c2h","超ロー二色"),("AsAhKd","AAK"),("2s2d2h","モノ222は不可…","skip"),
    ("Ks7d7h","K77ツーペア盤"),("QsJd9c","QJ9連結バラ"),("Th9c8d","T98連結バラ"),("5s5d5h","555は不可…","skip"),
]
FLOPS = [f for f in FLOPS if len(f) == 2]  # drop placeholders

if __name__ == "__main__":
    out = []
    for s, label in FLOPS:
        flop = [cd(s[i:i+2]) for i in range(0, 6, 2)]
        if len(set(flop)) != 3:  # skip impossible (duplicate card)
            continue
        res = solve_flop(flop)
        print(f"[{s}] {label}: c-bet {res['cbet_overall']}% | BB call {res['call_overall']}% raise {res['raise_overall']}%", flush=True)
        res["flop"] = s; res["label"] = label
        out.append(res)
        json.dump({"flops": out}, open(os.path.join(D, "srp_flop.json"), "w"))  # incremental save
    print("SAVED data/srp_flop.json |", len(out), "flops")
