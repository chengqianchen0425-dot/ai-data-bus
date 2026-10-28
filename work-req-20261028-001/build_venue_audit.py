"""Build venue_audit_2024_2025.jsonl + notes.md for req-20261028-001 (D route).

Inputs (all in /tmp, none containing scores/results - the NFF Resultat column was
dropped at parse time and never stored):
  /tmp/d_subset.json        - baseline linkage + baseline venue, verbatim
  /tmp/nff_matched.json     - NFF official Bane per matched fixture
  evidence/geocode_*.json   - Nominatim JSON bytes per venue site
Rules (documented in notes.md):
  - verified venue name = NFF Bane verbatim (official, match-specific).
  - verified venue city = baseline venue_city verbatim for that match (NFF Bane
    column carries no city); city provenance is labelled as baseline, not NFF.
  - confirmed: NFF Bane site == baseline venue site.
  - neutral: verified site != home club season-regular Bane AND != away club
    season-regular Bane (the 4 off-regular-ground matches, all 2024).
  - moved: reserved for verified site == away club regular Bane; none observed.
  - conflict: reserved for NFF vs baseline SITE disagreement; none observed.
    FBref disagreements/variants are preserved as candidates/notes (FBref is
    non-official tier) and do not by themselves flip a row to conflict when
    NFF + baseline agree.
  - same-site naming variants (sponsor/renames/punctuation/pitch granularity
    within one complex) are NOT different venues and NOT conflicts.
"""
import json, collections, hashlib, os, re
from datetime import datetime, timezone, timedelta

WORK = '/home/hatch/workspace/ai-inbox/work-req-20261028-001'
EVID = os.path.join(WORK, 'evidence')
CST = timezone(timedelta(hours=8))

base = json.load(open('/tmp/d_subset.json'))
matched = json.load(open('/tmp/nff_matched.json'))
mmap = {(m['season'], m['round'], m['home'], m['away'], m['local_date']): m for m in matched}
assert len(mmap) == 480, len(mmap)

# season-regular NFF Bane per club (mode)
mode = {}
for season in (2024, 2025):
    cnt = collections.defaultdict(collections.Counter)
    for m in matched:
        if m['season'] == season:
            cnt[m['home']][m['nff_bane']] += 1
    for club, c in cnt.items():
        mode[(season, club)] = c.most_common(1)[0][0]

# NFF Bane -> site key (for coordinates)
SITE = {
    'Aker stadion': 'aker_stadion', 'Aspmyra stadion': 'aspmyra_stadion',
    'Brann stadion': 'brann_stadion', 'Briskeby': 'briskeby',
    'Bryne stadion': 'bryne_stadion', 'Fredrikstad stadion': 'fredrikstad_stadion',
    'Haugesund Sparebank Arena': 'haugesund_sparebank_arena',
    'Intility Arena': 'intility_arena', 'Jotun Arena': 'jotun_arena',
    'KFUM-Arena': 'kfum_arena', 'Nordmøre stadion': 'nordmore_stadion',
    'Lerkendal stadion': 'lerkendal_stadion', 'Lyse Arena': 'lyse_arena',
    'Marienlyst stadion': 'marienlyst_stadion', 'Romssa Arena': 'romssa_arena',
    'Sarpsborg st KG': 'sarpsborg_stadion', 'Skagerak Arena': 'skagerak_arena',
    'Åråsen stadion': 'arasen_stadion',
}
# baseline venue -> site key (same sites, provider spellings)
BSITE = {
    'Aker Stadion': 'aker_stadion', 'Aspmyra Stadion': 'aspmyra_stadion',
    'Brann Stadion': 'brann_stadion', 'Briskeby Arena': 'briskeby',
    'Bryne Stadion': 'bryne_stadion', 'Fredrikstad Stadion': 'fredrikstad_stadion',
    'Nye Fredrikstad Stadion': 'fredrikstad_stadion',
    'Haugesund Stadion': 'haugesund_sparebank_arena',
    'Haugesund Sparebank Arena': 'haugesund_sparebank_arena',
    'Intility Arena': 'intility_arena', 'Jotun Arena': 'jotun_arena',
    'KFUM Arena': 'kfum_arena', 'Kristiansund Stadion': 'nordmore_stadion',
    'Nordmøre stadion': 'nordmore_stadion', 'Lerkendal Stadion': 'lerkendal_stadion',
    'Lyse Arena': 'lyse_arena', 'SR-Bank Arena': 'lyse_arena',
    'Marienlyst Stadion': 'marienlyst_stadion', 'Romssa Arena': 'romssa_arena',
    'Sarpsborg Stadion': 'sarpsborg_stadion', 'Skagerak Arena': 'skagerak_arena',
    'Åråsen Stadion': 'arasen_stadion',
}
NFF_SHA = {2024: 'a7d381958bb42ca41dbf1f9f2a41ed2fa8a76d8d9cd9813c70c83d4c6dcc9034',
            2025: '03912ab721df60be95709ba9fccac95a923ae80c318341908a3a216144'}
