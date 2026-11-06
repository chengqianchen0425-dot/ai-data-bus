#!/usr/bin/env python3
"""Build austrian_2025_26_rounds.csv for req-20261106-001 D route.
Source: RSSSF Austria 2025/26 (https://www.rsssf.org/tableso/oost2026.html),
cross-checked against Simple Wikipedia 2025-26 Austrian football championship
(rounds 1-24) and bundesliga.at season-preview / final-round articles.
Only dates, teams and round labels are transcribed. No scores, no results.
"""
import csv
from collections import Counter

OUT = "/home/hatch/workspace/ai-inbox/work-req-20261106-001/austrian_2025_26_rounds.csv"

# canonical team names
STURM = "SK Sturm Graz"
SALZBURG = "FC Red Bull Salzburg"
LASK = "LASK"
AUSTRIA = "FK Austria Wien"
RAPID = "SK Rapid Wien"
HARTBERG = "TSV Hartberg"
WSG = "WSG Tirol"
ALTACH = "SCR Altach"
RIED = "SV Ried"
WAC = "Wolfsberger AC"
GAK = "Grazer AK"
BWL = "FC Blau-Weiß Linz"

SLUG = {STURM: "sturm-graz", SALZBURG: "rb-salzburg", LASK: "lask",
        AUSTRIA: "austria-wien", RAPID: "rapid-wien", HARTBERG: "hartberg",
        WSG: "wsg-tirol", ALTACH: "altach", RIED: "ried", WAC: "wolfsberg",
        GAK: "grazer-ak", BWL: "bw-linz"}

# (round, date, home, away, phase)
GD = "Grunddurchgang"
MG = "Meistergruppe"
QG = "Qualifikationsgruppe"

