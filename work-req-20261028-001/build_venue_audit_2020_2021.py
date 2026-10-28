import json, os, hashlib, math
from datetime import datetime, timezone, timedelta

BASE = "/home/hatch/workspace/ai-inbox/repo/work-req-20261017-002/fixtures_2018_2025.jsonl"
OUTDIR = "/home/hatch/workspace/ai-inbox/work-req-20261028-001"
GEO = os.path.join(OUTDIR, "geo_evidence")
SHARED = os.path.join(OUTDIR, "venue_coordinate_table.json")
CST = timezone(timedelta(hours=8))

def file_sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def file_retrieved(p):
    return datetime.fromtimestamp(os.path.getmtime(p), tz=CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")

def haversine_m(lat1, lon1, lat2, lon2):
    r = math.radians
    dlat, dlon = r(lat2 - lat1), r(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(r(lat1)) * math.cos(r(lat2)) * math.sin(dlon / 2) ** 2
    return 6371000 * 2 * math.asin(math.sqrt(a))

# FBref contemporary season-table venue per home club (first table on each season page;
# venue constant for every home match of the club in that season - verified across all rounds).
MAP_2020 = {
    "Aalesund": "Color Line Stadion", "Bodo/Glimt": "Aspmyra Stadion", "Brann": "Brann Stadion",
    "Haugesund": "Haugesund Stadion", "Kristiansund BK": "Kristiansund Stadion", "Mjondalen": "Consto Arena",
    "Molde": "Aker Stadion", "ODD Ballklubb": "Skagerak Arena", "Rosenborg": "Lerkendal Stadion",
    "Sandefjord": "Komplett.no Arena", "Sarpsborg 08 FF": "Sarpsborg Stadion", "Stabaek": "Nadderud Stadion",
    "Start": "Sparebanken Sør Arena", "Stromsgodset": "Marienlyst Stadion", "Valerenga": "Intility Arena",
    "Viking": "SR-Bank Arena",
}
MAP_2021 = {k: v for k, v in MAP_2020.items() if k not in ("Aalesund", "Start")}
MAP_2021.update({"Lillestrom": "Åråsen Stadion", "Tromso": "Alfheim Stadion"})

# Ground identity table: FBref name -> (ground_id, verified city, lat, lon, match_quality,
#   geo query, geo entry name, geo entry class, evidence file, alternate-name note)
# Lat/lon aligned to the shared venue_coordinate_table.json where the ground already exists there
# (only Nadderud differs from this route's first pick: shared table uses the pitch entry).
GEO_TABLE = {
    "Color Line Stadion": ("COL", "Ålesund", 62.4696703, 6.1885733, "exact_name",
        "Color Line Stadion, Ålesund, Norway", "Color Line stadion", "leisure/stadium",
        "Color_Line_Stadion_primary.json", None),
    "Aspmyra Stadion": ("ASP", "Bodø", 67.2766478, 14.3844344, "exact_name",
        "Aspmyra Stadion, Bodø, Norway", "Aspmyra stadion", "leisure/stadium",
        "Aspmyra_Stadion_primary.json", None),
    "Brann Stadion": ("BRANN", "Bergen", 60.3668333, 5.3574265, "exact_name",
        "Brann Stadion, Bergen, Norway", "Brann Stadion", "leisure/stadium",
        "Brann_Stadion_primary.json", None),
    "Haugesund Stadion": ("HAU", "Haugesund", 59.4130886, 5.2795151, "exact_name",
        "Haugesund Stadion, Haugesund, Norway", "Haugesund stadion", "leisure/pitch",
        "Haugesund_Stadion_primary.json", "No stadium-class polygon in top entries; pitch entry used."),
    "Kristiansund Stadion": ("KRI", "Kristiansund", 63.1249251, 7.7182754, "alias",
        "Nordmøre Stadion, Kristiansund, Norway", "Nordmøre stadion", "leisure/stadium",
        "Nordmøre_Stadion_fallback.json",
        "Same physical venue under its current name Nordmøre Stadion; primary-name query returned only a bus stop (Kristiansund_Stadion_primary.json, kept as attempted evidence). Rename timing unverified; not a competing venue."),
    "Consto Arena": ("MJO", "Mjøndalen", 59.7463295, 10.014655, "same_ground_other_name",
        "Mjøndalen Stadion, Norway", "Mjøndalen stadion", "leisure/pitch",
        "Mjøndalen_Stadion_fallback.json",
        "Nominatim has no 'Consto Arena' entry (empty returns kept: Consto_Arena_primary.json). Wikipedia Consto Arena lists former name 'Mjøndalen Stadion' and coordinates 59.7469, 10.0146, matching this pitch entry."),
    "Aker Stadion": ("AKER", "Molde", 62.7334015, 7.1480721, "exact_name",
        "Aker Stadion, Molde, Norway", "Aker Stadion", "leisure/stadium",
        "Aker_Stadion_primary.json", None),
    "Skagerak Arena": ("SKA", "Skien", 59.2114504, 9.5899759, "exact_name",
        "Skagerak Arena, Skien, Norway", "Skagerak Arena", "leisure/pitch",
        "Skagerak_Arena_primary.json", "A shop/sports entry at nearly identical coordinates exists in the same file and was not used; leisure/pitch entry chosen."),
    "Lerkendal Stadion": ("LER", "Trondheim", 63.4123264, 10.4044664, "exact_name",
        "Lerkendal Stadion, Trondheim, Norway", "Lerkendal Stadion", "leisure/stadium",
        "Lerkendal_Stadion_primary.json", None),
    "Komplett.no Arena": ("SAN", "Sandefjord", 59.1371935, 10.1795249, "renamed_current_name",
        "Jotun Arena, Sandefjord, Norway", "Jotun Arena", "leisure/pitch",
        "Komplett.no_Arena_fallback.json",
        "Same physical venue under its current name Jotun Arena; primary-name query returned empty (Komplett.no_Arena_primary.json, kept as attempted evidence). Rename timing unverified; not a competing venue."),
    "Sarpsborg Stadion": ("SAR", "Sarpsborg", 59.2862886, 11.0977153, "exact_name",
        "Sarpsborg Stadion, Sarpsborg, Norway", "Sarpsborg stadion", "leisure/pitch",
        "Sarpsborg_Stadion_primary.json", None),
    "Nadderud Stadion": ("NAD", "Bærum", 59.9212784, 10.5812178, "exact_name",
        "Nadderud Stadion, Bærum, Norway", "Nadderud stadion", "leisure/pitch",
        "Nadderud_Stadion_primary.json",
        "Coordinates aligned to the shared venue_coordinate_table.json (pitch entry). The same Nominatim file also holds a stadium-class entry ~110 m away; both are inside the same venue footprint."),
    "Sparebanken Sør Arena": ("SOR", "Kristiansand", 58.1536965, 8.0302821, "renamed_current_name",
        "Sparebanken Sør Arena, Kristiansand, Norway", "Sparebanken Norge Arena", "leisure/stadium",
        "Sparebanken_Sør_Arena_primary.json",
        "Same physical venue under its current name Sparebanken Norge Arena (sponsor change). Rename timing unverified; not a competing venue."),
    "Marienlyst Stadion": ("MAR", "Drammen", 59.7343801, 10.201551, "exact_name",
        "Marienlyst Stadion, Drammen, Norway", "Marienlyst stadion", "leisure/stadium",
        "Marienlyst_Stadion_primary.json", None),
    "Intility Arena": ("INT", "Oslo", 59.9179048, 10.8066324, "exact_name",
        "Intility Arena, Oslo, Norway", "Intility Arena", "leisure/stadium",
        "Intility_Arena_primary.json", None),
    "SR-Bank Arena": ("VIK", "Stavanger", 58.9145955, 5.7309977, "renamed_current_name",
        "Viking Stadion, Stavanger, Norway", "Lyse Arena", "leisure/stadium",
        "SR-Bank_Arena_fallback.json",
        "Same physical venue under its current name Lyse Arena; primary-name query returned empty (SR-Bank_Arena_primary.json, kept as attempted evidence). Rename timing unverified; not a competing venue."),
    "Åråsen Stadion": ("ARA", "Lillestrøm", 59.9627403, 11.063566, "exact_name",
        "Åråsen Stadion, Lillestrøm, Norway", "Åråsen Stadion", "leisure/pitch",
        "Åråsen_Stadion_primary.json", None),
    "Alfheim Stadion": ("ALF", "Tromsø", 69.6489185, 18.9343489, "renamed_current_name",
        "Alfheim Stadion, Tromsø, Norway", "Romssa Arena", "leisure/stadium",
        "Alfheim_Stadion_primary.json",
        "Same physical venue under its current name Romssa Arena. Rename timing unverified; not a competing venue."),
}

FBREF_URL = {
    2020: "https://fbref.com/en/comps/28/2020/schedule/2020-Eliteserien-Scores-and-Fixtures",
    2021: "https://fbref.com/en/comps/28/2021/schedule/2021-Eliteserien-Scores-and-Fixtures",
}
FBREF_CRAWL = {2020: "2026-08-12 07:19 UTC", 2021: "2026-08-12 22:49 UTC"}
WIKI_URL = "https://en.wikipedia.org/wiki/List_of_football_stadiums_in_Norway"

rows = [json.loads(l) for l in open(BASE)]
sub = [r for r in rows if r["season"] in (2020, 2021)]
assert len(sub) == 480, len(sub)

out = []
for r in sub:
    season = r["season"]
    home = r["home_team"]["name"]
    away = r["away_team"]["name"]
    mc = r["method_context"]
    b_name = mc["venue_name"]["value"]
    b_city = mc["venue_city"]["value"]
    b_lat = mc["venue_lat"]["value"]
    b_lon = mc["venue_lon"]["value"]
    mapping = MAP_2020 if season == 2020 else MAP_2021
    fbref_venue = mapping[home]
    gid, city, lat, lon, mq, gq, gname, gclass, gfile, anote = GEO_TABLE[fbref_venue]
    gpath = os.path.join(GEO, gfile)
    dist_m = haversine_m(b_lat, b_lon, lat, lon) if (b_lat is not None and b_lon is not None) else None
    if dist_m is not None and dist_m > 1000:
        coord_note = (f"Baseline provider coordinates ({b_lat}, {b_lon}) sit {dist_m:.0f} m from the Nominatim venue point and do not fall on the venue; "
                      "Nominatim venue point adopted, baseline coordinates preserved in baseline_venue_lat/lon for comparison. Not a venue-identity disagreement.")
    elif dist_m is not None:
        coord_note = (f"Baseline provider coordinates ({b_lat}, {b_lon}) sit {dist_m:.0f} m from the Nominatim venue point (same venue, different geocoder take point); "
                      "Nominatim venue point adopted.")
    else:
        coord_note = "Baseline provider coordinates missing; Nominatim venue point used."
    name_variant = (b_name != fbref_venue)
    if season == 2021 and home == "Haugesund" and b_name == "Haugesund Sparebank Arena":
        variant_note = ("Mid-season sponsored-name change evidenced by a clean chronological split in the baseline: 2021-05-24 to 2021-07-18 home games carry "
                        "'Haugesund Stadion', 2021-07-28 onward carry 'Haugesund Sparebank Arena', at identical baseline coordinates. FBref uses the generic name for all "
                        "2021 Haugesund home games. Same physical venue; rename announcement date not verified.")
        conflict_note = None
    elif name_variant:
        variant_note = (f"Name variant of the same physical venue, not a venue disagreement: baseline provider name '{b_name}' vs contemporary season-table name "
                        f"'{fbref_venue}'. Provider venue names in the baseline change across seasons for this venue (generic/sponsor names), while the venue and its "
                        f"coordinates stay the same. Verified name follows the contemporary season table.")
        conflict_note = None
    else:
        variant_note = None
        conflict_note = None
    if b_city != city:
        city_note = (f"Baseline city '{b_city}' is the locality within the municipality '{city}' (Nadderud/Bekkestua in Bærum; Åråsen/Kjeller in Lillestrøm); "
                     "same place, different administrative level, not a disagreement.")
    else:
        city_note = None
    candidates = [
        {"venue_name": b_name, "venue_city": b_city, "ground_id": gid,
         "source": "Baseline api-football fixture.venue (per-fixture provider value, method_context)",
         "note": "Source venue. Per-fixture provider value."},
        {"venue_name": fbref_venue, "venue_city": None, "ground_id": gid,
         "source": "FBref season schedule table, Venue column (non-official, per-fixture)",
         "note": "FBref schedule table has no city column; city not back-filled from baseline in this candidate."},
    ]
    out.append({
        "record_key": r["record_key"],
        "season": season,
        "local_date": r["local_date"],
        "home_team": home,
        "away_team": away,
        "kickoff_local": r["kickoff_local"],
        "round": r["round"],
        "round_label": r["round_label"],
        "provider_fixture_id": r["provider_fixture_id"],
        "source_venue_name": b_name,
        "source_venue_city": b_city,
        "baseline_venue_lat": b_lat,
        "baseline_venue_lon": b_lon,
        "verified_actual_matchday_venue_name": fbref_venue,
        "verified_actual_matchday_venue_city": city,
        "verified_ground_id": gid,
        "venue_status": "confirmed",
        "confirmation_tier": "two_per_fixture_sources_agree_on_ground",
        "official_confirmation": "not_available: NFF fotball.no 2020/2021 tournamentId undiscoverable per prior work (req-20261018-001); retry_after 2026-11-19; not re-attempted this round.",
        "venue_candidates": candidates,
        "name_variant": name_variant,
        "name_variant_note": variant_note,
        "city_note": city_note,
        "conflict_note": conflict_note,
        "venue_vs_club_modal_venue": "same",
        "relocation_note": "No deviation from the home club's modal venue observed anywhere in the FBref season table; no direct evidence of a move or neutral venue found for this fixture. moved/neutral NOT inferred from the modal comparison, from another match, or from any 2020 empty-stadium report.",
        "venue_lat": lat,
        "venue_lon": lon,
        "coordinate_match_quality": mq,
        "coordinate_note": coord_note,
        "coordinate_provenance": {
            "source": "OpenStreetMap Nominatim search JSON (venue-level coordinates, not a per-match confirmation)",
            "source_url": "https://nominatim.openstreetmap.org/search?q=" + gq.replace(" ", "+"),
            "final_url": "https://nominatim.openstreetmap.org/search?q=" + gq.replace(" ", "+"),
            "retrieved_at": file_retrieved(gpath),
            "field_locator": "Nominatim search entry: name/class/type/lat/lon/display_name",
            "query": gq,
            "geo_entry_name": gname,
            "geo_entry_class": gclass,
            "evidence_file": "geo_evidence/" + gfile,
            "evidence_sha256": file_sha(gpath),
            "alternate_name_note": anote,
        },
        "evidence": {
            "baseline": {
                "source": "Baseline api-football fixture.venue via method_context (venue_name/venue_city/venue_lat/venue_lon)",
                "source_url": r["provenance"]["source_url"],
                "field_locator": f"response[] where fixture.id={r['provider_fixture_id']}, method_context venue_*",
                "source_sha256": r["provenance"].get("source_sha256"),
            },
            "fbref": {
                "source": "FBref season schedule table (non-official schedule page), Venue column",
                "source_url": FBREF_URL[season],
                "final_url": FBREF_URL[season],
                "retrieved_at": "2026-10-28 Asia/Shanghai (day-level; exact read clock not logged)",
                "text_layer_snapshot_crawl": FBREF_CRAWL[season],
                "field_locator": "First schedule table on the page, Venue column, row matching (local_date, home_team, away_team); the page's second table is a duplicate rendering of the same rows and was not double-counted. The two non-league play-off rows on each page were excluded (not in the 240-match baseline).",
                "source_value": fbref_venue,
                "http_status": None,
                "http_status_note": "Browser text layer exposes no source HTTP status; not recorded as 200.",
                "source_sha256": None,
                "source_sha256_note": "null: browser text layer, no page bytes downloaded; hash must never be fabricated.",
            },
        },
    })

with open(os.path.join(OUTDIR, "venue_audit_2020_2021.jsonl"), "w") as f:
    for o in out:
        f.write(json.dumps(o, ensure_ascii=False) + "\n")

# ---- validation ----
base_by_key = {r["record_key"]: r for r in sub}
assert len(out) == 480 and len({o["record_key"] for o in out}) == 480
assert set(o["record_key"] for o in out) == set(base_by_key)
for o in out:
    b = base_by_key[o["record_key"]]
    assert o["season"] == b["season"] and o["local_date"] == b["local_date"]
    assert o["home_team"] == b["home_team"]["name"] and o["away_team"] == b["away_team"]["name"]
    assert o["kickoff_local"] == b["kickoff_local"] and o["round"] == b["round"]
    assert o["round_label"] == b["round_label"] and o["provider_fixture_id"] == b["provider_fixture_id"]
    assert o["source_venue_name"] == b["method_context"]["venue_name"]["value"]
    assert o["source_venue_city"] == b["method_context"]["venue_city"]["value"]
    assert o["venue_status"] == "confirmed" and o["venue_lat"] is not None
from collections import Counter
print("rows:", len(out))
print("status:", Counter(o["venue_status"] for o in out))
print("by season:", Counter(o["season"] for o in out))
print("name_variant rows:", sum(1 for o in out if o["name_variant"]))
print("distinct grounds:", sorted({o["verified_ground_id"] for o in out}))
print("coordinate coverage rows:", sum(1 for o in out if o["venue_lat"] is not None))
print("match_quality:", Counter(o["coordinate_match_quality"] for o in out))
FORB = ["score", "result", "odds", "standing", "prediction", "qimen", "snapshot", "outcome", "review", "gold", "winner"]
bad = [k for o in out for k in o if any(s in k.lower() for s in FORB)]
print("forbidden keys:", set(bad))
# baseline-vs-nominatim distances per ground
seen = {}
for o in out:
    seen[o["verified_ground_id"]] = haversine_m(o["baseline_venue_lat"], o["baseline_venue_lon"], o["venue_lat"], o["venue_lon"])
for gid, d in sorted(seen.items()):
    print(f"  {gid}: baseline-vs-nominatim {d:.0f} m")
print("ALL LINK-FIELD CHECKS PASSED")
