#!/usr/bin/env python3
"""B路: 审计 A 路交付物 bundesliga_201819_kickoff_rows.jsonl.
1) 行数 306 / 无重复 fixture_key
2) source_sha256: 对 evidence/ 内 5 份 PDF 逐字节重算,逐行核对(5/5 全验,超任务要求的至少 2 个)
3) 时区: 全行 Europe/Berlin; kickoff_utc 用 zoneinfo 独立重算(含 2019-03-31 夏令时切换)
4) field_locator: 逐行解析 verbatim 行内日期/时间/轮次/官方队名,与行值核对
5) 行值 vs -007 基线 / vs B路独立 PDF 解析 / vs FBref 转录,逐项比对
"""
import json, hashlib, re
from datetime import datetime
from zoneinfo import ZoneInfo

W = '/home/hatch/workspace/ai-inbox/work-req-20261029-001'
A = json.load(open(W + '/bundesliga_201819_kickoff_rows.jsonl', encoding='utf-8')) \
    if False else [json.loads(l) for l in open(W + '/bundesliga_201819_kickoff_rows.jsonl', encoding='utf-8')]
B007 = json.load(open('/tmp/b-verify/req-20261003-007.json', encoding='utf-8'))['data']['rows']
PDF = json.load(open('/tmp/b-verify/pdf_vs_007.json', encoding='utf-8'))['pdf_rows']
FB = json.load(open('/tmp/b-verify/fbref_vs_all.json', encoding='utf-8'))['diffs']

print('A rows:', len(A))
print('dup fixture_key:', len(A) - len({r['fixture_key'] for r in A}))
print('dup (round,home,away):', len(A) - len({(r['round'], r['home_team'], r['away_team']) for r in A}))

# --- 2) sha256 ---
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()
ev = {'dfl_spieltage_1-6.pdf': None, 'dfl_spieltage_7-14.pdf': None,
      'dfl_spieltage_15-21.pdf': None, 'dfl_spieltage_22-28.pdf': None,
      'dfl_spieltage_29-34.pdf': None}
for fn in ev:
    ev[fn] = sha(W + '/evidence/' + fn)
print('evidence sha:', json.dumps(ev, indent=0))
url2file = {
    'https://media.dfl.de/sites/3/2018/11/Bundesliga_2018-19_Spieltage_1-6.pdf': 'dfl_spieltage_1-6.pdf',
    'https://media.dfl.de/sites/3/2018/11/Bundesliga_2018-19_Spieltage_7-14.pdf': 'dfl_spieltage_7-14.pdf',
    'https://media.bundesliga-gruppe.de/sites/2/2018/11/Bundesliga_2018-19_Spieltage_15-21-1.pdf': 'dfl_spieltage_15-21.pdf',
    'https://media.bundesliga-gruppe.de/sites/2/2018/12/BL-MD-22-28.pdf': 'dfl_spieltage_22-28.pdf',
    'https://media.dfl.de/sites/2/2019/03/Bundesliga_Spieltage_29-34.pdf': 'dfl_spieltage_29-34.pdf',
}
bad_sha = []
src_urls = {}
for r in A:
    src_urls.setdefault(r['source_url'], []).append(r['fixture_key'])
    fn = url2file.get(r['source_url'])
    if fn is None:
        bad_sha.append((r['fixture_key'], 'unknown source_url', r['source_url']))
    elif r['source_sha256'] != ev[fn]:
        bad_sha.append((r['fixture_key'], 'sha mismatch', r['source_sha256'], ev[fn]))
print('source_url distribution:', {u.split('/')[-1]: len(v) for u, v in src_urls.items()})
print('sha bad rows:', len(bad_sha), bad_sha[:5])
print('rows with null sha:', sum(1 for r in A if not r.get('source_sha256')))

# --- 3) timezone + utc ---
berlin = ZoneInfo('Europe/Berlin')
print('timezone values:', {r['timezone'] for r in A})
print('kickoff_utc_method missing:', sum(1 for r in A if not r.get('kickoff_utc_method')))
bad_utc = []
for r in A:
    d = datetime.strptime(r['match_date'] if r['official_match_date'] is None else r['official_match_date'], '%d/%m/%Y')
    # UTC 换算应以官方日期(即 PDF 行内日期)为准; Frankfurt-Mainz 行官方日期 11/05, A 路 kickoff_utc 用 2019-05-11T13:30Z
    hh, mm = r['kickoff_local'].split(':')
    local = datetime(d.year, d.month, d.day, int(hh), int(mm), tzinfo=berlin)
    expect = local.astimezone(ZoneInfo('UTC')).strftime('%Y-%m-%dT%H:%M:%SZ')
    if r['kickoff_utc'] != expect:
        bad_utc.append((r['fixture_key'], r['kickoff_utc'], expect, 'official_date_used' if r['official_match_date'] else 'match_date'))
