# req-20261022-001 C 路审计：API / 批量赔率源探查（Copa Libertadores 2018–2025，FT 1X2）

## 结论先行（0 行，不是 0 场断言）

- **`api_odds_rows.jsonl` 为空文件（0 行）。** 本路没有编造任何赔率行。
- 最大障碍不是“找不到源”，而是**唯一实证有解放者杯覆盖的批量 API 被付费墙 + 密钥挡住，而本路规则禁止付费、禁止碰付费额度、禁止使用任何密钥**：
  - **5DollarFootballAPI**：数据质量页实证有 Copa Libertadores（league id `3899038422`，Pro and Ultra，13 个赛季，自 2015 年起），且文档明确定义了 opening / closing 语义；但 2018–2025 历史查询需要 **Ultra**（Pro 只给最近 12 个月，tick history 端点只给 Ultra），本路未持有、未申请、未使用任何密钥，未付费，因此**一行也取不回**。
  - **football-data.co.uk**：实证**没有** Copa Libertadores 覆盖。它的 data.php 全文检索 “Libertadores” 与 “CONMEBOL” 均为 0 命中，全部链接只是 11 个欧洲主流联赛 + 16 个各国国内顶级联赛（巴西 = Serie A、阿根廷 = Primera Division，均为国内联赛，无洲际杯赛）。
- 其他公开批量源本轮未找到可验证的免费批量源（见 §4），均未取行。
- **expected 一律 null。** 本路没有把上一单的 2,506 行当分母、没有用它作 expected、没有拿它的 FBref / SoccerAssociation 行来“认领”任何场次。按赛季 × 阶段 × bookmaker × phase 的行数表全部为 0，见 §5。
- 检索时间：2026-10-22 16:27–16:30（Asia/Shanghai，UTC+8）。所有页面均通过浏览器文本层打开原文核实，不只看搜索摘要。未返回任何比分、进球、赛果、晋级、概率、模型方向字段；5Dollar odds/history 文档提到 ticks 含当时比分字段，本路记录该字段存在、提取时必须丢弃，本路未提取任何 tick，故无比分落盘。

---

## 1. 5DollarFootballAPI（api.5dollarfootballapi.com）——有覆盖，需 Ultra，0 行

### 1.1 覆盖核实结论：有 Copa Libertadores，但赛季标签 ≠ 历届年份

- 来源：`https://5dollarfootballapi.com/docs/data-quality`（America 分组）：
  - `Copa Libertadores 3899038422 | Pro | 126 | … | Odds 100% | … | 2015 · 13 seasons`
  - 按赛季页：`https://5dollarfootballapi.com/docs/data-quality/3899038422`，标题行：`League id 3899038422 · Pro and Ultra · 13 seasons on record, first kickoff 2015-02-04`；最近 12 个月：126 / 128 fixtures recorded，Odds 100%（按 finished 场次计）。
- 该页公布的“赛季”划分如下（**照抄，不映射为历届年份**）：

| 页内赛季标签 | 页内窗口 | Fixtures | Finished | Odds |
|---|---|---|---|---|
| 2026/27 | 2026-08-12 → 2026-10-16 | 27 | 26 | 100% |
| 2025/26 | 2025-08-13 → 2026-05-29 | 125 | 124 | 100% |
| 2024/25 | 2024-08-14 → 2025-05-30 | 129 | 124 | 100% |
| 2023/24 | 2023-08-02 → 2024-06-09 | 127 | 126 | 100% |
| 2022/23 | 2022-07-01 → 2023-06-30 | 122 | 119 | 100% |
| 2021/22 | 2021-07-14 → 2022-06-30 | 165 | 158 | 100% |
| 2020/21 | 2020-09-16 → 2021-05-28 | 222 | 219 | 99.1% |
| 2019/20 | 2019-07-24 → 2020-03-13 | 94 | 85 | 100% |
| 2018/19 | 2018-08-08 → 2019-05-10 | 159 | 157 | 100% |
| 2017/18 | 2017-07-05 → 2018-05-25 | 156 | 156 | 100% |
| 2016/17 | 2016-07-07 → 2017-05-26 | 132 | 132 | 100% |
| 2015/16 | 2015-07-15 → 2016-05-25 | 138 | 138 | 100% |
| 2014/15 | 2015-02-04 → 2015-05-29 | 131 | 130 | 90.8% |

