#!/usr/bin/env python3
"""Build a self-contained GTO-Wizard-style preflop chart viewer + quiz trainer.
Reads all chart sources, normalizes, embeds JSON inline, writes index.html."""
import json, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

# Persistent data sources (self-contained — no /private/tmp dependency).
SRC_100 = os.path.join(DATA, "charts_100bb.json")     # 6-max 100bb cash (20)
SRC_EXTRA = os.path.join(DATA, "charts_extra.json")   # full-ring / MTT / 50bb (17)
SRC_PUSHFOLD = os.path.join(DATA, "pushfold_nash.json")       # HU push/fold Nash (16)
SRC_MULTIWAY = os.path.join(DATA, "pushfold_multiway.json")   # 6-max first-in jam Nash (60)
SRC_EDGE = os.path.join(DATA, "pushfold_edge.json")           # EDGE push/fold +1bb ante
SRC_EDGE_EARLY = os.path.join(DATA, "charts_edge_early.json") # EDGE 4-max 40bb +ante ranges

charts = []
# 1) 6-max 100bb cash
for c in json.load(open(SRC_100)):
    c = dict(c); c.setdefault("config", "6-max 100bb cash")
    charts.append(c)
# 2) EDGE POKER (matched to the app: +1bb ante; early 4-max + final-table push/fold)
if os.path.exists(SRC_EDGE_EARLY):
    charts += json.load(open(SRC_EDGE_EARLY))
if os.path.exists(SRC_EDGE):
    charts += json.load(open(SRC_EDGE))["charts"]
# 3) generic push/fold Nash (exact)
if os.path.exists(SRC_PUSHFOLD):
    charts += json.load(open(SRC_PUSHFOLD))["charts"]
if os.path.exists(SRC_MULTIWAY):
    charts += json.load(open(SRC_MULTIWAY))["charts"]
# 4) extra configs (full-ring / MTT / 50bb)
if os.path.exists(SRC_EXTRA):
    charts += json.load(open(SRC_EXTRA))
# 5) BTN vs BB SRP flop GTO (self-built vector-CFR solver: 2 sizes + check-raise)
SRC_SRP = os.path.join(DATA, "srp_flop.json")
SRP_CAVEAT = ("自前vector-CFR（cベットを小33%/大75%の2サイズ＋BBチェックレイズまで）。"
              "ターン/リバーをエクイティで評価する単一ベットラウンドの厳密Nashのため、"
              "**cベット頻度は実戦GTOより控えめ**に出ます（ターンの追撃価値を含まないため）。"
              "手の強さ・盤面差・守備の相対傾向の学習用。真の多ストリート解はロードマップ参照。")
DETAIL_CFG = "BTN vs BB SRP・詳細(サイズ/CR)"
if os.path.exists(SRC_SRP):
    for f in json.load(open(SRC_SRP))["flops"]:
        cat = f"{f['flop']} — {f['label']}"
        charts.append({
            "config": DETAIL_CFG, "cat": cat,
            "title": f"{f['flop']} BTN ベット/チェック", "sizing": "小33% / 大75%",
            "rangePct": f"bet {f['cbet_overall']}%（控えめ）", "aggroLabel": "大ベット", "exact": False,
            "notes": f"BTN vs BB SRP フロップ {f['flop']}（{f['label']}）。赤=大ベット(75%) / 緑=小ベット(33%) / 青=チェック。{SRP_CAVEAT}",
            "hands": [{"hand": k, "aggroPct": f["cbet_big"].get(k, 0), "callPct": f["cbet_small"].get(k, 0),
                       "foldPct": 100 - f["cbet_big"].get(k, 0) - f["cbet_small"].get(k, 0)} for k in f["cbet"]],
        })
        charts.append({
            "config": DETAIL_CFG, "cat": cat,
            "title": f"{f['flop']} BB vs c-bet", "sizing": "vs c-bet",
            "rangePct": f"call {f['call_overall']}% / raise {f['raise_overall']}%", "aggroLabel": "レイズ", "exact": False,
            "notes": f"BB が BTN の c ベットに対して フォールド/コール/チェックレイズ（フロップ {f['flop']}）。赤=チェックレイズ / 緑=コール / 青=フォールド。ウェットな盤ほど守備が広い。{SRP_CAVEAT}",
            "hands": [{"hand": k, "aggroPct": f["bb_raise"].get(k, 0), "callPct": f["bb_call"].get(k, 0),
                       "foldPct": 100 - f["bb_raise"].get(k, 0) - f["bb_call"].get(k, 0)} for k in f["bb_call"]],
        })

# 5b) BTN vs BB SRP — TWO-STREET solve (flop+turn, river=equity): REALISTIC c-bet frequency
SRC_SRP2 = os.path.join(DATA, "srp_turn.json")
REAL_CFG = "BTN vs BB SRP・実戦(2-street)"
SRP2_NOTE = ("2ストリート解（フロップ＋ターンを解き、リバーはエクイティで評価）。"
             "ターンの追撃（バレル）価値が入るため、**cベット頻度が実戦GTOに近い水準**で出ます。"
             "ベットは2/3ポット1サイズ、ターンのドンク/チェックレイズは簡略化。")
if os.path.exists(SRC_SRP2):
    for f in json.load(open(SRC_SRP2))["flops"]:
        cat = f"{f['flop']} — {f['label']}"
        charts.append({
            "config": REAL_CFG, "cat": cat,
            "title": f"{f['flop']} BTN c-bet（実戦）", "sizing": "2/3 pot",
            "rangePct": f"c-bet {f['cbet_overall']}%", "aggroLabel": "Cbet", "exact": False,
            "notes": f"BTN vs BB SRP フロップ {f['flop']}（{f['label']}）。赤=cベット / 青=チェック。{SRP2_NOTE}",
            "hands": [{"hand": k, "aggroPct": v, "callPct": 0, "foldPct": 100 - v} for k, v in f["cbet"].items()],
        })
        charts.append({
            "config": REAL_CFG, "cat": cat,
            "title": f"{f['flop']} BB vs c-bet（実戦）", "sizing": "vs 2/3 pot",
            "rangePct": f"call {f['call_overall']}%", "aggroLabel": "Call", "exact": False,
            "notes": f"BB が BTN の c ベットに コール/フォールド（フロップ {f['flop']}）。緑=コール / 青=フォールド。{SRP2_NOTE}",
            "hands": [{"hand": k, "aggroPct": 0, "callPct": v, "foldPct": 100 - v} for k, v in f["bb_call"].items()],
        })

# normalize: hands -> {name:[a,c,f]}
norm = []
for c in charts:
    hd = {}
    for h in c.get("hands", []):
        a = float(h.get("aggroPct", 0) or 0); cc = float(h.get("callPct", 0) or 0)
        f = h.get("foldPct", None)
        f = float(f) if f is not None else max(0.0, 100 - a - cc)
        s = a + cc + f
        if s <= 0: continue
        hd[h["hand"]] = [round(a/s*100), round(cc/s*100), round(f/s*100)]
    norm.append({
        "config": c.get("config", "?"), "cat": c.get("cat", ""), "title": c.get("title", ""),
        "sizing": c.get("sizing", ""), "rangePct": c.get("rangePct", ""),
        "aggroLabel": c.get("aggroLabel", "Raise"), "exact": bool(c.get("exact", False)),
        "notes": c.get("notes", ""), "hands": hd,
        "ev": c.get("ev"), "evFold": c.get("evFold"), "evUnit": c.get("evUnit", "bb"),
    })

print(f"charts: {len(norm)}  configs: {sorted(set(c['config'] for c in norm))}")

PAYLOAD = json.dumps(norm, ensure_ascii=False, separators=(",", ":"))

# glossary (optional — generated by workflow, persisted to data/glossary.json)
SRC_GLOSSARY = os.path.join(DATA, "glossary.json")
glossary = []
if os.path.exists(SRC_GLOSSARY):
    g = json.load(open(SRC_GLOSSARY))
    glossary = g.get("cats", g) if isinstance(g, dict) else g
print(f"glossary categories: {len(glossary)}  terms: {sum(len(c.get('terms', [])) for c in glossary)}")
GLOSSARY = json.dumps(glossary, ensure_ascii=False, separators=(",", ":"))

# SRP solver data embedded raw for the postflop strategy quiz
_srp_path = os.path.join(DATA, "srp_flop.json")
_srp_data = json.load(open(_srp_path)) if os.path.exists(_srp_path) else {"flops": []}
SRP_JSON = json.dumps(_srp_data, ensure_ascii=False, separators=(",", ":"))
_srp2_path = os.path.join(DATA, "srp_turn.json")   # 2-street (realistic c-bet)
_srp2_data = json.load(open(_srp2_path)) if os.path.exists(_srp2_path) else {"flops": []}
SRP2_JSON = json.dumps(_srp2_data, ensure_ascii=False, separators=(",", ":"))
print(f"SRP quiz flops: {len(_srp_data.get('flops', []))}  (2-street: {len(_srp2_data.get('flops', []))})")

