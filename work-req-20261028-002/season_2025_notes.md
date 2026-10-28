# req-20261028-002 — Veikkausliiga 2025: cross-check + gap-fill notes

Scope rule obeyed: pre-match facts only. No scores, results, standings-as-evidence,
odds or predictions are written into any fixture row. Where a post-season table is
mentioned below (e.g. a club's final position), it is flagged as post-season
context only and is never used to infer a fixture fact.

## Counts

- expected (from -004 baseline): 177
- discovered / delivered: 177
- complete: 0
- partial: 170
- conflict: 7
- unavailable: 0 rows in full (but meeting_number is unavailable on all 177 rows,
  and kickoff_utc is withheld on all 177 rows — see below)
- blocked: 0 rows (official-source access is the blocker for upgrades, not for rows)
- missing: 0 (no -004 row is missing, no extra fixture was invented)
- -004 rows carried unchanged (date / home / away / kickoff / display round): 177
- identity overwrites (old value replaced by a stronger value): 0
- new rows added beyond -004: 0
- round values filled from missing: 0 — all 177 already had a display round in -004;
  what changed is the honest relabelling of its source (see below), plus the new
  `series_or_phase` field on all 177 rows.

## 1. The 177 = 132 + 15 + 30 answer (format, sourced, not guessed)

2025 was NOT a plain double round-robin, and it was NOT 132 + 30 = 162 either.

- Regular season: 12 teams, each pair home and away, 22 rounds × 6 = **132** matches.
  After round 22 the league split into a top six and a bottom six, points carried over.
- Relegation round: bottom six, **single** round-robin, 5 weeks × 3 = **15** matches;
  each bottom-six team finished on 27 matches.
- Championship round: top six, **double** round-robin (home and away), 10 weeks × 3
  = **30** matches; each top-six team finished on 32 matches.
- Total: 132 + 15 + 30 = **177**. The "missing 15" in the task's 162 framing are
  exactly the second half of the double championship round.

Sources: Wikipedia "Veikkausliiga" Structure section (curl bytes, 2026-10-28,
sha256 25b048575b0f2386b02e62e902c88da43e892f44b2d1ac1336caf10b53122161):
"After 22 rounds … the last six teams will play a single relegation round,
totalling 27 matches, and the six best teams continue to a double championship
round, totalling 32 matches", announced late November 2024 with the Europa
Play-offs abolished for 2025. Corroborated arithmetically by the FBref fixture
list (132 Regular-season rows, 30 Championship-round rows, 15 Relegation-round
rows) and by the 2025 season page's own per-group tables (top six on 32 played,
bottom six on 27 played).

Warnings about two stale/superseded sources that must NOT be used for the format:
- The 2025 season page infobox still says "Matches 162" and "5 April – 26 October"
  in the snapshot read — inconsistent with its own championship table (32 games
  per top-six team) and with the 9 November final fixtures. It is a stale
  mid-season snapshot, not evidence against 177.
- A pre-season Soccerway preview describes both split groups as five matches.
  That description was superseded by the November 2024 format change and is not
  used anywhere in the output.

## 2. Rounds 28–32 (15 fixtures): what they are

They are NOT a play-off, NOT a Europa League play-off, and NOT an extra series
outside the championship round. They are the **second half of the double
Championship round**:

| -004 display round | FBref Championship week | Fixtures (date, home–away, -004 kickoff) |
|---|---|---|
| 28 | week 6 | 2025-10-16 Ilves–KuPS 16:00; 2025-10-22 Inter Turku–Gnistan 16:00; 2025-10-22 HJK–SJK 17:00 |
| 29 | week 7 | 2025-10-25 Gnistan–Ilves 15:00; 2025-10-26 HJK–Inter Turku 15:00; 2025-10-27 SJK–KuPS 16:00 |
| 30 | week 8 | 2025-10-30 Inter Turku–SJK 16:00; 2025-10-30 KuPS–Gnistan 16:00; 2025-10-30 Ilves–HJK 17:00 |
| 31 | week 9 | 2025-11-02 KuPS–Inter Turku 14:00; 2025-11-03 Ilves–SJK 16:00; 2025-11-03 Gnistan–HJK 17:00 |
| 32 | week 10 | 2025-11-09 HJK–KuPS 13:00; 2025-11-09 Inter Turku–Ilves 13:00; 2025-11-09 SJK–Gnistan 13:00 |

Why only 3 per round: after the Relegation round ended with its week 5
(18 October), only the six Championship-round teams were still playing, so each
week had 6 teams / 2 = 3 fixtures. The same logic explains display rounds 23–27
(6 fixtures each): each of those calendar windows bundled one Championship week
AND one Relegation week. The per-fixture split for 23–27 is encoded in
`series_or_phase` in the JSONL (Championship weeks 1–5 + Relegation weeks 1–5).

