# 奥甲 2025/2026 逐场官方轮次／场地变更／开盘赔率可得性 — 说明文件

- 请求：ai-data-bus req-20261106-001，D 路（Q2＋Q4＋Q5）
- 赛季：奥地利足球超级联赛（Admiral Bundesliga）2025/2026，12 队
- 交付：`austrian_2025_26_rounds.csv`（192 行联赛＋表头）＋ 本文件
- 范围：只取足球事实，不含模型字段；只做赛前事实，不碰比分／赛果／预测。CSV 不含任何比分列。
- 语言与口径：队名用官方全称；日期为当地比赛日（YYYY-MM-DD），未含开球时刻（见 §6 未覆盖清单）。

## 1. 交付物与字段

| 文件 | 内容 |
|---|---|
| `austrian_2025_26_rounds.csv` | 192 行联赛逐场表，SHA-256 `01e0d5b48980a6a40766803a9216d544d9fc8a1b2a68ebede2bc497321c960e4` |
| `build_austrian_rounds.py` | 生成脚本（含全部 192 场转录数据与校验断言） |

CSV 字段：`match_id`（`austrian-2025-26-r{轮次02d}-{主队slug}-vs-{客队slug}`）、`date`、`home_team`、`away_team`、`official_round`、`competition_phase`、`venue_status`、`venue_actual`、`venue_city`、`venue_note`、`venue_source_url`、`source_url`、`schedule_note`。

校验结果（脚本断言全部通过）：总行 192；常规赛 132 行、Meistergruppe 30 行、Qualifikationsgruppe 30 行；每轮场次数正确（常规赛每轮 6 场，分裂组每轮每组 3 场）；每队 32 场（16 主场／16 客场）；(date, home, away) 无重复；`match_id` 唯一；日期范围 2025-08-01 → 2026-05-17。

## 2. 分裂边界（Q2）

- **赛制**：12 队。常规赛 Grunddurchgang 第 **1–22 轮**，2025-08-01 至 2026-03-08，共 **132 场**。
- **分裂点：第 22 轮结束后分裂，积分减半**。常规赛末轮 2026-03-08 六场同日进行。
- **分裂组**：Meistergruppe（冠军组，前 6 名）与 Qualifikationsgruppe（保级组，后 6 名）各再打 **10 轮（第 23–32 轮）**，每组 30 场；联赛总计 **192 场**。分裂后两组继续沿用第 23–32 轮编号，不重新编号。
- 冠军组（按常规赛结束时排名）：SK Sturm Graz、FC Red Bull Salzburg、LASK、FK Austria Wien、SK Rapid Wien、TSV Hartberg。
- 保级组：WSG Tirol、SCR Altach、SV Ried、Wolfsberger AC、Grazer AK、FC Blau-Weiß Linz。
- 末轮：冠军组 2026-05-17；保级组 2026-05-16。
- **唯一延期**：R4 SK Sturm Graz vs WSG Tirol 原定 2025-08-24，因 Sturm 备战欧冠附加赛次回合 vs Bodø/Glimt，推迟至 **2025-12-03** 补赛；场地仍为默认主场 Merkur Arena（仅改期，不改场地；见 CSV `schedule_note`）。
- **欧会杯附加赛（不属于联赛轮次，不在 CSV 内）**：半决赛 2026-05-19 SV Ried–Wolfsberger AC；决赛两回合 2026-05-22 SV Ried–SK Rapid Wien、2026-05-25 SK Rapid Wien–SV Ried。共 3 场，另行记录于此，不计入 192 场。

### 来源与核对

