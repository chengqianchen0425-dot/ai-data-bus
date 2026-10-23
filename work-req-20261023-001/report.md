# req-20261023-001 报告：Copa Libertadores 2018–2025 canonical fixture 清单 + 可审计历史 pre-match FT 1X2 赔率

## 结论先行（全部按本单 Q4 口径）

- **Fixture 清单：1,124 行，按源分开保存，绝不跨源拼合。** CONMEBOL 官方 PROGRAMA 38 行（全部有字节 SHA-256，100%）；FBref 文本层 1,086 行（2018–2024，字节哈希 0%，因 Cloudflare 拦截，结构性缺口）；2025 季本轮阻塞，0 行（上一单的 155 行未复制）。
- **赔率行：53 行，全部 phase=unspecified；符合开盘/收盘定义的赔率行仍然是 0 行。** 其中上一单 5 行经第二轮实时浏览器渲染全部确认（不是文本层确认——文本层因 JS 渲染表为空，5/5 无法确认也无法证伪；文本层未确认不等于上一单错了）；新增 SoccerPunter 48 行（1 场 Nacional vs River Plate 2024：主表 10 家 + 188Bet H 历史 38 条 tick），全部为美式原值呈现，十进制列是按公式换算、非源显示值。
- **不花钱、不凭证的前提下，带时间戳 tick 的 opening/closing 历史仍然拿不到。** 本轮新增一项终结性修正：API-Football 官方文档证实赔率只保留最近 7 天（by design），付费也无解，该 pending 项关闭，不再派单。

## 1. Fixture 清单（fixture_inventory.jsonl，1,124 行）

按赛季（源分开计数，含跨源重复，不是去重场次）：2018=156、2019=155、2020=155、2021=155、2022=185（FBref 155 + CONMEBOL 30）、2023=155、2024=163（FBref 155 + CONMEBOL 8）、2025=0。
状态：complete 1,062、partial 60（FBref 球场截断 57 + CONMEBOL "A definir" 3）、conflict 2、unmatched 0、ambiguous 0。
时区：1,124 行全部无源发布时区名/偏移（source_timezone_text 全 null）；CONMEBOL 的 GMT 列时刻字符串绝不与 match_date 拼成时间戳。
字节哈希：全部 38/1,124=3.38%；CONMEBOL 子集 38/38=100%（3 份 PDF，2026-10-23 下载，HTTP 200，两轮哈希一致）；FBref 子集 0/1,086=0%（curl 探针：HTTP 403 Cloudflare 挑战或 000 空回复；挑战页哈希绝未用作行哈希）。
禁字段扫描：score/goals/result/winner 类键 0 命中。

### 本轮对上一单的 3 处纠正（不得沿用旧读数）

1. **CONMEBOL 覆盖分母**：上一单审计写 4/56 是算术错误。正确网格是 8 季 × 8 阶段 = 64，覆盖 4/64，未覆盖 60/64。
2. **CONMEBOL "A definir" 3 行**（2022 Fase 1/2 PDF，按 Ciudad=28、País=39、Estadio=68、Hora Local=98 列位）：city="A definir"、country=null、venue="A definir"；#11/#14 的 kickoff_local=null（源文本 "A definir" 另存于 kickoff_local_source_text）。上一单读作 city/country="A definir"、venue=null 是错的。
3. **上一单 request_sha**：按请求文件字节重算，前 16 位与上一单回执一致，所谓 malformed/mismatched 不是前缀错误；本单回执同时附完整 64 位摘要，供任一口径核对。

## 2. 赔率行（fixture_odds_rows.jsonl，53 行，opening/closing 均为 0）

| 来源 | 赛季 | 博彩公司 | 相位 | 行数 | 验证 |
|---|---|---|---|---|---|
| NowGoal 1x2（2661153） | 2024 | Bet 365 | unspecified（Initial） | 1 | 第二轮渲染确认 3.00/3.10/2.50；Last Updated 栏 18-09 08:15；页面不定义 Initial 为开盘 |
| NowGoal 1x2（2661153） | 2024 | Bet 365 | unspecified（Live） | 1 | 第二轮渲染确认 3.30/3.00/2.40；Last Updated 栏同样 18-09 08:15；页面不定义 Live 为赛前收盘 |
| BetExplorer 单场页 | 2025 | Stake.com | unspecified | 1 | 第二轮渲染确认 3.55/3.00/2.42（仅一家渲染）；无 Opening/Closing 标注 |
| BetExplorer 结果表 | 2025 | 未标明 | unspecified | 1 | 第二轮渲染确认 1.22/7.40/14.00；博彩公司仍未标明 |
| BetExplorer 结果表 | 2024 | 未标明 | unspecified | 1 | 第二轮渲染确认 4.33/3.19/1.90；博彩公司仍未标明 |
| SoccerPunter 主表 | 2024 | 10 家（见下） | unspecified（渲染时各家最新显示 tick） | 10 | 图标识别（文本层该列为空）；美式原值；1 家后缀不明 |
| SoccerPunter 188Bet H 历史 | 2024 | 188Bet（仅弹窗标题归属） | unspecified（带时间戳 tick，无端点定义） | 38 | 另有 2 条显示为 -/-/- 的空缺 tick 只记审计、不成行 |

