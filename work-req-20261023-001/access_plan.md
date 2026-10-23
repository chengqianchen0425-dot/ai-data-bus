# req-20261023-001 C 路：访问计划与 blocker 分析

**主题**：Copa Libertadores 2018–2025 fixture 与历史 pre-match 1X2 赔率 —— 不花钱、不凭证能不能拿到数据
**核查日期**：2026-10-23（Asia/Shanghai）
**硬约束**：不购买订阅、不登录、不使用任何密钥/凭证、不动用任何已有付费额度；只做公开文档与公开页面核查。
**交付性质**：本文件是访问计划分析，**不是赔率行**。不含任何比分、赛果、预测字段，不编赔率行。
**上一单关系**：work-req-20261022-001 的结论只作起点；每项关键断言都经本轮公开核查复核，复核失败的写“本轮未复核”，不照抄。复核明细见同目录 `access_audit.md`。

---

## 0. 四档总表（11 个候选源）

| # | 源 | 本轮核查后的档位 | 解放者杯覆盖 | 免费/公开层能看到什么 | opening/closing 语义 |
|---|---|---|---|---|---|
| 1 | 5DollarFootballAPI | **需付费 + 需密钥** | ✅ 已确认（官方数据质量页） | 免费层看不到本赛事（官方页标注 Pro and Ultra） | 官方文档定义：bet365 1X2 首条 tick 即 opening，closing = 开球前最后一次赛前价（上一单结论，本轮未复核文档原文） |
| 2 | OddsPortal | **免费公开可达（浏览）/ 需登录（完整服务）** | ✅ 已确认（上一单渲染页；本轮条款页未列赛事清单） | 赛季/单场页可浏览；但上一单样本渲染后为 0 家博彩公司 | 无 Opening/Closing 标注（上一单结论） |
| 3 | BetExplorer | **免费公开可达（浏览）/ 需登录（个性化功能）** | ✅ 已确认（上一单各季页；本轮搜索页见解放者杯条目） | 结果表与单场页单值价格；博彩公司常为 null | 无 Opening/Closing 标注；页内只有单值 |
| 4 | NowGoal（含静态文件与渲染页） | **免费公开可达（无登录/付费/密钥墙）** | ✅ 已确认（联赛页 89 标题即 Copa Libertadores） | 渲染页 1x2 页的 Initial/Live 两组值；文本层只能看到骨架 | **无定义**：Initial 只是数据流首次捕获（≠真实开盘，见 AGENTS.md 纠正）；Live 不得标 closing |
| 5 | Football-Data.co.uk | **免费公开可达，但无覆盖** | ❌ **无覆盖（本轮复核确认）** | 免费 CSV（仅欧洲 11 联赛 + 各国国内联赛 16 个） | 有定义（开盘后第一套 + closing 列 `C`），但因无覆盖而不产生行 |
| 6 | The Odds API | **需付费 + 需密钥** | ❌ **官方联赛清单未列出** | Free 档仅 NFL/NBA/MLB 的 h2h，无足球 | 历史档案为 Business 档；解放者杯 sport key 未验证 |
| 7 | OddAlerts | **需付费 + 需密钥** | ⚠️ **未验证**（官方 API 页未列赛事清单） | 免费账号只能用网站工具，无 API | 有定义：opening/closing/peak 无限期保留，逐 tick 仅 21 天 |
| 8 | API-Football | **需密钥（任何计划都要 key；本单禁动用额度）** | ✅ 已确认（官方指南明文列出 Copa Libertadores） | 免费账号 100 requests/天，全部端点开放 | /odds 为 pre-match 价；**但 7 天保留期使历史赔率在任何计划下都拿不到** |
| 9 | Kaggle/GitHub 公开数据集 | **需登录（Kaggle 下载）/ 免费公开（GitHub 浏览）** | ⚠️ **未验证**（本轮未找到可验证的解放者杯 1X2 批量集） | GitHub 公开仓库可浏览；Kaggle 下载需账号 | 取决于各数据集自带列定义，无统一语义 |
| 10 | OpenFootball | **免费公开可达（CC0）** | ✅ 已确认（south-america 仓库含 copa-libertadores 目录） | 赛程/赛果 JSON（Football.TXT 格式） | 无赔率字段，无 opening/closing |
| 11 | SoccerPunter | **免费公开可达（页面可爬取；H 按钮全量历史门控未复核）** | ✅ 已确认（本轮搜索见多场解放者杯 live-odds 页） | live-odds 页骨架 + opening/daily fluctuation 描述；部分博彩公司标 Premium | 页内称 opening odds + daily fluctuation，但无时间戳定义，不得标母请求口径的 opening/closing；1X2 适用 90 分钟有页内定义 |

