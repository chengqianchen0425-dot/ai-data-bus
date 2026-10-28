import json

TS_URL = "https://www.topscorersfootball.com/veikkausliiga/standing-and-matches-2026"
TS_SHA = "ac4bc404ce6e3bbe8f3b75aa017fe0990c71d1277c6fbf09dd314bb074e996a2"
TS_RETRIEVED = "2026-10-28T16:12:00+08:00"
WIKI_URL = "https://en.wikipedia.org/wiki/2026_Veikkausliiga"
WIKI_SHA = "792e4fd6bdc69b995a07e6e31503d89f7abb0730e8146d218ebd118b0904256d"
WIKI_RETRIEVED = "2026-10-28T16:13:00+08:00"
FS_URL = "https://www.flashscore.co.ke/news/soccer-veikkausliiga-veikkausliiga-2026-season-preview-kups-title-again-or-can-hjk-bounce-back/OSSLRfPG/"
FS_RETRIEVED = "2026-10-28T16:13:00+08:00"

# canonical club name -> identity (founded year from Wikipedia club infobox, byte captures in evidence/club_*.html)
CLUBS = {
    "Oulu":      {"canonical": "AC Oulu", "founded": 2002, "lineage": None, "entry_2026": None},
    "Inter Turku": {"canonical": "FC Inter Turku", "founded": 1990, "lineage": None, "entry_2026": None},
    "Lahti":     {"canonical": "FC Lahti", "founded": 1996, "lineage": None, "entry_2026": 2026},
    "Jaro":      {"canonical": "FF Jaro", "founded": 1965, "lineage": None, "entry_2026": None},
    "HJK":       {"canonical": "HJK Helsinki", "founded": 1907, "lineage": "Founded 19 June 1907.", "entry_2026": None},
    "Gnistan":   {"canonical": "IF Gnistan", "founded": 1924, "lineage": None, "entry_2026": None},
    "Mariehamn": {"canonical": "IFK Mariehamn", "founded": 1919, "lineage": None, "entry_2026": None},
    "Ilves":     {"canonical": "Ilves", "founded": 1931, "lineage": "Multi-sport club; football ground is Tammelan Stadion per the 2026 season table (club infobox lists an ice-hockey arena, not used).", "entry_2026": None},
    "KuPS":      {"canonical": "Kuopion Palloseura (KuPS)", "founded": 1923, "lineage": None, "entry_2026": None},
    "SJK Seinäjoki": {"canonical": "SJK Seinäjoki", "founded": 2007, "lineage": "Founded 5 November 2007 after the merger of TP-Seinäjoki and Sepsi-78 (club page). Promotion to Veikkausliiga in 2014 is stated on the club page; the first top-flight season itself is not separately confirmed here, so competition_entry_year stays null.", "entry_2026": None},
    "TPS":       {"canonical": "Turun Palloseura (TPS)", "founded": 1922, "lineage": None, "entry_2026": 2026},
    "VPS":       {"canonical": "Vaasan Palloseura (VPS)", "founded": 1924, "lineage": None, "entry_2026": None},
}
# topscorers labels are the keys above; note SJK label is "SJK Seinäjoki", VPS label is "VPS"

