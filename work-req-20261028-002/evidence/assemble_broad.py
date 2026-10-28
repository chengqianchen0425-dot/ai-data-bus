#!/usr/bin/env python3
"""B-road assembly: -004 rows (2019-2021) + FBref overlays -> method_context_2019_2021.jsonl."""
import json, collections
from datetime import datetime, timezone
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

WORK = "/home/hatch/workspace/ai-inbox/work-req-20261028-002/"
EV = WORK + "evidence/"
D004 = json.load(open("/home/hatch/workspace/ai-inbox/repo/work-req-20261006-004/req-20261006-004-rows.json"))["rows"]
VC = json.load(open("/home/hatch/workspace/ai-inbox/repo/work-req-20261006-004/venue-coords.json"))["stadiums"]

NORM = {"KuPS": "Kuopion PS", "SJK": "SJK Seinäjoki", "Lahti": "FC Lahti",
        "Ilves": "Ilves Tampere", "FC Inter": "Inter Turku", "Haka": "Haka Valkeakoski",
        "Helsinki IFK": "Helsingfors IFK", "KPV": "KPV Kokkola", "VPS": "Vaasan PS", "TPS": "TPS Turku"}
def norm_team(fb, season):
    if fb == "RoPS":
        return "Rovaniemi PS" if season == "2019" else "Rovaniemen PS"
    return NORM.get(fb, fb)

# canonical venue: FBref name -> (canonical name, city, lat, lon, precision, coords_source)
COORDS_SRC_004 = "req-20261006-004 venue-coords.json (geocoding result, cited as provenance, NOT a hash)"
def ventry(name, display=None):
    s = VC[name]
    return (display or name, s["city"], s["lat"], s["lon"], s["precision"], COORDS_SRC_004)
CANON = {
    "Telia 5G -areena": ventry("Bolt Arena"),
    "Bolt Arena": ventry("Bolt Arena"),
    "Savon Sanomat Areena": ventry("Väre Areena"),
    "Väre Areena": ventry("Väre Areena"),
    "Raatin stadion": ventry("Raatin Stadion"),
    "Raatti Stadion": ventry("Raatin Stadion"),
    "Ratinan Stadion": ventry("Ratinan stadion"),
    "Tampere Stadium": ventry("Ratinan stadion"),
    "Kokkolan Keskuskenttä": ventry("Kokkolan keskuskenttä"),
    "Kokkolan keskuskenttä": ventry("Kokkolan keskuskenttä"),
    "OmaSP Stadion": ventry("OmaSP Stadion"),
    "OmaSp Stadion": ventry("OmaSP Stadion"),
    "Lahden Stadion": ventry("Lahden Stadion"),
    "Lahden stadion": ventry("Lahden Stadion"),
    "Tapiolan Urheilupuisto": ventry("Tapiolan Urheilupuisto"),
    "Tapiolan urheilupuisto": ventry("Tapiolan Urheilupuisto"),
    "Tammelan Stadion": ventry("Tammelan Stadion"),
    "Tammelan stadion": ventry("Tammelan Stadion"),
    "Rovaniemen Keskuskenttä": ventry("Rovaniemen keskuskenttä"),
    "Rovaniemen keskuskenttä": ventry("Rovaniemen keskuskenttä"),
    "Veritas Stadion": ventry("Veritas Stadion"),
    "Wiklöf Holding Arena": ventry("Idrottsparken (Wiklöf Holding Arena)", "Wiklöf Holding Arena"),
    "Arto Tolsa Areena": ventry("Arto Tolsa Areena"),
    "Tehtaan kenttä": ventry("Tehtaan kenttä"),
    "Elisa Stadion": ventry("Elisa Stadion"),
    "Kisapuisto": ("Kisapuisto", "Lahti", 60.98594, 25.64931, "FULL_ADDRESS",
                   "map.geocode this round (2026-10-28): Lahden Kisapuisto, Kartanonkatu, FI-15140 Lahti, FULL_ADDRESS"),
}
def canon_of(fbref_venue):
    return CANON[fbref_venue]

