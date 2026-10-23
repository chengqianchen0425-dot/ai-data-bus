# req-20261023-001 B 路审计：上一单 5 行赔率独立重验 + 新公开源探查

## 结论先行

- **重验通过：0 / 5 行。** 上一单（req-20261022-001）的 5 行赔率在本路均未获得可追溯的源证据确认，因此**一律不复制为有效赔率**，全部剔除并进 unresolved 队列。`odds_reverified_rows.jsonl` 为有意为空的空文件（0 字节），不是遗漏。
- **这不是“5 行全是错的”断言。** 重验使用的是文本抓取层（browser.open），而 NowGoal / BetExplorer 的赔率表是 JS 渲染的：文本层里赔率格系统性为空或为 "-"。文本层既不能证实、也不能证伪上一单实时浏览器观测到的数值。唯一诚实的结论是：**在本路可用通道内证据不足**， live-browser 重验仍需主代理另行派发（本路子代理无真浏览器能力，见末节“需主代理派发”）。
- **新源最大发现：SoccerPunter 确有 2018–2025 范围内的 movement 页，且 2024 年一场有带时间戳的 1X2 tick 表；但 tick 行的博彩公司栏在文本层为空，且赔率是美式格式，因此无法在不推断博彩公司的前提下产出任何行。** 这是结构性障碍，不是缺数据。

## 重验方法（可复现）

- 逐页重新打开上一单 work-req-20261022-001/browser_findings.md 里的 URL（NowGoal 1x2 页、BetExplorer 单场页及 2025/2024 结果表页），用 browser.open 文本层抓取，2026-10-23 晚间（Asia/Shanghai）。
- 每页的文本层转储保存于 `odds_evidence/`（见末节清单与 sha256），转储中出现的比分列/进球者行已按任务规则删除，仅保留场次身份与赔率表结构；转储文件本身不是原始 HTML（文本层不提供原始 HTML），这一点已在每个文件头注明，不得误读为 HTML 证据。
- HTTP status：文本抓取工具不暴露源站 HTTP 状态，全部记 null，不得把工具自身状态误读为源站 200。
- 判定标准：只有当重新抓取的证据中同时出现（队名 + 日期 + 博彩公司 + 1/X/2 值）且与上一单一致时，才算通过；缺任一项即为证据不足；日期等字段不一致时两边都保留、不裁决、不覆盖。

## 上一单 5 行逐行重验结论

| # | 上一单行 | 重验结果 | 证据摘要 | 冲突 / 备注 |
|---|---|---|---|---|
| R1 | NowGoal 2661153，Colo-Colo vs River Plate，2024 Quarterfinals，Bet 365 Initial 3.00/3.10/2.50 | ❌ 未通过（证据不足） | 1x2 页文本层确认页标题与表头、Initial/Live 筛选器与汇总行存在，但博彩公司行全部为空；oddscomp 页确认该场为 Quarterfinals、Bet365 为 12 家公司之一，但全部赔率格为 "-" | 值既未证实也未证伪；Initial 不得标 opening（源无定义），见上一单结论 |
| R2 | NowGoal 2661153，同场，Bet 365 Live 3.30/3.00/2.40 | ❌ 未通过（证据不足） | 同 R1；Live 值在文本层中不存在；页面无 Closing 一词 | 同上；Live 不得标 closing |
| R3 | BetExplorer 2025 决赛，Palmeiras vs Flamengo RJ，Stake.com 3.55/3.00/2.42 | ❌ 未通过（证据不足 + 日期冲突） | 单场页文本层确认场次身份（2025-11-29T22:00:00+01:00，Estadio Monumental, Lima）与 1X2 Stats 标签存在，但无 Odds Comparison 表、无 Stake.com 行、无数值 | ⚠️ 日期冲突（两边保留）：上一单 match_date 2025-11-30（来自上一单实时浏览器结果表日期 30.11.2025）vs 本次文本层结果表 29.11.2025 与单场事件 2025-11-29T22:00:00+01:00。差 1 天的模式与时区显示差一致，但显示时区未被证实，故不换算、不覆盖 |
| R4 | BetExplorer 2025 结果表，Palmeiras vs LDU Quito，博彩公司未标明，1.22/7.40/14.00 | ❌ 未通过（证据不足） | 结果表文本层确认该行存在（Semi-finals - Second leg，31.10.2025），日期与上一单一致，但 1/X/2 格全部为空；博彩公司仍未标明 | 日期一致是唯一吻合项，不足以通过（值缺失） |
| R5 | BetExplorer 2024 结果表，Atletico-MG vs Botafogo RJ，博彩公司未标明，4.33/3.19/1.90 | ❌ 未通过（证据不足 + 日期冲突） | 结果表文本层确认 Final 行与队名存在，但 1/X/2 格全部为空；博彩公司仍未标明 | ⚠️ 日期冲突（两边保留）：上一单 match_date 2024-12-01（上一单实时浏览器结果表日期 01.12.2024）vs 本次文本层 30.11.2024。与 R3 同为 +1 天模式，时区未证实，不换算 |

