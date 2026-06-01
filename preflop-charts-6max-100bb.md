# プリフロップ GTO 近似レンジ表（6-max / 100bb / キャッシュ）

自動生成（生成→敵対的検証→整合性チェックの多エージェント構成）。学習用近似。

## 凡例 / Legend

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


---

## 目次

- **Open-Raise (RFI)**
  - UTG RFI — ~16%
  - MP (HJ) RFI — ~19%
  - CO RFI — ~28%
  - BTN RFI — ~45%
  - SB RFI (raise-or-fold) — ~43% (raise-or-fold)
- **BB Defense vs RFI**
  - BB vs UTG open — ~36% total defend (call ~28%, 3bet ~8%)
  - BB vs MP open — ~11% 3bet, plus wide flat defense (~45%+ total defense)
  - BB vs CO open — 3bet ~13%, flat ~45% (very wide defense)
  - BB vs BTN open — ~15% 3bet / defend ~62% total (call very wide)
  - BB vs SB open — ~3bet 16% / total defend ~78%+ (call extremely wide, fold only worst offsuit)
- **IP/SB vs RFI (3bet or flat)**
  - BTN vs CO open — ~9% 3bet, ~27% flat (call)
  - BTN vs UTG open — ~24-26% total continue (~7% 3bet, ~18% flat)
  - CO vs UTG open — ~7% 3bet (value-heavy + a few suited-blocker bluffs), ~5% flat
  - SB vs BTN open — ~14% 3bet, ~0% flat (3bet-or-fold)
  - SB vs CO open — ~10-11% 3bet (3bet-or-fold)
- **Facing 3bet (4bet / call / fold)**
  - BTN open vs SB 3bet  (★ your example) — BTN continues ~30-34% of its wide opening range vs the SB 3bet: roughly 6-8% pure 4bet (value + suited-ace bluffs) and ~24-27% flat. The rest folds.
  - BTN open vs BB 3bet — ~6-8% 4bet, ~28-34% call, rest fold
  - CO open vs BTN 3bet — 4bet ~5%, call ~8%, rest fold
  - UTG open vs BTN 3bet — 4bet ~5% / call ~6% of UTG opening range
  - SB open vs BB 3bet — 4bet ~7-9% of hands (value + bluffs); call ~7-9%; fold the rest. Out of the original ~40-45% SB open, the continuing range vs a 3bet is roughly 15-18%.


---

## Open-Raise (RFI)

### UTG RFI

**Range ≈ ~16%** ｜ Sizing: 2.3bb ｜ 主アクション: Open

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | R | R | R | R | R | R | R* | R* | R* | R | R* | R* | R* |
| **K** | R | R | R | R | R | R* |   |   |   |   |   |   |   |
| **Q** | R | R* | R | R | R | R* |   |   |   |   |   |   |   |
| **J** | R* | R* | R* | R | R | R* |   |   |   |   |   |   |   |
| **T** | R* |   |   |   | R | R | R* |   |   |   |   |   |   |
| **9** |   |   |   |   |   | R | R* |   |   |   |   |   |   |
| **8** |   |   |   |   |   |   | R | R* |   |   |   |   |   |
| **7** |   |   |   |   |   |   |   | R | R* |   |   |   |   |
| **6** |   |   |   |   |   |   |   |   | R | R* |   |   |   |
| **5** |   |   |   |   |   |   |   |   |   | R | R* |   |   |
| **4** |   |   |   |   |   |   |   |   |   |   | R* |   |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   | R* |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   | R* |

**Mixed:** A8s: Open 75% / fold 25% · A7s: Open 55% / fold 45% · A6s: Open 40% / fold 60% · A4s: Open 95% / fold 5% · A3s: Open 85% / fold 15% · A2s: Open 65% / fold 35% · K9s: Open 65% / fold 35% · KQo: Open 75% / fold 25% · Q9s: Open 55% / fold 45% · AJo: Open 90% / fold 10% · KJo: Open 15% / fold 85% · QJo: Open 10% / fold 90% · J9s: Open 75% / fold 25% · ATo: Open 20% / fold 80% · T8s: Open 50% / fold 50% · 98s: Open 75% / fold 25% · 87s: Open 70% / fold 30% · 76s: Open 60% / fold 40% · 65s: Open 45% / fold 55% · 54s: Open 35% / fold 45% · 44: Open 90% / fold 10% · 33: Open 65% / fold 35% · 22: Open 55% / fold 45%

> UTG RFI, tightest 6-max opening range (~16%, ~212 combos). RFI = raise or fold so callPct=0 throughout. Pure-raise core: 55+, AJs+, ATs, A9s, A5s, KTs+, QTs+, JTs, T9s, AQo+, KQs/KJs/QJs. Wheel aces (A5s-A2s) are the primary low-suited-ace block via nut blocker + straight equity, opened at higher freq than the equivalent middling aces (A8s-A6s). Small pairs taper (44 ~90%, 33 ~65%, 22 ~55%). Offsuit broadways below the AJo/KQo/AQo+ core (ATo, KJo, QJo) are low-frequency partial bluffs only. Suited connectors 54s-98s opened at moderate freq for board coverage, 76s+ the more solid block. 2.3bb sizing is standard for low/no-rake; 2.0-2.5bb is the common band with negligible range change.

### MP (HJ) RFI

**Range ≈ ~19%** ｜ Sizing: 2.3bb ｜ 主アクション: Open

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | R | R | R | R | R | R | R | R | R | R | R | R | R |
| **K** | R | R | R | R | R | R | R* | R* | R* | R* | R* |   |   |
| **Q** | R | R | R | R | R | R | R* | R* |   |   |   |   |   |
| **J** | R | R | R | R | R | R | R* | R* |   |   |   |   |   |
| **T** | R | R* | R* | R* | R | R | R | R* |   |   |   |   |   |
| **9** | R* | R* | R* | R* | R* | R | R | R* | R* |   |   |   |   |
| **8** | R* |   |   |   |   | R* | R | R | R* |   |   |   |   |
| **7** | R* |   |   |   |   |   |   | R | R | R* |   |   |   |
| **6** |   |   |   |   |   |   |   |   | R | R | R* |   |   |
| **5** | R* |   |   |   |   |   |   |   |   | R | R* | R* |   |
| **4** | R* |   |   |   |   |   |   |   |   |   | R* | R* |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   | R* |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   | R* |

**Mixed:** K8s: Open 85% / fold 15% · K7s: Open 65% / fold 35% · K6s: Open 55% / fold 45% · K5s: Open 45% / fold 55% · K4s: Open 30% / fold 70% · Q8s: Open 80% / fold 20% · Q7s: Open 40% / fold 60% · J8s: Open 90% / fold 10% · J7s: Open 45% / fold 55% · KTo: Open 95% / fold 5% · QTo: Open 90% / fold 10% · JTo: Open 90% / fold 10% · T7s: Open 70% / fold 30% · A9o: Open 80% / fold 20% · K9o: Open 40% / fold 60% · Q9o: Open 40% / fold 60% · J9o: Open 35% / fold 65% · T9o: Open 55% / fold 45% · 97s: Open 90% / fold 10% · 96s: Open 45% / fold 55% · A8o: Open 60% / fold 40% · 98o: Open 35% / fold 65% · 86s: Open 80% / fold 20% · A7o: Open 30% / fold 70% · 75s: Open 65% / fold 35% · 64s: Open 50% / fold 50% · A5o: Open 40% / fold 60% · 54s: Open 95% / fold 5% · 53s: Open 45% / fold 55% · A4o: Open 25% / fold 75% · 44: Open 95% / fold 5% · 43s: Open 30% / fold 70% · 33: Open 85% / fold 15% · 22: Open 75% / fold 25%

> MP/HJ open-or-fold at 6-max 100bb, 4 players behind, 2.3bb open. Total ~19% of combos. Pure opens: 55+, all broadways suited, all Axs (A2s-AKs), KQo/KJo, KQs-K9s, QJs-Q9s, JTs-J9s, T9s/T8s, 98s, 87s/76s/65s, 54s near-pure, AJo-AKo. Marginal mixes include small pairs 44-22, weak suited Kx (K8s-K4s), Qx/Jx gappers, suited gappers (T7s, 96s, 86s, 75s, 64s, 53s, 43s), A8o-A9o, A5o/A4o as offsuit blocker bluffs, KTo/QTo/JTo, T9o/98o. Wider than UTG via KJo+, A8o+, more suited gappers and connectors. callPct=0 throughout since this is an unopened pot (open-or-fold). Frequencies are approximate study-grade references aligned with published solver charts, not exact solver output.

### CO RFI

**Range ≈ ~28%** ｜ Sizing: 2.3bb ｜ 主アクション: Open

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | R | R | R | R | R | R | R | R | R | R | R | R | R |
| **K** | R | R | R | R | R | R | R* | R* | R* | R* | R* |   |   |
| **Q** | R | R | R | R | R | R | R* | R* | R* |   |   |   |   |
| **J** | R | R | R | R | R | R | R* | R* |   |   |   |   |   |
| **T** | R | R* | R* | R* | R | R | R | R* |   |   |   |   |   |
| **9** | R* | R* | R* | R* | R* | R | R | R* | R* |   |   |   |   |
| **8** | R* |   |   |   |   | R* | R | R | R* |   |   |   |   |
| **7** | R* |   |   |   |   |   |   | R | R | R* |   |   |   |
| **6** | R* |   |   |   |   |   |   |   | R | R | R* |   |   |
| **5** | R* |   |   |   |   |   |   |   |   | R | R* | R* |   |
| **4** | R* |   |   |   |   |   |   |   |   |   | R |   |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   | R |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   | R |

**Mixed:** K8s: Open 95% / fold 5% · K7s: Open 85% / fold 15% · K6s: Open 75% / fold 25% · K5s: Open 65% / fold 35% · K4s: Open 40% / fold 60% · Q8s: Open 90% / fold 10% · Q7s: Open 50% / fold 50% · Q6s: Open 40% / fold 60% · J8s: Open 90% / fold 10% · J7s: Open 45% / fold 55% · KTo: Open 95% / fold 5% · QTo: Open 90% / fold 10% · JTo: Open 90% / fold 10% · T7s: Open 80% / fold 20% · A9o: Open 80% / fold 20% · K9o: Open 40% / fold 60% · Q9o: Open 40% / fold 60% · J9o: Open 35% / fold 65% · T9o: Open 55% / fold 45% · 97s: Open 90% / fold 10% · 96s: Open 40% / fold 60% · A8o: Open 70% / fold 30% · 98o: Open 35% / fold 65% · 86s: Open 85% / fold 15% · A7o: Open 55% / fold 45% · 75s: Open 75% / fold 25% · A6o: Open 35% / fold 65% · 64s: Open 60% / fold 40% · A5o: Open 55% / fold 45% · 54s: Open 90% / fold 10% · 53s: Open 35% / fold 65% · A4o: Open 35% / fold 65%

> CO RFI open-or-fold (callPct=0 throughout). All pocket pairs 22-AA are pure opens from CO at this stack/format. All suited aces A2s-AKs pure. Offsuit aces taper: A9o-AKo strong, then A8o/A7o/A5o mixed, A6o/A4o thin blocker mixes. Suited kings K4s-KQs, suited queens Q6s-QJs, suited jacks J7s-JTs, plus suited connectors/one-gappers down to 53s/64s. Offsuit broadways KTo/QTo/JTo near-pure, K9o/Q9o/J9o/98o thin. Range lands ~28% combo-weighted, consistent with published CO 6-max 100bb RFI charts at 2.3bb.

### BTN RFI

**Range ≈ ~45%** ｜ Sizing: 2.2-2.5bb ｜ 主アクション: Open

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | R | R | R | R | R | R | R | R | R | R | R | R | R |
| **K** | R | R | R | R | R | R | R | R | R | R | R | R | R* |
| **Q** | R | R | R | R | R | R | R | R | R | R* | R* | R* | R* |
| **J** | R | R | R | R | R | R | R | R | R* | R* | R* |   |   |
| **T** | R | R | R | R | R | R | R | R | R* | R* |   |   |   |
| **9** | R | R* | R* | R* | R* | R | R | R | R* | R* |   |   |   |
| **8** | R | R* | R* | R* | R* | R* | R | R | R* | R* |   |   |   |
| **7** | R* | R* |   |   |   | R* | R* | R | R | R* | R* |   |   |
| **6** | R* |   |   |   |   |   |   | R* | R | R | R* |   |   |
| **5** | R* |   |   |   |   |   |   |   | R* | R | R | R* |   |
| **4** | R* |   |   |   |   |   |   |   |   |   | R | R* |   |
| **3** | R* |   |   |   |   |   |   |   |   |   |   | R |   |
| **2** | R* |   |   |   |   |   |   |   |   |   |   |   | R |

