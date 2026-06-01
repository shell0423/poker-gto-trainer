#!/usr/bin/env python3
import json, os, sys

# Historical one-off: SRC was the original multi-agent workflow task-output JSON.
# Pass it via env var if you want to re-render; the output markdown is already in the repo.
SRC = os.environ.get("SRC", os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "_legacy_task_output.json"))
OUTDIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTDIR, exist_ok=True)

data = json.load(open(SRC))
res = data["result"]
charts = res["charts"]
consistency = res.get("consistency", "")

CAT_ORDER = [
    "Open-Raise (RFI)",
    "BB Defense vs RFI",
    "IP/SB vs RFI (3bet or flat)",
    "Facing 3bet (4bet / call / fold)",
]

LEGEND = """## 凡例 / Legend

| 記号 | 意味 |
|---|---|
| `R` | Open（オープンレイズ）100% |
| `3` | 3bet 100% |
| `4` | 4bet 100% |
| `C` | Call（フラット）100% |
| (空白) | Fold 100% |
| `R*` `3*` `4*` `C*` | **ミックス**（主アクションを表示／正確な内訳は表の下の **Mixed:** 行を参照） |

- グリッドは標準のハンドマトリクス（左上AA、右上方向=スーテッド、左下方向=オフスート、対角線=ペア）。
- 前提: **6-max / 100bb / キャッシュ / レーキ最小**。
- ⚠️ これは公開ソルバーチャートに整合させた **学習用の近似値** であり、GTO Wizard等の厳密なソルバー出力ではありません。
"""

def section(c):
    s = []
    s.append(f"### {c['title']}\n")
    s.append(f"**Range ≈ {c['rangePct']}** ｜ Sizing: {c['sizing']} ｜ 主アクション: {c['aggroLabel']}\n")
    s.append(c["markdown"])
    s.append("")
    s.append(f"> {c['notes']}")
    s.append("")
    return "\n".join(s)

# Build full document
doc = []
doc.append("# プリフロップ GTO 近似レンジ表（6-max / 100bb / キャッシュ）\n")
doc.append("自動生成（生成→敵対的検証→整合性チェックの多エージェント構成）。学習用近似。\n")
doc.append(LEGEND)
doc.append("\n---\n")

# TOC
doc.append("## 目次\n")
for cat in CAT_ORDER:
    doc.append(f"- **{cat}**")
    for c in charts:
        if c["cat"] == cat:
            doc.append(f"  - {c['title']} — {c['rangePct']}")
doc.append("")

for cat in CAT_ORDER:
    doc.append(f"\n---\n\n## {cat}\n")
    for c in charts:
        if c["cat"] == cat:
            doc.append(section(c))

if consistency:
    doc.append("\n---\n\n## 整合性チェック / 注意点\n")
    doc.append(consistency)

outpath = os.path.join(OUTDIR, "preflop-charts-6max-100bb.md")
open(outpath, "w").write("\n".join(doc))

print("WROTE:", outpath)
print("CHARTS:", len(charts))
print("=" * 60)
print("SUMMARY TABLE")
print("=" * 60)
for cat in CAT_ORDER:
    print(f"\n[{cat}]")
    for c in charts:
        if c["cat"] == cat:
            print(f"  - {c['title']:<34} {c['rangePct']:<28} ({c['sizing']})")

def dump(key):
    for c in charts:
        if c["key"] == key:
            print("\n" + "=" * 60)
            print("INLINE:", c["title"])
            print("=" * 60)
            print(f"Range {c['rangePct']} | Sizing {c['sizing']} | {c['aggroLabel']}\n")
            print(c["markdown"])
            print("\nNOTES:", c["notes"])
            return

dump("btn_v_sb3")
dump("btn_rfi")

print("\n" + "=" * 60)
print("CONSISTENCY")
print("=" * 60)
print(consistency)
