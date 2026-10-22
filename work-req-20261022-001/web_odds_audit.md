# req-20261022-001 B 路审计：OddsPortal / BetExplorer 等网页历史赔率源探查

> 角色：B 路（网页历史赔率源探查），只收集赔率证据，不做预测，不返回比分/进球/赛果/晋级/概率/模型方向。
> 结论先行：**本路验证行数 = 0 行。** `web_odds_rows.jsonl` 为空文件（0 字节、0 行），不是漏写——三站的文本抓取层均未暴露任何一家公司的 FT 1X2 赔率表，故无一行满足“源内明确字段 + 可定位 + 可唯一对应场次”的成行标准。搜索摘要里出现过的数字一律未转成行（见 §6）。
> 检索日期：2026-10-22（UTC+8 下午会话）。文本抓取层不暴露 HTTP 状态码与精确抓取时刻，故本审计不编造任何 HTTP 状态码与 retrieved_at 分秒；凡写“可达”均指页面外壳/导航/广告层被返回，而非数据表被返回。

## 1. 逐站结论

### 1.1 OddsPortal — 可达外壳，数据表为零（parse_failed，JS 渲染障碍）

- 竞赛页（2025，verbatim URL）：
  - `https://www.oddsportal.com/football/south-america/copa-libertadores-2025/`
  - 文本层仅有导航 Next Matches / Results / Standings 与一段宣传文案（声称结果可回溯至 2005、含“赔率”），无任何场次行、无任何赔率值。
- 结果页（2025，经竞赛页真实外链 Results 进入，非猜测 URL）：
  - `https://www.oddsportal.com/football/south-america/copa-libertadores-2025/results/`
  - 文本层只有博彩广告（DraftKings / bet365.us / BetMGM.us），**0 场次行、0 赔率值**。结果表是 JS 渲染的，文本层抓不到。
- 赛季 standings 页（2022，verbatim URL）：
  - `https://www.oddsportal.com/football/south-america/copa-libertadores-2022/standings/ln7hLyD2/`
  - 文本层只有赌博求助 disclaimer，积分表本身未出现。
- 单场页（2020，verbatim URL）：
  - `https://www.oddsportal.com/pl/football/south-america/copa-libertadores-2020/libertad-palmeiras-jLk7eKxt/`
  - 文本层只有 7 行 “Reklama”（广告），无队名、无日期、无赔率表。单场赔率表同样不在文本层。
