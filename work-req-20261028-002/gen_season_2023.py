#!/usr/bin/env python3
"""Generate season_2023.jsonl for req-20261028-002 (Veikkausliiga 2023 cross-check).
No scores, results, standings, odds or predictions are written anywhere.
Kickoff correction: -004 times are UK-clock times mislabelled Europe/Helsinki;
FBref venue-local times are exactly -004 + 2h on every directly compared row.
"""
import json, datetime

SRC = "/home/hatch/workspace/ai-inbox/repo/work-req-20261006-004/req-20261006-004-rows.json"
COORDS = "/home/hatch/workspace/ai-inbox/repo/work-req-20261006-004/venue-coords.json"
OUT = "/home/hatch/workspace/ai-inbox/work-req-20261028-002/season_2023.jsonl"

NOW = "2026-10-28T16:45:00+08:00"  # Asia/Shanghai retrieval window for this round
WIKI_SHA = "a0643547005eb91cf8fd75f9add38f26539144c3ee61f4b11bd666fe9e3d3e75"
WIKI_URL = "https://en.wikipedia.org/wiki/2023_Veikkausliiga"
WIKI_RETR = "2026-10-28T16:12:46+08:00"
FBREF_URL = "https://fbref.com/en/comps/43/2023/schedule/2023-Veikkausliiga-Scores-and-Fixtures"
WF_URL = "https://www.worldfootball.net/competition/co134/finland-veikkausliiga/"

def prov(name, url, locator, sha=None, retr=NOW, note=""):
    d = {"source_name": name, "source_url": url, "final_url": url,
         "retrieved_at": retr, "field_locator": locator, "source_sha256": sha}
    if note:
        d["note"] = note
    return d

# ---- venue coords from -004 (cite file, not a hash) ----
vc = json.load(open(COORDS))
coord_by_name = {}
for stad, v in vc["stadiums"].items():
    for k in v.get("venue_keys", [stad]):
        coord_by_name[k] = (stad, v["city"], v["lat"], v["lon"], v.get("precision", ""))
    coord_by_name.setdefault(stad, (stad, v["city"], v["lat"], v["lon"], v.get("precision", "")))

def coord(name):
    return coord_by_name[name]

