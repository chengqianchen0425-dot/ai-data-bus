#!/usr/bin/env python3
"""req-20261010-002 Football-Data 批量填充：2848 fixture×bookmaker 缺口填 earliest_verified_pre_match + closing。
铁律：缺失记 NULL+原因，绝不猜测；FD 快照列绝不冒充 true_opening。"""
import csv, json, hashlib, os
from datetime import datetime

BASE = os.path.expanduser('~/workspace/ai-inbox')
REQ = BASE + '/repo/requests/req-20261010-002.json'
BATCH = BASE + '/work-req-20261010-004/fd_batch/'
OUT = BASE + '/work-req-20261010-002/fd_fill.jsonl'

SEASON_FILE = {'2021/22': 'fd_2122_P1.csv', '2022/23': 'fd_2223_P1.csv',
               '2023/24': 'fd_2324_P1.csv', '2024/25': 'fd_2425_P1.csv'}
SEASON_CODE = {'2021/22': '2122', '2022/23': '2223', '2023/24': '2324', '2024/25': '2425'}
BOOK_COLS = {
    'bet365':       {'pre': ['B365H', 'B365D', 'B365A'], 'clo': ['B365CH', 'B365CD', 'B365CA']},
    'pinnacle':     {'pre': ['PSH', 'PSD', 'PSA'],       'clo': ['PSCH', 'PSCD', 'PSCA']},
    'william_hill': {'pre': ['BWH', 'BWD', 'BWA'],       'clo': ['BWCH', 'BWCD', 'BWCA']},
}
PRE_FIELDS = ['earliest_verified_pre_match_home', 'earliest_verified_pre_match_draw', 'earliest_verified_pre_match_away']
CLO_FIELDS = ['closing_home', 'closing_draw', 'closing_away']

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