**Mixed:** K2s: Open 85% / fold 15% · Q5s: Open 90% / fold 10% · Q4s: Open 75% / fold 25% · Q3s: Open 55% / fold 45% · Q2s: Open 40% / fold 60% · J6s: Open 85% / fold 15% · J5s: Open 55% / fold 45% · J4s: Open 35% / fold 65% · T6s: Open 90% / fold 10% · T5s: Open 45% / fold 55% · K9o: Open 95% / fold 5% · Q9o: Open 90% / fold 10% · J9o: Open 90% / fold 10% · T9o: Open 95% / fold 5% · 96s: Open 80% / fold 20% · 95s: Open 40% / fold 60% · K8o: Open 75% / fold 25% · Q8o: Open 55% / fold 45% · J8o: Open 50% / fold 50% · T8o: Open 55% / fold 45% · 98o: Open 65% / fold 35% · 86s: Open 90% / fold 10% · 85s: Open 50% / fold 50% · A7o: Open 95% / fold 5% · K7o: Open 55% / fold 45% · 97o: Open 30% / fold 70% · 87o: Open 50% / fold 50% · 75s: Open 85% / fold 15% · 74s: Open 35% / fold 65% · A6o: Open 90% / fold 10% · 76o: Open 45% / fold 55% · 64s: Open 80% / fold 20% · A5o: Open 85% / fold 15% · 65o: Open 40% / fold 60% · 53s: Open 75% / fold 25% · A4o: Open 80% / fold 20% · 43s: Open 65% / fold 35% · A3o: Open 70% / fold 30% · A2o: Open 55% / fold 45%

> BTN RFI is open-or-fold (no flat), so callPct=0 everywhere; aggroPct=open frequency, foldPct=remainder. Premiums, all pairs, all suited aces, suited Broadways, and all strong connectors open at 100%. Suited-King and suited-Queen wings extended (K3s now 100%, K2s 85%, Q2s 40%) per standard ~45-48% BTN charts. Offsuit aces smoothed to be monotonic by kicker (A7o 95 > A6o 90 > A5o 85 > A4o 80 > A3o 70 > A2o 55) — the original had a wheel bias inflating A5o/A4o above A6o. Marginal offsuit gappers trimmed slightly. Weighted total = 600 combos = 45.2%, squarely within the 43-48% target. Small 2.2-2.5bb sizing exploiting positional edge over SB+BB.

### SB RFI (raise-or-fold)

**Range ≈ ~43% (raise-or-fold)** ｜ Sizing: 3bb ｜ 主アクション: Open

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | R | R | R | R | R | R | R | R | R | R | R | R | R |
| **K** | R | R | R | R | R | R | R | R | R | R* | R* | R* | R* |
| **Q** | R | R | R | R | R | R | R | R* | R* | R* | R* | R* | R* |
| **J** | R | R | R* | R | R | R | R* | R* | R* | R* |   |   |   |
| **T** | R | R* | R* | R* | R | R | R | R* | R* | R* |   |   |   |
| **9** | R | R* | R* | R* | R* | R | R | R* | R* | R* |   |   |   |
| **8** | R | R* | R* | R* | R* | R* | R | R | R* | R* | R* |   |   |
| **7** | R* | R* |   |   |   | R* | R* | R | R | R* | R* |   |   |
| **6** | R* |   |   |   |   |   | R* | R* | R | R | R* | R* |   |
| **5** | R* |   |   |   |   |   |   | R* | R* | R | R* | R* | R* |
| **4** | R* |   |   |   |   |   |   |   |   | R* | R | R* | R* |
| **3** | R* |   |   |   |   |   |   |   |   |   |   | R | R* |
| **2** | R* |   |   |   |   |   |   |   |   |   |   |   | R* |

**Mixed:** K5s: Open 95% / fold 5% · K4s: Open 90% / fold 10% · K3s: Open 85% / fold 15% · K2s: Open 75% / fold 25% · Q7s: Open 90% / fold 10% · Q6s: Open 80% / fold 20% · Q5s: Open 75% / fold 25% · Q4s: Open 65% / fold 35% · Q3s: Open 50% / fold 50% · Q2s: Open 40% / fold 60% · QJo: Open 95% / fold 5% · J8s: Open 95% / fold 5% · J7s: Open 80% / fold 20% · J6s: Open 50% / fold 50% · J5s: Open 35% / fold 65% · KTo: Open 95% / fold 5% · QTo: Open 85% / fold 15% · JTo: Open 85% / fold 15% · T7s: Open 90% / fold 10% · T6s: Open 65% / fold 35% · T5s: Open 35% / fold 65% · K9o: Open 70% / fold 30% · Q9o: Open 55% / fold 45% · J9o: Open 50% / fold 50% · T9o: Open 70% / fold 30% · 97s: Open 95% / fold 5% · 96s: Open 70% / fold 30% · 95s: Open 35% / fold 65% · K8o: Open 45% / fold 55% · Q8o: Open 30% / fold 70% · J8o: Open 30% / fold 70% · T8o: Open 45% / fold 55% · 98o: Open 55% / fold 45% · 86s: Open 90% / fold 10% · 85s: Open 60% / fold 40% · 84s: Open 30% / fold 70% · A7o: Open 90% / fold 10% · K7o: Open 30% / fold 70% · 97o: Open 30% / fold 70% · 87o: Open 45% / fold 55% · 75s: Open 85% / fold 15% · 74s: Open 45% / fold 55% · A6o: Open 80% / fold 20% · 86o: Open 25% / fold 75% · 76o: Open 40% / fold 60% · 64s: Open 75% / fold 25% · 63s: Open 35% / fold 65% · A5o: Open 95% / fold 5% · 75o: Open 20% / fold 80% · 65o: Open 35% / fold 65% · 54s: Open 95% / fold 5% · 53s: Open 70% / fold 30% · 52s: Open 30% / fold 70% · A4o: Open 85% / fold 15% · 54o: Open 30% / fold 70% · 43s: Open 75% / fold 25% · 42s: Open 30% / fold 70% · A3o: Open 75% / fold 25% · 32s: Open 35% / fold 65% · A2o: Open 60% / fold 40% · 22: Open 95% / fold 5%

> SB raise-or-fold (open-or-fold) vs BB at 100bb, ~43% of hands raised to 3bb. callPct is 0 by construction since SB cannot call its own open; every continued hand raises. With only the BB left to act, the SB plays this range a bit wider and more polarized at the bottom than a BTN open: all suited Kx down to K2s and all offsuit Ax are raised at high frequency for blocker/playability value, while weak offsuit Kx/Qx/Jx junk is the first to fold. Pocket pairs 33+ are pure raises and 22 is near-pure. IMPORTANT: in full GTO solutions vs a single BB, the SB's highest-EV strategy is actually a MIXED limp/raise (open-limp) construction, where SB limps a large portion of its range (strong traps plus many speculative hands) and raises a polar/value-leaning portion. This raise-or-fold simplification is a study-grade, easier-to-execute heuristic; it sacrifices a little EV versus the mixed-limp tree but is far simpler and avoids playing large limped pots OOP. The 3bb sizing is a common simplification; many solvers prefer a slightly larger SB open (e.g. 3-3.5bb) since there is only one player left to act.


---

## BB Defense vs RFI

### BB vs UTG open

**Range ≈ ~36% total defend (call ~28%, 3bet ~8%)** ｜ Sizing: 3bet to ~11bb ｜ 主アクション: 3bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 3 | 3 | 3* | C* | C* | C* | C* | C* | C* | C* | C* | C* | C* |
| **K** | 3 | 3 | C* | C* | C* | C* | C* | C* | C* | C* |   |   |   |
| **Q** | C* | C* | 3 | C* | C* | C* | C* |   |   |   |   |   |   |
| **J** | C* | C* | C* | 3* | C* | C* | C* |   |   |   |   |   |   |
| **T** | C* | C* | C* | C* | C* | C* | C* | C* |   |   |   |   |   |
| **9** | C* |   |   |   |   | C* | C* | C* |   |   |   |   |   |
| **8** |   |   |   |   |   |   | C* | C* | C* |   |   |   |   |
| **7** |   |   |   |   |   |   |   | C* | C* | C* |   |   |   |
| **6** |   |   |   |   |   |   |   |   | C | C* | C* |   |   |
| **5** |   |   |   |   |   |   |   |   |   | C | C* | C* |   |
| **4** |   |   |   |   |   |   |   |   |   |   | C* | C* |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   | C* |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   | C* |

**Mixed:** AQs: 3bet 55% / call 45% · AJs: 3bet 30% / call 70% · ATs: 3bet 15% / call 85% · A9s: 3bet 5% / call 95% · A8s: 3bet 5% / call 90% / fold 5% · A7s: 3bet 5% / call 85% / fold 10% · A6s: 3bet 10% / call 80% / fold 10% · A5s: 3bet 40% / call 58% / fold 2% · A4s: 3bet 35% / call 60% / fold 5% · A3s: 3bet 25% / call 65% / fold 10% · A2s: 3bet 15% / call 65% / fold 20% · KQs: 3bet 20% / call 80% · KJs: 3bet 20% / call 78% / fold 2% · KTs: 3bet 10% / call 85% / fold 5% · K9s: 3bet 5% / call 70% / fold 25% · K8s: call 45% / fold 55% · K7s: call 35% / fold 65% · K6s: call 20% / fold 80% · K5s: call 15% / fold 85% · AQo: 3bet 45% / call 52% / fold 3% · KQo: 3bet 15% / call 65% / fold 20% · QJs: 3bet 15% / call 83% / fold 2% · QTs: 3bet 10% / call 85% / fold 5% · Q9s: call 65% / fold 35% · Q8s: call 35% / fold 65% · AJo: 3bet 15% / call 70% / fold 15% · KJo: 3bet 5% / call 45% / fold 50% · QJo: call 40% / fold 60% · JJ: 3bet 55% / call 45% · JTs: 3bet 15% / call 83% / fold 2% · J9s: 3bet 5% / call 75% / fold 20% · J8s: call 40% / fold 60% · ATo: 3bet 5% / call 60% / fold 35% · KTo: call 30% / fold 70% · QTo: call 25% / fold 75% · JTo: call 25% / fold 75% · TT: 3bet 35% / call 65% · T9s: 3bet 10% / call 85% / fold 5% · T8s: call 60% / fold 40% · T7s: call 25% / fold 75% · A9o: call 20% / fold 80% · 99: 3bet 15% / call 85% · 98s: 3bet 5% / call 80% / fold 15% · 97s: call 45% / fold 55% · 88: 3bet 10% / call 90% · 87s: 3bet 5% / call 75% / fold 20% · 86s: call 35% / fold 65% · 77: 3bet 5% / call 95% · 76s: 3bet 5% / call 70% / fold 25% · 75s: call 30% / fold 70% · 65s: 3bet 5% / call 65% / fold 30% · 64s: call 25% / fold 75% · 54s: 3bet 5% / call 60% / fold 35% · 53s: call 25% / fold 75% · 44: call 90% / fold 10% · 43s: call 20% / fold 80% · 33: call 80% / fold 20% · 22: call 70% / fold 30%

> BB closes the action getting an excellent price: with 1bb already posted, BB calls only ~1.3bb more to win a ~4.6bb pot (~3.5:1), so it defends very wide and primarily via CALL. UTG opens a tight ~16-18% range, so BB does not flat pure trash, but realized-equity plus closing action justify all suited connectors/one-gappers down to ~43s, most suited Broadways, all Ax-suited, and pairs down to a high-frequency 22 (small pairs almost always call for set value; 55/66 are pure defends). 3bet construction is value-heavy and polarized vs a tight opener: linear value of QQ+/AK pure, a value-leaning JJ/TT/AQs region, balanced by suited bluffs that block the opener's continuing range — A5s-A2s (wheel/blockers, top bluff group), A6s-A7s, KJs/KQs, plus low-frequency suited-connector flair (T9s/98s/87s/76s/65s/54s). Total 3bet ~8% keeps UTG from auto-continuing. Offsuit holdings defend much narrower than suited due to the realization penalty.