- **关键警告：不要把 `2025/26` 当成 2025 届、把 `2018/19` 当成 2018 届。** 该源的赛季窗口是 8 月至次年 5/6 月左右，而解放者杯历届是 2 月至 11 月左右的自然年赛制；窗口与场次数（如 2020/21 的 222 场、2019/20 的 94 场）都与单届历届场次数对不上，说明该源的赛季切分不是历届切分。后续取数时必须用 `start_time / end_time` 按历届实际日期窗口切片，**绝不能用 `?season=` 标签直接指派 season_year**。这是本路留给取数方的最大身份风险点之一。
- 另注意：数据质量页的 Odds % 是“该季 finished 场次中有 pre-match odds 的比例”，不是 opening / closing 齐全率，也不是可下载行数；不得把它当成行数。

### 1.2 端点（文档原文，`https://5dollarfootballapi.com/docs`）

| 用途 | 端点 |
|---|---|
| 联赛 fixture 批量入口 | `GET /v1/leagues/{id}/fixtures`（支持 `start_time / end_time`、`status`、`order=asc/desc`、`include=odds,events,stats`；`per_page` 最大 100，include 时 50） |
| 单场赔率 | `GET /v1/fixtures/{id}/odds`（`bookmakers` 参数，默认 bet365） |
| 赔率变动历史 | `GET /v1/fixtures/{id}/odds/history`（`market` 必填，`bookmaker` 一次一个，默认 bet365；ticks 按时间升序） |
| 联赛列表 | `GET /v1/leagues`（可按 `country=AMERICAS`、`search` 过滤；`include=seasons` 给出各联赛的赛季数组） |
| Bookmaker 列表 | `GET /v1/bookmakers` |
| 状态探针 | `GET /v1/status` |

### 1.3 免费 / 付费状态（文档原文，价格冲突如实记录）

- **Free**：仅 top-5 欧洲联赛，60 requests / 小时，历史仅最近 3 个月；列表接口的 `include=odds` 从 Pro 起（Free 只能按单场读 `/v1/fixtures/{id}/odds` 的同类市场）。
- **Community Access（$0）**：top-5 联赛 + 自选一个**国家**的联赛包，Bet365 全部市场，最近 12 个月历史，300 requests / 小时。洲际杯赛不是“国家包”，按文档字面它不在 Community 的覆盖描述内；本路未向厂商核实，不把 Community 算作解放者杯可用层。
- **Pro（$5/月，文档）**：137 个 competitions（含各大洲俱乐部杯赛），但**历史查询仅最近 12 个月**（文档 History depth 节原文：`Free returns the last 3 months … Pro ($5/month) the last 12 months, and Ultra everything`；列表接口节亦同：`3 months on Free, 12 months on Pro, back to 2014 on Ultra`）。
- **Ultra**：全部历史（回溯至 2014）、全部 tick history。**odds/history 端点整段只给 Ultra 及以上，Free 与 Pro 密钥返回 403 insufficient_plan**（文档 Odds movement history 节原文）。
- **Ultra 价格未钉死**：首页称 “everything included for $25”；文档 rate limits 节称 Ultra 基础 40 requests / 分钟，更高速率档为 $35 / $45 / $55 / $65 每月。本路不采信单一价格，取数前必须以账单页为准。**本路未付费、未订阅、未试用。**
- **未鉴权探针实测**：本机 shell 对 `https://api.5dollarfootballapi.com/v1/status`（无 Authorization 头）返回 JSON 信封 `success=0`，错误类型 `authentication_error`、错误码 `missing_api_key`（“No API key provided”）。该探针未使用任何密钥；HTTP 状态码因本次 curl 未带 `-i` 而未单独记录，审计中记 `http_status=null（未单独记录）`，不编造 401。另：本机 shell 直连 `www.football-data.co.uk` 30 秒超时 0 字节（见 §2），属本机 egress 限制，不是对方站点宕机——浏览器文本层随后成功打开该站。

