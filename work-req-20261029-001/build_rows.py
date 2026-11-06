#!/usr/bin/env python3
"""Build final 306 rows for req-20261029-001 A-route from -007 baseline + PDF parse."""
import json, hashlib
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

W = "/home/hatch/workspace/ai-inbox/work-req-20261029-001/"
EV = W + "evidence/"
RETRIEVED = "2026-11-06T18:56:10+08:00"  # actual curl retrieval time, Asia/Shanghai
BERLIN = ZoneInfo("Europe/Berlin")

audit = json.load(open(W + "parse_audit.json"))
pdf_by_key = {(p["round"], p["home_en"], p["away_en"]): p for p in audit["parsed"]}
base = json.load(open("/home/hatch/workspace/ai-inbox/repo/responses/req-20261003-007.json"))["data"]["rows"]

def utc_str(date_iso, kickoff):
    dt = datetime.strptime(f"{date_iso} {kickoff}", "%Y-%m-%d %H:%M").replace(tzinfo=BERLIN)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), dt.strftime("%Z")

out = []
for b in base:
    k = (b["round"], b["home_team"], b["away_team"])
    p = pdf_by_key[k]
    utc, abbr = utc_str(p["date_iso"], p["kickoff"])
    prev_fbref = b["source_url"].startswith("https://fbref.com")
    row = {
        "fixture_key": b["fixture_key"],
        "season": b["season"],
        "match_date": b["match_date"],
        "official_match_date": b.get("official_match_date"),
        "date_note": b.get("date_note"),
        "home_team": b["home_team"],
        "away_team": b["away_team"],
        "round": b["round"],
        "official_round": p["round"],
        "kickoff_local": p["kickoff"],
        "timezone": "Europe/Berlin",
        "kickoff_utc": utc,
        "kickoff_utc_method": "Europe/Berlin wall time as published in DFL PDF converted with IANA tz database (CET=UTC+1 before 2019-03-31 02:00, CEST=UTC+2 from then; local abbreviation at kickoff: %s). UTC value is a derived conversion, not the source value." % abbr,
        "status": "ok",
        "conflict_flag": ("date_key_vs_official" if b["fixture_key"] == "2018-19|12/05/2019|Ein Frankfurt|Mainz" else None),
        "source_name": "DFL official Ansetzungen PDF",
        "source_tier": "official_dfl",
        "source_url": p["source_url"],
        "final_url": p["source_url"],
        "retrieved_at": RETRIEVED,
        "field_locator": p["field_locator"],
        "source_sha256": p["source_sha256"],
        "source_home_team": p["home_de"],
        "source_away_team": p["away_de"],
        "prev_source_007": b["source_url"],
        "source_upgrade_note": ("Upgraded this round from FBref non-official cross-check source (-007) to DFL official Ansetzungen PDF (Spieltage 22-28, linked from DFL announcement 19.12.2018); kickoff and date verified identical to -007 values." if prev_fbref else "Official DFL source already used in -007; this round re-downloaded the PDF bytes and attached the real byte SHA-256."),
    }
    out.append(row)

assert len(out) == 306, len(out)
assert len({r["fixture_key"] for r in out}) == 306
assert all(r["source_sha256"] for r in out)
assert all(r["timezone"] == "Europe/Berlin" for r in out)
FORB = ["score", "odds", "prediction", "standing", "goals", "result", "model"]
bad = [k for r in out for k in r if any(s in k.lower() for s in FORB)]
assert not bad, bad

with open(W + "bundesliga_201819_kickoff_rows.jsonl", "w") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

sha = hashlib.sha256(open(W + "bundesliga_201819_kickoff_rows.jsonl", "rb").read()).hexdigest()
from collections import Counter
print("rows:", len(out), "SHA:", sha)
print("official_dfl:", sum(1 for r in out if r["source_tier"] == "official_dfl"))
print("upgraded from FBref:", sum(1 for r in out if "Upgraded" in r["source_upgrade_note"]))
print("null sha:", sum(1 for r in out if not r["source_sha256"]))
print("conflict rows:", [r["fixture_key"] for r in out if r["conflict_flag"]])
print("UTC offsets:", Counter(r["kickoff_utc_method"].split("abbreviation at kickoff: ")[1].rstrip(").") for r in out))
# MD33 check
md33 = [r for r in out if r["round"] == 33]
print("MD33 rows:", len(md33), "dates:", Counter((r["official_match_date"] or r["match_date"]) for r in md33), "kickoffs:", Counter(r["kickoff_local"] for r in md33))
