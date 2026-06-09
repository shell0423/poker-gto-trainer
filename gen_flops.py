#!/usr/bin/env python3
"""Generate all 1755 strategically-distinct flops (suit isomorphism), with auto labels.
Writes data/flops_1755.json = [{"flop":"As7d2c","label":"A72 レインボー"}, ...]."""
import json, os, itertools
from collections import Counter

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
R = "23456789TJQKA"; SUITS = "shdc"   # index 0=s,1=h,2=d,3=c (matches solve_srp_turn.cd)

def canon_key(cards):
    best = None
    for perm in itertools.permutations(range(4)):
        rel = tuple(sorted((r, perm[s]) for r, s in cards))
        if best is None or rel < best: best = rel
    return best

def label(cards):
    rs = sorted((r for r, s in cards), reverse=True)
    chars = ''.join(R[r] for r in rs)
    sw = {1: 'モノトーン', 2: '二色', 3: 'レインボー'}[len(set(s for r, s in cards))]
    rc = Counter(r for r, s in cards)
    pw = '・トリップス' if 3 in rc.values() else ('・ペア' if 2 in rc.values() else '')
    conn = '・連結' if (not pw and (max(rs) - min(rs)) <= 4) else ''
    return f"{chars} {sw}{pw}{conn}"

seen = set(); out = []
allc = [(r, s) for r in range(13) for s in range(4)]
for combo in itertools.combinations(allc, 3):
    k = canon_key(list(combo))
    if k in seen: continue
    seen.add(k)
    cs = ''.join(R[r] + SUITS[s] for r, s in combo)
    rs = sorted((r for r, s in combo), reverse=True)
    paired = 1 if (2 in Counter(r for r, s in combo).values() or 3 in Counter(r for r, s in combo).values()) else 0
    out.append({"flop": cs, "label": label(combo), "_sort": (-paired, [-x for x in rs])})

out.sort(key=lambda x: (x["_sort"][0], tuple(x["_sort"][1])))
for o in out: del o["_sort"]
json.dump(out, open(os.path.join(D, "flops_1755.json"), "w"), ensure_ascii=False)
print(f"WROTE data/flops_1755.json | {len(out)} flops")
print("samples:", [o["flop"] + ' ' + o["label"] for o in out[:3]], "...", [o["flop"] for o in out[-3:]])
