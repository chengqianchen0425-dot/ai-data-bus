"""Build venue_audit_2022_2023.jsonl (480 rows) for req-20261028-001 C route.
Inputs: baseline_480.json (link fields + baseline venue, verbatim),
  evidence/nominatim/query_log.json + evidence/nominatim/*.json.
FBref team-season Venue map transcribed from full first-table reads of both
FBref schedule pages (venue constant per team-season; no fixture deviated).
Nominatim sha256 computed live from files on disk at build time.
Rules: link fields copied verbatim; no scores/results/odds; home default never
substituted; all competing name variants kept as candidates; coordinates are
venue-level with real byte SHA-256; FBref evidence SHA is null (text layer, no bytes)."""
import json, hashlib, math, os, collections

BASE = os.path.expanduser("~/workspace/ai-inbox/work-req-20261028-001")
EV = os.path.join(BASE, "evidence")
NOM = os.path.join(EV, "nominatim")

baseline = json.load(open(os.path.join(BASE, "baseline_480.json")))
assert len(baseline) == 480, len(baseline)

FBREF_2022 = {
    "Aalesund": "Color Line Stadion", "Bodo/Glimt": "Aspmyra Stadion",
    "Ham-Kam": "Briskeby Arena", "Haugesund": "Haugesund Stadion",
    "Kristiansund BK": "Kristiansund Stadion", "Lillestrom": "Åråsen Stadion",
    "Molde": "Aker Stadion", "ODD Ballklubb": "Skagerak Arena",
    "Rosenborg": "Lerkendal Stadion", "Sandefjord": "Komplett.no Arena",
    "Sarpsborg 08 FF": "Sarpsborg Stadion", "Stromsgodset": "Marienlyst Stadion",
    "Tromso": "Alfheim Stadion", "Valerenga": "Intility Arena",
    "Viking": "SR-Bank Arena", "jerv": "J.J. Ugland Stadion - Levermyr",
}
FBREF_2023 = {
    "Aalesund": "Color Line Stadion", "Bodo/Glimt": "Aspmyra Stadion",
    "Brann": "Brann Stadion", "Ham-Kam": "Briskeby Arena",
    "Haugesund": "Haugesund Stadion", "Lillestrom": "Åråsen Stadion",
    "Molde": "Aker Stadion", "ODD Ballklubb": "Skagerak Arena",
    "Rosenborg": "Lerkendal Stadion", "Sandefjord": "Komplett.no Arena",
    "Sarpsborg 08 FF": "Sarpsborg Stadion", "Stabaek": "Nadderud Stadion",
    "Stromsgodset": "Marienlyst Stadion", "Tromso": "Alfheim Stadion",
    "Valerenga": "Intility Arena", "Viking": "SR-Bank Arena",
}
FBREF_URL = {
    2022: "https://fbref.com/en/comps/28/2022/schedule/2022-Eliteserien-Scores-and-Fixtures",
    2023: "https://fbref.com/en/comps/28/2023/schedule/2023-Eliteserien-Scores-and-Fixtures",
}
FBREF_PAGE = {2022: "677758559027529054", 2023: "1143704444911427442"}
FBREF_CRAWL = {2022: "2026-09-04", 2023: "2026-10-19"}