FOUNDED = {"HJK Helsinki": 1907, "Helsingfors IFK": 1897, "IFK Mariehamn": 1919,
           "Ilves Tampere": 1931, "Inter Turku": 1990, "Kuopion PS": 1923,
           "SJK Seinäjoki": 2007, "Vaasan PS": 1924, "FC Honka": 1957, "FC Lahti": 1996,
           "KPV Kokkola": 1930, "Rovaniemi PS": 1950, "Rovaniemen PS": 1950,
           "Haka Valkeakoski": 1934, "TPS Turku": 1922, "AC Oulu": 2002, "KTP": 1927}
CITY = {"HJK Helsinki": "Helsinki", "Helsingfors IFK": "Helsinki", "IFK Mariehamn": "Mariehamn",
        "Ilves Tampere": "Tampere", "Inter Turku": "Turku", "Kuopion PS": "Kuopio",
        "SJK Seinäjoki": "Seinäjoki", "Vaasan PS": "Vaasa", "FC Honka": "Espoo", "FC Lahti": "Lahti",
        "KPV Kokkola": "Kokkola", "Rovaniemi PS": "Rovaniemi", "Rovaniemen PS": "Rovaniemi",
        "Haka Valkeakoski": "Valkeakoski", "TPS Turku": "Turku", "AC Oulu": "Oulu", "KTP": "Kotka"}
MAPPING = {
    "2019": {"FC Honka": "Tapiolan urheilupuisto", "FC Lahti": "Lahden stadion",
             "HJK Helsinki": "Telia 5G -areena", "Helsingfors IFK": "Telia 5G -areena",
             "IFK Mariehamn": "Wiklöf Holding Arena", "Ilves Tampere": "Tammelan stadion",
             "Inter Turku": "Veritas Stadion", "KPV Kokkola": "Kokkolan keskuskenttä",
             "Kuopion PS": "Savon Sanomat Areena", "Rovaniemi PS": "Rovaniemen keskuskenttä",
             "SJK Seinäjoki": "OmaSp Stadion", "Vaasan PS": "Elisa Stadion"},
    "2020": {"FC Honka": "Tapiolan Urheilupuisto", "FC Lahti": "Lahden Stadion",
             "HJK Helsinki": "Bolt Arena", "Haka Valkeakoski": "Tehtaan kenttä",
             "Helsingfors IFK": "Bolt Arena", "IFK Mariehamn": "Wiklöf Holding Arena",
             "Ilves Tampere": "Tammelan Stadion", "Inter Turku": "Veritas Stadion",
             "Kuopion PS": "Savon Sanomat Areena", "Rovaniemen PS": "Rovaniemen keskuskenttä",
             "SJK Seinäjoki": "OmaSP Stadion", "TPS Turku": "Veritas Stadion"},
    "2021": {"AC Oulu": "Raatti Stadion", "FC Honka": "Tapiolan Urheilupuisto",
             "FC Lahti": "Lahden Stadion", "HJK Helsinki": "Bolt Arena",
             "Haka Valkeakoski": "Tehtaan kenttä", "Helsingfors IFK": "Bolt Arena",
             "IFK Mariehamn": "Wiklöf Holding Arena", "Ilves Tampere": "Tampere Stadium",
             "Inter Turku": "Veritas Stadion", "KTP": "Arto Tolsa Areena",
             "Kuopion PS": "Savon Sanomat Areena", "SJK Seinäjoki": "OmaSP Stadion"},
}
SPLIT = {
    "2019": ({"Inter Turku", "Kuopion PS", "Ilves Tampere", "HJK Helsinki", "FC Honka", "IFK Mariehamn"},
             {"Helsingfors IFK", "SJK Seinäjoki", "FC Lahti", "Rovaniemi PS", "Vaasan PS", "KPV Kokkola"},
             "championship_series", "challenger_series"),
    "2021": ({"HJK Helsinki", "Kuopion PS", "SJK Seinäjoki", "Inter Turku", "Ilves Tampere", "Helsingfors IFK"},
             {"FC Lahti", "KTP", "Haka Valkeakoski", "FC Honka", "IFK Mariehamn", "AC Oulu"},
             "championship_round", "relegation_round"),
}
FBREF_URL = {s: f"https://fbref.com/en/comps/43/{s}/schedule/{s}-Veikkausliiga-Scores-and-Fixtures"
             for s in ("2019", "2020", "2021")}
