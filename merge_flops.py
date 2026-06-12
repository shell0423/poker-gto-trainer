#!/usr/bin/env python3
"""Merge solver shards + any prior srp_turn_full.json into srp_turn_full.json.
Carries forward already-solved flops (e.g. the earlier 200-flop run) so partial /
resumed runs accumulate. De-dups by flop string; re-indexes by flops_1755 order.
Safe to run anytime (e.g. to publish partial progress). Keeps the curated
38-flop srp_turn.json (browsable charts) untouched."""
import json, os, glob

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
out = os.path.join(D, "srp_turn_full.json")

flops = []
if os.path.exists(out):                                   # carry forward prior progress
    flops.extend(json.load(open(out))["flops"])
for p in sorted(glob.glob(os.path.join(D, "srp_turn_parts", "part_*.json"))):
    try:
        flops.extend(json.load(open(p))["flops"])
    except Exception as e:
        print("skip", p, e)

seen = {}
for r in flops:
    seen[r["flop"]] = r                                   # last write wins (parts override)

# re-index by canonical flops_1755 order for a tidy file
idx_of = {}
fp = os.path.join(D, "flops_1755.json")
if os.path.exists(fp):
    idx_of = {f["flop"]: i for i, f in enumerate(json.load(open(fp)))}
merged = sorted(seen.values(), key=lambda r: idx_of.get(r["flop"], r.get("idx", 0)))
for r in merged:
    r["idx"] = idx_of.get(r["flop"], r.get("idx", 0))

json.dump({"flops": merged}, open(out, "w"), ensure_ascii=False, separators=(",", ":"))
print(f"MERGED {len(merged)} flops -> data/srp_turn_full.json ({os.path.getsize(out)} bytes)")
if merged:
    cb = [r["cbet_overall"] for r in merged]
    print(f"c-bet overall: min {min(cb)}% / max {max(cb)}% / mean {sum(cb)/len(cb):.1f}%")
    total = len(idx_of) or len(merged)
    print(f"coverage: {len(merged)}/{total} flops ({len(merged)/total*100:.1f}%)")
