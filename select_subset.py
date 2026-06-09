#!/usr/bin/env python3
"""Pick ~200 diverse flops from the 1755 for a mid-size low-load solve.
Stratified by suit-pattern x pairedness so minority textures (monotone/paired)
are well represented; deterministic (fixed seed). -> data/flops_subset.json."""
import json, os, random
from collections import Counter, defaultdict

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
R = "23456789TJQKA"; SU = {'s': 0, 'h': 1, 'd': 2, 'c': 3}
allf = json.load(open(os.path.join(D, "flops_1755.json")))

def bucket(flop):
    cards = [(R.index(flop[i]), SU[flop[i+1]]) for i in range(0, 6, 2)]
    nsuit = len(set(s for r, s in cards))                      # 1 mono / 2 two-tone / 3 rainbow
    rc = Counter(r for r, s in cards)
    pair = 'trips' if 3 in rc.values() else ('pair' if 2 in rc.values() else 'unp')
    return (nsuit, pair)

groups = defaultdict(list)
for f in allf:
    groups[bucket(f["flop"])].append(f)

random.seed(42)
TARGET = 200
total = len(allf)
subset = []
for key, items in groups.items():
    random.shuffle(items)
    # proportional share, with a floor of 4 per non-trivial bucket
    share = max(4, round(TARGET * len(items) / total))
    subset.extend(items[:min(share, len(items))])
random.shuffle(subset)
subset = subset[:TARGET] if len(subset) > TARGET else subset

json.dump(subset, open(os.path.join(D, "flops_subset.json"), "w"), ensure_ascii=False)
print(f"WROTE data/flops_subset.json | {len(subset)} flops")
bc = Counter(bucket(f["flop"]) for f in subset)
sm = {1: 'mono', 2: 'two-tone', 3: 'rainbow'}
for k in sorted(bc): print(f"  {sm[k[0]]:9} {k[1]:5}: {bc[k]}")