# season stadium table (Wikipedia 2026 teams table) + geocode results; venue is a CANDIDATE, never fixture-confirmed
VENUES = {
    "Oulu": {"name": "Raatti Stadium", "city": "Oulu", "lat": 65.01973, "lon": 25.46442, "latlon_note": "Geocode FULL_ADDRESS match (relevance 100) for Raatti Stadium, Oulu.",
             "status": "conflict", "competing": ["Heinäpää Stadium (club page stadium section: Heinäpää Stadium 2026–present; Raatti Stadium 2011–2026) - a mid-2026 home-ground change is possible, so no single venue is confirmed for any AC Oulu home fixture."],
             "tz": "Europe/Helsinki"},
    "Inter Turku": {"name": "Veritas Stadion", "city": "Turku", "lat": 60.443, "lon": 22.29045, "latlon_note": "Geocode FULL_ADDRESS match (relevance 90).",
             "status": "neutral", "competing": [], "tz": "Europe/Helsinki"},
    "Lahti": {"name": "Lahti Stadium", "city": "Lahti", "lat": 60.98279, "lon": 25.66243, "latlon_note": "Geocode FULL_ADDRESS match (relevance 100).",
             "status": "neutral", "competing": ["Toolpoint Arena (sponsor name on the club page for the Lahti ground; treated as an alternate name for the same ground, not a separate venue)."], "tz": "Europe/Helsinki"},
    "Jaro": {"name": "Project Liv Arena", "city": "Jakobstad (Pietarsaari)", "lat": None, "lon": None,
             "latlon_note": "Coordinates NOT confirmed. Geocode candidates disagree and neither is a confirmed stadium match: Centralvägen street point (63.6745, 22.68205, STREET level) and Styrmansgatan point (63.67603, 22.70633, relevance 74, matched to a construction firm, not a stadium).",
             "status": "conflict", "competing": ["Jakobstads Centralplan (older name for the Jakobstad ground in earlier sources; the 2026 season table lists Project Liv Arena). Whether this is a rename or a new ground is not confirmed by a single source in this round."], "tz": "Europe/Helsinki"},
    "HJK": {"name": "Bolt Arena", "city": "Helsinki", "lat": 60.1875, "lon": 24.92209, "latlon_note": "Geocode FULL_ADDRESS match (relevance 100).",
             "status": "neutral", "competing": ["Töölö Football Stadium (generic name on the club page for the same ground)."], "tz": "Europe/Helsinki"},
    "Gnistan": {"name": "Markku.fi Areena", "city": "Helsinki (Oulunkylä)", "lat": 60.23381, "lon": 24.96251,
             "latlon_note": "Coordinates are for Mustapekka Areena, Käskynhaltijantie 11, Oulunkylä (geocode FULL_ADDRESS, relevance 100); the ground location is used, the name is the disputed part.",
             "status": "conflict", "competing": ["Mustapekka Areena (name used in the upcoming-fixture listing for Gnistan home fixtures, e.g. Gnistan vs VPS on 8 Nov 2026)", "Oulunkylä Football Stadium (generic name on the club page). A July 2024 fire at Mustapekka Areena is reported on the club page, which may explain a later rename, but no single source in this round confirms the names denote the same ground."], "tz": "Europe/Helsinki"},
    "Mariehamn": {"name": "Wiklöf Holding Arena", "city": "Mariehamn", "lat": None, "lon": None,
             "latlon_note": "Coordinates NOT confirmed. Geocode candidates: Idrottsgatan street point (60.10325, 19.93565, STREET level, relevance 52) and a central-Mariehamn business address (60.09788, 19.94165, relevance 88, not a stadium). Neither is a confirmed stadium match.",
             "status": "neutral", "competing": [], "tz": "Europe/Mariehamn"},
    "Ilves": {"name": "Tammelan Stadion", "city": "Tampere", "lat": 61.50028, "lon": 23.78538, "latlon_note": "Geocode FULL_ADDRESS match (relevance 100).",
             "status": "neutral", "competing": [], "tz": "Europe/Helsinki"},
    "KuPS": {"name": "Väre Areena", "city": "Kuopio", "lat": None, "lon": None,
             "latlon_note": "Coordinates NOT confirmed: two geocode results disagree (62.82283, 27.60319, relevance 51; 62.83599, 27.62325, relevance 79). Neither is confirmed as the stadium.",
             "status": "neutral", "competing": ["Kuopio Football Stadium (generic English name used in fixture listings for the same club ground)."], "tz": "Europe/Helsinki"},
    "SJK Seinäjoki": {"name": "OmaSP Stadion", "city": "Seinäjoki", "lat": 62.77903, "lon": 22.81542, "latlon_note": "Geocode FULL_ADDRESS match (relevance 100).",
             "status": "neutral", "competing": [], "tz": "Europe/Helsinki"},
    "TPS": {"name": "Veritas Stadion", "city": "Turku", "lat": 60.443, "lon": 22.29045, "latlon_note": "Geocode FULL_ADDRESS match (relevance 90); shared with FC Inter Turku.",
             "status": "neutral", "competing": [], "tz": "Europe/Helsinki"},
    "VPS": {"name": "Hietalahti Stadium", "city": "Vaasa", "lat": 63.08551, "lon": 21.62855,
             "latlon_note": "Coordinates are for Elisa Stadion, Rantamaantie 6, Vaasa (geocode FULL_ADDRESS, relevance 100); Elisa Stadion is the sponsor name for the Hietalahti ground.",
             "status": "conflict", "competing": ["Elisa Stadion (sponsor name used in fixture listings, e.g. VPS vs HJK on 2 Nov 2026). Name conflict only; the ground address is the same."], "tz": "Europe/Helsinki"},
}