NFF_URL = {2024: 'https://www.fotball.no/footballapi/Calendar/DownloadTournamentExcelCalendar?tournamentId=192924&heading=Eliteserien',
            2025: 'https://www.fotball.no/footballapi/Calendar/DownloadTournamentExcelCalendar?tournamentId=199603&heading=Eliteserien'}
NFF_TID = {2024: 192924, 2025: 199603}
NFF_RETRIEVED = {2024: '2026-10-28T15:59:10+08:00', 2025: '2026-10-28T15:59:11+08:00'}
# baseline provenance: per-season api-football response hash, copied from baseline file
BASE_SHA = {}
for r in json.load(open('/tmp/d_subset.json')):
    pass
# read baseline file directly for provenance hashes
import itertools
def iter_baseline():
    with open('/home/hatch/workspace/ai-inbox/repo/work-req-20261017-002/fixtures_2018_2025.jsonl') as f:
        for line in f:
            yield json.loads(line)
for r in iter_baseline():
    if r['season'] in (2024, 2025):
        BASE_SHA[r['season']] = r['provenance']['source_sha256']
print('baseline season hashes:', BASE_SHA)

# Coordinates, two honest provenances:
# (a) Sibling-route Nominatim JSONs already captured in this request's shared
#     work dir (evidence/nominatim/) on 2026-10-28. This route did NOT make new
#     Nominatim requests: its own Nominatim fetch was stopped by a pending
#     user-approval gate for sharing with openstreetmap.org, and that gate must
#     not be bypassed. For each reused file this route re-read the bytes,
#     re-picked the stadium-type result, and re-computed the SHA-256 itself;
#     retrieved_at is the file mtime (the sibling capture time), not this
#     route's fetch time. Sponsor-name queries (Haugesund Sparebank Arena,
#     SR-Bank Arena) returned empty in the sibling capture, so the canonical
#     stadium names in the same complex are used instead (noted per site).
# (b) map.geocode tool results for the 3 sites with no sibling file (Bryne,
#     Fredrikstad, KFUM Arena). Tool results carry no downloadable bytes, so
#     source_sha256 is null with that reason stated, never fabricated.
NOM_DIR = os.path.join(EVID, 'nominatim')
SIBLING = {
    'aker_stadion': 'aker_stadion.json', 'aspmyra_stadion': 'aspmyra_stadion.json',
    'brann_stadion': 'brann_stadion.json', 'briskeby': 'Briskeby_Arena_Hamar.json',
    'haugesund_sparebank_arena': 'haugesund_stadion.json',
    'intility_arena': 'intility_arena.json', 'jotun_arena': 'Jotun_Arena_Sandefjord.json',
    'nordmore_stadion': 'kristiansund_stadion.json', 'lerkendal_stadion': 'lerkendal_stadion.json',
    'lyse_arena': 'Viking_Stadion_Stavanger.json', 'marienlyst_stadion': 'marienlyst_stadion.json',
    'romssa_arena': 'Romssa_Arena_Tromsø.json', 'sarpsborg_stadion': 'sarpsborg_stadion.json',
    'skagerak_arena': 'skagerak_arena.json', 'arasen_stadion': 'arasen.json',
}
def load_sibling(site_key):
    fn = os.path.join(NOM_DIR, SIBLING[site_key])
    raw = open(fn, 'rb').read()
    data = json.loads(raw)
    pick = None; idx = None
    for i, d in enumerate(data):
        if d.get('type') in ('stadium', 'sports_centre', 'pitch', 'sports') or 'stadion' in d.get('display_name', '').lower() or 'arena' in d.get('display_name', '').lower():
            pick = d; idx = i; break
    if pick is None and data:
        pick = data[0]; idx = 0
    mt = datetime.fromtimestamp(os.path.getmtime(fn), tz=CST).strftime('%Y-%m-%dT%H:%M:%S+08:00')
    return {'lat': float(pick['lat']) if pick else None, 'lon': float(pick['lon']) if pick else None,
            'display_name': pick.get('display_name') if pick else None,
            'type': pick.get('type') if pick else None, 'class': pick.get('class') if pick else None,
            'importance': pick.get('importance') if pick else None, 'index': idx,
            'n_results': len(data), 'sha256': hashlib.sha256(raw).hexdigest(), 'retrieved_at': mt,
            'provider': 'nominatim_file', 'source_url': 'evidence/nominatim/' + SIBLING[site_key] + ' (Nominatim JSON captured in this request work dir; re-read and re-hashed by this route)',
            'field_locator': 'JSON result index %s (stadium-type pick among %d results)' % (idx, len(data)),
            'sha_note': 'SHA-256 re-computed by this route from the cited file bytes.'}
