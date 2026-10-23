# Live-browser re-verification log (2026-10-23, second independent rendering run)
Purpose: re-verify the 5 odds observations from req-20261022-001, as required by req-20261023-001 Q4.
Method: live browser re-opened the exact pages and read rendered tables. No login, no payment, no bet.
Note: the browser task report itself did not carry the prior values, so comparison below is done by the main agent
against the req-20261022-001 delivery (fixture_odds_rows.jsonl). Scores visible on rendered pages are NOT
recorded here and are NOT part of any odds row.

## Row-by-row comparison (all 5 CONFIRMED as rendered in this second run)
1. NowGoal 2661153, Colo-Colo vs River Plate, Quarterfinals, Bet 365, Initial filter:
   rendered HW/D/AW 3.00 / 3.10 / 2.50; Last Updated column 18-09 08:15; page top 18-09-2024 08:30 Wednesday.
   Matches prior row exactly. Page does NOT define Initial as market opening; Notes only explain HWR/DR/AWR
   calculations (calculated by live odds). Phase stays unspecified.
2. Same page, Live filter: Bet 365 HW/D/AW 3.30 / 3.00 / 2.40; Last Updated also 18-09 08:15.
   Matches prior row exactly. Page does NOT define Live as a pre-kickoff close. Phase stays unspecified.
3. BetExplorer 2025 final single-match page (palmeiras-flamengo-rj/IwUrkvRk/):
   Odds Comparison (1X2) renders exactly one bookmaker, Stake.com, 1/X/2 3.55 / 3.00 / 2.42.
   Matches prior row exactly. No Opening/Closing label; footer notes odds service in cooperation with OddsPortal.com.
4. BetExplorer 2025 results page, Palmeiras vs LDU Quito: rendered 1/X/2 1.22 / 7.40 / 14.00, dated 31.10.2025.
   Matches prior row exactly. Results table columns are date/teams/1/X/2 only; no bookmaker labelled for this row.
5. BetExplorer 2024 results page, Atletico-MG vs Botafogo RJ: rendered 1/X/2 4.33 / 3.19 / 1.90, dated 01.12.2024.
   Matches prior row exactly. No bookmaker labelled for this row.

## Date conflicts (recorded, NOT resolved, NOT converted)
- Palmeiras-Flamengo: single-match page top displays 30.11.2025 - 05:00, but the SAME page's Head-to-Head
  section displays 29.11.2025 for the same fixture (same values 3.55/3.00/2.42); results page displays 30.11.2025.
  The conflict is therefore inside BetExplorer itself, not only between checks. No timezone label was displayed
  on any of the four pages checked. Final rows keep match_date as the results/single-match-top date
  (2025-11-30) with this conflict noted; the H2H date (2025-11-29) is preserved in the conflict queue.
- Atletico-MG-Botafogo: results page in this run displays 01.12.2024, while the text-layer check in this
  round displayed 30.11.2024. Same +1-day pattern, timezone unconfirmed, not converted.
- NowGoal 2661153: displayed 18-09-2024 08:30 in both runs; the task reference date 2024-09-17 is a
  different timezone's date, still unresolved.

## Evidence limits
- Live-browser rendering yields no stable source bytes and no source HTTP status, so source_sha256 and
  http_status remain null for these 5 rows. This log file itself is the traceable record of the
  re-verification run (who/what/when/URL/values), not a hash of source bytes; it must not be presented
  as a source hash.
- Text-layer checks in this round could neither confirm nor refute these values (JS-rendered tables are
  empty in the text layer). The re-verification above rests on rendered tables, not on the text layer.
