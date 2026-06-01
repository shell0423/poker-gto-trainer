# 引き継ぎ書 — ポーカーGTOプリフロップ・トレーナー

最終更新: 2026-06-01 ／ 場所: `~/Claude/poker-gto/`

---

## 0. 30秒サマリー

ポーカーのプリフロップGTOレンジを **GTO Wizard風カラーグリッド**で閲覧・練習するローカルツール。
`index.html` をブラウザで開くだけで動く（自己完結HTML・データ埋め込み・サーバ不要）。

```bash
open ~/Claude/poker-gto/index.html
```

**現状: 当初4点＋拡張（理由解説・用語集・相互リンク・用語クイズ）＋§6拡張（マルチウェイNash・全構成展開・クイズ強化・EV表示）まで実装・稼働済み。** 残るは §6 の #5（本物のポストフロップ・ソルバー）のみ＝意図的に次回送り。
**Git: 初期化済み**（`~/Claude/poker-gto/` がリポジトリ。`.venv/`等は`.gitignore`済み。リモート未設定）。

---

## 1. 何が入っているか（257チャート / 8構成）

> **EDGE POKER（DeNA×世界のヨコサワの日本アプリ）対応**: 12人→4-max→決勝6人→HU、40bb・**1bb BBアンティ**・超ターボ。専用の push/fold（自前ソルバーをアンティ＋任意卓人数に拡張）＋序盤4-maxレンジ＋クイズ「EDGE POKER」出題範囲。優勝システムは **`EDGE_SYSTEM.md`** にチートシート化。

| 構成 | スポット | 精度 | 由来 |
|---|---|---|---|
| **★EDGE Push/Fold (Nash, +1bb ante)** | 102（4-max/6-max/HU の jam＋call × 8-20bb）＋EV | **厳密(自前ソルバー・1bbアンティ)** | 自前計算 |
| **EDGE 4-max 40bb +ante** | 10（4-max序盤 RFI/3bet/守備） | 近似 | 多エージェント生成 |
| 6-max 100bb cash | 20（RFI5・BB守備5・3bet/flat5・4bet/call/fold5） | 近似（学習用） | 多エージェント生成 |
| **HU Push/Fold (exact Nash)** | 16（jam/call × 8スタック）＋**EV表示** | **厳密** | 自前計算 |
| **First-in Push/Fold (6-max, Nash)** | 60（UTG/HJ/CO/BTN の jam＋SB/BB call × 8-20bb）＋**EV** | **厳密(自前マルチウェイ・ソルバー)** | 自前計算 |
| 50bb 6-max | 18（フル20スポット構成） | 近似 | 多エージェント生成 |
| Full-ring 9-max 100bb | 18（RFI8＋BB守備＋3bet/4bet） | 近似 | 多エージェント生成 |
| MTT 40bb +ante 6-max | 13（RFI＋守備＋3bet/4bet） | 近似 | 多エージェント生成 |

