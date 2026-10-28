#!/usr/bin/env python3
"""B-road validation: -004 rows (2019-2021) vs FBref overlays."""
import json, collections, sys

BASE = "/home/hatch/workspace/ai-inbox/work-req-20261028-002/evidence/"
D004 = json.load(open("/home/hatch/workspace/ai-inbox/repo/work-req-20261006-004/req-20261006-004-rows.json"))["rows"]

NORM = {
    "KuPS": "Kuopion PS", "SJK": "SJK Seinäjoki", "Lahti": "FC Lahti",
    "Ilves": "Ilves Tampere", "FC Inter": "Inter Turku", "Haka": "Haka Valkeakoski",
    "Helsinki IFK": "Helsingfors IFK", "RoPS": None,  # season-dependent
    "KPV": "KPV Kokkola", "VPS": "Vaasan PS", "TPS": "TPS Turku",
}
VENUE_ALIAS = {
    "Telia 5G -areena": "Bolt Arena", "Savon Sanomat Areena": "Väre Areena",
    "Raatin stadion": "Raatin Stadion", "Ratinan Stadion": "Ratinan stadion",
    "Kokkolan Keskuskenttä": "Kokkolan keskuskenttä",
    "Lahden Stadion": "Lahden Stadion", "Tapiolan Urheilupuisto": "Tapiolan Urheilupuisto",
    "OmaSP Stadion": "OmaSP Stadion", "Veritas Stadion": "Veritas Stadion",
    "Wiklöf Holding Arena": "Wiklöf Holding Arena", "Arto Tolsa Areena": "Arto Tolsa Areena",
    "Tehtaan kenttä": "Tehtaan kenttä", "Elisa Stadion": "Elisa Stadion",
    "Rovaniemen Keskuskenttä": "Rovaniemen keskuskenttä", "Tammelan Stadion": "Tammelan Stadion",
    "Kisapuisto": "Kisapuisto",
}

def norm_team(fb, season):
    if fb == "RoPS":
        return "Rovaniemi PS" if season == "2019" else "Rovaniemen PS"
    return NORM.get(fb, fb)

def load_overlay(season):
    out = []
    for ln in open(f"{BASE}fbref_{season}_overlay.jsonl"):
        ln = ln.strip()
        if ln:
            out.append(json.loads(ln))
    return out

def mins(t):
    h, m = t.split(":")
    return int(h) * 60 + int(m)

for season in ("2019", "2020", "2021"):
    rows = [r for r in D004 if str(r["season"]) == season]
    ov = load_overlay(season)
    print(f"===== {season}: -004 rows={len(rows)} overlay rows={len(ov)}")
    # index overlay by (date, home, away) and by (home, away)
    by_key, by_pair = {}, collections.defaultdict(list)
    for o in ov:
        h = norm_team(o["h"], season); a = norm_team(o["a"], season)
        by_key[(o["d"], h, a)] = o
        by_pair[(h, a)].append(o)
    matched, unmatched_rows, used = [], [], set()
    date_conflicts = []
    for r in rows:
        if r["date"] is None:
            cands = by_pair[(r["home_team"], r["away_team"])]
            if len(cands) == 1:
                matched.append((r, cands[0], "date-null-match"))
                used.add(id(cands[0]))
            else:
                unmatched_rows.append((r["fixture_key"], f"date-null, {len(cands)} pair candidates"))
        else:
            o = by_key.get((r["date"], r["home_team"], r["away_team"]))
            if o is not None:
                matched.append((r, o, "exact"))
                used.add(id(o))
            else:
                # team-pair fallback (date conflict candidate)
                cands = by_pair[(r["home_team"], r["away_team"])]
                if len(cands) == 1:
                    matched.append((r, cands[0], "DATE-CONFLICT"))
                    used.add(id(cands[0]))
                    date_conflicts.append((r["fixture_key"], r["date"], cands[0]["d"]))
                else:
                    unmatched_rows.append((r["fixture_key"], f"no date match, {len(cands)} pair candidates"))
    unused = [o for o in ov if id(o) not in used]
    print(f"matched={len(matched)} unmatched_rows={len(unmatched_rows)} unused_overlay={len(unused)}")
    for k, why in unmatched_rows: print("  UNMATCHED ROW:", k, why)
    for o in unused: print("  UNUSED OVERLAY:", o)
    for fk, d004, dfb in date_conflicts: print("  DATE CONFLICT:", fk, "-004", d004, "FBref", dfb)

    # Wk group completeness (regular season only: s is None)
    if season in ("2020", "2021"):
        groups = collections.defaultdict(list)
        for r, o, _ in matched:
            if o["s"] is None:
                groups[o["w"]].append((r, o))
        print(f"  regular Wk groups: {sorted(groups.keys())}")
        for w in sorted(groups):
            teams = []
            for r, o in groups[w]:
                teams += [norm_team(o["h"], season), norm_team(o["a"], season)]
            dup = [t for t, c in collections.Counter(teams).items() if c > 1]
            print(f"    Wk {w}: n={len(groups[w])} distinct={len(set(teams))} dups={dup}")
    # series mapping check
    for r, o, _ in matched:
        if o["s"] is not None and o["w"] is not None:
            expect = str(22 + o["w"])
            if str(r.get("official_round")) != expect:
                print(f"  SERIES MISMATCH: {r['fixture_key']} -004 round={r.get('official_round')} FBref 22+Wk={expect}")
    # 2020 round equivalence
    if season == "2020":
        eq = neq = 0
        for r, o, _ in matched:
            if r.get("official_round") is not None:
                if int(r["official_round"]) == o["w"]: eq += 1
                else:
                    neq += 1
                    print(f"  ROUND DIFF: {r['fixture_key']} -004={r['official_round']} FBref Wk={o['w']}")
        print(f"  2020 -004 round == FBref Wk: {eq} equal, {neq} differ")
    # kickoff diff distribution
    diffs = collections.Counter()
    exceptions = []
    for r, o, _ in matched:
        if r.get("kickoff") is None:
            diffs["004-null-filled"] += 1
        else:
            d = mins(o["t"]) - mins(r["kickoff"])
            diffs[d] += 1
            if d != 120:
                exceptions.append((r["fixture_key"], r["kickoff"], o["t"], d))
    print(f"  kickoff diff (FBref - -004 minutes): {dict(diffs)}")
    for e in exceptions: print("    KICKOFF EXCEPTION:", e)
    # venue diff
    vdiff = collections.Counter()
    vrows = []
    for r, o, _ in matched:
        canon = VENUE_ALIAS.get(o["v"], o["v"])
        old = r.get("venue")
        if o["v"] == old:
            vdiff["exact-same"] += 1
        elif canon == old:
            vdiff["alias-only"] += 1
            vrows.append((r["fixture_key"], old, o["v"], "alias"))
        else:
            vdiff["DIFFERENT"] += 1
            vrows.append((r["fixture_key"], old, o["v"], "DIFF"))
    print(f"  venue diff: {dict(vdiff)}")
    for v in vrows: print("    VENUE DIFF:", v)
