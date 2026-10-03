#!/usr/bin/env python3
"""联赛完成度矩阵：汇总 requests/responses，按联赛分组输出 Markdown 表格。
用法: league-matrix.py [--write]   # 默认打印到 stdout；--write 写入 leagues/MATRIX.md
审计数字为 best-effort 汇总（递归累加 audit 里 complete/missing 数值字段）。
"""
import json
import os
import sys
import time

REPO = os.path.expanduser("~/workspace/ai-inbox/repo")
STALL_SECS = 900


def sum_fields(obj, keys):
    total = {k: 0 for k in keys}
    found = {k: False for k in keys}
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in keys and isinstance(v, (int, float)) and not isinstance(v, bool):
                    total[k] += v
                    found[k] = True
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    return {k: (total[k] if found[k] else "") for k in keys}


def main():
    write = "--write" in sys.argv
    req_dir = os.path.join(REPO, "requests")
    res_dir = os.path.join(REPO, "responses")
    now = time.time()
    by_league = {}
    for fn in sorted(os.listdir(req_dir)):
        if not fn.endswith(".json"):
            continue
        rid = fn[:-5]
        try:
            q = json.load(open(os.path.join(req_dir, fn)))
        except Exception:
            continue
        scope = q.get("scope") or {}
        league = scope.get("competition_key", "?")
        seasons = scope.get("seasons") or ["?"]
        seasons_s = ", ".join(str(s).replace("/", "-") for s in seasons)
        rtype = q.get("type", "?")
        tgt = q.get("target", "muse")
        rp = os.path.join(res_dir, fn)
        status, upd, agg = "no-response", "", {"complete": "", "missing": ""}
        if os.path.exists(rp):
            try:
                r = json.load(open(rp))
                status = r.get("status", "?")
                mt = os.path.getmtime(rp)
                upd = time.strftime("%m-%d %H:%M", time.localtime(mt))
                if status == "processing" and now - mt > STALL_SECS:
                    status += " [stalled]"
                agg = sum_fields((r.get("data") or {}).get("audit"), ("complete", "missing"))
            except Exception:
                status = "read-error"
        by_league.setdefault(league, []).append(
            (seasons_s, rid, rtype, tgt, status, agg["complete"], agg["missing"], upd))

    out = ["# 联赛完成度矩阵", "", "_自动生成：`bin/league-matrix.py --write`；审计数字为 best-effort 汇总_", ""]
    for league in sorted(by_league):
        out += ["## " + league, "",
                "| 赛季 | 请求 | 类型 | lane | 状态 | complete | missing | 更新 |",
                "|---|---|---|---|---|---|---|---|"]
        for seasons_s, rid, rtype, tgt, status, c, m, upd in by_league[league]:
            out.append(f"| {seasons_s} | {rid} | {rtype} | {tgt} | {status} | {c} | {m} | {upd} |")
        out.append("")
    text = "\n".join(out)
    if write:
        p = os.path.join(REPO, "leagues", "MATRIX.md")
        open(p, "w").write(text + "\n")
        print("wrote " + p)
    else:
        print(text)


if __name__ == "__main__":
    main()
