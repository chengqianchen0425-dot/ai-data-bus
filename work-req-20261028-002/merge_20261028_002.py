#!/usr/bin/env python3
"""Merge req-20261028-002 four routes into one normalized JSONL.
Rules (documented in merge notes):
- meeting_number: null for ALL rows. D-route's 169 schedule-order occurrence
  counts are preserved ONLY under meeting_number_schedule_order_count_unverified,
  because the request forbids deriving meeting_number from team occurrence
  counts / date order; D's basis string says exactly that, so it must not be
  carried as meeting_number.
- venue_status normalized to the request enum:
  confirmed = per-fixture venue confirmed (route tier noted; official flag separate)
  neutral   = verified neutral ground (neither team's home) -- NO route produced
              a verified neutral ground this round, so merged neutral = 0
  moved     = per-fixture venue differs from club's listed home
  conflict  = competing venue candidates, none chosen
  unavailable = venue name/candidate known but NOT fixture-verified, or identity/
              coordinates unresolved (this is where A-route 'neutral' =
              unresolved identity and D-route 'neutral' = uncontested but
              unverified season-table candidate land; original label kept in
              venue_status_route + note)
  blocked   = source blocked for that row (0 this round; FBref byte-provenance
              block is evidence-level, recorded in provenance, not row status)
- official_round_is_official: false for every row with a round value this round
  (all round labels are Soccerway / worldfootball / FBref / topscorersfootball
  cross-check labels, none is league-official wording).
- row_status_merged (uniform rule, NOT the routes' differing row_status):
  conflict if round_conflict or venue conflict or a B-route 2020 kickoff/date
    disagreement row (B row_status==conflict in 2020; the systematic +2h
    relabel rows are NOT conflicts -- B's own row_status proves it: its 451
    complete rows include every systematic row)
  complete if round + verified venue (status confirmed/moved + coords + tz) +
    kickoff all present and no unresolved kickoff disagreement
  partial  if at least one of those present but not all, or kickoff carries an
    unresolved systematic disagreement (C 2025: -004 kept, FBref systematically
    +2h, UTC withheld -- disputed, not adopted, not resolved)
  unavailable if none present (0 expected)
  Deliberately NOT carried into merged conflict:
  - C-route 'conflict' on the two 2023-04-15 moved rows: a winner venue WAS
    established by two agreeing sources (FBref+Sky); competing candidates are
    preserved in venue_competing_candidates. Route label kept verbatim.
  - D-route 'conflict' on 8 rows: that label marks meeting_number count
    disagreement (brought-forward pairs), not a field conflict; merged file
    keeps meeting_number null + the unverified schedule-order count separate.
  - kickoff_conflict_note presence in B/C: it is a change log, not a conflict
    flag (it fires on every systematic +2h correction).
- Route row_status preserved verbatim in row_status_route.
- No market data, no scores, no standings, no predictions are carried (none exist
  in route files; verified by key scan).
"""
import json, hashlib
from collections import Counter

W = "/home/hatch/workspace/ai-inbox/work-req-20261028-002/"

DOUBLE = {  # season -> (is_pure_double_round_robin, basis)
    2016: (False, "33 rounds, 3 meetings per pair (triple round-robin structure; season page Matches 1-22 / 23-33)"),
    2017: (False, "33 rounds, 3 meetings per pair (triple round-robin structure)"),
    2018: (False, "33 rounds, 3 meetings per pair (triple round-robin structure)"),
    2019: (False, "22 regular rounds + split groups of 5 (27 matches/team), not a single double round-robin"),
    2020: (True,  "22 rounds only; split series cancelled 2020-10-28 (COVID), so the season is a 22-round double round-robin"),
    2021: (False, "22 regular rounds + split groups of 5 (27 matches/team)"),
    2022: (False, "22 regular rounds (132) + two split groups single round-robin 30 (27 matches/team)"),
    2023: (False, "22 regular rounds (132) + split groups single round-robin 30 + playoffs 5 (167)"),
    2024: (False, "22 regular rounds (132) + split groups single round-robin 30 + Euro playoffs 5 + relegation playoffs 2 (169)"),
    2025: (False, "22 regular rounds (132) + relegation group single round-robin 15 + championship group double round-robin 30 (177); season as a whole is mixed"),
    2026: (False, "22 regular rounds (132) + relegation group single round-robin 15 + championship group double round-robin 30 (177); season as a whole is mixed"),
}
EXPECTED = {2016: 198, 2017: 198, 2018: 198, 2019: 162, 2020: 132, 2021: 162,
            2022: 162, 2023: 167, 2024: 169, 2025: 177, 2026: 177}

