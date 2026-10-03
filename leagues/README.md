# 联赛画像（leagues/）——Codex 发单前必读

## 这是什么
每个联赛一个 `<league_key>.profile.json`，收敛该联赛的全部差异：
赛季范围、源优先级链、已知的坑（quirks）、已完成的（done）、还缺的（known_gaps）。

## 发单规则
1. 发单前先读对应画像，按它的 source_chain 顺序找数，不要自己发明顺序。
2. 任务拆到最小独立单元：`(联赛 × 赛季 × 任务类型)` 一个请求一个 id。
   反面教材：req-20261002-002 把 2670 场+Q1–Q4 塞一个单，一个子项卡住整单 19 小时。
3. 新单只发缺口（`incremental_only`），不重发已完成的。
4. 每个请求的 `scope` 必须带 `competition_key` + `seasons`（矩阵脚本靠这个汇总）。
5. 画像里未知项写 `TODO`，不许编；补上后更新画像。
6. 熔断规则：同一请求连续 3 轮接手无实质进展 → 停手并预警用户，不静默空转。

## 完成度矩阵
跑 `bin/league-matrix.py`（`--write` 则写入 `leagues/MATRIX.md`），一眼看各联赛各赛季缺什么。
