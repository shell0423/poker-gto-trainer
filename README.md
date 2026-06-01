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

**全257チャート / 8構成（EDGE POKER対応）。** EDGEの優勝システムは `EDGE_SYSTEM.md` 参照。

| 構成 | 内容 | 精度 |
|---|---|---|
| **★EDGE Push/Fold (Nash, +1bb ante)** | EDGEの 4-max/6-max/HU 短スタック jam＋call（102）＋EV | **厳密（自前ソルバー・1bbアンティ）** |
| **EDGE 4-max 40bb +ante** | EDGE序盤の4-max RFI/3bet/守備（10） | 近似 |
| **6-max 100bb cash** | RFI・BB守備・3bet/フラット・4bet/call/fold（20スポット） | 近似（学習用） |
| **HU Push/Fold (exact Nash)** | ヘッズアップ jam/call（8スタック×2＝16）＋EV | **厳密（自前計算）** |
| **First-in Push/Fold (6-max, Nash)** | アンオープン jam＋SB/BB call（UTG/HJ/CO/BTN×8-20bb、60）＋EV | **厳密（自前マルチウェイ・ソルバー）** |
| **50bb / Full-ring 9-max / MTT 40bb+ante** | 追加コンフィグ（各〜18スポット、49） | 近似（学習用） |

- 色: 🔴 Open/3bet/4bet/Jam ・ 🟢 Call ・ 🔵 Fold（マスは頻度で比例分割）。Nash構成は各ハンドの **EV** も表示。
- **チャート**タブ: クリックで内訳＋理由解説。解説文の専門用語は用語集へホバーリンク
- **クイズ**タブ: 戦略クイズ（回答後に理由解説）＋用語クイズ（定義↔用語の4択）、正答率を記録
- **用語集**タブ: ポーカー用語 257語/9カテゴリ。検索、関連語ジャンプ、「📊チャートで見る」で該当スポットへ
- **計算機**タブ: ボード＋各プレイヤーのハンド or **レンジ**を設定してエクイティ（勝率）を計算（Equilab/PokerStove相当、四色デッキ）。**ハンド/レンジ自由切替・レンジvsレンジ**、各プレイヤーの**詳細（役の内訳・アウツ）**も表示。検証済み7枚評価器をJSに移植、フロップ以降は厳密・プリフロップ/レンジはMC近似

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