def norm_A(r):
    v = r["venue"]
    vs_route = v["venue_status"]
    if vs_route in ("confirmed", "moved"):
        vs, note = vs_route, "A-route per-fixture FBref venue column, parsed; route status kept."
    elif vs_route == "neutral":
        vs = "unavailable"
        note = ("Route label 'neutral' = venue identity NOT fully resolved (same-complex "
                "different pitch / alias unconfirmed / no coordinates); normalized to "
                "unavailable for charting; per-fixture venue name retained in venue_name.")
    else:
        vs, note = "unavailable", f"Unexpected route status {vs_route}"
    kickoff_conflict = False
    return {
        "fixture_key": r["fixture_key"], "season": int(r["season"]),
        "match_date": r["match_date"],
        "home_team": r["home_team_fbref"], "away_team": r["away_team_fbref"],
        "official_round": r["official_round"],
        "official_round_kind": "fbref_matchweek_label",
        "official_round_basis": "FBref Wk label, kept verbatim; NOT league-official wording. 2017 Wk 1-17 and 2018 Wk 3-10/19-20 are label-conflicted (see round_conflict).",
        "official_round_is_official": False,
        "round_conflict": bool(r.get("round_label_conflict")),
        "round_conflict_note": "; ".join(r.get("round_conflict_notes") or []),
        "double_round_robin": DOUBLE[int(r["season"])][0],
        "double_round_robin_basis": DOUBLE[int(r["season"])][1],
        "meeting_number": None,
        "meeting_number_schedule_order_count_unverified": None,
        "meeting_number_note": r.get("meeting_number_reason"),
        "venue_name": v.get("venue_canonical") or v.get("venue_name_fbref"),
        "venue_name_per_fixture": v.get("venue_name_fbref"),
        "venue_city": v.get("venue_city"),
        "venue_lat": v.get("venue_lat"), "venue_lon": v.get("venue_lon"),
        "venue_iana_timezone": v.get("venue_tz"),
        "venue_status": vs, "venue_status_route": vs_route,
        "venue_status_note": note + (" " + "; ".join(v.get("venue_status_notes") or []) if v.get("venue_status_notes") else ""),
        "venue_official_confirmation": False,
        "venue_competing_candidates": v.get("venue_candidates"),
        "venue_listed_home": v.get("home_club_season_listed_home"),
        "kickoff_local": r.get("kickoff_local"),
        "kickoff_timezone": r.get("kickoff_timezone"),
        "kickoff_utc": r.get("kickoff_utc"),
        "kickoff_basis": r.get("kickoff_local_semantics"),
        "kickoff_conflict": kickoff_conflict,
        "kickoff_conflict_note": None,
        "kickoff_disagreement_unresolved": False,
        "kickoff_disagreement_note": None,
        "date_as_in_req20261006_004": None,
        "meeting_number_count_disagreement": False,
        "meeting_number_count_disagreement_note": None,
        "home_club_identity": r.get("home_club"), "away_club_identity": r.get("away_club"),
        "csv_join_status": r.get("csv_join_status"),
        "row_status_route": r.get("row_status"),
        "route": "A_2016_2018",
        "provenance": r.get("provenance"),
    }

