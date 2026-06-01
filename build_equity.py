#!/usr/bin/env python3
"""Vectorized Monte-Carlo preflop all-in equity matrix (169x169 hand classes).
No external poker lib — pure numpy 7-card evaluator. Outputs equity.npy + classes.json."""
import json, os, sys
import numpy as np

RANKS = "23456789TJQKA"          # index 0..12 = value 2..A
RIDX = np.arange(13)
B = 16
BASE = B ** 5

# ---- hand classes (169) in 13x13 display order (rows/cols high->low: A,K,...,2) ----
DISP = "AKQJT98765432"
def rv(ch): return RANKS.index(ch)   # value index 0..12

def combos_for(name):
    """name like 'AA','AKs','AKo' -> list of (cardA,cardB) with card=rank*4+suit."""
    if len(name) == 2:                       # pair
        r = rv(name[0]); cs = [r*4+s for s in range(4)]
        return [(cs[a], cs[b]) for a in range(4) for b in range(a+1,4)]
    hi, lo, t = rv(name[0]), rv(name[1]), name[2]
    out = []
    if t == 's':
        for s in range(4): out.append((hi*4+s, lo*4+s))
    else:
        for s1 in range(4):
            for s2 in range(4):
                if s1 != s2: out.append((hi*4+s1, lo*4+s2))
    return out

CLASSES, COMBOS = [], {}
for i in range(13):
    for j in range(13):
        a, b = DISP[i], DISP[j]
        if i == j: nm = a + a
        elif i < j: nm = a + b + 's'
        else:       nm = b + a + 'o'
        if nm not in COMBOS:
            CLASSES.append(nm); COMBOS[nm] = np.array(combos_for(nm), dtype=np.int64)
# CLASSES now has 169 unique names
assert len(CLASSES) == 169, len(CLASSES)
IDX = {n: k for k, n in enumerate(CLASSES)}

# ---- straights (high value, rank-index set), ordered high -> low ----
STRAIGHTS = []
for hi in range(12, 3, -1):                  # 12(A-high)..4(6-high)
    STRAIGHTS.append((hi, list(range(hi-4, hi+1))))
STRAIGHTS.append((3, [12, 0, 1, 2, 3]))      # wheel (5-high)

def straight_high(pres):                      # pres (N,13) bool -> (N,) high value or -1
    sh = np.full(pres.shape[0], -1, dtype=np.int64)
    for hi, idxs in STRAIGHTS:
        hit = pres[:, idxs].all(axis=1) & (sh < 0)
        sh[hit] = hi
    return sh

def topk(pres, k):                            # top-k present rank values (N,k), pad 0
    pres = pres.copy()
    N = pres.shape[0]
    out = np.zeros((N, k), dtype=np.int64)
    ar = np.arange(N)
    for t in range(k):
        hi = np.where(pres, RIDX, -1).max(axis=1)
        out[:, t] = np.maximum(hi, 0)
        v = hi >= 0
        pres[ar[v], hi[v]] = False
    return out

