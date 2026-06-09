# ♠ GTO Preflop Trainer

ポーカーのプリフロップGTO（近似）レンジを**GTO Wizard風の色分けグリッド**で閲覧・練習できるローカルツール。
`index.html` をブラウザで開くだけで動きます（自己完結・サーバ不要・データ埋め込み）。

## 🌐 公開ページ（友人に共有）

ブラウザでこのURLを開くだけで使えます（インストール不要）：

**https://shell0423.github.io/poker-gto-trainer/**

更新を反映するには、`build_site.py` で `index.html` を作り直したあと **`publish.command`** をダブルクリック（または `git add -A && git commit -m update && git push`）。GitHub Pagesが数十秒〜1分で再デプロイします。

## 起動方法（ローカル）

- **いちばん簡単**: **`GTO Trainer.app`** をダブルクリック（デスクトップにも配置済み。Dockにドラッグで常駐可）。
- ランチャーが無い/作り直したい時: **`make_launcher.command`** をダブルクリックすると `GTO Trainer.app` を再生成（パスは自動）。
- ターミナル派: `open index.html`

```bash
open index.html        # ブラウザで開く（ターミナル）
```

## 中身

**全409チャート / 10構成（EDGE POKER＋ポストフロップSRP対応）。** EDGEの優勝システムは `EDGE_SYSTEM.md` 参照。

| 構成 | 内容 | 精度 |
|---|---|---|
| **★EDGE Push/Fold (Nash, +1bb ante)** | EDGEの 4-max/6-max/HU 短スタック jam＋call（102）＋EV | **厳密（自前ソルバー・1bbアンティ）** |
| **EDGE 4-max 40bb +ante** | EDGE序盤の4-max RFI/3bet/守備（10） | 近似 |
| **6-max 100bb cash** | RFI・BB守備・3bet/フラット・4bet/call/fold（20スポット） | 近似（学習用） |
| **HU Push/Fold (exact Nash)** | ヘッズアップ jam/call（8スタック×2＝16）＋EV | **厳密（自前計算）** |
| **First-in Push/Fold (6-max, Nash)** | アンオープン jam＋SB/BB call（UTG/HJ/CO/BTN×8-20bb、60）＋EV | **厳密（自前マルチウェイ・ソルバー）** |
| **50bb / Full-ring 9-max / MTT 40bb+ante** | 追加コンフィグ（各〜18スポット、49） | 近似（学習用） |
| **BTN vs BB SRP・実戦 (2-street)** | フロップc-bet/BB守備（38盤）。**フロップ＋ターンを解きリバー=エクイティ** | 自前2ストリートCFR（c-bet頻度が実戦的） |
| **BTN vs BB SRP・詳細 (サイズ/CR)** | 小/大2サイズ＋BBチェックレイズ（38盤） | 自前単一ストリートCFR（c-betは控えめ） |

- 色: 🔴 Open/3bet/4bet/Jam ・ 🟢 Call ・ 🔵 Fold（マスは頻度で比例分割）。Nash構成は各ハンドの **EV** も表示。
- **チャート**タブ: クリックで内訳＋理由解説。解説文の専門用語は用語集へホバーリンク
- **クイズ**タブ: 戦略クイズ（回答後に理由解説）＋用語クイズ＋**ポストフロップ・クイズ**（フロップ/ターン/リバーで役・エクイティ・アウツ・ポットオッズを出題、全て厳密計算）＋**SRP戦略クイズ**（BTN vs BBのフロップで、BTNのc-bet＝実戦的2ストリート解【約200盤を網羅】／BBの守備＝コール/チェックレイズの混合戦略を出題、GTOミックスは寛容採点）、正答率を記録
- **用語集**タブ: ポーカー用語 257語/9カテゴリ。検索、関連語ジャンプ、「📊チャートで見る」で該当スポットへ
- **計算機**タブ: ボード＋各プレイヤーのハンド or **レンジ**を設定してエクイティ（勝率）を計算（Equilab/PokerStove相当、四色デッキ）。**ハンド/レンジ自由切替・レンジvsレンジ**、各プレイヤーの**詳細（役の内訳・アウツ）**も表示。検証済み7枚評価器をJSに移植、フロップ以降は厳密・プリフロップ/レンジはMC近似
- **使い方**タブ: 初心者向けガイド（各タブの意味・色の読み方・基本用語・最初の一歩）。クイズはテーブルに**スタック（bb＋チップ併記）とポット**を表示、**スタック深さフィルタ**（≤10bb等）で短スタック練習も可

