#!/usr/bin/env python3
"""Q1 odds gap fill: 2020+2021 J1 fixtures missing from odds_evidence_csv.
Source: 捷报网 (live.nowscore.com) 1x2 JS data endpoint https://1x2.NowScore.com/<schedid>.js
Semantics: 初指/即时快照 (NOT true opening, NOT per-tick). 每行带真实 URL + 抓取时间。
Incremental: 每抓完一个日期就落盘一次 work-002/odds-gap-2020-21.csv
"""
import csv, json, re, sys, time, urllib.request
from datetime import datetime, timezone

CN2EN = {'FC东京':'fc_tokyo','东京绿茵':'tokyo_verdy','京都不死鸟':'kyoto_sanga','仙台维加泰':'vegalta_sendai',
'冈山绿雉':'fagiano_okayama','名古屋鲸八':'nagoya_grampus','大分三神':'oita_trinita','大阪樱花':'cerezo_osaka',
'大阪钢巴':'gamba_osaka','川崎前锋':'kawasaki_frontale','广岛三箭':'sanfrecce_hiroshima','德岛漩涡':'tokushima_vortis',
'新泻天鹅':'albirex_niigata','札幌冈萨多':'consadole_sapporo','柏太阳神':'kashiwa_reysol','横滨FC':'yokohama_fc',
'横滨水手':'yokohama_f_marinos','浦和红钻':'urawa_red_diamonds','清水鼓动':'shimizu_s_pulse','湘南海洋':'shonan_bellmare',
'町田泽维亚':'machida_zelvia','磐田喜悦':'jubilo_iwata','神户胜利船':'vissel_kobe','福冈黄蜂':'avispa_fukuoka',
'长崎成功丸':'v_varen_nagasaki','鸟栖沙岩':'sagan_tosu','鹿岛鹿角':'kashima_antlers'}
def cn2en(n):
    n = re.sub(r'\(主\)|\(中\)$', '', n)
    return CN2EN.get(n, n)

TARGETS = [('William Hill','William Hill'), ('Bet 365','bet365'), ('Pinnacle','Pinnacle'), ('Ladbrokes','Ladbrokes')]
HDR = ['date','home_team','away_team','bookmaker','init_1','init_x','init_2','current_1','current_x','current_2',
       'odds_page_url','retrieved_at_utc','semantics_note']
NOTE = '捷报网1x2初指/即时快照，非逐tick，非true opening'
OUT = '/home/hatch/workspace/ai-inbox/repo/work-002/odds-gap-2020-21.csv'
VLOG = '/home/hatch/workspace/ai-inbox/repo/work-002/odds-gap-2020-21.validation.log'

def fetch_js(sid, tries=3):
    url = f'https://1x2.NowScore.com/{sid}.js'
    last = None
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            return urllib.request.urlopen(req, timeout=25).read().decode('utf-8-sig'), url
        except Exception as e:
            last = e; time.sleep(2)
    raise last

def parse_match(raw):
    def var(name):
        m = re.search(r'var '+name+r'="([^"]*)"', raw)
        return m.group(1) if m else ''
    meta = {v: var(v) for v in ['hometeam_cn','guestteam_cn','MatchTime','neutrality','season']}
    start = raw.find('var game=Array('); end = raw.find(');', start)
    entries = re.findall(r'"([^"]+)"', raw[start:end])
    i = raw.find('var gameDetail=Array('); j = raw.find(');', i)
    gd = {}
    if i >= 0:
        for e in re.findall(r'"([^"]+)"', raw[i:j]):
            if '^' in e:
                oid, ticks = e.split('^',1)
                tl = [t for t in ticks.split(';') if t]
                if tl: gd[oid] = tl
    return meta, entries, gd