def norm_BC(r, route):
    vs_route = r.get("venue_status")
    vs = vs_route  # B/C confirmed/moved/conflict already use request semantics
    note = ""
    if vs_route == "confirmed":
        note = "Per-fixture FBref Venue column agreeing with -004 season mapping; secondary source, NOT official confirmation (venue_official_confirmation=false)."
    elif vs_route == "moved":
        note = "Per-fixture venue differs from club's listed home (fixture-level evidence)."
    elif vs_route == "conflict":
        note = "Competing venue candidates, none chosen; verified venue null."
    kc = r.get("kickoff_conflict_note")
    # B 2020 conflict rows only: B's own row_status==conflict in 2020 marks the
    # genuine unresolved kickoff/date disagreements (2 pure time + 2 date
    # corrections vs -004). Systematic +2h rows are resolved corrections.
    is_b2020_conflict = (route == "B_2019_2021" and int(r["season"]) == 2020
                         and r.get("row_status") == "conflict")
    kc_unresolved = (route == "C_2022_2025" and int(r["season"]) == 2025 and bool(kc))
    return {
        "fixture_key": r["fixture_key"], "season": int(r["season"]),
        "match_date": r.get("date"),
        "home_team": r["home_team"], "away_team": r["away_team"],
        "official_round": r.get("official_round"),
        "official_round_kind": r.get("official_round_kind"),
        "official_round_basis": r.get("official_round_source") or r.get("round_non_official_source"),
        "official_round_is_official": False if r.get("official_round") is not None else None,
        "round_conflict": (r.get("official_round_status") == "conflict"),
        "round_conflict_note": r.get("notes") if r.get("official_round_status") == "conflict" else None,
        "double_round_robin": DOUBLE[int(r["season"])][0],
        "double_round_robin_basis": DOUBLE[int(r["season"])][1],
        "meeting_number": None,
        "meeting_number_schedule_order_count_unverified": None,
        "meeting_number_note": r.get("meeting_number_attempts"),
        "venue_name": r.get("venue_verified") or r.get("venue_candidate"),
        "venue_name_per_fixture": r.get("venue_candidate"),
        "venue_city": r.get("venue_verified_city") or r.get("venue_candidate_city"),
        "venue_lat": r.get("venue_lat"), "venue_lon": r.get("venue_lon"),
        "venue_iana_timezone": r.get("venue_timezone"),
        "venue_status": vs, "venue_status_route": vs_route,
        "venue_status_note": note,
        "venue_official_confirmation": bool(r.get("venue_official_confirmation")),
        "venue_competing_candidates": r.get("venue_candidates"),
        "venue_listed_home": None,
        "kickoff_local": r.get("kickoff_local"),
        "kickoff_timezone": r.get("kickoff_timezone"),
        "kickoff_utc": r.get("kickoff_utc"),
        "kickoff_basis": r.get("kickoff_handling"),
        "kickoff_conflict": bool(is_b2020_conflict),
        "kickoff_conflict_note": kc if is_b2020_conflict else None,
        "kickoff_disagreement_unresolved": bool(kc_unresolved),
        "kickoff_disagreement_note": (kc if kc_unresolved else None),
        "date_as_in_req20261006_004": r.get("date_004_old"),
        "home_club_identity": r.get("home_club_identity"),
        "away_club_identity": r.get("away_club_identity"),
        "csv_join_status": r.get("csv_join_status"),
        "row_status_route": r.get("row_status"),
        "route": route,
        "provenance": r.get("provenance"),
    }

def norm_D(r):
    vs_route = r.get("venue_status")
    if vs_route == "neutral":
        vs = "unavailable"
        note = ("Route label 'neutral' = venue name uncontested but taken from the Wikipedia "
                "2026 season stadium table (season-level), NOT fixture-level evidence; "
                "normalized to unavailable; candidate name retained in venue_name.")
    elif vs_route == "conflict":
        vs = "conflict"
        note = "Competing venue names, none chosen; verified venue null."
    else:
        vs, note = "unavailable", f"Unexpected route status {vs_route}"
    mn = r.get("meeting_number")
    return {
        "fixture_key": r["row_key"], "season": int(r["season"]),
        "match_date": r.get("match_date"),
        "home_team": r.get("home_team_canonical"), "away_team": r.get("away_team_canonical"),
        "official_round": r.get("official_round"),
        "official_round_kind": "topsoccerersfootball_round_label",
        "official_round_basis": r.get("official_round_basis"),
        "official_round_is_official": False,
        "round_conflict": False,
        "round_conflict_note": None,
        "double_round_robin": DOUBLE[2026][0],
        "double_round_robin_basis": DOUBLE[2026][1],
        "meeting_number": None,
        "meeting_number_schedule_order_count_unverified": mn,
        "meeting_number_note": ("D-route schedule-order occurrence count (round-order and date-order "
            "agreeing) -- explicitly NOT an authoritative meeting_number: the request forbids "
            "deriving meeting_number from team occurrence counts / date order. Retained for "
            "reference only; meeting_number_published=false for all 2026 rows."),
        "venue_name": r.get("venue_name_candidate"),
        "venue_name_per_fixture": None,
        "venue_city": r.get("venue_city"),
        "venue_lat": r.get("venue_lat_wgs84"), "venue_lon": r.get("venue_lon_wgs84"),
        "venue_iana_timezone": r.get("venue_iana_timezone"),
        "venue_status": vs, "venue_status_route": vs_route,
        "venue_status_note": note,
        "venue_official_confirmation": False,
        "venue_competing_candidates": r.get("venue_competing_candidates"),
        "venue_listed_home": None,
        "kickoff_local": r.get("kickoff_local_time"),
        "kickoff_timezone": r.get("kickoff_timezone_as_published"),
        "kickoff_utc": r.get("kickoff_utc"),
        "kickoff_basis": r.get("kickoff_semantics"),
        "kickoff_conflict": False,
        "kickoff_conflict_note": None,
        "kickoff_disagreement_unresolved": False,
        "kickoff_disagreement_note": None,
        "date_as_in_req20261006_004": None,
        "meeting_number_count_disagreement": r.get("meeting_number") is None,
        "meeting_number_count_disagreement_note": r.get("row_status_reason"),
        "home_club_identity": {"founded_year_natal": r.get("home_club_founded_year_natal"),
            "competition_entry_year": r.get("home_club_competition_entry_year"),
            "lineage_note": r.get("home_club_lineage_note")},
        "away_club_identity": {"founded_year_natal": r.get("away_club_founded_year_natal"),
            "competition_entry_year": r.get("away_club_competition_entry_year"),
            "lineage_note": r.get("away_club_lineage_note")},
        "csv_join_status": r.get("csv_join_status"),
        "row_status_route": r.get("row_status"),
        "route": "D_2026",
        "provenance": r.get("provenance"),
    }