def evaluate(cards7):                          # (N,7) ints 0..51 -> (N,) score int64
    N = cards7.shape[0]
    rank = cards7 // 4; suit = cards7 % 4
    sp = np.zeros((N, 4, 13), dtype=np.int8)
    rows = np.repeat(np.arange(N), 7)
    sp[rows, suit.ravel(), rank.ravel()] = 1
    rc = sp.sum(axis=1)                         # (N,13) counts
    pres = rc > 0
    suit_count = sp.sum(axis=2)                 # (N,4)
    is_flush = suit_count.max(axis=1) >= 5
    flush_suit = suit_count.argmax(axis=1)
    flush_pres = sp[np.arange(N), flush_suit].astype(bool)

    straight_h = straight_high(pres)
    sf = straight_high(flush_pres)
    sf = np.where(is_flush, sf, -1)

    has4 = (rc == 4).any(axis=1)
    quad_rank = np.where(rc == 4, RIDX, -1).max(axis=1)
    qk = np.where(pres & (RIDX != quad_rank[:, None]), RIDX, -1).max(axis=1)

    trips = rc == 3; pairs = rc == 2
    n_trip = trips.sum(axis=1); n_pair = pairs.sum(axis=1)
    top_trip = np.where(trips, RIDX, -1).max(axis=1)
    second_trip = np.where(trips & (RIDX < top_trip[:, None]), RIDX, -1).max(axis=1)
    top_pair = np.where(pairs, RIDX, -1).max(axis=1)
    fh_has = (n_trip >= 1) & ((n_trip >= 2) | (n_pair >= 1))
    fh_pair = np.maximum(second_trip, top_pair)

    ftop = topk(flush_pres, 5)
    tkick = topk(pres & (RIDX != top_trip[:, None]), 2)
    psorted = topk(pairs, 2)
    p1, p2 = psorted[:, 0], psorted[:, 1]
    tp_kick = topk(pres & (RIDX != p1[:, None]) & (RIDX != p2[:, None]), 1)[:, 0]
    okick = topk(pres & (RIDX != top_pair[:, None]), 3)
    hc = topk(pres, 5)

    NEG = np.int64(-1)
    c_sf = np.where(sf >= 0, 8*BASE + sf*B**4, NEG)
    c_q  = np.where(has4, 7*BASE + quad_rank*B**4 + qk*B**3, NEG)
    c_fh = np.where(fh_has, 6*BASE + top_trip*B**4 + fh_pair*B**3, NEG)
    c_fl = np.where(is_flush, 5*BASE + ftop[:,0]*B**4 + ftop[:,1]*B**3 + ftop[:,2]*B**2 + ftop[:,3]*B + ftop[:,4], NEG)
    c_st = np.where(straight_h >= 0, 4*BASE + straight_h*B**4, NEG)
    c_tr = np.where(n_trip >= 1, 3*BASE + top_trip*B**4 + tkick[:,0]*B**3 + tkick[:,1]*B**2, NEG)
    c_2p = np.where(n_pair >= 2, 2*BASE + p1*B**4 + p2*B**3 + tp_kick*B**2, NEG)
    c_1p = np.where(n_pair >= 1, 1*BASE + top_pair*B**4 + okick[:,0]*B**3 + okick[:,1]*B**2 + okick[:,2]*B, NEG)
    c_hc = hc[:,0]*B**4 + hc[:,1]*B**3 + hc[:,2]*B**2 + hc[:,3]*B + hc[:,4]

    score = c_hc
    for c in (c_1p, c_2p, c_tr, c_st, c_fl, c_fh, c_q, c_sf):
        score = np.maximum(score, c)
    return score

def equity(nameA, nameB, N, rng):
    ca = COMBOS[nameA]; cb = COMBOS[nameB]
    ia = rng.integers(len(ca), size=N); ib = rng.integers(len(cb), size=N)
    A = ca[ia]; Bc = cb[ib]
    for _ in range(40):
        conf = (A[:,0]==Bc[:,0])|(A[:,0]==Bc[:,1])|(A[:,1]==Bc[:,0])|(A[:,1]==Bc[:,1])
        if not conf.any(): break
        Bc[conf] = cb[rng.integers(len(cb), size=conf.sum())]
    used = np.concatenate([A, Bc], axis=1)              # (N,4)
    keys = rng.random((N, 52)); keys[np.arange(N)[:,None], used] = 2.0
    board = np.argsort(keys, axis=1)[:, :5]
    h7 = np.concatenate([A, board], axis=1)
    v7 = np.concatenate([Bc, board], axis=1)
    hs = evaluate(h7); vs = evaluate(v7)
    win = (hs > vs).sum(); tie = (hs == vs).sum()
    return (win + 0.5*tie) / N

def C(rch, sch):  # card from rank char + suit 0..3
    return RANKS.index(rch)*4 + sch