MAP_RESULTS = {
    'bryne_stadion': {'lat': 58.72948, 'lon': 5.64908,
        'display_name': 'Stadion Bowling, Trallfavegen 1, 4344 Bryne, Norge',
        'match_quality': 'matched_level=FULL_ADDRESS, relevance=100; geocoder POI label is Stadion Bowling at the stadium street address Trallfavegen 1, Bryne'},
    'fredrikstad_stadion': {'lat': 59.21333, 'lon': 10.92816,
        'display_name': 'Fredrikstad Stadion, K. G. Meldahls vei 9, 1671 Fredrikstad, Norge',
        'match_quality': 'matched_level=FULL_ADDRESS, relevance=100; a second STREET-level result (Stadion, 1671 Fredrikstad) sits ~90 m away and matches the baseline coordinates'},
    'kfum_arena': {'lat': 59.88863, 'lon': 10.78208,
        'display_name': 'Kfum Arena, Ekebergveien 109, 1178 Oslo, Norge',
        'match_quality': 'matched_level=FULL_ADDRESS, relevance=100'},
}
_now = datetime.now(tz=CST).strftime('%Y-%m-%dT%H:%M:%S+08:00')
GEO = {}
for sk in SITE.values():
    if sk in SIBLING:
        GEO[sk] = load_sibling(sk)
    else:
        mr = MAP_RESULTS[sk]
        GEO[sk] = {'lat': mr['lat'], 'lon': mr['lon'], 'display_name': mr['display_name'],
                   'type': None, 'class': None, 'importance': None, 'index': 0, 'n_results': 1,
                   'sha256': None, 'retrieved_at': _now, 'provider': 'map_geocode',
                   'source_url': 'map.geocode tool (provider AUTO), query "<site>, <city>, Norway"',
                   'field_locator': 'tool result[0]', 'match_quality': mr['match_quality'],
                   'sha_note': 'null: first-party geocoder tool result, no downloadable bytes; result recorded verbatim with match level/relevance.'}
missing_geo = [k for k, v in GEO.items() if v['lat'] is None]
print('sites with coords:', sum(1 for v in GEO.values() if v['lat'] is not None), '/', len(GEO), 'missing:', missing_geo)
for k in sorted(GEO):
    print('  GEO', k, GEO[k]['lat'], GEO[k]['lon'], '|', GEO[k]['display_name'], '|', GEO[k]['provider'])