FIX = [
    # Grunddurchgang R1-R22
    (1, "2025-08-01", LASK, STURM, GD), (1, "2025-08-02", WAC, ALTACH, GD),
    (1, "2025-08-02", WSG, HARTBERG, GD), (1, "2025-08-02", RIED, SALZBURG, GD),
    (1, "2025-08-03", GAK, AUSTRIA, GD), (1, "2025-08-03", RAPID, BWL, GD),
    (2, "2025-08-09", BWL, HARTBERG, GD), (2, "2025-08-09", ALTACH, RIED, GD),
    (2, "2025-08-09", SALZBURG, GAK, GD), (2, "2025-08-10", AUSTRIA, WAC, GD),
    (2, "2025-08-10", STURM, RAPID, GD), (2, "2025-08-10", WSG, LASK, GD),
    (3, "2025-08-16", GAK, WSG, GD), (3, "2025-08-16", HARTBERG, SALZBURG, GD),
    (3, "2025-08-16", RIED, STURM, GD), (3, "2025-08-17", LASK, AUSTRIA, GD),
    (3, "2025-08-17", RAPID, ALTACH, GD), (3, "2025-08-17", WAC, BWL, GD),
    (4, "2025-08-23", BWL, RIED, GD), (4, "2025-08-23", SALZBURG, LASK, GD),
    (4, "2025-08-24", AUSTRIA, HARTBERG, GD), (4, "2025-08-24", WAC, RAPID, GD),
    (4, "2025-08-24", ALTACH, GAK, GD), (4, "2025-12-03", STURM, WSG, GD),
    (5, "2025-08-30", LASK, RIED, GD), (5, "2025-08-30", SALZBURG, BWL, GD),
    (5, "2025-08-30", GAK, STURM, GD), (5, "2025-08-31", AUSTRIA, ALTACH, GD),
    (5, "2025-08-31", HARTBERG, RAPID, GD), (5, "2025-08-31", WSG, WAC, GD),
    (6, "2025-09-13", BWL, GAK, GD), (6, "2025-09-13", WAC, SALZBURG, GD),
    (6, "2025-09-13", ALTACH, LASK, GD), (6, "2025-09-14", RAPID, WSG, GD),
    (6, "2025-09-14", RIED, HARTBERG, GD), (6, "2025-09-14", STURM, AUSTRIA, GD),
    (7, "2025-09-20", AUSTRIA, RIED, GD), (7, "2025-09-20", SALZBURG, STURM, GD),
    (7, "2025-09-20", HARTBERG, WAC, GD), (7, "2025-09-21", LASK, BWL, GD),
    (7, "2025-09-21", ALTACH, WSG, GD), (7, "2025-09-21", GAK, RAPID, GD),
    (8, "2025-09-27", BWL, ALTACH, GD), (8, "2025-09-27", WAC, LASK, GD),
    (8, "2025-09-27", RIED, GAK, GD), (8, "2025-09-28", STURM, HARTBERG, GD),
    (8, "2025-09-28", WSG, SALZBURG, GD), (8, "2025-09-28", RAPID, AUSTRIA, GD),
    (9, "2025-10-04", AUSTRIA, BWL, GD), (9, "2025-10-04", GAK, WAC, GD),
    (9, "2025-10-04", RIED, WSG, GD), (9, "2025-10-05", LASK, HARTBERG, GD),
    (9, "2025-10-05", ALTACH, STURM, GD), (9, "2025-10-05", SALZBURG, RAPID, GD),
    (10, "2025-10-18", GAK, HARTBERG, GD), (10, "2025-10-18", WAC, RIED, GD),
    (10, "2025-10-18", WSG, AUSTRIA, GD), (10, "2025-10-19", BWL, STURM, GD),
    (10, "2025-10-19", SALZBURG, ALTACH, GD), (10, "2025-10-19", RAPID, LASK, GD),
    (11, "2025-10-25", LASK, GAK, GD), (11, "2025-10-25", ALTACH, HARTBERG, GD),
    (11, "2025-10-25", WSG, BWL, GD), (11, "2025-10-26", STURM, WAC, GD),
    (11, "2025-10-26", RIED, RAPID, GD), (11, "2025-10-26", AUSTRIA, SALZBURG, GD),
    (12, "2025-11-01", BWL, LASK, GD), (12, "2025-11-01", GAK, ALTACH, GD),
    (12, "2025-11-01", HARTBERG, AUSTRIA, GD), (12, "2025-11-02", SALZBURG, RIED, GD),
    (12, "2025-11-02", WAC, WSG, GD), (12, "2025-11-02", RAPID, STURM, GD),
    (13, "2025-11-08", AUSTRIA, GAK, GD), (13, "2025-11-08", WAC, HARTBERG, GD),
    (13, "2025-11-08", RIED, BWL, GD), (13, "2025-11-09", LASK, ALTACH, GD),
    (13, "2025-11-09", WSG, RAPID, GD), (13, "2025-11-09", STURM, SALZBURG, GD),
    (14, "2025-11-22", BWL, AUSTRIA, GD), (14, "2025-11-22", ALTACH, WAC, GD),
    (14, "2025-11-22", HARTBERG, RIED, GD), (14, "2025-11-23", SALZBURG, WSG, GD),
    (14, "2025-11-23", RAPID, GAK, GD), (14, "2025-11-23", STURM, LASK, GD),
    (15, "2025-11-29", AUSTRIA, WSG, GD), (15, "2025-11-29", GAK, BWL, GD),
    (15, "2025-11-29", RIED, WAC, GD), (15, "2025-11-30", ALTACH, SALZBURG, GD),
    (15, "2025-11-30", LASK, RAPID, GD), (15, "2025-11-30", HARTBERG, STURM, GD),
    (16, "2025-12-06", HARTBERG, LASK, GD), (16, "2025-12-06", BWL, SALZBURG, GD),
    (16, "2025-12-06", RAPID, RIED, GD), (16, "2025-12-07", WAC, AUSTRIA, GD),
    (16, "2025-12-07", STURM, GAK, GD), (16, "2025-12-07", WSG, ALTACH, GD),
    (17, "2025-12-13", GAK, LASK, GD), (17, "2025-12-13", RIED, ALTACH, GD),
    (17, "2025-12-13", HARTBERG, WSG, GD), (17, "2025-12-14", AUSTRIA, STURM, GD),
    (17, "2025-12-14", BWL, RAPID, GD), (17, "2025-12-14", SALZBURG, WAC, GD),
    (18, "2026-02-06", SALZBURG, AUSTRIA, GD), (18, "2026-02-07", LASK, WSG, GD),
    (18, "2026-02-07", RAPID, HARTBERG, GD), (18, "2026-02-08", WAC, GAK, GD),
    (18, "2026-02-08", ALTACH, BWL, GD), (18, "2026-02-08", STURM, RIED, GD),
    (19, "2026-02-14", RIED, LASK, GD), (19, "2026-02-14", HARTBERG, ALTACH, GD),
    (19, "2026-02-14", WSG, STURM, GD), (19, "2026-02-15", BWL, WAC, GD),
    (19, "2026-02-15", GAK, SALZBURG, GD), (19, "2026-02-15", AUSTRIA, RAPID, GD),
    (20, "2026-02-21", RAPID, WAC, GD), (20, "2026-02-21", HARTBERG, GAK, GD),
    (20, "2026-02-21", ALTACH, AUSTRIA, GD), (20, "2026-02-22", STURM, BWL, GD),
    (20, "2026-02-22", WSG, RIED, GD), (20, "2026-02-22", LASK, SALZBURG, GD),
    (21, "2026-03-01", SALZBURG, HARTBERG, GD), (21, "2026-03-01", WAC, STURM, GD),
    (21, "2026-03-01", AUSTRIA, LASK, GD), (21, "2026-03-01", BWL, WSG, GD),
    (21, "2026-03-01", ALTACH, RAPID, GD), (21, "2026-03-01", GAK, RIED, GD),
    (22, "2026-03-08", STURM, ALTACH, GD), (22, "2026-03-08", LASK, WAC, GD),
    (22, "2026-03-08", RAPID, SALZBURG, GD), (22, "2026-03-08", HARTBERG, BWL, GD),
    (22, "2026-03-08", RIED, AUSTRIA, GD), (22, "2026-03-08", WSG, GAK, GD),
    # Meistergruppe R23-R32
    (23, "2026-03-13", LASK, HARTBERG, MG), (23, "2026-03-15", SALZBURG, RAPID, MG),
    (23, "2026-03-15", AUSTRIA, STURM, MG),
    (24, "2026-03-20", STURM, SALZBURG, MG), (24, "2026-03-22", HARTBERG, AUSTRIA, MG),
    (24, "2026-03-22", RAPID, LASK, MG),
    (25, "2026-04-05", LASK, AUSTRIA, MG), (25, "2026-04-05", HARTBERG, SALZBURG, MG),
    (25, "2026-04-05", RAPID, STURM, MG),
    (26, "2026-04-10", SALZBURG, LASK, MG), (26, "2026-04-12", STURM, HARTBERG, MG),
    (26, "2026-04-12", AUSTRIA, RAPID, MG),
    (27, "2026-04-19", AUSTRIA, SALZBURG, MG), (27, "2026-04-19", HARTBERG, RAPID, MG),
    (27, "2026-04-19", LASK, STURM, MG),
    (28, "2026-04-22", RAPID, HARTBERG, MG), (28, "2026-04-22", SALZBURG, AUSTRIA, MG),
    (28, "2026-04-22", STURM, LASK, MG),
    (29, "2026-04-26", RAPID, SALZBURG, MG), (29, "2026-04-26", HARTBERG, LASK, MG),
    (29, "2026-04-26", STURM, AUSTRIA, MG),
    (30, "2026-05-03", AUSTRIA, HARTBERG, MG), (30, "2026-05-03", SALZBURG, STURM, MG),
    (30, "2026-05-04", LASK, RAPID, MG),
    (31, "2026-05-10", LASK, SALZBURG, MG), (31, "2026-05-10", RAPID, AUSTRIA, MG),
    (31, "2026-05-10", HARTBERG, STURM, MG),
    (32, "2026-05-17", AUSTRIA, LASK, MG), (32, "2026-05-17", SALZBURG, HARTBERG, MG),
    (32, "2026-05-17", STURM, RAPID, MG),
    # Qualifikationsgruppe R23-R32
    (23, "2026-03-14", GAK, WAC, QG), (23, "2026-03-14", ALTACH, BWL, QG),
    (23, "2026-03-14", RIED, WSG, QG),
    (24, "2026-03-21", BWL, RIED, QG), (24, "2026-03-21", WAC, ALTACH, QG),
    (24, "2026-03-21", WSG, GAK, QG),
    (25, "2026-04-03", RIED, ALTACH, QG), (25, "2026-04-04", GAK, BWL, QG),
    (25, "2026-04-04", WSG, WAC, QG),
    (26, "2026-04-11", WAC, RIED, QG), (26, "2026-04-11", ALTACH, GAK, QG),
    (26, "2026-04-11", BWL, WSG, QG),
    (27, "2026-04-17", GAK, RIED, QG), (27, "2026-04-18", WAC, BWL, QG),
    (27, "2026-04-18", WSG, ALTACH, QG),
    (28, "2026-04-21", BWL, WAC, QG), (28, "2026-04-21", ALTACH, WSG, QG),
    (28, "2026-04-21", RIED, GAK, QG),
    (29, "2026-04-24", BWL, ALTACH, QG), (29, "2026-04-25", WAC, GAK, QG),
    (29, "2026-04-25", WSG, RIED, QG),
    (30, "2026-05-02", GAK, WSG, QG), (30, "2026-05-02", RIED, BWL, QG),
    (30, "2026-05-04", ALTACH, WAC, QG),
    (31, "2026-05-09", GAK, ALTACH, QG), (31, "2026-05-09", RIED, WAC, QG),
    (31, "2026-05-09", WSG, BWL, QG),
    (32, "2026-05-16", BWL, GAK, QG), (32, "2026-05-16", WAC, WSG, QG),
    (32, "2026-05-16", ALTACH, RIED, QG),
]

