#!/usr/bin/env python3
"""Parse the 3 downloaded CONMEBOL PROGRAMA PDFs (byte-verified) into inventory rows.

Method: pdftotext -layout only (the -raw extraction wraps 2024 team labels
across lines, e.g. 'Colo-Colo16' / 'CHI' on separate lines, so raw lines are
NOT row-complete for 2024; layout lines keep each fixture on one line).
Section order comes from layout section headers; fields come from layout rows:
  <#> <weekday> <date> <city+country+venue segment> <hora> <GMT> <BRA>
  <team A> vs <team B> <Grupo|Llave> <broadcast columns, ignored>
City/country/venue are split from the pre-time segment by the first all-uppercase
3-letter country code token (city names like 'Rio de Janeiro'/'Viña del Mar'
contain no all-uppercase 3-letter token, so this is unambiguous).
A-definir rows are resolved by LAYOUT CHARACTER POSITION (header columns in
the Fase 1/2 PDF: Ciudad=28, Pais=39, Estadio=68, Hora Local=98, GMT=114):
  #9:  A definir at 28 (Ciudad) and 68 (Estadio); Pais blank; Hora Local 18:15.
  #11/#14: A definir at 28 (Ciudad), 68 (Estadio), 99 (Hora Local); Pais blank.
This corrects the previous round's reading (city/country=A definir, venue=null).
No scores/results exist in these schedule PDFs; none are transcribed.
"""
import re, subprocess, json, hashlib, os

W = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(W, 'fixture_evidence')

FILES = [
    ('conmebol_2022_fase12.pdf', 2022, 'Versión de 28/01/2022',
     'https://cdn.conmebol.com/wp-content/uploads/2022/01/Fixture_CONMEBOL-Libertadores-Fase-1-2_-v-28-01-2022.pdf'),
    ('conmebol_2022_fase3.pdf', 2022, 'Versión de 04/03/2022',
     'https://cdn.conmebol.com/wp-content/uploads/2022/03/Fixture_CONMEBOL-Libertadores-Fase-3_01-03-2022-sin-picks.pdf'),
    ('conmebol_2024_qf.pdf', 2024, '26/8/2024 (header date; no "Versión de" wording in this PDF)',
     'https://cdn.conmebol.com/wp-content/uploads/2024/08/Fixture-Libertadores_Cuartos-de-Final_2024.pdf'),
]

MONTHS = {'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6,
          'jul': 7, 'ago': 8, 'sep': 9, 'set': 9, 'oct': 10, 'nov': 11, 'dic': 12}

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def team_b_and_code(team_b_raw, num):
    m = re.match(r'^(E\d+)\s+([A-Z]\d+|S\d+)\b', team_b_raw)
    if m:
        return m.group(1), m.group(2)
    m = re.match(r'^(.+?)\s+([A-Z]\d+|S\d+)\b', team_b_raw)
    assert m, f'team B parse failed #{num}: {team_b_raw!r}'
    return m.group(1), m.group(2)

def norm_ws(s):
    return re.sub(r'\s+', ' ', s).strip()

def attach_seed(label):
    """Join a standalone seed-number token to the preceding token, as printed
    in the PDF text stream (e.g. 'Fluminense 4 BRA' -> 'Fluminense4 BRA').
    The seed number's meaning is NOT interpreted; it is kept verbatim."""
    return re.sub(r'\s(\d{1,2})\s+([A-Z]{3})\b', r'\1 \2', norm_ws(label))

def raw_team_labels_2024(path):
    """Team labels from pdftotext -raw groups (2024 only). In -raw, the seed
    numbers that -layout sometimes drops to a separate line reappear in the
    token stream; attaching them reproduces the printed label. Returns
    {fixture_num: (team_a, team_b, tie_code)}."""
    raw = subprocess.run(['pdftotext', '-raw', path, '-'],
                         capture_output=True, text=True).stdout.splitlines()
    groups = {}
    cur = None
    for line in raw:
        m = re.match(r'(\d+)\s+\S+\s+\d{1,2}-[a-z]{3}\b', line)
        if m:
            cur = int(m.group(1))
            groups[cur] = [line]
        elif cur is not None and not line.startswith('# Dia'):
            groups[cur].append(line)
    out = {}
    for num, lines in groups.items():
        text = norm_ws(' '.join(lines))
        m = re.match(r'^\d+\s+\S+\s+\S+\s+.+?\s+(\d{2}:\d{2})\s+(\d{2}:\d{2})\s+(\d{2}:\d{2})\s+(.+?)\s+vs\s+(.+)$', text)
        assert m, f'raw team parse failed #{num}: {text!r}'
        team_a = attach_seed(m.group(4))
        team_b, code = team_b_and_code(attach_seed(m.group(5)), num)
        out[num] = (team_a, team_b, code)
    return out