**四档计数**：免费公开可达 6（OddsPortal、BetExplorer、NowGoal、Football-Data、OpenFootball、SoccerPunter，其中 Football-Data 无覆盖）；
需登录 1（Kaggle/GitHub 数据集家族，以 Kaggle 下载侧计）；
需付费 3（5DollarFootballAPI、The Odds API、OddAlerts）；
需密钥 1（API-Football，密钥为其唯一绑定约束，且另有 7 天保留期这一计划无关的硬 blocker）。
合计 11，与候选清单一一对应，无遗漏。

**档位判定说明**：OddsPortal 与 BetExplorer 的“需登录”只影响个性化/完整服务，浏览本身公开可达，故主档位计为免费公开可达，登录列为次要约束；API-Football 虽有免费账号，但任何调用都必须带 key，且本单禁动用额度，故主档位计为需密钥，不计入免费档。

---

## 1. 逐源 blocker 原文与核查结论

### 1.1 5DollarFootballAPI —— 需付费 + 需密钥

- **覆盖核实（本轮确认）**：官方数据质量页 `https://5dollarfootballapi.com/docs/data-quality` 的 America 分组与分季页 `https://5dollarfootballapi.com/docs/data-quality/3899038422` 均列出 Copa Libertadores。
- **blocker 原文（官方页，本轮打开）**：
  > "League id 3899038422 · Pro and Ultra · 13 seasons on record, first kickoff 2015-02-04, recounted 8 hours ago"
  > "Finished, last 12 mo … 127 of 129 fixtures recorded … Odds, 100%, 127 of finished"
- **本轮修正/并列**：上一单写的是“最近 12 个月 126/128 场”；本轮打开显示 **127/129 场**，页面自述 8 小时前重算。差异极可能是重算时点不同，**不擅自调和**，两时点观测并列。上一单“Pro and Ultra”标注本轮得到确认。
- **免费层能看到什么**：按官方页标注，本赛事不在免费层。免费层/Community 档的具体价格与历史窗口（Free 仅 top-5 欧洲联赛、3 个月；Community $0 为 top-5 + 自选一个国家包、12 个月；Pro $5/月 130+ 赛事、12 个月；Ultra $25/月 全部赛事、19 家博彩公司、完整 tick 历史、回溯至 2014）**本轮只在 dev.to / SourceForge / Slashdot 等第三方综述中出现，未经官方文档核实，一律标注 unverified，不采信、不背书**。上一单关于“历史查询与 tick history 只给 Ultra”“bet365 1X2 首条 tick 即 opening、closing = 开球前最后一次赛前价”的断言，**本轮未复核官方文档原文**（未打开官方 odds/history 文档页），交付中保留为“上一单结论、本轮未复核”。
- **赛季标签陷阱（本轮确认）**：分季表用欧洲赛季标签，如 `2025/26 | 2025-08-13 → 2026-05-29`、`2024/25 | 2024-08-14 → 2025-05-30`，与解放者杯自然年届次对不上。取数必须按历届实际开球日期窗口切片，禁用 `?season=` 指派 season_year。
- **本单可用性**：❌ 不可用。付费墙 + 密钥墙双重阻断，且本单禁购买禁凭证。即使将来付费，也须先复核官方文档的 Ultra 门槛与 opening/closing 定义。

### 1.2 OddsPortal —— 免费公开可达（浏览），但条款禁自动化提取

- **覆盖核实**：上一单实时浏览器渲染过解放者杯页（2025 结果页、单场页、H2H 页）；本轮打开的是官方条款页，未在条款页核赛事清单，覆盖沿用上一单。
- **blocker 原文（官方条款页，本轮打开，`https://www.oddsportal.com/terms/`）**：
  > "2.3. Registration. We may require registration in order for you to access certain parts or features of the Website. Without registration, you may not be able to view and use all content and the features of the Website may be limited."
  > "5.2. User account functions. With a user account, the user can use the Service in its entirety."
  > "2.11. Illegal interventions. … You must not burden our server … with automated requests … you are not permitted to use our content available on the Website by embedding, aggregating, scraping or recreating it without our express consent, unless otherwise provided for by applicable laws and regulations."
  > "2.2. … for your personal use only. You may not use the Website or our content for commercial purposes."
  > "2.10. … no extraction (copying) or exploitation … of the Database Content or of a qualitatively or quantitatively substantial part thereof is permitted without our express consent."