def merged_status(row):
    if row["round_conflict"] or row["venue_status"] == "conflict" or row["kickoff_conflict"]:
        return "conflict"
    has_round = row["official_round"] is not None
    has_venue = (row["venue_status"] in ("confirmed", "moved")
                 and row["venue_lat"] is not None and row["venue_lon"] is not None
                 and row["venue_iana_timezone"] is not None)
    has_kick = row["kickoff_local"] is not None
    if has_round and has_venue and has_kick and not row.get("kickoff_disagreement_unresolved"):
        return "complete"
    if has_round or has_venue or has_kick:
        return "partial"
    return "unavailable"

out = []
for fname, fn, route in [
    ("method_context_2016_2018.jsonl", norm_A, "A_2016_2018"),
    ("method_context_2019_2021.jsonl", lambda r: norm_BC(r, "B_2019_2021"), "B_2019_2021"),
    ("method_context_2022_2025.jsonl", lambda r: norm_BC(r, "C_2022_2025"), "C_2022_2025"),
    ("method_context_2026.jsonl", norm_D, "D_2026"),
]:
    for line in open(W + fname):
        line = line.strip()
        if line:
            out.append(fn(json.loads(line)))

for row in out:
    row["row_status_merged"] = merged_status(row)

# forbidden-key scan
FORB = ["score", "odds", "prediction", "standing", "goals", "result_"]
bad = [k for r in out for k in r if any(s in k.lower() for s in FORB)]
assert not bad, bad

keys = [r["fixture_key"] for r in out]
assert len(keys) == len(set(keys)), f"duplicate fixture_keys: {[k for k, c in Counter(keys).items() if c > 1][:5]}"

out.sort(key=lambda r: (r["season"], r["match_date"] or "", r["fixture_key"]))
with open(W + "method_context_rows_merged.jsonl", "w") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
sha = hashlib.sha256(open(W + "method_context_rows_merged.jsonl", "rb").read()).hexdigest()

print("TOTAL", len(out), "SHA", sha)
print("dup keys: 0")
for s in sorted(EXPECTED):
    rs = [r for r in out if r["season"] == s]
    c = Counter(r["row_status_merged"] for r in rs)
    print(s, "expected", EXPECTED[s], "discovered", len(rs),
          "complete", c.get("complete", 0), "partial", c.get("partial", 0),
          "conflict", c.get("conflict", 0), "unavailable", c.get("unavailable", 0),
          "blocked 0 missing", EXPECTED[s] - len(rs))
print("venue_status merged:", Counter(r["venue_status"] for r in out))
print("venue_official_confirmation true:", sum(1 for r in out if r["venue_official_confirmation"]))
print("meeting_number non-null:", sum(1 for r in out if r["meeting_number"] is not None))
print("meeting_number_schedule_order_count_unverified non-null:",
      sum(1 for r in out if r["meeting_number_schedule_order_count_unverified"] is not None))
print("official_round non-null:", sum(1 for r in out if r["official_round"] is not None))
print("official_round null by season:",
      {s: sum(1 for r in out if r["season"] == s and r["official_round"] is None) for s in sorted(EXPECTED)})
print("kickoff non-null:", sum(1 for r in out if r["kickoff_local"] is not None))
print("venue coords non-null:", sum(1 for r in out if r["venue_lat"] is not None and r["venue_lon"] is not None))
print("row_status_merged total:", Counter(r["row_status_merged"] for r in out))