## 精度について（重要）

- 「近似」ラベルのレンジは **公開ソルバーチャートに整合させた学習用の近似値**で、GTO Wizard等の厳密なソルバー出力ではありません。
- 「厳密Nash」ラベルのプッシュ/フォールドのみ、**自前のエクイティ計算＋fictitious playで計算した本物のチップEV Nash均衡**です（レンジ重みのカードリムーバルは未モデル化＝標準的簡略化）。

## ファイル構成と再生成

```
poker-gto/
├─ index.html                 # 生成物（ブラウザで開く）
├─ build_site.py              # 全データを統合してindex.htmlを生成
├─ build_equity.py            # 169×169 プリフロップ全in エクイティ行列（numpy MC、決定論検証つき）
├─ nash_pushfold.py           # HU プッシュ/フォールド Nash（fictitious play）
├─ solve_srp.py               # BTN vs BB SRP 単一ストリートCFR（2サイズ＋チェックレイズ）→ srp_flop.json
├─ solve_srp_turn.py          # BTN vs BB SRP 2ストリートCFR（flop+turn, river=equity）→ srp_turn.json
├─ render_charts.py           # 100bbチャートをMarkdownリファレンスに整形
├─ preflop-charts-6max-100bb.md
├─ data/
│  ├─ equity.npy              # エクイティ行列（厳密検証済み）
│  ├─ classes.json            # 169ハンドクラスの並び
│  └─ pushfold_nash.json      # Nash結果（16チャート）
└─ .venv/                     # numpy用（python3.13）
```

再生成:
```bash
.venv/bin/python build_equity.py     # エクイティ行列（~2分、初回のみ）
.venv/bin/python nash_pushfold.py    # Nash計算（数秒）
.venv/bin/python build_site.py       # index.html を再生成
```

近似レンジ（6-max 100bb／追加コンフィグ）は多エージェント・ワークフロー
（生成→敵対的検証→整合性チェック）で作成。クラウド側の生成物のため、
ローカル再生成は build_site.py がワークフロー出力JSONを読む構成です。

## 手法メモ

- **エクイティ**: 純numpyの7枚ハンド評価器（役判定を決定論ユニットテスト＋全盤面厳密列挙で検証。例: AKo vs QQ = 0.4284 が厳密列挙と一致）。各マッチアップ Monte Carlo 4000サンプル。
- **Nash**: HUブラインド対決。SB(ボタン)が jam/fold、BBが call/fold。fictitious play で双方の最適応答を平均化し均衡へ収束。チップEV（ICMなし）。
- 検証: jam% はスタックが深いほど単調減少（3bb 78% → 25bb 35%）、AA/KKは全スタックで jam。
- **ポストフロップ SRP ソルバー（自前 vector-CFR）**: BTN vs BB のシングルレイズドポット。レンジは自前のプリフロップ表から。
  - **単一ストリート版**（`solve_srp.py`）: フロップだけを解く木（BTN: チェック/小ベット/大ベット、BB: フォールド/コール/チェックレイズ、BTN: フォールド/コール）。終端はリバーまでのエクイティ。**サイズ選択とチェックレイズが見えるが、ターン以降の利益を含まないため c-bet 頻度は実戦より控えめ**。
  - **2ストリート版**（`solve_srp_turn.py`）: フロップ＋ターンを解き、リバーをエクイティで評価。ターンのチャンスノード（各ターン札、カードリムーバル）を持つ。**ターンの追撃（バレル）価値が入るため c-bet 頻度が実戦GTOに近い**（例: As7d2c で c-bet 38%→73%）。ベットは2/3ポット1サイズ、ターンのドンク/チェックレイズは簡略化。
  - 妥当性: ウェットな盤ほど BB の守備が広がり、チェックレイズも増える。乾いた A 高ではほぼ全レンジ c-bet。
  - **限界（正直に）**: 全1755フロップ・複数サイズ・リバーまでの完全多ストリート解は純Pythonでは計算量的に未対応（代表38盤に限定）。PioSOLVER 等の本格ソルバーの代替ではなく、傾向学習用。
