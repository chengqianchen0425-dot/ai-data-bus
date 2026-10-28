#!/usr/bin/env python3
"""Merge FBref season transcriptions (2016/2017/2018) + club/stadium evidence
into method_context_2016_2018.jsonl. Pre-match facts only; no scores/results."""
import json, os, hashlib
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta

W = os.path.expanduser("~/workspace/ai-inbox/work-req-20261028-002")
EV = os.path.join(W, "evidence")
def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
def g(r, *names):
    for n in names:
        if n in r: return r[n]
    return None
def mtime_iso(path):
    t = os.path.getmtime(path)
    return datetime.fromtimestamp(t, tz=timezone(timedelta(hours=8))).isoformat()

WIKI_SHA = {2016: "f9813cf559773cda1665cc7177c625d22b4a024f7e6783a9b44c691b326f7025",
            2017: "462e60e9942bf04d03fe1053bee703c3d7fa2c630146221b29512c93abf63efa",
            2018: "95a918bde0b5069ae0e302605ae3e91c1f5f79b8802620822f5f8ecedc945970"}
WIKI_URL = {y: f"https://en.wikipedia.org/wiki/{y}_Veikkausliiga" for y in (2016, 2017, 2018)}
FBREF_URL = {y: f"https://fbref.com/en/comps/43/{y}/schedule/{y}-Veikkausliiga-Scores-and-Fixtures" for y in (2016, 2017, 2018)}

CLUB_ART = json.load(open(os.path.join(EV, "club_articles.json")))
STAD_EVID = json.load(open(os.path.join(EV, "stadium_coords_evidence.json")))

# FBref label -> club identity
CLUBS = {
 "HJK Helsinki": dict(canonical="Helsingin Jalkapalloklubi (HJK)", founded=1907, detail="19 June 1907",
    lineage=None, art="HJK"),
 "Helsinki IFK": dict(canonical="HIFK Fotboll (HIFK)", founded=1897, detail="1897 (infobox)",
    lineage="Helsingin IFK football section; shares Helsinki's Sonera Stadium / Telia 5G -areena with HJK in these seasons.",
    art="HIFK"),
 "IFK Mariehamn": dict(canonical="IFK Mariehamn", founded=1919, detail="1919 (infobox)", lineage=None, art="IFK Mariehamn"),
 "Ilves": dict(canonical="FC Ilves", founded=1931, detail="1931 (infobox)", lineage=None, art="Ilves"),
 "Inter Turku": dict(canonical="FC Inter Turku", founded=1990, detail="1990 (infobox)", lineage=None, art="FC Inter Turku"),
 "Kemi Kings": dict(canonical="Palloseura Kemi Kings (PS Kemi)", founded=1999, detail="Established 21 October 1999",
    lineage=("Merger of Kemin Palloseura (KePS), Kemin Pallotoverit-85 (KPT-85) and Visan Pallo. "
             "TRAP AVOIDED: the Wikipedia title 'Palloseura Kemi Kings' redirects to 'Kemin Palloseura', whose infobox "
             "figure 1932 belongs to KePS, not to the Veikkausliiga club; 1932 must not be used for this club. "
             "Parent company ceased operations Feb 2019; successor Kemi City FC formed early 2019, reverted to PS Kemi name Feb 2022 (post-period lineage)."),
    art="PS Kemi"),
 "KuPS": dict(canonical="Kuopion Palloseura (KuPS)", founded=1923, detail="1923 (infobox)", lineage=None, art="KuPS"),
 "Lahti": dict(canonical="FC Lahti", founded=1996, detail="1996 (infobox)", lineage=None, art="FC Lahti"),
 "PK–35": dict(canonical="PK-35 Vantaa (men)", founded=2008,
    detail="as PK-35 Vantaa 2008 (lineage: as Viipurin Pallokerho 1935; as Pallokerho-35 1948)",
    lineage=("Dissolved 2016. DISTINCT CLUB: the surviving Helsinki PK-35 (men) is a different club; the 2016 Veikkausliiga "
             "participant is the Vantaa club. The Wikipedia title 'PK-35' is only a disambiguation page."),
    art="PK-35 Vantaa"),
 "RoPS": dict(canonical="Rovaniemen Palloseura (RoPS)", founded=1950, detail="1950 (infobox)", lineage=None, art="RoPS"),
 "SJK": dict(canonical="Seinäjoen Jalkapallokerho (SJK)", founded=2007, detail="5 November 2007 (infobox; merger-era club)",
    lineage=None, art="SJK"),
 "VPS": dict(canonical="Vaasan Palloseura (VPS)", founded=1924, detail="1924 (infobox)", lineage=None, art="VPS"),
 "JJK": dict(canonical="Jyväskylän Jalkapalloklubi (JJK)", founded=None, detail="Founded 2000 (1992) (infobox verbatim; parenthetical not interpreted)",
    lineage="Infobox figure is ambiguous (2000 vs 1992); no single founded year asserted.", art="JJK"),
 "FC Honka": dict(canonical="FC Honka", founded=1957, detail="1957 (infobox)", lineage=None, art="FC Honka"),
 "TPS": dict(canonical="Turun Palloseura (TPS)", founded=1922, detail="1922 (infobox)", lineage=None, art="TPS"),
}