### 1.4 Bookmaker 清单（文档 Bookmakers 表原文，1X2 列）

- 全部计划都带 **bet365**（1X2：Pre + Live）；其余 bookmaker 只给 Ultra 及以上，1X2 均为 Pre：
  - Pinnacle（`pinnacle`）、William Hill（`williamhill`）、Ladbrokes（`ladbrokes`）、Vcbet（`vcbet`）、1xBet（`1xbet`）、Bwin（`bwin`）、Easybets（`easybets`）、Interwetten（`interwetten`）、Betfair（`betfair`）、SNAI（`snai`）、Macauslot（`macauslot`）、Betsson（`betsson`）、Bet-at-home（`betathome`）、18Bet（`18bet`）、10BET（`10bet`）、12bet（`12bet`）、Coral（`coral`）、Crown（`crown`）、Hong Kong Jockey Club（`hkjc`）、China Sports Lottery（`chinasportslottery`）。
- 非 bet365 的 bookmaker 在 odds/history 里只支持 `market=1x2 | asian | goalline | corner`，其他市场值返回 400 invalid_market。
- **本路取回的各 bookmaker 行数：全部 0。** 上表只是文档载明的可用清单，不是观测。

### 1.5 Opening / Closing 语义结论：文档有明确定义，但本路无观测可标

文档中明确到可直接执行的定义有三处（均在 `https://5dollarfootballapi.com/docs`）：

1. **Opening（bet365 1X2）**：Odds movement history 节原文——`On bet365 1x2 the first tick is always the opening /v1/fixtures/{id}/odds serves.` 即 bet365 1X2 的第一条 tick 就是 `/odds` 端点给出的 opening。
2. **Closing（通用定义）**：China Sports Lottery 小节注释原文——`closing is the latest pre-match price until kickoff, then frozen — the same as every other market.` 即 closing = 开球前最后一次赛前价，之后冻结；并称“与其他每个市场相同”。
3. **odds_full 形状**：仅限 Business 计划、仅限 live 场的 `include=odds_full`，其 block 含 opening、closing、in-play 三种价，形状与 `/v1/fixtures/{id}/odds` 的 bet365 条目相同（`in the same shape as the bet365 entry of /v1/fixtures/{id}/odds`）。

据此，**取数方的合法推导规则**（须在取数时逐场执行，不得提前断言行）：
- opening = 该场该 bookmaker 1X2 tick 流中**开球前第一条** tick（bet365 时与 `/odds` 的 opening 字段交叉核对）；
- closing = 该场该 bookmaker 1X2 tick 流中**开球前最后一条** tick（与 `/odds` 的 closing 字段交叉核对）；
- **in-play tick 一律排除在 closing 之外**；只有一条中间价时 phase 标 `unspecified`，不得标 opening 或 closing；
- 非 bet365 bookmaker 的 closing 定义除上述通用注释外，文档未在 odds/history 节单独展开，取数时须以 tick 时间戳 vs 开球时间逐场验证，验证前 phase 标 `unspecified`。
- ticks 含当时比分字段（文档：`every recorded price/line change with the score at that moment`），提取时**整列丢弃**，不得把比分带入赔率行。

### 1.6 本源行数与下一步（精确到可执行）

- 行数：**0**。原因链：有覆盖（Pro/Ultra）→ 但 2018–2025 历史查询需 Ultra（Pro 仅 12 个月）→ tick history 端点只给 Ultra → 本路禁付费/禁密钥 → 未调用任何需鉴权端点。
- 下一步（需请求方决定，C 路不代付）：
  1. 请求方确认是否订阅 Ultra（先以账单页核实价格，首页 $25 说法与文档 $35–$65 高速率档冲突）；
  2. 持 Ultra key 先调 `GET /v1/leagues/3899038422/fixtures?start_time=<历届首日>&end_time=<历届末日>&order=asc&status=finished`，**不用 `?season=`**，按历届实际日期窗口切片，并记录每批响应的字节 sha256、HTTP 状态、field_locator；
  3. 逐场调 `GET /v1/fixtures/{id}/odds/history?market=1x2&bookmaker=bet365`，丢弃 score 列，取开球前首/末 tick 为 opening / closing，与 `/odds` 的 opening / closing 字段交叉核对，不一致时两边都保留、不裁决；
  4. 其余 bookmaker 一次一个 slug 重复第 3 步，closing 先标 `unspecified` 直至 tick 时间戳验证通过；
  5. 每个观测用 5Dollar fixture id + kickoff_utc + 队名三重证据匹配到确切场次，无法唯一匹配的进 ambiguous 队列，不硬指派。