# ---- club identities (founded years verified this round via club Wikipedia pages,
# text extraction; bytes not retained, so sha256 is null per provenance rule) ----
CLUBS = {
 "AC Oulu": {"full_name": "AC Oulu", "founded": "2002", "founded_note": "Founded 2002 (club infobox).",
   "season_2023_entry": "Returning Veikkausliiga club (not the 2023 promoted club).",
   "notes": "No merger/rename fact verified this round; do not confuse with OLS/Oulun Luistinseura."},
 "HJK": {"full_name": "Helsingin Jalkapalloklubi (HJK Helsinki)", "founded": "1907-06-19",
   "founded_note": "Founded 19 June 1907 (club infobox).",
   "season_2023_entry": "Defending champions entering 2023 (per 2023 season page).", "notes": ""},
 "Haka": {"full_name": "Valkeakosken Haka", "founded": "1934", "founded_note": "Founded 1934 (club infobox).",
   "season_2023_entry": "Returning Veikkausliiga club.", "notes": ""},
 "Honka": {"full_name": "FC Honka", "founded": "1957", "founded_note": "Founded 1957 (club infobox).",
   "season_2023_entry": "Returning Veikkausliiga club.",
   "notes": "Season-end administrative status (not a match result): demoted to 2024 Kakkonen for financial reasons, per 2023 season page intro. Do not use this to re-interpret any match."},
 "Ilves": {"full_name": "Tampereen Ilves", "founded": "1931",
   "founded_note": "1931 is the Ilves sports-club founding year shown on the club page; a distinct football-section founding year was NOT separately verified this round and must not be substituted for it.",
   "season_2023_entry": "Returning Veikkausliiga club.", "notes": "Season home in the 2023 season stadia table is listed as 'Tampere Stadium'; that is the Ratinan ground (alias, not a different venue)."},
 "Inter Turku": {"full_name": "FC Inter Turku", "founded": "1990", "founded_note": "Founded 1990 (club infobox).",
   "season_2023_entry": "Returning Veikkausliiga club.", "notes": ""},
 "KTP": {"full_name": "Kotkan Työväen Palloilijat (FC KTP)", "founded": "1927-09-22",
   "founded_note": "Founded 22 September 1927. In December 2013 FC KooTeePee adopted the KTP name and the merged club retained KooTeePee's Ykkönen place from 2014; do not merge the pre-2013 KTP bankruptcy history into the current club without that distinction.",
   "season_2023_entry": "Promoted club: 2022 Ykkönen champions, the sole promoted team into 2023 (2023 season page: 'Promoted from 2022 Ykkönen: KTP'; HIFK relegated out).",
   "notes": "Season-end administrative status (not a match result): relegated to 2024 Ykkösliiga, per 2023 season page intro."},
 "KuPS": {"full_name": "Kuopion Palloseura", "founded": "1923", "founded_note": "Founded 1923 (club infobox).",
   "season_2023_entry": "Returning Veikkausliiga club.",
   "notes": "Season stadia table lists 'Savon Sanomat Areena'; same ground as Väre Areena (renamed) per -004 geocode note."},
 "Lahti": {"full_name": "FC Lahti", "founded": "1996", "founded_note": "Founded 1996 (club infobox). Predecessor/merger detail NOT verified this round; left blank, not guessed.",
   "season_2023_entry": "Returning Veikkausliiga club.", "notes": ""},
 "Mariehamn": {"full_name": "IFK Mariehamn", "founded": "1919", "founded_note": "Founded 1919 (club infobox).",
   "season_2023_entry": "Returning Veikkausliiga club.",
   "notes": "The 11th-placed Veikkausliiga club entered a separate Veikkausliiga/Ykkönen play-off whose matches are OUTSIDE this 167-row set; no outcome is recorded here."},
 "SJK": {"full_name": "Seinäjoen Jalkapallokerho", "founded": "2007-11-05",
   "founded_note": "Founded 5 November 2007 (club infobox). Merger partners NOT verified this round; left blank, not guessed.",
   "season_2023_entry": "Returning Veikkausliiga club.", "notes": ""},
 "VPS": {"full_name": "Vaasan Palloseura", "founded": "1924", "founded_note": "Founded 1924 (club infobox).",
   "season_2023_entry": "Returning Veikkausliiga club.",
   "notes": "Ground aliases for the same Vaasa ground: Hietalahti / Elisa Stadion / Lemonsoft Stadion (per -004 geocode note)."},
}
CLUB_URL = {
 "AC Oulu": "https://en.wikipedia.org/wiki/AC_Oulu", "HJK": "https://en.wikipedia.org/wiki/HJK_Helsinki",
 "Haka": "https://en.wikipedia.org/wiki/FC_Haka", "Honka": "https://en.wikipedia.org/wiki/FC_Honka",
 "Ilves": "https://en.wikipedia.org/wiki/Ilves", "Inter Turku": "https://en.wikipedia.org/wiki/FC_Inter_Turku",
 "KTP": "https://en.wikipedia.org/wiki/Kotkan_Ty%C3%B6v%C3%A4en_Palloilijat",
 "KuPS": "https://en.wikipedia.org/wiki/Kuopion_Palloseura", "Lahti": "https://en.wikipedia.org/wiki/FC_Lahti",
 "Mariehamn": "https://en.wikipedia.org/wiki/IFK_Mariehamn",
 "SJK": "https://en.wikipedia.org/wiki/Sein%C3%A4joen_Jalkapallokerho",
 "VPS": "https://en.wikipedia.org/wiki/Vaasan_Palloseura",
}
def club_identity(team):
    c = CLUBS[team]
    return {"team_as_in_fixture": team, "full_name": c["full_name"], "founded": c["founded"],
            "founded_note": c["founded_note"], "season_2023_entry": c["season_2023_entry"],
            "identity_notes": c["notes"],
            "source": prov("Wikipedia club page (text extraction via curl; bytes not retained)",
                           CLUB_URL[team], "club infobox 'Founded' field", sha=None,
                           note="文本层/文本抽取，无保留字节，sha256=null")}