- **本轮新增的关键 blocker**：条款 §2.11 明确禁止未经书面同意的 scraping/aggregation 与自动化请求。这是**条款墙**，不是付费墙：人工浏览可达，自动化批量提取不在本单合规路径内。
- **免费层能看到什么**：赛季/单场/H2H 页可浏览（上一单渲染证据）；但上一单样本结果是 **0 家博彩公司 / 空表 / 404**，且无 Opening/Closing 标注。上一单“无登录验证（任务禁登录）”的约束本单同样适用。
- **本单可用性**：⚠️ 仅限人工浏览参考。批量抓取被条款明文禁止；且样本产出为 0，不能作为批量替代方案。

### 1.3 BetExplorer —— 免费公开可达（浏览）

- **覆盖核实**：上一单经站内赛季选择器到达 2018–2025 各季页（URL 形式 `copa-libertadores-YYYY/`）；本轮搜索页亦见解放者杯相关条目。
- **blocker 原文（本轮搜索，betexplorer.com 站内页脚/登录框）**：
  > "Register for free" / "Login"
  > "If you have forgotten your username and/or password on BetExplorer.com, enter your e-mail address used in registration."
  即：注册免费，登录只用于个性化（关注联赛、偏好博彩公司等）；**未发现查看赔率的付费墙**。条款页 `https://www.betexplorer.com/terms-of-service.php` 本轮仅在搜索中出现，未单独打开核对 scraping 条款，**记为本轮未复核**。
- **免费层能看到什么**：结果表与单场页单值价格（上一单：2025、2024 结果表渲染出数值；2025 决赛单场页只渲染 Stake.com 一家；2023/2022/2018 所见淘汰赛表为空；2021/2020/2019 只查了总览页决赛行，未开全量结果页，不能断言整季为空）。页脚称赔率服务由 OddsPortal 合作提供。
- **opening/closing 语义**：页内无 Opening/Closing 标注；单值只能标 phase=unspecified，不得标 opening/closing。
- **本单可用性**：✅ 可用（人工/浏览器核验路径），但产出是单值、博彩公司常为 null，且 2021/2020/2019 全量结果页与 2 行结果表博彩公司核查仍是上一单遗留 pending_work。

### 1.4 NowGoal（含静态文件与渲染页）—— 免费公开可达，无登录/付费/密钥墙

- **覆盖核实（本轮确认）**：本轮打开 `https://football.nowgoal.net/league/89`，页标题即 "2026 Copa Libertadores Schedule, Fixture, Latest Results"，确认联赛页 89 = 解放者杯（当前季默认 2026）。上一单的 `?season=2024` 季页参数**本轮未复核**。
- **本轮文本层实测**：打开后只返回骨架——时区选择器、赔率格式选择器、Schedule / Standings / Statistics / ODDS STATS 等空章节标题，**无任何 fixture 行、无任何赔率值**。与上一单“文本层只能抓到骨架”一致，复核确认。
- **blocker**：无登录/付费/密钥墙；blocker 是技术性的——(1) 文本层抓不到数据，需实时浏览器渲染（上一单已验证渲染路径：联赛页、match 页 `https://www.nowgoal.net/match/live-2661153`、赔率总览 `https://www.nowgoal.net/oddscomp/2661153`、1x2 页 `https://www.nowgoal.net/1x2-odds/2661153`）；(2) 静态文件路线已失效：上一单 s89_en.json 在 nowgoal.net / nowgoal2.top 上 404，1x2.nowgoal50.com DNS 失败，**retry_after 2026-10-29**（上一单登记，本轮未到重试日，不重撞）；(3) 89 与 sclass 的对应（s89）上一单即未验证，本轮仍未验证。
- **opening/closing 语义**：页内只有 All/Initial/Live 筛选器，**无 opening/closing 定义**。按 2026-10-22 纠正（已写入 AGENTS.md）：Initial 只是数据流首次捕获，一律标 initial_first_capture，不得标 true_opening；Live/最新价不得标 closing。
- **本单可用性**：✅ 可用（渲染页路径），但产出只能是 Initial/Live 单值（phase=unspecified），且上一单只观测到 2661153 一场的 Bet365 两组值，其余 146 家未提取，是遗留 pending_work。

