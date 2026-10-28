#!/usr/bin/env python3
"""req-20261028-003: join the 868-row CSV identity input to -002 merged rows.
Join key: (season, match_date, home_team, away_team) with a per-season alias
table mapping CSV short team names to merged-row team spellings.
NO string join on fixture_key (formats differ). NO fuzzy matching: a CSV row
matches iff the alias-mapped pair hits exactly one merged row on the same
season+date; 0 or >=2 hits -> unmatched, evidence null, row kept.
"""
import csv, json
from collections import defaultdict

BASE = "/home/hatch/workspace/ai-inbox/"
OUT = BASE + "work-req-20261028-003/"

# Per-season alias table: CSV short name -> merged-row team spelling.
# Derived from the observed team lists (CSV tokens vs merged spellings per
# season) + string relations (exact / strip FC / parenthetical short form /
# city-prefix / initials) and validated by the exactly-one-hit test below.
ALIAS = {
    2016: {"HIFK": "Helsinki IFK", "HJK": "HJK Helsinki", "Ilves": "Ilves",
           "Lahti": "Lahti", "Mariehamn": "IFK Mariehamn", "PS Kemi": "Kemi Kings",
           "SJK": "SJK", "VPS": "VPS"},
    2017: {"HIFK": "Helsinki IFK", "HJK": "HJK Helsinki", "Ilves": "Ilves",
           "Inter Turku": "Inter Turku", "KuPS": "KuPS", "Lahti": "Lahti",
           "Mariehamn": "IFK Mariehamn", "PS Kemi": "Kemi Kings",
           "SJK": "SJK", "VPS": "VPS"},
    2018: {"HJK": "HJK Helsinki", "Honka": "FC Honka", "Ilves": "Ilves",
           "Lahti": "Lahti", "Mariehamn": "IFK Mariehamn", "PS Kemi": "Kemi Kings",
           "SJK": "SJK", "TPS": "TPS", "VPS": "VPS"},
    2019: {"HIFK": "Helsingfors IFK", "HJK": "HJK Helsinki", "Honka": "FC Honka",
           "Ilves": "Ilves Tampere", "Lahti": "FC Lahti", "Mariehamn": "IFK Mariehamn",
           "SJK": "SJK Seinäjoki", "VPS": "Vaasan PS"},
    2020: {"HIFK": "Helsingfors IFK", "HJK": "HJK Helsinki", "Haka": "Haka Valkeakoski",
           "Honka": "FC Honka", "Ilves": "Ilves Tampere", "Lahti": "FC Lahti",
           "Mariehamn": "IFK Mariehamn", "SJK": "SJK Seinäjoki", "TPS": "TPS Turku"},
    2021: {"AC Oulu": "AC Oulu", "HIFK": "Helsingfors IFK", "HJK": "HJK Helsinki",
           "Haka": "Haka Valkeakoski", "Honka": "FC Honka", "Ilves": "Ilves Tampere",
           "KTP": "KTP", "Lahti": "FC Lahti", "Mariehamn": "IFK Mariehamn",
           "SJK": "SJK Seinäjoki"},
    2022: {"AC Oulu": "AC Oulu", "HIFK": "Helsingfors IFK", "HJK": "HJK Helsinki",
           "Haka": "Haka Valkeakoski", "Honka": "FC Honka", "Ilves": "Ilves Tampere",
           "Inter Turku": "Inter Turku", "Lahti": "FC Lahti",
           "Mariehamn": "IFK Mariehamn", "SJK": "SJK Seinäjoki",
           "TPS": None,  # no Veikkausliiga team TPS in merged 2022 (Ykkonen side)
           "VPS": "Vaasan PS"},
    2023: {"AC Oulu": "AC Oulu", "HJK": "HJK", "Haka": "Haka", "Honka": "Honka",
           "Ilves": "Ilves", "KTP": "KTP", "Lahti": "Lahti",
           "Mariehamn": "Mariehamn", "SJK": "SJK", "VPS": "VPS"},
    2024: {"AC Oulu": "AC Oulu", "Gnistan": "Gnistan", "HJK": "HJK", "Haka": "Haka",
           "Ilves": "Ilves", "Lahti": "Lahti", "Mariehamn": "Mariehamn",
           "SJK": "SJK", "VPS": "VPS"},
    2025: {"AC Oulu": "AC Oulu", "Gnistan": "Gnistan", "HJK": "HJK", "Haka": "Haka",
           "Ilves": "Ilves", "KTP": "KTP", "Mariehamn": "Mariehamn",
           "SJK": "SJK", "VPS": "VPS"},
    2026: {"AC Oulu": "AC Oulu", "Gnistan": "IF Gnistan", "HJK": "HJK Helsinki",
           "Ilves": "Ilves", "Lahti": "FC Lahti", "Mariehamn": "IFK Mariehamn",
           "SJK": "SJK Seinäjoki", "TPS": "Turun Palloseura (TPS)",
           "VPS": "Vaasan Palloseura (VPS)"},
}