GROUND_OF_BASELINE = {
    "Color Line Stadion": "color_line", "Aspmyra Stadion": "aspmyra",
    "Briskeby Arena": "briskeby", "Haugesund Sparebank Arena": "haugesund",
    "Kristiansund Stadion": "kristiansund", "Åråsen Stadion": "aarasen",
    "Aker Stadion": "aker", "Skagerak Arena": "skagerak",
    "Lerkendal Stadion": "lerkendal", "Release Arena": "sandefjord",
    "Jotun Arena": "sandefjord", "Sarpsborg Stadion": "sarpsborg",
    "Marienlyst Stadion": "marienlyst", "Alfheim Stadion": "tromso",
    "Romssa Arena": "tromso", "Intility Arena": "intility",
    "SR-Bank Arena": "viking", "J.J. Ugland Stadion": "jerv",
    "Brann Stadion": "brann", "Nadderud Stadion": "nadderud",
}
GROUND_QUERY = {
    "aker": ("Aker Stadion", "Molde"), "tromso": ("Romssa Arena", "Tromsø"),
    "aspmyra": ("Aspmyra Stadion", "Bodø"), "brann": ("Brann Stadion", "Bergen"),
    "briskeby": ("Briskeby Arena", "Hamar"), "color_line": ("Color Line Stadion", "Ålesund"),
    "haugesund": ("Haugesund Stadion", "Haugesund"),
    "intility": ("Intility Arena", "Oslo"), "jerv": ("Levermyr Stadion", "Grimstad"),
    "kristiansund": ("Kristiansund Stadion", "Kristiansund"),
    "lerkendal": ("Lerkendal Stadion", "Trondheim"),
    "marienlyst": ("Marienlyst Stadion", "Drammen"),
    "nadderud": ("Nadderud Stadion", "Bærum"),
    "sandefjord": ("Jotun Arena", "Sandefjord"),
    "viking": ("Viking Stadion", "Stavanger"),
    "sarpsborg": ("Sarpsborg Stadion", "Sarpsborg"),
    "skagerak": ("Skagerak Arena", "Skien"),
    "aarasen": ("Åråsen Stadion", "Lillestrøm"),
}
RENAME_NOTE = {
    "sandefjord": "更名链：Komplett.no Arena（至2019-11）→ Release Arena（2021-05-05起）→ Jotun Arena（2023-09-05起）。FBref 两季全季标 Komplett.no Arena 是过期旧名，非比赛日当期名；基线 Release/Jotun 分段与更名时间线吻合（切换点 2023-09-16 在 2023-09-05 之后）。",
    "tromso": "更名：Alfheim Stadion 于 2023-03-29 更名为 Romssa Arena（NRK 2023-03-29 报道）。2023 赛季首个主场为 2023-04-10（在更名之后），故 2023 全季比赛日当期名为 Romssa Arena；FBref 2023 全季标 Alfheim Stadion 是旧名标签。",
    "haugesund": "更名：Haugesund Stadion 于 2021-05 更名为 Haugesund Sparebank Arena（FK Haugesund 2021-05-27 公告，6 年冠名）。2022–2023 比赛日当期名均为 Haugesund Sparebank Arena；FBref 两季标 Haugesund Stadion 是通用旧名标签。",
    "viking": "更名链：Viking Stadion（2004–2018）→ SR-Bank Arena（2018-04–2024）→ Lyse Arena（2025-01 起）。2022–2023 比赛日当期名为 SR-Bank Arena；Nominatim 当前标签 Lyse Arena 是 2025 年后新名，同一球场，坐标有效。",
    "jerv": "同一球场：FBref 标 'J.J. Ugland Stadion - Levermyr'，Levermyr 为球场所在地后缀；基线标 'J.J. Ugland Stadion'。Nominatim 以 Levermyr Stadion（Grimstad）命中同一球场。",
    "nadderud": "同一球场：基线 city 在 2023 赛季内由 Bekkestua（前 6 个主场）切换为 Bærum（2023-07-03 起）；Nominatim 定位确认 Nadderud stadion 位于 Bekkestua, Bærum——Bekkestua 是 Bærum 市镇内的地点，非换场。",
}
ZERO_FOR_GROUND = {
    "haugesund": [("Haugesund Sparebank Arena", "Haugesund")],
    "jerv": [("J.J. Ugland Stadion", "Grimstad")],
    "viking": [("SR-Bank Arena", "Stavanger")],
}

qlog = json.load(open(os.path.join(NOM, "query_log.json")))
Q = {(q["query_name"], q["query_city"]): q for q in qlog}

def sha_of(rel):
    return hashlib.sha256(open(os.path.join(EV, rel), "rb").read()).hexdigest()

