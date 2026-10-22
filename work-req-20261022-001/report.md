# req-20261022-001 交付报告：Copa Libertadores 2018–2025 历史 pre-match FT 1X2 赔率证据

## 结论先行（先说清楚这单到底拿到什么）

- **符合“开盘/收盘”定义的赔率行：0 行。** 没有任何一个被核查的源，为它展示的价格给出开盘或收盘的明确定义。
- **观察到的、但只能标 phase=unspecified 的价格行：5 行。** 它们是真实渲染页上看到的价格，不是批量覆盖：NowGoal 1 场比赛的 Bet 365 Initial + Live 各 1 行，BetExplorer 2025 决赛 Stake.com 1 行、2025/2024 结果表各 1 行（结果表行未标明博彩公司）。
- **批量源：0 行。** 唯一实证有覆盖且语义明确的批量源（5DollarFootballAPI）被 Ultra 付费墙挡住，本单未付费、未用密钥；Football-Data.co.uk 实证根本没有解放者杯覆盖；NowGoal 静态批量路线未验证；OddsPortal 渲染后仍是 0 家博彩公司。
- **这 5 行不是“解放者杯赔率数据库”，只是一次源审计附带的 5 个已验证样本。** 任何把它们当成开盘价、收盘价或赛季覆盖来用的做法，都是对本单的误读。

## 5 行明细（fixture_odds_rows.jsonl）

| 赛季 | 源 | 场次（源标签） | 博彩公司 | 源内标签 | 1 / X / 2 | 状态 |
|---|---|---|---|---|---|---|
| 2024 | NowGoal 1x2 页（matchId 2661153） | Colo-Colo vs River Plate（Quarterfinals） | Bet 365 | Initial | 3.00 / 3.10 / 2.50 | partial |
| 2024 | NowGoal 1x2 页（matchId 2661153） | 同上 | Bet 365 | Live | 3.30 / 3.00 / 2.40 | partial |
| 2025 | BetExplorer 单场页 | Palmeiras vs Flamengo RJ（Final） | Stake.com | Odds Comparison (1X2) | 3.55 / 3.00 / 2.42 | partial |
| 2025 | BetExplorer 结果表 | Palmeiras vs LDU Quito | 未标明 | 结果表 1/X/2 | 1.22 / 7.40 / 14.00 | partial |
| 2024 | BetExplorer 结果表 | Atletico-MG vs Botafogo RJ | 未标明 | 结果表 1/X/2 | 4.33 / 3.19 / 1.90 | partial |

全部 5 行 phase 均为 unspecified，quote_timestamp、source_sha256、http_status 均为 null（渲染页不提供稳定字节哈希与源 HTTP 状态，未编造），时区均为 null（无源标注时区）。

## 语义铁律（本单最重要的一句话）

- **NowGoal Initial ≠ 开盘价。** Initial 只是该数据流首次捕获的价格，页面本身没有把它定义为市场开盘。上一单荷甲批次曾用 field_semantics=true_opening 标签，**本单明确不继承、并纠正它**：以后 NowGoal Initial 一律标 initial_first_capture，不得写 true_opening。
- **Live / 最新价 ≠ 收盘价。** NowGoal 页面根本没有 Closing 一词；BetExplorer 页面也没有 Opening/Closing 标注。单个渲染价格既不是开盘也不是收盘。
- **结果表价格的博彩公司不能猜。** BetExplorer 结果表不标明博彩公司，2025 决赛那行能标 Stake.com 是因为单场页只渲染了这一家且数值一致；其余两行结果表行博彩公司保持 null，待单场页核查（见 UQ）。

## 逐源审计