### 1.5 Football-Data.co.uk —— 免费公开可达，但无覆盖（本轮复核确认）

- **覆盖核实（本轮确认）**：打开 `https://football-data.co.uk/data.php` 全文 143 行：Main Leagues 11 个欧洲联赛 + Extra Leagues 16 个各国国内联赛（含阿根廷 Primera Division、巴西 Serie A），**全文无 Copa Libertadores / CONMEBOL 条目**。上一单“无覆盖”断言**本轮确认**。
- **blocker 原文（官方数据页，本轮打开）**：
  > 全部 FREE，但用途限 "private individuals only"，且 "NOT commercial or data training products using automated bots/scrapers/AI"
  > 赔率口径：第一套在市场开盘后按 fixtures 页指定时间采集，第二套为 closing odds（列名含 `C`），Pinnacle closing 可追溯至 2012/13；并警告自 2025-07-23 起 Pinnacle 公共 API 不可靠、其赔率系统性过时、不再计入市场平均/最高价。
- **本单可用性**：❌ 不可用——不是付费问题，是**源级无覆盖**：付费也拿不到解放者杯。且站方禁 bot/scraper/AI 的商业/数据训练用途，上一单因此未下载其任何 CSV，本单同样不下载。

### 1.6 The Odds API —— 需付费 + 需密钥，且官方联赛清单未列出解放者杯

- **覆盖核实（本轮确认未列出）**：官网首页 `https://theoddsapi.com/`（本轮打开）列出的足球覆盖为 EPL、欧冠、欧联、西甲、德甲、意甲、法甲、荷甲、英冠及 2026 世界杯，**未列出 Copa Libertadores**；官方 FAQ（theoddsapi.com，本轮搜索）列出的足球联赛为 "English Premier League, Champions League, Europa League, La Liga, Bundesliga, Serie A, Ligue 1, Eredivisie, EFL Championship, Liga MX, and MLS"，同样**没有解放者杯**。解放者杯 sport key 是否存在**本轮未验证**（需 key 才能调 sports 端点，本单禁凭证），不得凭首页/FAQ 断言“绝对没有”，但**不能把它列入可用计划**。
- **blocker 原文（官方首页，本轮打开）**：
  > "Free $0/month (25 requests/day, NFL/NBA/MLB h2h only)"
  > "Professional $29/month (20,000 requests, 25+ sports)"
  > "Business $99/month (200,000 requests, historical odds archive, 26 sports)"
  > 官方 FAQ："Historical archive access and edge detection are available for all soccer leagues on the Business plan." / "Authentication is a single x-api-key HTTP header on every request"
- **第三方传闻（标注 unverified）**：历史回溯至 2020 年、历史查询 10 倍信用等说法未经官方文档核实，不采信。
- **本单可用性**：❌ 不可用。免费档无足球；历史档在 Business 付费墙 + 密钥墙内；且解放者杯是否在列都未验证。

### 1.7 OddAlerts —— 需付费 + 需密钥，解放者杯覆盖未验证

- **覆盖核实（本轮未验证）**：官方 API 页 `https://www.oddalerts.com/football-data-api`（上一单打开、本轮搜索复核）**未列出赛事清单**，因此 OddAlerts 是否覆盖解放者杯**本轮仍未验证**，不得写成已确认有覆盖。
- **blocker 原文（官方 API 页）**：
  > "Is there a free football API plan? No. API access comes with the Advanced plan, or with a one-off 48-hour Advanced Day Pass for £9.99 if you want to try it first. A free OddAlerts account still gets you the tools on the website."
  > "Opening, closing and peak odds are kept indefinitely. Full tick-by-tick odds movement is kept for 21 days."
  > "Add your api_token as a query parameter on every request. Tokens allow 300 requests per minute… Going over returns HTTP 429."
  > 8 家博彩公司：Pinnacle、Bet365、1xBet、William Hill、Betfair Exchange、Kambi、Betano、FanDuel；API 在 Advanced 计划内，£69.99/月。
- **本单可用性**：❌ 不可用。付费墙 + 密钥墙双重阻断；且覆盖未验证，即使将来付费也须先核赛事清单。