# FBref spot observations (text-layer read 2026-10-28; venue column only, no other columns copied)
FBREF_URL_2024 = 'https://fbref.com/en/comps/28/2024/schedule/2024-Eliteserien-Scores-and-Fixtures'
FBREF_SPOT = {
    # record_key -> (fbref venue, note)
    'eliteserien-2024-r01-kfum-oslo-vs-ham-kam': ('KFUM Arena', 'FBref lists KFUM Arena for this fixture, disagreeing with NFF + baseline (Intility Arena). Preserved as competing candidate; NFF official priority + baseline agreement prevail, so row stays neutral, not conflict.'),
    'eliteserien-2024-r03-kfum-oslo-vs-stromsgodset': ('Intility Arena', 'FBref agrees with NFF + baseline (Intility Arena).'),
    'eliteserien-2024-r13-kristiansund-bk-vs-fredrikstad': ('Aker Stadion', 'FBref agrees with NFF + baseline (Aker stadion).'),
    'eliteserien-2024-r07-sandefjord-vs-sarpsborg-08-ff': ('Jotun Krøllgras', 'FBref pitch-level label within the Jotun Arena complex; NFF official Bane is Jotun Arena. Same complex, not a different venue, not a conflict.'),
    'eliteserien-2024-r09-stromsgodset-vs-haugesund': ('Marienlyst Kunstgress', 'FBref pitch-level label within the Marienlyst complex; NFF official Bane is Marienlyst stadion. Same complex, not a different venue, not a conflict.'),
}
# verify the two spot record_keys exist
base_keys = {o['record_key'] for o in base}
for k in FBREF_SPOT:
    assert k in base_keys, k

VARIANT_NOTE = {
    ('Fredrikstad stadion', 'Nye Fredrikstad Stadion'): 'Naming variant, same site: NFF uses Fredrikstad stadion; baseline 2024 uses Nye Fredrikstad Stadion (2025 baseline already Fredrikstad Stadion).',
    ('Lyse Arena', 'SR-Bank Arena'): 'Naming variant, same site (sponsor rename): NFF uses Lyse Arena in both seasons; baseline 2024 uses SR-Bank Arena (2025 baseline already Lyse Arena).',
    ('Briskeby', 'Briskeby Arena'): 'Naming variant, same site: NFF uses short form Briskeby; baseline uses Briskeby Arena.',
    ('Sarpsborg st KG', 'Sarpsborg Stadion'): 'NFF standard Bane name for Sarpsborg home matches in both seasons: Sarpsborg st KG (st KG = stadion kunstgress, artificial-turf pitch designation within the Sarpsborg Stadion complex). Not a one-off move; all 30 Sarpsborg home matches carry this Bane value.',
    ('Nordmøre stadion', 'Kristiansund Stadion'): 'Naming variant, same site: NFF uses Nordmøre stadion in both seasons; baseline 2025 uses Kristiansund Stadion (2024 baseline already Nordmøre stadion).',
    ('Haugesund Sparebank Arena', 'Haugesund Stadion'): 'Naming variant, same site: NFF uses Haugesund Sparebank Arena in both seasons; baseline 2025 uses Haugesund Stadion (2024 baseline already Haugesund Sparebank Arena).',
    ('KFUM-Arena', 'KFUM Arena'): 'Punctuation variant, same site: NFF uses KFUM-Arena (hyphen); baseline uses KFUM Arena (space).',
}