print('utc bad rows:', len(bad_utc), bad_utc[:5])
# DST 边界抽查
for k in ['2018-19|29/03/2019|Hoffenheim|Leverkusen', '2018-19|30/03/2019|Freiburg|Bayern Munich',
          '2018-19|31/03/2019|Hannover|Schalke 04', '2018-19|31/03/2019|Ein Frankfurt|Stuttgart']:
    r = next(x for x in A if x['fixture_key'] == k)
    print('DST check', k, r['kickoff_local'], '->', r['kickoff_utc'])

# --- 4) field_locator ---
loc_pat = re.compile(r'(\d{2})\.(\d{2})\.(\d{4})\s*-\s*\w+\s+(\d{2})[.:](\d{2})\s+(\d+)\s+\d+\s+(.+?)\s{2,}(.+)$')
bad_loc, no_loc = [], []
for r in A:
    loc = r.get('field_locator') or ''
    if not loc:
        no_loc.append(r['fixture_key']); continue
    m = loc_pat.search(loc)
    if not m:
        bad_loc.append((r['fixture_key'], 'unparsed', loc[:120])); continue
    dd, mo, yy, hh, mi, rnd, h_off, a_off = m.groups()
    exp_date = r['official_match_date'] or r['match_date']
    if f'{dd}/{mo}/{yy}' != exp_date or f'{hh}:{mi}' != r['kickoff_local'] or int(rnd) != r['round'] \
       or h_off.strip() != r['source_home_team'] or a_off.strip() != r['source_away_team']:
        bad_loc.append((r['fixture_key'], 'value mismatch', loc[:160],
                        {'loc_date': f'{dd}/{mo}/{yy}', 'row_date': exp_date,
                         'loc_time': f'{hh}:{mi}', 'row_time': r['kickoff_local'],
                         'loc_round': rnd, 'row_round': r['round']}))
print('locator missing:', len(no_loc), 'locator bad/unparsed:', len(bad_loc))
for b in bad_loc[:5]:
    print('  ', b)

# --- 5a) vs -007 ---
m007 = {r['fixture_key']: r for r in B007}
print('A-only keys:', sorted(set(r['fixture_key'] for r in A) - set(m007)))
print('007-only keys:', sorted(set(m007) - set(r['fixture_key'] for r in A)))
v007 = []
for r in A:
    b = m007.get(r['fixture_key'])
    if not b: continue
    for f in ['match_date', 'official_match_date', 'date_note', 'home_team', 'away_team', 'round', 'kickoff_local']:
        if r.get(f) != b.get(f):
            v007.append((r['fixture_key'], f, r.get(f), b.get(f)))
print('value diffs vs -007:', len(v007), v007[:5])

# --- 5b) vs B路独立 PDF 解析 ---
OFFICIAL_MAP = {
    'FC Bayern München': 'Bayern Munich', 'TSG 1899 Hoffenheim': 'Hoffenheim',
    'Fortuna Düsseldorf': 'Fortuna Dusseldorf', 'FC Augsburg': 'Augsburg',
    'Hertha BSC': 'Hertha', '1. FC Nürnberg': 'Nurnberg',
    'SV Werder Bremen': 'Werder Bremen', 'Hannover 96': 'Hannover',
    'VfL Wolfsburg': 'Wolfsburg', 'FC Schalke 04': 'Schalke 04',
    'SC Freiburg': 'Freiburg', 'Sport-Club Freiburg': 'Freiburg',
    'Eintracht Frankfurt': 'Ein Frankfurt',
    'Borussia Mönchengladbach': "M'gladbach", 'Bayer 04 Leverkusen': 'Leverkusen',
    '1. FSV Mainz 05': 'Mainz', 'VfB Stuttgart': 'Stuttgart',
    'Borussia Dortmund': 'Dortmund', 'RB Leipzig': 'RB Leipzig',
}
def dmy(s): return datetime.strptime(s, '%d/%m/%Y').strftime('%Y-%m-%d')
pmap = {}
for p in PDF:
    pmap[(p['round'], OFFICIAL_MAP[p['home_off']], OFFICIAL_MAP[p['away_off']])] = p
vpdf = []
for r in A:
    p = pmap.get((r['round'], r['home_team'], r['away_team']))
    if not p:
        vpdf.append((r['fixture_key'], 'missing in B-pdf-parse')); continue
    exp_date = r['official_match_date'] or r['match_date']
    if dmy(p['date']) != dmy(exp_date) or p['kickoff'] != r['kickoff_local']:
        vpdf.append((r['fixture_key'], p['date'], exp_date, p['kickoff'], r['kickoff_local']))
print('value diffs vs B-pdf-parse:', len(vpdf), vpdf[:5])

# --- 5c) vs FBref: 仅 Frankfurt-Mainz 一场应有差异 ---
print('FBref diffs (expected: 1 fixture, 4 rows):', len(FB))
# status / conflict_flag
print('status values:', {r['status'] for r in A})
print('conflict_flag values:', [(r['fixture_key'], r['conflict_flag']) for r in A if r.get('conflict_flag')])
print('source_tier values:', {r['source_tier'] for r in A})
print('retrieved_at values:', {r['retrieved_at'] for r in A})