- 主源：RSSSF Austria 2025/26 全量轮次表 `https://www.rsssf.org/tableso/oost2026.html`（轮次×日期×主客队 1–32 轮＋附加赛）。
- 交叉核对：Simple Wikipedia 2025-26 Austrian football championship 页 `https://simple.wikipedia.org/wiki/2025-26_Austrian_football_championship`，1–24 轮与 RSSSF 一致。
- 赛制确认：bundesliga.at 赛季说明文 `https://www.bundesliga.at/de/news/artikel/alles-wissenswerte-zur-saison-2025-26`（2025-07-31，确认第 22 轮后分裂、每组再打 10 轮）；OEFBL 赛制页 `https://www.oefbl.at/de/die-liga/derspielmodus`；bundesliga.at 决赛阶段赛程文 `https://www.bundesliga.at/de/news/artikel/admiral-bundesliga-spielplan-fuer-den-finaldurchgang-2025-26`（决赛阶段自 2026-03-13 LASK–Hartberg 起）。
- **官方赛程页未直接取数**：bundesliga.at/de/spielplan 文本层（2026-11-06 10:55 UTC 实测）只有 JS 外壳、无赛程数据，须主代理用实时浏览器复核。官方轮次标签未逐场直接取自官方页——本表以 RSSSF＋Simple Wikipedia＋bundesliga.at 赛季说明文三重交叉为准（见 §6）。
- 队名映射（RSSSF 简写 → CSV 规范名）：Sturm→SK Sturm Graz、Salzburg→FC Red Bull Salzburg、LASK→LASK、Austria W→FK Austria Wien、Rapid→SK Rapid Wien、Hartberg→TSV Hartberg、Wattens→WSG Tirol、Altach→SCR Altach、Ried→SV Ried、Wolfsberg→Wolfsberger AC、GAK→Grazer AK、BW Linz→FC Blau-Weiß Linz。

## 3. Q4 实际比赛场地：偏离默认主场的场次

**结论：仅 1 家俱乐部、4 场联赛主场偏离默认主场**，全部为 TSV Hartberg 因 Profertil Arena 改建，赛季初临时迁至 Datenpol Arena（Bundesstadion Südstadt，Maria Enzersdorf）。其余 188 场均为默认主场。

| 轮次 | 日期 | 主场 | 客队 | 实际场地 | 城市 | 来源 |
|---|---|---|---|---|---|---|
| R3 | 2025-08-16 | TSV Hartberg | FC Red Bull Salzburg | Datenpol Arena (Bundesstadion Südstadt) | Maria Enzersdorf | bundesliga.at R3 前瞻（列 DATENPOL ARENA）；kicker 直播：Hartberg 因 Profertil Arena 改建须在 Südstadt 踢三个月 |
| R5 | 2025-08-31 | TSV Hartberg | SK Rapid Wien | Datenpol Arena (Bundesstadion Südstadt) | Maria Enzersdorf | deradmiraner.at：Hartberg 在“Exil Südstadt”迎战 Rapid；三场计划 Südstadt 主场之一（Salzburg、Rapid、WAC） |
| R7 | 2025-09-20 | TSV Hartberg | Wolfsberger AC | Datenpol Arena (Bundesstadion Südstadt) | Maria Enzersdorf | ligaportal.at 战报：2025-09-20 17:00，Datenpol Arena Maria Enzersdorf/Südstadt；官方第三场 Südstadt 主场 |
| R12 | 2025-11-01 | TSV Hartberg | FK Austria Wien | Datenpol Arena (Bundesstadion Südstadt) | Maria Enzersdorf | kicker Spielinfo：2025-11-01 17:00，Stadion Datenpol Arena (Bundesstadion Südstadt)；标题称“Südstadt 最后一场主场” |

来源链接（逐字）：
- R3：`https://www.bundesliga.at/de/news/artikel/vorschau-auf-die-3-runde-der-admiral-bundesliga-3`；kicker 直播 `https://www.kicker.ch/hartberg-gegen-salzburg-2025-bundesliga-oesterreich-5051366/ticker`
- R5：`https://www.deradmiraner.at/2025/08/01/august-2025/`
- R7：`https://www.ligaportal.at/bundesliga/spielberichte/19418-erster-punkt-an-ausweichstaette-joker-fillafer-rettet-remis-fuer-tsv-hartberg-vs-wac`
- R12：`https://www.kicker.ch/hartberg-gegen-austria-wien-2025-bundesliga-oesterreich-5051422/spielinfo`

### 计划与实际的出入（⚠️ 如实记录，不抹平）

- 赛季初计划：前 11 轮内仅 3 场主场在 Südstadt（Salzburg、Rapid、WAC），改建原定 11 月 1 日完工。
- ligaportal（2025-09-20，R7 当日）称 R7 是“官方第三场、据称也是最后一场”Südstadt 主场。
- 但改建未按期完工：**R12（2025-11-01 vs Austria Wien）仍在 Südstadt**，kicker 称其为“letztes Heimspiel in der Südstadt”（Südstadt 最后一场主场）。
- 以实际赛程为准：**共 4 场**。ligaportal 的“最后一场”指当时计划，kicker 的“最后一场”指实际最后一场；两者口径不同，交付物保留这一出入，不擅自调和。

### 回迁

