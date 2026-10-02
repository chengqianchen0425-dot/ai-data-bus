# Q1 赔率缺口（2022+2023 赛季）浏览器抓取委托规格

目标：补齐 J1 2022、2023 赛季逐场 1x2 赔率证据，写入 `work-002/odds-gap-2022-23.csv`
（schema 与 `responses/req-20261002-002.json` 内 `data.odds_evidence_csv` 完全一致）。

## 工作清单（已备好，直接可用）
- `work-002/gap-manifest-2022-23.csv`：603 场缺口 fixture（season,round,stable_key,date_jst,
  home_en,away_en,home_zh_best_effort,away_zh_best_effort），148 个比赛日（2022-02-19 至 2023-12-03）
- `work-002/gap-dates-2022-23.txt`：148 个缺口日期，一行一个
- `work-002/odds-gap-2022-23.csv`：目标文件，表头已写好，**每抓完一个日期就增量 append 落盘一次**

已覆盖（跳过，不要重复抓）：2022-02-18（1 场）、2022-05-21（8 场）——行已在 responses 内。

## 抓取路线（需真浏览器，JS 渲染）
1. 捷报网单场 1x2 页：`https://live.nowscore.com/1x2/<matchid>.htm`
   （样本：`https://live.nowscore.com/1x2/1496605.htm` = 2018-02-23 鸟栖沙岩 vs 神户胜利船）
2. 2022/2023 赛季的 matchid 未知：从捷报网日职联 2022/2023 赛程页逐场点进，
   或按日期在"百家欧指"列表页定位。**未找到"按日聚合"的 1x2 页面 URL 规律**（已搜索，无结果），
   按单场页逐场抓是确定可行的路线。
3. 每页等表格渲染完后提取每家公司两行：初指（第一子行）、即时（第二子行）。

## 字段规则
- 公司名映射：页面 `威*`/`威廉希尔` → `William Hill`；`36*` → `bet365`；
  `Pinna*`/`平博` → `Pinnacle`；Ladbrokes 等其他公司原样保留页面名。
- `init_*` = 初指，`current_*` = 即时；用页面底部"初指最高/最低、即时最高/最低"行交叉验证无反转。
- `odds_page_url` = 实际抓取的单场 URL（必须真实）；`retrieved_at_utc` = 实际抓取时间的 UTC ISO
 （如 `2026-10-02T10:30:00Z`）；`semantics_note` 统一写
  `捷报网1x2初指/即时快照，非逐tick，非true opening`。
- 允许与 responses 已有行重复（合并时去重）；不要因怕重复而跳过整场。
- 铁律：说不清来源的行不要；禁止猜测；**禁止把 closing 标成 opening**。

## 备选源
单源卡住 3–5 分钟标记 failed 换源：betexplorer 单场页（opening/closing 语义与捷报网不同，
`semantics_note` 必须如实改写，如 `betexplorer opening/closing快照`），或 nowscore 其他镜像。
语义必须如实标注，不得混写。

## 审计口径
- expected：603 场 → 约 1809 行（每场 William Hill + bet365 + Pinnacle 三行；Ladbrokes 仅 2018 数据有，2022/23 未知）
- 完成后报告：实际写入行数、distinct(date,home,away) 新增场数、完成的日期范围、
  剩余未抓日期清单及逐条原因、expected/discovered/complete/partial/missing
