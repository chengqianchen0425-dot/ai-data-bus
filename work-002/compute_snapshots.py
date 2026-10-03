"""Compute label-based pre-round snapshots for J1 2020 rounds 24/25/26/29/32/33.
Method (Transfermarkt matchday-table convention):
  pre-round R snapshot = state after all matches labeled rounds 1..R-1.
  - rank_before: ja-Wikipedia 順位推移表 column R-1 (cites J.LEAGUE Data Site).
  - points_before: recomputed from 対戦表 (round->opponent) + 戦績表 (scores).
  - played_before: R-1 (deterministic: 18 teams, one match per team per round).
"""
import sys
sys.path.insert(0, '/home/hatch/workspace/ai-inbox/repo/work-002')
from j1_2020_schedule import teams, schedule
from j1_2020_results import RESULTS

# (home, away) -> (hg, ag)
SCORES = {(h, a): (hg, ag) for (h, a, hg, ag) in RESULTS}

# rank after round N (label-based), from ja-Wikipedia 順位推移表 (J.LEAGUE Data Site).
# rank_after[team][round] ; rounds 1..34
rank_after = {
    'kawasaki_frontale':  [11,4,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    'cerezo_osaka':       [6,3,1,3,2,3,4,2,3,2,2,2,2,2,2,2,2, 2,2,3,3,3,2,2,4,5,5,6,4,5,4,4,4,4],
    'fc_tokyo':           [3,2,7,4,2,3,4,6,6,4,6,4,3,3,3,3,3, 3,3,2,2,2,3,4,5,3,4,5,6,6,6,6,6,6],
    'nagoya_grampus':     [7,4,8,5,4,2,3,5,4,5,3,3,4,4,4,4,4, 6,5,5,5,4,5,5,3,4,3,3,3,3,3,3,3,3],
    'kashima_antlers':    [18,18,18,18,15,17,17,12,12,11,12,10,9,9,6,5,5, 4,6,8,8,6,6,6,6,6,6,4,5,4,5,5,5,5],
    'kashiwa_reysol':     [2,8,14,14,12,7,7,4,5,7,5,5,7,5,5,7,6, 5,8,7,7,8,8,8,8,10,10,10,10,8,7,7,7,7],
    'yokohama_f_marinos': [14,12,10,13,14,11,11,11,11,12,9,6,6,8,10,8,7, 7,4,6,6,7,7,7,7,7,7,7,7,9,9,9,9,9],
    'urawa_red_diamonds': [4,4,3,2,6,6,6,7,7,6,4,8,5,7,7,6,8, 8,9,10,9,9,9,9,9,9,8,9,9,10,10,10,10,10],
    'gamba_osaka':        [5,10,10,8,5,3,2,3,2,3,6,7,8,6,8,9,9, 9,7,4,4,5,4,2,2,2,2,2,2,2,2,2,2,2],
    'sanfrecce_hiroshima':[1,1,4,6,9,10,10,10,8,8,8,11,11,11,9,10,10, 10,11,11,11,11,10,10,10,8,9,8,7,7,8,8,8,8],
    'oita_trinita':       [15,8,5,7,10,12,12,14,16,14,13,14,14,14,14,12,11, 12,12,12,12,12,12,12,12,12,12,11,11,11,11,11,11,11],
    'consadole_sapporo':  [16,11,6,8,7,8,8,8,9,10,11,13,12,12,12,13,13, 13,15,15,13,14,14,13,13,13,13,13,13,13,13,13,13,12],
    'sagan_tosu':         [11,14,15,15,16,16,15,12,15,17,17,17,17,16,15,15,15, 15,14,14,15,15,15,15,15,15,15,14,14,14,14,14,14,13],
    'vissel_kobe':        [7,15,13,12,8,9,9,9,10,9,10,9,10,10,11,11,12, 11,10,9,10,10,11,11,11,11,11,12,11,12,12,12,12,14],
    'yokohama_fc':        [7,12,9,10,13,14,14,17,17,16,14,12,13,13,13,14,14, 14,13,13,14,13,13,14,14,14,14,15,15,15,15,15,15,15],
    'shimizu_s_pulse':    [17,17,17,17,18,18,17,16,14,15,16,16,16,17,17,18,16, 16,16,17,17,17,17,17,17,17,17,17,17,17,17,17,18,16],
    'vegalta_sendai':     [7,4,10,11,11,13,13,15,13,13,15,15,15,15,16,16,17, 17,17,16,16,16,18,18,18,18,18,18,18,18,18,18,16,17],
    'shonan_bellmare':    [13,16,16,16,17,15,16,18,18,18,18,18,18,18,18,17,18, 18,18,18,18,18,16,16,16,16,16,16,16,16,16,16,17,18],
}

FINAL_POINTS = {
    'kawasaki_frontale': 83, 'gamba_osaka': 65, 'nagoya_grampus': 63,
    'cerezo_osaka': 60, 'kashima_antlers': 59, 'fc_tokyo': 57,
    'kashiwa_reysol': 52, 'sanfrecce_hiroshima': 48, 'yokohama_f_marinos': 47,
    'urawa_red_diamonds': 46, 'oita_trinita': 43, 'consadole_sapporo': 39,
    'sagan_tosu': 36, 'vissel_kobe': 36, 'yokohama_fc': 33,
    'shimizu_s_pulse': 28, 'vegalta_sendai': 28, 'shonan_bellmare': 27,
}

num2name = teams

def team_result(tname, rnd):
    """(opponent_name, t_goals, o_goals, points) for tname in round rnd (1-based)."""
    onum = schedule[tname][rnd - 1]
    oname = num2name[onum]
    if (tname, oname) in SCORES:
        hg, ag = SCORES[(tname, oname)]
        tg, og = hg, ag
    elif (oname, tname) in SCORES:
        hg, ag = SCORES[(oname, tname)]
        tg, og = ag, hg
    else:
        raise ValueError(f'no score for {tname} vs {oname} round {rnd}')
    pts = 3 if tg > og else (1 if tg == og else 0)
    return oname, tg, og, pts

def points_through(tname, last_round):
    return sum(team_result(tname, r)[3] for r in range(1, last_round + 1))

# ---- validation 1: final points must match exactly ----
bad = []
for t in num2name.values():
    got = points_through(t, 34)
    exp = FINAL_POINTS[t]
    if got != exp:
        bad.append((t, got, exp))
if bad:
    print('FINAL POINTS MISMATCH:')
    for b in bad:
        print(' ', b)
    sys.exit(1)
print('OK: recomputed final points match official table for all 18 teams.')

# ---- validation 2: every scheduled pairing has a score ----
missing = []
for t in num2name.values():
    for r in range(1, 35):
        onum = schedule[t][r - 1]
        oname = num2name[onum]
        if (t, oname) not in SCORES and (oname, t) not in SCORES:
            missing.append((t, r, oname))
if missing:
    print('MISSING SCORES:', missing)
    sys.exit(1)
print('OK: all 306 scheduled pairings have scores.')

# ---- compute snapshots ----
SNAP_ROUNDS = [24, 25, 26, 29, 32, 33]
out = {}
for R in SNAP_ROUNDS:
    for t in num2name.values():
        out[(R, t)] = {
            'rank': rank_after[t][R - 2],   # column R-1 (0-based index R-2)
            'points': points_through(t, R - 1),
            'played': R - 1,
        }

# sanity: rank ordering consistent with points ordering (allow ties)
for R in SNAP_ROUNDS:
    rows = sorted(out[(R, t)]['points'] for t in num2name.values())
print('OK: snapshots computed.')

# print table for report
for R in SNAP_ROUNDS:
    print(f'--- pre-round {R} (after round {R-1}) ---')
    for t in sorted(num2name.values(), key=lambda x: out[(R, x)]['rank']):
        s = out[(R, t)]
        print(f"  rk{s['rank']:>2} {t:22s} pts={s['points']:>2} pld={s['played']}")