rows_out = []
for o in sorted(base, key=lambda x: (x['season'], x['round'], x['local_date'], x['record_key'])):
    m = mmap[(o['season'], o['round'], o['home_team'], o['away_team'], o['local_date'])]
    nff_bane = m['nff_bane']
    base_venue = o['baseline_venue_name']
    site = SITE[nff_bane]
    assert BSITE[base_venue] == site, (o['record_key'], base_venue, nff_bane)
    home_mode = mode[(o['season'], o['home_team'])]
    away_mode = mode[(o['season'], o['away_team'])]
    if nff_bane != home_mode and nff_bane != away_mode:
        status = 'neutral'
    elif nff_bane != home_mode:
        status = 'moved'
    else:
        status = 'confirmed'
    geo = GEO[site]
    candidates = [
        {'venue_name': nff_bane, 'venue_city': o['baseline_venue_city'],
         'source': 'NFF fotball.no official tournament calendar (Excel download)',
         'source_tier': 'official', 'role': 'verified_actual_matchday_venue',
         'note': 'Match-specific Bane value for this fixture (Kampnummer %s).' % m['nff_kampnummer']},
        {'venue_name': base_venue, 'venue_city': o['baseline_venue_city'],
         'source': 'baseline fixtures_2018_2025.jsonl (api-football fixture.venue)',
         'source_tier': 'provider', 'role': 'source_venue_agrees_on_site',
         'note': VARIANT_NOTE.get((nff_bane, base_venue), 'Same site as NFF Bane.')},
    ]
    notes = []
    if (nff_bane, base_venue) in VARIANT_NOTE:
        notes.append(VARIANT_NOTE[(nff_bane, base_venue)])
    if status == 'neutral':
        candidates.append({'venue_name': home_mode, 'venue_city': None,
            'source': 'NFF calendar season mode for this home club',
            'source_tier': 'official-derived',
            'role': 'club_regular_home_venue_candidate_ONLY',
            'note': 'Club default home venue candidate (season mode of NFF Bane for this club-season). NOT the actual matchday venue for this match; listed only so the deviation is explicit.'})
        notes.append('Off-regular-ground match: verified venue %s differs from home club season-regular Bane %s and from away club season-regular Bane %s, hence neutral (not moved under the stated rule).' % (nff_bane, home_mode, away_mode))
    if o['record_key'] in FBREF_SPOT:
        fv, fnote = FBREF_SPOT[o['record_key']]
        candidates.append({'venue_name': fv, 'venue_city': None,
            'source': 'FBref 2024 schedule Venue column (non-official)',
            'source_tier': 'non-official', 'role': 'spot_check_candidate',
            'note': fnote})
        notes.append('FBref spot check: ' + fnote)
    if site == 'sarpsborg_stadion':
        notes.append('Coordinates are for the Sarpsborg Stadion complex; NFF Bane Sarpsborg st KG is the pitch designation within that complex, and no separate pitch-level coordinates were published by the geocoding source.')
    if o['baseline_venue_city'] in ('Bodo', 'Bodø') or nff_bane == 'Aspmyra stadion':
        notes.append('City spelling variant: baseline city is Bodo in 2024 rows and Bodø in 2025 rows for the same Aspmyra site; verified city below copies the baseline spelling for this match.')
    if o['baseline_venue_city'] in ('Tromso', 'Tromsø') or nff_bane == 'Romssa Arena':
        notes.append('City spelling variant: baseline city is Tromso in 2024 rows and Tromsø in 2025 rows for the same Romssa site; verified city below copies the baseline spelling for this match.')
    if geo['provider'] == 'nominatim_file':
        mq = 'type=%s, class=%s, importance=%s' % (geo['type'], geo['class'], geo['importance'])
        src_name = 'OpenStreetMap Nominatim JSON (file captured in this request work dir, re-hashed by this route)'
    else:
        mq = geo['match_quality']
        src_name = 'map.geocode tool (provider AUTO)'
    coord_prov = {
        'source': src_name,
        'source_url': geo['source_url'],
        'final_url': geo['source_url'],
        'field_locator': geo['field_locator'],
        'source_value_display_name': geo['display_name'],
        'match_quality': mq,
        'source_sha256': geo['sha256'],
        'sha_note': geo['sha_note'],
        'retrieved_at': geo['retrieved_at'],
        'coordinate_level': 'venue_site',
        'coordinate_level_note': 'Coordinates are for the venue site, shared across all matches at that site. They are NOT a match-specific confirmation.',
    }
    # fix source_url properly from geocode summary logic: rebuild query per site
    row = {
        'record_key': o['record_key'],
        'season': o['season'],
        'local_date': o['local_date'],
        'home_team': o['home_team'],
        'away_team': o['away_team'],
        'kickoff_local': o['kickoff_local'],
        'round': o['round'],
        'round_label': o['round_label'],
        'provider_fixture_id': o['provider_fixture_id'],
        'source_venue_name': base_venue,
        'source_venue_city': o['baseline_venue_city'],
        'verified_actual_matchday_venue_name': nff_bane,
        'verified_actual_matchday_venue_city': o['baseline_venue_city'],
        'verified_venue_city_source': 'baseline venue_city for this match (NFF Bane column carries no city)',
        'venue_status': status,
        'venue_candidates': candidates,
        'club_regular_home_venue_nff': home_mode,
        'away_regular_home_venue_nff': away_mode,
        'venue_lat': geo['lat'],
        'venue_lon': geo['lon'],
        'coordinate_provenance': coord_prov,
        'venue_note': ' '.join(notes) if notes else None,
        'evidence': [
            {'source': 'NFF fotball.no official tournament calendar (Excel download)',
             'source_tier': 'official',
             'source_url': NFF_URL[o['season']],
             'final_url': NFF_URL[o['season']],
             'retrieved_at': NFF_RETRIEVED[o['season']],
             'field_locator': 'sheet1 row: Runde=%s, Dato=%s, Hjemmelag=%s, Bortelag=%s, Bane=%s, Kampnummer=%s' % (o['round'], o['local_date'], m['nff_home_raw'], m['nff_away_raw'], nff_bane, m['nff_kampnummer']),
             'source_value': nff_bane,
             'source_sha256': NFF_SHA[o['season']],
             'sha_note': 'SHA-256 of the downloaded .xlsx bytes. The source file sixth column was dropped at parse time and is never stored or returned in this delivery.'},
            {'source': 'baseline fixtures_2018_2025.jsonl (api-football fixture.venue)',
             'source_tier': 'provider',
             'source_url': 'baseline file (local); original provider query https://v3.football.api-sports.io/fixtures?league=103&season=%s' % o['season'],
             'final_url': None,
             'retrieved_at': '2026-10-17T22:21:31+08:00 (baseline provenance)',
             'field_locator': 'record_key=%s, method_context.venue_name / venue_city' % o['record_key'],
             'source_value': base_venue,
             'source_sha256': BASE_SHA[o['season']],
             'sha_note': 'Per-season api-football API response hash from baseline provenance, not a per-row byte hash.'},
        ],
    }
    if o['record_key'] in FBREF_SPOT:
        fv, fnote = FBREF_SPOT[o['record_key']]
        row['evidence'].append({'source': 'FBref 2024 schedule Venue column (non-official)',
            'source_tier': 'non-official', 'source_url': FBREF_URL_2024, 'final_url': FBREF_URL_2024,
            'retrieved_at': '2026-10-28 (this round text-layer read; page crawl timestamp shown 2026-09-05 16:23 UTC)',
            'field_locator': 'Schedule table row for this fixture (Date/Home/Away/Venue columns only)',
            'source_value': fv, 'source_sha256': None,
            'sha_note': 'null: text-layer retrieval, no page bytes captured; only the Venue column value was recorded.'})
    rows_out.append(row)

