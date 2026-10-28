#!/usr/bin/env python3
"""Build unresolved_queue_868.jsonl + print verification stats for req-20261028-003."""
import json
from collections import Counter

OUT = "/home/hatch/workspace/ai-inbox/work-req-20261028-003/"
rows = [json.loads(l) for l in open(OUT + "method_context_rows_868.jsonl")]

uq = []
for r in rows:
    if not r["matched_merged_fixture_key"]:
        uq.append({"fixture_key": r["fixture_key"], "season": r["season"],
                   "match_date": r["match_date"], "type": "join_zero_hit",
                   "fields": ["join"],
                   "detail": r["join_reason"],
                   "diagnostic": ("merged 2022 league universe ends 2022-10-16 (round 27); "
                                  "this fixture falls 2022-10-19..30, after league end; "
                                  "no merged rows exist on this date at all; same pair exists "
                                  "in merged 2022 on other dates (date differs, not joined: "
                                  "date is part of the join key, no date inference allowed); "
                                  "TPS-Lahti 2022-10-20 is consistent with a relegation-playoff "
                                  "leg but that is NOT asserted here -- requester adjudication needed")})
        continue
    fields, details = [], []
    if r["row_status_merged"] == "conflict":
        fields.append("merged_conflict")
        details.append(f"merged status conflict (route {r['route']})")
    if r["official_round"] is None:
        fields.append("official_round")
        details.append("official_round null (2022 regular season: rounds not recoverable from "
                       "WorldFootball pagination / FBref Wk buckets; 2021-09-14: FBref Wk14 "
                       "group-completeness conflict)")
    if r["venue_status"] in ("conflict", "unavailable"):
        fields.append("venue")
        details.append(f"venue_status={r['venue_status']}: " +
                       ("competing venue candidates, none chosen" if r["venue_status"] == "conflict"
                        else "venue candidate known but not fixture-verified (route label normalized)"))
    if r["kickoff_local"] is None:
        fields.append("kickoff")
        details.append("kickoff null (source gives date only)")
    if r["kickoff_disagreement_unresolved"]:
        fields.append("kickoff")
        details.append("kickoff disputed: -004 value kept, FBref systematically +2h, UTC withheld")
    if fields:
        uq.append({"fixture_key": r["fixture_key"], "season": r["season"],
                   "match_date": r["match_date"],
                   "type": "carried_gap",
                   "matched_merged_fixture_key": r["matched_merged_fixture_key"],
                   "fields": sorted(set(fields)),
                   "detail": "; ".join(details)})

with open(OUT + "unresolved_queue_868.jsonl", "w") as f:
    for item in uq:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("UQ items:", len(uq))
print("by type:", Counter(i["type"] for i in uq))
print("by aspect:", Counter(f for i in uq for f in i["fields"]))
print("by season:", Counter(i["season"] for i in uq))