- H2H 页（Huachipato – Carabobo，verbatim URL）：
  - `https://www.oddsportal.com/football/h2h/carabobo-6cmntinM/huachipato-SlhZpIaP/`
  - 文本层只给了一条 **2026-02-24** 的场次（超出本单 2018–2025 范围，已排除，不成行），并写明“Match links open with the event id in the URL hash (for example #MHaHJHqA:1X2;2)”——即单场赔率藏在 URL hash 驱动的 JS 视图后，文本层无法进入。这是本路在 OddsPortal 上最直接的 JS 障碍证据。
- 登录墙/付费墙：**本路未观察到**。文本层未出现登录提示、付费提示或 403/404 文案，故不把障碍定性为登录墙；已证实的障碍是 JS 渲染 + hash 导航。是否另有登录墙，需真浏览器任务实测后才能说。
- Bookmaker 清单：**无一可验证**。广告中出现的 DraftKings / bet365 / BetMGM 是赞助广告位，不是赔率表中的公司行，绝不能把它们列为本单的 bookmaker。
- Opening / Closing 语义：**在 OddsPortal 自身被抓到的页面里无任何定义、无任何 opening/closing 标注、无任何赔率格**。第三方爬虫教程（ScrapeHero、WebHarvy）描述“closing 显示在单场页、opening 只在鼠标悬停弹窗里”——那是第三方说法，未在本路抓到的任一 OddsPortal 页面上验证，**不能据此给任何行标 phase=opening/closing**。本路 0 行，故无语义误标。

### 1.2 BetExplorer — 结果表结构可达，但 1/X/2 格全空；单场页亦无赔率表（parse_failed）

- 赛季页（2005，仅作结构探查；2005 不在本单范围，其行不计入）：
  - `https://betexplorer.com/football/south-america/copa-libertadores-2005/`
  - 文本层有 Summary / Results / Fixtures / Stats / Head-to-head H2H 导航与 Main / Play Offs 分页，但只显示决赛两行，且 1 / X / 2 列全空。
- 结果页（2005，经赛季页真实外链 Results 进入）：
  - `https://www.betexplorer.com/football/south-america/copa-libertadores-2005/results/`
  - 文本层渲染了从决赛到 2 月初早期轮次的完整结果行（阶段标签 + 队名 + 日期齐全，最早日期为 01.02.2005），但 **全部行的 1 / X / 2 格均为空**。页脚帮助文案声称“Click on match detail and find out … 1X2 … odds offered for the game”——即赔率在单场详情页，但：
- 单场页（2005 决赛，https://www.betexplorer.com/football/south-america/copa-libertadores-2005/sao-paulo-athletico-pr/zwcXQ2aT/）：
  - 文本层有队名、一个 “1X2” 标题、场次时间 `2005-07-14T23:55:00+02:00`，但 **无任何公司、无任何赔率值**。单场赔率表同样不在文本层。
- 本单范围（2018–2025）的 BetExplorer 赛季页：**搜索未返回**。本路只见到 2005 赛季页、2013 单场页与一张赛季未在文本层标明的 standings top_scorers 页（`ts=pzk4jfy0`），均不在 2018–2025 范围内。**没有猜测 2018–2025 赛季 URL**（如 `…/copa-libertadores-2024/` 这类拼接一律未用），故 2018–2025 在 BetExplorer 的覆盖是“未定位”，不是“已证实不存在”。
- Bookmaker 清单：**无一可验证**（文本层赔率区为空；广告中的 bet365 / FanDuel 是赞助文案，不是赔率行）。
- Opening / Closing 语义：BetExplorer 自身被抓到的页面里**无任何 opening/closing 定义与标注**，无法标 phase。

### 1.3 Oddspedia（“等”站之一）— 纯编辑页，无赔率表（parse_failed）

- `https://oddspedia.com/football/south-america/copa-libertadores/odds`
- 文本层是市场类型科普（1X2、Outright、BTTS、Correct Score 等）与“比较几十家公司赔率”的宣传，无任何场次赔率表；Events 一节只列 2026 年场次（超出范围，已排除）。
- Bookmaker：文案点名 bet365、Pinnacle 为“值得考虑的公司”，但无任何赔率行与之对应，不能列为本单 bookmaker。
- Opening / Closing 语义：无定义、无标注。

## 2. 按赛季 × 阶段 × bookmaker × phase 行数

| 赛季 | 阶段 | bookmaker | phase | 行数 | 状态 |
|---|---|---|---|---|---|
| 2018–2025 全部 8 季 | 全部阶段（资格赛 / 小组赛 / 十六强 / 四分之一决赛 / 半决赛 / 决赛） | （无可验证公司） | opening / closing / unspecified | 0 | parse_failed（文本层无赔率表） |
| — | — | — | — | — | expected = null（无权威源公布应有场次数；本路不以任何已发现行数作分母） |

- “0 行”适用于本路探查的三站全部范围；不是抽查结论——OddsPortal 结果页、单场页、BetExplorer 结果页与单场页的赔率区在文本层均为系统性空白，不是某一页偶然缺失。
- 本路未使用上一单的 2,506 行作分母、作 expected，也未用其行来“认领”任何赔率观测（本路本就无观测可认领）。

## 3. 未覆盖清单（全部 8 季 × 全部阶段 × 全部公司）

- OddsPortal：2018、2019、2020、2021、2022、2023、2024、2025 各季的资格赛、小组赛、十六强、四分之一决赛、半决赛、决赛，opening 与 closing 均未覆盖。2020 单场页与 2025 结果页已证实文本层空白；其余季连可验证的单场/结果页 URL 都未在搜索中返回（不猜 URL）。
- BetExplorer：2018–2025 各季各阶段、opening 与 closing 均未覆盖；2018–2025 赛季页本身未定位（见 §1.2）。
- Oddspedia：2018–2025 各季各阶段均未覆盖（仅见编辑页与 2026 场次）。
- 共同缺口：**没有任何一家公司**的 FT 1X2 赔率在本路得到验证；quote timestamp / 快照语义、source fixture ID、kickoff/timezone、官方阶段/轮次等字段因此全部无从填写。

## 4. 最大障碍（按致命程度排）

1. **JS 渲染 + hash 导航（OddsPortal）**：结果表与单场赔率表不在文本层；H2H 页自述单场链接以 URL hash 中的 event id 打开（`#…:1X2;2`）。文本抓取到此为止，继续用文本层重复抓同一批页不会有新结果。**需要真浏览器任务**（JS 渲染 + 悬停弹窗才能看到 opening 价，据第三方描述；该描述本身亦需在真浏览器里验证）。
2. **赔率区系统性空白（BetExplorer）**：结果页与单场页的文本层都渲染了结构、唯独赔率格为空。同样需要真浏览器任务验证赔率表是否在 JS 层、以及单场页是否区分 opening/closing。
3. **2018–2025 赛季页未定位（BetExplorer）**：搜索只返回 2005/2013 页；不猜 URL 的前提下，须经站内导航（从已验证的赛季页导航或站内赛季选择器）或真浏览器站内检索定位各季页。
4. **语义无源可依**：即使真浏览器拿到了数字，opening/closing 仍须以源自身的标注为准；latest/current 价不是 closing，单个中间价既不是开盘也不是收盘。本路未在任何一站看到源自身的 opening/closing 定义，故后续真浏览器任务必须把“源内是否标注 opening/closing”作为首要核查项，而不是默认把页面主价当 closing、把悬停价当 opening。

## 5. 明确不做的事（本路边界自查）

- 未付费、未碰任何付费额度、未绕登录墙/反爬墙、未猜任何 URL（所有打开的 URL 均来自搜索结果原文或已打开页面的真实外链）。
- 未用上一单 FBref / SoccerAssociation 的行认领场次，未把 2,506 行当分母或 expected。
- 未把广告商（DraftKings、bet365、BetMGM、FanDuel）当作赔率 bookmaker。
- 未把搜索摘要中的数字转成行（见 §6）；未返回任何比分/赛果/概率/预测。

## 6. 见过但未转成行的材料（ambiguous / 未采用队列，0 行成行）

| 材料 | 为什么未成行 |
|---|---|
| BetExplorer H2H 页搜索摘要中的带日期 1X2 数字行（如 Newells Old Boys – Boca Juniors 页） | 摘要未给公司名、未给 phase 语义、未给可验证的 field_locator；且该页为 2013 赛季标签、球队为国内联赛队，不在 2018–2025 Libertadores 范围内；摘要数字不是已打开页面的实测字段。 |
| SportyTrader / Radio Times 等预测页给出的 bet365 单场价（如 2024 决赛） | 预测/新闻页的“当前价”，无 opening/closing 定义、无 quote timestamp、无源内场次 ID；单家新闻价不能当作历史赔率快照，且有赛后发布时间混杂风险。 |
| SoccerPunter 单场 odds movement 页的搜索摘要（含多行带时间戳的价目表） | 不属于本路主探查的两站，且摘要中公司名被抹去、价目为美式赔率 + 涨跌幅、opening/closing 未标注；可作为**后续独立一路**的候选线索，但本路未打开其页面、未验证字段，故不转成行、不计入本路行数。 |
| BetsAPI 2025 场次列表 | 只有场次与赛果倾向信息，无公司赔率表；且含赛果字段，按本路规则丢弃、不采用。 |
| OddsPortal / Oddspedia 文本层出现的 2026 场次 | 超出 2018–2025 范围，一律排除。 |

## 7. 给主代理的下一步（需真浏览器或独立一路，非本路可完成）

1. **OddsPortal 真浏览器任务**：用真浏览器打开已验证的 2025 结果页与 2020 单场页，核查 JS 渲染后的赔率表是否存在、公司清单为何、页面是否自带 opening/closing 标注、opening 是否确为悬停弹窗；先以 1–2 个单场页验证，再决定是否批量。
2. **BetExplorer 真浏览器任务**：用真浏览器经站内导航定位 2018–2025 赛季页（勿猜 URL），核查单场页赔率表与 opening/closing 标注；先以 1 个单场页验证文本层空白是否仅为渲染问题。
3. **SoccerPunter 独立一路（可选）**：其单场 movement 页在搜索索引中呈现带时间戳的价目表，值得单独一路打开页面验证公司、价目格式与 opening 定义；注意其价目含赛后时间戳，需严格区分 pre-match 快照与 in-play 价。
4. 以上任一路若拿到数字，仍须按本单硬规则执行：phase 只有源明确定义时才标 opening/closing，否则标 unspecified；无法唯一对应场次的观测进 ambiguous 队列，不硬指派；expected 保持 null。

## 8. 交付文件说明

- `web_odds_rows.jsonl`：空文件，0 行。字段规范（供后续有行时复用）：season_year、source_fixture_id（仅源明确发布时）、home_team_source_label、away_team_source_label、match_date、kickoff、timezone（仅源发布时）、official_stage、official_round（仅有证据时）、bookmaker（原文）、market=FT 1X2、phase（opening/closing 仅源明确定义时，否则 unspecified）、decimal_home、decimal_draw、decimal_away、quote_timestamp_or_snapshot_semantics、source_url、final_url、retrieved_at（UTC+8）、http_status、field_locator、source_sha256（有字节时计算，否则 null 并注明）、fixture_match_evidence、status、status_reason。
- `web_odds_audit.md`：本文件。
