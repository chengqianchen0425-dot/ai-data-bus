"""Transcribed from ja-Wikipedia 2020 J1 League 対戦表 (matchup table), lines 425-507.
Each team's list = opponent NUMBER (by 2019 rank) for rounds 1..34.
Source: https://ja.wikipedia.org/wiki/2020%E5%B9%B4%E3%81%AEJ1%E3%83%AA%E3%83%BC%E3%82%B0 (cites J.LEAGUE Data Site)
NOTE: Yokohama FC round 3 was '16' in Wikipedia but reciprocity check proves it must be
'17' (Kashiwa row has round 3 = 18 = Yokohama FC). Corrected here.
"""
teams = {
    1: 'yokohama_f_marinos',
    2: 'fc_tokyo',
    3: 'kashima_antlers',
    4: 'kawasaki_frontale',
    5: 'cerezo_osaka',
    6: 'sanfrecce_hiroshima',
    7: 'gamba_osaka',
    8: 'vissel_kobe',
    9: 'oita_trinita',
    10: 'consadole_sapporo',
    11: 'vegalta_sendai',
    12: 'shimizu_s_pulse',
    13: 'nagoya_grampus',
    14: 'urawa_red_diamonds',
    15: 'sagan_tosu',
    16: 'shonan_bellmare',
    17: 'kashiwa_reysol',
    18: 'yokohama_fc',
}

# opponent numbers for rounds 1..34 (index 0 = round 1)
schedule = {
    'yokohama_f_marinos': [7,14,16,2,3,18,10,11,17,9,12,6,8,4,13,5,15,
                            11,17,8,9,7,5,12,15,16,14,2,10,4,3,6,13,18],
    'fc_tokyo':           [12,17,4,1,14,10,3,15,5,13,6,16,7,9,18,8,11,
                            5,15,16,7,12,18,9,4,3,13,1,14,17,6,11,10,8],
    'kashima_antlers':    [6,4,10,14,1,16,2,9,15,8,18,7,17,13,11,12,5,
                            16,9,7,18,15,10,6,13,2,4,11,17,14,1,12,8,5],
    'kawasaki_frontale':  [15,3,2,17,18,11,16,7,9,10,5,13,12,1,8,6,14,
                            18,16,5,11,6,13,8,2,10,3,9,7,1,12,15,14,17],
    'cerezo_osaka':       [9,7,12,13,6,8,15,16,2,17,4,11,18,14,10,1,3,
                            2,11,4,13,16,1,14,8,7,12,6,9,18,10,17,15,3],
    'sanfrecce_hiroshima':[3,8,9,15,5,7,13,18,16,14,2,1,11,10,12,4,17,
                            9,7,15,12,4,8,3,11,14,18,5,16,10,2,1,17,13],
    'gamba_osaka':        [1,5,13,12,9,6,8,4,18,15,14,3,2,11,17,16,10,
                            13,6,3,2,1,9,17,10,5,11,14,4,15,16,8,18,12],
    'vissel_kobe':        [18,6,15,9,12,5,7,10,11,3,17,14,1,16,4,2,13,
                            15,10,1,17,9,6,4,5,12,16,18,13,11,14,7,3,2],
    'oita_trinita':       [5,15,6,8,7,13,12,3,4,1,10,17,14,2,16,11,18,
                            6,3,12,1,8,7,2,14,18,17,4,5,13,11,10,16,15],
    'consadole_sapporo':  [17,18,3,16,11,2,1,8,12,4,9,15,13,6,5,14,7,
                            17,8,11,16,13,3,18,7,4,15,12,1,6,5,9,2,14],
    'vegalta_sendai':     [13,16,14,18,10,4,17,1,8,12,15,5,6,7,3,9,2,
                            1,5,10,4,18,14,13,6,17,7,3,15,8,9,2,12,16],
    'shimizu_s_pulse':    [2,13,5,7,8,15,9,14,10,11,1,18,4,17,6,3,16,
                            14,13,9,6,2,15,1,17,8,5,10,18,16,4,3,11,7],
    'nagoya_grampus':     [11,12,7,5,15,9,6,17,14,2,16,4,10,3,1,18,8,
                            7,12,14,5,10,4,11,3,15,2,16,8,9,17,18,1,6],
    'urawa_red_diamonds': [16,1,11,3,2,17,18,12,13,6,7,8,9,5,15,10,4,
                            12,18,13,15,17,11,5,9,6,1,7,2,3,8,16,4,10],
    'sagan_tosu':         [4,9,8,6,13,12,5,2,3,7,11,10,16,18,14,17,1,
                            8,2,6,14,3,12,16,1,13,10,17,11,7,18,4,5,9],
    'shonan_bellmare':    [14,11,1,10,17,3,4,5,6,18,13,2,15,8,9,7,12,
                            3,4,2,10,5,17,15,18,1,8,13,6,12,7,14,9,11],
    'kashiwa_reysol':     [10,2,18,4,16,14,11,13,1,5,8,9,3,12,7,15,6,
                            10,1,18,8,14,16,7,12,11,9,15,3,2,13,5,6,4],
    # Wikipedia had 16 at round 3; corrected to 17 per reciprocity (Kashiwa r3 = 18).
    'yokohama_fc':        [8,10,17,11,4,1,14,6,7,16,3,12,5,15,2,13,9,
                            4,14,17,3,11,2,10,16,9,6,8,12,5,15,13,7,1],
}

if __name__ == '__main__':
    # Reciprocity check: if T plays O in round r, O must play T in round r.
    errors = []
    for tname, opps in schedule.items():
        tnum = {v: k for k, v in teams.items()}[tname]
        assert len(opps) == 34, (tname, len(opps))
        for i, onum in enumerate(opps):
            r = i + 1
            oname = teams[onum]
            back = schedule[oname][i]
            if back != tnum:
                errors.append((r, tname, oname, back, tnum))
    # Each team plays each other exactly once in rounds 1-17 and 18-34
    for tname, opps in schedule.items():
        tnum = {v: k for k, v in teams.items()}[tname]
        first = opps[:17]
        second = opps[17:]
        if sorted(first) != sorted(set(first)) or tnum in first:
            errors.append(('dup1', tname, first))
        if sorted(second) != sorted(set(second)) or tnum in second:
            errors.append(('dup2', tname, second))
        if set(first) | {tnum} != set(range(1, 19)):
            errors.append(('miss1', tname, sorted(set(first))))
        if set(second) | {tnum} != set(range(1, 19)):
            errors.append(('miss2', tname, sorted(set(second))))
    if errors:
        print('ERRORS:')
        for e in errors:
            print(' ', e)
    else:
        print('OK: schedule reciprocal and complete (34 rounds, home/away halves clean).')
