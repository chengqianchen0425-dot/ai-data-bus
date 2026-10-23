# req-20261023-001 C 路：访问核查审计

**核查日期**：2026-10-23（Asia/Shanghai）
**核查方式**：公开文档与公开页面核查（browser.open 文本层 + browser.search）。未购买、未登录、未使用任何密钥/凭证、未动用任何已有付费额度。
**HTTP 状态说明**：本轮使用的 browser.open / browser.search 工具层**不返回 HTTP 状态码**，下表 HTTP 状态一律记为“未提供（工具层不返回）”；“页面成功返回文本”仅表示工具返回了可读页面内容，不等同于断言 HTTP 200。上一单记录为 null 的 HTTP 状态项同样保留 null，不补编。
**复核结论定义**：确认 = 本轮公开核查与上一单断言一致；修正 = 本轮观测与上一单不同，以本轮为准并说明原因；未复核 = 本轮未打开对应官方文档/页面，不得在汇总时升级为已确认。

---

## 1. 逐源核查记录

### 1.1 5DollarFootballAPI

| 项目 | 记录 |
|---|---|
| 核查方法 | browser.open 官方数据质量总页与分季页；browser.search 第三方综述（仅作线索） |
| 打开的 URL | `https://5dollarfootballapi.com/docs/data-quality`；`https://5dollarfootballapi.com/docs/data-quality/3899038422` |
| HTTP 状态 | 未提供（工具层不返回）；两页均成功返回文本 |
| 关键原文 | "League id 3899038422 · Pro and Ultra · 13 seasons on record, first kickoff 2015-02-04, recounted 8 hours ago"；"Finished, last 12 mo … 127 of 129 fixtures recorded … Odds, 100%, 127 of finished"；分季表如 "2025/26 \| 2025-08-13 → 2026-05-29" |
| 复核结论 | **确认**：联赛 id 3899038422、Pro and Ultra 标注、13 季、自 2015 年起、各季 Odds 100%。**修正**：最近 12 个月场次由上一单的 126/128 变为本轮的 127/129，页面自述 8 小时前重算，两时点观测并列，不调和。**未复核**：官方 odds/history 文档原文（Ultra 门槛、bet365 首条 tick = opening、closing = 开球前最后一次赛前价）、各档价格与历史窗口——第三方综述（dev.to / SourceForge / Slashdot）一致称 Free 仅 top-5 联赛 3 个月、Community $0 top-5 + 一国包 12 个月、Pro $5/月 130+ 赛事 12 个月、Ultra $25/月 全部赛事 19 家博彩公司完整 tick 回溯至 2014，但**一律标注 unverified**，不采信。 |

### 1.2 OddsPortal

| 项目 | 记录 |
|---|---|
| 核查方法 | browser.open 官方条款页；browser.search 官方隐私政策与条款摘要 |
| 打开的 URL | `https://www.oddsportal.com/terms/`（全文 510 行，本轮读至 359 行，关键条款均在已读范围内） |
| HTTP 状态 | 未提供（工具层不返回）；页面成功返回文本 |
| 关键原文 | §2.3 "We may require registration in order for you to access certain parts or features of the Website. Without registration, you may not be able to view and use all content and the features of the Website may be limited."；§5.2 "With a user account, the user can use the Service in its entirety."；§2.11 "you are not permitted to use our content available on the Website by embedding, aggregating, scraping or recreating it without our express consent" 及 "You must not burden our server … with automated requests"；§2.2 "for your personal use only"；§2.10 数据库提取禁令 |
| 复核结论 | **确认**：注册/完整服务关系与 scraping/aggregation 禁令（本轮新增的关键 blocker，上一单未引用条款原文）。**未复核**：本轮具体解放者杯场次的渲染状态（沿用上一单：2025 结果页 0 家博彩公司、单场页 404、H2H 空表、无 Opening/Closing 标注）；条款页未列赛事清单，覆盖沿用上一单。 |