rows = []
for fname, year, version, url in FILES:
    path = os.path.join(EV, fname)
    digest = sha256(path)
    layout = subprocess.run(['pdftotext', '-layout', path, '-'],
                            capture_output=True, text=True).stdout.splitlines()
    stage = round_ = None
    for line in layout:
        m = re.search(r'Fase\s+(\d)\s*\((Ida|Vuelta)\)', line)
        if m:
            stage, round_ = f'Fase {m.group(1)}', m.group(2)
            continue
        m = re.search(r'Cuartos de Final\s*-\s*(IDA|VUELTA)', line)
        if m:
            stage, round_ = 'Cuartos de Final', m.group(1)
            continue
        rm = re.match(r'\s*(\d+)\s+(\S+)\s+(\d{2}/\d{2}|\d{1,2}-[a-z]{3})\s+(.*)$', line)
        if not rm or stage is None:
            continue
        num, _wd, date_tok, rest = rm.groups()
        num = int(num)
        if '/' in date_tok:
            dd, mm = date_tok.split('/')
            match_date = f'{year}-{int(mm):02d}-{int(dd):02d}'
        else:
            dd, mon = date_tok.split('-')
            match_date = f'{year}-{MONTHS[mon.lower()]:02d}-{int(dd):02d}'
        if 'A definir' in line:
            city = line[28:39].strip() if len(line) > 28 else None
            venue = line[68:98].strip() if len(line) > 68 else None
            hora_col = line[98:114].strip() if len(line) > 98 else None
            tail = line[114:]
            tm = re.match(r'(\d{2}:\d{2})\s+(\d{2}:\d{2})\s+(.+?)\s+vs\s+(.+)$', tail)
            assert tm, f'A-definir tail parse failed #{num}: {tail!r}'
            gmt, _bra, team_a, team_b_raw = tm.groups()
            team_b, code = team_b_and_code(team_b_raw, num)
            if hora_col == 'A definir':
                kickoff_local, kickoff_note = None, 'Hora Local column reads "A definir" (to be defined)'
            else:
                kickoff_local, kickoff_note = hora_col, None
            country = None
        else:
            m2 = re.match(r'^(.+?)\s+(\d{2}:\d{2})\s+(\d{2}:\d{2})\s+(\d{2}:\d{2})\s+(.+?)\s+vs\s+(.+)$', rest)
            assert m2, f'row parse failed #{num}: {rest!r}'
            segment, hora, gmt, _bra, team_a, team_b_raw = m2.groups()
            m3 = re.match(r'^(.+?)\s+([A-Z]{3})\s+(.+)$', segment)
            assert m3, f'segment parse failed #{num}: {segment!r}'
            city, country, venue = m3.groups()
            team_b, code = team_b_and_code(team_b_raw, num)
            kickoff_local, kickoff_note = hora, None
        team_a = norm_ws(team_a)
        team_b = norm_ws(team_b)
        if stage.startswith('Fase'):
            group_id, tie_id = code, None
        else:
            group_id, tie_id = None, code
        partial = (venue == 'A definir') or (kickoff_local is None)
        rows.append({
            'season_year': year,
            'home_team_source_label': team_a,
            'away_team_source_label': team_b,
            'match_date': match_date,
            'kickoff_local': kickoff_local,
            'kickoff_local_source_text': kickoff_note,
            'kickoff_utc': gmt,
            'kickoff_utc_note': 'GMT column time-of-day string only; source publishes no UTC date, so do NOT combine with match_date.',
            'source_timezone_text': None,
            'timezone_note': 'Source labels the local column only as "Hora Local" with no timezone name/offset; GMT column is a second time column, not a timezone label for the local time.',
            'official_stage': stage,
            'official_round': round_,
            'group_id': group_id,
            'tie_id': tie_id,
            'source_fixture_id': num,
            'source_fixture_id_scope': 'within this phase PDF document only; NOT assumed globally unique',
            'venue_or_stadium': venue,
            'city': city,
            'country': country,
            'source_id': 'SRC-CONMEBOL-PROGRAMA',
            'source_url': url,
            'final_url': url,
            'http_status': 200,
            'retrieved_at': '2026-10-23T21:23:00+08:00',
            'retrieval_method': 'curl byte download',
            'field_locator': f'PDF PROGRAMA DE PARTIDOS, {stage} ({round_}) section, row #{num}',
            'source_sha256': digest,
            'evidence_file': fname,
            'document_version': version,
            'status': 'partial' if partial else 'complete',
        })

# 2024: recover seed numbers from the -raw token stream (see raw_team_labels_2024).
# Layout parsing alone drops them for #144/#146/#149, where pdftotext puts
# the seed digit on a separate line; raw labels must agree with layout labels
# once seed digits and whitespace are stripped, otherwise the row is flagged.
_raw_2024 = raw_team_labels_2024(os.path.join(EV, 'conmebol_2024_qf.pdf'))
def _strip_seed(s):
    return re.sub(r'(\D)\d{1,2}\s+([A-Z]{3})\b', r'\1 \2', s)
for _r in rows:
    if _r['season_year'] != 2024:
        continue
    _ta, _tb, _code = _raw_2024[_r['source_fixture_id']]
    assert _code == _r['tie_id'], f"tie mismatch #{_r['source_fixture_id']}: {_code} vs {_r['tie_id']}"
    assert _strip_seed(_ta) == _strip_seed(_r['home_team_source_label']), \
        f"team A mismatch #{_r['source_fixture_id']}: raw={_ta!r} layout={_r['home_team_source_label']!r}"
    assert _strip_seed(_tb) == _strip_seed(_r['away_team_source_label']), \
        f"team B mismatch #{_r['source_fixture_id']}: raw={_tb!r} layout={_r['away_team_source_label']!r}"
    _r['home_team_source_label'], _r['away_team_source_label'] = _ta, _tb
    _r['team_label_note'] = ('Team label includes the seed number as printed '
                             '(e.g. Flamengo11); its meaning is not interpreted.')

rows.sort(key=lambda r: (r['season_year'], r['source_fixture_id']))
with open(os.path.join(W, 'conmebol_inventory.jsonl'), 'w') as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print('rows:', len(rows))
from collections import Counter
print(Counter((r['season_year'], r['official_stage'], r['official_round']) for r in rows))
print('partial:', [(r['source_fixture_id'], r['city'], r['country'], r['venue_or_stadium'], r['kickoff_local']) for r in rows if r['status'] == 'partial'])
print('hashes:', sorted(set(r['source_sha256'] for r in rows)))