FBREF_CRAWL = {"2019": "2026-09-05T12:13:00+00:00", "2020": "2026-09-05T10:35:00+00:00",
               "2021": "2026-08-27T05:07:00+00:00"}
WIKI_MTIME = {"2019": "2026-10-28T16:11:44+08:00", "2020": "2026-10-28T16:11:46+08:00",
              "2021": "2026-10-28T16:11:48+08:00"}
SHA_NOTE = "text layer only, no bytes downloaded; null per provenance rule, not a descriptor hash"
MEETING_ATTEMPTS = {
    "2019": "Official Veikkausliiga schedule (veikkausliiga.com archive, HTTP 500), Tulospalvelu (JS-only app, API Cloudflare-blocked), Soccerway ROUND grouping, FBref Wk column: none defines a meeting_number for these fixtures; not inferred from date order, team appearance counts, results, standings or odds (per task rule).",
    "2020": "Official Veikkausliiga schedule (veikkausliiga.com archive, HTTP 500), Tulospalvelu (JS-only app, API Cloudflare-blocked), Soccerway ROUND grouping, FBref Wk column: none defines a meeting_number for these fixtures; not inferred from date order, team appearance counts, results, standings or odds (per task rule).",
    "2021": "Official Veikkausliiga schedule (veikkausliiga.com archive, HTTP 500), Tulospalvelu (JS-only app, API Cloudflare-blocked), Soccerway ROUND grouping, FBref Wk column: none defines a meeting_number for these fixtures; not inferred from date order, team appearance counts, results, standings or odds (per task rule).",
}
KICKOFF_HANDLING = {
    "2019": "fbref_local_all_rows: FBref Time column read per row for all 162 matches; -004 values were exactly FBref-2h on all 132 non-null rows (UK-clock values mislabelled Europe/Helsinki, consistent with the C-road 2022 finding and Soccerway-epoch validation); 30 -004-null rows filled from FBref; old values in kickoff_004_old; UTC via zoneinfo (EEST UTC+3; all 2019 dates inside DST 2019-03-31..2019-10-27).",
    "2020": "fbref_local_all_rows: FBref Time column read per row for all 132 matches; -004 values equal FBref on 57/61 non-null rows (no systematic +2h offset in 2020, unlike 2019/2021); 71 -004-null rows filled from FBref; 4 rows differ from -004 (see kickoff_conflict_note); UTC via zoneinfo (EEST UTC+3 in DST to 2020-10-25, EET UTC+2 after).",
    "2021": "fbref_local_all_rows: FBref Time column read per row for all 162 matches; -004 values were exactly FBref-2h on all 147 non-null rows (UK-clock values mislabelled Europe/Helsinki, consistent with the C-road 2022 finding and Soccerway-epoch validation); 15 -004-null rows filled from FBref; old values in kickoff_004_old; UTC via zoneinfo (EEST UTC+3 in DST to 2021-10-31 01:00 UTC, EET UTC+2 after; 2021-10-31 matches are EET).",
}