### 1.3 BetExplorer

| 项目 | 记录 |
|---|---|
| 核查方法 | browser.search 站内页（登录框/注册文案）；上一单渲染证据作起点 |
| 打开的 URL | 未单独打开条款页；搜索返回的 betexplorer.com 站内页（含登录框）与 `https://www.betexplorer.com/terms-of-service.php`（仅搜索结果，未打开正文） |
| HTTP 状态 | 未提供 |
| 关键原文 | "Register for free"；"If you have forgotten your username and/or password on BetExplorer.com, enter your e-mail address used in registration." |
| 复核结论 | **确认**：注册免费、登录只用于个性化；未发现查看赔率的付费墙。**未复核**：条款页 scraping 细则（未打开正文）；本轮各季页渲染状态（沿用上一单：2025/2024 结果表有数值、2025 决赛单场页仅 Stake.com 一家、2023/2022/2018 淘汰赛表为空、2021/2020/2019 未开全量结果页）。 |

### 1.4 NowGoal（含静态文件与渲染页）

| 项目 | 记录 |
|---|---|
| 核查方法 | browser.open 联赛页文本层；上一单渲染证据与静态文件记录作起点 |
| 打开的 URL | `https://football.nowgoal.net/league/89`（本轮打开，全文 159 行） |
| HTTP 状态 | 未提供（工具层不返回）；页面成功返回文本，但仅为骨架 |
| 关键观测 | 页标题 "2026 Copa Libertadores Schedule, Fixture, Latest Results"；正文只有时区选择器、赔率格式选择器、Schedule / Standings / Statistics / ODDS STATS 等空章节标题，**无任何 fixture 行、无任何赔率值** |
| 复核结论 | **确认**：联赛页 89 = 解放者杯；文本层只能抓到骨架（与上一单一致）。**未复核**：`?season=2024` 等季页参数；89 与 sclass 的对应（s89）；静态文件路线（上一单：s89_en.json 在 nowgoal.net / nowgoal2.top 上 404，1x2.nowgoal50.com DNS 失败，retry_after 2026-10-29——本轮未到重试日，不重撞）。上一单渲染页 URL（match/live-2661153、oddscomp/2661153、1x2-odds/2661153）与 Initial/Live 两组值沿用上一单，未在本轮重开。 |

### 1.5 Football-Data.co.uk

| 项目 | 记录 |
|---|---|
| 核查方法 | browser.open 官方数据页全文 |
| 打开的 URL | `https://football-data.co.uk/data.php`（本轮打开，全文 143 行） |
| HTTP 状态 | 未提供（工具层不返回）；页面成功返回文本 |
| 关键原文 | 全部 FREE，但用途限 private individuals only，且 NOT commercial or data training products using automated bots/scrapers/AI；Main Leagues 11 个欧洲联赛 + Extra Leagues 16 个各国国内联赛（含阿根廷 Primera Division、巴西 Serie A）；**全文无 Copa Libertadores / CONMEBOL 条目**；赔率口径：第一套在市场开盘后按 fixtures 页指定时间采集，第二套为 closing odds（列名含 `C`），Pinnacle closing 可追溯至 2012/13；自 2025-07-23 起 Pinnacle 公共 API 不可靠、其赔率系统性过时、不再计入市场平均/最高价 |
| 复核结论 | **确认**：上一单“无覆盖”断言本轮得到确认；用途限制与 opening/closing 列口径亦经本轮原文确认。站方禁令原因，上一单未下载其任何 CSV，本单同样未下载。 |

### 1.6 The Odds API