补充核对（不在上一单 5 行内，但有助于主代理判断）：
- 2024 结果表文本层确认 Colo Colo vs River Plate Quarter-finals First leg 行为 18.09.2024，与 NowGoal 页面显示日期 18-09-2024 一致；上一单任务参考日期 2024-09-17 是另一时区的日期，仍未解决，不换算。
- BetExplorer 单场页的 1X2 标签页（.../IwUrkvRk/1x2/）文本层与主单场页相关部分完全一致，同样无赔率表。

## 按赛季 × 博彩公司 × phase 计数（重验后）

| 赛季 | 博彩公司 | phase | 上一单行数 | 重验通过 | 剔除 / 未解决 |
|---|---|---|---|---|---|
| 2024 | Bet 365（NowGoal） | unspecified（Initial） | 1 | 0 | 1 |
| 2024 | Bet 365（NowGoal） | unspecified（Live） | 1 | 0 | 1 |
| 2024 | 未标明（BetExplorer 结果表） | unspecified | 1 | 0 | 1 |
| 2025 | Stake.com（BetExplorer 单场） | unspecified | 1 | 0 | 1 |
| 2025 | 未标明（BetExplorer 结果表） | unspecified | 1 | 0 | 1 |
| 合计 | — | — | 5 | 0 | 5 |

opening / closing 行：上一单 0 行，本路 0 行（无任何源在本路证据中定义 opening/closing 端点；SoccerPunter 的通用描述“由开盘价与每日波动组成”不是逐行端点定义）。
expected：一律 null（无权威源公布应有场次数或赔率行数）。

## 新公开源探查

### SoccerPunter 单场 movement 页（重点线索，已验证结构、未产出行）

- **存在性（范围内）**：Copa Libertadores 2024 movement 页已直接打开验证：Nacional vs River Plate（https://www.soccerpunter.com/live-odds/19104674/Nacional-vs-River-Plate），Date 07/05/2024，Kick Off 17:00，Venue Estadio Gran Parque Central (Montevideo)，含 1X2 tick 表。2025 movement 页经搜索确认存在（River Plate vs Independiente del Valle；Fortaleza vs Velez Sarsfield），但其搜索摘要中无 tick 表，tick 表是否出现因场次而异，不得假设。
- **tick 表格式（2024 Nacional 页，逐字转储见 odds_evidence/soccerpunter_nacional_river_2024.txt）**：表头 Bookmaker | H | 1 | X | 2 | Updated；共 10 行 tick，时间戳 07/05/2024 15:40–17:00（开球 17:00），值均为美式格式（如 240、275、104、-109、-125），每行附带涨跌百分比。
- **致命障碍 1：博彩公司栏在文本层为空。** 10 行 tick 的 Bookmaker 格全部空白（仅有 "H" 标记，即站内 history 按钮）。页内 "My Bookmakers" 列表（Bet365、10Bet、188Bet、Ladbrokes、Pinnacle、William Hill、Winner、Vulcanbet、Singapore Pools、bwin、Betfair，均标 Premium）是站内通用列表，不是逐行归属，绝不能用它来指派 tick 行。
- **致命障碍 2：同时间戳多行，无法按时间推导单家开盘/收盘。** 16:32 同时出现两行不同数值（240/229/-109 与 260/250/-102），说明各行是不同博彩公司的快照，而非同一家的时间序列。没有博彩公司标签，就无法确定任一家的最早/最晚赛前 tick，也就无法用时间戳确立 opening/closing。
- **致命障碍 3：美式格式。** 值须换算为十进制才符合本单 decimal 字段；换算本身是确定性算术，但无博彩公司归属的换算行仍是不可归属行，故本路未做换算、未产出行。
- **付费边界说明（未测试、不妄断）**：各博彩公司名后标 "Premium"，但本路未登录、未付费、未测试 Premium 是否为查看逐行归属的前提；tick 表本身在文本层可公开读到。因此结论只写“文本层无法归属”，不写“SoccerPunter 须付费才能看 tick”。
- **易混淆项（已隔离）**：SoccerPunter 上另一页 Colo-Colo vs River Plate（https://www.soccerpunter.com/live-odds/18513320/Colo-Colo-vs-River-Plate）是 **2022 届**、Estadio Monumental David Arellano，文本层中无日期、无开球时间、无 1X2 tick 表；它不是 2024 四分之一决赛场（NowGoal 2661153），不得把两页的任何数据混用。另有一页 2026 Junior FC vs Palmeiras 已排除（2026 不在范围）。

