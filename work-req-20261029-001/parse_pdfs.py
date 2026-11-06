#!/usr/bin/env python3
"""Parse DFL official Ansetzungen PDFs (2018-19 Bundesliga) and crosswalk to -007 rows.
League rows only: Spieltag column must be numeric (excludes UEL/UCL/DFB/DFL-SC/UEFA rows).
Team split by exact German official names (longest-first).
"""
import json, re, hashlib, csv
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

EV = "/home/hatch/workspace/ai-inbox/work-req-20261029-001/evidence/"
W = "/home/hatch/workspace/ai-inbox/work-req-20261029-001/"

DE_TEAMS = [
    "Borussia Mönchengladbach", "Eintracht Frankfurt", "TSG 1899 Hoffenheim",
    "Bayer 04 Leverkusen", "Sport-Club Freiburg", "Fortuna Düsseldorf",
    "FC Bayern München", "Borussia Dortmund", "1. FSV Mainz 05",
    "SV Werder Bremen", "VfL Wolfsburg", "FC Schalke 04",
    "1. FC Nürnberg", "FC Augsburg", "Hertha BSC",
    "Hannover 96", "VfB Stuttgart", "RB Leipzig",
]
DE2EN = {
    "FC Bayern München": "Bayern Munich", "TSG 1899 Hoffenheim": "Hoffenheim",
    "Hertha BSC": "Hertha", "1. FC Nürnberg": "Nurnberg",
    "SV Werder Bremen": "Werder Bremen", "Hannover 96": "Hannover",
    "Sport-Club Freiburg": "Freiburg", "Eintracht Frankfurt": "Ein Frankfurt",
    "VfL Wolfsburg": "Wolfsburg", "FC Schalke 04": "Schalke 04",
    "Fortuna Düsseldorf": "Fortuna Dusseldorf", "FC Augsburg": "Augsburg",
    "Borussia Mönchengladbach": "M'gladbach", "Bayer 04 Leverkusen": "Leverkusen",
    "1. FSV Mainz 05": "Mainz", "VfB Stuttgart": "Stuttgart",
    "Borussia Dortmund": "Dortmund", "RB Leipzig": "RB Leipzig",
}
TEAM_ALT = "|".join(re.escape(t) for t in sorted(DE_TEAMS, key=len, reverse=True))
ROW_RE = re.compile(
    r"^\s*(\d{2})\.(\d{2})\.(\d{4})\s*-\s*[A-Za-z]{2}\s+(\d{2})[.:](\d{2})\s+(\d{1,2})\s+\d+\s+(.+?)\s*$"
)

PDFS = [
    ("dfl_spieltage_1-6.pdf", "https://media.dfl.de/sites/3/2018/11/Bundesliga_2018-19_Spieltage_1-6.pdf", "DFL official Ansetzungen PDF Spieltage 1-6"),
    ("dfl_spieltage_7-14.pdf", "https://media.dfl.de/sites/3/2018/11/Bundesliga_2018-19_Spieltage_7-14.pdf", "DFL official Ansetzungen PDF Spieltage 7-14"),
    ("dfl_spieltage_15-21.pdf", "https://media.bundesliga-gruppe.de/sites/2/2018/11/Bundesliga_2018-19_Spieltage_15-21-1.pdf", "DFL official Ansetzungen PDF Spieltage 15-21"),
    ("dfl_spieltage_22-28.pdf", "https://media.bundesliga-gruppe.de/sites/2/2018/12/BL-MD-22-28.pdf", "DFL official Ansetzungen PDF Spieltage 22-28 (linked from DFL announcement 19.12.2018)"),
    ("dfl_spieltage_29-34.pdf", "https://media.dfl.de/sites/2/2019/03/Bundesliga_Spieltage_29-34.pdf", "DFL official Ansetzungen PDF Spieltage 29-34"),
]

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