| 项目 | 记录 |
|---|---|
| 核查方法 | browser.open 官网首页；browser.search 官方 FAQ |
| 打开的 URL | `https://theoddsapi.com/`（本轮打开）；搜索返回的 theoddsapi.com 官方 FAQ 页（未单独打开正文，以官方域名搜索结果为准） |
| HTTP 状态 | 未提供（工具层不返回）；首页成功返回文本 |
| 关键原文 | 首页："Free $0/month (25 requests/day, NFL/NBA/MLB h2h only)"、"Professional $29/month (20,000 requests, 25+ sports)"、"Business $99/month (200,000 requests, historical odds archive, 26 sports)"；首页足球覆盖列出 EPL、欧冠、欧联、西甲、德甲、意甲、法甲、荷甲、英冠及 2026 世界杯，**未列出 Copa Libertadores**；官方 FAQ 足球清单："English Premier League, Champions League, Europa League, La Liga, Bundesliga, Serie A, Ligue 1, Eredivisie, EFL Championship, Liga MX, and MLS"，同样**没有解放者杯**；"Historical archive access and edge detection are available for all soccer leagues on the Business plan."；"Authentication is a single x-api-key HTTP header on every request" |
| 复核结论 | **确认**：免费档范围、Business 历史档、官方足球清单未列出解放者杯。**未复核**：解放者杯 sport key 是否存在（需 key 调 sports 端点，本单禁凭证）；第三方“历史回溯至 2020 年、历史查询 10 倍信用”说法未经官方文档核实，标注 unverified。 |

### 1.7 OddAlerts

| 项目 | 记录 |
|---|---|
| 核查方法 | browser.open 官方 API 页（上一单）+ browser.search 官方 API 页复核（本轮） |
| 打开的 URL | `https://www.oddalerts.com/football-data-api`（上一单打开；本轮搜索返回同一官方页内容） |
| HTTP 状态 | 未提供（工具层不返回） |
| 关键原文 | "Is there a free football API plan? No. API access comes with the Advanced plan, or with a one-off 48-hour Advanced Day Pass for £9.99 if you want to try it first. A free OddAlerts account still gets you the tools on the website."；"Opening, closing and peak odds are kept indefinitely. Full tick-by-tick odds movement is kept for 21 days."；"Add your api_token as a query parameter on every request. Tokens allow 300 requests per minute… Going over returns HTTP 429."；API 在 Advanced 计划内，£69.99/月；8 家博彩公司：Pinnacle、Bet365、1xBet、William Hill、Betfair Exchange、Kambi、Betano、FanDuel |
| 复核结论 | **确认**：无免费 API 计划、Advanced/Day Pass 价格、opening/closing/peak 保留规则、21 天 tick 窗口、api_token 认证与 429 规则。**未复核**：解放者杯覆盖——官方 API 页未列赛事清单，不得写成已确认有覆盖。 |

### 1.8 API-Football

| 项目 | 记录 |
|---|---|
| 核查方法 | browser.open 官方新手指南全文定位；browser.find 定位 7 天限制原文 |
| 打开的 URL | `https://www.api-football.com/news/post/how-to-get-started-with-api-football-the-complete-beginners-guide`（本轮打开，全文 1216 行；find 命中 L946） |
| HTTP 状态 | 未提供（工具层不返回）；页面成功返回文本 |
| 关键原文 | "API-Football covers more than 1 200 leagues and cups worldwide, from the Premier League and La Liga down to the Kazakh Premier League and the Copa Libertadores."；"The free tier gives you 100 requests per day and access to every endpoint without exception. … Pro plan at $19/month gives you 7,500 daily requests, Ultra at $29/month gives 75,000, Mega at $39/month gives 150,000. All plans include all endpoints, all data types, no paywalled features."；"Authentication happens through a single request header: x-apisports-key set to your API key."；"**The 7-day history limit is the most important thing to know about this endpoint.** Only the last seven days of odds data is retained. Query for odds on a fixture from eight days ago and you'll get nothing back. This is by design, not a bug…"；"/odds endpoint paginates at 10 per page." |
| 复核结论 | **确认**：联赛覆盖含解放者杯、免费档 100 requests/天、全端点开放、各档价格、x-apisports-key 认证、7 天保留期、/odds 10 条/页。**修正**：上一单“赔率端点对旧场的保留期与语义未验证”→本轮修正为已验证：保留期 7 天、语义为 pre-match 价；第三方“全计划有 pre-match odds”与“7 天保留”两种说法实为同一事实的两面，不再冲突。本单禁动用已有 connector 额度，未作任何 API 调用。 |