- R14 2025-11-22 vs SV Ried 已回 Profertil Arena（news.steiermark.at `https://www.news.steiermark.at/cms/beitrag/13000959/29771102/`；abseits.at 第 14 轮前瞻 `https://abseits.at/fusball-in-osterreich/bundesliga/faktencheck-zur-14-bundesliga-runde-2025-26/`）。
- 官方揭幕为 2025-11-30 R15 vs SK Sturm Graz。

### 已核查的非偏离（不算偏离，不列入偏离表）

- SK Sturm Graz 与 Grazer AK 共用 Merkur Arena：赛季默认安排（12 队 11 座球场，客户端已核验），不算偏离。
- WSG Tirol 主场 Tivoli Innsbruck：默认主场，不算偏离。
- R4 Sturm–WSG 补赛（2025-12-03）：仅改期，场地仍为默认主场 Merkur Arena（theyscored／wildstat 均列 Merkur Arena, Graz）。
- LiveScore 曾把 2025-11-01 一场误标为 Profertil Arena（过期数据），以 kicker（Datenpol Arena）为准。

### 核查方法与范围

- RSSSF 全量赛程逐轮核对＋德语搜索（Ausweichstadion／Südstadt／Umbau／Profertil Arena）＋ kicker／ligaportal／bundesliga.at／deradmiraner 逐场核对。
- 范围：仅联赛 192 场。ÖFB 杯场次不在本单范围，未查。未发现其他临时主场／中立场。

## 4. Q5 开盘赔率可得性（逐源表）

问题：能否取得 2025/2026 及更早赛季的赛前开盘 1X2 赔率（Pinnacle／Bet365，明确标注 opening）？

| 来源 | 开盘可得？ | 证据（2026-11-06 文本层实测） | 门槛／限制 |
|---|---|---|---|
| Football-Data AUT.csv（`football-data.co.uk/mmz4281/2526/AUT.csv`） | **不能** | 仅含收盘列 PSCH／PSCD／PSCA（Pinnacle 收盘）及 B365H／B365D／B365A 等收盘列；schema 中无任何开盘列（客户端已确认）。本轮尝试直取标准路径：先 302、跟随重定向后 404，未能独立复核表头——结论以客户端确认为准，直取失败如实记录，不谎称已复核。 | 无（但无开盘列） |
| OddsPortal（`oddsportal.com/football/austria/bundesliga/`） | **可能（待实时浏览器确认）** | 赛季页文本层 200、561KB，含 "Opening odds" 字符串；其自述称单场页可查 opening odds 与全部赔率变动，赛季结果可回溯至 2003/04。 | 条款 §2.11 禁止未经书面同意的 scraping／aggregation：只可单场合规查阅，不可批量抓取。是否需登录看完整历史，文本层未证实，须实时浏览器核实。 |
| BetExplorer（`betexplorer.com/football/austria/bundesliga-2025-2026/`） | **未定（待实时浏览器确认）** | 赛季页文本层 200、122KB；帮助文本称可看往场 archive odds；文本层未检出 "opening" 字样、0 处 Pinnacle。 | 单场页是否有带 opening 标注的赔率列，文本层无法证实，须实时浏览器核实。 |
| NowGoal／Goaloo | **不能（开盘不可得）** | 有 Initial 列，但 Initial＝数据流首次捕获，不是真实开盘（req-20261028-004 已确立教训）。例：Goaloo 2026-04-05 Rapid–Sturm 页 `https://www.goaloo.com/football/austrian-bundesliga-rapid-wien-vs-sturm-graz/oddscomp-2958477`。逐笔时间戳可证明某报价早于开球，但标签是 Initial，不得标 opening。 | 无（但无 opening 标签） |
| SoccerPunter | **不能（付费墙）** | 赔率历史为 Platinum 会员专属，Pinnacle 列为 Premium（req-20261028-004 已确认）。 | 须登录／付费；本单不登录、不购买、不订阅。 |
| FBref／Sportradar／thefishy 等 | **不能** | 无公开开盘赔率数据。 | — |

**Q5 结论**：文本层范围内，**没有任何来源能干净地取得带 opening 标注的 Pinnacle／Bet365 赛前开盘 1X2**。最有希望的合规路径是 OddsPortal 单场页（自述含 opening odds＋赔率变动，可回溯至 2003/04），但须实时浏览器确认实际显示与登录门槛，且受 §2.11 约束不得批量抓取。铁律执行：凡只有 closing 或单一中间价的，一律标 unavailable；未把 closing 当 opening，未把单一中间价当区间；未批量抓取 OddsPortal，未登录、未购买、未动用任何付费 API 额度。