### 1.8 API-Football —— 需密钥；且 7 天保留期使历史赔率在任何计划下都拿不到

- **覆盖核实（本轮确认）**：官方新手指南（api-football.com，本轮打开）明文：
  > "API-Football covers more than 1 200 leagues and cups worldwide, from the Premier League and La Liga down to the Kazakh Premier League and the Copa Libertadores."
  联赛覆盖有，但赔率端点另有保留期限制（见下）。
- **blocker 原文（官方指南，本轮打开）**：
  > "The free tier gives you 100 requests per day and access to every endpoint without exception. … Pro plan at $19/month gives you 7,500 daily requests, Ultra at $29/month gives 75,000, Mega at $39/month gives 150,000. All plans include all endpoints, all data types, no paywalled features."
  > "Authentication happens through a single request header: x-apisports-key set to your API key."
  > "**The 7-day history limit is the most important thing to know about this endpoint.** Only the last seven days of odds data is retained. Query for odds on a fixture from eight days ago and you'll get nothing back. This is by design, not a bug…"
  > "/odds endpoint paginates at 10 per page."
- **上一单冲突说法的裁决（本轮部分解决）**：上一单记录第三方存在“全计划有 pre-match odds”与“7 天保留”两种冲突说法；本轮官方指南同时证实两者——**全计划确实都有 /odds 端点，但只保留最近 7 天**。因此 2018–2025 历史赔率在 API-Football **任何计划下都拿不到**，这不是付费能解决的问题。
- **本单可用性**：❌ 不可用。双重阻断：(1) 本单禁动用已有 connector 额度、禁凭证；(2) 即使有 key，7 天保留期也使目标年份赔率为零。上一单“赔率端点对旧场的保留期与语义未验证”一项，**本轮修正为已验证：保留期 7 天，语义为 pre-match 价**。

### 1.9 Kaggle / GitHub 公开数据集 —— 需登录（Kaggle 下载）/ 免费公开（GitHub 浏览），内容未验证

- **本轮检索结果**：未找到可验证的解放者杯 1X2 批量 CSV。
  - Kaggle "Brazilian Soccer Database"（ricardomattos05）自述覆盖 Brasileirão、Libertadores、Sudamericana、Copa do Brasil，但描述中**未提赔率列**，且“match statistics”列为下一步计划；赔率存在性**未验证**，Kaggle 下载需账号。
  - Kaggle "70+ Football Leagues Dataset 2019-2023" 自述含 "Match Odds for 1X2 and O/U 2.5 Goals"，但是否含解放者杯**未在描述中确认**，下载需账号。
  - GitHub awesome-football 清单与 gist 通用源表均未指向解放者杯赔率集；Scribd 出现的莫扎特投注单 PDF 是单期投注单，不是可审计历史数据集，不列入。
- **本单可用性**：⚠️ 仅列为待验证线索。需登录下载 + 逐文件验赔率列、赛季覆盖、博彩公司标注后才能进入计划；本轮不承诺任何一个数据集可用。

### 1.10 OpenFootball —— 免费公开可达（CC0），只有赛程/赛果，无赔率

- **覆盖核实（本轮确认）**：打开 `https://github.com/openfootball/south-america`，公开仓库（Public，CC0-1.0，93 stars），根目录含 `copa-libertadores` 目录；README 自述 "Free open public domain football datasets"、"datasets in the Football.TXT format for match schedules, results and more"。
- **blocker**：无登录/付费/密钥墙；blocker 是**字段缺失**：football.db schema 只有赛程/赛果，无赔率字段（上一单结论，本轮仓库 README 未提赔率，与之相符）。分季文件覆盖年份本轮未逐个打开，记为未复核。
- **本单可用性**：✅ 可用，但只能作 fixture 交叉核对上下文，不能作赔率证据。

### 1.11 SoccerPunter —— 免费公开可达（页面可爬取），H 按钮全量历史门控未复核