### BB vs MP open

**Range ≈ ~11% 3bet, plus wide flat defense (~45%+ total defense)** ｜ Sizing: 3bet to ~11bb ｜ 主アクション: 3bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 3 | 3 | 3* | 3* | C* | C* | C* | C* | C* | C* | C* | C* | C* |
| **K** | 3 | 3 | 3* | C* | C* | C* | C* | C* | C* | C* | C* |   |   |
| **Q** | 3* | C* | 3* | C* | C* | C* | C* | C* | C* |   |   |   |   |
| **J** | C* | C* | C* | 3* | C* | C* | C* | C* |   |   |   |   |   |
| **T** | C* | C* | C* | C* | 3* | C* | C* | C* |   |   |   |   |   |
| **9** | C* | C* | C* | C* | C* | C* | C* | C* | C* |   |   |   |   |
| **8** | C* |   |   |   | C* | C* | C* | C* | C* | C* |   |   |   |
| **7** |   |   |   |   |   |   | C* | C* | C* | C* | C* |   |   |
| **6** |   |   |   |   |   |   |   |   | C* | C* | C* |   |   |
| **5** | C* |   |   |   |   |   |   |   |   | C* | C* | C* |   |
| **4** | C* |   |   |   |   |   |   |   |   |   | C* | C* |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   | C* |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   | C* |

**Mixed:** AQs: 3bet 85% / call 15% · AJs: 3bet 55% / call 45% · ATs: 3bet 40% / call 60% · A9s: 3bet 20% / call 80% · A8s: 3bet 18% / call 82% · A7s: 3bet 15% / call 85% · A6s: 3bet 12% / call 88% · A5s: 3bet 45% / call 55% · A4s: 3bet 40% / call 60% · A3s: 3bet 30% / call 70% · A2s: 3bet 20% / call 80% · KQs: 3bet 65% / call 35% · KJs: 3bet 45% / call 55% · KTs: 3bet 35% / call 65% · K9s: 3bet 15% / call 85% · K8s: 3bet 8% / call 85% / fold 7% · K7s: 3bet 6% / call 79% / fold 15% · K6s: 3bet 5% / call 70% / fold 25% · K5s: 3bet 5% / call 60% / fold 35% · K4s: 3bet 4% / call 46% / fold 50% · AQo: 3bet 70% / call 30% · KQo: 3bet 40% / call 58% / fold 2% · QQ: 3bet 95% / call 5% · QJs: 3bet 45% / call 55% · QTs: 3bet 40% / call 60% · Q9s: 3bet 18% / call 82% · Q8s: 3bet 8% / call 82% / fold 10% · Q7s: 3bet 4% / call 61% / fold 35% · Q6s: 3bet 3% / call 47% / fold 50% · AJo: 3bet 40% / call 60% · KJo: 3bet 25% / call 60% / fold 15% · QJo: 3bet 20% / call 65% / fold 15% · JJ: 3bet 80% / call 20% · JTs: 3bet 45% / call 55% · J9s: 3bet 20% / call 80% · J8s: 3bet 8% / call 82% / fold 10% · J7s: 3bet 4% / call 56% / fold 40% · ATo: 3bet 25% / call 70% / fold 5% · KTo: 3bet 15% / call 60% / fold 25% · QTo: 3bet 12% / call 63% / fold 25% · JTo: 3bet 12% / call 63% / fold 25% · TT: 3bet 55% / call 45% · T9s: 3bet 30% / call 70% · T8s: 3bet 15% / call 85% · T7s: 3bet 6% / call 74% / fold 20% · A9o: 3bet 8% / call 52% / fold 40% · K9o: 3bet 5% / call 45% / fold 50% · Q9o: 3bet 4% / call 51% / fold 45% · J9o: 3bet 4% / call 51% / fold 45% · T9o: 3bet 8% / call 62% / fold 30% · 99: 3bet 35% / call 65% · 98s: 3bet 25% / call 75% · 97s: 3bet 12% / call 83% / fold 5% · 96s: 3bet 5% / call 60% / fold 35% · A8o: 3bet 5% / call 40% / fold 55% · T8o: 3bet 3% / call 47% / fold 50% · 98o: 3bet 5% / call 55% / fold 40% · 88: 3bet 20% / call 80% · 87s: 3bet 22% / call 78% · 86s: 3bet 10% / call 80% / fold 10% · 85s: 3bet 4% / call 51% / fold 45% · 87o: 3bet 4% / call 46% / fold 50% · 77: 3bet 12% / call 88% · 76s: 3bet 18% / call 82% · 75s: 3bet 8% / call 77% / fold 15% · 74s: 3bet 3% / call 37% / fold 60% · 66: 3bet 8% / call 92% · 65s: 3bet 15% / call 85% · 64s: 3bet 6% / call 74% / fold 20% · A5o: 3bet 10% / call 45% / fold 45% · 55: 3bet 6% / call 94% · 54s: 3bet 12% / call 88% · 53s: 3bet 5% / call 65% / fold 30% · A4o: 3bet 6% / call 34% / fold 60% · 44: 3bet 5% / call 95% · 43s: 3bet 4% / call 56% / fold 40% · 33: 3bet 4% / call 96% · 22: 3bet 4% / call 96%

> BB vs MP 3bet to ~11bb (OOP, larger size). Value core: AA-JJ, AKs/AKo, AQs all 3bet heavily. Bluffs: suited wheel aces (A5s-A2s) as best blocker semi-bluffs, suited Broadways (KQs/KJs/QJs/JTs) and suited connectors mixed; small offsuit-ace 3bet bluffs (A5o/A4o) at low freq. Because BB closes the action and is getting a price (no callers behind), the flat range is very wide — essentially all suited hands down to weak Kx/Qx, all small pairs, suited connectors, and many offsuit Broadways defend by calling. Defend slightly wider than vs UTG since MP's range is marginally weaker.

### BB vs CO open

**Range ≈ 3bet ~13%, flat ~45% (very wide defense)** ｜ Sizing: 3bet to ~12bb ｜ 主アクション: 3bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 3 | 3 | 3* | 3* | 3* | C* | C* | C* | C* | 3* | 3* | 3* | C* |
| **K** | 3 | 3 | 3* | 3* | C* | C* | C* | C* | C* | C* | C* |   |   |
| **Q** | 3* | 3* | 3* | 3* | C* | C* | C* | C* | C* |   |   |   |   |
| **J** | 3* | C* | C* | 3* | C* | C* | C* | C* |   |   |   |   |   |
| **T** | C* | C* | C* | C* | 3* | C* | C* | C* | C* |   |   |   |   |
| **9** | C* | C* | C* | C* | C* | C* | C* | C* | C* |   |   |   |   |
| **8** | C* | C* |   |   | C* | C* | C* | C* | C* | C* |   |   |   |
| **7** | C* |   |   |   |   | C* | C* | C* | C* | C* |   |   |   |
| **6** | C* |   |   |   |   |   | C* | C* | C* | C* | C* |   |   |
| **5** | C* |   |   |   |   |   |   | C* | C* | C* | C* | C* |   |
| **4** | C* |   |   |   |   |   |   |   |   | C* | C* | C* | C* |
| **3** | C* |   |   |   |   |   |   |   |   |   |   | C* | C* |
| **2** | C* |   |   |   |   |   |   |   |   |   |   |   | C* |

**Mixed:** AQs: 3bet 90% / call 10% · AJs: 3bet 65% / call 35% · ATs: 3bet 50% / call 50% · A9s: 3bet 25% / call 75% · A8s: 3bet 22% / call 78% · A7s: 3bet 20% / call 80% · A6s: 3bet 25% / call 75% · A5s: 3bet 65% / call 35% · A4s: 3bet 60% / call 40% · A3s: 3bet 50% / call 50% · A2s: 3bet 40% / call 60% · KQs: 3bet 75% / call 25% · KJs: 3bet 55% / call 45% · KTs: 3bet 40% / call 60% · K9s: 3bet 20% / call 80% · K8s: 3bet 12% / call 78% / fold 10% · K7s: 3bet 10% / call 75% / fold 15% · K6s: 3bet 8% / call 67% / fold 25% · K5s: 3bet 8% / call 57% / fold 35% · K4s: 3bet 6% / call 44% / fold 50% · AQo: 3bet 80% / call 20% · KQo: 3bet 55% / call 45% · QQ: 3bet 95% / call 5% · QJs: 3bet 55% / call 45% · QTs: 3bet 40% / call 60% · Q9s: 3bet 20% / call 80% · Q8s: 3bet 12% / call 78% / fold 10% · Q7s: 3bet 5% / call 60% / fold 35% · Q6s: 3bet 5% / call 50% / fold 45% · AJo: 3bet 55% / call 45% · KJo: 3bet 35% / call 62% / fold 3% · QJo: 3bet 30% / call 67% / fold 3% · JJ: 3bet 80% / call 20% · JTs: 3bet 45% / call 55% · J9s: 3bet 22% / call 78% · J8s: 3bet 12% / call 78% / fold 10% · J7s: 3bet 5% / call 60% / fold 35% · ATo: 3bet 35% / call 65% · KTo: 3bet 22% / call 70% / fold 8% · QTo: 3bet 20% / call 72% / fold 8% · JTo: 3bet 22% / call 70% / fold 8% · TT: 3bet 55% / call 45% · T9s: 3bet 40% / call 60% · T8s: 3bet 20% / call 80% · T7s: 3bet 10% / call 80% / fold 10% · T6s: 3bet 5% / call 55% / fold 40% · A9o: 3bet 12% / call 78% / fold 10% · K9o: 3bet 8% / call 60% / fold 32% · Q9o: 3bet 6% / call 59% / fold 35% · J9o: 3bet 6% / call 54% / fold 40% · T9o: 3bet 12% / call 73% / fold 15% · 99: 3bet 35% / call 65% · 98s: 3bet 35% / call 65% · 97s: 3bet 15% / call 80% / fold 5% · 96s: 3bet 8% / call 67% / fold 25% · A8o: 3bet 8% / call 62% / fold 30% · K8o: 3bet 4% / call 41% / fold 55% · T8o: 3bet 5% / call 50% / fold 45% · 98o: 3bet 8% / call 67% / fold 25% · 88: 3bet 25% / call 75% · 87s: 3bet 35% / call 65% · 86s: 3bet 12% / call 78% / fold 10% · 85s: 3bet 5% / call 55% / fold 40% · A7o: 3bet 6% / call 54% / fold 40% · 97o: 3bet 4% / call 46% / fold 50% · 87o: 3bet 6% / call 59% / fold 35% · 77: 3bet 20% / call 80% · 76s: 3bet 30% / call 70% · 75s: 3bet 10% / call 80% / fold 10% · A6o: 3bet 5% / call 50% / fold 45% · 86o: 3bet 3% / call 42% / fold 55% · 76o: 3bet 5% / call 50% / fold 45% · 66: 3bet 15% / call 85% · 65s: 3bet 28% / call 72% · 64s: 3bet 10% / call 75% / fold 15% · A5o: 3bet 12% / call 58% / fold 30% · 75o: 3bet 3% / call 37% / fold 60% · 65o: 3bet 4% / call 46% / fold 50% · 55: 3bet 15% / call 85% · 54s: 3bet 25% / call 75% · 53s: 3bet 8% / call 72% / fold 20% · A4o: 3bet 10% / call 50% / fold 40% · 54o: 3bet 3% / call 42% / fold 55% · 44: 3bet 12% / call 88% · 43s: 3bet 6% / call 64% / fold 30% · 42s: 3bet 4% / call 46% / fold 50% · A3o: 3bet 8% / call 42% / fold 50% · 33: 3bet 10% / call 90% · 32s: 3bet 4% / call 46% / fold 50% · A2o: 3bet 5% / call 40% / fold 55% · 22: 3bet 8% / call 92%