csv_rows = list(csv.DictReader(open(BASE + "repo/work-req-20261028-003/fixture_identity_input.csv",
                                     encoding="utf-8-sig")))
merged = [json.loads(l) for l in open(BASE + "work-req-20261028-002/method_context_rows_merged.jsonl")]
m_by_sd = defaultdict(list)
for m in merged:
    m_by_sd[(m["season"], m["match_date"])].append(m)
m_by_key = {m["fixture_key"]: m for m in merged}
rows004 = json.load(open(BASE + "repo/work-req-20261006-004/req-20261006-004-rows.json"))["rows"]
by004 = {r["fixture_key"]: r for r in rows004}

EVID_FIELDS = ["official_round", "official_round_kind", "official_round_basis",
               "official_round_is_official", "round_conflict", "round_conflict_note",
               "double_round_robin", "double_round_robin_basis",
               "meeting_number", "meeting_number_schedule_order_count_unverified",
               "meeting_number_note",
               "venue_name", "venue_name_per_fixture", "venue_city", "venue_lat", "venue_lon",
               "venue_iana_timezone", "venue_status", "venue_status_route",
               "venue_status_note", "venue_official_confirmation",
               "venue_competing_candidates",
               "kickoff_local", "kickoff_timezone", "kickoff_utc", "kickoff_basis",
               "kickoff_conflict", "kickoff_conflict_note",
               "kickoff_disagreement_unresolved", "kickoff_disagreement_note",
               "date_as_in_req20261006_004",
               "home_club_identity", "away_club_identity",
               "row_status_merged", "row_status_route", "route"]

out = []
join_stats = {"exact_one": 0, "zero": 0, "multi": 0}
zero_rows, multi_rows = [], []
for c in csv_rows:
    season = int(c["season"])
    amap = ALIAS[season]
    mh, ma = amap.get(c["home_team"], "MISSING_TOKEN"), amap.get(c["away_team"], "MISSING_TOKEN")
    cands = []
    if mh and ma:
        cands = [m for m in m_by_sd.get((season, c["match_date"]), [])
                 if m["home_team"] == mh and m["away_team"] == ma]
    row = {"fixture_key": c["fixture_key"], "season": c["season"],
           "match_date": c["match_date"], "home_team": c["home_team"],
           "away_team": c["away_team"], "api_fixture_id": c["api_fixture_id"],
           "alias_mapped_home": mh, "alias_mapped_away": ma}
    if len(cands) == 1:
        m = cands[0]
        join_stats["exact_one"] += 1
        row["matched_merged_fixture_key"] = m["fixture_key"]
        row["join_method"] = "alias_exact_one"
        row["join_confidence"] = "exact"
        row["join_reason"] = None
        # -004 crosswalk (priority for 2019-2025): merged B/C keys are verbatim -004 keys
        if 2019 <= season <= 2025:
            r004 = by004.get(m["fixture_key"])
            if r004:
                row["matched_004_fixture_key"] = r004["fixture_key"]
                row["crosswalk_004"] = {"status": "matched",
                    "004_date": r004.get("date"), "004_kickoff": r004.get("kickoff"),
                    "004_kickoff_timezone": r004.get("kickoff_timezone"),
                    "004_official_round": r004.get("official_round"),
                    "004_venue": r004.get("venue"), "004_city": r004.get("city"),
                    "note": "merged key is verbatim the -004 key; -004 values shown so -002 corrections (kickoff +2h, 2020 date corrections, Gnistan fire relocation) are visible in-row"}
            else:
                row["matched_004_fixture_key"] = None
                row["crosswalk_004"] = {"status": "missing_in_004",
                    "note": "season in -004 scope but merged key not found in -004 rows file"}
        else:
            row["matched_004_fixture_key"] = None
            row["crosswalk_004"] = {"status": "out_of_004_scope",
                "note": "-004 covers 2019-2025 only; this season has no -004 row"}
        for f in EVID_FIELDS:
            row[f] = m.get(f)
        row["provenance_pointer"] = {
            "merged_file": "work-req-20261028-002/method_context_rows_merged.jsonl",
            "matched_merged_fixture_key": m["fixture_key"],
            "route": m.get("route"),
            "route_file": {"A_2016_2018": "method_context_2016_2018.jsonl",
                           "B_2019_2021": "method_context_2019_2021.jsonl",
                           "C_2022_2025": "method_context_2022_2025.jsonl",
                           "D_2026": "method_context_2026.jsonl"}.get(m.get("route")),
            "provenance_keys": sorted((m.get("provenance") or {}).keys())}
        row["provenance"] = m.get("provenance")
    elif len(cands) == 0:
        join_stats["zero"] += 1
        zero_rows.append(c)
        row["matched_merged_fixture_key"] = None
        row["join_method"] = "alias_exact_one_failed_zero_hit"
        row["join_confidence"] = "unresolved"
        if mh is None or ma is None:
            row["join_reason"] = (f"no merged team spelling for CSV token in season {season} "
                                  f"(home map: {mh}, away map: {ma}); no merged row can match")
        elif not m_by_sd.get((season, c["match_date"])):
            row["join_reason"] = (f"no merged rows exist at all on {c['match_date']} in season {season}; "
                                  f"merged {season} league universe ends earlier (see notes)")
        else:
            row["join_reason"] = ("alias-mapped pair found no merged row on this season+date; "
                                  "same-date merged rows are other fixtures; not fuzzy-matched")
        row["matched_004_fixture_key"] = None
        row["crosswalk_004"] = {"status": "unmatched", "note": "no merged match, hence no -004 correspondence"}
        for f in EVID_FIELDS:
            row[f] = None
        row["provenance_pointer"] = None
        row["provenance"] = None
    else:
        join_stats["multi"] += 1
        multi_rows.append((c, [m["fixture_key"] for m in cands]))
        row["matched_merged_fixture_key"] = None
        row["join_method"] = "alias_multi_hit"
        row["join_confidence"] = "unresolved"
        row["join_reason"] = f"{len(cands)} merged rows match the alias-mapped pair; not disambiguated by impression"
        row["matched_004_fixture_key"] = None
        row["crosswalk_004"] = {"status": "unmatched", "note": "multi-hit, hence no -004 correspondence"}
        for f in EVID_FIELDS:
            row[f] = None
        row["provenance_pointer"] = None
        row["provenance"] = None
    out.append(row)

