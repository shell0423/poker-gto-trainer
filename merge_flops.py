#!/usr/bin/env python3
"""Merge data/srp_turn_parts/part_*.json shards into data/srp_turn_full.json (sorted by idx).
Keeps the curated 38-flop data/srp_turn.json untouched (used for the browsable charts);
the full 1755-flop set goes to srp_turn_full.json (used by the quiz + flop lookup)."""
import json, os, glob

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
parts = sorted(glob.glob(os.path.join(D, "srp_turn_parts", "part_*.json")))
flops = []
for p in parts:
    flops.extend(json.load(open(p))["flops"])
# de-dup by flop string, sort by idx
seen = {}
for r in flops:
    seen[r["flop"]] = r
merged = sorted(seen.values(), key=lambda r: r.get("idx", 0))
out = os.path.join(D, "srp_turn_full.json")
json.dump({"flops": merged}, open(out, "w"), ensure_ascii=False, separators=(",", ":"))
print(f"MERGED {len(merged)} flops -> data/srp_turn_full.json ({os.path.getsize(out)} bytes)")
if merged:
    cb = [r["cbet_overall"] for r in merged]
    print(f"c-bet overall: min {min(cb)}% / max {max(cb)}% / mean {sum(cb)/len(cb):.1f}%")