> BB vs CO is one of the widest defense spots: BB closes the action getting a discounted price, so it flats an enormous range (most suited hands, suited Ax/Kx down to gappers, all small pairs, plenty of offsuit broadways and offsuit Ax). 3bet ~13% blends value (QQ+/AK pure, JJ/TT/AQ/KQs mostly) with polar bluffs concentrated in suited wheel aces (A5s-A2s, A4s, A3s) that have nut-blocker plus playability, plus a smattering of suited connectors and suited Kx/Qx as semibluffs. Big offsuit Ax (A8s/A7s/A6s) are mostly FLAT, not 3bet — the blocker-bluff role belongs to the wheel suited aces, so I lowered A7s/A8s/A6s aggro. Because CO range is weaker and wider than EP, BB widens the 3bet and flats wider rather than folding. Sizing ~12bb (4x+) because OOP needs a larger size to deny the CO's wide range its equity. Marginal offsuit broadways (KJo/QTo/JTo) mostly flat with low-freq 3bet mixes. Suited junk (K5s-K8s, Q7s, 64s, 53s, 43s) splits between low-freq 3bet, flat, and fold.

### BB vs BTN open

**Range ≈ ~15% 3bet / defend ~62% total (call very wide)** ｜ Sizing: 3bet to ~12bb ｜ 主アクション: 3bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 3 | 3* | 3* | 3* | C* | C* | C* | C* | C* | 3* | 3* | C* | C* |
| **K** | 3* | 3 | 3* | C* | C* | C* | C* | C* | C* | C* | C* | C* | C* |
| **Q** | 3* | C* | 3* | C* | C* | C* | C* | C* | C* | C* | C* | C* |   |
| **J** | C* | C* | C* | 3* | C* | C* | C* | C* | C* |   |   |   |   |
| **T** | C* | C* | C* | C* | 3* | C* | C* | C* | C* |   |   |   |   |
| **9** | C* | C* | C* | C* | C* | C* | C* | C* | C* |   |   |   |   |
| **8** | C* | C* |   |   | C* | C* | C* | C* | C* | C* |   |   |   |
| **7** | C* |   |   |   |   |   | C* | C* | C* | C* | C* |   |   |
| **6** | C* |   |   |   |   |   |   | C* | C* | C* | C* |   |   |
| **5** | C* |   |   |   |   |   |   |   |   | C* | C* | C* |   |
| **4** | C* |   |   |   |   |   |   |   |   |   | C* | C* | C* |
| **3** | C* |   |   |   |   |   |   |   |   |   |   | C* | C* |
| **2** | C* |   |   |   |   |   |   |   |   |   |   |   | C* |

**Mixed:** AKs: 3bet 95% / call 5% · AQs: 3bet 75% / call 25% · AJs: 3bet 60% / call 40% · ATs: 3bet 45% / call 55% · A9s: 3bet 40% / call 60% · A8s: 3bet 40% / call 60% · A7s: 3bet 42% / call 58% · A6s: 3bet 40% / call 60% · A5s: 3bet 55% / call 45% · A4s: 3bet 52% / call 48% · A3s: 3bet 48% / call 52% · A2s: 3bet 38% / call 62% · AKo: 3bet 90% / call 10% · KQs: 3bet 55% / call 45% · KJs: 3bet 45% / call 55% · KTs: 3bet 40% / call 60% · K9s: 3bet 25% / call 75% · K8s: 3bet 15% / call 82% / fold 3% · K7s: 3bet 12% / call 78% / fold 10% · K6s: 3bet 12% / call 72% / fold 16% · K5s: 3bet 12% / call 68% / fold 20% · K4s: 3bet 10% / call 62% / fold 28% · K3s: 3bet 8% / call 54% / fold 38% · K2s: 3bet 8% / call 48% / fold 44% · AQo: 3bet 55% / call 45% · KQo: 3bet 40% / call 60% · QQ: 3bet 99% / call 1% · QJs: 3bet 45% / call 55% · QTs: 3bet 40% / call 60% · Q9s: 3bet 25% / call 75% · Q8s: 3bet 12% / call 82% / fold 6% · Q7s: 3bet 8% / call 70% / fold 22% · Q6s: 3bet 8% / call 62% / fold 30% · Q5s: 3bet 8% / call 56% / fold 36% · Q4s: 3bet 6% / call 49% / fold 45% · Q3s: 3bet 5% / call 40% / fold 55% · AJo: 3bet 40% / call 60% · KJo: 3bet 25% / call 70% / fold 5% · QJo: 3bet 25% / call 67% / fold 8% · JJ: 3bet 80% / call 20% · JTs: 3bet 45% / call 55% · J9s: 3bet 30% / call 70% · J8s: 3bet 15% / call 80% / fold 5% · J7s: 3bet 10% / call 62% / fold 28% · J6s: 3bet 5% / call 45% / fold 50% · ATo: 3bet 25% / call 75% · KTo: 3bet 18% / call 70% / fold 12% · QTo: 3bet 15% / call 70% / fold 15% · JTo: 3bet 15% / call 70% / fold 15% · TT: 3bet 55% / call 45% · T9s: 3bet 40% / call 60% · T8s: 3bet 25% / call 73% / fold 2% · T7s: 3bet 12% / call 68% / fold 20% · T6s: 3bet 6% / call 49% / fold 45% · A9o: 3bet 12% / call 83% / fold 5% · K9o: 3bet 6% / call 60% / fold 34% · Q9o: 3bet 4% / call 56% / fold 40% · J9o: 3bet 4% / call 54% / fold 42% · T9o: 3bet 8% / call 64% / fold 28% · 99: 3bet 35% / call 65% · 98s: 3bet 38% / call 62% · 97s: 3bet 20% / call 72% / fold 8% · 96s: 3bet 8% / call 52% / fold 40% · A8o: 3bet 8% / call 72% / fold 20% · K8o: 3bet 3% / call 42% / fold 55% · T8o: 3bet 3% / call 45% / fold 52% · 98o: 3bet 5% / call 57% / fold 38% · 88: 3bet 25% / call 75% · 87s: 3bet 35% / call 65% · 86s: 3bet 18% / call 67% / fold 15% · 85s: 3bet 6% / call 44% / fold 50% · A7o: 3bet 6% / call 64% / fold 30% · 87o: 3bet 4% / call 51% / fold 45% · 77: 3bet 18% / call 82% · 76s: 3bet 30% / call 68% / fold 2% · 75s: 3bet 15% / call 65% / fold 20% · 74s: 3bet 5% / call 35% / fold 60% · A6o: 3bet 5% / call 55% / fold 40% · 76o: 3bet 3% / call 42% / fold 55% · 66: 3bet 12% / call 88% · 65s: 3bet 28% / call 70% / fold 2% · 64s: 3bet 12% / call 63% / fold 25% · A5o: 3bet 12% / call 70% / fold 18% · 55: 3bet 12% / call 88% · 54s: 3bet 25% / call 70% / fold 5% · 53s: 3bet 10% / call 60% / fold 30% · A4o: 3bet 10% / call 65% / fold 25% · 44: 3bet 10% / call 90% · 43s: 3bet 8% / call 52% / fold 40% · 42s: 3bet 3% / call 27% / fold 70% · A3o: 3bet 6% / call 54% / fold 40% · 33: 3bet 8% / call 92% · 32s: 3bet 3% / call 32% / fold 65% · A2o: 3bet 4% / call 46% / fold 50% · 22: 3bet 8% / call 92%

> BB closes the action getting ~3.5:1, so defend extremely wide via flatting almost any suited hand, all pairs, and most offsuit broadways. 3bet a value core (QQ+/AKs/AKo near-pure) plus a large polar bluff group: suited wheel aces A5s-A2s (blocker + nut potential), suited connectors/gappers (54s-T9s, 86s, 75s, 64s) and select offsuit broadways/aces. Heavy mixing on JJ/TT, AQs/AJs, KQs and bluff candidates so BTN cannot exploit either branch. Total defend ~62%; 3bet ~15%.

### BB vs SB open

**Range ≈ ~3bet 16% / total defend ~78%+ (call extremely wide, fold only worst offsuit)** ｜ Sizing: 3bet to ~10bb ｜ 主アクション: 3bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 3* | 3* | 3* | 3* | C* | C* | C* | C* | C* | C* | C* | C* | C* |
| **K** | 3* | 3* | 3* | C* | C* | C* | C* | C* | C* | C* | C* | C* | C* |
| **Q** | 3* | C* | 3* | C* | C* | C* | C* | C* | C* | C* | C* | C* | C* |
| **J** | C* | C* | C* | 3* | C* | C* | C* | C* | C* | C* |   |   |   |
| **T** | C* | C* | C* | C* | 3* | C* | C* | C* | C* |   |   |   |   |
| **9** | C* | C* | C* | C* | C* | C* | C* | C* | C* |   |   |   |   |
| **8** | C* | C* | C* | C* | C* | C* | C* | C* | C* | C* |   |   |   |
| **7** | C* | C* | C* |   |   | C* | C* | C* | C* | C* |   |   |   |
| **6** | C* | C* |   |   |   |   | C* | C* | C* | C* | C* |   |   |
| **5** | C* |   |   |   |   |   |   | C* | C* | C* | C* | C* |   |
| **4** | C* |   |   |   |   |   |   |   |   | C* | C* | C* |   |
| **3** | C* |   |   |   |   |   |   |   |   |   |   | C* |   |
| **2** | C* |   |   |   |   |   |   |   |   |   |   |   | C* |

**Mixed:** AA: 3bet 92% / call 8% · AKs: 3bet 88% / call 12% · AQs: 3bet 68% / call 32% · AJs: 3bet 52% / call 48% · ATs: 3bet 42% / call 58% · A9s: 3bet 28% / call 72% · A8s: 3bet 25% / call 75% · A7s: 3bet 24% / call 76% · A6s: 3bet 22% / call 78% · A5s: 3bet 42% / call 58% · A4s: 3bet 38% / call 62% · A3s: 3bet 34% / call 66% · A2s: 3bet 28% / call 72% · AKo: 3bet 85% / call 15% · KK: 3bet 92% / call 8% · KQs: 3bet 52% / call 48% · KJs: 3bet 44% / call 56% · KTs: 3bet 40% / call 60% · K9s: 3bet 25% / call 75% · K8s: 3bet 18% / call 82% · K7s: 3bet 15% / call 85% · K6s: 3bet 14% / call 86% · K5s: 3bet 14% / call 86% · K4s: 3bet 12% / call 88% · K3s: 3bet 10% / call 90% · K2s: 3bet 8% / call 92% · AQo: 3bet 55% / call 45% · KQo: 3bet 45% / call 55% · QQ: 3bet 88% / call 12% · QJs: 3bet 42% / call 58% · QTs: 3bet 40% / call 60% · Q9s: 3bet 25% / call 75% · Q8s: 3bet 16% / call 84% · Q7s: 3bet 10% / call 90% · Q6s: 3bet 8% / call 92% · Q5s: 3bet 8% / call 92% · Q4s: 3bet 6% / call 94% · Q3s: 3bet 5% / call 95% · Q2s: 3bet 4% / call 96% · AJo: 3bet 40% / call 60% · KJo: 3bet 35% / call 65% · QJo: 3bet 32% / call 68% · JJ: 3bet 75% / call 25% · JTs: 3bet 42% / call 58% · J9s: 3bet 28% / call 72% · J8s: 3bet 18% / call 82% · J7s: 3bet 10% / call 90% · J6s: 3bet 5% / call 95% · J5s: 3bet 4% / call 94% / fold 2% · ATo: 3bet 30% / call 70% · KTo: 3bet 28% / call 72% · QTo: 3bet 28% / call 72% · JTo: 3bet 28% / call 72% · TT: 3bet 58% / call 42% · T9s: 3bet 35% / call 65% · T8s: 3bet 24% / call 76% · T7s: 3bet 15% / call 85% · T6s: 3bet 8% / call 92% · A9o: 3bet 15% / call 85% · K9o: 3bet 12% / call 84% / fold 4% · Q9o: 3bet 12% / call 82% / fold 6% · J9o: 3bet 12% / call 82% / fold 6% · T9o: 3bet 20% / call 80% · 99: 3bet 42% / call 58% · 98s: 3bet 28% / call 72% · 97s: 3bet 18% / call 82% · 96s: 3bet 8% / call 92% · A8o: 3bet 12% / call 86% / fold 2% · K8o: 3bet 8% / call 74% / fold 18% · Q8o: 3bet 6% / call 70% / fold 24% · J8o: 3bet 5% / call 70% / fold 25% · T8o: 3bet 8% / call 77% / fold 15% · 98o: 3bet 15% / call 81% / fold 4% · 88: 3bet 30% / call 70% · 87s: 3bet 26% / call 74% · 86s: 3bet 15% / call 85% · 85s: 3bet 6% / call 90% / fold 4% · A7o: 3bet 10% / call 86% / fold 4% · K7o: 3bet 6% / call 64% / fold 30% · Q7o: 3bet 4% / call 51% / fold 45% · 97o: 3bet 6% / call 69% / fold 25% · 87o: 3bet 12% / call 83% / fold 5% · 77: 3bet 25% / call 75% · 76s: 3bet 24% / call 76% · 75s: 3bet 12% / call 88% · A6o: 3bet 10% / call 84% / fold 6% · K6o: 3bet 4% / call 56% / fold 40% · 86o: 3bet 5% / call 65% / fold 30% · 76o: 3bet 10% / call 80% / fold 10% · 66: 3bet 20% / call 80% · 65s: 3bet 22% / call 78% · 64s: 3bet 10% / call 90% · A5o: 3bet 14% / call 84% / fold 2% · 75o: 3bet 5% / call 60% / fold 35% · 65o: 3bet 8% / call 77% / fold 15% · 55: 3bet 18% / call 82% · 54s: 3bet 20% / call 80% · 53s: 3bet 8% / call 90% / fold 2% · A4o: 3bet 12% / call 84% / fold 4% · 54o: 3bet 6% / call 69% / fold 25% · 44: 3bet 15% / call 85% · 43s: 3bet 10% / call 86% / fold 4% · A3o: 3bet 10% / call 82% / fold 8% · 33: 3bet 12% / call 88% · A2o: 3bet 8% / call 78% / fold 14% · 22: 3bet 10% / call 90%