CHAMP = {"HJK", "KuPS", "SJK", "VPS", "Honka", "Inter Turku"}
# Playoff phases verified by Wikipedia 2023 season page (Play-offs section, curl bytes)
# + FBref schedule page (text layer). Seeding positions are the play-off entry
# positions from the championship/relegation tables, used only as play-off seeding.
PLAYOFF = {
 ("2023-10-25", "Honka", "Inter Turku"): ("Conference League play-offs — Quarter-finals", "quarter-final, single leg"),
 ("2023-10-25", "SJK", "AC Oulu"): ("Conference League play-offs — Quarter-finals", "quarter-final, single leg"),
 ("2023-10-28", "Honka", "AC Oulu"): ("Conference League play-offs — Semi-final", "semi-final, single leg"),
 ("2023-11-01", "Honka", "VPS"): ("Conference League play-offs — Final, leg 1", "final, first leg of two"),
 ("2023-11-05", "VPS", "Honka"): ("Conference League play-offs — Final, leg 2", "final, second leg of two"),
}
# Match-level venue moves verified this round (FBref + Sky Sports agree; SportsMole differs)
MOVED = {
 ("2023-04-15", "Honka", "SJK"): {"venue": "Myyrmäen jalkapallostadion", "aka": "ISS Stadion",
   "city": "Vantaa", "lat": 60.26024, "lon": 24.84279,
   "evidence": "FBref schedule row + Sky Sports match page ('ISS Stadion'); SportsMole lists season home Tapiolan Urheilupuisto (retained as competing candidate)."},
 ("2023-04-15", "Ilves", "Inter Turku"): {"venue": "Tehtaan kenttä", "aka": None,
   "city": "Valkeakoski", "lat": 61.2665, "lon": 24.02617,
   "evidence": "FBref schedule row + Sky Sports match page ('Tehtaan Kentta'); SportsMole lists Tammelan Stadion (retained as competing candidate)."},
}
SKY_HONKA_SJK = "https://www.skysports.com/football/honka-vs-sjk/stats/480986"
SKY_ILVES_INTER = "http://www.skysports.com/football/ilves-vs-fc-inter-turku/480987"

def add2(t):
    h, m = map(int, t.split(":"))
    m += 120
    h += m // 60; m %= 60
    return f"{h:02d}:{m:02d}"

def utc_of(date, local):
    # Finland: EEST UTC+3 until 2023-10-29 (DST ends that Sunday); EET UTC+2 from 2023-10-29.
    off = 3 if date < "2023-10-29" else 2
    h, m = map(int, local.split(":"))
    tot = h * 60 + m - off * 60
    day = date
    if tot < 0:
        tot += 1440
        day = (datetime.date.fromisoformat(date) - datetime.timedelta(days=1)).isoformat()
    return f"{day}T{tot//60:02d}:{tot%60:02d}:00Z", off