## 5. 队名与球场说明

- CSV 只在偏离行填写 `venue_actual`／`venue_city`；默认行 `venue_status=default_home`，`venue_actual` 留空——默认主场 11 座球场表由客户端已核验，本单不重复抄球场表（任务要求）。
- 12 队 11 座球场：Sturm 与 GAK 共用 Merkur Arena，其余各队一座主场。

## 6. 未覆盖清单（UQ）

| # | 未覆盖项 | 类别 | 说明 |
|---|---|---|---|
| 1 | 官方赛程页逐场轮次标签 | pending_work | bundesliga.at/de/spielplan 文本层只有 JS 外壳、无赛程数据；官方轮次标签未逐场直接取自官方页，以 RSSSF＋Simple Wikipedia＋bundesliga.at 赛季说明文三重交叉为准。待主代理实时浏览器复核。 |
| 2 | 开球时刻（kickoff time） | pending_work | CSV 只有比赛日，未含开球时刻。RSSSF 只给日期；官方赛程页 JS 渲染。如需时刻，须实时浏览器读 bundesliga.at。 |
| 3 | OddsPortal／BetExplorer 单场页 opening 显示与登录门槛 | pending_work | 文本层无法证实，待实时浏览器核查。 |
| 4 | Football-Data AUT.csv 表头独立复核 | pending_work | 本轮直取标准路径 404，未能独立复核表头；结论依赖客户端确认。低优先级：不影响“无开盘列”结论（schema 本身无开盘列）。 |
| 5 | 欧会杯附加赛 3 场 | out_of_scope | 不属于联赛轮次，仅在 §2 记录，不在 CSV 内。 |
| 6 | ÖFB 杯场次场地 | out_of_scope | 不在本单范围，未查。 |

## 7. 来源清单（逐字 URL）

- RSSSF：`https://www.rsssf.org/tableso/oost2026.html`
- Simple Wikipedia：`https://simple.wikipedia.org/wiki/2025-26_Austrian_football_championship`
- bundesliga.at 赛季说明：`https://www.bundesliga.at/de/news/artikel/alles-wissenswerte-zur-saison-2025-26`
- bundesliga.at 决赛阶段赛程：`https://www.bundesliga.at/de/news/artikel/admiral-bundesliga-spielplan-fuer-den-finaldurchgang-2025-26`
- bundesliga.at 官方赛程页（JS 外壳，文本层无数据）：`https://www.bundesliga.at/de/spielplan`
- OEFBL 赛制：`https://www.oefbl.at/de/die-liga/derspielmodus`
- kicker Hartberg–Austria Spielinfo：`https://www.kicker.ch/hartberg-gegen-austria-wien-2025-bundesliga-oesterreich-5051422/spielinfo`
- ligaportal Hartberg–WAC 战报：`https://www.ligaportal.at/bundesliga/spielberichte/19418-erster-punkt-an-ausweichstaette-joker-fillafer-rettet-remis-fuer-tsv-hartberg-vs-wac`
- news.steiermark.at 回迁报道：`https://www.news.steiermark.at/cms/beitrag/13000959/29771102/`
- bundesliga.at R3 前瞻：`https://www.bundesliga.at/de/news/artikel/vorschau-auf-die-3-runde-der-admiral-bundesliga-3`
- abseits.at 第 14 轮前瞻：`https://abseits.at/fusball-in-osterreich/bundesliga/faktencheck-zur-14-bundesliga-runde-2025-26/`
- deradmiraner.at 2025-08：`https://www.deradmiraner.at/2025/08/01/august-2025/`
- OddsPortal 奥甲赛季页：`https://www.oddsportal.com/football/austria/bundesliga/`
- BetExplorer 奥甲 2025/26 赛季页：`https://www.betexplorer.com/football/austria/bundesliga-2025-2026/`
- Goaloo 例（Rapid–Sturm 2026-04-05）：`https://www.goaloo.com/football/austrian-bundesliga-rapid-wien-vs-sturm-graz/oddscomp-2958477`

## 8. 工作说明

- 未购买、未登录、未使用任何密钥／凭证、未动用任何付费 API 额度；未批量抓取 OddsPortal（条款 §2.11）。
- 未写 repo/responses/（主代理的事）；未重复抓赛果（赛果由 Football-Data AUT.csv 提供）。
- 实时浏览器核查未做（由主代理另行安排），本文件不谎称已做。