with open(OUT + "method_context_rows_868.jsonl", "w") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("join:", join_stats)
print("zero rows:")
for c in zero_rows: print("  ", c["fixture_key"])
print("multi rows:", multi_rows)
# -004 verification for matched 2019-2025 rows
bad004 = [r for r in out if r["matched_merged_fixture_key"] and 2019 <= int(r["season"]) <= 2025
          and r["crosswalk_004"]["status"] != "matched"]
print("-004 correspondence failures (2019-2025 matched):", len(bad004))
# injectivity per (season,date): no two CSV rows -> same merged row
seen = {}
dup_claim = []
for r in out:
    k = r["matched_merged_fixture_key"]
    if k:
        if k in seen: dup_claim.append((k, seen[k], r["fixture_key"]))
        seen[k] = r["fixture_key"]
print("merged rows claimed twice:", dup_claim)
# uniqueness check of alias table: for each (season, token), try every other merged
# spelling in that season as the mapping; count alternatives that would ALSO give
# full exactly-one coverage for that token's rows (opponent mapping fixed).
merged_teams = defaultdict(set)
for m in merged:
    merged_teams[m["season"]].add(m["home_team"]); merged_teams[m["season"]].add(m["away_team"])
amb = []
for season, amap in ALIAS.items():
    for token, mapped in amap.items():
        if mapped is None: continue
        token_rows = [c for c in csv_rows if int(c["season"]) == season
                      and token in (c["home_team"], c["away_team"])]
        if not token_rows: continue
        alts = []
        for alt in sorted(merged_teams[season]):
            if alt == mapped: continue
            ok = True
            for c in token_rows:
                mh = alt if c["home_team"] == token else amap.get(c["home_team"])
                ma = alt if c["away_team"] == token else amap.get(c["away_team"])
                if not mh or not ma: ok = False; break
                hits = [m for m in m_by_sd.get((season, c["match_date"]), [])
                        if m["home_team"] == mh and m["away_team"] == ma]
                if len(hits) != 1: ok = False; break
            if ok: alts.append(alt)
        if alts: amb.append((season, token, mapped, alts))
print("ambiguous alias mappings (alternative gives full coverage):", amb)
import hashlib
print("output rows:", len(out), "sha:",
      hashlib.sha256(open(OUT + "method_context_rows_868.jsonl", "rb").read()).hexdigest())