Two cautions, both preserved in the data rather than smoothed over:
- Display round ≠ phase week ≠ date order. Example: display 28's Ilves–KuPS
  (Championship week 6, 16 October) was played BEFORE Championship week 5
  (19 October). A moved/early fixture keeps its week label; nobody re-numbered
  anything from date order in this round.
- The Finnish name of the split groups is not asserted: secondary sources differ
  (Mestaruussarja is consistent for the top group; the bottom group appears as
  both Haastajasarja and Karsintasarja in secondary material). Only the English
  "Championship round / Relegation round" labels from FBref are used.

## 3. Official round: NOT upgraded

`official_round` keeps the -004 values 1–32 on all 177 rows, but
`official_round_source` is now honestly
`worldfootball_matchday_non_official` and `official_round_status` is
`from_req-20261006-004` on every row. No row was upgraded to an official
KIERROS label, because no official round source was accessible in this round
(see "Failed sources"). FBref's Wk column is also a secondary label, not an
official KIERROS record, so it was used only for `series_or_phase`, never to
relabel `official_round`.

## 4. Meeting number: null on all 177 rows

`meeting_number` = null, `meeting_number_status` = "unavailable" on every row.
FBref's Wk is a round/week label, not a meeting count, and was deliberately not
repurposed as one. No meeting number was inferred from date order, appearance
counts, standings or odds. Attempted sources: FBref Wk, WorldFootball matchday,
official KIERROS source (inaccessible — see below).

## 5. Kickoff times: carried, with a systematic unresolved conflict

-004 kickoff times and the Europe/Helsinki label are carried verbatim on all
177 rows (including odd minutes such as 17:23 and 17:31, which are not typos:
FBref shows the same minutes). `kickoff_utc` is null on all rows, deliberately:
FBref shows the same minutes but systematically **+2 hours** in every spot check
(e.g. Ilves–HJK 13:00 → 15:00; KuPS–AC Oulu 17:23 → 19:23; AC Oulu–VPS
21:00 → 23:00), in April as well as October/November, while FBref states no
timezone for its Time column. A constant +2h offset cannot be a Helsinki
summer/winter conversion, so one of the two conventions is unstated. Converting
-004 times to UTC on the strength of an unverified local label would launder
that conflict, so no UTC value is emitted. This is the single largest
unresolved item for downstream use: do not treat `kickoff_local` as verified
local time until an official match page or club announcement settles the
convention. The conflict is recorded per-row in `kickoff_conflict_note` and in
provenance.

## 6. Venues: match-level secondary confirmation 170, conflict 7, official 0

- Official league/club match-page confirmations: **0**. No official match page
  was obtained for any 2025 fixture in this round (see failed sources).
- FBref match-level Venue column agrees with the -004 season mapping: **170**
  rows. These rows have `venue_verified` set and `venue_status` = "confirmed",
  but the evidence tier is recorded as
  `fbref_match_level_secondary_agrees_with_season_mapping` — "confirmed" here
  means "a match-level secondary source agrees with the season mapping", NOT
  "confirmed by the league/club". Coordinates are carried from -004
  `venue-coords.json` with that provenance noted, not re-geocoded.
- Conflict: **7** rows, all FF Jaro home games from 25 July 2025 onward
  (2025-07-25 vs VPS; 2025-08-09 vs Haka; 2025-08-18 vs SJK; 2025-08-24 vs KuPS;
  2025-09-14 vs AC Oulu; 2025-09-28 vs Mariehamn; 2025-10-03 vs Haka).
  For these, `venue_verified` = null, `venue_status` = "conflict", coordinates
  null, and all three competing candidates are retained:
  (a) Jakobstads Centralplan — -004 season mapping and Sportradar match pages;
  (b) "Länsikenttä TN" — FBref match-level Venue column;
  (c) Project Liv Arena (Pietarsaari Football Stadium) — Wikipedia stadium
  history: opened 2025, first men's match FF Jaro vs VPS on 25 July 2025,
  coordinates 63.672, 22.694.
  (b) and (c) are NOT merged: it is unproven that FBref's "Länsikenttä TN" label
  denotes the new arena. Jaro home games before 25 July (e.g. 20 July vs Ilves)
  agree on Centralplan in both FBref and Sportradar and are not conflicted.
- Same-ground aliases retained as candidates, not conflicts: VPS
  Hietalahti / Elisa Stadion / Lemonsoft Stadion; KuPS Väre Areena /
  Savon Sanomat Areena; HJK Bolt Arena / Telia 5G-areena (per -004
  venue-coords notes).
