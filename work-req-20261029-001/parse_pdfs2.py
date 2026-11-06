import json, re
from collections import Counter

d007 = json.load(open('/home/hatch/workspace/ai-inbox/repo/responses/req-20261003-007.json'))['data']
rows007 = d007['rows']
off2fd = {}
offnames = set()
for r in rows007:
    off2fd[r['source_home_team']] = r['home_team']
    off2fd[r['source_away_team']] = r['away_team']
    offnames.add(r['source_home_team']); offnames.add(r['source_away_team'])
offnames = sorted(offnames, key=len, reverse=True)
key007 = {(r['match_date'], r['home_team'], r['away_team']): r for r in rows007}

def parse_txt(path):
    out = []
    for ln in open(path, encoding='utf-8', errors='ignore'):
        m = re.match(r'\s*(\d{2})\.(\d{2})\.(\d{4})\s*-\s*[A-Za-z]{2}\s+(\d{2})[.:](\d{2})\s+(\d{1,2})\s+\d+\s+(.*)$', ln)
        if not m:
            continue
        dd, mo, yy, hh, mm, rnd, rest = m.groups()
        rest = rest.strip()
        home = away = None
        for name in offnames:
            if rest.startswith(name):
                home = name
                away = rest[len(name):].strip()
                break
        if home is None or not away:
            out.append({'date': f'{dd}/{mo}/{yy}', 'kickoff': f'{hh}:{mm}', 'round': int(rnd),
                        'home_off': None, 'away_off': None, 'raw': ln.rstrip(), 'parse_fail': True})
            continue
        out.append({'date': f'{dd}/{mo}/{yy}', 'kickoff': f'{hh}:{mm}',
                    'round': int(rnd), 'home_off': home, 'away_off': away, 'raw': ln.rstrip()})
    return out

files = {'1-6': 'Bundesliga_2018-19_Spieltage_1-6.txt', '7-14': 'Bundesliga_2018-19_Spieltage_7-14.txt',
         '15-21': 'Bundesliga_2018-19_Spieltage_15-21-1.txt', '22-28': 'BL-MD-22-28.txt',
         '29-34': 'Bundesliga_Spieltage_29-34.txt'}
allpdf = []
for label, f in files.items():
    rs = parse_txt(f)
    fails = [r for r in rs if r.get('parse_fail')]
    print(label, 'rows:', len(rs), 'parse_fail:', len(fails), 'per-round:', sorted(Counter(r['round'] for r in rs).items()))
    for r in fails: print('   FAIL:', r['raw'])
    allpdf.extend(rs)
print('TOTAL:', len(allpdf), 'dups:', len(allpdf)-len(set((r['date'], r['home_off'], r['away_off']) for r in allpdf if r['home_off'])))

diffs, unmatched = [], []
for r in allpdf:
    if r.get('parse_fail'):
        unmatched.append((r, 'parse fail')); continue
    fh, fa = off2fd.get(r['home_off']), off2fd.get(r['away_off'])
    if fh is None or fa is None:
        unmatched.append((r, 'unknown official name')); continue
    b = key007.get((r['date'], fh, fa))
    if b is None:
        unmatched.append((r, 'no -007 row')); continue
    if b['round'] != r['round'] or b['kickoff_local'] != r['kickoff']:
        diffs.append({'pdf': r, '007': b})
print('unmatched:', len(unmatched))
for r, w in unmatched: print('  ', r.get('date'), r.get('home_off'), 'vs', r.get('away_off'), '|', w)
print('diffs:', len(diffs))
for x in diffs: print('  ', x)

pdfkeys = set()
for r in allpdf:
    if r.get('home_off'):
        pdfkeys.add((r['date'], off2fd[r['home_off']], off2fd[r['away_off']]))
missing = [b for b in rows007 if (b.get('official_match_date') or b['match_date'], b['home_team'], b['away_team']) not in pdfkeys]
print('missing-in-pdf (official date):', len(missing))
for b in missing: print('  ', b['fixture_key'], b['round'], b['kickoff_local'])
json.dump({'pdf_rows': allpdf, 'diffs': diffs,
           'unmatched': [{'row': r, 'why': w} for r, w in unmatched],
           'missing_in_pdf': missing}, open('pdf_vs_007.json', 'w'), ensure_ascii=False, indent=1)