RSSSF = "https://www.rsssf.org/tableso/oost2026.html"
# Hartberg relocated home games: (round, date, away) -> venue evidence
MOVED = {
    (3, "2025-08-16", SALZBURG): (
        "https://www.bundesliga.at/de/news/artikel/vorschau-auf-die-3-runde-der-admiral-bundesliga-3",
        "bundesliga.at R3 preview lists DATENPOL ARENA; kicker ticker: Hartberg must play in Südstadt for three months while Profertil Arena is rebuilt"),
    (5, "2025-08-31", RAPID): (
        "https://www.deradmiraner.at/2025/08/01/august-2025/",
        "deradmiraner.at: Hartberg host Rapid 'im Exil Südstadt'; one of three planned Südstadt home games (Salzburg, Rapid, WAC)"),
    (7, "2025-09-20", WAC): (
        "https://www.ligaportal.at/bundesliga/spielberichte/19418-erster-punkt-an-ausweichstaette-joker-fillafer-rettet-remis-fuer-tsv-hartberg-vs-wac",
        "ligaportal.at match report: 20 Sep 2025, 17:00, Datenpol Arena Maria Enzersdorf/Südstadt; officially the third Südstadt home game"),
    (12, "2025-11-01", AUSTRIA): (
        "https://www.kicker.ch/hartberg-gegen-austria-wien-2025-bundesliga-oesterreich-5051422/spielinfo",
        "kicker Spielinfo: 01.11.2025 17:00, Stadion Datenpol Arena (Bundesstadion Südstadt), Maria Enzersdorf; headline: last home game in Südstadt"),
}