- **覆盖核实（本轮确认）**：搜索见多场解放者杯 live-odds 页（Toluca vs Nacional、Libertad vs Sport Boys、Grêmio vs Aurora、Grêmio vs Caracas、2 de Mayo vs Alianza Lima（2026，超出范围，仅证覆盖存在）及 Racing Club vs Guaraní 的 tipster 行），页模板含 Pre-Match / 1X2 / Asian Handicap 等市场与 "Copa Libertadores Form" 栏。
- **blocker 原文（本轮搜索，soccerpunter.com live-odds 页）**：
  > "It consists of the opening odds and the daily fluctuation. … To view the odds history and archive, simply mouseover or click on H button."
  > 博彩公司栏含 "Bet365 Premium"、"Winner Premium"、"Vulcanbet Premium"、"Singapore Pools Premium"——部分博彩公司标 Premium，是否 H 按钮全量历史需 Premium 会员**本轮未复核**，不得断言免费可拿全量。
  > "All soccer bets for Fixed Odds (1X2) apply only to the full 90 minutes play of match results unless otherwise stated. This includes injury time goals but not extra-time (ET) score and golden goal or penalty shoot-outs."——1X2 的 90 分钟口径有页内定义，可用。
- **opening/closing 语义**：页内称 opening odds + daily fluctuation，但**无时间戳定义、无 closing 定义**；按母请求口径，仍只能标 unspecified，不得标 opening/closing。上一单意甲批次曾用 SoccerPunter 批量抓取（浏览器任务），但本单的解放者杯 H 按钮门控与批量可行性**本轮未复核**。
- **本单可用性**：✅ 可用（页面浏览路径），但批量与 H 按钮全量历史待浏览器任务验证后才能承诺；单页骨架本身不含赔率值。

---

## 2. 最大的 3 个 blocker（按致命程度排）

1. **付费 + 密钥墙封死全部能定义 opening/closing 的批量源**。5DollarFootballAPI（官方页标注联赛为 Pro and Ultra；tick 历史的 Ultra 门槛为第三方说法，unverified）、OddAlerts（官方：无免费 API 计划，Advanced £69.99/月或 £9.99 48 小时 Day Pass + api_token）、The Odds API（官方：历史档案在 Business $99/月档 + x-api-key）。三者是仅有的、文档定义了 opening/closing 的批量源，全部在付费墙内；本单禁购买禁凭证，故**批量 opening/closing 路径整体封死**，不是“下一步去订就行”。
2. **API-Football 的 7 天保留期：付费也无解**。官方指南明文：只保留最近 7 天赔率，8 天前的查不到，"This is by design"。2018–2025 历史赔率在该源任何计划下都是零，与额度无关；且本单禁动用已有额度。这是唯一一个“花钱也拿不到”的批量源 blocker。
3. **条款墙 + 语义墙 + 源级无覆盖三重叠加**。OddsPortal 官方条款 §2.11 明文禁止未经书面同意的 scraping/aggregation 与自动化请求（人工浏览可达，批量提取不合规）；NowGoal 的 Initial/Live 无 opening/closing 定义（Initial 只是首次捕获），渲染页单值永远只能标 unspecified；Football-Data.co.uk 源级无解放者杯覆盖（本轮复核确认），且站方禁 bot/scraper/AI 用途——付费也无解。三者合计说明：免费侧即使能看到价格，也**拿不到母请求口径的 opening/closing 行**。

---

## 3. 不花钱、不凭证能拿到的最大范围（诚实版）

### 3.1 能拿到：fixture 锚点（非赔率证据）

- CONMEBOL 官方 PROGRAMA 行（上一单 38 行，唯一 pre-match 合格行；版本日期均早于开球）——复用时保留原口径与 partial 标注。
- FBref / SoccerAssociation 候选行（上一单 1,241 / 1,227 行；须保留 not_eligible_post_match_page / 候选标注，不得当 pre-match 证据）。
- OpenFootball south-america 仓库 copa-libertadores 目录（公共 CC0，赛程/赛果，无赔率）——作 fixture 交叉核对。

### 3.2 能拿到：赔率单值，但一律只能标 phase=unspecified，不得标 opening/closing

- **BetExplorer 渲染页**：结果表与单场页单值（上一单：2025/2024 结果表数值、2025 决赛 Stake.com 一家；博彩公司常为 null，保留 null 不推断）。
- **NowGoal 1x2 渲染页**：Initial/Live 两组值（上一单：2661153 一场 Bet365 两组值；其余 146 家未提取为遗留 pending_work，需主代理派浏览器任务）。
- **SoccerPunter live-odds 页**：opening/daily fluctuation 描述与页骨架（H 按钮全量历史门控未复核，批量不可承诺；1X2 的 90 分钟口径有页内定义）。
- **OddsPortal 渲染页**：上一单样本产出为 0（0 家博彩公司/空表/404），免费可浏览但对解放者杯样本无赔率产出；本轮未复核具体场次，不把“0”推广为全量结论。