---

## 2. football-data.co.uk —— 实证无 Copa Libertadores 覆盖，0 行

### 2.1 覆盖核实结论：无洲际杯赛，只有国内联赛

- 打开原文：`https://www.football-data.co.uk/` 首页 → Historical 链接 → `https://football-data.co.uk/data.php` 全文（143 行文本层）。
- 该页自述：`Access fulltime and halftime results for up to 22 European league divisions`，以及 `Additionally, Football-data now provides data for 16 other worldwide premier divisions`。
- 该页链接表（逐项核对，无遗漏）：
  - **Main Leagues（11 个欧洲国家）**：England（Premiership & Divs 1,2,3 & Conference）、Scotland、Germany、Italy、Spain、France、Netherlands、Belgium、Portugal、Turkey、Greece。
  - **Extra Leagues（16 个各国国内顶级联赛）**：Argentina（Primera Division）、Austria、Brazil（Serie A）、China、Denmark、Finland、Ireland、Japan、Mexico、Norway（Eliteserien）、Poland、Romania、Russia、Sweden、Switzerland、USA（MLS）。
- **全文检索**：在 data.php 文本层中检索 `Libertadores` → 0 命中；检索 `CONMEBOL` → 0 命中。
- **站外检索复核**：以 `"football-data.co.uk" "Copa Libertadores" OR "Libertadores" odds CSV` 检索，返回结果中没有任何一条指向 football-data.co.uk（返回的是投注分析、xG、赔率指南等无关页）。
- **结论**：该站没有 Copa Libertadores 文件、没有洲际杯赛分类；巴西/阿根廷文件只是国内联赛，不能用来覆盖解放者杯场次。上一单关于它“无 Eliteserien 代码”的核实方法同样适用：不是“没找到”，而是**站内分类表本身就没有该赛事**。
- 补充：本机 shell curl 该站 30 秒超时 0 字节，但浏览器文本层成功打开 data.php 全文，故超时是本机 egress 限制，不是该站宕机；覆盖结论以浏览器文本层为准。

### 2.2 该站的赔率语义（仅作记录，因无覆盖而不产生行）

- data.php 原文：第一套赔率在市场开盘后、按 fixtures 页指定时间采集；第二套为 closing odds（列名含 `C`）；Pinnacle 的 closing 主胜/平/客胜赔率可追溯至 2012/13，更早赛季只有 pre-closing 赔率。
- 另有站方警告（2025-07-23 起）：`Pinnacle's public API for odds delivery has become unreliable … systematically out of date`，Pinnacle 赔率（含 pre-closing 与 closing）须谨慎使用，且不再计入市场平均/最高赔率。——即使该站有覆盖，2025 季的 Pinnacle closing 也要单独标注此警告；但因无覆盖，本条不产生任何行。
- **使用限制（站方原文，决定本路不爬它）**：data.php 称数据免费，但 `its use is intended for private individuals only, NOT commercial or data training products using automated bots/scrapers/AI`。本任务的批量自动化采集与该站明示的 intended use 冲突，因此即使对国内联赛也不应以 bot 批量抓取；本路未下载其任何 CSV。

### 2.3 本源行数

- 行数：**0**。access_status：data.php 页面本身可公开打开（浏览器文本层成功），但**赛事覆盖 = 无**。

---

## 3. 5Dollar 与 football-data 之外的其他公开批量源

以下均未产生行，逐项说明“为什么不算可用源”，不把“听说过”写成覆盖。