- **NowGoal 文本路线**：本机 shell 连 example.com 都超时，浏览器文本层也抓不到上一单已验证的荷甲赛程 JSON；解放者杯 sclass 在本地文件与搜索索引中均无记录，未猜 URL。结论是“本环境不可达”，不是“NowGoal 已下线”。
- **NowGoal 实时浏览器**：联赛页 league/89（2024 季页）已找到，示例场 matchId 2661153 的 1x2 页列出 147 家博彩公司，但报告中只观测到 Bet 365 两组值，其余 146 家未提取、不得补编。89 只是联赛页编号，与 sclass 的对应仅为与荷甲 league/16 对 s16 的类比，**s89 未验证**：s89_en.json 在现用域名（nowgoal.net / nowgoal2.top）上 404（旧 s16 路径同样 404，故 404 不能证伪 89）；1x2 旧 JS 域名 DNS 失败；页面上未见 game=Array 链接。www.nowgoal.com 本身连不上，nowgoal.net 可用。
- **OddsPortal 文本路线**：parse_failed，赔率藏在 JS/hash 视图后。**实时浏览器渲染后仍为 0**：2025 结果页提示所选博彩公司无赔率；2020 单场页 404；H2H 页空表且明文写 0 家博彩公司。未登录验证（任务禁登录），登录后或换博彩公司选择是否出数仍未知。
- **BetExplorer 文本路线**：parse_failed，结构渲染了、赔率格为空。**实时浏览器**：站内赛季选择器可到达 2018–2025 各季页（URL 形式 copa-libertadores-YYYY/）；结果表在 2025、2024 渲染出数值，2023/2022/2018 所见淘汰赛表为空，2021/2020/2019 只查了总览页决赛行（未开全量结果页，不能断言整季为空）。单场页：2025 决赛只渲染 Stake.com 一家；2023 与 2005 抽查单场页明文称无博彩公司提供赔率。页脚称赔率服务由 OddsPortal 合作提供。
- **5DollarFootballAPI**：唯一实证有覆盖的批量源。数据质量页：解放者杯 league id 3899038422，Pro and Ultra，13 季、自 2015 年起；端点含联赛 fixtures、单场 odds、odds/history（market=1x2，一次一家，ticks 升序）。语义文档明确：bet365 1X2 首条 tick 即 /odds 给出的 opening，closing 为开球前最后一次赛前价、之后冻结，in-play tick 须排除。**但历史查询与 tick history 只给 Ultra**：Free 仅 top-5 联赛，Pro 仅最近 12 个月。未用密钥、未付费，故 0 行。另有赛季标签陷阱：该源标签如 2025/26（约 8 月至次年 5/6 月）与解放者杯自然年届次对不上，取数必须按历届实际日期窗口切片，禁用 ?season= 指派 season_year。
- **Football-Data.co.uk**：实证无覆盖。数据索引页只有国内联赛（巴西 Serie A、阿根廷 Primera Division），全文检索 Libertadores/CONMEBOL 均为 0 命中。且站方条款限制自动化抓取/AI 数据产品，故未下载其任何 CSV。
- **其他批量源**：The Odds API（历史端点需 key 才能核实覆盖，付费传闻未验证）、OddAlerts（付费计划、客户评价说法未验证）、Kaggle/GitHub（未找到可验证批量 CSV）、OpenFootball（无赔率字段，已排除）均未采用。API-Football 已有 Pro 额度本单**故意未动用**（保留期待请求方决定，且其旧场保留期与语义未验证）。

## 未解决队列（14 项，见 unresolved_queue.json）

- blocked：5Dollar Ultra 付费墙（决策门控，非日期门控）；NowGoal 静态文件（retry_after 2026-10-29，须从页面网络请求找真实数据接口）。
- unavailable：Football-Data 无覆盖；OddsPortal 渲染 0 家；BetExplorer 所见空单元格。
- pending_work：BetExplorer 2021/2020/2019 全量结果页；2 行结果表行的博彩公司单场页核查；NowGoal 2661153 其余 146 家 Initial/Live 表提取；API-Football 额度决定；The Odds API / OddAlerts 覆盖核实。
- ambiguous：NowGoal 2661153 日期时区差（任务参考 2024-09-17 vs 页面显示 18-09-2024 08:30，未换算）；联赛编号 89 与 sclass 对应未验证。
- permanent_rule：Initial 不得标 opening、Live/结果表值不得标 closing；不得跨源按队名拼合、不得用上一单 2,506 行作分母或 expected。

## 交付文件（repo/work-req-20261022-001/）

fixture_odds_rows.jsonl（5 行）＋ audit.json ＋ unresolved_queue.json ＋ report.md（本文件）＋ 各路审计（nowgoal_audit.md / web_odds_audit.md / api_odds_audit.md / browser_findings.md）。回执 data.fixture_odds_rows 与 fixture_odds_rows.jsonl 内容一致。上一单 38 行 CONMEBOL 锚点仅作对照，未被用作任何赔率行的证据。