def utc_of(date, hhmm, tzname):
    if ZoneInfo is not None:
        z = ZoneInfo(tzname)
        dt = datetime.strptime(date + " " + hhmm, "%Y-%m-%d %H:%M").replace(tzinfo=z)
        return dt.astimezone(timezone.utc).strftime("%H:%M")
    # manual fallback (DST tables)
    dst_end = {"2019": "2019-10-27", "2020": "2020-10-25", "2021": "2021-10-31"}
    off = 3 if date <= dst_end[date[:4]] or (date[:4] == "2021" and date == "2021-10-31" and False) else 2
    if date[:4] == "2021" and date == "2021-10-31":
        off = 2
    h, m = map(int, hhmm.split(":"))
    tot = (h * 60 + m - off * 60) % 1440
    return f"{tot // 60:02d}:{tot % 60:02d}"

def club_identity(team, season):
    if season in SPLIT:
        top, bot, topname, botname = SPLIT[season]
        split = topname if team in top else (botname if team in bot else None)
    else:
        split = None
    notes = f"Founded {FOUNDED[team]} (English Wikipedia club infobox wikitext, downloaded 2026-10-28 via Wikipedia API)."
    if split:
        notes += f" {season} split group: {split}."
    else:
        notes += f" {season}: no split (single-season format)."
    if team in ("Rovaniemi PS", "Rovaniemen PS"):
        notes += " Name variant: 'Rovaniemi PS' in 2019 -004 rows, 'Rovaniemen PS' in 2020 -004 rows; same club (RoPS); rows not merged."
    return {"city_" + season: CITY[team],
            "founded_source": "English Wikipedia club infobox wikitext (Wikipedia API, downloaded 2026-10-28)",
            "founded_year": FOUNDED[team],
            "notes": notes,
            "split_group_" + season: split,
            "stadium_" + season + "_season_mapping": MAPPING[season][team],
            "team": team}

def series_phase(season, s):
    if season == "2020":
        return "regular_season"
    if s is None:
        return "regular_season"
    if season == "2019":
        return "championship_series" if s == "championship" else "challenger_series"
    return "championship_round" if s == "championship" else "relegation_round"