# season listed homes (Wikipedia season page Teams section; candidate only, NOT match-level confirmation)
LISTED_HOME = {
 2016: {"Inter Turku": "Veritas Stadion", "Lahti": "Lahden kisapuisto", "Helsinki IFK": "Sonera Stadium",
        "HJK Helsinki": "Sonera Stadium", "IFK Mariehamn": "Wiklöf Holding Arena", "Ilves": "Tammelan Stadion",
        "KuPS": "Savon Sanomat Areena", "PK–35": "Myyrmäen jalkapallostadion",
        "Kemi Kings": "Sauvosaaren Urheilupuisto", "RoPS": "Rovaniemen keskuskenttä", "SJK": "OmaSP Stadion",
        "VPS": "Hietalahti Stadium"},
 2017: {"Inter Turku": "Veritas Stadion", "Lahti": "Lahden Stadion", "Helsinki IFK": "Telia 5G -areena",
        "HJK Helsinki": "Telia 5G -areena", "IFK Mariehamn": "Wiklöf Holding Arena", "Ilves": "Tammelan Stadion",
        "KuPS": "Savon Sanomat Areena", "JJK": "Harjun stadion",
        "Kemi Kings": "Sauvosaaren Urheilupuisto", "RoPS": "Rovaniemen keskuskenttä", "SJK": "OmaSP Stadion",
        "VPS": "Elisa Stadion"},
 2018: {"FC Honka": "Tapiolan Urheilupuisto", "Inter Turku": "Veritas Stadion", "Lahti": "Lahden Stadion",
        "HJK Helsinki": "Telia 5G -areena", "IFK Mariehamn": "Wiklöf Holding Arena", "Ilves": "Tammelan Stadion",
        "KuPS": "Savon Sanomat Areena", "Kemi Kings": "Sauvosaaren Urheilupuisto",
        "RoPS": "Rovaniemen keskuskenttä", "SJK": "OmaSP Stadion", "TPS": "Veritas Stadion", "VPS": "Elisa Stadion"},
}