### 3.3 明确拿不到（在不花钱不凭证的前提下，根本拿不到）

- 任何带时间戳 tick 的 opening/closing 历史（5Dollar Ultra、OddAlerts Advanced/Day Pass、The Odds API Business 历史档——全部在付费 + 密钥墙内）。
- Football-Data.co.uk 的解放者杯赔率（源级无覆盖，付费也无解）。
- API-Football 的 2018–2025 赔率（7 天保留期，任何计划、任何额度都拿不到）。
- The Odds API 的解放者杯赔率（官方联赛清单未列出，sport key 未验证，不能列入计划）。
- OddAlerts 的解放者杯赔率（覆盖未验证；且 API 本身在付费墙内）。
- 任何 Kaggle/GitHub 解放者杯 1X2 批量集（本轮未找到可验证集；候选集需登录下载 + 逐文件验证后才能谈）。

---

## 4. 不花钱不凭证的替代方案清单（按优先级排序）

| 优先级 | 方案 | 产出与口径 | 前置条件 / 遗留项 |
|---|---|---|---|
| P0 | 复用上一单 fixture 锚点：CONMEBOL 官方 PROGRAMA 38 行 + FBref/SA 候选行 | fixture 台账，不作赔率证据；保留原 partial/候选标注 | 无；复用时不得把候选行升级为 pre-match 证据 |
| P1 | BetExplorer 渲染页逐场核验（结果表 + 单场页） | 单值，phase=unspecified，博彩公司 null 时保留 null | 补 2021/2020/2019 全量结果页；补 2 行结果表博彩公司核查（上一单 pending_work） |
| P2 | NowGoal 1x2 渲染页补提取（主代理派浏览器任务） | Initial/Live 单值，标 initial_first_capture / live，不得标 opening/closing | 补 2661153 其余 146 家；静态文件路线 retry_after 2026-10-29 前不重撞 |
| P3 | SoccerPunter live-odds 页验证（主代理派浏览器任务） | opening/daily fluctuation 描述值，phase=unspecified；1X2 按页内 90 分钟口径 | 先验证 H 按钮全量历史是否需 Premium、解放者杯页批量可行性；本轮未复核，不得提前承诺批量 |
| P4 | OpenFootball copa-libertadores 目录作 fixture 交叉核对 | 赛程/赛果上下文，无赔率 | 逐文件确认年份覆盖（本轮未逐个打开） |
| P5 | Kaggle/GitHub 候选集内容核验 | 仅当某文件被验证含 1X2 赔率列 + 2018–2025 覆盖 + 博彩公司标注时才进入计划 | 需登录下载（Kaggle）；逐文件验证；本轮未找到可验证集，不承诺 |
| —（不列入） | 5Dollar / OddAlerts / The Odds API 付费档 | — | 本单禁购买禁凭证；付费档不写成“下一步去订就行” |
| —（不列入） | API-Football 任何计划 | — | 禁凭证 + 7 天保留期使目标年份为零 |
| —（不列入） | OddsPortal 批量抓取 | — | 条款 §2.11 禁 scraping/aggregation（未经书面同意）；仅人工浏览参考 |
| —（不列入） | Football-Data.co.uk | — | 源级无覆盖；站方禁 bot/scraper/AI 用途 |

---

## 5. 给主代理的交接要点

- 四档计数：免费公开可达 6、需登录 1、需付费 3、需密钥 1，合计 11，无遗漏。
- 最大 blocker 是第 2 节的 3 项；其中第 1 项（付费墙封死批量 opening/closing）与第 2 项（API-Football 7 天保留）共同决定：**母请求 Q2 口径的 opening/closing 行在不花钱不凭证的前提下是 0 行可预期**，免费侧最大产出只能是 phase=unspecified 的单值。
- 本文件所有“上一单结论”引用处均已标注复核状态；未复核项（5Dollar Ultra 门槛与 opening/closing 文档原文、OddAlerts 解放者杯覆盖、The Odds API sport key、BetExplorer 条款 scraping 细则、SoccerPunter H 按钮门控、NowGoal 季页参数与 s89 对应、OpenFootball 分季文件覆盖）不得在汇总时升级为已确认。
- 本 C 路未写 `repo/responses/`，汇总与回执由主代理负责。