> BB closes the action getting an excellent price (call ~7bb to win ~14.5bb) and is in position postflop vs a very wide SB 3bb open, so it defends extremely wide. Key principle: BB calls essentially ALL suited hands (down to Q2s/J5s/53s) and only folds the very worst offsuit trash. 3bet is polar to ~10bb: linear value (QQ+, AK, AQs, KQs) plus a large bluff block led by suited wheel aces (A5s-A2s, which 3bet MORE than A9s-A6s due to nut/blocker value), suited gappers, small suited kings, and offsuit broadways. Premium cores AA/KK/QQ slow-play a small slice (8-12%) to protect the flat range. notes-on-defense: vs SB's ~85% open BB folds very little — nearly 100% of offsuit broadways and offsuit aces continue, only marginal offsuit gappers/small kings (K6o, Q7o, J8o-, 75o) drop into meaningful folds. Heavy mixing throughout the marginal region; exact frequencies vary by solver and rake.


---

## IP/SB vs RFI (3bet or flat)

### BTN vs CO open

**Range ≈ ~9% 3bet, ~27% flat (call)** ｜ Sizing: 3bet to ~8bb ｜ 主アクション: 3bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 3 | 3* | 3* | C* | C* | C* | C* | C* | C* | C* | C* | C* | C* |
| **K** | 3* | 3 | C* | C* | C* | C* | C* | C* | C* | C* |   |   |   |
| **Q** | 3* | C* | 3* | C* | C* | C* | C* |   |   |   |   |   |   |
| **J** | C* | C* | C* | 3* | C* | C* | C* |   |   |   |   |   |   |
| **T** | C* | C* | C* | C* | C* | C* | C* |   |   |   |   |   |   |
| **9** | C* |   |   |   | C* | C* | C* | C* |   |   |   |   |   |
| **8** |   |   |   |   |   |   | C* | C* | C* |   |   |   |   |
| **7** |   |   |   |   |   |   |   | C* | C* | C* |   |   |   |
| **6** |   |   |   |   |   |   |   |   | C* | C* | C* |   |   |
| **5** | C* |   |   |   |   |   |   |   |   | C* | C* | C* |   |
| **4** | C* |   |   |   |   |   |   |   |   |   | C* | C* |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   | C* |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   | C* |

**Mixed:** AKs: 3bet 85% / call 15% · AQs: 3bet 55% / call 45% · AJs: 3bet 35% / call 65% · ATs: 3bet 25% / call 75% · A9s: 3bet 12% / call 88% · A8s: 3bet 10% / call 90% · A7s: 3bet 8% / call 92% · A6s: 3bet 12% / call 88% · A5s: 3bet 45% / call 55% · A4s: 3bet 42% / call 58% · A3s: 3bet 30% / call 70% · A2s: 3bet 18% / call 82% · AKo: 3bet 90% / call 10% · KQs: 3bet 45% / call 55% · KJs: 3bet 35% / call 65% · KTs: 3bet 25% / call 75% · K9s: 3bet 12% / call 88% · K8s: 3bet 6% / call 74% / fold 20% · K7s: 3bet 5% / call 55% / fold 40% · K6s: 3bet 5% / call 50% / fold 45% · K5s: 3bet 8% / call 42% / fold 50% · AQo: 3bet 50% / call 50% · KQo: 3bet 30% / call 60% / fold 10% · QQ: 3bet 90% / call 10% · QJs: 3bet 30% / call 70% · QTs: 3bet 25% / call 75% · Q9s: 3bet 10% / call 90% · Q8s: 3bet 5% / call 75% / fold 20% · AJo: 3bet 20% / call 70% / fold 10% · KJo: 3bet 15% / call 55% / fold 30% · QJo: 3bet 10% / call 55% / fold 35% · JJ: 3bet 55% / call 45% · JTs: 3bet 30% / call 70% · J9s: 3bet 12% / call 88% · J8s: 3bet 8% / call 72% / fold 20% · ATo: 3bet 10% / call 60% / fold 30% · KTo: 3bet 8% / call 42% / fold 50% · QTo: 3bet 5% / call 45% / fold 50% · JTo: 3bet 8% / call 52% / fold 40% · TT: 3bet 35% / call 65% · T9s: 3bet 20% / call 80% · T8s: 3bet 12% / call 78% / fold 10% · A9o: 3bet 5% / call 25% / fold 70% · T9o: 3bet 5% / call 45% / fold 50% · 99: 3bet 20% / call 80% · 98s: 3bet 18% / call 82% · 97s: 3bet 10% / call 75% / fold 15% · 88: 3bet 15% / call 85% · 87s: 3bet 18% / call 77% / fold 5% · 86s: 3bet 8% / call 67% / fold 25% · 77: 3bet 12% / call 88% · 76s: 3bet 15% / call 75% / fold 10% · 75s: 3bet 5% / call 60% / fold 35% · 66: 3bet 10% / call 90% · 65s: 3bet 12% / call 78% / fold 10% · 64s: 3bet 5% / call 55% / fold 40% · A5o: 3bet 10% / call 20% / fold 70% · 55: 3bet 12% / call 88% · 54s: 3bet 10% / call 75% / fold 15% · 53s: 3bet 5% / call 50% / fold 45% · A4o: 3bet 6% / call 14% / fold 80% · 44: 3bet 8% / call 92% · 43s: 3bet 3% / call 42% / fold 55% · 33: 3bet 5% / call 95% · 22: 3bet 5% / call 95%

> BTN vs CO open is the widest cold-call spot in NLHE: IP with only blinds behind, so BTN flats nearly ALL suited hands down to low Axs/Kxs/suited connectors-gappers to realize equity IP, plus pairs TT-22 and offsuit broadways. 3bet is a polar mix: value QQ+/AK pure-ish with JJ/TT/AQ mixing; bluffs cluster in A2s-A5s wheel (A5s/A4s lead, best blockers) plus suited broadways (KJs/KQs/QJs) and suited connectors at low freq. Key principle: because BTN can profitably flat almost every suited hand IP, suited hands should NOT carry meaningful fold%; only the very bottom suited (K5s, 53s, 43s, 64s) and most offsuit non-broadway hands fold. Offsuit suited-connector-style hands (A4o/A5o/T9o etc.) are mostly fold with a thin 3bet-bluff/flat mix. Adjust 3bet bluffs up vs over-folding CO; flat wider vs strong/sticky CO. Study-grade approximations aligned with published solver charts, not exact output.

### BTN vs UTG open

**Range ≈ ~24-26% total continue (~7% 3bet, ~18% flat)** ｜ Sizing: 3bet to ~7.5bb ｜ 主アクション: 3bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 3 | 3* | C* | C* | C* | C* | C* |   |   | 3* | 3* | 3* | C* |
| **K** | 3* | 3 | C* | C* | C* | C* |   |   |   |   |   |   |   |
| **Q** | 3* | C* | 3* | C* | C* | C* |   |   |   |   |   |   |   |
| **J** | C* | C* |   | 3* | C* | C* |   |   |   |   |   |   |   |
| **T** | C* |   |   |   | C* | C* | C* |   |   |   |   |   |   |
| **9** |   |   |   |   |   | C* | C* | C* |   |   |   |   |   |
| **8** |   |   |   |   |   |   | C* | C* |   |   |   |   |   |
| **7** |   |   |   |   |   |   |   | C | C* |   |   |   |   |
| **6** |   |   |   |   |   |   |   |   | C | C* |   |   |   |
| **5** |   |   |   |   |   |   |   |   |   | C* | C* |   |   |
| **4** |   |   |   |   |   |   |   |   |   |   | C* |   |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   | C* |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   | C* |

**Mixed:** AKs: 3bet 90% / call 10% · AQs: 3bet 45% / call 55% · AJs: 3bet 25% / call 75% · ATs: 3bet 15% / call 85% · A9s: call 70% / fold 30% · A8s: call 40% / fold 60% · A5s: 3bet 55% / call 45% · A4s: 3bet 45% / call 40% / fold 15% · A3s: 3bet 35% / call 35% / fold 30% · A2s: 3bet 25% / call 30% / fold 45% · AKo: 3bet 90% / call 10% · KQs: 3bet 35% / call 65% · KJs: 3bet 20% / call 75% / fold 5% · KTs: 3bet 10% / call 80% / fold 10% · K9s: call 45% / fold 55% · AQo: 3bet 40% / call 40% / fold 20% · KQo: 3bet 15% / call 40% / fold 45% · QQ: 3bet 92% / call 8% · QJs: 3bet 20% / call 75% / fold 5% · QTs: 3bet 10% / call 75% / fold 15% · Q9s: call 45% / fold 55% · AJo: 3bet 15% / call 30% / fold 55% · KJo: 3bet 5% / call 20% / fold 75% · JJ: 3bet 55% / call 45% · JTs: 3bet 15% / call 80% / fold 5% · J9s: call 50% / fold 50% · ATo: call 20% / fold 80% · TT: 3bet 25% / call 75% · T9s: 3bet 10% / call 75% / fold 15% · T8s: call 40% / fold 60% · 99: 3bet 10% / call 90% · 98s: 3bet 10% / call 65% / fold 25% · 97s: call 35% / fold 65% · 88: 3bet 5% / call 95% · 87s: 3bet 10% / call 55% / fold 35% · 76s: 3bet 10% / call 45% / fold 45% · 65s: 3bet 5% / call 40% / fold 55% · 55: call 95% / fold 5% · 54s: 3bet 5% / call 30% / fold 65% · 44: call 90% / fold 10% · 33: call 80% / fold 20% · 22: call 75% / fold 25%

> vs a tight UTG open, BTN is IP and has the widest continuing range of any seat because position maximizes equity realization. Value 3bets are QQ+/AKs/AKo (near-pure), with JJ/TT/AQs mixing toward flatting since they realize equity well in position. Bluff 3bets favor suited wheel aces (A5s-A2s) for blocker/playability, plus a few suited broadways (KJs/KQs/QJs/JTs) and suited connectors (98s/87s/76s) at low frequency. The bulk of the range FLATS: all pocket pairs set-mine very profitably IP (22-77 near-pure continue — small pairs vs a tight UTG range that stacks off light realize huge implied odds), suited broadways and suited connectors flat to keep UTG's range wide and exploit positional edge. Offsuit broadways outside AKo/AQo/AJo/KQo are mostly folds vs a tight range. Total continue ~24-26%, 3bet ~7% value-leaning with a thin bluff layer.

### CO vs UTG open