def unit_tests():
    """Deterministic 7-card category/order tests."""
    def sc(cs): return int(evaluate(np.array([cs], dtype=np.int64))[0])
    rf  = sc([C('A',0),C('K',0),C('Q',0),C('J',0),C('T',0),C('2',1),C('3',2)])  # royal flush
    sf  = sc([C('9',0),C('8',0),C('7',0),C('6',0),C('5',0),C('A',1),C('A',2)])  # 9-high str flush
    quad= sc([C('Q',0),C('Q',1),C('Q',2),C('Q',3),C('A',0),C('2',1),C('3',2)])  # quad Q + A
    fh  = sc([C('K',0),C('K',1),C('K',2),C('3',0),C('3',1),C('2',2),C('5',3)])  # KKK33
    fl  = sc([C('A',0),C('J',0),C('8',0),C('5',0),C('2',0),C('K',1),C('Q',2)])  # A-flush
    st  = sc([C('T',0),C('9',1),C('8',2),C('7',3),C('6',0),C('A',1),C('K',2)])  # T-high straight
    wheel = sc([C('A',0),C('2',1),C('3',2),C('4',3),C('5',0),C('K',1),C('Q',2)])# 5-high wheel
    trip= sc([C('7',0),C('7',1),C('7',2),C('K',0),C('Q',1),C('2',2),C('3',3)])  # set 7
    tp  = sc([C('A',0),C('A',1),C('K',0),C('K',1),C('5',2),C('2',3),C('3',0)])  # AA KK 5
    op  = sc([C('A',0),C('A',1),C('K',0),C('Q',1),C('J',2),C('2',3),C('3',0)])  # AA + KQJ
    hc  = sc([C('A',0),C('K',1),C('Q',2),C('J',3),C('9',0),C('2',1),C('3',2)])  # A-high
    order = [hc,op,tp,trip,wheel,st,fl,fh,quad,sf,rf]
    names = "highcard onepair twopair trips wheel straight flush fullhouse quads strFlush royal".split()
    ok = all(order[i] < order[i+1] for i in range(len(order)-1))
    print("=== evaluator unit tests ===")
    print("category order strictly increasing:", "OK" if ok else "FAIL")
    # wheel must beat two pair AAKK, lose to 6-high straight
    assert wheel > tp and wheel < st, "wheel ordering wrong"
    # AAKKQ two pair beats AA-pair-only
    assert tp > op, "two pair vs one pair wrong"
    return ok

def exact_equity(handA, handB):
    from itertools import combinations
    used = set(handA) | set(handB)
    deck = [c for c in range(52) if c not in used]
    boards = np.array(list(combinations(deck, 5)), dtype=np.int64)
    M = boards.shape[0]
    A = np.tile(np.array(handA, dtype=np.int64), (M,1))
    Bc = np.tile(np.array(handB, dtype=np.int64), (M,1))
    h7 = np.concatenate([A, boards], axis=1); v7 = np.concatenate([Bc, boards], axis=1)
    win = tie = 0
    for s in range(0, M, 200000):
        hs = evaluate(h7[s:s+200000]); vs = evaluate(v7[s:s+200000])
        win += int((hs > vs).sum()); tie += int((hs == vs).sum())
    return (win + 0.5*tie) / M

def sanity():
    rng = np.random.default_rng(7)
    if not unit_tests():
        return False
    tests = [("AA","KK",0.823),("AA","AKs",0.877),("AKs","QQ",0.463),("AKo","22",0.472),
             ("JTs","AKo",0.402),("QQ","AKo",0.564),("72o","AA",0.123)]
    print("=== MC equity vs known ===")
    ok = True
    for a,b,exp in tests:
        e = equity(a,b,60000,rng)
        flag = "OK" if abs(e-exp) < 0.012 else "CHECK"
        if flag=="CHECK": ok=False
        print(f"{a:>4} vs {b:<4} MC={e:.3f}  known~{exp:.3f}  {flag}")
    # ground-truth: exact full board enumeration for AKo vs QQ (specific suits)
    ex = exact_equity((C('A',0),C('K',1)), (C('Q',2),C('Q',3)))
    print(f"EXACT enum AKo vs QQ: QQ={1-ex:.4f} / AKo={ex:.4f}  (confirms MC, validates evaluator)")
    if not (0.42 < ex < 0.45): ok = False
    return ok

def build(N=4000, seed=12345):
    rng = np.random.default_rng(seed)
    E = np.full((169,169), 0.5, dtype=np.float64)
    tot = 169*168//2; done = 0
    for i in range(169):
        for j in range(i+1, 169):
            e = equity(CLASSES[i], CLASSES[j], N, rng)
            E[i,j] = e; E[j,i] = 1.0 - e
            done += 1
        if i % 20 == 0:
            print(f"  row {i}/169 ({done}/{tot} matchups)", flush=True)
    return E

if __name__ == "__main__":
    OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(OUT, exist_ok=True)
    if not sanity():
        print("SANITY FAILED — aborting", file=sys.stderr); sys.exit(1)
    print("=== building 169x169 equity matrix (N=4000/matchup) ===", flush=True)
    E = build()
    np.save(os.path.join(OUT,"equity.npy"), E)
    json.dump(CLASSES, open(os.path.join(OUT,"classes.json"),"w"))
    json.dump({n:[int(x) for x in COMBOS[n][0]] for n in CLASSES}, open(os.path.join(OUT,"_combo_sample.json"),"w"))
    print("SAVED equity.npy + classes.json; shape", E.shape)