### 1.9 Kaggle / GitHub 公开数据集

| 项目 | 记录 |
|---|---|
| 核查方法 | browser.search 两轮（通用检索 + Kaggle 定向检索）；browser.open OpenFootball 仓库（见 1.10） |
| 打开的 URL | 搜索返回：`https://www.kaggle.com/datasets/ricardomattos05/jogos-do-campeonato-brasileiro/`（Brazilian Soccer Database）、`https://www.kaggle.com/datasets/takidaki/70-football-leagues-data-2019-2023`（70+ Football Leagues 2019-2023）、`https://awesome.ecosyste.ms/lists/openfootball%2Fawesome-football`、gist 通用源表；均未单独打开数据集详情页正文 |
| HTTP 状态 | 未提供 |
| 关键观测 | Brazilian Soccer Database 自述覆盖 Brasileirão、Libertadores、Sudamericana、Copa do Brasil，但**未提赔率列**，"match statistics" 列为下一步计划；70+ Football Leagues 自述含 "Match Odds for 1X2 and O/U 2.5 Goals"，但是否含解放者杯未在描述中确认；Scribd 莫扎特投注单 PDF 为单期投注单，不是可审计历史数据集，不列入 |
| 复核结论 | **未复核**：本轮未找到可验证的解放者杯 1X2 批量集；两个 Kaggle 候选集的内容（赔率列、赛季覆盖、博彩公司标注）与 Kaggle 下载登录墙均未单独验证；GitHub 侧无指向解放者杯赔率集的链接。结论为“未找到可验证集”，不是“不存在”。 |

### 1.10 OpenFootball

| 项目 | 记录 |
|---|---|
| 核查方法 | browser.open GitHub 仓库根页；browser.search 背景检索 |
| 打开的 URL | `https://github.com/openfootball/south-america`（本轮打开，全文 104 行） |
| HTTP 状态 | 未提供（工具层不返回）；页面成功返回文本 |
| 关键原文 | "Free open public domain football data (football.db) for South America (incl. Brazil, Argentina, Colombia, and much more)"；Visibility: Public；License: Creative Commons Zero v1.0 Universal (CC0-1.0)；根目录含 `copa-libertadores` 目录；README："datasets in the Football.TXT format for match schedules, results and more"、"The football.db schema, data and scripts are dedicated to the public domain." |
| 复核结论 | **确认**：公开仓库、CC0、copa-libertadores 目录存在、赛程/赛果定位；README 未提赔率，与上一单“只有赛程/赛果 JSON，无赔率字段”相符。**未复核**：copa-libertadores 目录内分季文件覆盖年份（未逐个打开）。 |

### 1.11 SoccerPunter