def main():
    d = json.load(open(SRC))
    rows = [r for r in d["rows"] if str(r.get("season")) == "2023"]
    assert len(rows) == 167, len(rows)
    rows.sort(key=lambda r: (r["date"], r["home_team"], r["away_team"]))
    out = []
    for r in rows:
        date, home, away = r["date"], r["home_team"], r["away_team"]
        old_time = r["kickoff"]
        new_time = add2(old_time)
        utc, off = utc_of(date, new_time)
        is_playoff = (date, home, away) in PLAYOFF
        is_moved = (date, home, away) in MOVED
        if is_playoff:
            phase, leg = PLAYOFF[(date, home, away)]
            official_round = phase
            official_source = "fbref+wikipedia_crosscheck_non_official"
            round_status = "filled_this_round"
            series = phase
        else:
            rnd = r["official_round"]
            official_round = rnd
            official_source = "worldfootball_matchday_non_official"
            round_status = "from_req-20261006-004"
            if rnd is None:
                series = None
            elif int(rnd) <= 22:
                series = "Regular season"
            else:
                series = "Championship round" if home in CHAMP else "Relegation round"
        # venue
        cand_name, cand_city = r["venue"], r["city"]
        _, _, clat, clon, prec = coord(cand_name)
        if is_moved:
            mv = MOVED[(date, home, away)]
            venue_verified, vcity, vlat, vlon = mv["venue"], mv["city"], mv["lat"], mv["lon"]
            vstatus = "moved"
            candidates = [cand_name, venue_verified] + ([mv["aka"]] if mv["aka"] else [])
            if (date, home) == ("2023-04-15", "Ilves"):
                candidates.append("Tammelan Stadion")
            if (date, home) == ("2023-04-15", "Honka"):
                candidates.append("Tapiolan Urheilupuisto (SportsMole listing)")
            row_status = "conflict"
            venue_note = mv["evidence"]
        else:
            venue_verified, vcity, vlat, vlon = cand_name, cand_city, clat, clon
            vstatus = "confirmed"
            candidates = [cand_name]
            if home == "VPS":
                candidates += ["Hietalahti", "Elisa Stadion"]
            if home == "KuPS":
                candidates += ["Savon Sanomat Areena"]
            if home == "HJK":
                candidates += ["Telia 5G -areena"]
            if home == "Ilves":
                candidates += ["Tampere Stadium"]
            row_status = "complete"
            venue_note = ("Match-level venue from FBref schedule row for this fixture (non-official "
                          "cross-source); official league/club match-page confirmation = 0 rows this round. "
                          "Coordinates from -004 venue-coords.json (geocode result, cited as source, not a hash).")
        prov_obj = {
          "fixture_identity": prov("req-20261006-004 rows (inherited)", r.get("source_url") or "https://www.football-data.co.uk/new/Finland.csv",
                                   "row fixture_key/date/home/away as in -004", sha=None,
                                   note="沿用-004；-004 的 source_sha256 为描述符式哈希，本轮不复用，sha256=null"),
          "date_home_away": prov("req-20261006-004 rows (inherited)", r.get("source_url") or "https://www.football-data.co.uk/new/Finland.csv",
                                 "row date/home_team/away_team", sha=None, note="无更强证据覆盖，沿用-004"),
          "kickoff": prov("FBref 2023 Veikkausliiga schedule (text layer)", FBREF_URL,
                           "schedule table row for this fixture, Time column (venue-local; parenthetical Pacific time corroborates the column)",
                           sha=None, note=f"文本层，无字节，sha256=null；旧值 {old_time}（-004，实为英国时钟时间）→ 新值 {new_time} Europe/Helsinki；系统性+2h，见 notes（21 行逐行比对全中）"),
          "official_round": (prov("Wikipedia 2023 Veikkausliiga, Play-offs section + FBref schedule Round column", WIKI_URL,
                                  "Play-offs: Conference League play-off section (quarter-finals/semi-finals/final legs)", sha=WIKI_SHA, retr=WIKI_RETR,
                                  note="curl 实下载字节哈希；该源为交叉源而非官方源，official_round_source 仍标非官方") if is_playoff else
                             prov("WorldFootball matchday grouping via -004 (non-official)", WF_URL,
                                  "worldfootball.net competition/co134 Matchday N group header, as recorded in -004", sha=None,
                                  note="沿用-004；WorldFootball curl 曾 403，本轮未复取字节，sha256=null；绝不升级为官方")),
          "series_or_phase": prov("Wikipedia 2023 Veikkausliiga (format + tables)", WIKI_URL,
                                  "Teams section (split after 22 games) + Championship/Relegation Round tables + Play-offs section",
                                  sha=WIKI_SHA, retr=WIKI_RETR, note="curl 实下载字节哈希；分组归属以常规赛后分组表为准，非日期推断"),
          "venue": (prov("FBref schedule row + Sky Sports match page (text layer)", SKY_HONKA_SJK if home == "Honka" else SKY_ILVES_INTER,
                         "match page venue field", sha=None, note="文本层，无字节，sha256=null；" + venue_note) if is_moved else
                    prov("FBref 2023 Veikkausliiga schedule (text layer)", FBREF_URL,
                         "schedule table row for this fixture, Venue column", sha=None, note="文本层，无字节，sha256=null；" + venue_note)),
          "venue_coords": prov("-004 venue-coords.json (geocode result)", "~/workspace/ai-inbox/repo/work-req-20261006-004/venue-coords.json",
                               f"stadiums entry for {cand_name} (or moved-venue geocode for moved rows)", sha=None,
                               note="地理编码结果出处，非字节哈希，sha256=null" + ("" if not is_moved else "；易地场馆坐标为本轮 map.geocode 全地址结果")),
          "home_club_identity": prov("Wikipedia club page (text extraction)", CLUB_URL[home], "club infobox 'Founded'", sha=None, note="文本抽取，字节未保留，sha256=null"),
          "away_club_identity": prov("Wikipedia club page (text extraction)", CLUB_URL[away], "club infobox 'Founded'", sha=None, note="文本抽取，字节未保留，sha256=null"),
          "meeting_number": prov("attempted: veikkausliiga.com / Tulospalvelu / WorldFootball / FBref / Wikipedia",
                                "https://tulospalvelu.palloliitto.fi/", "no meeting_number field in any attempted source", sha=None,
                                note="veikkausliiga.com 本轮 curl 000 不可达；Tulospalvelu 仅返回 JS 壳（2597 字节）；其余源无该字段"),
        }
        notes = []
        if is_playoff:
            notes.append(f"附加赛已核实：{phase}（{leg}）；参赛资格为附加赛入围名次（冠军组第3名直通决赛，其余4队打四分之一决赛/半决赛，单场；决赛两回合）——依据 Wikipedia 赛季页 Play-offs 节与 FBref Round 列；官方芬兰语名 Eurolopputurnaus 本轮未在官方源核实，不作已核实名称使用。")
            notes.append(f"开球时间覆盖：-004 {old_time}（英国时钟时间，误标 Europe/Helsinki）→ {new_time} Europe/Helsinki（FBref 场次级时间；UTC {utc}，换算：{'EEST UTC+3' if off==3 else 'EET UTC+2'}）。")
        else:
            notes.append(f"轮次沿用-004（WorldFootball 分组，非官方）；系列：{series}。开球时间系统性覆盖：-004 {old_time} → {new_time} Europe/Helsinki（UTC {utc}）。")
        if is_moved:
            notes.append("场馆易地（moved）：赛季主场映射不是本场场馆；见 venue_candidates（含竞争候选）。")
        out.append({
          "fixture_key": r["fixture_key"], "season": "2023", "date": date,
          "kickoff_local": new_time, "kickoff_timezone": "Europe/Helsinki", "kickoff_utc": utc,
          "kickoff_old_req20261006_004": old_time,
          "home_team": home, "away_team": away,
          "official_round": official_round, "official_round_source": official_source,
          "official_round_status": round_status,
          "series_or_phase": series,
          "meeting_number": None, "meeting_number_status": "unavailable",
          "meeting_number_attempted_sources": ["veikkausliiga.com (curl 000, unreachable this round)",
             "tulospalvelu.palloliitto.fi (JS shell only, 2597 bytes, no bulk data)",
             "worldfootball.net (no meeting_number field)", "FBref schedule (no meeting_number field)",
             "Wikipedia 2023 season page (no meeting_number field)"],
          "venue_candidate": cand_name, "venue_candidate_city": cand_city,
          "venue_lat": vlat, "venue_lon": vlon, "venue_timezone": "Europe/Helsinki",
          "venue_verified": venue_verified, "venue_status": vstatus,
          "venue_candidates": candidates,
          "venue_coords_source": "-004 venue-coords.json" + ("; moved-venue geocode this round (FULL_ADDRESS)" if is_moved else ""),
          "venue_coords_precision": ("FULL_ADDRESS (map.geocode)" if is_moved else prec),
          "home_club_identity": club_identity(home), "away_club_identity": club_identity(away),
          "csv_join_status": "matched_to_req-20261006-004_row_csv_join_pending",
          "provenance": prov_obj, "row_status": row_status, "notes": " ".join(notes),
        })
    with open(OUT, "w", encoding="utf-8") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    print("wrote", len(out), OUT)

if __name__ == "__main__":
    main()