**Range ≈ ~7% 3bet (value-heavy + a few suited-blocker bluffs), ~5% flat** ｜ Sizing: 3bet to ~7.5bb ｜ 主アクション: 3bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 3 | 3 | 3* | C* | C* |   |   |   |   | 3* | 3* | 3* | 3* |
| **K** | 3* | 3 | C* | C* | C* |   |   |   |   |   |   |   |   |
| **Q** | 3* |   | 3* | C* | C* |   |   |   |   |   |   |   |   |
| **J** |   |   |   | 3* | C* |   |   |   |   |   |   |   |   |
| **T** |   |   |   |   | C* | C* |   |   |   |   |   |   |   |
| **9** |   |   |   |   |   | C* | C* |   |   |   |   |   |   |
| **8** |   |   |   |   |   |   | C* | C* |   |   |   |   |   |
| **7** |   |   |   |   |   |   |   | C* | C* |   |   |   |   |
| **6** |   |   |   |   |   |   |   |   | C* | C* |   |   |   |
| **5** |   |   |   |   |   |   |   |   |   | C* |   |   |   |
| **4** |   |   |   |   |   |   |   |   |   |   | C* |   |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   | C* |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   | C* |

**Mixed:** AQs: 3bet 50% / call 50% · AJs: 3bet 30% / call 60% / fold 10% · ATs: 3bet 15% / call 60% / fold 25% · A5s: 3bet 40% / fold 60% · A4s: 3bet 25% / fold 75% · A3s: 3bet 10% / fold 90% · A2s: 3bet 5% / fold 95% · AKo: 3bet 95% / call 5% · KQs: 3bet 40% / call 55% / fold 5% · KJs: 3bet 20% / call 50% / fold 30% · KTs: 3bet 10% / call 40% / fold 50% · AQo: 3bet 35% / call 15% / fold 50% · QQ: 3bet 95% / call 5% · QJs: 3bet 20% / call 45% / fold 35% · QTs: 3bet 10% / call 40% / fold 50% · JJ: 3bet 55% / call 45% · JTs: 3bet 15% / call 50% / fold 35% · TT: 3bet 15% / call 85% · T9s: 3bet 5% / call 40% / fold 55% · 99: 3bet 10% / call 90% · 98s: call 30% / fold 70% · 88: 3bet 5% / call 90% / fold 5% · 87s: call 20% / fold 80% · 77: call 80% / fold 20% · 76s: call 15% / fold 85% · 66: call 55% / fold 45% · 65s: call 10% / fold 90% · 55: call 40% / fold 60% · 44: call 30% / fold 70% · 33: call 20% / fold 80% · 22: call 15% / fold 85%

> CO vs UTG (tightest RFI we face) with squeeze risk behind: value-heavy 3bet, compact flat, mostly 3bet-or-fold on offsuit hands. Value core QQ+/AKs/AKo is pure or near-pure; JJ and AQs split 3bet/flat. Bluffs come primarily from suited wheel aces for blocker value, weighted down sharply by rank (A5s>A4s>A3s>A2s) since UTG is strong, plus low-freq suited-broadway mix-ins (KJs/QJs/JTs/KQs). The flat range is dominated by pocket pairs set-mining in position (TT-22, tapering by frequency) and suited broadways (AJs/ATs/KQs/KJs) and a few suited connectors (JTs/T9s/98s) that play well IP. Offsuit hands other than AKo/AQo are not flatted. Frequencies are approximate study-grade references aligned with common solver charts, not exact output. Adjust toward more 3bet-or-fold if blinds are aggressive squeezers; add a few flats if players behind are passive.

### SB vs BTN open

**Range ≈ ~14% 3bet, ~0% flat (3bet-or-fold)** ｜ Sizing: 3bet to ~10-11bb ｜ 主アクション: 3bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 3 | 3 | 3 | 3* | 3* | 3* | 3* | 3* | 3* | 3* | 3* | 3* | 3* |
| **K** | 3 | 3 | 3 | 3* | 3* | 3* |   |   |   | 3* | 3* |   |   |
| **Q** | 3* | 3* | 3 | 3* | 3* | 3* |   |   |   |   |   |   |   |
| **J** | 3* | 3* | 3* | 3 | 3* | 3* |   |   |   |   |   |   |   |
| **T** | 3* |   |   | 3* | 3* | 3* | 3* |   |   |   |   |   |   |
| **9** |   |   |   |   |   | 3* | 3* |   |   |   |   |   |   |
| **8** |   |   |   |   |   |   | 3* | 3* |   |   |   |   |   |
| **7** |   |   |   |   |   |   |   | 3* | 3* |   |   |   |   |
| **6** |   |   |   |   |   |   |   |   | 3* | 3* |   |   |   |
| **5** |   |   |   |   |   |   |   |   |   | 3* | 3* |   |   |
| **4** |   |   |   |   |   |   |   |   |   |   | 3* |   |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   | 3* |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   | 3* |

**Mixed:** AJs: 3bet 95% / fold 5% · ATs: 3bet 85% / fold 15% · A9s: 3bet 35% / fold 65% · A8s: 3bet 25% / fold 75% · A7s: 3bet 25% / fold 75% · A6s: 3bet 25% / fold 75% · A5s: 3bet 85% / fold 15% · A4s: 3bet 80% / fold 20% · A3s: 3bet 70% / fold 30% · A2s: 3bet 50% / fold 50% · KJs: 3bet 85% / fold 15% · KTs: 3bet 65% / fold 35% · K9s: 3bet 30% / fold 70% · K5s: 3bet 25% / fold 75% · K4s: 3bet 20% / fold 80% · AQo: 3bet 97% / fold 3% · KQo: 3bet 50% / fold 50% · QJs: 3bet 75% / fold 25% · QTs: 3bet 60% / fold 40% · Q9s: 3bet 30% / fold 70% · AJo: 3bet 35% / fold 65% · KJo: 3bet 30% / fold 70% · QJo: 3bet 25% / fold 75% · JTs: 3bet 70% / fold 30% · J9s: 3bet 35% / fold 65% · ATo: 3bet 30% / fold 70% · JTo: 3bet 15% / fold 85% · TT: 3bet 97% / fold 3% · T9s: 3bet 55% / fold 45% · T8s: 3bet 30% / fold 70% · 99: 3bet 80% / fold 20% · 98s: 3bet 45% / fold 55% · 88: 3bet 55% / fold 45% · 87s: 3bet 40% / fold 60% · 77: 3bet 40% / fold 60% · 76s: 3bet 35% / fold 65% · 66: 3bet 30% / fold 70% · 65s: 3bet 30% / fold 70% · 55: 3bet 30% / fold 70% · 54s: 3bet 25% / fold 75% · 44: 3bet 25% / fold 75% · 33: 3bet 20% / fold 80% · 22: 3bet 18% / fold 82%

> SB is OOP with BB still behind, so flatting is avoided — play a 3bet-or-fold strategy (callPct ~0). Range is polar (~14%): linear value core (QQ+/AK plus AQ/AJs/KQs/JJ-TT, which are pure or near-pure) merged with bluffs that hold blockers and playability. Primary bluffs are wheel Axs (A5s-A2s, descending freq) which block AA/AK and make nut flushes, suited Broadways (KJs/KTs/QTs/QJs/JTs), and suited connectors (T9s/98s/87s/76s). Weaker suited Ax (A6s-A9s), small pairs, and low Kxs mix in at low frequency. Premiums are pure; marginals randomize. Sizing ~10-11bb (roughly 4x the open) is larger than IP 3bets because OOP we want to deny equity and discourage flats.

### SB vs CO open

**Range ≈ ~10-11% 3bet (3bet-or-fold)** ｜ Sizing: 3bet to ~10bb ｜ 主アクション: 3bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 3 | 3 | 3 | 3* | 3* | 3* | 3* | 3* | 3* | 3* | 3* | 3* | 3* |
| **K** | 3 | 3 | 3* | 3* | 3* | 3* |   |   |   | 3* |   |   |   |
| **Q** | 3* | 3* | 3 | 3* | 3* | 3* |   |   |   |   |   |   |   |
| **J** | 3* | 3* | 3* | 3 | 3* | 3* |   |   |   |   |   |   |   |
| **T** | 3* |   |   |   | 3* | 3* | 3* |   |   |   |   |   |   |
| **9** |   |   |   |   |   | 3* | 3* | 3* |   |   |   |   |   |
| **8** |   |   |   |   |   |   | 3* | 3* |   |   |   |   |   |
| **7** |   |   |   |   |   |   |   | 3* | 3* |   |   |   |   |
| **6** |   |   |   |   |   |   |   |   | 3* | 3* |   |   |   |
| **5** |   |   |   |   |   |   |   |   |   | 3* | 3* |   |   |
| **4** |   |   |   |   |   |   |   |   |   |   |   |   |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   |   |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   |   |

**Mixed:** AJs: 3bet 95% / fold 5% · ATs: 3bet 85% / fold 15% · A9s: 3bet 30% / fold 70% · A8s: 3bet 25% / fold 75% · A7s: 3bet 25% / fold 75% · A6s: 3bet 25% / fold 75% · A5s: 3bet 85% / fold 15% · A4s: 3bet 75% / fold 25% · A3s: 3bet 60% / fold 40% · A2s: 3bet 45% / fold 55% · KQs: 3bet 90% / fold 10% · KJs: 3bet 70% / fold 30% · KTs: 3bet 55% / fold 45% · K9s: 3bet 25% / fold 75% · K5s: 3bet 20% / fold 80% · AQo: 3bet 92% / fold 8% · KQo: 3bet 50% / fold 50% · QJs: 3bet 65% / fold 35% · QTs: 3bet 60% / fold 40% · Q9s: 3bet 30% / fold 70% · AJo: 3bet 45% / fold 55% · KJo: 3bet 20% / fold 80% · QJo: 3bet 20% / fold 80% · JTs: 3bet 65% / fold 35% · J9s: 3bet 30% / fold 70% · ATo: 3bet 20% / fold 80% · TT: 3bet 95% / fold 5% · T9s: 3bet 50% / fold 50% · T8s: 3bet 25% / fold 75% · 99: 3bet 70% / fold 30% · 98s: 3bet 40% / fold 60% · 97s: 3bet 20% / fold 80% · 88: 3bet 45% / fold 55% · 87s: 3bet 40% / fold 60% · 77: 3bet 30% / fold 70% · 76s: 3bet 35% / fold 65% · 66: 3bet 20% / fold 80% · 65s: 3bet 30% / fold 70% · 55: 3bet 15% / fold 85% · 54s: 3bet 25% / fold 75%

> SB vs CO open is a pure 3bet-or-fold spot (no flatting OOP with BB behind). vs CO's ~26-28% open the SB 3bets a polar ~10-11% range to ~10bb. Value: TT+, AQs+/AKo, AJs, ATs, KQs, plus high-frequency strong broadways (KJs/QJs/JTs/QTs). Bluffs are dominated by suited blockers: wheel aces A5s-A2s are the primary bluffs (best blockers, nut-flush/wheel potential), then suited connectors 87s/76s/65s/98s/T9s and a thinner mix of A9s-A6s and suited broadways. Key corrections vs the draft: (1) removed/cut the small-pair "bluffs" - solvers fold 22-44 entirely and 3bet 55-77 only marginally in 3bet-or-fold OOP spots since pairs have no blocker value and play badly when 4bet/called; trimmed 88-99 and dropped 22/33/44 (and cut 55 to a token mix); (2) cut the mid suited-ace bluff frequencies (A9s-A6s) from ~40-45% to ~25% - their blockers are weak; (3) bumped A2s up and kept A5s-A3s as the core wheel bluffs; (4) thinned offsuit bluffs (AJo, ATo, KJo, QJo) which were too aggressive OOP; (5) removed K7s/K6s/Q8s/J8s/86s as fringe pure-fold marginals. Net range is slightly tighter (~10-11%) and more correctly polarized than the draft. Frequencies are approximate study-grade references, not exact solver output; marginal hands mix heavily.


---

## Facing 3bet (4bet / call / fold)

### BTN open vs SB 3bet  (★ your example)

**Range ≈ BTN continues ~30-34% of its wide opening range vs the SB 3bet: roughly 6-8% pure 4bet (value + suited-ace bluffs) and ~24-27% flat. The rest folds.** ｜ Sizing: 4bet to ~22-24bb ｜ 主アクション: 4bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 4 | 4* | C* | C* | C* | C* | C* |   |   | 4* | 4* | C* | C* |
| **K** | 4 | 4 | C* | C* | C* |   |   |   |   |   |   |   |   |
| **Q** | C* | C* | 4* | C* | C* |   |   |   |   |   |   |   |   |
| **J** | C* | C* |   | C* | C* | C* |   |   |   |   |   |   |   |
| **T** | C* |   |   |   | C* | C* | C* |   |   |   |   |   |   |
| **9** |   |   |   |   |   | C | C* |   |   |   |   |   |   |
| **8** |   |   |   |   |   |   | C | C* |   |   |   |   |   |
| **7** |   |   |   |   |   |   |   | C* | C* |   |   |   |   |
| **6** |   |   |   |   |   |   |   |   | C* | C* |   |   |   |
| **5** | 4* |   |   |   |   |   |   |   |   | C* | C* |   |   |
| **4** |   |   |   |   |   |   |   |   |   |   | C* |   |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   | C* |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   | C* |