ROUND1_TIMES = {  # Flashscore preview, "All times CEST" as labelled by that source
    ("Inter Turku", "VPS"): "12:00",
    ("HJK", "SJK Seinäjoki"): "14:00",
    ("Ilves", "KuPS"): "16:00",
    ("Jaro", "Lahti"): "16:00",
    ("Mariehamn", "TPS"): "16:00",
    ("Gnistan", "Oulu"): "18:00",
}

rows = json.load(open('evidence/fixtures_enriched.json'))
out = []
for r in rows:
    home, away = r['home'], r['away']
    v = VENUES[home]
    hc, ac = CLUBS[home], CLUBS[away]
    stage = r['stage']
    if stage == 'regular':
        stage_format = "Double round robin (each pair twice) in the regular season."
        double_rr = True
    elif stage == 'championship':
        stage_format = "Championship group: top 6 after the regular season, double round robin (each pair twice more, 10 further matches per club)."
        double_rr = True
    else:
        stage_format = "Relegation group: bottom 6 after the regular season, single round robin (each pair once more, 5 further matches per club)."
        double_rr = False
    t = ROUND1_TIMES.get((home, away))
    if r['round'] == 1 and t:
        ko_time, ko_tz, ko_sem = t, "CEST (as labelled by Flashscore preview)", "Kickoff time as listed in the Flashscore season preview under the heading 'All times CEST'. Finland local time is EEST (UTC+3) in April, which differs from CEST (UTC+2); the source label is preserved verbatim and NO UTC conversion is asserted, so kickoff_utc stays null."
        ko_prov = {"source_name": "Flashscore season preview (flashscore.co.ke)", "source_url": FS_URL, "final_url": FS_URL, "retrieved_at": FS_RETRIEVED, "field_locator": "Section 'The opening weekend', 'All times CEST', Saturday 4th April list", "source_sha256": None, "source_sha256_note": "null: browser text layer only, no source bytes captured; a text-layer hash must never be presented as a source hash."}
    else:
        ko_time, ko_tz, ko_sem = None, None, "No kickoff time in the fixture source: topscorersfootball publishes match dates only. Time is left null, never guessed."
        ko_prov = None
    # row status
    if r['meeting_number'] is None:
        status, status_reason = "conflict", "meeting_number is null because round-order and date-order counting disagree for this pair (brought-forward fixtures: a later-round match was played before an earlier-round match of the same pair). Both the round label and the date are kept as published; no meeting number is asserted."
    elif v['status'] == 'conflict':
        status, status_reason = "partial", "Venue name has competing candidates (see venue_competing_candidates); venue is a season-table candidate, not fixture-confirmed, so venue_verified is null."
    else:
        status, status_reason = "complete", "Season, date, teams, round label, stage and (where unambiguous) meeting_number are all present from the published schedule. Venue is still only a season-table candidate (venue_verified null) and kickoff time is present only for round 1; see the separate venue/kickoff fields, which are not folded into this status."
    out.append({
        "season": 2026,
        "row_key": f"2026|{r['date']}|{home}|{away}",
        "csv_join_status": "csv_unavailable_on_this_vm_derived_from_public_schedule",
        "csv_join_note": "The requester's identity CSV (Windows path D:\\...method_context_request_fixtures_20261028.csv) does not exist on this VM and could not be read. Rows are keyed season|match_date|home_team|away_team from the public schedule only; NO claim of exact correspondence to the CSV is made and NO fuzzy matching was performed.",
        "match_date": r['date'],
        "match_date_text_as_published": r['date_text'],
        "home_team_source_label": home,
        "away_team_source_label": away,
        "home_team_canonical": hc['canonical'],
        "away_team_canonical": ac['canonical'],
        "official_round": r['round_label'],
        "official_round_number": r['round'],
        "official_round_basis": "Round label as published in the topscorersfootball 'All matches' list. The Veikkausliiga official schedule document itself was not retrieved in this round, so this is a source round label, not a claim about the league's official round wording.",
        "stage": stage,
        "stage_format": stage_format,
        "double_round_robin": double_rr,
        "meeting_number": r['meeting_number'],
        "meeting_number_basis": "Occurrence index of the unordered pair in the published schedule, counted in round order; round-order and date-order counting agree for this pair." if r['meeting_number'] else "NULL: round-order and date-order counting disagree for this pair (see status_reason). No meeting number is published by any source retrieved in this round; meeting_number_published is false for every row.",
        "meeting_number_published": False,
        "home_club_founded_year_natal": hc['founded'],
        "away_club_founded_year_natal": ac['founded'],
        "home_club_lineage_note": hc['lineage'],
        "away_club_lineage_note": ac['lineage'],
        "home_club_competition_entry_year": hc['entry_2026'],
        "away_club_competition_entry_year": ac['entry_2026'],
        "competition_entry_year_definition": "Year the club entered the 2026 Veikkausliiga by promotion (Lahti and TPS, promoted from Ykkösliiga, per the Flashscore preview calling them 'promoted sides'). For all other clubs the first top-flight season was not verified in this round, so the field is null rather than guessed.",
        "competition_entry_year_note": "Promoted-club entry is 2026 for Lahti and TPS only; every other club's competition_entry_year is null (unverified), not 2026 and not the founding year.",
        "kickoff_local_time": ko_time,
        "kickoff_timezone_as_published": ko_tz,
        "kickoff_utc": None,
        "kickoff_semantics": ko_sem,
        "kickoff_provenance": ko_prov,
        "venue_name_candidate": v['name'],
        "venue_city": v['city'],
        "venue_lat_wgs84": v['lat'],
        "venue_lon_wgs84": v['lon'],
        "venue_latlon_note": v['latlon_note'],
        "venue_iana_timezone": v['tz'],
        "venue_status": v['status'],
        "venue_verified": None,
        "venue_verified_note": "Venue is the home club's ground from the Wikipedia 2026 season stadium table (a season-level table), NOT a fixture-level confirmation. No per-fixture venue evidence was retrieved for any row, so venue_verified is null on all 177 rows. Where venue_status is 'conflict', competing names are listed and none is chosen.",
        "venue_competing_candidates": v['competing'],
        "row_status": status,
        "row_status_reason": status_reason,
        "provenance": {
            "fixture_source": {"source_name": "topscorersfootball.com", "source_url": TS_URL, "final_url": TS_URL, "retrieved_at": TS_RETRIEVED, "field_locator": f"All matches Veikkausliiga 2026, '{r['round_label']}' block, match-details-comp data-apif-id={r['apif_id']}", "source_fixture_id": r['apif_id'], "source_fixture_id_scope": "topscorersfootball match id (not a league official id)", "source_sha256": TS_SHA, "source_sha256_note": "SHA-256 of the captured source bytes file evidence/topscorers_2026.html (154,635 bytes, downloaded 2026-10-28). This is a genuine source-bytes hash, not a descriptor/URL hash.", "evidence_file": "evidence/topscorers_2026.html"},
            "venue_source": {"source_name": "Wikipedia 2026 Veikkausliiga, teams table", "source_url": WIKI_URL, "final_url": WIKI_URL, "retrieved_at": WIKI_RETRIEVED, "field_locator": "Section 'Location of teams in 2026 Veikkausliiga', Club/Location/Stadium table", "source_sha256": WIKI_SHA, "source_sha256_note": "SHA-256 of the captured source bytes file evidence/wiki_2026_veikkausliiga.html.", "evidence_file": "evidence/wiki_2026_veikkausliiga.html"},
            "club_identity_source": {"source_name": "Wikipedia club pages (infobox Founded)", "source_url": "https://en.wikipedia.org/wiki/<club page>", "final_url": None, "retrieved_at": "2026-10-28T16:13:00+08:00 to 2026-10-28T16:14:00+08:00", "field_locator": "Club page infobox, 'Founded' row", "source_sha256": None, "source_sha256_note": "null at row level: per-club page hashes are listed in the build log (evidence/club_*.html SHA-256 values are in the working notes); the row carries the founded year and the club page name, not a fabricated hash. See method_context_2026_notes.md for the per-club hash table."},
        },
    })

with open('method_context_2026.jsonl', 'w') as f:
    for row in out:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
from collections import Counter
print("rows:", len(out))
print("stages:", Counter(r['stage'] for r in out))
print("row_status:", Counter(r['row_status'] for r in out))
print("venue_status:", Counter(r['venue_status'] for r in out))
print("meeting null:", sum(1 for r in out if r['meeting_number'] is None))
print("kickoff present:", sum(1 for r in out if r['kickoff_local_time']))
print("venue lat null:", sum(1 for r in out if r['venue_lat_wgs84'] is None))
print("venue_verified non-null:", sum(1 for r in out if r['venue_verified'] is not None))