HTML = """<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GTO Preflop Trainer</title>
<style>
:root{--ag:#d64545;--ca:#3f9d58;--fo:#4a78b5;--bg:#0f1620;--pan:#1a2533;--ink:#e8eef5;--mut:#8aa0b5;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Hiragino Kaku Gothic ProN",Meiryo,sans-serif}
header{padding:12px 18px;background:#13202e;border-bottom:1px solid #243443;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
header h1{font-size:16px;margin:0 14px 0 0;font-weight:700}
select,button{background:#22303f;color:var(--ink);border:1px solid #33475a;border-radius:7px;padding:7px 10px;font-size:13px;cursor:pointer}
button.tab{background:#1b2735}button.tab.on{background:var(--ag);border-color:var(--ag);color:#fff;font-weight:700}
.wrap{display:flex;flex-wrap:wrap;gap:18px;padding:18px;align-items:flex-start}
.gridwrap{flex:0 0 auto}
.grid{display:grid;grid-template-columns:repeat(13,minmax(30px,42px));gap:2px}
.cell{position:relative;aspect-ratio:1;border-radius:4px;overflow:hidden;cursor:pointer;border:1px solid #0c1219}
.cell .lab{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;text-shadow:0 1px 2px rgba(0,0,0,.85);z-index:2}
.cell .pc{position:absolute;left:0;right:0;bottom:1px;text-align:center;font-size:8px;opacity:.9;z-index:2;text-shadow:0 1px 2px #000}
.cell.dim{opacity:.28}
.panel{flex:1;min-width:280px;max-width:520px;background:var(--pan);border:1px solid #243443;border-radius:12px;padding:16px}
.panel h2{margin:0 0 6px;font-size:16px}
.meta{color:var(--mut);font-size:12px;margin-bottom:10px}
.legend{display:flex;gap:14px;margin:10px 0;flex-wrap:wrap;font-size:12px}
.legend i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.notes{font-size:12.5px;color:#cdd9e6;background:#13202e;border-radius:8px;padding:10px 12px;margin-top:8px;white-space:pre-wrap}
.detail{margin-top:10px;font-size:13px;min-height:20px}
.why{margin-top:10px;padding:10px 12px;background:#13202e;border-left:3px solid var(--ca);border-radius:6px;font-size:12.5px;line-height:1.65}
.why b{color:#9fe2b6}
.why .role{color:var(--mut);font-size:12px;margin:4px 0 6px}
.why details{margin-top:8px}
.why summary{cursor:pointer;color:#7fb0e0;font-size:11.5px}
.bar{height:14px;border-radius:4px;display:flex;overflow:hidden;margin:4px 0 8px}
.bar span{display:block}
.tag{display:inline-block;font-size:10px;padding:1px 7px;border-radius:10px;background:#234;color:#9fd;margin-left:6px}
.tag.exact{background:#143d27;color:#7ee29f}
/* quiz */
#quiz{display:none}
#quiz.on{display:flex}
#qchart{max-width:470px}
#qchart h3{margin:0 0 6px;font-size:15px}
#qcGrid{grid-template-columns:repeat(13,minmax(20px,30px))}
#qcGrid .lab{font-size:9px}
#qcGrid .pc{display:none}
.qhand{font-size:34px;font-weight:800;letter-spacing:1px;margin:6px 0}
.qspot{color:var(--mut);font-size:13px}
.qbtns{display:flex;gap:10px;margin:14px 0}
.qbtns button{flex:1;padding:14px;font-size:15px;font-weight:700}
.qres{font-size:13px;margin-top:10px;min-height:40px}
.score{font-size:13px;color:var(--mut)}
kbd{background:#26384a;border-radius:4px;padding:1px 6px;border:1px solid #3a5066;font-size:11px}
/* glossary */
#gloss{display:none;padding:18px}
#gloss.on{display:block}
.gsearchbar{margin-bottom:16px}
.gsearchbar input{width:100%;max-width:440px;padding:10px 13px;font-size:14px;background:#22303f;border:1px solid #33475a;border-radius:8px;color:var(--ink)}
.gcat{margin-bottom:24px}
.gcat h3{font-size:15px;margin:0 0 10px;color:#cfe0f0;border-bottom:1px solid #243443;padding-bottom:6px}
.gcat h3 span{color:var(--mut);font-size:12px;font-weight:400;margin-left:6px}
.gcards{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:10px}
.gterm{background:var(--pan);border:1px solid #243443;border-radius:10px;padding:12px 14px}
.gterm.flash{outline:2px solid var(--ca)}
.gt-h b{font-size:14px}
.gt-r{color:var(--mut);font-size:12px;margin-left:8px}
.gt-s{font-size:12.5px;margin-top:5px;color:#dbe6f0}
.gt-l{font-size:12px;margin-top:6px;color:var(--mut);line-height:1.6}
.gt-rel{margin-top:8px;font-size:11px;color:var(--mut)}
.chip{display:inline-block;background:#22303f;border:1px solid #33475a;border-radius:10px;padding:1px 8px;margin:2px 3px 0 0;font-size:11px}
.chip.lk{cursor:pointer;color:#7fb0e0;border-color:#3a5a78}
.chip.lk:hover{background:#2a3e52}
.gmut{color:var(--mut)}
/* interlinks + term quiz */
.gl{border-bottom:1px dotted #6fa8dc;cursor:help;color:#bcd9f5}
.gl:hover{background:#1d3147}
.gl-go{display:inline-block;margin-top:9px;font-size:11px;padding:4px 9px;background:#1d3a2a;border-color:#2f6b46;color:#8fe0ab}
.qmode{display:flex;gap:8px;margin-bottom:12px}
.qm{background:#1b2735}
.qm.on{background:var(--ag);border-color:var(--ag);color:#fff;font-weight:700}
.tdef .defbox{background:#13202e;border-radius:8px;padding:12px 14px;font-size:14px;margin:6px 0 12px;line-height:1.7}
.tdef .mut2{color:var(--mut);font-size:12.5px}
.tchoices{flex-direction:column}
.tchoices button{text-align:left}
.evrow{margin-top:8px;font-size:12.5px;background:#10242f;border-radius:6px;padding:7px 10px}
.qctl{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:12px;font-size:12px;color:var(--mut)}
.qctl select{padding:5px 8px;font-size:12px}
.qmini{font-size:11px;padding:5px 9px;background:#1b2735}
.qmini.on{background:var(--ca);border-color:var(--ca);color:#08120b;font-weight:700}
/* poker-table view (strategy quiz) */
.ptable{position:relative;width:100%;max-width:560px;aspect-ratio:16/10;margin:8px auto 4px;border-radius:48%/46%;
  background:radial-gradient(ellipse at center,#1f6b46 0%,#155236 68%,#0e3b27 100%);
  border:6px solid #2a1c12;box-shadow:inset 0 0 28px rgba(0,0,0,.55)}
.seat{position:absolute;transform:translate(-50%,-50%);width:72px;text-align:center;font-size:11px;z-index:2}
.seat .pos{font-weight:700;color:#e6eef6;background:#1a2533;border:1px solid #33475a;border-radius:6px;padding:1px 3px;display:inline-block;min-width:40px}
.seat.hero .pos{background:var(--ag);border-color:var(--ag);color:#fff}
.seat.fold{opacity:.42}
.seat .act{margin-top:3px;font-size:10px;font-weight:800;border-radius:8px;padding:1px 6px;display:inline-block;letter-spacing:.5px}
.act.f{background:#33475a;color:#9fb2c4}
.act.r{background:#d6a23a;color:#241a06}
.act.t{background:#d6643a;color:#fff}
.act.c{background:#3f9d58;color:#06140b}
.act.b{background:#4a78b5;color:#fff}
.act.w{background:#1c2a36;color:#6b7d8f}
.seat .cards{display:flex;gap:3px;justify-content:center;margin-top:3px}
.seat .stack{margin-top:3px;font-size:10px;font-weight:700;color:#ffe8b0;background:rgba(0,0,0,.45);border-radius:9px;padding:0 7px;display:inline-block}
.seat.hero .stack{color:#fff;background:rgba(214,69,69,.5)}
.card{width:24px;height:34px;border-radius:3px;background:#fafafa;color:#15171a;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:800;font-size:13px;line-height:1.05;box-shadow:0 1px 3px rgba(0,0,0,.55)}
.card.red{color:#cc1133}
.card span{font-size:12px}
.board{position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);display:flex;gap:4px}
.board .slot{width:24px;height:34px;border-radius:3px;border:1px dashed rgba(255,255,255,.28);background:rgba(255,255,255,.04)}
.pot{position:absolute;left:50%;top:62%;transform:translate(-50%,-50%);font-size:11px;color:#ffe;background:rgba(0,0,0,.4);padding:2px 12px;border-radius:10px}
/* equity calculator */
#calc{display:none;padding:18px;max-width:600px}
#calc.on{display:block}
.calc-board{display:flex;gap:8px;margin:12px 0 20px}
.cslot{width:56px;height:78px;border-radius:9px;border:2px dashed #33475a;background:#13202e;cursor:pointer;overflow:hidden}
.cslot.filled{border-style:solid;border-color:#33475a}
.ccard{width:100%;height:100%;background:#f3f6fa;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:800}
.ccard .rk{font-size:24px;line-height:1}
.ccard .st{font-size:22px;line-height:1}
.calc-players-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.calc-players-head h3{margin:0;font-size:16px}
.prow{display:flex;align-items:center;gap:12px;background:var(--pan);border:1px solid #243443;border-radius:12px;padding:10px 12px;margin-bottom:10px}
.prow .ph{display:flex;gap:5px;flex:0 0 auto}
.pslot{width:40px;height:56px;border-radius:7px;border:2px dashed #33475a;background:#13202e;cursor:pointer;overflow:hidden}
.pslot.filled{border-style:solid}
.pslot .ccard .rk{font-size:17px}.pslot .ccard .st{font-size:16px}
.prow .eq{font-size:28px;font-weight:800}
.prow .eq small{font-size:13px;color:var(--mut);font-weight:600}
.prow .cats{font-size:11px;color:var(--mut);margin-top:2px}
.prow .rm{background:#33475a;border:none;color:#cdd9e6;border-radius:6px;cursor:pointer;padding:4px 9px;font-size:12px}
#picker{position:fixed;inset:0;background:rgba(0,0,0,.65);display:none;align-items:center;justify-content:center;z-index:50}
#picker.on{display:flex}
.pickbox{background:#1a2533;border:1px solid #33475a;border-radius:12px;padding:14px}
.pickbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;gap:10px}
.pickgrid{display:grid;grid-template-columns:repeat(13,1fr);gap:3px}
.pcard{width:30px;height:40px;border-radius:4px;background:#f3f6fa;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;cursor:pointer}
.pcard.used{opacity:.22;pointer-events:none}
#rangeed,#details{position:fixed;inset:0;background:rgba(0,0,0,.65);display:none;align-items:center;justify-content:center;z-index:50}
#rangeed.on,#details.on{display:flex}
.rgrid{display:grid;grid-template-columns:repeat(13,26px);gap:2px}
.rcell{height:26px;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;border-radius:3px;background:#22303f;border:1px solid #2c3e50;cursor:pointer;color:#9fb2c4}
.rcell.ron{background:var(--ca);color:#06140b;border-color:var(--ca)}
#detbox{min-width:280px}
#howto{display:none;padding:18px;max-width:680px;line-height:1.75}
#howto.on{display:block}
#howto h2{margin:0 0 8px}
#howto h3{margin:18px 0 6px;font-size:15px;color:#cfe0f0;border-bottom:1px solid #243443;padding-bottom:4px}
#howto p{margin:6px 0;font-size:13.5px;color:#dbe6f0}
#howto ul,#howto ol{margin:6px 0;padding-left:20px;font-size:13px;color:#cdd9e6}
#howto li{margin:3px 0}
#howto .tip{background:var(--pan);border:1px solid #243443;border-radius:10px;padding:10px 14px;margin:10px 0}
/* postflop quiz */
#pQuiz .pq-board{background:radial-gradient(ellipse at center,#1f6b46,#0e3b27);border:4px solid #2a1c12;border-radius:14px;padding:14px;margin:8px 0;text-align:center}
#pQuiz .pq-board .pq-lbl{color:#cfe9d8;display:block;margin-bottom:6px}
.pqc{display:inline-block;min-width:28px;padding:4px 6px;margin:2px;background:#f3f6fa;border-radius:5px;font-weight:800;font-size:17px;box-shadow:0 1px 3px rgba(0,0,0,.5)}
.pq-lbl{font-size:11px;color:var(--mut)}
#pQuiz .pq-hands{margin:12px 0;font-size:13px}
#pQuiz .pq-q{font-size:15px;font-weight:700;margin:14px 0 6px}
</style></head><body>
<header>
  <h1>♠ GTO Preflop Trainer</h1>
  <label>構成 <select id="cfg"></select></label>
  <label>スポット <select id="spot"></select></label>
  <button class="tab on" id="tabChart">チャート</button>
  <button class="tab" id="tabQuiz">クイズ</button>
  <button class="tab" id="tabGloss">用語集</button>
  <button class="tab" id="tabCalc">計算機</button>
  <button class="tab" id="tabHowto">使い方</button>
  <span class="score" id="score"></span>
</header>

<div class="wrap" id="chartView">
  <div class="gridwrap"><div class="grid" id="grid"></div>
    <div class="legend" id="legend"></div>
  </div>
  <div class="panel">
    <h2 id="ttl">—</h2>
    <div class="meta" id="meta"></div>
    <div class="detail" id="detail">マスにマウスを乗せる/クリックで内訳。</div>
    <div class="notes" id="notes"></div>
  </div>
</div>

<div class="wrap" id="quiz">
  <div style="flex:1;max-width:640px">
    <div class="qmode">
      <button class="qm on" id="qmStrat">戦略クイズ</button>
      <button class="qm" id="qmTerm">用語クイズ</button>
      <button class="qm" id="qmPost">ポストフロップ</button>
      <button class="qm" id="qmSrp">SRP戦略</button>
    </div>
    <div class="panel" id="sQuiz">
      <div class="qctl">
        出題範囲 <select id="qscope"><option value="edge">EDGE POKER（推奨）</option><option value="cfg">この構成のみ</option><option value="all">全構成</option></select>
        スタック <select id="qstack"><option value="all">全部</option><option value="le10">≤10bb</option><option value="11-20">11-20bb</option><option value="21-50">21-50bb</option><option value="deep">50bb+</option></select>
        <button class="qmini" id="qreview">復習モード (<span id="missN">0</span>)</button>
        <button class="qmini" id="qclear">履歴クリア</button>
        <button class="qmini" id="qChartBtn">📊 チャート</button>
      </div>
      <div class="qspot" id="qspot"></div>
      <div class="ptable" id="ptable"></div>
      <div class="qbtns" id="qbtns"></div>
      <div class="qres" id="qres"></div>
      <button id="qnext">次の問題 ▶ <kbd>Enter</kbd></button>
      <div class="legend" id="qlegend" style="margin-top:14px"></div>
    </div>
    <div class="panel" id="tQuiz" style="display:none">
      <div class="qspot" id="tprompt"></div>
      <div class="tdef" id="tdef"></div>
      <div class="qbtns tchoices" id="tbtns"></div>
      <div class="qres" id="tres"></div>
      <button id="tnext">次の問題 ▶ <kbd>Enter</kbd></button>
    </div>
    <div class="panel" id="pQuiz" style="display:none">
      <div id="pQuizBody"></div>
      <button id="pqnext">次の問題 ▶ <kbd>Enter</kbd></button>
    </div>
    <div class="panel" id="srpQuiz" style="display:none">
      <div id="srpQuizBody"></div>
      <button id="srpnext">次の問題 ▶ <kbd>Enter</kbd></button>
    </div>
  </div>
  <div class="panel" id="qchart" style="display:none">
    <h3 id="qcTtl"></h3>
    <div class="meta" id="qcMeta"></div>
    <div class="grid" id="qcGrid"></div>
    <div class="legend" id="qcLeg"></div>
    <div class="detail" id="qcDetail" style="margin-top:8px"></div>
  </div>
</div>

<div id="gloss">
  <div class="gsearchbar"><input id="gsearch" placeholder="用語を検索（英語・カナ・日本語）…" autocomplete="off"></div>
  <div id="glist"></div>
</div>

<div id="calc">
  <h2 style="margin:0 0 2px">Calculation <span style="font-size:12px;color:var(--mut);font-weight:400">エクイティ計算機</span></h2>
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px"><span style="font-size:12px;color:var(--mut)">ボード（コミュニティカード）</span><button class="qmini" id="clearBoard">ボード消去</button></div>
  <div class="calc-board" id="cboard"></div>
  <div class="calc-players-head"><h3>Player Hands</h3><div style="display:flex;gap:6px;flex-wrap:wrap"><button class="qmini" id="catLang">EN</button><button class="qmini" id="randomDeal">🎲 ランダム</button><button class="qmini" id="calcReset">キャンセル</button><button class="qmini" id="addPlayer">＋ 追加</button></div></div>
  <div id="players"></div>
  <div style="font-size:11px;color:var(--mut);margin-top:12px;line-height:1.6">カードをタップ→選択。2人以上のハンドが揃うと<b>勝率（エクイティ）</b>を自動計算します。フロップ以降は厳密計算、プリフロップ等の重い局面はモンテカルロ近似（〜近似 と表示）。「キャンセル」で全消去。</div>
</div>
<div id="howto">
  <h2>使い方ガイド <span style="font-size:12px;color:var(--mut);font-weight:400">— はじめての方へ</span></h2>
  <p>このアプリは、ポーカー（テキサスホールデム）の<b>プリフロップ（最初の2枚での判断）</b>を、色分けチャート・クイズ・計算機で学ぶツールです。インストール不要、スマホでもOK。</p>
  <div class="tip">💡 <b>いちばんの近道</b>：上の「<b>クイズ</b>」タブを開いて10問ほど解き、回答後に出る<b>理由</b>を読むこと。間違えた手は「復習モード」で繰り返せます。</div>
  <h3>最低限の言葉</h3>
  <ul>
    <li><b>bb（ビッグブラインド）</b>＝賭けの単位。スタック「10bb」＝ブラインド10回分の持ちチップ（本アプリでは <b>1bb＝100チップ</b>で併記）。</li>
    <li><b>ポジション</b>＝席（UTG/CO/BTN/SB/BBなど）。後に行動できる席ほど有利。</li>
    <li><b>レンジ</b>＝「その状況で打つ手の範囲」。<b>GTO</b>＝理論上いちばん損しない打ち方。</li>
    <li>分からない言葉は「<b>用語集</b>」タブで検索できます（257語）。</li>
  </ul>
  <h3>① チャート タブ — 「どの手をどう打つか」の早見表</h3>
  <ul>
    <li>13×13のマス＝169通りの手。色＝🔴攻める（Open/3bet/4bet/Jam）・🟢コール・🔵フォールド。</li>
    <li>マスが2色に割れている＝<b>ミックス</b>（その手は◯%で攻め、◯%で降りるのが正解）。</li>
    <li>マスにマウス/タップで<b>頻度・EV・理由</b>を表示。</li>
  </ul>
  <h3>▸ 「構成」と「スポット」の選び方（上のメニュー）</h3>
  <ul>
    <li><b>構成</b>＝ゲームの種類とスタックの深さ。例：<b>6-max 100bb cash</b>（6人・100bb）、<b>EDGE Push/Fold</b>（EDGE実戦の短スタック）、<b>First-in Push/Fold</b>、<b>50bb / フルリング / MTT</b> など。まず「どんな状況か」をここで選ぶ。</li>
    <li><b>スポット</b>＝その中の具体的な局面。例：<b>UTG RFI</b>（UTGで最初に開くか）、<b>BTN vs SB 3bet</b>、<b>4-max BTN Jam — 10bb</b>（4-maxのBTNで10bbをジャムするか）。ポジション・相手の行動・スタックがここで決まる。</li>
    <li><b>スポット名の読み方</b>：「自分のポジション＋状況」。<b>RFI</b>＝最初に自分が開く／<b>vs ○○</b>＝相手の○○に対して／<b>Jam — Xbb</b>＝Xbbをオールインするか。</li>
    <li><b>ポストフロップGTO（BTN vs BB SRP、38フロップ）</b>：自前のvector-CFRソルバーで計算。2つの構成があります。
      <ul style="margin:4px 0">
        <li><b>「BTN vs BB SRP・実戦(2-street)」</b>＝<b>フロップ＋ターンを解いた実戦的なc-bet頻度</b>（赤=ベット/青=チェック）と BB守備（緑=コール/青=フォールド）。<b>まずこちらを見てください</b>。</li>
        <li><b>「BTN vs BB SRP・詳細(サイズ/CR)」</b>＝ベットのサイズ選択（赤=大75%/緑=小33%/青=チェック）と BBの<b>チェックレイズ</b>（赤=CR/緑=コール/青=フォールド）。<span style="color:#9fb3c6;font-size:12px">※こちらはc-bet頻度が控えめに出ます（サイズ/CRの傾向を見る用）。</span></li>
      </ul>
      ウェットな盤ほどBBが広く守り、チェックレイズも増えます。</li>
  </ul>
  <h3>▸ よく出るアクション用語</h3>
  <ul>
    <li><b>jam（ジャム）</b>＝<b>オールイン</b>（持ちチップを全部賭ける）。<b>push / shove</b> も同じ意味。スタックが短いとき「中途半端に上げず全部賭けて、相手に〈降りる or コール〉を迫る」打ち方。</li>
    <li><b>RFI</b>＝誰もまだ上げていない場面で、自分が<b>最初にレイズして参加</b>すること（＝オープン）。</li>
    <li><b>open（オープン）</b>＝最初のレイズ。<b>3bet</b>＝その上げ返し、<b>4bet</b>＝さらに上げ返し。</li>
    <li><b>call</b>＝同額を出してついていく／<b>fold</b>＝降りる／<b>raise</b>＝上げる。</li>
    <li>他の言葉は「<b>用語集</b>」タブで検索できます（257語）。</li>
  </ul>
  <h3>② クイズ タブ — 「あなたならどうする？」</h3>
  <ul>
    <li>ポーカーテーブルに各プレイヤーの行動（FOLD/RAISE/JAM…）・<b>スタック（bbとチップ）</b>・<b>ポット</b>、自分の席に手札を表示。</li>
    <li>下のボタンで回答 → 正解の頻度・EV・理由が出ます。</li>
    <li>「<b>出題範囲</b>」でEDGE/全構成、「<b>スタック</b>」で深さ（≤10bb等）を絞れます。</li>
    <li>「<b>📊チャート</b>」で答えの表、「<b>用語クイズ</b>」で言葉も練習。</li>
    <li><b>ポストフロップ</b>＝フロップ以降の役・勝率・アウツ・ポットオッズを当てる練習（全て厳密計算）。</li>
    <li><b>SRP戦略</b>＝BTN vs BBのフロップで、自分のハンドの<b>GTOアクション</b>（BTN: ベット/チェック、BB: フォールド/コール/チェックレイズ）を当てる練習。混合戦略なので、<b>GTOが使う行動ならどれも正解</b>として頻度を表示します。</li>
  </ul>
  <h3>③ 計算機 タブ — 勝率（エクイティ）計算</h3>
  <ul>
    <li>ボードと各プレイヤーの<b>ハンド or レンジ</b>を入れると、勝率を自動計算（Equilab相当）。</li>
    <li>「詳細」で<b>役の確率内訳</b>と<b>アウツ</b>（次の1枚で逆転するカード）も見られます。</li>
  </ul>
  <h3>🏆 EDGE POKERで勝ちたい人へ</h3>
  <p>EDGEは<b>4-max・超短スタックの速い構造</b>。勝敗の大半は<b>短スタックの jam/call</b>で決まります。クイズの出題範囲を「<b>EDGE POKER</b>」にして、jam/callを体に入れるのが最短です。</p>
  <h3>👣 最初の一歩</h3>
  <ol>
    <li>「クイズ」タブを開く（最初からEDGE出題）。</li>
    <li>10問解いて、回答後の「理由」を読む。</li>
    <li>間違えた手は「チャート」タブで色を確認。</li>
    <li>分からない言葉は「用語集」で引く。</li>
  </ol>
  <div class="tip" style="font-size:12px;color:var(--mut)">※「近似」表示のレンジは公開ソルバー整合の学習用。「厳密Nash」表示（プッシュ/フォールド）と計算機のエクイティは自前計算の本物です。</div>
</div>
<div id="picker"><div class="pickbox" id="pickbox"></div></div>
<div id="rangeed"><div class="pickbox" id="rangeedbox"></div></div>
<div id="details"><div class="pickbox" id="detbox"></div></div>

<script>
const DATA = __PAYLOAD__;
const GLOSSARY = __GLOSSARY__;   // defined early: used by the term-quiz (ALLTERMS) before the glossary section
const SRP = __SRP__;             // single-street SRP (sizing + check-raise) — for BB defense quiz
const SRP2 = __SRP2__;           // two-street SRP (realistic c-bet) — for BTN bet quiz
const RANKS=['A','K','Q','J','T','9','8','7','6','5','4','3','2'];
const COL={a:'var(--ag)',c:'var(--ca)',f:'var(--fo)'};
function handName(i,j){const a=RANKS[i],b=RANKS[j];return i===j?a+a:(i<j?a+b+'s':b+a+'o');}
function combos(n){return n.length===2?6:(n[2]==='s'?4:12);}

// ---- selectors ----
const cfgSel=document.getElementById('cfg'), spotSel=document.getElementById('spot');
const configs=[...new Set(DATA.map(c=>c.config))];
configs.forEach(c=>{const o=document.createElement('option');o.value=o.textContent=c;cfgSel.appendChild(o);});
function fillSpots(){
  spotSel.innerHTML='';const cf=cfgSel.value;
  let cat=null;
  DATA.filter(c=>c.config===cf).forEach((c,idx)=>{
    if(c.cat!==cat){cat=c.cat;const og=document.createElement('optgroup');og.label=cat;og.id='og';spotSel.appendChild(og);}
    const o=document.createElement('option');o.value=DATA.indexOf(c);o.textContent=c.title;
    spotSel.lastElementChild.appendChild(o);
  });
}
function curChart(){return DATA[+spotSel.value];}

// ---- grid render ----
function cellBg(fr){ // fr=[a,c,f]
  const a=fr[0],c=fr[1];const s1=a,s2=a+c;
  return `linear-gradient(to right, ${COL.a} 0 ${s1}%, ${COL.c} ${s1}% ${s2}%, ${COL.f} ${s2}% 100%)`;
}
function gridCells(ch,gEl,detailFn){
  gEl.innerHTML='';
  for(let i=0;i<13;i++)for(let j=0;j<13;j++){
    const nm=handName(i,j);const fr=ch.hands[nm]||[0,0,100];
    const d=document.createElement('div');d.className='cell'+(fr[0]+fr[1]===0?' dim':'');
    d.style.background=cellBg(fr);
    d.innerHTML=`<span class="lab">${nm}</span>`+(fr[0]+fr[1]>0&&fr[0]+fr[1]<100?`<span class="pc">${Math.max(fr[0],fr[1])}%</span>`:'');
    if(detailFn){const show=()=>detailFn(nm,fr,ch);d.addEventListener('mouseenter',show);d.addEventListener('click',show);}
    gEl.appendChild(d);
  }
}
function renderGrid(){
  const ch=curChart();
  gridCells(ch,document.getElementById('grid'),showDetail);
  const ch2=ch;document.getElementById('ttl').textContent=ch2.title+(ch2.exact?'':'');
  document.getElementById('ttl').innerHTML=ch2.title+(ch2.exact?'<span class="tag exact">厳密Nash</span>':'<span class="tag">近似</span>');
  document.getElementById('meta').textContent=`${ch2.config} ｜ Range ${ch2.rangePct} ｜ Sizing ${ch2.sizing}`;
  document.getElementById('notes').innerHTML=annotate(ch2.notes);
  legend(document.getElementById('legend'),ch2);
}
function legend(el,ch){
  const ag=ch.aggroLabel||'Raise';
  el.innerHTML=`<span><i style="background:var(--ag)"></i>${ag}</span>`+
    (anyCall(ch)?`<span><i style="background:var(--ca)"></i>Call</span>`:'')+
    `<span><i style="background:var(--fo)"></i>Fold</span>`;
}
function anyCall(ch){return Object.values(ch.hands).some(f=>f[1]>0);}

// ---- explanation engine (why is this action GTO?) ----
function hinfo(nm){
  const R='AKQJT98765432';
  const pair=nm.length===2, suited=nm.length===3&&nm[2]==='s', off=nm.length===3&&nm[2]==='o';
  const hi=R.indexOf(nm[0]), lo=pair?hi:R.indexOf(nm[1]);
  const bw='AKQJT', aceHi=nm[0]==='A';
  const isBroadway=bw.includes(nm[0])&&(pair||bw.includes(nm[1]));
  const gap=pair?0:Math.abs(lo-hi);
  return {pair,suited,off,hi,lo,isBroadway,aceHi,
    wheelAce:aceHi&&suited&&'5432'.includes(nm[1]||''),
    bwAce:aceHi&&'KQJT'.includes(nm[1]||''), conn:gap===1, oneGap:gap===2};
}
function handRole(nm){
  const h=hinfo(nm);
  if(h.pair){ if(h.hi<=2)return'プレミアムペア'; if(h.hi<=4)return'強いペア(JJ/TT)'; if(h.hi<=8)return'ミドルペア'; return'スモールペア（セットマイン主体）'; }
  if(h.wheelAce)return'ウィール系スーテッドエース（ナットブロッカー＋ストレート/フラッシュ性）';
  if(h.bwAce&&h.suited)return'ブロードウェイ・スーテッドエース（強）';
  if(h.aceHi&&h.suited)return'ミドル・スーテッドエース（ブロッカー＋フラッシュ性）';
  if(h.bwAce&&h.off)return'オフスートのAブロードウェイ';
  if(h.aceHi&&h.off)return'オフスートのAハイ（キッカー弱め）';
  if(h.suited&&h.isBroadway)return'スーテッド・ブロードウェイ';
  if(h.suited&&h.conn)return'スーテッドコネクター';
  if(h.suited&&h.oneGap)return'スーテッド・ワンギャッパー';
  if(h.suited)return'スーテッドハンド';
  if(h.off&&h.isBroadway)return'オフスート・ブロードウェイ（支配されやすい）';
  return'オフスートの弱いハンド';
}
function spotKind(ch){
  if(ch.exact)return ch.aggroLabel==='Jam'?'jam':'calljam';
  const hasCall=Object.values(ch.hands).some(f=>f[1]>0);
  if(/BB vs/.test(ch.title))return'bbdef';
  if(ch.aggroLabel==='Open'&&!hasCall)return'rfi';
  if(ch.aggroLabel==='4bet')return'v3bet';
  if(ch.aggroLabel==='3bet')return'vopen';
  return'other';
}
function whyAction(ch,nm,fr,kind,best){
  const h=hinfo(nm), ag=ch.aggroLabel, mixed=fr.filter(x=>x>0&&x<100).length>1;
  const isAgg=best===ag, isCall=best==='Call', P=x=>x+'%';
  if(kind==='rfi'){
    if(isAgg&&!mixed)return'このポジションのオープン核。バリュー・プレイアビリティとも十分で降りる理由がない。';
    if(isAgg&&mixed)return`境界ハンド。オープンEVがほぼ0付近なので頻度を割って${P(fr[0])}だけ開く（ミックス）、残りはフォールド。`+(h.wheelAce?'ウィールエースはブロッカー＋A5s系の遊びやすさでギリギリ開ける。':(h.off?'オフスートは支配されやすく頻度が下がる。':''));
    return'このポジションには弱い/支配されやすく、後ろの人数を考えるとフォールドが最大EV。早いポジションほど開かない。';
  }
  if(kind==='bbdef'){
    if(isCall)return'BBはアクションをクローズし好オッズ（既に1bb投入済みで安く受けられる）。降りるには十分なエクイティがあるのでコールで広く守る。';
    if(isAgg&&!mixed)return'明確なバリュー。3betして価値とレンジ優位を取りに行く。';
    if(isAgg&&mixed)return`ポラー3betの${(h.wheelAce||h.suited)?'ブラフ側':'バリュー寄り'}。`+(h.wheelAce?'相手の継続域(AA/AK/Ax)をブロックしつつフラッシュ/ウィール性がある。':'')+`コール一辺倒だとレンジが受け身になるため、バランス上${P(fr[0])}で3bet。`;
    return'好オッズでもオフスートで支配されやすく実現が悪い、数少ないフォールド。';
  }
  if(kind==='v3bet'){
    if(isAgg&&!mixed)return'支配的バリュー。4betして価値を取りに行く（コールされても優位）。';
    if(isAgg&&mixed)return`4betの${h.wheelAce?'ブラフ主力':'ミックス'}。`+(h.wheelAce?'相手のバリュー継続(AA/AK/Ax)をブロックし、コールされてもプレイアビリティがある。':'')+`${P(fr[0])}で4bet。`;
    if(isCall)return'4betには弱いがフォールドには強すぎる中堅。ポジションがあればフラットしてエクイティを実現する（4betすると降ろされて損）。';
    return'支配されており4betもフラットも割に合わずフォールド。元のオープンが広いほど(=BTN等)多く降りる。';
  }
  if(kind==='vopen'){
    const sb=ch.title.indexOf('SB ')===0||ch.title.indexOf('SB vs')>=0;
    if(isAgg&&!mixed)return'バリュー3bet。'+(sb?'SBはOOPでBBも残るためフラットが弱く、強い手は3betする。':'価値を取りに行く。');
    if(isAgg&&mixed)return`3betの${h.wheelAce?'ブラフ側':'ミックス'}。`+(h.wheelAce?'ブロッカー＋プレイアビリティでブラフに最適。':'')+(sb?'SBはOOPなので3bet-or-fold寄り。':'')+`${P(fr[0])}で3bet。`;
    if(isCall)return'ポジションがあるのでフラットして安く見る（3betするには中途半端、降りるには強い）。';
    return sb?'SBはOOP＋BB残りでフラットできず、3betに値しない手は全てフォールド。':'支配されやすくフォールド。';
  }
  if(kind==='jam'){
    if(isAgg&&!mixed)return`このスタックでは全in推奨。ショーダウン価値＋フォールドエクイティで+EV。オールインはインプライドオッズが消えるため${h.pair?'ペアの素の強さ':(h.aceHi?'Aハイのショーダウン価値':'素のショーダウン価値')}が効く。`;
    if(isAgg&&mixed)return`均衡上の境界。${P(fr[0])}でjam（残りフォールド）。スタックが浅くなるほどjam域は広がる。`;
    return'全inには弱すぎる（支配される/ショーダウン価値不足）。ただしスタックが浅いほどjam域は広がるので、より短ければjamに変わる。';
  }
  if(kind==='calljam'){
    if(isCall&&!mixed)return'相手のジャムレンジに対し十分なエクイティがあり、コールが+EV。';
    if(isCall&&mixed)return`コール/フォールドの境界（${P(fr[1])}でコール）。ジャムが浅いほどコール域は広い。`;
    return'相手のジャム域に支配される。ジャムが大きい（スタックが深い）ほどコール域は狭まる。';
  }
  return'役割と頻度から最大EVのアクションを選ぶ。';
}
function explain(ch,nm,fr){
  const kind=spotKind(ch), ag=ch.aggroLabel||'Raise';
  const acts=[[ag,fr[0]],['Call',fr[1]],['Fold',fr[2]]];
  const best=acts.reduce((a,b)=>b[1]>a[1]?b:a)[0];
  return `<b>なぜ「${best}」か</b><div class="role">▷ ${nm} = ${handRole(nm)}</div>${whyAction(ch,nm,fr,kind,best)}`+
    `<details><summary>このスポットの全体解説を表示</summary>${annotate(ch.notes||'')}</details>`;
}
function detailHtml(nm,fr,ch){
  const ag=ch.aggroLabel||'Raise';
  return `<b>${nm}</b> <span style="color:var(--mut)">(${combos(nm)} combos)</span>`+
    `<div class="bar">${fr[0]?`<span style="width:${fr[0]}%;background:var(--ag)"></span>`:''}${fr[1]?`<span style="width:${fr[1]}%;background:var(--ca)"></span>`:''}${fr[2]?`<span style="width:${fr[2]}%;background:var(--fo)"></span>`:''}</div>`+
    `${ag} ${fr[0]}% &nbsp; Call ${fr[1]}% &nbsp; Fold ${fr[2]}%`+
    evLine(ch,nm)+
    `<div class="why">${explain(ch,nm,fr)}</div>`;
}
function showDetail(nm,fr,ch){document.getElementById('detail').innerHTML=detailHtml(nm,fr,ch);}
// quiz-side chart (shows the chart for the current quiz spot in the right panel)
let qchartOpen=false;
function showQuizChart(ch){
  document.getElementById('qcTtl').innerHTML=ch.title+(ch.exact?'<span class="tag exact">厳密</span>':'<span class="tag">近似</span>');
  document.getElementById('qcMeta').textContent=`${ch.config} ｜ ${ch.rangePct} ｜ ${ch.sizing}`;
  gridCells(ch,document.getElementById('qcGrid'),(nm,fr,c)=>{document.getElementById('qcDetail').innerHTML=detailHtml(nm,fr,c);});
  legend(document.getElementById('qcLeg'),ch);
  document.getElementById('qcDetail').innerHTML='マスにマウス/クリックで内訳。';
}
function toggleQuizChart(){
  qchartOpen=!qchartOpen;
  document.getElementById('qchart').style.display=qchartOpen?'block':'none';
  document.getElementById('qChartBtn').classList.toggle('on',qchartOpen);
  if(qchartOpen&&cur)showQuizChart(cur.ch);
}

// ---- quiz ----
let score=0,tries=0,cur=null,qmode='strat';
const WNAMES=[];for(let i=0;i<13;i++)for(let j=0;j<13;j++){const nm=handName(i,j),w=combos(nm);for(let q=0;q<w;q++)WNAMES.push(nm);} // combo-weighted
let reviewMode=false, missed=[];
try{missed=JSON.parse(localStorage.getItem('gtoMissed')||'[]');}catch(e){missed=[];}
function saveMissed(){try{localStorage.setItem('gtoMissed',JSON.stringify(missed.slice(-500)));}catch(e){}}
function updMissedUI(){const el=document.getElementById('missN');if(el)el.textContent=missed.length;}
function evLine(ch,nm){
  if(!ch.ev||ch.ev[nm]===undefined||ch.ev[nm]===null)return '';
  const e=ch.ev[nm],ef=ch.evFold||0,ag=ch.aggroLabel||'Jam',u=ch.evUnit||'bb',better=e>ef;
  return `<div class="evrow">EV(${ag}) <b style="color:${e>=0?'var(--ca)':'var(--ag)'}">${e>=0?'+':''}${e} ${u}</b> vs Fold ${ef} ${u} → 推奨 <b style="color:${better?'var(--ca)':'var(--fo)'}">${better?ag:'Fold'}</b></div>`;
}
// ---- poker-table view ----
const SUIT={s:['♠','b'],h:['♥','r'],d:['♦','r'],c:['♣','b']};
function handToCards(nm){
  const r1=nm[0], r2=nm.length>2?nm[1]:nm[0];
  if(nm.length===2)return [[r1,'s'],[r2,'h']];
  if(nm[2]==='s')return [[r1,'s'],[r2,'s']];
  return [[r1,'s'],[r2,'h']];
}
function cardHtml(rank,suit){const sy=SUIT[suit];const R=rank==='T'?'10':rank;return '<div class="card '+(sy[1]==='r'?'red':'')+'">'+R+'<span>'+sy[0]+'</span></div>';}
function posTokens(s){const re=/UTG\+?2|UTG\+?1|UTG|LJ|HJ|MP|CO|BTN|SB|BB/g;const out=[];let m;while((m=re.exec(s))){let p=m[0].replace('+','');if(p==='MP')p='HJ';if(out[out.length-1]!==p)out.push(p);}return out;}
function seatsFor(ch){const x=ch.config+' '+ch.title;
  if(/\bHU\b/.test(x))return ['SB','BB'];
  if(/4-max/.test(x))return ['UTG','BTN','SB','BB'];
  if(/Full-ring|9-max|\bFR\b/.test(x))return ['UTG','UTG1','UTG2','LJ','HJ','CO','BTN','SB','BB'];
  return ['UTG','HJ','CO','BTN','SB','BB'];}
function scenario(ch){
  const seats=seatsFor(ch), n=seats.length;
  const isRFI=/RFI/i.test(ch.title), ag=ch.aggroLabel, jam=/jam/i.test(ch.title);
  let toks=posTokens(ch.title);
  let hero=toks[0]; if(seats.indexOf(hero)<0)hero=seats[Math.max(0,n-3)];
  const hi=seats.indexOf(hero);
  let opp=null;
  if(!isRFI){ opp=toks[1]||null; if(opp===null&&ag==='Call')opp=seats[hi-1]||null; }
  const st={}; seats.forEach(s=>{st[s]= s==='SB'?'sb': s==='BB'?'bb':'none';});
  if(opp===null){
    for(let i=0;i<hi;i++)st[seats[i]]='fold';
    for(let i=hi+1;i<n;i++){if(st[seats[i]]==='sb'||st[seats[i]]==='bb')continue;st[seats[i]]='wait';}
  } else if(ag==='4bet'){
    seats.forEach(s=>{ if(s===hero)st[s]='open'; else if(s===opp)st[s]='3bet'; else st[s]='fold'; });
  } else {
    seats.forEach((s,i)=>{ if(s===hero||s===opp)return;
      if(i>hi){ if(st[s]!=='sb'&&st[s]!=='bb')st[s]='wait'; } else st[s]='fold'; });
    st[opp]= jam?'jam':'open';
  }
  st[hero]='hero';
  return {seats,hero,hi,n,st};
}
const CHIP_PER_BB=100; // 初心者向けチップ換算（BB=100チップ）
function spotStack(ch){let m=(ch.title||'').match(/(\d+)\s*bb/i);if(m)return +m[1];m=(ch.config||'').match(/(\d+)\s*bb/i);if(m)return +m[1];return 100;}
function potSize(ch,sc){const ante=/ante/i.test(ch.config||'')?1:0,stk=spotStack(ch),v4=ch.aggroLabel==='4bet';let pot=ante;
  sc.seats.forEach(pos=>{const a=sc.st[pos],bl=pos==='SB'?0.5:pos==='BB'?1.0:0;
    if(a==='open')pot+=2.3;else if(a==='3bet')pot+=10;else if(a==='jam')pot+=stk;else if(a==='hero')pot+=bl+(v4?2.3:0);else pot+=bl;});
  return pot;}
function renderTable(ch,nm){
  const sc=scenario(ch), cs=handToCards(nm), stk=spotStack(ch), pot=Math.round(potSize(ch,sc)*10)/10;
  const CH=v=>Math.round(v*CHIP_PER_BB).toLocaleString();
  let h='<div class="board">'+'<div class="slot"></div>'.repeat(5)+'</div><div class="pot">ポット ≈ '+pot+'bb（'+CH(pot)+'チップ）</div>';
  const A={fold:['FOLD','f'],open:['RAISE','r'],'3bet':['3BET','t'],jam:['JAM','t'],call:['CALL','c'],sb:['SB','b'],bb:['BB','b'],wait:['…','w']};
  sc.seats.forEach((pos,j)=>{
    const k=(j-sc.hi+sc.n)%sc.n, th=Math.PI+2*Math.PI*k/sc.n;
    const x=(50+44*Math.sin(th)).toFixed(1), y=(50-40*Math.cos(th)).toFixed(1);
    const stt=sc.st[pos], hero=pos===sc.hero;
    let inner='<div class="pos">'+pos+(hero?' ★':'')+'</div>';
    if(hero) inner+='<div class="cards">'+cardHtml(cs[0][0],cs[0][1])+cardHtml(cs[1][0],cs[1][1])+'</div>';
    else if(A[stt]) inner+='<div class="act '+A[stt][1]+'">'+A[stt][0]+'</div>';
    inner+='<div class="stack">'+(hero?'あなた ':'')+stk+'bb・'+CH(stk)+'</div>';
    h+='<div class="seat'+(hero?' hero':'')+(stt==='fold'?' fold':'')+'" style="left:'+x+'%;top:'+y+'%">'+inner+'</div>';
  });
  document.getElementById('ptable').innerHTML=h;
}
function pickQuiz(){
  let ch,nm;const scope=document.getElementById('qscope');
  if(reviewMode&&missed.length){
    const m=missed[Math.floor(Math.random()*missed.length)];
    ch=DATA.find(c=>c.config===m.config&&c.title===m.title);nm=m.nm;
    if(!ch){missed=missed.filter(x=>x!==m);saveMissed();updMissedUI();return pickQuiz();}
  }else{
    const sv=scope?scope.value:'cfg';
    const isEdge=c=>c.config.indexOf('EDGE')===0;
    let pool;
    if(sv==='edge')pool=DATA.filter(c=>isEdge(c)&&Object.keys(c.hands).length);
    else if(sv==='all')pool=DATA.filter(c=>Object.keys(c.hands).length);
    else pool=DATA.filter(c=>c.config===cfgSel.value&&Object.keys(c.hands).length);
    if(!pool.length)pool=DATA.filter(c=>Object.keys(c.hands).length);
    const sk=document.getElementById('qstack'),sv2=sk?sk.value:'all';
    if(sv2!=='all'){const inR=v=>sv2==='le10'?v<=10:sv2==='11-20'?(v>=11&&v<=20):sv2==='21-50'?(v>=21&&v<=50):v>50;
      const f=pool.filter(c=>inR(spotStack(c)));if(f.length)pool=f;}
    ch=pool[Math.floor(Math.random()*pool.length)];
    nm=WNAMES[Math.floor(Math.random()*WNAMES.length)];   // combo-weighted
  }
  const fr=ch.hands[nm]||[0,0,100];
  cur={ch,nm,fr};
  if(qchartOpen)showQuizChart(ch);
  document.getElementById('qspot').textContent=`${ch.config} — ${ch.title}（${nm}）`+(reviewMode?'  [復習]':'');
  renderTable(ch,nm);
  document.getElementById('qres').innerHTML='';
  const ag=ch.aggroLabel||'Raise';
  let acts; if(ag==='Call'){acts=[['Call',1],['Fold',2]];} else {acts=[[ag,0]];if(anyCall(ch))acts.push(['Call',1]);acts.push(['Fold',2]);}
  const bw=document.getElementById('qbtns');bw.innerHTML='';
  acts.forEach(([label,idx])=>{const b=document.createElement('button');b.textContent=label;
    b.onclick=()=>answer(idx,label);bw.appendChild(b);});
  legend(document.getElementById('qlegend'),ch);
}
function answer(idx,label){
  if(!cur||cur.done)return;cur.done=true;tries++;
  const fr=cur.fr;const best=Math.max(fr[0],fr[1],fr[2]);
  const chosen=fr[idx];const ok=chosen===best;
  if(ok)score++;
  if(!ok){missed.push({config:cur.ch.config,title:cur.ch.title,nm:cur.nm});saveMissed();updMissedUI();}
  else if(reviewMode){const i=missed.findIndex(m=>m.config===cur.ch.config&&m.title===cur.ch.title&&m.nm===cur.nm);if(i>=0){missed.splice(i,1);saveMissed();updMissedUI();}}
  const ag=cur.ch.aggroLabel||'Raise';
  document.getElementById('qres').innerHTML=
    `<b style="color:${ok?'var(--ca)':'var(--ag)'}">${ok?'◎ 正解':'✕ 不正解'}</b> — あなた: ${label} (${chosen}%)<br>`+
    `<div class="bar" style="height:18px;margin-top:8px">${fr[0]?`<span style="width:${fr[0]}%;background:var(--ag)"></span>`:''}${fr[1]?`<span style="width:${fr[1]}%;background:var(--ca)"></span>`:''}${fr[2]?`<span style="width:${fr[2]}%;background:var(--fo)"></span>`:''}</div>`+
    `GTO: ${ag} ${fr[0]}% / Call ${fr[1]}% / Fold ${fr[2]}%`+
    evLine(cur.ch,cur.nm)+
    `<div class="why">${explain(cur.ch,cur.nm,fr)}</div>`;
  updScore();
}
function updScore(){if(qmode!=='strat')return;document.getElementById('score').textContent=tries?`戦略クイズ 正解 ${score}/${tries} (${Math.round(score/tries*100)}%)`:'';}

// ---- term quiz (用語当て / 定義当て) ----
const ALLTERMS=[];GLOSSARY.forEach(c=>c.terms.forEach(t=>ALLTERMS.push(t)));
let tscore=0,ttries=0,tcur=null;
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));const x=a[i];a[i]=a[j];a[j]=x;}return a;}
function updTScore(){if(qmode!=='term')return;document.getElementById('score').textContent=ttries?`用語クイズ 正解 ${tscore}/${ttries} (${Math.round(tscore/ttries*100)}%)`:'';}
function pickTermQuiz(){
  if(!ALLTERMS.length)return;
  const dir=Math.random()<0.5?'d2t':'t2d';
  const correct=ALLTERMS[Math.floor(Math.random()*ALLTERMS.length)];
  const pool=shuffle(ALLTERMS.filter(t=>t.term!==correct.term).slice()).slice(0,3);
  const opts=shuffle([correct,...pool]);
  tcur={correct,done:false};
  const tp=document.getElementById('tprompt'),td=document.getElementById('tdef'),tb=document.getElementById('tbtns'),tr=document.getElementById('tres');
  tr.innerHTML='';tb.innerHTML='';
  if(dir==='d2t'){
    tp.textContent='次の説明に当てはまる用語は？';
    td.innerHTML=`<div class="defbox">${correct.short}${correct.long?'<br><span class="mut2">'+correct.long+'</span>':''}</div>`;
    opts.forEach(o=>{const b=document.createElement('button');b.innerHTML=`${o.term} <span class="gt-r">${o.reading}</span>`;b.onclick=()=>answerTerm(o.term===correct.term);tb.appendChild(b);});
  }else{
    tp.textContent='次の用語の説明として正しいのは？';
    td.innerHTML=`<div class="defbox"><b style="font-size:20px">${correct.term}</b> <span class="gt-r">${correct.reading}</span></div>`;
    opts.forEach(o=>{const b=document.createElement('button');b.textContent=o.short;b.onclick=()=>answerTerm(o.term===correct.term);tb.appendChild(b);});
  }
}
function answerTerm(ok){
  if(!tcur||tcur.done)return;tcur.done=true;ttries++;if(ok)tscore++;
  const c=tcur.correct;
  document.getElementById('tres').innerHTML=
    `<b style="color:${ok?'var(--ca)':'var(--ag)'}">${ok?'◎ 正解':'✕ 不正解'}</b>`+
    `<div class="why" style="border-color:${ok?'var(--ca)':'var(--ag)'}"><b>${c.term}</b> <span class="gt-r">${c.reading}</span><div class="gt-s">${c.short}</div>${c.long?`<div class="gt-l">${c.long}</div>`:''}<div style="margin-top:8px"><span class="chip lk" id="tgo">用語集で見る ▸</span></div></div>`;
  const go=document.getElementById('tgo');if(go)go.onclick=()=>gotoGloss(slug(c.term));
  updTScore();
}
function setQMode(m){
  qmode=m;
  document.getElementById('qmStrat').classList.toggle('on',m==='strat');
  document.getElementById('qmTerm').classList.toggle('on',m==='term');
  document.getElementById('qmPost').classList.toggle('on',m==='post');
  document.getElementById('qmSrp').classList.toggle('on',m==='srp');
  document.getElementById('sQuiz').style.display=m==='strat'?'block':'none';
  document.getElementById('tQuiz').style.display=m==='term'?'block':'none';
  document.getElementById('pQuiz').style.display=m==='post'?'block':'none';
  document.getElementById('srpQuiz').style.display=m==='srp'?'block':'none';
  document.getElementById('qchart').style.display=(m==='strat'&&qchartOpen)?'block':'none';
  if(m==='strat'){pickQuiz();updScore();}
  else if(m==='term'){pickTermQuiz();updTScore();}
  else if(m==='post'){pickPost();updPScore();}
  else{pickSrp();updSScore();}
}
// ---- postflop skill quiz (engine-based: hand reading / equity / outs / pot odds) ----
let pscore=0,ptries=0,pcur=null;
function updPScore(){if(qmode!=='post')return;document.getElementById('score').textContent=ptries?('ポストフロップ 正解 '+pscore+'/'+ptries+' ('+Math.round(pscore/ptries*100)+'%)'):'';}
function pqCard(c){const r=RKS[(c/4)|0],s=c%4,R=r==='T'?'10':r;return '<span class="pqc" style="color:'+SUITCOL[s]+'">'+R+SUITSYM[s]+'</span>';}
function dealPost(){const deck=[];for(let c=0;c<52;c++)deck.push(c);for(let i=51;i>0;i--){const j=(Math.random()*(i+1))|0;const t=deck[i];deck[i]=deck[j];deck[j]=t;}
  const street=[3,3,4,4,5][(Math.random()*5)|0];return {you:[deck[0],deck[1]],opp:[deck[2],deck[3]],board:deck.slice(4,4+street)};}
function outsVs(you,opp,board){const dead={};[].concat(board,you,opp).forEach(c=>dead[c]=1);const deck=[];for(let c=0;c<52;c++)if(!dead[c])deck.push(c);let cnt=0,cards=[];for(let i=0;i<deck.length;i++){const full=board.concat([deck[i]]);if(evaluate7(you.concat(full))>=evaluate7(opp.concat(full))){cnt++;cards.push(deck[i]);}}return {count:cnt,cards:cards};}
function shuffleArr(a){for(let i=a.length-1;i>0;i--){const j=(Math.random()*(i+1))|0;const t=a[i];a[i]=a[j];a[j]=t;}return a;}
function catOptions(correct){const s=new Set([correct]);while(s.size<4)s.add((Math.random()*9)|0);return shuffleArr([...s]);}
function numOptions(correct){const s=new Set([correct]);const cand=[correct-2,correct+2,correct-4,correct+4,correct-1,correct+1,correct+6,Math.max(0,correct-3)];for(let i=0;i<cand.length;i++){if(cand[i]>=0&&s.size<4)s.add(cand[i]);}let n=correct+1;while(s.size<4)s.add(n++);return shuffleArr([...s]);}
function pickPost(){
  const d=dealPost(),street=d.board.length;
  const eq=computeEquity([d.you,d.opp],d.board),myEq=eq[0].equity;
  const myS=evaluate7(d.you.concat(d.board)),opS=evaluate7(d.opp.concat(d.board));
  const myCat=(myS/EBASE)|0,opCat=(opS/EBASE)|0,behind=myS<opS;
  let pool=['cat','ahead'];if(street<5){pool.push('equity','potodds');if(behind)pool.push('outs');}
  const type=pool[(Math.random()*pool.length)|0];let q;
  if(type==='cat')q={showOpp:false,prompt:'あなたの今の役は？',options:catOptions(myCat).map(k=>({label:catName(k),correct:k===myCat})),explain:'あなたの5枚での最強の役です。'};
  else if(type==='ahead'){const cor=myS>opS?'win':myS<opS?'lose':'tie',L={win:'あなたが上（リード）',lose:'相手が上（ビハインド）',tie:'同じ（タイ）'};q={showOpp:true,prompt:'今、手が強いのはどっち？',options:['win','lose','tie'].map(k=>({label:L[k],correct:k===cor})),explain:'あなた: '+catName(myCat)+' ／ 相手: '+catName(opCat)+'（このあと変わる可能性あり）'};}
  else if(type==='equity'){const b=myEq<30?0:myEq<50?1:myEq<70?2:3,L=['〜30%（不利）','30〜50%','50〜70%','70%〜（有利）'];q={showOpp:true,prompt:'リバーまでのあなたの勝率は？',options:L.map((l,i)=>({label:l,correct:i===b})),explain:'実際は約'+myEq.toFixed(0)+'%。'};}
  else if(type==='outs'){const o=outsVs(d.you,d.opp,d.board);q={showOpp:true,prompt:'次の1枚で逆転（最強以上）になるカードは何枚？',options:numOptions(o.count).map(n=>({label:n+'枚',correct:n===o.count})),explain:'アウツ '+o.count+'枚: '+o.cards.slice(0,18).map(pcardText1).join(' ')};}
  else{const P=[2,3,4,6,8][(Math.random()*5)|0],Bm=[0.33,0.5,0.75,1][(Math.random()*4)|0],B=Math.round(P*Bm*10)/10,need=B/(P+2*B)*100,call=myEq>=need;q={showOpp:true,prompt:'ポット '+P+'bb に相手が '+B+'bb ベット。あなたの勝率 ≈ '+myEq.toFixed(0)+'%。どうする？',options:shuffleArr([{label:'コール',correct:call},{label:'フォールド',correct:!call}]),explain:'必要勝率 = ベット/(ポット+ベット×2) = '+need.toFixed(0)+'%。あなた '+myEq.toFixed(0)+'% '+(call?'≥':'<')+' '+need.toFixed(0)+'% → '+(call?'コール':'フォールド')+'。'};}
  pcur={d,q,done:false};renderPost();
}
function renderPost(){
  const d=pcur.d,q=pcur.q,sn=d.board.length===3?'フロップ':d.board.length===4?'ターン':'リバー';
  let h='<div class="pq-board"><span class="pq-lbl">ボード（'+sn+'）</span>'+d.board.map(pqCard).join('')+'</div>';
  h+='<div class="pq-hands"><span class="pq-lbl">あなた</span> '+d.you.map(pqCard).join('');
  if(q.showOpp)h+=' &nbsp;&nbsp;<span class="pq-lbl">相手</span> '+d.opp.map(pqCard).join('');
  h+='</div><div class="pq-q">'+q.prompt+'</div><div class="qbtns" id="pqbtns"></div><div class="qres" id="pqres"></div>';
  document.getElementById('pQuizBody').innerHTML=h;
  const bw=document.getElementById('pqbtns');q.options.forEach((o,i)=>{const b=document.createElement('button');b.textContent=o.label;b.onclick=()=>answerPost(i);bw.appendChild(b);});
}
function answerPost(i){
  if(!pcur||pcur.done)return;pcur.done=true;ptries++;
  const ok=pcur.q.options[i].correct;if(ok)pscore++;
  const cor=pcur.q.options.find(o=>o.correct).label;
  document.getElementById('pqres').innerHTML='<b style="color:'+(ok?'var(--ca)':'var(--ag)')+'">'+(ok?'◎ 正解':'✕ 不正解（正解: '+cor+'）')+'</b><div class="why">'+pcur.q.explain+'</div>';
  updPScore();
}

// ---- SRP postflop STRATEGY quiz (BTN vs BB single-raised pot, self-built vector-CFR) ----
let sscore=0,stries=0,scur=null;
const SRPNOTE='※単一ベットラウンド解（ターン以降=エクイティ）のため、ベット頻度は実戦GTOより控えめに出ます。相対傾向・盤面差・守備の広さを学ぶ用です。複数の行動がGTOミックスなら、いずれも正解として扱います。';
function updSScore(){if(qmode!=='srp')return;document.getElementById('score').textContent=stries?('SRP戦略 '+sscore+'/'+stries+' ('+Math.round(sscore/stries*100)+'%)'):'';}
function srpCard(t){return RKS.indexOf(t[0])*4+({s:0,h:1,d:2,c:3})[t[1]];}
function srpFlopCards(s){return [srpCard(s.slice(0,2)),srpCard(s.slice(2,4)),srpCard(s.slice(4,6))];}
function srpPickCombo(name,dead){const cs=classCombos(name).filter(c=>!dead[c[0]]&&!dead[c[1]]);return cs.length?cs[(Math.random()*cs.length)|0]:null;}
const SRPNOTE2='※2ストリート解（フロップ＋ターン、リバー=エクイティ）。ターンの追撃価値が入るため実戦的なc-bet頻度。複数の行動がGTOミックスなら、いずれも正解として扱います。';
function srpStart(F,board,name,combo,mix,prompt,note){scur={F,board,combo,name,mix,prompt,note,done:false};renderSrp();}
function srpDeal(F){const board=srpFlopCards(F.flop),dead={};board.forEach(c=>dead[c]=1);return {board,dead};}
function srpHand(names,dead){let name=null,combo=null;for(let t=0;t<16&&!combo;t++){name=names[(Math.random()*names.length)|0];combo=srpPickCombo(name,dead);}return {name,combo};}
function pickSrp(){
  const has2=!!(SRP2.flops&&SRP2.flops.length), has1=!!(SRP.flops&&SRP.flops.length);
  if(!has1&&!has2){document.getElementById('srpQuizBody').innerHTML='<div class="gmut">SRPデータがありません。</div>';return;}
  let side=Math.random()<0.5?'btn':'bb';
  if(side==='bb'&&!has1)side='btn';
  if(side==='btn'&&has2){            // BTN c-bet from realistic 2-street solve
    const F=SRP2.flops[(Math.random()*SRP2.flops.length)|0],{board,dead}=srpDeal(F);
    const {name,combo}=srpHand(Object.keys(F.cbet),dead),bet=F.cbet[name]||0;
    srpStart(F,board,name,combo,[['cベット(2/3)',bet],['チェック',Math.max(0,100-bet)]],
      'あなたは <b>BTN</b>。BBがチェックした。あなたの行動は？','ターンの追撃価値込みの実戦的c-bet頻度。'+SRPNOTE2);return;
  }
  if(side==='btn'){                  // fallback: single-street sizing
    const F=SRP.flops[(Math.random()*SRP.flops.length)|0],{board,dead}=srpDeal(F);
    const {name,combo}=srpHand(Object.keys(F.cbet),dead),big=F.cbet_big[name]||0,small=F.cbet_small[name]||0;
    srpStart(F,board,name,combo,[['大ベット(75%)',big],['小ベット(33%)',small],['チェック',Math.max(0,100-big-small)]],
      'あなたは <b>BTN</b>。BBがチェックした。あなたの行動は？','BTNのc-betは小33%/大75%の2サイズから選択。'+SRPNOTE);return;
  }
  // BB defense (single-street includes check-raise)
  const F=SRP.flops[(Math.random()*SRP.flops.length)|0],{board,dead}=srpDeal(F);
  const {name,combo}=srpHand(Object.keys(F.bb_call),dead),rai=F.bb_raise[name]||0,cal=F.bb_call[name]||0;
  srpStart(F,board,name,combo,[['チェックレイズ',rai],['コール',cal],['フォールド',Math.max(0,100-rai-cal)]],
    'あなたは <b>BB</b>。BTNがc-betした。あなたの行動は？','ウェット（連結・二色）な盤ほど守備（コール/レイズ）を広げる。'+SRPNOTE);
}
function renderSrp(){
  const s=scur;
  let h='<div class="pq-board"><span class="pq-lbl">フロップ（'+s.F.label+'）</span>'+s.board.map(pqCard).join('')+'</div>';
  h+='<div class="pq-hands"><span class="pq-lbl">あなたのハンド（'+s.name+'）</span> '+(s.combo?s.combo.map(pqCard).join(''):s.name)+'</div>';
  h+='<div class="pq-q">'+s.prompt+'</div><div class="qbtns" id="srpbtns"></div><div class="qres" id="srpres"></div>';
  document.getElementById('srpQuizBody').innerHTML=h;
  const bw=document.getElementById('srpbtns');s.mix.forEach((m,i)=>{const b=document.createElement('button');b.textContent=m[0];b.onclick=()=>answerSrp(i);bw.appendChild(b);});
}
function answerSrp(i){
  if(!scur||scur.done||i>=scur.mix.length)return;scur.done=true;stries++;
  const mix=scur.mix,freq=mix[i][1];let amax=0;for(let k=1;k<mix.length;k++)if(mix[k][1]>mix[amax][1])amax=k;
  const ok=(freq>=20)||(i===amax);if(ok)sscore++;
  const bars=mix.map((m,k)=>'<div style="display:flex;justify-content:space-between;gap:12px;padding:1px 0'+(k===amax?';font-weight:700':'')+'"><span>'+m[0]+(k===amax?' ◀ 最頻':'')+'</span><b>'+Math.round(m[1])+'%</b></div>').join('');
  document.getElementById('srpres').innerHTML='<b style="color:'+(ok?'var(--ca)':'var(--ag)')+'">'+(ok?'◎ GTOミックスに含まれる行動':'△ 頻度の低い行動（最頻は別）')+'</b><div class="why"><div style="margin:0 0 6px">GTO頻度（'+scur.name+'）:</div>'+bars+'<div style="margin-top:8px">'+scur.note+'</div></div>';
  updSScore();
}

// ---- glossary ---- (GLOSSARY is declared at the top)
function slug(s){return s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');}
const GTERMS={};
GLOSSARY.forEach(cat=>cat.terms.forEach(t=>{GTERMS[slug(t.term)]=t;}));

// ---- interlinks: glossary <-> chart, and hover-link engine ----
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
const TERM2CHART={
  '3-bet':['6-max 100bb cash','BTN open vs SB 3bet'],'4-bet':['6-max 100bb cash','BTN open vs SB 3bet'],
  'blocker':['6-max 100bb cash','BTN open vs SB 3bet'],'polar-linear-merged':['6-max 100bb cash','BTN open vs SB 3bet'],
  'polarization':['6-max 100bb cash','BTN open vs SB 3bet'],
  'mixed-strategy':['6-max 100bb cash','BTN open vs SB 3bet'],'cold-4-bet':['6-max 100bb cash','BTN open vs SB 3bet'],
  'rfi-raise-first-in':['6-max 100bb cash','BTN RFI'],'open':['6-max 100bb cash','BTN RFI'],'open-raise':['6-max 100bb cash','BTN RFI'],
  'open-range':['6-max 100bb cash','BTN RFI'],
  'steal':['6-max 100bb cash','BTN RFI'],'range':['6-max 100bb cash','BTN RFI'],
  'big-blind-defense':['6-max 100bb cash','BB vs BTN open'],'squeeze':['6-max 100bb cash','BB vs BTN open'],
  'defend':['6-max 100bb cash','BB vs BTN open'],
  'push-fold':['HU Push/Fold (exact Nash)','HU SB Jam — 10bb'],'jam':['HU Push/Fold (exact Nash)','HU SB Jam — 10bb'],
  'all-in':['HU Push/Fold (exact Nash)','HU SB Jam — 10bb'],'open-jam':['HU Push/Fold (exact Nash)','HU SB Jam — 10bb'],
  'heads-up':['HU Push/Fold (exact Nash)','HU SB Jam — 10bb'],'blind-vs-blind':['HU Push/Fold (exact Nash)','HU SB Jam — 10bb'],
  'nash-equilibrium':['HU Push/Fold (exact Nash)','HU SB Jam — 10bb'],'icm':['HU Push/Fold (exact Nash)','HU SB Jam — 10bb'],
  'effective-stack':['HU Push/Fold (exact Nash)','HU SB Jam — 10bb'],'short-stack':['HU Push/Fold (exact Nash)','HU SB Jam — 10bb'],
  'ante':['MTT 40bb +ante 6-max','MTT BTN RFI'],
};
function gotoGloss(s){showView('gloss');const gi=document.getElementById('gsearch');if(gi)gi.value='';renderGloss('');const el=document.getElementById('t_'+s);if(el){el.scrollIntoView({behavior:'smooth',block:'center'});el.classList.add('flash');setTimeout(()=>el.classList.remove('flash'),1200);}}
function gotoChart(cfg,like){cfgSel.value=cfg;fillSpots();const o=[...spotSel.options].find(x=>x.textContent.indexOf(like)>=0);if(o)spotSel.value=o.value;renderGrid();showView('chart');}
const LINK_DEFS=[
  ['equity realization','Equity realization'],['range advantage','Range advantage'],['nut advantage','Nut advantage'],
  ['pot odds','Pot odds'],['implied odds','Implied odds'],['fold equity','Fold equity'],['suited connector','Suited connector'],
  ['mixed strateg(?:y|ies)','Mixed strategy'],['cold call','Cold call'],['isolation','Isolation raise'],
  ['3-?bet','3-bet'],['4-?bet','4-bet'],['5-?bet','5-bet'],['c-?bet','C-bet'],['semi-?bluff','Semi-bluff'],
  ['push/?fold','Push/fold'],['all-?in','All-in'],['open-?jam','Open-jam'],['jams?','Jam'],
  ['RFI','RFI'],['MDF','MDF'],['ICM','ICM'],['SPR','SPR'],['GTO','GTO'],['OESD','OESD'],
  ['equity','Equity'],['blocker','Blocker'],['polar','Polar'],['linear','Linear'],['merged','Merged'],
  ['squeeze','Squeeze'],['overbet','Overbet'],['dominated','Dominated'],['cooler','Cooler'],
  ['gutshot','Gutshot'],['Nash','Nash equilibrium'],['wheel','Wheel'],['broadway','Broadway'],
];
const LINKS=LINK_DEFS.map(([pat,name])=>{const s=slug(name);return GTERMS[s]?{re:new RegExp('(?<![\\\\w-])('+pat+')(?![\\\\w-])','i'),slug:s,label:(GTERMS[s].reading?GTERMS[s].reading+'：':'')+GTERMS[s].short}:null;}).filter(Boolean);
function annotate(text){let s=esc(text);const store=[];LINKS.forEach(L=>{s=s.replace(L.re,(m)=>{const i=store.length;store.push('<span class="gl" data-go="'+L.slug+'" title="'+L.label.replace(/"/g,'&quot;')+'">'+m+'</span>');return '\\u0000'+i+'\\u0000';});});return s.replace(/\\u0000(\\d+)\\u0000/g,(_,i)=>store[+i]);}

function renderGloss(q){
  q=(q||'').trim().toLowerCase();
  const root=document.getElementById('glist');root.innerHTML='';let shown=0;
  GLOSSARY.forEach(cat=>{
    const hits=cat.terms.filter(t=>!q||((t.term+' '+t.reading+' '+t.short+' '+(t.long||'')).toLowerCase().includes(q)));
    if(!hits.length)return;
    const sec=document.createElement('div');sec.className='gcat';
    sec.innerHTML=`<h3>${cat.label}<span>${hits.length}語</span></h3>`;
    const grid=document.createElement('div');grid.className='gcards';
    hits.forEach(t=>{shown++;
      const card=document.createElement('div');card.className='gterm';card.id='t_'+slug(t.term);
      const rel=(t.related||[]).map(r=>{const s=slug(r);return `<span class="chip${GTERMS[s]?' lk':''}"${GTERMS[s]?` data-go="${s}"`:''}>${r}</span>`;}).join('');
      const go=TERM2CHART[slug(t.term)];
      const goBtn=go?`<div><button class="gl-go" data-cfg="${go[0]}" data-like="${go[1]}">📊 チャートで見る</button></div>`:'';
      card.innerHTML=`<div class="gt-h"><b>${t.term}</b>${t.reading?`<span class="gt-r">${t.reading}</span>`:''}</div>`+
        `<div class="gt-s">${t.short}</div>`+(t.long?`<div class="gt-l">${t.long}</div>`:'')+
        (rel?`<div class="gt-rel">関連: ${rel}</div>`:'')+goBtn;
      grid.appendChild(card);});
    sec.appendChild(grid);root.appendChild(sec);
  });
  if(!shown)root.innerHTML='<div class="gmut">該当する用語がありません。</div>';
  root.querySelectorAll('.chip.lk').forEach(c=>c.onclick=()=>gotoGloss(c.getAttribute('data-go')));
  root.querySelectorAll('.gl-go').forEach(b=>b.onclick=()=>gotoChart(b.dataset.cfg,b.dataset.like));
}
const gs=document.getElementById('gsearch');if(gs)gs.oninput=()=>renderGloss(gs.value);

// ---- equity calculator (validated 7-card evaluator, ported from build_equity.py) ----
const EB=16, EBASE=Math.pow(EB,5);
const ESTR=[]; for(let hi=12;hi>=4;hi--){const idx=[];for(let r=hi-4;r<=hi;r++)idx.push(r);ESTR.push([hi,idx]);} ESTR.push([3,[12,0,1,2,3]]);
const CATS_JA=['ハイカード','ワンペア','ツーペア','スリーカード','ストレート','フラッシュ','フルハウス','フォーカード','ストレートフラッシュ'];
const CATS_EN=['High Card','Pair','Two Pair','Three of a Kind','Straight','Flush','Full House','Four of a Kind','Straight Flush'];
let catLang='ja';
function catName(i){return (catLang==='en'?CATS_EN:CATS_JA)[i];}
const SUITSYM=['♠','♥','♦','♣'], SUITCOL=['#26303c','#d6455d','#2f7fe0','#2fae66'];
const RKS='23456789TJQKA';
function straightHigh(pres){for(let q=0;q<ESTR.length;q++){const idx=ESTR[q][1];let ok=true;for(let z=0;z<idx.length;z++)if(!pres[idx[z]]){ok=false;break;}if(ok)return ESTR[q][0];}return -1;}
function topk(pres,k){const a=pres.slice();const out=[];for(let t=0;t<k;t++){let hi=-1;for(let r=12;r>=0;r--){if(a[r]){hi=r;break;}}if(hi>=0){out.push(hi);a[hi]=false;}else out.push(0);}return out;}
function evaluate7(cards){
  const rc=new Array(13).fill(0), sc=new Array(4).fill(0);
  const sp=[new Array(13).fill(false),new Array(13).fill(false),new Array(13).fill(false),new Array(13).fill(false)];
  for(let q=0;q<cards.length;q++){const c=cards[q],r=(c/4)|0,s=c%4;rc[r]++;sc[s]++;sp[s][r]=true;}
  const pres=rc.map(x=>x>0);
  let fsu=0;for(let s=1;s<4;s++)if(sc[s]>sc[fsu])fsu=s;
  const isFlush=sc[fsu]>=5, straight_h=straightHigh(pres), sf=isFlush?straightHigh(sp[fsu]):-1;
  let has4=false,quad=-1,topTrip=-1,secTrip=-1,topPair=-1,nTrip=0,nPair=0;
  for(let r=12;r>=0;r--){ if(rc[r]===4){has4=true;if(quad<0)quad=r;} else if(rc[r]===3){nTrip++;if(topTrip<0)topTrip=r;else if(secTrip<0)secTrip=r;} else if(rc[r]===2){nPair++;if(topPair<0)topPair=r;} }
  const P4=Math.pow(EB,4),P3=Math.pow(EB,3),P2=EB*EB;
  const hc=topk(pres,5); let score=hc[0]*P4+hc[1]*P3+hc[2]*P2+hc[3]*EB+hc[4];
  if(nPair>=1){const p2=pres.slice();p2[topPair]=false;const ok=topk(p2,3);const c=1*EBASE+topPair*P4+ok[0]*P3+ok[1]*P2+ok[2]*EB;if(c>score)score=c;}
  if(nPair>=2){const ps=topk(rc.map(x=>x===2),2);const p2=pres.slice();p2[ps[0]]=false;p2[ps[1]]=false;const k=topk(p2,1)[0];const c=2*EBASE+ps[0]*P4+ps[1]*P3+k*P2;if(c>score)score=c;}
  if(nTrip>=1){const p2=pres.slice();p2[topTrip]=false;const tk=topk(p2,2);const c=3*EBASE+topTrip*P4+tk[0]*P3+tk[1]*P2;if(c>score)score=c;}
  if(straight_h>=0){const c=4*EBASE+straight_h*P4;if(c>score)score=c;}
  if(isFlush){const ft=topk(sp[fsu],5);const c=5*EBASE+ft[0]*P4+ft[1]*P3+ft[2]*P2+ft[3]*EB+ft[4];if(c>score)score=c;}
  if(nTrip>=1&&(nTrip>=2||nPair>=1)){const fhP=Math.max(secTrip,topPair);const c=6*EBASE+topTrip*P4+fhP*P3;if(c>score)score=c;}
  if(has4){const p2=pres.slice();p2[quad]=false;const qk=topk(p2,1)[0];const c=7*EBASE+quad*P4+qk*P3;if(c>score)score=c;}
  if(sf>=0){const c=8*EBASE+sf*P4;if(c>score)score=c;}
  return score;
}
function computeEquity(hands,board){
  const used={};board.forEach(c=>used[c]=1);hands.forEach(h=>h.forEach(c=>used[c]=1));
  const deck=[];for(let c=0;c<52;c++)if(!used[c])deck.push(c);
  const N=hands.length,need=5-board.length;
  const wins=new Array(N).fill(0),cat=hands.map(()=>new Array(9).fill(0));let tot=0;
  function settle(full){let best=-1,who=[];const cs=new Array(N);for(let i=0;i<N;i++){const s=evaluate7(hands[i].concat(full));cs[i]=(s/EBASE)|0;if(s>best){best=s;who=[i];}else if(s===best)who.push(i);}tot++;const sh=1/who.length;for(let z=0;z<who.length;z++){wins[who[z]]+=sh;cat[who[z]][cs[who[z]]]++;}}
  if(need<=0)settle(board);
  else if(need===1){for(let a=0;a<deck.length;a++)settle(board.concat([deck[a]]));}
  else if(need===2){for(let a=0;a<deck.length;a++)for(let b=a+1;b<deck.length;b++)settle(board.concat([deck[a],deck[b]]));}
  else{const iters=N<=2?120000:N<=4?60000:30000,D=deck.length;for(let t=0;t<iters;t++){const dd=deck.slice(),pk=[];for(let x=0;x<need;x++){const r=(Math.random()*(D-x))|0;pk.push(dd[r]);dd[r]=dd[D-1-x];}settle(board.concat(pk));}}
  return hands.map((h,i)=>{const c=cat[i],top=c.map((v,k)=>[v,k]).filter(a=>a[0]>0).sort((a,b)=>b[0]-a[0]).slice(0,3).map(a=>a[1]);return {equity:wins[i]/tot*100,cats:top,exact:need<=2};});
}
// ---- calculator: ranges, equity (hand/range), details ----
const DISP='AKQJT98765432';
function cardFace(c){const r=RKS[(c/4)|0],s=c%4,R=r==='T'?'10':r;return '<div class="ccard" style="color:'+SUITCOL[s]+'"><span class="rk">'+R+'</span><span class="st">'+SUITSYM[s]+'</span></div>';}
function pcardText1(c){return (RKS[(c/4)|0]==='T'?'10':RKS[(c/4)|0])+SUITSYM[c%4];}
function pcardText(cards){return cards.map(c=>c==null?'?':pcardText1(c)).join(' ');}
function rangeName(i,j){const a=DISP[i],b=DISP[j];return i===j?a+a:(i<j?a+b+'s':b+a+'o');}
function classCombos(name){
  if(name.length===2){const r=RKS.indexOf(name[0]);const out=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)out.push([r*4+a,r*4+b]);return out;}
  const hi=RKS.indexOf(name[0]),lo=RKS.indexOf(name[1]),out=[];
  if(name[2]==='s'){for(let s=0;s<4;s++)out.push([hi*4+s,lo*4+s]);}
  else{for(let a=0;a<4;a++)for(let b=0;b<4;b++)if(a!==b)out.push([hi*4+a,lo*4+b]);}
  return out;
}
function rangeComboCount(rng){let n=0;for(const k in rng)if(rng[k])n+=(k.length===2?6:(k[2]==='s'?4:12));return n;}
function expandRange(rng,dead){const out=[];for(const k in rng){if(!rng[k])continue;const cs=classCombos(k);for(let z=0;z<cs.length;z++)if(!dead[cs[z][0]]&&!dead[cs[z][1]])out.push(cs[z]);}return out;}
function computeEquityRange(specs,board){
  const N=specs.length,need=5-board.length;
  const gdead={};board.forEach(c=>gdead[c]=1);specs.forEach(s=>{if(s.type==='hand')s.cards.forEach(c=>gdead[c]=1);});
  const rc=specs.map(s=>s.type==='range'?expandRange(s.range,gdead):null);
  for(let i=0;i<N;i++)if(specs[i].type==='range'&&rc[i].length===0)return null;
  const iters=N<=2?150000:N<=4?70000:35000;
  const wins=new Array(N).fill(0),cat=specs.map(()=>new Array(9).fill(0));let valid=0;
  for(let t=0;t<iters;t++){
    const used={};for(const c in gdead)used[c]=1;
    const hole=new Array(N);let ok=true;
    for(let i=0;i<N;i++){
      if(specs[i].type==='hand')hole[i]=specs[i].cards;
      else{const cl=rc[i];let pk=null;for(let tr=0;tr<12;tr++){const cc=cl[(Math.random()*cl.length)|0];if(!used[cc[0]]&&!used[cc[1]]){pk=cc;break;}}if(!pk){ok=false;break;}hole[i]=pk;used[pk[0]]=1;used[pk[1]]=1;}
    }
    if(!ok)continue;
    const deck=[];for(let c=0;c<52;c++)if(!used[c])deck.push(c);
    const D=deck.length,pk=[];for(let x=0;x<need;x++){const r=(Math.random()*(D-x))|0;pk.push(deck[r]);deck[r]=deck[D-1-x];}
    const full=board.concat(pk);
    let best=-1,who=[];const cs=new Array(N);
    for(let i=0;i<N;i++){const sc=evaluate7(hole[i].concat(full));cs[i]=(sc/EBASE)|0;if(sc>best){best=sc;who=[i];}else if(sc===best)who.push(i);}
    valid++;const sh=1/who.length;for(let z=0;z<who.length;z++){wins[who[z]]+=sh;cat[who[z]][cs[who[z]]]++;}
  }
  if(!valid)return null;
  return specs.map((s,i)=>{const c=cat[i],top=c.map((v,k)=>[v,k]).filter(a=>a[0]>0).sort((a,b)=>b[0]-a[0]).slice(0,3).map(a=>a[1]);return{equity:wins[i]/valid*100,cats:top,exact:false};});
}
function handDetails(pi){
  const me=cPlayers[pi];if(me.mode!=='hand'||me.cards[0]==null||me.cards[1]==null)return null;
  const bd=cBoard.filter(c=>c!=null),dead={};bd.forEach(c=>dead[c]=1);me.cards.forEach(c=>dead[c]=1);
  cPlayers.forEach((p,j)=>{if(j!==pi&&p.mode==='hand')p.cards.forEach(c=>{if(c!=null)dead[c]=1;});});
  const deck=[];for(let c=0;c<52;c++)if(!dead[c])deck.push(c);
  const need=5-bd.length,dist=new Array(9).fill(0);let tot=0;
  const add=full=>{dist[(evaluate7(me.cards.concat(full))/EBASE)|0]++;tot++;};
  if(need<=0)add(bd);
  else if(need===1){for(let a=0;a<deck.length;a++)add(bd.concat([deck[a]]));}
  else if(need===2){for(let a=0;a<deck.length;a++)for(let b=a+1;b<deck.length;b++)add(bd.concat([deck[a],deck[b]]));}
  else{const it=40000,D=deck.length;for(let t=0;t<it;t++){const dd=deck.slice(),pk=[];for(let x=0;x<need;x++){const r=(Math.random()*(D-x))|0;pk.push(dd[r]);dd[r]=dd[D-1-x];}add(bd.concat(pk));}}
  const distPct=dist.map(v=>v/tot*100);
  let outs=null;
  if(bd.length===3||bd.length===4){
    const opps=[];cPlayers.forEach((p,j)=>{if(j!==pi&&p.mode==='hand'&&p.cards[0]!=null&&p.cards[1]!=null)opps.push(p.cards);});
    if(opps.length>=1){
      const stand=extra=>{const full=bd.concat(extra),my=evaluate7(me.cards.concat(full));let lead=true,tie=false;for(let z=0;z<opps.length;z++){const os=evaluate7(opps[z].concat(full));if(os>my){lead=false;break;}if(os===my)tie=true;}return lead?(tie?'tie':'win'):'lose';};
      const now=stand([]);let cnt=0;const oc=[];
      if(now!=='win'){for(let a=0;a<deck.length;a++){const st=stand([deck[a]]);if(st==='win'||st==='tie'){cnt++;oc.push(deck[a]);}}}
      outs={now,count:cnt,cards:oc.slice(0,18)};
    }
  }
  return {dist:distPct,outs};
}
// ---- state + render ----
let cBoard=[null,null,null,null,null];
let cPlayers=[{mode:'hand',cards:[null,null],range:{}},{mode:'hand',cards:[null,null],range:{}}];
let activeSlot=null, rangeEditPi=null;
function newPlayer(){return {mode:'hand',cards:[null,null],range:{}};}
function usedCards(except){const u={};cBoard.forEach(c=>{if(c!=null)u[c]=1;});cPlayers.forEach(p=>{if(p.mode==='hand')p.cards.forEach(c=>{if(c!=null)u[c]=1;});});if(except!=null)delete u[except];return u;}
function calcResults(){const specs=[],idx=[];
  cPlayers.forEach((p,pi)=>{if(p.mode==='range'){if(rangeComboCount(p.range)>0){specs.push({type:'range',range:p.range});idx.push(pi);}}else if(p.cards[0]!=null&&p.cards[1]!=null){specs.push({type:'hand',cards:p.cards.slice()});idx.push(pi);}});
  const out={};if(specs.length<2)return out;
  const bd=cBoard.filter(c=>c!=null),allHand=specs.every(s=>s.type==='hand');
  const r=allHand?computeEquity(specs.map(s=>s.cards),bd):computeEquityRange(specs,bd);
  if(r)idx.forEach((pi,k)=>out[pi]=r[k]);return out;}
function renderCalc(){
  let bh='';cBoard.forEach((c,i)=>{bh+='<div class="cslot'+(c!=null?' filled':'')+'" data-b="'+i+'">'+(c!=null?cardFace(c):'')+'</div>';});
  document.getElementById('cboard').innerHTML=bh;
  const res=calcResults();let ph='';
  cPlayers.forEach((p,pi)=>{
    let hand;
    if(p.mode==='range')hand='<div class="ph"><button class="qmini" data-redit="'+pi+'">レンジ編集</button> <span class="cats">'+rangeComboCount(p.range)+' combos</span></div>';
    else{let slots='';p.cards.forEach((c,ci)=>{slots+='<div class="pslot'+(c!=null?' filled':'')+'" data-p="'+pi+'" data-c="'+ci+'">'+(c!=null?cardFace(c):'')+'</div>';});hand='<div class="ph">'+slots+'</div>';}
    const r=res[pi];let info;
    if(r){const ip=Math.floor(r.equity),dp=(r.equity-ip).toFixed(2).slice(2);const wl=catLang==='en'?'wins by ':'勝ち筋: ',sep=catLang==='en'?', ':'、';
      info='<div class="eq">'+ip+'<small>.'+dp+'% equity'+(r.exact?'':' 〜近似')+'</small></div><div class="cats">'+(r.cats.length?(wl+r.cats.map(catName).join(sep)):'')+'</div>';}
    else info='<div class="cats" style="font-size:12px">（ハンド/レンジを設定）</div>';
    const mode='<button class="qmini" data-mode="'+pi+'">'+(p.mode==='range'?'ハンド':'レンジ')+'</button>';
    const det=(p.mode==='hand'&&p.cards[0]!=null&&p.cards[1]!=null)?'<button class="rm" data-det="'+pi+'">詳細</button>':'';
    ph+='<div class="prow">'+hand+'<div style="flex:1;min-width:120px">'+info+'</div>'+mode+det+'<button class="rm" data-clr="'+pi+'">クリア</button><button class="rm" data-rm="'+pi+'">✕</button></div>';});
  document.getElementById('players').innerHTML=ph;
  document.querySelectorAll('#cboard .cslot').forEach(el=>el.onclick=()=>openPicker({t:'b',i:+el.getAttribute('data-b')}));
  document.querySelectorAll('#players .pslot').forEach(el=>el.onclick=()=>openPicker({t:'p',pi:+el.getAttribute('data-p'),ci:+el.getAttribute('data-c')}));
  document.querySelectorAll('#players [data-mode]').forEach(el=>el.onclick=()=>{const i=+el.getAttribute('data-mode');cPlayers[i].mode=cPlayers[i].mode==='range'?'hand':'range';renderCalc();});
  document.querySelectorAll('#players [data-redit]').forEach(el=>el.onclick=()=>openRangeEd(+el.getAttribute('data-redit')));
  document.querySelectorAll('#players [data-det]').forEach(el=>el.onclick=()=>openDetails(+el.getAttribute('data-det')));
  document.querySelectorAll('#players [data-clr]').forEach(el=>el.onclick=()=>{const i=+el.getAttribute('data-clr');cPlayers[i].cards=[null,null];cPlayers[i].range={};renderCalc();});
  document.querySelectorAll('#players [data-rm]').forEach(el=>el.onclick=()=>{if(cPlayers.length>1){cPlayers.splice(+el.getAttribute('data-rm'),1);renderCalc();}});
}
function curCardOf(s){return s.t==='b'?cBoard[s.i]:cPlayers[s.pi].cards[s.ci];}
function setCard(s,c){if(s.t==='b')cBoard[s.i]=c;else cPlayers[s.pi].cards[s.ci]=c;}
function openPicker(slot){activeSlot=slot;const u=usedCards(curCardOf(slot));
  let h='<div class="pickbar"><b>カードを選択</b><span><button class="qmini" id="pkClear">空にする</button> <button class="qmini" id="pkClose">閉じる</button></span></div><div class="pickgrid">';
  const ranks=[12,11,10,9,8,7,6,5,4,3,2,1,0];
  for(let s=0;s<4;s++)for(let z=0;z<ranks.length;z++){const r=ranks[z],c=r*4+s,R=RKS[r]==='T'?'10':RKS[r];h+='<div class="pcard'+(u[c]?' used':'')+'" data-c="'+c+'" style="color:'+SUITCOL[s]+'">'+R+SUITSYM[s]+'</div>';}
  h+='</div>';
  document.getElementById('pickbox').innerHTML=h;document.getElementById('picker').classList.add('on');
  document.getElementById('pkClose').onclick=closePicker;
  document.getElementById('pkClear').onclick=()=>{setCard(activeSlot,null);closePicker();renderCalc();};
  document.querySelectorAll('#pickbox .pcard:not(.used)').forEach(el=>el.onclick=()=>{setCard(activeSlot,+el.getAttribute('data-c'));closePicker();renderCalc();});
}
function closePicker(){document.getElementById('picker').classList.remove('on');}
// ---- range editor ----
function openRangeEd(pi){rangeEditPi=pi;renderRangeEd();document.getElementById('rangeed').classList.add('on');}
function closeRangeEd(){document.getElementById('rangeed').classList.remove('on');renderCalc();}
function rangePreset(pi,kind){const r=cPlayers[pi].range;if(kind==='clear'){cPlayers[pi].range={};return;}
  for(let i=0;i<13;i++)for(let j=0;j<13;j++){const nm=rangeName(i,j);
    if(kind==='all')r[nm]=1;else if(kind==='pairs'){if(i===j)r[nm]=1;}else if(kind==='bway'){if('AKQJT'.indexOf(DISP[i])>=0&&'AKQJT'.indexOf(DISP[j])>=0)r[nm]=1;}}}
function renderRangeEd(){const r=cPlayers[rangeEditPi].range;
  let h='<div class="pickbar"><b>レンジ選択（'+rangeComboCount(r)+' combos）</b><span><button class="qmini" data-rp="all">全</button><button class="qmini" data-rp="pairs">ペア</button><button class="qmini" data-rp="bway">BW</button><button class="qmini" data-rp="clear">クリア</button><button class="qmini" id="reClose">閉じる</button></span></div><div class="rgrid">';
  for(let i=0;i<13;i++)for(let j=0;j<13;j++){const nm=rangeName(i,j);h+='<div class="rcell'+(r[nm]?' ron':'')+'" data-rn="'+nm+'">'+nm+'</div>';}
  h+='</div>';
  document.getElementById('rangeedbox').innerHTML=h;
  document.getElementById('reClose').onclick=closeRangeEd;
  document.querySelectorAll('#rangeedbox .rcell').forEach(el=>el.onclick=()=>{const nm=el.getAttribute('data-rn');r[nm]=r[nm]?0:1;renderRangeEd();});
  document.querySelectorAll('#rangeedbox [data-rp]').forEach(el=>el.onclick=()=>{rangePreset(rangeEditPi,el.getAttribute('data-rp'));renderRangeEd();});
}
// ---- details (made-hand distribution + outs) ----
function openDetails(pi){const d=handDetails(pi),me=cPlayers[pi];
  let h='<div class="pickbar"><b>'+pcardText(me.cards)+' の詳細</b><button class="qmini" id="dtClose">閉じる</button></div>';
  if(!d)h+='<div>ハンドを2枚設定してください。</div>';
  else{h+='<div style="margin:4px 0;font-size:13px;color:var(--mut)">役の内訳（リバーまで）</div><div style="font-size:12.5px">';
    [8,7,6,5,4,3,2,1,0].forEach(k=>{if(d.dist[k]>0.05)h+='<div style="display:flex;justify-content:space-between;gap:20px;padding:1px 0"><span>'+catName(k)+'</span><b>'+d.dist[k].toFixed(1)+'%</b></div>';});
    h+='</div>';
    if(d.outs){h+='<div style="margin:10px 0 4px;font-size:13px;color:var(--mut)">アウツ（次の1枚）</div>';
      if(d.outs.now==='win')h+='<div class="cats">現在リード（最強ハンド）。</div>';
      else h+='<div class="cats">次の1枚で最良になる: <b style="color:var(--ca)">'+d.outs.count+'枚</b>'+(d.outs.cards.length?'<br>'+d.outs.cards.map(pcardText1).join(' '):'')+'</div>';}
  }
  document.getElementById('detbox').innerHTML=h;document.getElementById('details').classList.add('on');
  document.getElementById('dtClose').onclick=closeDetails;
}
function closeDetails(){document.getElementById('details').classList.remove('on');}
// ---- controls ----
function resetCalc(){cBoard=[null,null,null,null,null];cPlayers=[newPlayer(),newPlayer()];closePicker();renderCalc();}
function clearBoard(){cBoard=[null,null,null,null,null];renderCalc();}
function randomDeal(){const u=usedCards(null);const avail=[];for(let c=0;c<52;c++)if(!u[c])avail.push(c);
  for(let i=avail.length-1;i>0;i--){const j=(Math.random()*(i+1))|0;const t=avail[i];avail[i]=avail[j];avail[j]=t;}
  let k=0;cPlayers.forEach(p=>{if(p.mode==='hand')for(let ci=0;ci<2;ci++)if(p.cards[ci]==null&&k<avail.length)p.cards[ci]=avail[k++];});renderCalc();}
function toggleCatLang(){catLang=catLang==='en'?'ja':'en';document.getElementById('catLang').textContent=catLang==='en'?'日本語':'EN';renderCalc();}

// ---- tabs ----
function showView(v){
  [['tabChart','chart'],['tabQuiz','quiz'],['tabGloss','gloss'],['tabCalc','calc'],['tabHowto','howto']].forEach(([id,name])=>document.getElementById(id).classList.toggle('on',v===name));
  document.getElementById('chartView').style.display=v==='chart'?'flex':'none';
  document.getElementById('quiz').classList.toggle('on',v==='quiz');
  document.getElementById('gloss').classList.toggle('on',v==='gloss');
  document.getElementById('calc').classList.toggle('on',v==='calc');
  document.getElementById('howto').classList.toggle('on',v==='howto');
  if(v==='quiz'){qmode==='strat'?pickQuiz():qmode==='term'?pickTermQuiz():qmode==='post'?pickPost():pickSrp();}
  if(v==='gloss')renderGloss(gs?gs.value:'');
  if(v==='calc')renderCalc();
}
document.getElementById('tabChart').onclick=()=>showView('chart');
document.getElementById('tabQuiz').onclick=()=>showView('quiz');
document.getElementById('tabGloss').onclick=()=>showView('gloss');
document.getElementById('tabCalc').onclick=()=>showView('calc');
document.getElementById('tabHowto').onclick=()=>showView('howto');
document.getElementById('addPlayer').onclick=()=>{if(cPlayers.length<10){cPlayers.push(newPlayer());renderCalc();}};
document.getElementById('calcReset').onclick=resetCalc;
document.getElementById('clearBoard').onclick=clearBoard;
document.getElementById('randomDeal').onclick=randomDeal;
document.getElementById('catLang').onclick=toggleCatLang;
document.getElementById('qnext').onclick=pickQuiz;
document.getElementById('tnext').onclick=pickTermQuiz;
document.getElementById('qmStrat').onclick=()=>setQMode('strat');
document.getElementById('qmTerm').onclick=()=>setQMode('term');
document.getElementById('qmPost').onclick=()=>setQMode('post');
document.getElementById('qmSrp').onclick=()=>setQMode('srp');
document.getElementById('pqnext').onclick=pickPost;
document.getElementById('srpnext').onclick=pickSrp;
document.getElementById('qscope').onchange=pickQuiz;
document.getElementById('qstack').onchange=pickQuiz;
document.getElementById('qreview').onclick=()=>{reviewMode=!reviewMode;document.getElementById('qreview').classList.toggle('on',reviewMode);pickQuiz();};
document.getElementById('qclear').onclick=()=>{missed=[];saveMissed();updMissedUI();};
document.getElementById('qChartBtn').onclick=toggleQuizChart;
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&document.getElementById('quiz').classList.contains('on')){qmode==='strat'?pickQuiz():qmode==='term'?pickTermQuiz():qmode==='post'?pickPost():pickSrp();}});
document.addEventListener('click',e=>{const el=e.target.closest('.gl');if(el&&el.dataset.go)gotoGloss(el.dataset.go);});
cfgSel.onchange=()=>{fillSpots();renderGrid();};
spotSel.onchange=renderGrid;
fillSpots();renderGrid();updScore();updMissedUI();
</script></body></html>"""

out = HTML.replace("__PAYLOAD__", PAYLOAD).replace("__GLOSSARY__", GLOSSARY).replace("__SRP__", SRP_JSON).replace("__SRP2__", SRP2_JSON)
open(os.path.join(BASE, "index.html"), "w").write(out)
print("WROTE", os.path.join(BASE, "index.html"), f"({len(out)} bytes)")