**Mixed:** AKs: 4bet 85% / call 15% · AQs: 4bet 20% / call 80% · AJs: 4bet 5% / call 90% / fold 5% · ATs: 4bet 5% / call 80% / fold 15% · A9s: call 60% / fold 40% · A8s: call 45% / fold 55% · A5s: 4bet 55% / call 30% / fold 15% · A4s: 4bet 50% / call 30% / fold 20% · A3s: 4bet 30% / call 35% / fold 35% · A2s: 4bet 15% / call 35% / fold 50% · KQs: 4bet 10% / call 80% / fold 10% · KJs: 4bet 10% / call 70% / fold 20% · KTs: 4bet 5% / call 60% / fold 35% · AQo: 4bet 10% / call 50% / fold 40% · KQo: call 35% / fold 65% · QQ: 4bet 70% / call 30% · QJs: call 65% / fold 35% · QTs: call 55% / fold 45% · AJo: call 40% / fold 60% · KJo: call 12% / fold 88% · JJ: 4bet 25% / call 75% · JTs: call 65% / fold 35% · J9s: call 40% / fold 60% · ATo: call 20% / fold 80% · TT: 4bet 5% / call 95% · T9s: call 55% / fold 45% · T8s: call 30% / fold 70% · 98s: call 45% / fold 55% · 87s: call 40% / fold 60% · 77: call 95% / fold 5% · 76s: call 35% / fold 65% · 66: call 90% / fold 10% · 65s: call 30% / fold 70% · A5o: 4bet 8% / call 5% / fold 87% · 55: call 80% / fold 20% · 54s: call 25% / fold 75% · 44: call 70% / fold 30% · 33: call 55% / fold 45% · 22: call 50% / fold 50%

> Canonical heavily-mixed BTN-vs-SB-3bet node. BTN opened wide (~45-50%) so it folds a large chunk of trash and continues ~30-34%. 4bet linear-polar blend: pure value AA/KK/AKo, mostly-value QQ/AKs, balanced by low-suited-ace blocker bluffs A5s/A4s (top of mix), then A3s/A2s thinner. Bluffs are SUITED aces; offsuit-ace 4bet bluffs are minimal IP (only a sliver of A5o). JJ/TT and QQ remainder flat IP to keep the cold-4bet range from being face-up. Wide IP flatting range realizes equity well: pairs 22-JJ (22-99 near-pure calls closing action for set value, only low pairs start folding a little), suited broadways AQs-KTs/QJs/JTs, AQo sometimes, plus suited connectors/gappers (T9s 98s 87s 76s 65s 54s J9s) as set/straight miners. Weak offsuit broadways (KJo/ATo/AJo) and offsuit aces below AQo mostly fold. Study-grade approximations aligned with published solver charts; marginal hands intentionally mixed.

### BTN open vs BB 3bet

**Range ≈ ~6-8% 4bet, ~28-34% call, rest fold** ｜ Sizing: 4bet to ~21-23bb ｜ 主アクション: 4bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 4* | 4* | C* | C* | C* | C* | C* | C* | C* | C* | C* | C* | C* |
| **K** | 4* | 4* | C* | C* | C* | C* | C* | C* | C* | C* |   |   |   |
| **Q** | C* | C* | 4* | C* | C* | C* | C* |   |   |   |   |   |   |
| **J** | C* | C* | C* | C* | C* | C* | C* |   |   |   |   |   |   |
| **T** | C* | C* | C* | C* | C* | C* | C* |   |   |   |   |   |   |
| **9** | C* |   |   |   | C* | C* | C* | C* |   |   |   |   |   |
| **8** |   |   |   |   |   |   | C* | C* | C* |   |   |   |   |
| **7** |   |   |   |   |   |   |   | C | C* | C* |   |   |   |
| **6** |   |   |   |   |   |   |   |   | C* | C* |   |   |   |
| **5** |   |   |   |   |   |   |   |   |   | C* | C* |   |   |
| **4** |   |   |   |   |   |   |   |   |   |   | C* | C* |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   | C* |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   | C* |

**Mixed:** AA: 4bet 92% / call 8% · AKs: 4bet 75% / call 25% · AQs: 4bet 30% / call 70% · AJs: 4bet 12% / call 88% · ATs: 4bet 8% / call 92% · A9s: 4bet 5% / call 90% / fold 5% · A8s: 4bet 5% / call 85% / fold 10% · A7s: 4bet 3% / call 80% / fold 17% · A6s: 4bet 5% / call 78% / fold 17% · A5s: 4bet 38% / call 57% / fold 5% · A4s: 4bet 32% / call 58% / fold 10% · A3s: 4bet 22% / call 58% / fold 20% · A2s: 4bet 12% / call 58% / fold 30% · AKo: 4bet 68% / call 32% · KK: 4bet 85% / call 15% · KQs: 4bet 18% / call 82% · KJs: 4bet 12% / call 88% · KTs: 4bet 6% / call 92% / fold 2% · K9s: 4bet 3% / call 80% / fold 17% · K8s: call 52% / fold 48% · K7s: call 38% / fold 62% · K6s: call 28% / fold 72% · K5s: call 22% / fold 78% · AQo: 4bet 15% / call 80% / fold 5% · KQo: 4bet 3% / call 72% / fold 25% · QQ: 4bet 55% / call 45% · QJs: 4bet 8% / call 90% / fold 2% · QTs: 4bet 6% / call 92% / fold 2% · Q9s: 4bet 3% / call 82% / fold 15% · Q8s: call 52% / fold 48% · AJo: 4bet 3% / call 80% / fold 17% · KJo: call 50% / fold 50% · QJo: call 42% / fold 58% · JJ: 4bet 20% / call 80% · JTs: 4bet 8% / call 90% / fold 2% · J9s: 4bet 3% / call 82% / fold 15% · J8s: call 52% / fold 48% · ATo: call 60% / fold 40% · KTo: call 30% / fold 70% · QTo: call 28% / fold 72% · JTo: call 32% / fold 68% · TT: 4bet 10% / call 90% · T9s: call 90% / fold 10% · T8s: call 65% / fold 35% · A9o: call 25% / fold 75% · T9o: call 22% / fold 78% · 99: 4bet 5% / call 95% · 98s: call 85% / fold 15% · 97s: call 55% / fold 45% · 88: 4bet 3% / call 97% · 87s: call 82% / fold 18% · 86s: call 45% / fold 55% · 76s: call 75% / fold 25% · 75s: call 35% / fold 65% · 66: call 98% / fold 2% · 65s: call 70% / fold 30% · 55: call 95% / fold 5% · 54s: call 58% / fold 42% · 44: call 90% / fold 10% · 43s: call 28% / fold 72% · 33: call 80% / fold 20% · 22: call 75% / fold 25%

> BTN is the in-position cold-caller here, so the defining trait is a very LARGE flat range — BTN profitably continues with a huge chunk of its opening range by just calling in position. 4bet frequency stays modest (~6-8%): linear-leaning value (AA/KK near-pure, QQ/AKs/AKo as the main mix) plus a blocker-bluff layer concentrated in suited aces (A5s/A4s/A3s, some A2s) that block BB's strong aces and unblock folds. KEY FIX vs the draft: the 4bet bluff layer was scattered onto weak Kx (K5s/K6s/K7s) and suited connectors (T9s/98s/87s/76s/65s/54s) at 3-5% — that is noise. At 100bb in a 4bet-or-call spot in position, those hands prefer pure-flat (they realize equity well and are poor 4bet bluffs since they don't block BB's continue range); converted to call. Also trimmed the very bottom of the Kx flat range (K5s/K6s/K7s) which is too thin vs a 3bet+cap even in position, and tightened a few thin offsuit/connector flats. AA/KK kept near-pure with a small flat slice to protect the calling range and trap an over-aggressive BB. QQ/JJ/AKs are the main mixing pivot. Offsuit hands fold far more than suited equivalents. Percentages are approximate, study-grade references with realistic mixing, not exact solver output; adjust 4bet bluff frequency up vs a BB that folds too much to 4bets and down vs a BB that 5bet-jams or calls 4bets too light.

### CO open vs BTN 3bet

**Range ≈ 4bet ~5%, call ~8%, rest fold** ｜ Sizing: 4bet to ~21bb ｜ 主アクション: 4bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 4 | 4* | C* | C* | C* | C* | C* | C* | C* | 4* | 4* | 4* | 4* |
| **K** | 4* | 4 | C* | C* | C* | C* | C* |   |   |   |   |   |   |
| **Q** | C* | C* | 4* | C* | C* | C* | C* |   |   |   |   |   |   |
| **J** | C* | C* |   | C* | C* | C* | C* |   |   |   |   |   |   |
| **T** | C* |   |   |   | C* | C* | C* |   |   |   |   |   |   |
| **9** |   |   |   |   |   | C* | C* | C* |   |   |   |   |   |
| **8** |   |   |   |   |   |   | C* | C* | C* |   |   |   |   |
| **7** |   |   |   |   |   |   |   | C* | C* | C* |   |   |   |
| **6** |   |   |   |   |   |   |   |   | C* | C* | C* |   |   |
| **5** | 4* |   |   |   |   |   |   |   |   | C* | C* |   |   |
| **4** | 4* |   |   |   |   |   |   |   |   |   | C* |   |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   | C* |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   | C* |

**Mixed:** AKs: 4bet 90% / call 10% · AQs: 4bet 45% / call 55% · AJs: 4bet 22% / call 72% / fold 6% · ATs: 4bet 15% / call 72% / fold 13% · A9s: 4bet 8% / call 24% / fold 68% · A8s: 4bet 8% / call 18% / fold 74% · A7s: 4bet 6% / call 14% / fold 80% · A6s: 4bet 5% / call 10% / fold 85% · A5s: 4bet 50% / call 22% / fold 28% · A4s: 4bet 45% / call 20% / fold 35% · A3s: 4bet 35% / call 15% / fold 50% · A2s: 4bet 22% / call 10% / fold 68% · AKo: 4bet 72% / call 28% · KQs: 4bet 28% / call 68% / fold 4% · KJs: 4bet 18% / call 64% / fold 18% · KTs: 4bet 12% / call 58% / fold 30% · K9s: 4bet 7% / call 28% / fold 65% · K8s: call 14% / fold 86% · AQo: 4bet 35% / call 45% / fold 20% · KQo: 4bet 14% / call 34% / fold 52% · QQ: 4bet 85% / call 15% · QJs: 4bet 14% / call 64% / fold 22% · QTs: 4bet 10% / call 58% / fold 32% · Q9s: 4bet 6% / call 30% / fold 64% · Q8s: 4bet 3% / call 14% / fold 83% · AJo: 4bet 12% / call 30% / fold 58% · KJo: 4bet 6% / call 14% / fold 80% · JJ: 4bet 14% / call 84% / fold 2% · JTs: 4bet 12% / call 68% / fold 20% · J9s: 4bet 7% / call 40% / fold 53% · J8s: 4bet 3% / call 14% / fold 83% · ATo: 4bet 7% / call 22% / fold 71% · TT: 4bet 4% / call 90% / fold 6% · T9s: 4bet 10% / call 52% / fold 38% · T8s: 4bet 5% / call 24% / fold 71% · 99: call 84% / fold 16% · 98s: 4bet 7% / call 46% / fold 47% · 97s: 4bet 3% / call 16% / fold 81% · 88: call 66% / fold 34% · 87s: 4bet 6% / call 44% / fold 50% · 86s: 4bet 2% / call 14% / fold 84% · 77: call 55% / fold 45% · 76s: 4bet 5% / call 42% / fold 53% · 75s: 4bet 2% / call 10% / fold 88% · 66: call 42% / fold 58% · 65s: 4bet 4% / call 36% / fold 60% · 64s: call 12% / fold 88% · A5o: 4bet 8% / fold 92% · 55: call 30% / fold 70% · 54s: 4bet 4% / call 28% / fold 68% · A4o: 4bet 5% / fold 95% · 44: call 20% / fold 80% · 33: call 14% / fold 86% · 22: call 12% / fold 88%

