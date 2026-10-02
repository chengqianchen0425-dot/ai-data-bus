# Q1 赔率缺口（2018+2019 赛季）浏览器抓取委托规格

目标：补齐 J1 2018、2019 赛季逐场 1x2 赔率证据，写入 `work-002/odds-gap-2018-19.csv`
（schema 与 `responses/req-20261002-002.json` 内 `data.odds_evidence_csv` 完全一致）。

## 缺口结论（已用 fixture 级精度核实）
- 2018：306/306 场已覆盖（按 date+中英文球队名逐场核对，含"磐田喜悦(中)"中立场变体）——**无需再抓**。
- 2019：0/306 场覆盖，72 个比赛日全部缺失（2019-02-22 至 2019-12-07）。

## 工作清单（已备好，直接可用）
- `work-002/gap-manifest-2018-19.csv`：306 场缺口 fixture（season,round,stable_key,date_jst,
  home_en,away_en,home_zh_best_effort,away_zh_best_effort），72 个比赛日
- `work-002/gap-dates-2018-19.txt`：72 个缺口日期，一行一个
- `work-002/odds-gap-2018-19.csv`：目标文件，表头已写好，**每抓完一个日期就增量 append 落盘一次**

中文名口径与 2018 年 responses 数据完全一致（湘南海洋、清水鼓动、名古屋鲸八）；
2019 升班马新增：大分三神（oita_trinita）、松本山雅（matsumoto_yamaga）。

## 抓取路线（需真浏览器，JS 渲染）
1. 捷报网单场 1x2 页：`https://live.nowscore.com/1x2/<matchid>.htm`
   （样本：`https://live.nowscore.com/1x2/1496605.htm` = 2018-02-23 鸟栖沙岩 vs 神户胜利船）
2. 2019 赛季的 matchid 未知：从捷报网日职联 2019 赛程页逐场点进，
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
- expected：306 场 → 约 918 行（每场 William Hill + bet365 + Pinnacle 三行；2018 年数据还有 Ladbrokes 行，2019 未知）
- 完成后报告：实际写入行数、distinct(date,home,away) 新增场数、完成的日期范围、
  剩余未抓日期清单及逐条原因、expected/discovered/complete/partial/missing

## 子代理已尝试但失败的路线（供参考，避免重复踩坑）
- `browser.open` 纯文本抓取：捷报网 1x2 表格、betexplorer 单场 odds 表、OddsPortal 结果页均为 JS 渲染，文本层无数据。
- 猜测 AJAX endpoint（`/1x2/xml/<id>.xml`、`/1x2/<id>.js`）→ 404。
- web.archive.org 抓源 HTML → 上游 500。
- r.jina.ai 渲染代理 → 被抓取层策略拦截。
结论：必须用真浏览器（`browser.spawn_task`）逐场抓取，文本抓取路线已穷尽。