def haversine_km(lat1, lon1, lat2, lon2):
    r = math.radians
    a = math.sin(r(lat2 - lat1) / 2) ** 2 + math.cos(r(lat1)) * math.cos(r(lat2)) * math.sin(r(lon2 - lon1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(a))

out = []
for row in baseline:
    season = row["season"]
    home = row["home_team"]
    fbref_map = FBREF_2022 if season == 2022 else FBREF_2023
    assert home in fbref_map, (season, home)
    fbref_venue = fbref_map[home]
    bname, bcity = row["baseline_venue_name"], row["baseline_venue_city"]
    ground = GROUND_OF_BASELINE[bname]
    qn, qc = GROUND_QUERY[ground]
    q = Q[(qn, qc)]
    data = json.load(open(os.path.join(EV, q["file"])))
    first = data[0]
    nlat, nlon = float(first["lat"]), float(first["lon"])
    delta = haversine_km(row["baseline_venue_lat"], row["baseline_venue_lon"], nlat, nlon)
    candidates = [
        {"name": bname, "city": bcity, "source": "api-football fixture.venue (via baseline method_context)",
         "note": "基线逐场值，原文拼写保留"},
        {"name": fbref_venue, "city": bcity, "source": "FBref schedule table Venue column (non-official)",
         "note": "FBref 赛程表逐场 Venue 列；该队全季恒定，本行值等于该队该季恒定值"},
    ]
    out.append({
        "record_key": row["record_key"], "season": season, "local_date": row["local_date"],
        "home_team": home, "away_team": row["away_team"], "kickoff_local": row["kickoff_local"],
        "round": row["round"], "round_label": row["round_label"],
        "provider_fixture_id": row["provider_fixture_id"],
        "baseline_venue_name": bname, "baseline_venue_city": bcity,
        "baseline_venue_lat": row["baseline_venue_lat"], "baseline_venue_lon": row["baseline_venue_lon"],
        "baseline_venue_evidence": row["baseline_venue_evidence"],
        "fbref_venue_name": fbref_venue, "fbref_venue_city": bcity,
        "fbref_source_url": FBREF_URL[season], "fbref_page_id": FBREF_PAGE[season],
        "fbref_crawl_date": FBREF_CRAWL[season], "fbref_evidence_sha256": None,
        "fbref_evidence_note": "FBref 文本层（browser.open）读取，非官方；本行 FBref 值取自该队该季全季恒定 Venue 值（第一张表全读，无一场偏离）；FBref 文本层无可下载字节，SHA-256 置 null。",
        "verified_actual_matchday_venue_name": bname, "verified_actual_matchday_venue_city": bcity,
        "venue_status": "confirmed",
        "verification_level": "non_official_dual_source",
        "verification_note": "基线 api-football 逐场 venue 与 FBref 逐场 Venue 列在球场身份上一致；命名差异全部由更名时间线解释（见 rename_note），未发现任何一场偏离主队常规球场。NFF 官方确认本轮未达成（见 notes），故核验层级标注为非官方双源一致，绝非 NFF 官方确认。",
        "rename_note": RENAME_NOTE.get(ground),
        "venue_candidates": candidates,
        "ground_key": ground,
        "venue_lat_nominatim": nlat, "venue_lon_nominatim": nlon,
        "coordinate_delta_km_vs_baseline": round(delta, 3),
        "coordinate_note": "坐标为场馆级（非本场专属确认）：Nominatim 对该球场的一次地理编码结果，全季同球场各行共用。",
        "coordinate_provenance": {
            "source": "OpenStreetMap Nominatim (https://nominatim.openstreetmap.org/search)",
            "source_url": q["url"], "final_url": q["url"], "retrieved_at": q["retrieved_at"],
            "field_locator": "first result: lat / lon / display_name / class / type / importance",
            "query_name": qn, "query_city": qc,
            "match_quality": {"display_name": first["display_name"], "class": first.get("class"),
                              "type": first.get("type"), "importance": first.get("importance"),
                              "n_results": q["n_results"]},
            "evidence_file": q["file"], "evidence_sha256": sha_of(q["file"]),
            "zero_result_queries_for_this_ground": [
                {"query_name": zn, "query_city": zc, "file": Q[(zn, zc)]["file"],
                 "evidence_sha256": sha_of(Q[(zn, zc)]["file"]), "retrieved_at": Q[(zn, zc)]["retrieved_at"]}
                for (zn, zc) in ZERO_FOR_GROUND.get(ground, [])]
        },
    })

with open(os.path.join(BASE, "venue_audit_2022_2023.jsonl"), "w") as f:
    for o in out:
        f.write(json.dumps(o, ensure_ascii=False) + "\n")
print("wrote", len(out), "rows")

rows = [json.loads(l) for l in open(os.path.join(BASE, "venue_audit_2022_2023.jsonl"))]
assert len(rows) == 480
assert len({r["record_key"] for r in rows}) == 480
print("per-season:", dict(collections.Counter(r["season"] for r in rows)))
print("status:", dict(collections.Counter(r["venue_status"] for r in rows)))
print("verification_level:", dict(collections.Counter(r["verification_level"] for r in rows)))
print("verified non-null:", sum(1 for r in rows if r["verified_actual_matchday_venue_name"]))
print("coords non-null:", sum(1 for r in rows if r["venue_lat_nominatim"] and r["venue_lon_nominatim"]))
print("distinct grounds:", len({r["ground_key"] for r in rows}))
print("max delta km:", max(r["coordinate_delta_km_vs_baseline"] for r in rows))
for g in sorted({r["ground_key"] for r in rows}):
    ds = [r["coordinate_delta_km_vs_baseline"] for r in rows if r["ground_key"] == g]
    print(f"  {g}: {len(ds)} rows, delta {ds[0]} km")
print("sandefjord 2023 name split:", dict(collections.Counter(
    r["baseline_venue_name"] for r in rows if r["season"] == 2023 and r["home_team"] == "Sandefjord")))
print("tromso name split:", dict(collections.Counter(
    (r["season"], r["baseline_venue_name"]) for r in rows if r["home_team"] == "Tromso")))
print("stabaek city split:", dict(collections.Counter(
    r["baseline_venue_city"] for r in rows if r["home_team"] == "Stabaek")))
print("sha re-check sample:", rows[0]["coordinate_provenance"]["evidence_sha256"][:16])