def main():
    gap = json.load(open('/tmp/gap_mapped.json'))
    gap.sort(key=lambda g: (g['date'], g['home']))
    dates = sorted(set(g['date'] for g in gap))
    # resume: skip dates already in output
    done_dates = set()
    try:
        with open(OUT, newline='', encoding='utf-8') as f:
            for r in csv.DictReader(f): done_dates.add(r['date'])
        print('resume: already done dates:', sorted(done_dates))
    except FileNotFoundError:
        with open(OUT,'w',newline='',encoding='utf-8') as f:
            csv.writer(f).writerow(HDR)
    vlog = open(VLOG,'a',encoding='utf-8')
    unresolved, n_rows, n_match = [], 0, 0
    for d in dates:
        if d in done_dates:
            continue
        day = [g for g in gap if g['date']==d]
        day_rows = []
        for g in day:
            sid = g['sched_id']
            try:
                raw, jsurl = fetch_js(sid)
            except Exception as e:
                unresolved.append({'sched_id':sid,'date':g['date'],'home':g['home'],'away':g['away'],
                                   'reason':f'JS fetch failed after 3 tries: {e}'})
                vlog.write(f"FETCH_FAIL {sid} {g['date']} {g['home']} vs {g['away']}: {e}\n"); vlog.flush()
                time.sleep(1.2); continue
            retrieved = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            meta, entries, gd = parse_match(raw)
            # team sanity check
            h_en, a_en = cn2en(meta['hometeam_cn']), cn2en(meta['away_team_cn'] if False else meta['guestteam_cn'])
            if h_en != g['home'] or a_en != g['away']:
                vlog.write(f"TEAM_MISMATCH {sid}: page {meta['hometeam_cn']}/{meta['guestteam_cn']} vs fixture {g['home']}/{g['away']}\n")
            page_url = f'https://live.nowscore.com/1x2/{sid}.htm'
            # per-page min/max for sanity
            all_init1 = []
            comp_rows = {}
            for e in entries:
                p = e.split('|')
                if len(p) < 22: continue
                en = p[2]
                for src_en, out_en in TARGETS:
                    if en == src_en:
                        init = (p[3],p[4],p[5]); cur = (p[10],p[11],p[12])
                        comp_rows[out_en] = (en, p[1], init, cur, p[20], p[21])
                try: all_init1.append(float(p[3]))
                except: pass
            mn, mx = (min(all_init1), max(all_init1)) if all_init1 else ('?','?')
            for out_en in [t[1] for t in TARGETS]:
                if out_en not in comp_rows:
                    vlog.write(f"COMPANY_MISSING {sid} {g['date']}: {out_en} not on page\n"); continue
                en, oid, init, cur, tm, cn = comp_rows[out_en]
                # gameDetail cross-check: init==oldest tick, cur==newest tick
                if oid in gd:
                    tl = gd[oid]
                    newest = tuple(tl[0].split('|')[:3]); oldest = tuple(tl[-1].split('|')[:3])
                    if tuple(init) != oldest or (cur[0] and tuple(cur) != newest):
                        vlog.write(f"TICK_MISMATCH {sid} {out_en}: game init={init} cur={cur} vs detail oldest={oldest} newest={newest}\n")
                # init/current sanity vs page min/max (detect swap)
                try:
                    if float(init[0]) < mn-0.01 or float(init[0]) > mx+0.01:
                        vlog.write(f"RANGE_WARN {sid} {out_en}: init_1={init[0]} outside page init range [{mn},{mx}]\n")
                except: pass
                day_rows.append([g['date'], meta['hometeam_cn'], meta['guestteam_cn'], out_en,
                                 init[0],init[1],init[2], cur[0],cur[1],cur[2],
                                 page_url, retrieved, NOTE])
                n_rows += 1
            n_match += 1
            time.sleep(1.2)
        with open(OUT,'a',newline='',encoding='utf-8') as f:
            csv.writer(f).writerows(day_rows)
        print(f'date {d}: {len(day)} matches, {len(day_rows)} rows written', flush=True)
        time.sleep(0.5)
    vlog.write(f"RUN_DONE rows={n_rows} matches_ok={n_match} unresolved={len(unresolved)}\n")
    json.dump(unresolved, open('/home/hatch/workspace/ai-inbox/repo/work-002/odds-gap-2020-21.unresolved.json','w'), ensure_ascii=False, indent=1)
    vlog.close()
    print(f'DONE: rows={n_rows} matches={n_match} unresolved={len(unresolved)}')

if __name__ == '__main__':
    main()
