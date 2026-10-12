# Workstream B: Pre-match Context Evidence (req-20261012-002)

**Scope:** 1,584 Swiss Super League regular-season fixtures, 2018/19–2025/26
**Source artifact audited:** `work-req-20261008-003/q2-snapshots.json`
**Date:** 2026-10-12
**Nature of data:** COMPUTED snapshots (reconstructed from published results), NOT official SFL pre-match standings. Every rank is derived and must be labeled as such.

---

## 1. Provenance (exact)

| Item | Value |
|---|---|
| Source dataset | `SWZ-current.csv` (Football-Data) |
| Source SHA-256 | `1c40b7cebed397a177643b6576f064e3c144b6d719dc9a5719636d88ca040021` |
| Source filter | `Country=Switzerland AND League=Super League AND Season in 2018/2019..2025/2026`; 2 mislabeled 2020/21 rows (actually the season's Barrage, Sion–Thun) + 9 Barrage rows excluded |
| Timezone | `Europe/Zurich`, IANA DST rules; `utc_offset` derived per kickoff date (+0200 summer / +0100 winter) |
| Kickoff rule | Snapshot = standings from all **completed** league matches with kickoff **strictly before** this fixture's kickoff (Date+Time). Fixtures sharing an identical kickoff timestamp **mutually exclude** each other (conservative). |
| Scoring | 3 points win / 1 draw / 0 loss |
| Ranking | **DERIVED**: points ↓ → goal difference ↓ → goals scored ↓; ties share rank (competition ranking 1,2,2,4). SFL official tie-breakers (e.g. head-to-head) may differ — rank is NOT official. |
| Round 1 | played=0, points=0, W=D=L=0, rank=NULL ("no matches played yet") |
| Unplayed | all fields NULL with reason (0 such fixtures — 2025/26 complete in source) |
| Score leakage | HG/AG/Res used internally for computation only; no score/result fields in output (leak scan passed per derivation block) |

## 2. Structure & coverage (verified)

- Top-level keys: `request_id, question, generated_at, derivation, coverage, per_season, excluded_rows, records`
- `records`: **1,584** (matches Q1 fixture count exactly; key alignment Q1↔Q2 = 1584/1584, zero diff)
- Record fields: `season, kickoff_local, home, away, home_pre_match{rank,played,points,W,D,L,rank_note}, away_pre_match{...}, matches_used_for_snapshot`
- Coverage: 1,572 with snapshots + 12 round-1 all-zero + 0 unplayed-null = 1,584
- Per-season: 180×5 (2018/19–2022/23) + 228×3 (2023/24–2025/26) = 1,584 ✓
- Crosswalk alignment (req-20261012-001 `fixture_source_crosswalk.csv` ↔ Q2): 1584/1584 keys match, zero diff
- Same-kickoff mutual exclusion verified live: e.g. 2018-07-28T18:00 (Grasshoppers–Zurich, Xamax–Basel) — both show `matches_used=5`, each counting only the prior round's 5 matches, not each other ✓
- 467 kickoff slots contain >1 fixture (staggered-round league); exclusion rule applied uniformly

## 3. Independent spot-check recomputation (5 fixtures)

Recomputed from scratch using the season split files in `work-req-20261009-001/SWZ-*.csv`
(independent Python implementation: strict `< kickoff` filter, 3-1-0, PTS→GD→GF, competition ranking).
All fields compared: rank, played, points, W, D, L, matches_used_for_snapshot.

| # | Fixture | Result |
|---|---|---|
| T1 | 2018/19 2018-07-21 Basel vs St. Gallen (round 1) | **PASS** — both sides zero, rank NULL, used=0 |
| T2 | 2019/20 2019-12-15 Lugano vs Young Boys | **PASS** — Lugano P17 20pts rank 6; YB P17 37pts rank 1; used=87 |
| T3 | 2020/21 2021-02-03 Sion vs St. Gallen | **PASS** — Sion P17 16pts rank 8; St. Gallen P16 23pts rank 5; used=81 (asymmetric played counts from staggered schedule, correctly handled) |
| T4 | 2022/23 2023-03-19 Lugano vs Servette (post-Forfait) | **PASS** — Lugano P24 34pts rank 4; Servette P24 35pts rank 2; used=123 |
| T5 | 2024/25 2025-05-24 Servette vs Lausanne (late Phase 2) | **PASS** — Servette P37 62pts rank 2; Lausanne P37 52pts rank 6; used=225 |

**5/5 PASS.** No discrepancies found between q2-snapshots.json and independent recomputation.

## 4. Known caveats (honest limitations)

1. **Not official snapshots.** These are computed reconstructions. SFL has never published historical pre-match standings; no official source exists to validate against. The `rank_note: "derived"` label on every record is correct and must be preserved downstream.
2. **Forfait match (2022/23 Servette–Luzern 2023-03-12).** SFL marked this fixture "Forfait" (no official score); Football-Data records it as 0–1 (Luzern win). Q2 uses the FD 0–1 result, so Luzern gets 3 points and Servette a loss in all subsequent snapshots. This follows the "use published source as-is" rule, but downstream users must know the SFL/FD conflict exists (it is recorded in the req-20261012-001 integrity manifest).
3. **Date conflict (2018/19 St. Gallen–Lugano).** FD says 2019-03-16, SFL says 2019-03-17 (Spielnummer 100302). Q2 uses the FD date; the crosswalk preserves the conflict. Snapshot membership is unaffected (both dates fall between the same neighboring rounds), but the kickoff identity differs by source.
4. **2025/26 completeness.** Source file retrieved 2026-10-09 contains a full 228-row 2025/26 season; treated as complete. If SFL later amends any result, snapshots would need recomputation.
5. **Tie-break divergence.** Derived rank uses PTS→GD→GF only. Any SFL head-to-head or other official tie-break would produce different ranks in tied cases. Rank ties in the data use shared competition ranking (1,2,2,4), which is a presentation choice, not an SFL rule.

## 5. Conclusion

`q2-snapshots.json` is **structurally sound, fully covering (1584/1584), and computationally reproducible** — 5/5 independent spot-checks pass with zero discrepancies, key alignment with Q1 and the req-20261012-001 crosswalk is exact, and the same-kickoff exclusion rule is verifiably applied. Provenance is fully documented above. The artifact is fit for use as **computed pre-match context** provided every downstream consumer retains the "derived, not official" labeling and the two known source conflicts (Forfait, date conflict).