- Method limit, stated plainly: FBref curl returned HTTP 403, so the FBref
  fixture list could not be parsed programmatically; the 170/7 split rests on a
  visual read of FBref's first fixture table (text layer, sha256 null by rule).
  A programmatic re-parse from an accessible copy should re-verify the venue
  column before any downstream use that treats "confirmed" as strong evidence.

## 7. Club identities (per team, independent facts only)

Founding years are Wikipedia club-infobox values from curl-downloaded bytes
(shas in each row's `home_club_identity.source` /
`away_club_identity.source`); similar names were not merged
(Inter Turku ≠ TPS; HJK ≠ any other Helsinki club).

- AC Oulu 2002; Gnistan 1924; HJK 19 June 1907; Haka 1934; Inter Turku 1990;
  Jaro 1965; KuPS 1923; IFK Mariehamn 1919; SJK 5 November 2007; VPS 1924.
- Ilves 1931 — CAVEAT: the fetched "Ilves" page is the ice-hockey infobox;
  a separate football-club founding year was not verified, so 1931 is recorded
  only as the sports-club year.
- KTP founding year — NOT VERIFIED (fetched "KTP" page is a disambiguation
  page, no infobox). No year is asserted; a remembered 1927 was deliberately
  not used.
- 2025 entry changes, relative to 2024 (2025 season page, Team changes, curl
  sha a8ee01701e6d6b650efacf30fdd2076743a4ad52bf69c2a9323745f986875e5c):
  promoted in: KTP (2024 Ykkösliiga champions, returning after a single-season
  absence) and FF Jaro (2024 Veikkausliiga play-off winners, returning after a
  nine-year absence); relegated out: EIF/Ekenäs (2024 bottom-placed, after a
  single season) and FC Lahti (2024 play-off losers, after a 13-year top-flight
  stint). The other ten teams are described only collectively ("ten teams
  remaining from the previous season"); no per-club history beyond the infobox
  year is claimed for them.
- AC Oulu current-infobox ground (Heinäpää) is a present-day value and was NOT
  used for any 2025 venue; 2025 AC Oulu venue evidence remains Raatti/Raatin
  Stadion.

## 8. CSV join

All 177 rows: `csv_join_status` =
"matched_to_req-20261006-004_row_csv_join_pending". The requester's identity
CSV (Windows path) does not exist on this VM and could not be read. No fuzzy
matching was attempted; any row that had not matched -004 would have been
recorded unresolved, but none fell in that bucket — all 177 matched -004 by
fixture_key.

## 9. Uncovered / conflict list

- Conflict rows (7): the Jaro venue rows listed in §6.
- Partial rows (170): blocked from "complete" by three independent gaps —
  (i) official_round still non-official, (ii) meeting_number unavailable,
  (iii) kickoff_utc withheld over the +2h convention conflict — plus the
  absence of any official match-page venue confirmation.
- Unverified club facts: KTP founding year; Ilves football-club founding year
  (sports-club year only); Finnish names of the split groups.

## 10. Attempted but failed sources

- veikkausliiga.com / Tulospalvelu (tulospalvelu.palloliitto.fi): official
  KIERROS labels and official match pages — not accessible to this subagent
  (JS-heavy / previously reported Cloudflare/500 behaviour; no bulk extraction
  path in this round). This is the maximum obstacle: it blocks the official
  round upgrade, meeting numbers, and official venue confirmations alike.
- WorldFootball.net: curl previously 403 per -004; not re-used as byte evidence
  in this round. Its matchday grouping is carried only via -004 and relabelled
  non-official.
- FBref: curl HTTP 403 (3,334-byte block page) on 2026-10-28, so no byte hash
  exists for it; all FBref evidence in this round is text-layer only
  (sha256 null, stated per row).
- Wikipedia: curl HTTP 200. Byte shas used: 2025 season page
  a8ee01701e6d6b650efacf30fdd2076743a4ad52bf69c2a9323745f986875e5c;
  Veikkausliiga structure page
  25b048575b0f2386b02e62e902c88da43e892f44b2d1ac1336caf10b53122161;
  per-club pages as recorded in each row's club-identity source object.
  No -004 stored hash is repeated as byte evidence anywhere: -004-carried
  fields carry sha256 null with the reason stated in provenance.

## 11. Provenance rule compliance

Every non-null field in the JSONL carries a provenance object with source_url,
final_url, retrieved_at (Asia/Shanghai, 2026-10-28), field_locator and
source_name; source_sha256 is filled ONLY for genuinely curl-downloaded
Wikipedia bytes, and is null — with the reason stated — for text-layer sources
(FBref) and for -004-carried fields. No descriptor hash is presented as a
source-evidence hash.

## Files

- `season_2025.jsonl` — 177 rows, one fixture per line.
- `season_2025_notes.md` — this file.
- Nothing was written to repo/responses/ or to any other season's files.