POSTPONED = {
    ("2025-12-03", STURM, WSG):
        "Postponed from 2025-08-24 (Sturm preparing for Champions League play-off return leg vs Bodo/Glimt); played 2025-12-03 at default home ground Merkur Arena",
}

rows = []
for rnd, date, home, away, phase in FIX:
    mid = f"austrian-2025-26-r{rnd:02d}-{SLUG[home]}-vs-{SLUG[away]}"
    key = (rnd, date, away)
    if home == HARTBERG and key in MOVED:
        url, note = MOVED[key]
        vstat, vact, vcity = "moved_temporary_home", "Datenpol Arena (Bundesstadion Südstadt)", "Maria Enzersdorf"
        vnote = "Temporary home: Profertil Arena Hartberg under rebuild; " + note
        vsrc = url
    else:
        vstat, vact, vcity = "default_home", "", ""
        vnote = "Default home ground per client-verified 11-stadium table (not re-copied here)"
        vsrc = ""
    s_note = POSTPONED.get((date, home, away), "")
    rows.append({"match_id": mid, "date": date, "home_team": home, "away_team": away,
                 "official_round": rnd, "competition_phase": phase,
                 "venue_status": vstat, "venue_actual": vact, "venue_city": vcity,
                 "venue_note": vnote, "venue_source_url": vsrc, "source_url": RSSSF,
                 "schedule_note": s_note})

rows.sort(key=lambda r: (r["date"], r["official_round"], r["home_team"]))

FIELDS = ["match_id", "date", "home_team", "away_team", "official_round",
          "competition_phase", "venue_status", "venue_actual", "venue_city",
          "venue_note", "venue_source_url", "source_url", "schedule_note"]
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)

# ---- validation ----
print("total rows:", len(rows))
assert len(rows) == 192, len(rows)
print("rounds 1-22:", sum(1 for r in rows if r["competition_phase"] == GD), "(expect 132)")
print("Meistergruppe:", sum(1 for r in rows if r["competition_phase"] == MG), "(expect 30)")
print("Qualifikationsgruppe:", sum(1 for r in rows if r["competition_phase"] == QG), "(expect 30)")
per_round = Counter((r["competition_phase"], r["official_round"]) for r in rows)
bad = {k: v for k, v in per_round.items() if v != (6 if k[0] == GD else 3)}
print("per-round counts != expected:", bad or "none")
team_games = Counter()
team_home = Counter()
for r in rows:
    team_games[r["home_team"]] += 1
    team_games[r["away_team"]] += 1
    team_home[r["home_team"]] += 1
print("per-team games:", dict(sorted(team_games.items())))
assert all(v == 32 for v in team_games.values())
print("per-team home games:", dict(sorted(team_home.items())))
assert all(v == 16 for v in team_home.values())
keys = [(r["date"], r["home_team"], r["away_team"]) for r in rows]
assert len(keys) == len(set(keys)), "duplicate fixtures"
print("duplicate (date,home,away): none")
print("moved rows:", sum(1 for r in rows if r["venue_status"] != "default_home"))
print("date range:", min(r["date"] for r in rows), "->", max(r["date"] for r in rows))
print("match_id unique:", len(set(r["match_id"] for r in rows)) == len(rows))