# FBref venue -> (canonical, city, lat, lon, tz, basis, coords_evidence_key or None, identity_note)
VENUES = {
 "Telia 5G -areena": ("Töölö Football Stadium (Bolt Arena)", "Helsinki", 60.1875, 24.9225, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Bolt Arena' (redirects to Töölö Football Stadium)", "Bolt Arena", None),
 "Veritas Stadion": ("Kupittaa Football Stadium (Veritas Stadion)", "Turku", 60.44277778, 22.29166667, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Veritas Stadion' (redirects to Kupittaa Football Stadium)", "Veritas Stadion", None),
 "Wiklöf Holding Arena": ("Wiklöf Holding Arena", "Mariehamn", 60.10222222, 19.93527778, "Europe/Mariehamn",
    "en.wikipedia API coordinates for 'Wiklöf Holding Arena'", "Wiklöf Holding Arena", None),
 "Wiklöf Holding Arena konstgräs": ("Wiklöf Holding Arena (complex; konstgräs = artificial-turf pitch)", "Mariehamn",
    60.10222222, 19.93527778, "Europe/Mariehamn",
    "Complex-level coordinates from Wiklöf Holding Arena article; pitch-level coordinates not separately sourced",
    "Wiklöf Holding Arena", "Pitch-level identity unresolved; coordinates are complex-level, not pitch-level."),
 "Tammelan Stadion": ("Tammela Stadium", "Tampere", 61.5003, 23.7853, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Tammela Stadium' (from 'Tammelan Stadion')", "Tammela Stadium", None),
 "Ratinan Stadion": ("Tampere Stadium (Ratina Stadium)", "Tampere", 61.4925, 23.76416667, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Ratina Stadium' (redirects to Tampere Stadium)", "Ratina Stadium", None),
 "Savon Sanomat Areena": ("Kuopio Football Stadium (Savon Sanomat Areena)", "Kuopio", 62.88463, 27.6718, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Kuopio Football Stadium'", "Kuopio Football Stadium", None),
 "Väinölänniemen stadion": ("Väinölänniemen stadion", "Kuopio", 62.88277778, 27.70055556, "Europe/Helsinki",
    "fi.wikipedia API coordinates for 'Väinölänniemen stadion'", "fi:Väinölänniemen stadion", None),
 "Myyrmäen jalkapallostadion": ("Myyrmäen jalkapallostadion", "Vantaa", 60.2621, 24.83818333, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Myyrmäen jalkapallostadion'", "Myyrmäen jalkapallostadion", None),
 "Rovaniemen Keskuskenttä": ("Rovaniemen keskuskenttä", "Rovaniemi", 66.5, 25.72166667, "Europe/Helsinki",
    "fi.wikipedia API coordinates for 'Rovaniemen keskuskenttä'", "fi:Rovaniemen keskuskenttä", None),
 "Raatin stadion": ("Raatti Stadium", "Oulu", 65.01972222, 25.46583333, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Raatti Stadium'", "Raatti Stadium", None),
 "Sauvosaaren urheilupuisto": ("Sauvosaaren urheilupuisto", "Kemi", 65.72972222, 24.56055556, "Europe/Helsinki",
    "fi.wikipedia API coordinates for 'Sauvosaaren urheilupuisto' (en article gives 65.729778, 24.560583; consistent)",
    "fi:Sauvosaaren urheilupuisto", None),
 "Sauvosaaren Takakenttä N": ("Sauvosaaren Takakenttä N (back field, Sauvosaari complex)", "Kemi", None, None,
    "Europe/Helsinki", "City from Sauvosaari complex (Kemi) + PS Kemi home city; no dedicated article/coordinates found",
    None, "Back field within the Sauvosaari complex; pitch-level coordinates not sourced; city is complex-level."),
 "Kisapuisto": ("Kisapuisto (Lahti sports park)", "Lahti", None, None, "Europe/Helsinki",
    "City from home club (FC Lahti) + park name; no dedicated Lahti-Kisapuisto article/coordinates found",
    None, ("HOMONYM REJECTED: the en.wikipedia 'Kisapuisto' article with coordinates (61.0577, 28.2288) is in "
           "Lappeenranta, not Lahti, and was NOT used. Lahti Stadium (60.9830, 25.6341) sits in/near the Kisapuisto park, "
           "but an alias between 'Kisapuisto' and 'Lahden Stadion' is not confirmed by a stadium article, so the two "
           "names are kept as separate candidates and no coordinates are asserted for Kisapuisto.")),
 "Lahden Stadion": ("Lahti Stadium", "Lahti", 60.98305556, 25.63416667, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Lahti Stadium'", "Lahti Stadium", None),
 "Kaarlen kenttä": ("Kaarlen kenttä", "Vaasa", 63.08277778, 21.64111111, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Kaarlen kenttä'", "Kaarlen kenttä", None),
 "Elisa Stadion": ("Hietalahti Stadium (Elisa Stadion)", "Vaasa", 63.08527778, 21.62777778, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Elisa Stadion' (redirects to Hietalahti Stadium); rename confirmed by redirect",
    "Hietalahti Stadium", None),
 "Jouppilanvuoren tekonurmi": ("Jouppilanvuoren tekonurmi", "Seinäjoki", 62.78, 22.81194444, "Europe/Helsinki",
    "fi.wikipedia API coordinates for 'Jouppilanvuoren tekonurmi'", "fi:Jouppilanvuoren tekonurmi", None),
 "Seinäjoen keskuskenttä": ("Seinäjoen keskuskenttä", "Seinäjoki", 62.78194444, 22.85111111, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Seinäjoen keskuskenttä'", "Seinäjoen keskuskenttä", None),
 "OmaSP Stadion": ("OmaSP Stadion", "Seinäjoki", 62.77861, 22.81472, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'OmaSP Stadion'", "OmaSP Stadion", None),
 "Harjun stadion": ("Harjun stadion", "Jyväskylä", 62.24472222, 25.74083333, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Harjun stadion'", "Harjun stadion", None),
 "Vaajakosken urheilukenttä": ("Vaajakosken urheilukenttä", "Jyväskylä", None, None, "Europe/Helsinki",
    "City from home club (JJK, Jyväskylä); Vaajakoski is a district of Jyväskylä; no dedicated article/coordinates found",
    None, "District-field identity unresolved; coordinates not asserted."),
 "Tapiolan Urheilupuisto": ("Tapiolan urheilupuisto", "Espoo", 60.1791, 24.7813, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Tapiolan urheilupuisto'", "Tapiolan urheilupuisto", None),
 "Paavo Nurmi Stadion": ("Paavo Nurmi Stadium", "Turku", 60.4425, 22.26083333, "Europe/Helsinki",
    "en.wikipedia API coordinates for 'Paavo Nurmi Stadium'", "Paavo Nurmi Stadium", None),
 "City Sport Areena": ("City Sport Areena", "Kemi", None, None, "Europe/Helsinki",
    "City from Merilappi United ground listing 'City Sport Areena, Kemi' and SoccerPunter venue label 'City Sport Areena (Kemi)' for the exact 2017 PS Kemi vs SJK match; no coordinates source found",
    None, "Venue identity (which Kemi facility) and coordinates unresolved; city only."),
}

# canonical equivalence groups for moved detection (same physical venue, different names)
EQUIV = [
 # Only rename equivalences confirmed by a redirect/article: Sonera -> Telia 5G -areena -> Bolt Arena (same Helsinki stadium);
 # Hietalahti Stadium -> Elisa Stadion (same Vaasa stadium). Same-complex pairs (Sauvosaari back field, Wiklöf konstgräs,
 # Lahti Kisapuisto/Lahden Stadion) are deliberately NOT equivalenced: alias unconfirmed by a stadium article.
 {"Töölö Football Stadium (Bolt Arena)", "Sonera Stadium", "Telia 5G -areena"},
 {"Hietalahti Stadium (Elisa Stadion)", "Hietalahti Stadium", "Elisa Stadion"},
]
def canon_key(name):
    for grp in EQUIV:
        if name in grp: return frozenset(grp)
    return frozenset([name])
LISTED_CANON = {
 "Veritas Stadion": "Kupittaa Football Stadium (Veritas Stadion)",
 "Lahden kisapuisto": "Lahden kisapuisto",
 "Sonera Stadium": "Töölö Football Stadium (Bolt Arena)",
 "Wiklöf Holding Arena": "Wiklöf Holding Arena",
 "Tammelan Stadion": "Tammela Stadium",
 "Savon Sanomat Areena": "Kuopio Football Stadium (Savon Sanomat Areena)",
 "Myyrmäen jalkapallostadion": "Myyrmäen jalkapallostadion",
 "Sauvosaaren Urheilupuisto": "Sauvosaaren urheilupuisto",
 "Rovaniemen keskuskenttä": "Rovaniemen keskuskenttä",
 "OmaSP Stadion": "OmaSP Stadion",
 "Hietalahti Stadium": "Hietalahti Stadium (Elisa Stadion)",
 "Lahden Stadion": "Lahti Stadium",
 "Telia 5G -areena": "Töölö Football Stadium (Bolt Arena)",
 "Harjun stadion": "Harjun stadion",
 "Elisa Stadion": "Hietalahti Stadium (Elisa Stadion)",
 "Tapiolan Urheilupuisto": "Tapiolan urheilupuisto",
}

# season entry (promotion into that season)
def season_entry(label, y):
    if y == 2016 and label == "Kemi Kings":
        return {"type": "promoted_champions", "entry_season": 2016,
                "note": "Ykkönen champions 2015, promoted into Veikkausliiga 2016 (Wikipedia 2016 season page, Teams section)."}
    if y == 2017 and label == "JJK":
        return {"type": "promoted_champions", "entry_season": 2017,
                "note": "Ykkönen champions 2016, promoted into Veikkausliiga 2017 (Wikipedia 2017 season page, Teams section)."}
    if y == 2018 and label == "TPS":
        return {"type": "promoted_champions", "entry_season": 2018,
                "note": "Ykkönen champions 2017, promoted into Veikkausliiga 2018 (Wikipedia 2018 season page, Teams section)."}
    if y == 2018 and label == "FC Honka":
        return {"type": "promoted_playoff", "entry_season": 2018,
                "note": "Beat 11th-placed HIFK in the promotion/relegation playoff to take the 2018 Veikkausliiga place (Wikipedia 2018 season page, Teams section)."}
    return {"type": "continuing", "entry_season": None,
            "note": "Continuing Veikkausliiga member for this season; first top-flight entry year not established from the sources used."}

# agent anomaly lists (keyed by season+date+home+away; same pair meets 3x/season so pair-only keys would over-flag)
ANOM = {
 (2016, "2016-04-02", "HJK Helsinki", "IFK Mariehamn"): "Wk 33 on the season's first day; no Wk 1 precedes it.",
 (2016, "2016-04-02", "PK\u201335", "RoPS"): "Wk 33 on the season's first day.",
 (2016, "2016-07-02", "Ilves", "SJK"): "Wk 33 dated 2016-07-02, between Wk 14/16 blocks.",
 (2016, "2016-07-03", "Lahti", "KuPS"): "Wk 33 dated 2016-07-03, between Wk 14/16 blocks.",
 (2016, "2016-07-03", "Kemi Kings", "Helsinki IFK"): "Wk 33 dated 2016-07-03, between Wk 14/16 blocks.",
 (2016, "2016-07-04", "Inter Turku", "VPS"): "Wk 33 dated 2016-07-04, between Wk 14/16 blocks.",
 (2016, "2016-06-23", "Kemi Kings", "RoPS"): "Wk 10 row appears after the Wk 14 block (rescheduled/early-match presentation).",
 (2016, "2016-06-28", "VPS", "Ilves"): "Wk 2 row appears after the Wk 14 block.",
 (2016, "2016-06-28", "Inter Turku", "SJK"): "Wk 16 row appears before the Wk 15 block.",
 (2016, "2016-06-29", "Lahti", "Kemi Kings"): "Wk 2 row appears after the Wk 14 block.",
 (2016, "2016-07-13", "VPS", "PK\u201335"): "Wk 14 row appears after the Wk 15 block.",
 (2016, "2016-08-24", "Ilves", "RoPS"): "Wk 3 row appears after the Wk 22 block.",
 (2016, "2016-08-24", "HJK Helsinki", "PK\u201335"): "Wk 28 row appears before the Wk 23 block.",
 (2017, "2017-04-30", "IFK Mariehamn", "VPS"): "Only Wk 5 row dated 2017-04-30; other Wk 5 rows 2017-05-06.",
 (2017, "2017-05-06", "JJK", "Inter Turku"): "Only Wk 6 row dated 2017-05-06; other Wk 6 rows 2017-05-11/12.",
 (2017, "2017-05-06", "Helsinki IFK", "RoPS"): "Presented after the Wk 6 first row (same day).",
 (2017, "2017-05-12", "SJK", "JJK"): "Only Wk 7 row dated 2017-05-12; other Wk 7 rows 2017-05-19.",
 (2017, "2017-05-19", "SJK", "RoPS"): "Only Wk 8 row dated 2017-05-19; other Wk 8 rows 2017-05-23/24.",
 (2017, "2017-05-24", "KuPS", "SJK"): "Only Wk 9 row dated 2017-05-24; other Wk 9 rows 2017-05-27.",
 (2017, "2017-05-27", "SJK", "IFK Mariehamn"): "Only Wk 10 row dated 2017-05-27; other Wk 10 rows 2017-05-31.",
 (2017, "2017-05-31", "Inter Turku", "Lahti"): "Only Wk 11 row dated 2017-05-31; other Wk 11 rows 2017-06-03/04.",
 (2017, "2017-06-04", "KuPS", "IFK Mariehamn"): "Only Wk 12 row dated 2017-06-04; other Wk 12 rows 2017-06-14/15/16.",
 (2017, "2017-06-21", "Inter Turku", "KuPS"): "Wk 13 tail row on the same day as the Wk 14 first row (2017-06-21).",
 (2017, "2017-06-26", "RoPS", "Ilves"): "Wk 14 tail row on the same day as the Wk 15 first row (2017-06-26).",
 (2017, "2017-07-08", "Inter Turku", "JJK"): "Only Wk 17 row dated 2017-07-08; other Wk 17 rows 2017-07-16/17.",
 (2018, "2018-05-29", "HJK Helsinki", "SJK"): "Wk 8 row dated 2018-05-29, presented after Wk 11, before Wk 12.",
 (2018, "2018-08-29", "Ilves", "IFK Mariehamn"): "Wk 3 row dated 2018-08-29, presented after Wk 25, before Wk 26 (about 4 months late).",
 (2018, "2018-09-26", "Inter Turku", "Lahti"): "Wk 8 row dated 2018-09-26, presented after Wk 29, before Wk 30.",
 (2018, "2018-09-26", "Ilves", "HJK Helsinki"): "Wk 23 row dated 2018-09-26, presented after the Wk 8 row above, before Wk 30.",
}

OUT = []
stats = {}
for y in (2016, 2017, 2018):
    rows = load_jsonl(os.path.join(W, f"fbref_{y}_schedule_rows.jsonl"))
    # Wk-team duplication weeks (computed)
    bywk = defaultdict(list)
    for r in rows:
        w = g(r, "Wk", "wk"); bywk[w].append(r["home_team"]); bywk[w].append(r["away_team"])
    dup_wk = {}
    for w, ts in bywk.items():
        for t, n in Counter(ts).items():
            if n != 1: dup_wk.setdefault(w, []).append((t, n))
    c = Counter()
    for r in rows:
        wk = g(r, "Wk", "wk"); home, away = r["home_team"], r["away_team"]
        fk = f"{y}|{r['match_date']}|{home}|{away}"
        hc, ac = CLUBS[home], CLUBS[away]
        listed = LISTED_HOME[y].get(home)
        listed_canon = LISTED_CANON.get(listed) if listed else None
        vn = r["venue_name_fbref"]
        vcanon, vcity, vlat, vlon, vtz, vbasis, vevid, vnote = VENUES[vn]
        vnotes = []
        if canon_key(vcanon) == canon_key(listed_canon):
            vstatus = "confirmed"
        elif vcanon in ("Kisapuisto (Lahti sports park)", "Sauvosaaren Takakenttä N (back field, Sauvosaari complex)",
                        "Wiklöf Holding Arena (complex; konstgräs = artificial-turf pitch)"):
            vstatus = "neutral"
        elif home == "Lahti" and listed == "Lahden kisapuisto" and vn == "Lahden Stadion":
            # 2016 listed home 'Lahden kisapuisto' vs match venue 'Lahden Stadion': same Kisapuisto area, alias unconfirmed
            vstatus = "neutral"
            vnotes.append("Listed home 'Lahden kisapuisto' and match venue 'Lahden Stadion' both refer to the Kisapuisto area; stadium-article confirmation of the alias is absent, so neither 'confirmed' nor 'moved' is asserted.")
        else:
            vstatus = "moved"
        if vnote: vnotes.append(vnote)
        if vstatus == "moved":
            vnotes.append(f"Match-level venue differs from the club's season listed home ({listed}); listed home is a candidate only, not match-level confirmation.")
        if home == "Helsinki IFK" and vn == "Veritas Stadion" or (home == "Inter Turku" and vn == "Myyrmäen jalkapallostadion") or (home == "PK–35" and vn == "Telia 5G -areena"):
            vnotes.append("Cross-city printed venue on 2016-08-26/27 (flagged by the 2016 transcription agent); reason (neutral event vs source error) unverified — kept as printed.")
        # round conflict
        rnotes = []
        if (y, r["match_date"], home, away) in ANOM: rnotes.append("Date-order/presentation anomaly: " + ANOM[(y, r["match_date"], home, away)])
        if wk in dup_wk:
            rnotes.append(f"Wk {wk} group is not a proper 12-team round in FBref data: duplicated team(s) "
                          + ", ".join(f"{t}×{n}" for t, n in sorted(dup_wk[wk])) + ".")
        rconflict = bool(rnotes)
        if rconflict: status = "conflict"
        elif vstatus == "neutral" or vlat is None: status = "partial"
        else: status = "complete"
        c[status] += 1; c["discovered"] += 1
        if vstatus == "confirmed": c["venue_confirmed"] += 1
        elif vstatus == "moved": c["venue_moved"] += 1
        elif vstatus == "neutral": c["venue_neutral"] += 1
        if rconflict: c["round_conflict_rows"] += 1
        # provenance
        def club_prov(key, club):
            a = CLUB_ART[key]
            return {"source_name": "Wikipedia (English)", "source_url": "https://en.wikipedia.org/wiki/" + a["resolved_title"].replace(" ", "_").replace("-> REDIRECTS to ", ""),
                    "evidence_file": a["file"], "source_sha256": a["sha256"],
                    "field_locator": "Infobox Founded + article history/lineage text",
                    "retrieved_at": mtime_iso(os.path.join(EV, a["file"]))}
        hprov = club_prov(hc["art"], hc)
        if home == "Kemi Kings":
            hprov["conflict_trap_file"] = {"file": "club_PSKemiKings.html",
                "sha256": "5c83affa264fb7e9aacaeed2b352f7d09c62f1ca45eed08586ae4e49bdb19fda",
                "note": "Redirect target 'Kemin Palloseura' infobox (1932) belongs to predecessor KePS, not this club."}
            hprov["evidence_file"] = "club_KemiCityFC.html"
            hprov["source_sha256"] = "e2733296abea83575999546245bdc1c319744c368e16fb3db0f8da09357cfb7f"
            hprov["source_url"] = "https://en.wikipedia.org/wiki/Kemi_City_F.C."
            hprov["field_locator"] = "PS Kemi Kings infobox (Founded 1999) + History text (established 21 October 1999 by merger)"
            hprov["retrieved_at"] = mtime_iso(os.path.join(EV, "club_KemiCityFC.html"))
        aprob = club_prov(ac["art"], ac)
        if away == "Kemi Kings":
            aprob = dict(hprov)
        sev = STAD_EVID.get(vevid) if vevid else None
        stad_prov = {"source_name": "Wikipedia API (coordinates)", "source_url": None,
                     "evidence_file": sev["file"] if sev else None, "source_sha256": sev["sha256"] if sev else None,
                     "field_locator": "prop=coordinates response for the resolved article title",
                     "basis": vbasis,
                     "retrieved_at": mtime_iso(os.path.join(EV, sev["file"])) if sev else None}
        if vevid and vevid.startswith("fi:"):
            stad_prov["source_name"] = "Wikipedia API, Finnish edition (coordinates)"
        OUT.append({
            "fixture_key": fk, "season": y, "match_date": r["match_date"], "match_day": g(r, "Day", "day"),
            "official_round": r["official_round"], "official_round_wk": wk,
            "round_label_conflict": rconflict, "round_conflict_notes": rnotes,
            "home_team_fbref": home, "away_team_fbref": away,
            "home_club": {"canonical_name": hc["canonical"], "founded_year": hc["founded"],
                          "founded_detail": hc["detail"], "lineage_note": hc["lineage"],
                          "season_entry": season_entry(home, y)},
            "away_club": {"canonical_name": ac["canonical"], "founded_year": ac["founded"],
                          "founded_detail": ac["detail"], "lineage_note": ac["lineage"],
                          "season_entry": season_entry(away, y)},
            "kickoff_local": r["kickoff_local"],
            "kickoff_local_semantics": ("FBref Time column, first token only. FBref publishes no timezone name or UTC offset "
                "for this column, so no timezone is asserted and no UTC conversion is generated. In the 2016 crawl the Time "
                "cell rendered as 'HH:MM (HH:MM)'; the parenthetical second value is a viewer-timezone conversion, not a source field, and is not recorded."),
            "kickoff_timezone": None, "kickoff_utc": None,
            "meeting_number": None,
            "meeting_number_reason": ("no authoritative source defines meeting_number; deriving it from date order, CSV order, "
                "team appearance counts, scores, standings or odds is forbidden by the task"),
            "venue": {"venue_name_fbref": vn, "venue_canonical": vcanon, "venue_city": vcity,
                      "venue_lat": vlat, "venue_lon": vlon, "venue_tz": vtz, "venue_status": vstatus,
                      "venue_status_notes": vnotes,
                      "home_club_season_listed_home": listed,
                      "venue_candidates": [listed] if listed else []},
            "row_status": status,
            "csv_join_status": "csv_unavailable_on_this_vm_derived_from_public_schedule",
            "provenance": {
                "fixture": {"source_name": "FBref", "source_url": FBREF_URL[y], "final_url": FBREF_URL[y],
                    "retrieved_at": r["retrieved_at"],
                    "field_locator": "FBref Scores & Fixtures table, columns Wk|Day|Date|Time|Home|Away|Venue",
                    "source_sha256": None,
                    "source_sha256_note": ("browser text layer only; direct download blocked by Cloudflare (HTTP 403 challenge); "
                        "no source bytes captured, hash must not be fabricated")},
                "season_format": {"source_name": "Wikipedia (English)", "source_url": WIKI_URL[y], "final_url": WIKI_URL[y],
                    "evidence_file": f"wiki_{y}.html", "source_sha256": WIKI_SHA[y],
                    "field_locator": "Results section headings 'Matches 1–22' and 'Matches 23–33'; Teams section (promotion/relegation + listed homes)",
                    "retrieved_at": mtime_iso(os.path.join(EV, f"wiki_{y}.html"))},
                "club_home": hprov, "club_away": aprob, "stadium": stad_prov},
        })
    stats[y] = dict(c)
    stats[y]["expected"] = 198
    stats[y]["missing"] = 198 - c["discovered"]
    stats[y]["unavailable"] = 0; stats[y]["blocked"] = 0

OUT.sort(key=lambda r: (r["season"], r["match_date"], r["home_team_fbref"], r["away_team_fbref"]))
with open(os.path.join(W, "method_context_2016_2018.jsonl"), "w", encoding="utf-8") as f:
    for r in OUT:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("rows:", len(OUT))
for y in (2016, 2017, 2018):
    s = stats[y]
    print(y, {k: s.get(k, 0) for k in ["expected", "discovered", "complete", "partial", "conflict", "unavailable", "blocked", "missing", "venue_confirmed", "venue_moved", "venue_neutral", "round_conflict_rows"]})
json.dump(stats, open(os.path.join(W, "merge_stats.json"), "w"), indent=2)
# venue usage counts
vc = Counter((r["venue"]["venue_name_fbref"], r["venue"]["venue_status"]) for r in OUT)
for k in sorted(vc): print(k, vc[k])