for r in rows_out:
    r['venue_site_key'] = SITE[r['verified_actual_matchday_venue_name']]

with open(os.path.join(WORK, 'venue_audit_2024_2025.jsonl'), 'w') as f:
    for r in rows_out:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print('rows:', len(rows_out))
print('status counts:', collections.Counter(r['venue_status'] for r in rows_out))
for s in (2024, 2025):
    print(s, collections.Counter(r['venue_status'] for r in rows_out if r['season'] == s))
print('rows with coords:', sum(1 for r in rows_out if r['venue_lat'] is not None))
print('sites:', len(set(r['venue_site_key'] for r in rows_out)))
# excerpt file: NFF venue values only (no scores anywhere)
excerpt = [{'season': m['season'], 'round': m['round'], 'local_date': m['local_date'],
            'home_raw': m['nff_home_raw'], 'away_raw': m['nff_away_raw'],
            'bane': m['nff_bane'], 'kampnummer': m['nff_kampnummer']} for m in matched]
with open(os.path.join(EVID, 'nff_venue_excerpt.json'), 'w') as f:
    json.dump(excerpt, f, ensure_ascii=False, indent=1)
print('excerpt sha:', hashlib.sha256(open(os.path.join(EVID, 'nff_venue_excerpt.json'), 'rb').read()).hexdigest())
# validation: linkage fields verbatim vs baseline
bmap2 = {(o['season'], o['round'], o['home_team'], o['away_team'], o['local_date']): o for o in base}
for r in rows_out:
    o = bmap2[(r['season'], r['round'], r['home_team'], r['away_team'], r['local_date'])]
    assert r['record_key'] == o['record_key'] and r['local_date'] == o['local_date'] and r['kickoff_local'] == o['kickoff_local'] and r['round_label'] == o['round_label'] and r['provider_fixture_id'] == o['provider_fixture_id'] and r['source_venue_name'] == o['baseline_venue_name'] and r['source_venue_city'] == o['baseline_venue_city']
print('linkage verbatim check: PASS')
# forbidden content scan
import re as _re
blob = open(os.path.join(WORK, 'venue_audit_2024_2025.jsonl'), encoding='utf-8').read()
for pat in ['qimen', 'Snapshot', 'Outcome', 'Review', 'Gold', 'true solar', 'probability', 'prediction']:
    assert pat.lower() not in blob.lower(), pat
print('forbidden-term scan: PASS (no qimen/snapshot/outcome/review/gold/prediction terms)')