- ユーザーが最初に聞いた具体例「**BTN open vs SB 3bet の 4bet/call/fold**」は `6-max 100bb cash` に収録（タイトルに ★）。
- 色: 🔴 Open/3bet/4bet/Jam ・ 🟢 Call ・ 🔵 Fold をマス内で**頻度比例分割**。
- UI: 3タブ —「チャート」（クリックで内訳＋**理由解説**、解説文の専門用語は**用語集へホバーリンク**）／「クイズ」（**戦略クイズ**＝回答後に理由解説／**用語クイズ**＝定義↔用語の4択、正答率記録）／「**用語集**」（257語・9カテゴリ、検索、関連語ジャンプ、**「📊チャートで見る」で該当スポットへ**）。
- 相互リンク: 用語↔チャートを双方向接続（`TERM2CHART` マップ＋`annotate()` ホバーリンク engine）。
- 解説はクライアントJSの決定論エンジン（`build_site.py`内の `hinfo/handRole/spotKind/whyAction/explain`）。ハンドの役割×スポット種別×頻度から組み立て、全257チャート×169ハンドで動作。各スポットの全体解説(`notes`)も折りたたみ表示。
- **クイズ「EDGE POKER」出題範囲**（デフォルト）: config名が `EDGE` で始まる構成だけ出題（`pickQuiz`の`isEdge`）。EDGEで起きる局面（4-max序盤＋短スタックpush/fold）を集中ドリル。
- **EV表示**: Nash構成（HU・First-in）は各ハンドの jam/call の chipEV をチャート内訳・クイズに表示（`evLine()`）。データは `nash_*.py` が `ev`/`evFold` を出力。
- **クイズ強化**: 出題範囲（この構成/全構成/**EDGE**）・コンボ重み出題・復習モード（間違いを `localStorage` 保存して再出題）・**📊チャート**（出題中スポットの色分け表を右に表示）・**ポーカーテーブル風UI**（各席の行動＋手札カード）。
- **計算機タブ**（Equilab/PokerStove相当）: ボード＋各プレイヤーの**ハンド or レンジ**（13×13エディタ）を設定→**エクイティをブラウザ内で計算**。`build_site.py`内: `evaluate7`（numpy評価器のJS移植＝3000ハンドでPython完全一致）、`computeEquity`（全specific・≤2枚未知=厳密/他=MC）、`computeEquityRange`（ハンド/レンジ混在=MC・カードリムーバル）、`handDetails`（役の内訳＋アウツ）。検証(Python基準): QsJh/9s9h/8s7d on AsKs7c=39.65/44.19/16.17、AKs vs {AA,KK,QQ}=34.5/65.5、AKs vs {99+} on 2s7dTh=21.5/78.5、QsJh vs 99 on AsKs7c=10アウツ。`node test_init.js`に自己テスト入り。

---

## 2. 精度の区別（最重要・ユーザーに明示済み）

- **「近似」ラベル** = 公開ソルバーチャートに整合させた**学習用の近似値**。GTO Wizard等の厳密出力ではない。多エージェント・ワークフロー（生成→敵対的検証→整合性チェック）で作成。
- **「厳密Nash」ラベル（プッシュ/フォールドのみ）** = **自前計算の本物のチップEV Nash均衡**。
  - 純numpyの7枚ハンド評価器を実装 → 役判定を決定論ユニットテスト＋**全盤面の厳密列挙**で検証（`AKo vs QQ = 0.4284` が列挙とMCで一致）。
  - 169×169 プリフロップ全in エクイティ行列（Monte Carlo 4000/マッチアップ）。
  - fictitious play で SB(jam/fold) × BB(call/fold) の最適応答を平均化し均衡へ収束。
  - 簡略化: ICMなし（チップEV）、レンジ重みのカードリムーバル未モデル化（標準的簡略化）。
  - 健全性: jam% は 3bb=77.7% → 25bb=35.3% で単調減少、AA/KKは全スタックで jam。

---

## 3. ファイル構成

```
~/Claude/poker-gto/
├─ index.html               ← 生成物（ブラウザで開く。145チャート埋め込み）
├─ build_site.py            ← 全データを統合して index.html を生成（自己完結）
├─ build_equity.py          ← 169×169 エクイティ行列（numpy MC＋決定論検証）
├─ nash_pushfold.py         ← HU プッシュ/フォールド Nash（fictitious play、EV出力）
├─ nash_multiway.py         ← マルチウェイ first-in jam Nash（任意卓人数＋アンティ対応、EV出力）
├─ nash_edge.py             ← EDGE専用 push/fold（4-max/6-max/HU + 1bbアンティ）
├─ render_charts.py         ← 100bbチャートを Markdown リファレンス化
├─ preflop-charts-6max-100bb.md
├─ EDGE_SYSTEM.md           ← EDGE優勝システムのチートシート
├─ README.md / HANDOVER.md
├─ data/                    ← ★永続データ（build_site.py はここだけを読む）
│  ├─ charts_100bb.json     #  6-max 100bb cash 20スポット
│  ├─ charts_extra.json     #  full-ring/MTT/50bb 49スポット（マージ済み）
│  ├─ pushfold_nash.json    #  HU Nash 16チャート（ev付き）
│  ├─ pushfold_multiway.json#  First-in jam Nash 60チャート（ev付き）
│  ├─ pushfold_edge.json    #  EDGE push/fold 102チャート（+1bbアンティ, ev付き）
│  ├─ charts_edge_early.json#  EDGE 4-max 40bb 10スポット
│  ├─ equity.npy            #  エクイティ行列（再生成 ~2分）
│  ├─ classes.json / glossary.json / _combo_sample.json
└─ .venv/                   ← python3.13 + numpy 2.4.6
```

---

## 4. 再生成手順（完全に自己完結。ネット/ワークフロー不要）

```bash
cd ~/Claude/poker-gto
.venv/bin/python build_equity.py     # エクイティ行列 → data/equity.npy（~2分、初回/再計算時のみ）
.venv/bin/python nash_pushfold.py    # HU Nash → data/pushfold_nash.json（数秒）
.venv/bin/python nash_multiway.py    # First-in jam Nash → data/pushfold_multiway.json（~1分）
.venv/bin/python nash_edge.py        # EDGE push/fold(+1bbアンティ) → data/pushfold_edge.json（~1.5分）
.venv/bin/python build_site.py       # index.html 再生成（数秒）
open index.html
```

近似レンジ（`data/charts_100bb.json` / `charts_extra.json`）は多エージェント生成物を
永続化したもの。**作り直す場合のみ**ワークフロー再実行が必要（§5）。

---

## 5. 環境・ハマりどころ（次の人向け）

- **Python**: Homebrew の `python3.14` は expat リンク不整合で **pip が壊れている**（`eval7`等のインストール不可）。
  → `python3.13` で作った `~/Claude/poker-gto/.venv` を使うこと（numpy導入済み）。
- **`eval7` は使っていない**（ビルド失敗したため）。エクイティは純numpyの自作評価器。依存は numpy のみ。
- **近似レンジの再生成**: クラウドの多エージェント・ワークフローで作成。スクリプトはセッション配下に残存:
  - 6-max 100bb: `…/workflows/scripts/gto-preflop-charts-wf_538d05b8-a67.js`（return に `hands` を含める版に編集済み）
  - 追加コンフィグ: `…/workflows/scripts/gto-extra-configs-wf_c161e923-885.js`
  - 用語集: `…/workflows/scripts/poker-glossary-wf_84910281-125.js`（出力の `result.cats` を `data/glossary.json` に保存）
  - 全構成展開: `…/workflows/scripts/gto-configs-fullexpand-wf_d18b1c36-bae.js`（出力をキーで `data/charts_extra.json` にマージ＝新版優先）
  - 再実行したら、出力タスクファイルの `result.charts` を `data/charts_*.json` に保存/マージし直す（build_site.py が読むのは data/ のみ）。
- **マルチウェイNash（`nash_multiway.py`）**: 等スタック前提でサイドポットなし＝単一ポット勝者総取り。各後続が独立Nashコール域（オーバーコール相互作用は無視）。タイは近似（双方非勝利、~<2%）。chipEV（ICMなし）。fictitious play は事前サンプルした deal を再利用＝CRNで滑らか収束。`build_equity` の `evaluate` を流用。
- **データフロー**: `build_site.py` は `data/*.json` を読み、正規化して `__PAYLOAD__` に JSON 埋め込み → `index.html` 出力。グリッド/クイズは全てクライアントJS（バニラ）。
- **⚠️ 検証は必ず `node test_init.js`**（build_site.py の後）。`new Function(js)` の構文チェックだけでは**実行時エラーを見逃す**（過去に `const GLOSSARY` の TDZ＝初期化順序バグで全描画が停止した）。`test_init.js` は最小DOMスタブで init を**実行**し、グリッド169マス・スポット・クイズ・用語集の全経路を通す。トップレベルで使う `const` は使用箇所より前で宣言すること（特に `GLOSSARY` は先頭で宣言）。

---

## 6. 次回の候補タスク

**✅ 実装済み（このセッション）**: #1 マルチウェイ first-in jam Nash（`nash_multiway.py`）／#2 全構成展開（49スポット）／#3 クイズ強化（範囲フィルタ・コンボ重み・復習モード）／#4 EV表示（`evLine`/`nash_*.py`の`ev`出力）／理由解説・用語集・用語クイズ・相互リンク。

**残: #5 レンジ精度の底上げ（意図的に次回送り）**
- 近似ラベルのレンジを本物に置換するには、プリフロップ・ソルバー（ポストフロップを簡略モデル化 or flop subtree solve）を自前実装 or 既存OSS統合が必要。**単一セッションには過大**（postflopのモデル化が本質的に重い）。
- 着手指針: HU/マルチウェイの全in手法は postflop には使えない（all-inでないとエクイティ実現が要る）。OpenSpiel等のCFR + 簡略postflop、または PioSOLVER系のプリフロップ機能の出力取り込みが現実的。

**その他の拡張候補**
- マルチウェイNashを **vs-jam の overcall 相互作用** まで厳密化（現状は独立コール近似）／タイの厳密chop処理。
- First-in jam に **MTT/ICM** 版（チップEV→$EV）。`nash_multiway.py` の settlement に ICM を噛ませる。
- 用語クイズの **間違い復習**（戦略クイズと同様に `localStorage`）。
- スポット横断の **レンジ比較ビュー**（2スポットを並べて差分ハイライト）。

---

## 7. ユーザー文脈メモ

- 日本語でやり取り。ポーカーGTOの理解は明確（GTO/ミックス頻度/3bet・4bet の用語OK）。
- 「実装で」「全部」と言われたら**フル実装志向**（このセッションも4提案を全実装）。
- 関連メモ리: `memory/poker-gto-trainer.md`（プロジェクト概要）。