out = []
stats = collections.Counter()
for season in ("2019", "2020", "2021"):
    rows = [r for r in D004 if str(r["season"]) == season]
    ov = [json.loads(l) for l in open(f"{EV}fbref_{season}_overlay.jsonl") if l.strip()]
    by_key, by_pair = {}, collections.defaultdict(list)
    for o in ov:
        h, a = norm_team(o["h"], season), norm_team(o["a"], season)
        by_key[(o["d"], h, a)] = o
        by_pair[(h, a)].append(o)
    for r in rows:
        if r["date"] is None:
            cands = by_pair[(r["home_team"], r["away_team"])]
            assert len(cands) == 1, r["fixture_key"]
            o, match_kind = cands[0], "date-null-match"
        else:
            o = by_key.get((r["date"], r["home_team"], r["away_team"]))
            if o is not None:
                match_kind = "exact"
            else:
                cands = by_pair[(r["home_team"], r["away_team"])]
                assert len(cands) == 1, r["fixture_key"]
                o, match_kind = cands[0], "DATE-CONFLICT"
        fb_time, fb_venue, fb_wk, fb_series = o["t"], o["v"], o["w"], o["s"]
        vname, vcity, vlat, vlon, vprec, vcsrc = canon_of(fb_venue)
        old_venue, old_city = r.get("venue"), r.get("city")
        old_map_canon = canon_of(old_venue)[0] if old_venue in CANON else old_venue
        # venue status
        if vname == old_map_canon:
            if fb_venue != old_venue:
                vrole = "season_home_mapping AND fbref_match_level_venue agree after alias normalisation (same ground, different name)"
            else:
                vrole = "season_home_mapping AND fbref_match_level_venue agree"
            vstatus = "confirmed"
            vcands = [{"city": vcity, "role": vrole, "venue": vname}]
            vnote = (f"Venue: FBref match-level venue agrees with -004 season-home mapping after alias normalisation "
                     f"(FBref '{fb_venue}' = mapping '{old_venue}', same ground); no official league/club match page retrieved, so venue_official_confirmation=false.")
        elif vname == "OmaSP Stadion":
            vstatus = "moved"
            vcands = [{"city": vcity, "role": "fbref_match_level_venue (adopted as venue_verified)", "venue": vname},
                      {"city": old_city, "role": "season_home_mapping (NOT confirmed for this match)", "venue": old_venue}]
            vnote = (f"Venue MOVED: FBref match-level venue OmaSP Stadion (Seinäjoki) differs from -004 season-home mapping "
                     f"Kokkolan keskuskenttä (Kokkola); FBref value adopted as venue_verified; reason for the relocation not sourced (FBref gives the venue, not the reason).")
        elif vname == "Kisapuisto":
            vstatus = "confirmed"
            vcands = [{"city": vcity, "role": "fbref_match_level_venue (adopted as venue_verified; same-city ground use, see notes)", "venue": vname},
                      {"city": old_city, "role": "season_home_mapping (NOT confirmed for this match)", "venue": old_venue}]
            vnote = (f"Venue: FBref match-level venue Kisapuisto (Lahti) differs from -004 season-home mapping Lahden Stadion; "
                     f"same-city ground use early in the season (Kisapuisto for Lahti home matches up to 2019-05-20, Lahden Stadion thereafter); "
                     f"coordinates geocoded this round (map.geocode, Lahden Kisapuisto, Kartanonkatu, Lahti).")
        elif vname == "Ratinan stadion":
            vstatus = "confirmed"
            vcands = [{"city": vcity, "role": "fbref_match_level_venue (adopted as venue_verified; same-city ground use, see notes)", "venue": vname},
                      {"city": old_city, "role": "season_home_mapping (NOT confirmed for this match)", "venue": old_venue}]
            if season == "2019":
                vnote = (f"Venue: FBref match-level venue Ratinan stadion (Tampere) differs from -004 season-home mapping Tammelan Stadion; "
                         f"same-city ground use early in the season (Ratinan for Ilves home matches on 2019-04-14 and 2019-04-26, Tammelan thereafter).")
            else:
                vnote = (f"Venue: FBref match-level venue Ratinan stadion (Tampere) differs from -004 season-home mapping Tammelan Stadion; "
                         f"same-city ground use (Ratinan for 10 of 11 Ilves home matches in 2020; the 2020-08-05 home match vs RoPS is at Tammelan Stadion).")
        else:
            raise AssertionError(f"unhandled venue diff {r['fixture_key']}: {old_venue} -> {fb_venue}")
        # kickoff
        old_ko = r.get("kickoff")
        vtzone = "Europe/Mariehamn" if r["home_team"] == "IFK Mariehamn" else "Europe/Helsinki"
        utc = utc_of(o["d"], fb_time, vtzone)
        if old_ko is None:
            kchange = f"null (req-20261006-004) -> {fb_time} {vtzone} local (filled from FBref Time column); UTC {utc}"
            kconf, knote = None, None
            ksent = f"Kickoff filled from FBref local time ({fb_time}); -004 had null."
            stats["kickoff_filled"] += 1
        elif old_ko == fb_time:
            kchange = f"{fb_time} unchanged (req-20261006-004 == FBref local); UTC {utc}"
            kconf, knote = None, None
            ksent = f"Kickoff unchanged: -004 {fb_time} == FBref local."
            stats["kickoff_unchanged"] += 1
        else:
            kchange = f"{old_ko} (req-20261006-004, labelled Europe/Helsinki) -> {fb_time} {vtzone} local (FBref Time column); UTC {utc}"
            kconf = f"-004 kickoff {old_ko} (labelled Europe/Helsinki) differs from FBref local time {fb_time}; FBref value adopted."
            knote = None
            ksent = f"Kickoff corrected: -004 {old_ko} -> FBref local {fb_time} (see kickoff_change)."
            stats["kickoff_replaced"] += 1
        if r["fixture_key"] == "2019|2019-06-29|Rovaniemi PS|KPV Kokkola":
            knote = "22:15 late kickoff as listed by FBref; -004 value was 20:15, consistent with the season-wide +2h pattern, no separate anomaly."
        # date
        new_date = o["d"]
        date_old = None
        if match_kind == "DATE-CONFLICT":
            date_old = r["date"]
            stats["date_corrected"] += 1
        elif match_kind == "date-null-match":
            stats["date_filled"] += 1
        # round
        old_round = r.get("official_round")
        is_series = fb_series is not None
        if season == "2021" and r["fixture_key"] == "2021|2021-09-14|Ilves Tampere|Helsingfors IFK":
            oround, okind, osource, ostatus = None, None, None, "conflict"
            rnon = ("FBref Wk14 label conflicts with group completeness: Wk14 already has 6 matches/12 teams without this match, "
                    "while Wk19 has 5 matches and lacks exactly Ilves+Helsinki IFK; likely an FBref Wk mislabel, but not overridden by inference.")
            rnon_src = "fbref_week_bucket_conflict"
            rsent = ("official_round left null: FBref Wk14 label conflicts with group completeness (Wk14 already has 6 matches/12 teams without this match; "
                     "Wk19 has 5 matches and lacks exactly Ilves+Helsinki IFK); likely an FBref Wk mislabel, but not overridden by inference.")
            rstatus = "conflict"
            stats["round_conflict_null"] += 1
        elif old_round is not None:
            oround, okind = int(old_round), "numeric"
            osource = "Soccerway round grouping (retained from -004; non-official cross-check, not FA-issued)"
            ostatus = "from_req-20261006-004"
            rnon = "Soccerway round grouping retained from -004 (non-official cross-check, not FA-issued)"
            rnon_src = "req-20261006-004"
            if is_series:
                rsent = f"official_round retained from -004 ({old_round}, series numbering); FBref series Wk {fb_wk} corroborates (22+Wk={22 + fb_wk})."
            else:
                rsent = f"official_round retained from -004 ({old_round}, Soccerway round grouping, non-official cross-check)."
            rstatus = None
            stats["round_retained"] += 1
        else:
            oround, okind = fb_wk, "numeric"
            osource = ("FBref Wk, validated as the round system: 2020 -004 rounds == FBref Wk on all 127 non-null rows, and "
                       "2021 regular Wk groups validated for completeness (21/22 groups exactly 6 matches/12 teams; see notes)")
            ostatus = "filled_from_fbref_wk"
            rnon, rnon_src = None, None
            rsent = f"official_round filled from FBref Wk {fb_wk} (validated round system; not FA-issued)."
            rstatus = None
            stats["round_filled"] += 1
        # row status: conflict is reserved for individual anomalies (date misdatings,
        # non-systematic time disagreements, round-label conflict). The systematic +2h
        # relabeling of -004 UK-clock times in 2019/2021 is a uniform source-semantics
        # correction validated on 100% of non-null rows, recorded per-row in
        # kickoff_change, and does not by itself make a row 'conflict'.
        is_time_anomaly = (match_kind == "exact" and old_ko is not None and old_ko != fb_time
                           and season == "2020")
        if match_kind == "DATE-CONFLICT" or rstatus == "conflict" or is_time_anomaly:
            row_status = "conflict"
            stats["rows_conflict"] += 1
        elif new_date and fb_time and vname and oround is not None:
            row_status = "complete"
            stats["rows_complete"] += 1
        else:
            row_status = "partial"
            stats["rows_partial"] += 1
        # notes
        notes = f"Carried over from -004 (fixture_key unchanged). {ksent} {vnote} {rsent}"
        if match_kind == "DATE-CONFLICT":
            if r["fixture_key"] == "2020|2020-11-04|Helsingfors IFK|Rovaniemen PS":
                notes += (" DATE CORRECTION: -004 date 2020-11-04 corrected to 2020-10-22 per FBref match-level row; FBref has no HIFK-RoPS match on Nov 4 "
                          "(Nov 4's six matches are all other fixtures, round 22 complete without it), while the Oct 22 round-21 cluster is complete with it; "
                          "kickoff corrected 18:30 -> 18:00; round filled 21 from FBref Wk21; fixture_key preserved for the -004 join (see date_004_old).")
            else:
                notes += (" DATE CORRECTION: -004 date 2020-09-19 corrected to 2020-09-20 per FBref match-level row (no Honka-HJK match on Sep 19 in FBref; "
                          "Sep 20 13:00 match at Tapiolan Urheilupuisto); kickoff corrected 18:30 -> 13:00; round 15 unchanged (FBref Wk15 == -004 round 15); "
                          "fixture_key preserved for the -004 join (see date_004_old).")
        if match_kind == "date-null-match":
            notes += f" Date filled from FBref match-level row ({new_date}); -004 had null."
        notes += " Meeting number unavailable. CSV join pending (requester CSV path does not exist on this VM; no fuzzy matching attempted)."
        if vstatus == "moved":
            stats["venue_moved"] += 1
        elif vname != old_map_canon:
            stats["venue_ground_changed"] += 1
        else:
            stats["venue_confirmed"] += 1
        if vname == "OmaSP Stadion" and old_map_canon != "OmaSP Stadion":
            pass
        # provenance
        fb_table_desc = {"2019": "regular season + championship/challenger series Wk1-5 (FBref Wk blank for regular rows)",
                         "2020": "regular season Wk1-22",
                         "2021": "regular Wk1-22 + championship/relegation Wk1-5"}[season]
        prov = {
            "club_identity": {"field_locator": f"English Wikipedia {season} Veikkausliiga page, Teams/Stadia sections; club infobox wikitext via Wikipedia API (founded year)",
                              "final_url": f"https://en.wikipedia.org/wiki/{season}_Veikkausliiga",
                              "retrieved_at": WIKI_MTIME[season], "sha256_note": SHA_NOTE,
                              "source_name": f"Wikipedia {season} Veikkausliiga + club infobox wikitexts",
                              "source_sha256": None,
                              "source_url": f"https://en.wikipedia.org/wiki/{season}_Veikkausliiga"},
            "identity_date_teams": {"field_locator": f"FBref {season} schedule table (full table read: {fb_table_desc}) + -004 row",
                                    "final_url": FBREF_URL[season], "retrieved_at": FBREF_CRAWL[season],
                                    "sha256_note": SHA_NOTE, "source_name": "FBref + req-20261006-004",
                                    "source_sha256": None, "source_url": FBREF_URL[season]},
            "kickoff": {"field_locator": "FBref schedule Time column, per match",
                        "final_url": FBREF_URL[season], "retrieved_at": FBREF_CRAWL[season],
                        "sha256_note": SHA_NOTE, "source_name": "FBref",
                        "source_sha256": None, "source_url": FBREF_URL[season]},
            "round": {"field_locator": ("Soccerway ROUND grouping via -004 row" if old_round is not None else "FBref Wk column, per match + Wk-group completeness validation"),
                      "final_url": (r.get("final_url") if old_round is not None else FBREF_URL[season]),
                      "retrieved_at": (r.get("retrieved_at") if old_round is not None else FBREF_CRAWL[season]),
                      "sha256_note": SHA_NOTE,
                      "source_name": (r.get("source_name") if old_round is not None else "FBref (Wk column)"),
                      "source_sha256": None,
                      "source_url": (r.get("source_url") if old_round is not None else FBREF_URL[season])},
            "venue": {"field_locator": "FBref schedule Venue column per match + Wikipedia season Stadia and locations table",
                      "final_url": FBREF_URL[season], "retrieved_at": FBREF_CRAWL[season],
                      "sha256_note": SHA_NOTE, "source_name": "FBref (match-level) + Wikipedia (season mapping)",
                      "source_sha256": None, "source_url": FBREF_URL[season]},
        }
        row = {"away_club_identity": club_identity(r["away_team"], season),
               "away_team": r["away_team"],
               "csv_join_note": None,
               "csv_join_status": "matched_to_req-20261006-004_row_csv_join_pending",
               "date": new_date,
               "fbref_week_bucket": fb_wk,
               "fixture_key": r["fixture_key"],
               "home_club_identity": club_identity(r["home_team"], season),
               "home_team": r["home_team"],
               "kickoff_004_old": old_ko,
               "kickoff_change": kchange,
               "kickoff_conflict_note": kconf,
               "kickoff_handling": KICKOFF_HANDLING[season],
               "kickoff_local": fb_time,
               "kickoff_note": knote,
               "kickoff_old_req20261006_004": None,
               "kickoff_timezone": vtzone,
               "kickoff_timezone_method": "FBref Time column is venue-local time; zone = venue IANA zone (Europe/Mariehamn for Wiklöf Holding Arena home matches, Europe/Helsinki otherwise); UTC computed with zoneinfo from local time + zone (EEST UTC+3 in DST, EET UTC+2 after DST end; DST ends 2019-10-27, 2020-10-25, 2021-10-31 01:00 UTC).",
               "kickoff_utc": utc,
               "meeting_number": None,
               "meeting_number_attempted": None,
               "meeting_number_attempted_sources": None,
               "meeting_number_attempts": MEETING_ATTEMPTS[season],
               "meeting_number_note": None,
               "meeting_number_status": "unavailable",
               "notes": notes,
               "official_round": oround,
               "official_round_is_official": None,
               "official_round_kind": okind,
               "official_round_source": osource,
               "official_round_status": ostatus,
               "provenance": prov,
               "round_non_official": rnon,
               "round_non_official_source": rnon_src,
               "row_status": row_status,
               "season": season,
               "series_or_phase": series_phase(season, fb_series),
               "series_or_phase_note": ("No series rounds in 2020: -004 and Wikipedia section structure agree; the cancelled 5-team Europa Conference League qualification competition noted on Wikipedia is a different matter, not a championship/relegation series." if season == "2020" else None),
               "series_week_fbref": fb_wk if is_series else None,
               "venue_candidate": old_venue,
               "venue_candidate_city": old_city,
               "venue_candidates": vcands,
               "venue_coords_precision": vprec,
               "venue_coords_source": vcsrc,
               "venue_evidence_tier": "fbref_match_level_secondary",
               "venue_lat": vlat,
               "venue_lon": vlon,
               "venue_official_confirmation": False,
               "venue_status": vstatus,
               "venue_timezone": vtzone,
               "venue_verified": vname,
               "venue_verified_city": vcity}
        if date_old is not None:
            row["date_004_old"] = date_old
        out.append(row)

out.sort(key=lambda x: (x["season"], x["date"], x["home_team"]))
with open(WORK + "method_context_2019_2021.jsonl", "w") as f:
    for row in out:
        f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
print("rows written:", len(out))
for k in sorted(stats):
    print(f"  {k}: {stats[k]}")
# per-season status counts
for season in ("2019", "2020", "2021"):
    sub = [r for r in out if r["season"] == season]
    c = collections.Counter(r["row_status"] for r in sub)
    print(season, dict(c), "total", len(sub))
# key check
keys = set()
for r in out:
    keys |= set(r.keys())
print("distinct keys:", len(keys), sorted(keys))
# assertions
assert len(out) == 456
assert len({r["fixture_key"] for r in out}) == 456
assert all(r["venue_verified"] for r in out)
assert all(r["kickoff_local"] for r in out)
assert all(r["date"] for r in out)
print("assertions passed")