> CO is OOP vs BTN's IP 3bet, so it defends tighter and 4bets a polarized range (value + wheel-ace bluffs) rather than flatting wide. Value: AA/KK pure 4bet, QQ mostly 4bet, AKs/AKo mostly 4bet, with thin merges of JJ/AQs/KQs. Bluffs are drawn primarily from suited wheel aces (A5s-A2s) which have the best removal against AA/KK/AK plus good board coverage and poor OOP flatting EV. The calling core is medium-strong: TT-99 pure call, JJ mostly call, broadway suited (KQs/KJs/QJs/JTs/KTs/QTs), suited connectors, and small pairs that set-mine. Marginal offsuit broadways and weak suited hands fold most of the time given the OOP disadvantage vs an IP 3bettor. Against a BTN that overfolds to 4bets, add bluffs; against a station, drop bluffs and just flat/4bet for value.

### UTG open vs BTN 3bet

**Range ≈ 4bet ~5% / call ~6% of UTG opening range** ｜ Sizing: 4bet to ~21bb ｜ 主アクション: 4bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 4 | 4* | C* | C* | C* |   |   |   |   | 4* | 4* |   |   |
| **K** | 4* | 4 | C* | C* |   |   |   |   |   |   |   |   |   |
| **Q** | C* |   | 4* | C* |   |   |   |   |   |   |   |   |   |
| **J** |   |   |   | C* |   |   |   |   |   |   |   |   |   |
| **T** |   |   |   |   | C* |   |   |   |   |   |   |   |   |
| **9** |   |   |   |   |   | C* |   |   |   |   |   |   |   |
| **8** |   |   |   |   |   |   | C* |   |   |   |   |   |   |
| **7** |   |   |   |   |   |   |   |   |   |   |   |   |   |
| **6** |   |   |   |   |   |   |   |   |   |   |   |   |   |
| **5** |   |   |   |   |   |   |   |   |   |   |   |   |   |
| **4** |   |   |   |   |   |   |   |   |   |   |   |   |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   |   |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   |   |

**Mixed:** AKs: 4bet 80% / call 20% · AQs: 4bet 25% / call 65% / fold 10% · AJs: 4bet 5% / call 50% / fold 45% · ATs: call 40% / fold 60% · A5s: 4bet 50% / call 10% / fold 40% · A4s: 4bet 20% / call 10% / fold 70% · AKo: 4bet 75% / call 25% · KQs: 4bet 5% / call 65% / fold 30% · KJs: call 35% / fold 65% · AQo: 4bet 5% / call 30% / fold 65% · QQ: 4bet 85% / call 15% · QJs: call 25% / fold 75% · JJ: 4bet 15% / call 85% · TT: 4bet 5% / call 80% / fold 15% · 99: call 50% / fold 50% · 88: call 25% / fold 75%

> UTG facing a BTN 3bet OOP, 100bb. As the tightest opener, UTG's continuing range is strong and value-leaning. 4bet to ~21bb is value (QQ+, AK) plus a small bluff slice (A5s primarily, some A4s) that blocks AA/AK/Ax 3bet-value while keeping nut-flush potential. AA/KK pure 4bet; QQ/AK mix toward 4bet (QQ ~85/15, AKs ~80/20, AKo ~75/25, all pure-continue with zero fold). Flat-call region: JJ-TT, AQs, KQs, some AJs/99. JJ never folds (pure continue, mostly call). Marginal broadways (AQo, KJs, QJs, ATs) defend at low frequency and mostly fold to the 3bet given OOP disadvantage and a tight perceived range. Everything not listed is a pure fold. Approximate study-grade references, not exact solver output.

### SB open vs BB 3bet

**Range ≈ 4bet ~7-9% of hands (value + bluffs); call ~7-9%; fold the rest. Out of the original ~40-45% SB open, the continuing range vs a 3bet is roughly 15-18%.** ｜ Sizing: 4bet to ~24-26bb ｜ 主アクション: 4bet

|   | A | K | Q | J | T | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 4* | 4* | C* | C* | C* | C* | C* |   |   | 4* | 4* | 4* | 4* |
| **K** | 4* | 4* | C* | C* | C* | C* |   |   |   |   |   |   |   |
| **Q** | C* | C* | 4* | C* | C* | C* |   |   |   |   |   |   |   |
| **J** | C* | C* |   | C* | C* | C* |   |   |   |   |   |   |   |
| **T** | C* |   |   |   | C* | C* | C* |   |   |   |   |   |   |
| **9** |   |   |   |   |   | C* | C* |   |   |   |   |   |   |
| **8** |   |   |   |   |   |   | C* | C* |   |   |   |   |   |
| **7** |   |   |   |   |   |   |   | C* | C* |   |   |   |   |
| **6** |   |   |   |   |   |   |   |   | C* | C* |   |   |   |
| **5** |   |   |   |   |   |   |   |   |   | C* | C* |   |   |
| **4** |   |   |   |   |   |   |   |   |   |   | C* |   |   |
| **3** |   |   |   |   |   |   |   |   |   |   |   | C* |   |
| **2** |   |   |   |   |   |   |   |   |   |   |   |   | C* |

**Mixed:** AA: 4bet 94% / call 6% · AKs: 4bet 78% / call 22% · AQs: 4bet 40% / call 57% / fold 3% · AJs: 4bet 22% / call 60% / fold 18% · ATs: 4bet 15% / call 58% / fold 27% · A9s: 4bet 8% / call 32% / fold 60% · A8s: 4bet 6% / call 24% / fold 70% · A5s: 4bet 48% / call 27% / fold 25% · A4s: 4bet 42% / call 26% / fold 32% · A3s: 4bet 32% / call 22% / fold 46% · A2s: 4bet 20% / call 18% / fold 62% · AKo: 4bet 58% / call 42% · KK: 4bet 90% / call 10% · KQs: 4bet 25% / call 62% / fold 13% · KJs: 4bet 15% / call 52% / fold 33% · KTs: 4bet 10% / call 44% / fold 46% · K9s: 4bet 5% / call 20% / fold 75% · AQo: 4bet 18% / call 50% / fold 32% · KQo: 4bet 6% / call 22% / fold 72% · QQ: 4bet 68% / call 32% · QJs: 4bet 12% / call 52% / fold 36% · QTs: 4bet 10% / call 47% / fold 43% · Q9s: 4bet 4% / call 26% / fold 70% · AJo: 4bet 6% / call 20% / fold 74% · KJo: call 6% / fold 94% · JJ: 4bet 28% / call 72% · JTs: 4bet 12% / call 56% / fold 32% · J9s: 4bet 4% / call 28% / fold 68% · ATo: call 10% / fold 90% · TT: 4bet 12% / call 86% / fold 2% · T9s: 4bet 7% / call 48% / fold 45% · T8s: 4bet 3% / call 22% / fold 75% · 99: 4bet 5% / call 85% / fold 10% · 98s: 4bet 5% / call 42% / fold 53% · 88: 4bet 2% / call 68% / fold 30% · 87s: 4bet 4% / call 36% / fold 60% · 77: call 52% / fold 48% · 76s: 4bet 3% / call 28% / fold 69% · 66: call 38% / fold 62% · 65s: 4bet 2% / call 22% / fold 76% · 55: call 25% / fold 75% · 54s: 4bet 2% / call 15% / fold 83% · 44: call 18% / fold 82% · 33: call 12% / fold 88% · 22: call 10% / fold 90%

> SB is OOP postflop, so the strategy leans 4bet-or-fold but still keeps a meaningful calling range (SB closes action). Value 4bets: AA/KK near-pure (small trap kept to protect the calling range), QQ and AKs heavy, AKo mixed. Critically, premiums and strong continues never fold to a 3bet at 100bb: AA/KK/QQ/JJ and AKs/AKo have foldPct 0, and TT/99 fold only marginally. Bluff 4bets are anchored by A5s-A2s (wheel + nut-flush blocker, best playability) plus a few suited-broadway/Ax blockers (A4s, KQs); K5s was removed as too thin a bluff and replaced/normalized with stronger A-blocker bluffs. AKo corrected to pure-continue (was incorrectly 5% fold). Calling range = JJ-22 set-mines (small pairs at low freq), suited broadways (AQs/AJs/KQs/KJs/QJs/QTs/JTs), AKo flat, and suited connectors that retain equity OOP. Frequencies are approximate study-grade references; exact mixes shift with BB 3bet size (assumed ~10-11bb) and population reads. vs a tight 3bettor, drop the lighter A-blocker bluffs and call tighter; vs a loose/aggressive 3bettor, push QQ/AKo toward pure 4bet and add more Ax/Kx blocker bluffs.


---

## 整合性チェック / 注意点

Here is the consistency review of these GTO preflop summaries:

1. **CO-vs-UTG continue range looks too narrow / value-light.** CO continues only ~12% total (7% 3bet + 5% flat) vs a 16% UTG open. Against a strong UTG range that is defensible, but the 5% flat is unusually thin — most solvers flat more (small/medium pairs, suited Broadways) IP in a 6-max single-raised pot. Treat the 5% as a floor, not gospel; cold-call width here is rake- and population-dependent.

2. **BTN-vs-UTG vs BTN-vs-CO 3bet sizing is inconsistent in spirit.** BTN 3bets to ~7.5bb vs UTG (3.3x) but to ~8bb vs CO (per the wider-opener line). You should 3bet LARGER vs earlier (tighter) openers and can go slightly smaller vs later (wider) openers because their range folds more / you have more fold equity. The listed sizings are nearly flat — fine as an approximation, but don't infer a real strategic gradient from them.

3. **Defender 3bet% vs opener width ordering is slightly off for BB.** BB 3bets ~8% vs UTG, ~11% vs MP, ~13% vs CO, ~15% vs BTN, ~16% vs SB. That monotonic widening is correct in direction, but the BB-vs-UTG 8% may be high relative to how tight UTG is — vs a 16% open many solvers 3bet closer to ~6-7% from the BB. Minor; direction is right, magnitude is the caveat.

4. **SB RFI at 43% with 3bb size is a "raise-or-fold" simplification — internalize that it's NOT a true GTO node.** True SB strategy mixes limps. The 43% raise-or-fold is a practical heuristic; against tough BBs who over-3bet, this range gets exploited. Flagged correctly as raise-or-fold, but remember the limp strategy is being suppressed here.

5. **BB total-defense numbers vs SB (78%+) and BTN (62%) are getting close to "defend everything," which is correct only because BB closes the action and gets a price.** Caveat: these huge flat ranges are highly playability-dependent post-flop. 78% defense vs a 3bb SB open is theoretically near-right but is the single most-punished spot for weak players post-flop — don't read "defend 78%" as "this is easy."

6. **4bet sizing scales correctly with 3bet size (good), but OOP vs IP isn't differentiated.** SB-open-vs-BB-3bet 4bets to ~24-26bb (larger, because SB is OOP and 3bet came from BB closing) vs BTN-vs-3bet 4bets to ~22-24bb. The summaries do bump OOP 4bets larger — consistent. Just note all 4bet bluffs here lean on suited-ace/blocker hands; without those exact combos the 4bet frequency is wrong.

7. **BTN RFI 45% and BTN-vs-CO continue (~36% total) are mutually coherent, but SB-vs-CO and SB-vs-BTN being 3bet-or-fold while BTN-vs-CO allows flatting is the key positional lesson.** Make sure you understand WHY: BTN can flat CO because BTN is IP and closes to position; SB cannot profitably flat (OOP, BB can squeeze), hence 3bet-or-fold. This is correct in the data — flagging it as the load-bearing concept, not an error.

8. **Open sizing of 2.3bb uniformly UTG→CO is a modern small-ball convention, not universal.** Many solver solutions use larger early-position opens (2.5x) and the BB-defense / IP-continue ranges are calibrated to the opening size. If you study these ranges with 2.3bb opens but play 2.5x live, your defending frequencies (especially BB flat width) should tighten modestly. Don't mix size assumptions across nodes.

Overall the set is internally coherent and directionally correct; the main study caveats are (a) the deliberately simplified SB raise-or-fold and BB mass-defend nodes, (b) thin CO-vs-UTG flat width, and (c) treating the near-flat 3bet/4bet sizings as approximations rather than a precise strategic gradient.