| 候选源 | 查到什么 | 为什么本路 0 行 |
|---|---|---|
| The Odds API（the-odds-api.com） | v4 文档有 historical 端点：`GET /v4/historical/sports/{sport}/events/{eventId}/markets?date=…`，返回不晚于给定时间的最近快照；第三方对其文档的转述称 historical 端点仅限付费计划、历史查询按 10 倍信用计费 | 需要 apiKey 才能调 `/v4/sports` 确认是否存在 `soccer_conmebol_copa_libertadores` 运动键；本路禁密钥、禁付费，故**覆盖未验证**，不得断言它有或没有解放者杯。另有第三方比较称其历史只回溯至 2020 年，该说法未经官方文档核实，**不采信**、不写入结论。下一步：持 key 后先调 sports 列表确认运动键，再谈快照。 |
| OddAlerts API | 官网称 API 在 Advanced 计划（£69.99/月，另有 £9.99 的 48 小时 Day Pass）；一条客户评价称其 `/odds/history` 保留 opening、closing、peak | 客户评价不是文档；付费墙内；解放者杯批量 1X2 覆盖未验证。0 行。 |
| Kaggle / GitHub 批量 CSV | 以 `Copa Libertadores historical odds dataset CSV github kaggle 1x2` 检索，返回无关 notebook、7msport 数据库页等，**没有一个可验证的解放者杯 1X2 批量 CSV** | 7msport 数据库页（`data.7msport.com/history_matches_data/…`）是网站赛程/统计页，属于网站抓取路线范畴，不是本 C 路的 API/批量源；本路不把它算作批量源，也不替网站路线认领。 |
| OpenFootball（football.json） | 社区赛程/赛果 JSON 档案 | 无赔率字段，直接排除。 |
| API-Football（工作区已有 connector） | **本路未调用** | 按本路“不碰任何付费额度”规则，未用其 Pro 额度做任何查询；其赔率端点对 2018–2025 旧场的保留期与 opening/closing 语义在本路**未验证**（第三方转述存在“全计划有 pre-match odds”与“7 天保留”两种冲突说法，均不采信）。是否动用已有额度、由主代理另行决定，不在本路结论内。 |

---

## 4. 按赛季 × 阶段 × Bookmaker × Phase 行数（全部 0，expected 全部 null）

下表是本路实际取回的行数，不是“应有场次数”。任何把 0 / 某数算成覆盖率的做法都是错的，因为 expected 没有权威源公布。

| 赛季 | 官方阶段 | Bookmaker | Phase | 本路行数 | expected |
|---|---|---|---|---|---|
| 2018 | 全部阶段 | 全部（bet365 / pinnacle / williamhill / 其他） | opening / closing / unspecified | 0 | null |
| 2019 | 全部阶段 | 全部 | opening / closing / unspecified | 0 | null |
| 2020 | 全部阶段 | 全部 | opening / closing / unspecified | 0 | null |
| 2021 | 全部阶段 | 全部 | opening / closing / unspecified | 0 | null |
| 2022 | 全部阶段 | 全部 | opening / closing / unspecified | 0 | null |
| 2023 | 全部阶段 | 全部 | opening / closing / unspecified | 0 | null |
| 2024 | 全部阶段 | 全部 | opening / closing / unspecified | 0 | null |
| 2025 | 全部阶段 | 全部 | opening / closing / unspecified | 0 | null |

- 按源分：5Dollar 0 行、football-data.co.uk 0 行、其他批量源 0 行，合计 0 行。
- 按 market 分：FT 1X2 0 行；其他市场不在本路范围内，未统计。
- 按状态分：eligible（pre-match 合格）0 行、partial 0 行、unavailable（无覆盖，如 football-data 的解放者杯）按源记 1 项源级结论、blocked（付费墙/密钥，如 5Dollar 的 Ultra 层）按源记 1 项源级结论、conflict 0、ambiguous-match 0、parse_failed 0。

## 5. Ambiguous 队列

**空。** Ambiguous 队列为空不是“没有歧义场次”的断言，而是“本路没有取回任何赔率观测，因此没有任何观测需要被指派或被判歧义”。一旦按 §1.6 取回 5Dollar ticks，凡是 fixture id + kickoff_utc + 队名三重证据不能唯一锁定确切场次的观测，必须进 ambiguous 队列，不得按队名相似度硬指派；5Dollar 赛季标签与历届年份的不对应（§1.1）是届时最可能的歧义来源。