### 其他公开源

- 本路未再验证出除 SoccerPunter 外的新免费公开历史赔率源。NowGoal / BetExplorer / OddsPortal 的重验结论见上；5DollarFootballAPI、Football-Data 等上一单结论（Ultra 付费墙、无覆盖）本路未重复探查，不作新的断言。
- 未登录、未付费、未使用任何密钥或凭证；未购买任何订阅。

## 未覆盖清单（本路之后仍为空白的部分）

- 上一单 5 行的全部赔率值（5/5 未重验，见上表）。
- SoccerPunter 全部 tick 行的博彩公司归属（文本层空白；需 live-browser 核查博彩公司名是否以图片/图标渲染，或 Premium 规则如何）。
- SoccerPunter tick 的十进制换算行（须先解决归属，否则换算也无意义）。
- BetExplorer 2025/2024 结果表其余场次的赔率值（文本层全部为空格；上一单仅抽查 3 行示例，本路未扩大抽查范围）。
- opening / closing 端点（本路证据中无任何源定义逐行端点）。

## 证据清单（odds_evidence/）

| 文件 | 内容 | sha256 |
|---|---|---|
| nowgoal_1x2_2661153.txt | NowGoal 1x2 页文本层转储（标题、表头、空表体、汇总行、Notes） | a355b42f522fb8f7ef4df66e56a71a6a69a6e6165bda4b21cc2f71b096b6c3a2 |
| nowgoal_oddscomp_2661153.txt | NowGoal oddscomp 页文本层转储（Quarterfinals、12 家公司、全部 "-" 格；比分行已删除） | 05263fec48b87777404a90e5eada6cb7f047cc6aaee806404ec153227fc26722 |
| betexplorer_single_palmeiras_flamengo.txt | BetExplorer 单场页文本层转储（场次身份、事件时间/地点、1X2 标签；比分与进球者行已删除） | 388b8225351affb311018fe2303464175a896e10e1e14dce03ab954b3fad2895 |
| betexplorer_results_2025.txt | BetExplorer 2025 结果表文本层转储（阶段、队名、日期、空赔率格；比分列已删除） | a93b656e4edf1da60997bfd5e2ca1714162417cb50a40569633d3a89485ef3d6 |
| betexplorer_results_2024.txt | BetExplorer 2024 结果表文本层转储（同上） | afbeec5a4c64b617dec1f6b2808b7082c672a488d37ef2274050876fa45359cd |
| soccerpunter_nacional_river_2024.txt | SoccerPunter 2024 Nacional-River tick 表逐字转储（美式值 + 时间戳；博彩公司栏空白；比分行已删除） | 04d4ee1f70cd68a37edaad383e8fd3db1e9aa617e637205bb405fa0a48350dd6 |
| soccerpunter_colocolo_river_2022_note.txt | SoccerPunter 2022 Colo-Colo-River 页说明（不同场次、无 tick 表；比分行已删除） | b43fc99facf1096e4376da4ae682a5692c8cf23857e46254882be7107f87a8f7 |
| evidence_sha256.txt | 上述 7 个文件的 sha256 清单（由 sha256sum 生成） | — |

（注：证据文件中的 "results" 字样仅出现在 URL 与页面名称中，如 /results/；"Score" 仅作为 SoccerPunter 市场分类名称出现；均不含任何比分值、赛果值或进球者。）

## 需主代理派发（本路子代理无法执行的 live-browser 部分）

1. **live-browser 重验上一单 5 行**：用真浏览器重新打开 NowGoal 1x2 页（2661153，Initial 与 Live 筛选器）与 BetExplorer 单场页/结果表页，核对 Bet 365、Stake.com 与结果表值是否在渲染后出现；同时核对 BetExplorer 决赛行的日期显示（29.11 vs 30.11、30.11 vs 01.12）随浏览器时区如何变化，以解决日期冲突。
2. **live-browser 核查 SoccerPunter 博彩公司栏**：打开 Nacional vs River Plate 2024 movement 页，确认 tick 行的博彩公司名是否以图片/图标形式渲染（文本层读不到），或是否须 Premium 会员才能看到逐行归属；确认后方可决定是否换算美式值为十进制行。
3. **以上两项均不得由本路文本层结论代替**：文本层“看不到”不等于渲染层“没有”，也不等于上一单数值错误；最终是否恢复 5 行，须以 live-browser 证据为准。