parsed = []   # dicts from PDFs
unparsed = []
for fname, url, label in PDFS:
    txt = open(EV + fname.replace(".pdf", ".txt"), encoding="utf-8").read().splitlines()
    n = 0
    for ln, line in enumerate(txt, 1):
        m = ROW_RE.match(line)
        if not m:
            continue
        dd, mm, yyyy, hh, mi, rnd, rest = m.groups()
        hm = re.match(r"^(" + TEAM_ALT + r")\s+(.+)$", rest.strip())
        if not hm:
            unparsed.append((fname, ln, line))
            continue
        home_de, away_raw = hm.group(1), hm.group(2).strip()
        if away_raw not in DE_TEAMS:
            unparsed.append((fname, ln, line + "  [away remainder: %r]" % away_raw))
            continue
        parsed.append({
            "date_de": f"{dd}.{mm}.{yyyy}", "date_iso": f"{yyyy}-{mm}-{dd}",
            "kickoff": f"{hh}:{mi}", "round": int(rnd),
            "home_de": home_de, "away_de": away_raw,
            "home_en": DE2EN[home_de], "away_en": DE2EN[away_raw],
            "source_file": fname, "source_url": url, "source_label": label,
            "source_sha256": sha(EV + fname),
            "field_locator": f"{label}, table row (verbatim line): {line.strip()}",
        })
        n += 1
    print(fname, "league rows:", n)

print("total parsed:", len(parsed))
print("unparsed candidate lines:", len(unparsed))
for u in unparsed:
    print("  UNPARSED:", u)

from collections import Counter
print("per-round:", sorted(Counter(p["round"] for p in parsed).items()))
print("dup (round,home,away):", [k for k, c in Counter((p["round"], p["home_en"], p["away_en"]) for p in parsed).items() if c > 1])

# crosswalk to -007
base = json.load(open("/home/hatch/workspace/ai-inbox/repo/responses/req-20261003-007.json"))["data"]["rows"]
by_key = {(r["round"], r["home_team"], r["away_team"]): r for r in base}
conflicts = []
matched = 0
pdf_keys = set()
for p in parsed:
    k = (p["round"], p["home_en"], p["away_en"])
    pdf_keys.add(k)
    b = by_key.get(k)
    if not b:
        conflicts.append({"type": "pdf_row_without_-007_match", "pdf": p})
        continue
    matched += 1
    base_date = datetime.strptime(b["match_date"], "%d/%m/%Y").strftime("%Y-%m-%d")
    if base_date != p["date_iso"]:
        conflicts.append({"type": "date_mismatch", "fixture_key": b["fixture_key"],
                          "-007_match_date": b["match_date"], "pdf_date": p["date_de"],
                          "official_match_date_-007": b.get("official_match_date"),
                          "date_note_-007": b.get("date_note"), "pdf_row": p})
    if b["kickoff_local"] != p["kickoff"]:
        conflicts.append({"type": "kickoff_mismatch", "fixture_key": b["fixture_key"],
                          "-007_kickoff": b["kickoff_local"], "pdf_kickoff": p["kickoff"], "pdf_row": p})
    if b["round"] != p["round"]:
        conflicts.append({"type": "round_mismatch", "fixture_key": b["fixture_key"], "pdf_row": p})

base_keys = set(by_key)
print("matched:", matched, "of -007:", len(base))
print("pdf rows without -007 match:", len([c for c in conflicts if c["type"] == "pdf_row_without_-007_match"]))
print("-007 rows without pdf match:", sorted(base_keys - pdf_keys))
print("date mismatches:", [c for c in conflicts if c["type"] == "date_mismatch"])
print("kickoff mismatches:", [c for c in conflicts if c["type"] == "kickoff_mismatch"])

json.dump({"parsed": parsed, "conflicts": conflicts, "unparsed": unparsed},
          open(W + "parse_audit.json", "w"), ensure_ascii=False, indent=2)
print("wrote parse_audit.json")