| 项目 | 记录 |
|---|---|
| 核查方法 | browser.search 两轮（通用检索 + 解放者杯定向检索） |
| 打开的 URL | 未单独打开单页正文；搜索返回的 soccerpunter.com live-odds 页：`https://www.soccerpunter.com/live-odds/1116114/Toluca-vs-Nacional`、`https://www.soccerpunter.com/live-odds/12030945/Libertad-vs-Sport-Boys`、`https://www.soccerpunter.com/live-odds/1116129/Gremio-vs-Aurora`、`https://www.soccerpunter.com/live-odds/1115639/Gremio-vs-Caracas`、`https://www.soccerpunter.com/live-odds/19629940/2-de-Mayo-vs-Alianza-Lima`（2026，超出范围，仅证覆盖存在） |
| HTTP 状态 | 未提供 |
| 关键原文 | "It consists of the opening odds and the daily fluctuation. … To view the odds history and archive, simply mouseover or click on H button."；博彩公司栏含 "Bet365 Premium"、"Winner Premium"、"Vulcanbet Premium"、"Singapore Pools Premium"；"All soccer bets for Fixed Odds (1X2) apply only to the full 90 minutes play of match results unless otherwise stated. This includes injury time goals but not extra-time (ET) score and golden goal or penalty shoot-outs."；页模板含 Pre-Match / 1X2 / Asian Handicap 等市场与 "Copa Libertadores Form" 栏 |
| 复核结论 | **确认**：解放者杯 live-odds 页存在、opening/daily fluctuation 描述、H 按钮说明、部分博彩公司 Premium 标注、1X2 的 90 分钟口径定义。**未复核**：H 按钮全量历史是否需 Premium 会员、单页实际渲染赔率值、解放者杯页批量可行性（上一单意甲批次曾用浏览器任务抓取 SoccerPunter，但本单解放者杯路径未验证）。页内 opening 无时间戳定义、无 closing 定义，按母请求口径仍只能标 unspecified。 |

---

## 2. 复核结论汇总

| 源 | 确认 | 修正 | 未复核 |
|---|---|---|---|
| 5DollarFootballAPI | 联赛 id/Pro and Ultra/13 季/自 2015/Odds 100% | 12 个月场次 126/128 → 127/129（重算时点不同） | Ultra 门槛、opening/closing 文档原文、各档价格与历史窗口 |
| OddsPortal | 条款 §2.3/§5.2/§2.11/§2.2/§2.10 原文 | — | 本轮场次渲染、赛事清单 |
| BetExplorer | 注册免费、无查看赔率付费墙 | — | 条款 scraping 细则、本轮季页渲染 |
| NowGoal | 联赛页 89、文本层骨架 | — | 季页参数、s89 对应、静态文件（retry_after 2026-10-29 未到） |
| Football-Data.co.uk | 无覆盖、FREE + 用途限制、opening/closing 列口径、Pinnacle 警告 | — | —（本轮全文核查完成） |
| The Odds API | 免费档范围、Business 历史档、官方足球清单无解放者杯 | — | sport key、历史回溯年份 |
| OddAlerts | 无免费 API 计划、价格、保留规则、api_token、429、8 家博彩公司 | — | 解放者杯覆盖 |
| API-Football | 覆盖、免费档、全端点开放、价格档、key 认证、7 天保留、10 条/页 | 保留期与语义由“未验证”→已验证（7 天 + pre-match） | 旧场 /odds 实测（本单禁凭证，未调用） |
| Kaggle/GitHub 数据集 | — | — | 全部内容项（无可验证集；候选集未验证；登录墙未单独验证） |
| OpenFootball | 公开仓库、CC0、copa-libertadores 目录、赛程/赛果定位 | — | 分季文件覆盖年份 |
| SoccerPunter | 解放者杯页存在、opening 描述、H 按钮说明、Premium 标注、90 分钟口径 | — | H 按钮门控、单页渲染值、批量可行性 |

**未复核项不得在汇总时升级为已确认**，尤其：5Dollar 的 Ultra 门槛与 opening/closing 文档原文、OddAlerts 的解放者杯覆盖、The Odds API 的 sport key、SoccerPunter 的 H 按钮门控。

---

## 3. 本轮未动用的项（合规记录）

- 未购买任何订阅（含 OddAlerts £9.99 Day Pass、任何 API 付费档）；未登录任何账号；未使用任何密钥/凭证；未动用 API-Football 已有 connector 额度；未下载 Football-Data.co.uk 任何 CSV（站方禁令）；未下载 Kaggle 数据集；未对 OddsPortal 做自动化提取（条款 §2.11 禁止）；未写 `repo/responses/`（主代理负责）。
- 同目录内其他路文件（build_conmebol.py、fbref_*_textlayer.jsonl、odds_audit.md 等）为并行路资产，本 C 路未改动。