SoccerPunter 主表 10 家：bet365、bet365 品牌图标（后缀不明，绝不命名为 Bet365 SM）、10Bet、188BET、Ladbrokes、PINNACLE、William HILL、Singapore Pools、bwin、betfair。
美式→十进制换算公式（仅用于 odds_*_decimal_computed 列，源未显示十进制值）：正值 1 + odds/100，负值 1 + 100/|odds|，保留 4 位小数。例如 240 → 3.4000、275 → 3.7500、104 → 2.0400、-109 → 1.9174。
SoccerPunter 为什么不能产出 opening/closing：页面描述 H 历史"包含初始赔率和每日波动"是通用描述，不是逐行端点定义；没有任何一行被标注 opening/closing；页面不定义收盘价；Nacional vs River Plate 的开球时刻未在页上确认，H tick 的赛前/滚球切分无证据。
SoccerPunter 日期口径：全部时间戳按页显示原样保留（08/05/2024 等），不转 ISO、不换算时区；DD/MM 与 MM/DD 两种读法都未证实，match_date 置 null（见 conflicts.json C-06）。

## 3. 访问计划与 blocker（access_plan.md / access_audit.md，11 源核查）

四档：免费公开可达 6（OddsPortal 浏览、BetExplorer 浏览、NowGoal、Football-Data.co.uk、OpenFootball、SoccerPunter）、需登录 1（Kaggle/GitHub 数据集家族）、需付费 3（5Dollar、The Odds API、OddAlerts）、需密钥 1（API-Football）。
最大 blocker：
1. **能定义 opening/closing 的批量源全部在付费/密钥墙内**，本单禁购买禁凭证，批量路径整体封死。
2. **API-Football 付费也无解**：官方文档原文——赔率只保留最近 7 天，by design。2018–2025 赔率在该源不存在。
3. **条款墙 + 语义墙 + 源级无覆盖**：OddsPortal 条款 §2.11 明文禁止未经书面同意的 scraping/aggregation 与自动化请求（人工浏览可达，批量提取不合规）；NowGoal Initial/Live 无 opening/closing 定义；Football-Data.co.uk 源级无解放者杯覆盖（data.php 全文 143 行复核确认），付费也无解。
不花钱能拿到的最大范围：CONMEBOL 官方 38 行 + FBref/SA 候选行（须保留候选标注）+ OpenFootball 公开 CC0 仓库 copa-libertadores 目录（本轮确认存在，无赔率字段；分季文件覆盖年份未核实，见 UQ-11）+ 上述 53 行 unspecified 赔率观测。
根本拿不到：任何带时间戳 tick 的 opening/closing 历史；Football-Data 的解放者杯；API-Football 的 2018–2025 赔率；The Odds API 的解放者杯（sport key 未验证、历史在 Business $99/月档）；OddAlerts 的解放者杯（覆盖未验证、API 在付费墙内）；任何已验证的 Kaggle/GitHub 解放者杯 1X2 批量集（本轮未找到）。

## 4. 冲突与未解决（分开两个文件，不混）

- **conflicts.json（7 项，两边都保留、不裁决）**：2020 开球时间冲突 2 项（Universitario 17:15 vs 19:15；Bolívar 20:30 vs 21:30，后者本轮页内双出处一致但仍不改判）；日期冲突 3 项（Palmeiras-Flamengo 在 BetExplorer 同页内顶栏 30.11.2025 vs H2H 栏 29.11.2025；Atletico-MG-Botafogo 渲染 01.12.2024 vs 文本层 30.11.2024；NowGoal 任务参考 2024-09-17 vs 页显 18-09-2024）；SoccerPunter 日期格式歧义 1 项；SoccerPunter 主表第 2 行博彩公司后缀不明 1 项。
- **unresolved_queue.json（18 项，四类分开）**：access_blocked 4（FBref 2025 页、FBref 字节、5Dollar Ultra 购买门、SoccerPunter 全量博彩公司登录门）、source_missing 2（CONMEBOL 60/64、API-Football 关闭项）、pending_work 7（FBref 2025 实时浏览器重读、2020 冲突重开页、SoccerPunter 其他场次、BetExplorer 2021/2020/2019 全量结果页、NowGoal 其余 146 家、OpenFootball 分季覆盖、SoccerPunter H 全量门控）、permanent_rule 3（禁字段、禁推断开盘收盘、禁推断博彩公司）、ambiguous 2（NowGoal 静态文件 retry_after=2026-10-29 未到、SoccerPunter 日期格式）。
- 5Dollar 最近 12 个月场次计数：上一单 126/128 与本轮 127/129 两时点并列（页自述 8 小时前重算），不调和。

## 5. 交付文件清单（本工作目录，随回执 commit）

fixture_inventory.jsonl（1,124 行）、fixture_odds_rows.jsonl（53 行）、audit.json、conflicts.json、unresolved_queue.json、report.md（本文件）、fixture_audit.md、odds_audit.md、access_plan.md、access_audit.md、live_reverification_log.md、soccerpunter_live_log.md、fixture_evidence/（3 份 CONMEBOL PDF 字节 + curl 探针日志 + FBref 文本层说明）、odds_evidence/（7 份文本层转储 + sha256 清单）、conmebol_inventory.jsonl、fbref_{YYYY}_textlayer.jsonl、build_conmebol.py。
合规：未购买、未登录、未使用任何凭证/密钥、未动用 API-Football 额度、未下载 Football-Data CSV、未对 OddsPortal 做自动化提取。实时浏览器渲染无稳定源字节，相关行 source_sha256 与 http_status 均为 null，不编造。