# 1. 读 FD
fd_index = {}          # (season, date_iso, home, away) -> row dict
fd_teams = {}          # season -> set(teams)
fd_meta = {}
for season, fname in SEASON_FILE.items():
    path = BATCH + fname
    fd_meta[season] = {'file': fname, 'sha256': sha256(path),
                       'mtime': datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')}
    with open(path, encoding='utf-8-sig') as fh:
        rows = list(csv.DictReader(fh))
    fd_teams[season] = set()
    for r in rows:
        d = datetime.strptime(r['Date'].strip(), '%d/%m/%Y').strftime('%Y-%m-%d')
        key = (season, d, r['HomeTeam'].strip(), r['AwayTeam'].strip())
        assert key not in fd_index, f'DUPLICATE FD KEY {key}'
        fd_index[key] = r
        fd_teams[season].add(r['HomeTeam'].strip()); fd_teams[season].add(r['AwayTeam'].strip())

# 2. 读请求
req = json.load(open(REQ))
scope = req['params']['fixture_scope']
assert len(scope) == 2848, f'fixture_scope={len(scope)} != 2848'

# 3. 队名映射：请求名 -> FD 名（逐赛季校验）
req_teams = {}
for e in scope:
    req_teams.setdefault(e['season'], set()).add(e['home_team'])
    req_teams.setdefault(e['season'], set()).add(e['away_team'])
team_mapping = {}
map_problems = []
for season, names in req_teams.items():
    for n in sorted(names):
        if n in fd_teams[season]:
            team_mapping[n] = n
        else:
            map_problems.append((season, n))
            team_mapping[n] = None  # 无法映射，绝不猜

def cell_float(v):
    v = (v or '').strip()
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        return None

stats = {'total': 0, 'full_filled': 0, 'partial': 0, 'all_missing': 0,
         'field_filled': 0, 'field_missing': 0, 'no_fd_row': 0}
no_row_keys = []
missing_by_bm_season = {}

with open(OUT, 'w', encoding='utf-8') as out:
    # 头记录：映射表
    out.write(json.dumps({
        'record_type': 'team_mapping',
        'request_id': 'req-20261010-002',
        'note': 'request team name -> football-data.csv team name; null=unmappable(never guessed)',
        'mapping': team_mapping,
        'fd_teams_per_season': {s: sorted(t) for s, t in fd_teams.items()},
        'mapping_problems': map_problems,
    }, ensure_ascii=False) + '\n')

    for e in scope:
        season, date, home, away, bm = e['season'], e['date'], e['home_team'], e['away_team'], e['bookmaker']
        fkey = f'{season}|{date}|{home}|{away}'
        stats['total'] += 1
        row = fd_index.get((season, date, team_mapping.get(home) or '', team_mapping.get(away) or ''))
        fields = {}
        if row is None:
            stats['no_fd_row'] += 1
            no_row_keys.append(fkey + '|' + bm)
            for f in PRE_FIELDS + CLO_FIELDS:
                fields[f] = {'value': None, 'status': 'missing', 'reason': 'fixture_not_in_source',
                             'field_semantics': 'unavailable'}
                stats['field_missing'] += 1
            src_file, src_url, src_sha = None, None, None
        else:
            cols = BOOK_COLS[bm]
            src_file = SEASON_FILE[season]
            src_url = f'https://www.football-data.co.uk/mmz4281/{SEASON_CODE[season]}/P1.csv'
            src_sha = fd_meta[season]['sha256']
            nfilled = 0
            for f, col in zip(PRE_FIELDS, cols['pre']):
                v = cell_float(row.get(col))
                if v is None:
                    fields[f] = {'value': None, 'status': 'missing', 'reason': 'source_missing',
                                 'field_semantics': 'snapshot_pre_match', 'evidence_column': col}
                    stats['field_missing'] += 1
                    missing_by_bm_season.setdefault((season, bm, 'pre'), 0)
                    missing_by_bm_season[(season, bm, 'pre')] += 1
                else:
                    fields[f] = {'value': v, 'status': 'filled',
                                 'field_semantics': 'snapshot_pre_match', 'evidence_column': col}
                    stats['field_filled'] += 1; nfilled += 1
            for f, col in zip(CLO_FIELDS, cols['clo']):
                v = cell_float(row.get(col))
                if v is None:
                    fields[f] = {'value': None, 'status': 'missing', 'reason': 'source_missing',
                                 'field_semantics': 'closing', 'evidence_column': col}
                    stats['field_missing'] += 1
                    missing_by_bm_season.setdefault((season, bm, 'clo'), 0)
                    missing_by_bm_season[(season, bm, 'clo')] += 1
                else:
                    fields[f] = {'value': v, 'status': 'filled',
                                 'field_semantics': 'closing', 'evidence_column': col}
                    stats['field_filled'] += 1; nfilled += 1
            if nfilled == 6:
                stats['full_filled'] += 1
            elif nfilled == 0:
                stats['all_missing'] += 1
            else:
                stats['partial'] += 1
        out.write(json.dumps({
            'record_type': 'fill',
            'fixture_key': fkey,
            'season': season, 'date': date, 'home_team': home, 'away_team': away,
            'bookmaker': bm,
            'fields': fields,
            'source_file': src_file,
            'source_url': src_url,
            'source_sha256': src_sha,
            'retrieved_at': '2026-10-10',
            'provenance': 'football-data.co.uk batch download 2026-10-10; snapshot cols are NOT opening; has_any_opening_col=false',
        }, ensure_ascii=False) + '\n')

print('=== 覆盖统计 ===')
print(json.dumps(stats, ensure_ascii=False, indent=2))
print('--- missing 按(赛季,书商,pre/clo) ---')
for k in sorted(missing_by_bm_season):
    print(k, missing_by_bm_season[k])
print('--- 无FD行 ---', stats['no_fd_row'])
for k in no_row_keys[:20]:
    print(' ', k)
print('--- 队名映射问题 ---', map_problems if map_problems else '无')
print('输出:', OUT, '| 行数(含头):', sum(1 for _ in open(OUT, encoding='utf-8')))
