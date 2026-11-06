#!/usr/bin/env python3
"""B路: FBref 2018-19 赛季赛程(文本层转录) vs -007 基线 / D1.csv / DFL PDF 解析,四方比对.
FBref 时间列首值 = 柏林本地时间(括号内为美国太平洋时间,已按夏令时核对).
比对键: (round, home, away),队名统一为 Football-Data 口径(-007/D1 所用).
-007 的 match_date 为请求键日期; official_match_date 仅 Frankfurt-Mainz 一行非空.
差异两值并存,不自动取舍.
"""
import csv, json
from collections import Counter
from datetime import datetime

FBREF = '/tmp/b-verify/fbref_201819.csv'
BASE  = '/tmp/b-verify/req-20261003-007.json'
D1    = '/tmp/b-verify/D1-1819.csv'
PDF   = '/tmp/b-verify/pdf_vs_007.json'
OUT   = '/tmp/b-verify/fbref_vs_all.json'

FBREF_MAP = {
    'Düsseldorf': 'Fortuna Dusseldorf', 'Hertha BSC': 'Hertha',
    'Nürnberg': 'Nurnberg', 'Hannover 96': 'Hannover',
    'Frankfurt': 'Ein Frankfurt', 'Gladbach': "M'gladbach",
    'Mainz 05': 'Mainz',
}
OFFICIAL_MAP = {
    'FC Bayern München': 'Bayern Munich', 'TSG 1899 Hoffenheim': 'Hoffenheim',
    'Fortuna Düsseldorf': 'Fortuna Dusseldorf', 'FC Augsburg': 'Augsburg',
    'Hertha BSC': 'Hertha', '1. FC Nürnberg': 'Nurnberg',
    'SV Werder Bremen': 'Werder Bremen', 'Hannover 96': 'Hannover',
    'VfL Wolfsburg': 'Wolfsburg', 'FC Schalke 04': 'Schalke 04',
    'SC Freiburg': 'Freiburg', 'Sport-Club Freiburg': 'Freiburg', 'Eintracht Frankfurt': 'Ein Frankfurt',
    'Borussia Mönchengladbach': "M'gladbach", 'Bayer 04 Leverkusen': 'Leverkusen',
    '1. FSV Mainz 05': 'Mainz', 'VfB Stuttgart': 'Stuttgart',
    'Borussia Dortmund': 'Dortmund', 'RB Leipzig': 'RB Leipzig',
}
def dmy_to_iso(s):
    return datetime.strptime(s.strip(), '%d/%m/%Y').strftime('%Y-%m-%d')

# --- FBref ---
fb = []
with open(FBREF, encoding='utf-8') as f:
    for r in csv.DictReader(f):
        fb.append({'round': int(r['wk']), 'date': r['date'], 'time': r['time'],
                   'home': FBREF_MAP.get(r['home'], r['home']),
                   'away': FBREF_MAP.get(r['away'], r['away'])})
print('fbref rows:', len(fb), 'dup keys:', len(fb) - len({(x['round'],x['home'],x['away']) for x in fb}))
print('fbref teams:', sorted({x['home'] for x in fb} | {x['away'] for x in fb}))

# --- -007 ---
base = json.load(open(BASE, encoding='utf-8'))['data']['rows']
b007 = {}
for r in base:
    b007[(r['round'], r['home_team'], r['away_team'])] = {
        'fixture_key': r['fixture_key'],
        'match_date': dmy_to_iso(r['match_date']),
        'official_date': dmy_to_iso(r['official_match_date']) if r.get('official_match_date') else None,
        'kickoff': r['kickoff_local'], 'source': r['source_url']}
print('007 rows:', len(b007))

# --- D1 ---
d1 = {}
with open(D1, encoding='utf-8') as f:
    for r in csv.DictReader(f):
        d1[(r['HomeTeam'], r['AwayTeam'])] = dmy_to_iso(r['Date'])
print('D1 rows:', len(d1))

# --- PDF parsed ---
pdf = json.load(open(PDF, encoding='utf-8'))['pdf_rows']
pdfmap = {}
for r in pdf:
    h, a = OFFICIAL_MAP.get(r['home_off'], r['home_off']), OFFICIAL_MAP.get(r['away_off'], r['away_off'])
    pdfmap[(r['round'], h, a)] = {'date': dmy_to_iso(r['date']), 'time': r['kickoff']}
print('pdf rows:', len(pdfmap), 'unmapped officials:',
      sorted({r['home_off'] for r in pdf} | {r['away_off'] for r in pdf} - set(OFFICIAL_MAP)))

fbmap = {(x['round'], x['home'], x['away']): x for x in fb}
print('fbref-only keys:', sorted(set(fbmap) - set(b007)))
print('007-only keys:', sorted(set(b007) - set(fbmap)))
print('d1-only keys (vs fbref):', sorted(set(d1) - {(k[1], k[2]) for k in fbmap}))
print('pdf-only keys:', sorted(set(pdfmap) - set(fbmap)))

diffs = []
for k in sorted(fbmap):
    f, b = fbmap[k], b007.get(k)
    if b is None:
        diffs.append({'key': [k[0], k[1], k[2]], 'type': 'missing_in_007', 'fbref': f})
        continue
    d1date = d1.get((k[1], k[2]))
    p = pdfmap.get(k)
    if f['date'] != b['match_date']:
        diffs.append({'key': [k[0], k[1], k[2]], 'type': 'date_fbref_vs_007_match_date',
                      'fbref_date': f['date'], 'fbref_time': f['time'],
                      '007_match_date': b['match_date'], '007_official_date': b['official_date'],
                      'd1_date': d1date, 'pdf_date': p['date'] if p else None,
                      'fixture_key': b['fixture_key']})
    if b['official_date'] and f['date'] != b['official_date']:
        diffs.append({'key': [k[0], k[1], k[2]], 'type': 'date_fbref_vs_007_official_date',
                      'fbref_date': f['date'], 'fbref_time': f['time'],
                      '007_match_date': b['match_date'], '007_official_date': b['official_date'],
                      'd1_date': d1date, 'pdf_date': p['date'] if p else None,
                      'fixture_key': b['fixture_key']})
    if f['time'] != b['kickoff']:
        diffs.append({'key': [k[0], k[1], k[2]], 'type': 'kickoff_fbref_vs_007',
                      'fbref_date': f['date'], 'fbref_time': f['time'],
                      '007_kickoff': b['kickoff'], '007_match_date': b['match_date'],
                      '007_official_date': b['official_date'],
                      'pdf_time': p['time'] if p else None,
                      'fixture_key': b['fixture_key']})
    if d1date and d1date != f['date']:
        diffs.append({'key': [k[0], k[1], k[2]], 'type': 'date_fbref_vs_d1',
                      'fbref_date': f['date'], 'd1_date': d1date})
    if p and p['date'] != f['date']:
        diffs.append({'key': [k[0], k[1], k[2]], 'type': 'date_fbref_vs_pdf',
                      'fbref_date': f['date'], 'pdf_date': p['date']})
    if p and p['time'] != f['time']:
        diffs.append({'key': [k[0], k[1], k[2]], 'type': 'kickoff_fbref_vs_pdf',
                      'fbref_time': f['time'], 'pdf_time': p['time']})

print('diff type counts:', Counter(d['type'] for d in diffs))
print('total diff rows:', len(diffs))
json.dump({'diffs': diffs}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
for d in diffs:
    print(json.dumps(d, ensure_ascii=False))