## 6. 未解决项 / 下一步（按优先级）

1. **请求方决定：是否为 5Dollar Ultra 付费（C 路不代付）。** 付费前先以账单页核实 Ultra 价格（首页 $25 说法与文档 $35–$65 高速率档冲突）；同时确认 Ultra 的“回溯至 2014”是否包含 2018–2025 全部历届的 1X2 tick（数据质量页的 Odds % 只说明有 pre-match odds，不保证 opening / closing 齐全）。
2. **取数方执行 §1.6 的 5 步**（历届日期窗口切片 → bet365 tick → opening / closing 交叉核对 → 其余 bookmaker 逐个验证 → 三重证据匹配 + sha256 / HTTP 状态 / field_locator 全量记录）。取数时 ticks 的 score 列整列丢弃；in-play tick 不得计入 closing。
3. **主代理另行决定：是否动用 API-Football 已有 Pro 额度。** 动用前必须以官方文档核实其赔率端点对 2018–2025 旧场的保留期与 opening/closing 定义；本路不替它背书。
4. **主代理另行决定：是否向 The Odds API / OddAlerts 申请 key 并核实覆盖。** 两者均为付费墙内、覆盖未验证；申请前应先以官方 sports / 覆盖列表确认解放者杯运动键存在。
5. **不再派任务去撞的墙**：football-data.co.uk 的解放者杯（站内分类表本身无此赛事，属源级无覆盖，不是“没找到”）；5Dollar 的 Free / Pro 层（文档明文：Free 仅 top-5、Pro 仅 12 个月、odds/history 仅 Ultra，Free/Pro 调 tick history 得 403）。

## 7. 证据 URL 清单（本路实际打开过的原文页）

- `https://5dollarfootballapi.com/`（首页：计划分层、top-5 免费层、Community 国家包、odds 含 opening / current / live 的 FAQ 表述）
- `https://5dollarfootballapi.com/docs`（端点参考：history depth、bookmakers 表、odds/history 的 Ultra 限制与 bet365 opening 定义、Jingcai closing 定义、联赛 fixture 端点）
- `https://5dollarfootballapi.com/docs/education`（Education Access：130+ competitions、20 bookmakers、tick history 示例、`/fixtures/{id}/odds/history?market=1x2&bookmaker=pinnacle` 用法）
- `https://5dollarfootballapi.com/docs/data-quality`（America 分组：Copa Libertadores `3899038422`、Pro、Odds 100%、2015 · 13 seasons）
- `https://5dollarfootballapi.com/docs/data-quality/3899038422`（Copa Libertadores 按赛季表：赛季标签与窗口、场次数、Odds %）
- `https://www.football-data.co.uk/`（首页）
- `https://football-data.co.uk/data.php`（数据页全文：22 个欧洲联赛分区 + 16 个各国国内联赛；opening / closing 两套赔率说明；Pinnacle 自 2025-07-23 不可靠警告；private individuals only、禁 bot/scraper/AI 的使用限制）
- 未鉴权探针（无密钥）：`https://api.5dollarfootballapi.com/v1/status` → 信封 `success=0`、错误码 `missing_api_key`；HTTP 状态未单独记录，记 null，不编造。

## 8. 本路未做的事（防误读）

- 未创建、未借用、未复用任何 API 密钥；未订阅、未试用、未付费任何计划；未消耗任何已有付费额度（包括 API-Football Pro）。
- 未下载 football-data.co.uk 的任何 CSV（无覆盖 + 站方禁 bot 条款）。
- 未用上一单的 2,506 行、1,241 场、155 场等任何数字作分母、作 expected、作认领依据。
- 未把搜索摘要、第三方比较文章的说法写成官方文档结论；凡第三方说法均已标注“未经官方文档核实，不采信”。
- 未猜测任何 URL、联赛 id（除文档与数据质量页原文给出的 `3899038422` 外）、bookmaker slug（除文档表原文外）、价格（Ultra 价格冲突已明示）。
