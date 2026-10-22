# req-20261022-001 A 路审计：NowGoal 静态赔率路线探查（Copa Libertadores 2018–2025，FT 1X2）

## 结论先行（本路交付 0 行赔率观测，不是 0 场比赛的断言）

- **nowgoal_odds_rows.jsonl 为空文件（0 行），系有意为空，不是遗漏。** 本路在可用通道内未能取得任何解放者杯 NowGoal 赛程 JSON 或 1x2 JS，未编造任何 matchId、赔率值、bookmaker 行或 sclass 编号。
- **最大障碍（按致命程度排）：**
  1. **本机直连与浏览器文本层双双取不到 NowGoal 静态文件**（见 §2 探针，含一次 browser.open 失败后按停表指令未再重复尝试）；
  2. **解放者杯的 NowGoal sclass 编号未知**，本地工作区与搜索引擎索引中均未找到，任务禁猜 URL，故无法构造赛程 JSON 地址；
  3. 镜像域名可能已轮换（上一单用 nowgoal1.top / nowgoal50.com / nowgoal831.com），未验证，无法确认。
- **语义结论（沿用上一单、并纠正上一单的一个标签错误）：** NowGoal 的 “Initial” 只是其数据流首次捕获，不等于博彩公司真实市场开盘时刻，**不得标为 true opening**（上一单 Eredivisie 批次曾用 field_semantics=true_opening，本路不继承该标签；正确标签应为 initial_first_capture）。Current/最新价只有在源明确定义为赛前收盘时才能标 closing，否则只能标 unspecified_current；单个中间价既不是开盘也不是收盘。本路因 0 行数据，以上语义未在解放者杯样本上得到新的实测验证。

## 1. 上一单走通的路线（作对照模板，不等于解放者杯已验证）

来源：~/workspace/ai-inbox/work-req-20261010-003/fetch_nowgoal_odds.py 及 nowgoal_1920_2021_audit.md（2026-10-15，荷甲 2019/20 + 2020/21，384/384 行）。

- 赛季赛程 JSON：`https://football.nowgoal1.top/jsData/matchResult/json/{2019-2020,2020-2021}/s16_en.json`
  - s16 = 荷甲（Eredivisie）的 sclass 编号；条目结构 `[matchId, sclassId, -1, 'YYYY-MM-DD HH:MM'(+08:00), homeId, awayId, …]`；赛程时间为北京时间，匹配当地日期需换算时区。
- 赔率 JS：`https://1x2.nowgoal50.com/{matchId}.js`（需 Referer + UA，否则 000；gzip 压缩需解压；`game=Array(...)` 每条含 Initial 三列与 lastUpdated（UTC）列）。
- 荷甲批次的 bookmaker 行（Pinnacle / Bet 365 / William Hill）**不能迁移为解放者杯的证据**：不同联赛、不同比赛的 bookmaker 覆盖必须逐场实测，本路未取得任何解放者杯 bookmaker 行，故 bookmaker 清单为“未观测到”，不是上述三家。

## 2. 本路探针（全部在本会话内执行，未重复被停表的请求）

| # | 探针 | 时间（UTC+8） | 结果 | HTTP 状态 |
|---|---|---|---|---|
| P1 | shell curl `https://example.com`（对照：判断本机直连是否通） | 2026-10-22 约 16:28 | 超时 15 秒，0 字节 | 000（未获得源状态） |
| P2 | shell curl `https://football.nowgoal1.top/jsData/matchResult/json/2019-2020/s16_en.json`（上一单已验证的荷甲地址，作通道对照） | 2026-10-22 约 16:28 | 超时 20 秒，0 字节 | 000（未获得源状态） |
| P3 | browser.open 同一荷甲 s16_en.json 地址（单次尝试） | 2026-10-22 约 16:29 | 抓取层失败：`browser_open source fetch failed without a source HTTP status`，service_status=200 仅为工具自身状态，**不是源站 HTTP 200**，不得误读 | 无源 HTTP 状态 |

- P1 与 P2 共同说明：本机 shell 直连通道目前对所有外站均不通（与上一单 A 路记录的 cdn.conmebol.com 直连超时一致），不是 NowGoal 单站问题。
- P3 失败后，**按停表指令未再以任何改动参数、其他工具或另一端点重复抓取该地址**（未用 agent-reach / scrapling / 其他镜像去绕过），故本路对 NowGoal 静态文件的可达性结论止于“本环境可用通道内不可达”，不等同于“NowGoal 站点已下线”或“该文件不存在”。
- 搜索引擎侧（browser.search，属索引检索、未直接抓取 NowGoal 文件）仅证实 NowGoal 覆盖解放者杯的编辑内容：`m.nowgoal.com/predictions/812805`（LDU Quito vs São Paulo，9 月 18 日，解放者杯预测页）。该页**未揭示** sclass 编号、赛程 JSON 地址或 1x2 JS 端点，且预测页 ID 不等于 1x2 端点的 matchId，不得混用。

## 3. sclass 编号：未知（本路最关键的未解项）

- 本地检索：grep 整个 ~/workspace/ai-inbox/，除荷甲 s16 外无任何解放者杯 sclass 记录；上一单（req-20261021-001）的源映射中也无 NowGoal 条目。
- 搜索引擎检索（“nowgoal Copa Libertadores league”、“nowgoal Libertadores sclass”、site:nowgoal.com 相关查询）未返回任何含 sclass 编号或 `jsData/matchResult/json/…/s*_en.json` 解放者杯地址的索引结果。
- 因此：**无法在不猜测的前提下构造解放者杯赛程 JSON 地址。** 解放者杯是单年赛季（2018、2019、…、2025），其 JSON 路径的年份写法（是否仍为 `YYYY-YYYY` 双年式）同样未知，一并不得猜测。

## 4. 锚点对照（只对照、不认领）

上一单 38 行 CONMEBOL 官方 PROGRAMA 行（~/workspace/ai-inbox/repo/work-req-20261021-001/fixture_rows_conmebol.jsonl）仅作锚点清单：

| 赛季 | 阶段 | 锚点行数 | 已取得 NowGoal matchId | 已取得赔率行 |
|---|---|---|---|---|
| 2022 | Fase 1 | 6 | 0 | 0 |
| 2022 | Fase 2 | 16 | 0 | 0 |
| 2022 | Fase 3 | 8 | 0 | 0 |
| 2024 | Cuartos de Final | 8 | 0 | 0 |
| 合计 | — | 38 | 0 | 0 |

- 锚点行的字段（日期、队名、球场、Grupo/Llave）**未被用作任何赔率行的证据**，仅用于说明：即使锚点场次明确，没有 matchId 仍无法拉取 1x2 JS。
- 其余 8 季 × 各阶段的场次不在锚点清单内，本路不以 FBref/SoccerAssociation 的 1,241/1,227 行去“认领”赔率场次（任务禁跨源按队名拼合）。

## 5. 按赛季 × 阶段 × bookmaker × phase 行数

全部为 0，原因统一为 blocked（通道不可达）+ source_missing（sclass 未知）。expected 一律 null（无权威源公布应有场次数；上一单的 1,241 场是 FBref 发现数，不是 expected 分母）。

| 赛季 | 阶段 | bookmaker | phase | 发现行数 | 状态 | 原因 |
|---|---|---|---|---|---|---|
| 2018–2025（每季同此） | 全部阶段（资格赛、小组赛、十六强、四分之一决赛、半决赛、决赛） | 未观测到（无 bookmaker 行） | opening / closing / unspecified_current | 0 | blocked + source_missing | P1–P3 通道不可达；sclass 未知，赛程 JSON 地址无法构造 |
| 合计 | — | — | — | **0** | — | — |

- 未覆盖清单 = 全部：2018、2019、2020、2021、2022、2023、2024、2025 共 8 季的全部阶段、全部 bookmaker、全部 phase。
- 歧义队列：本路无任何赔率观测，故无 ambiguous-match 行；38 个锚点场次记为“无赔率证据”，不记为 ambiguous（ambiguous 仅适用于已取得但无法唯一匹配的观测，本路尚无此类观测）。

## 6. 未观测到的字段（全部为 null 的原因）

- source_fixture_id（NowGoal matchId）：无赛程 JSON，故无。
- match date / kickoff / timezone / 官方阶段 / 轮次：无赔率行可附着，故无；锚点行的日期/阶段不转移为赔率行的证据。
- decimal H/D/A、quote timestamp、快照语义：无观测。
- source_url / final_url / field_locator：无成功抓取，故无；探针地址仅记录于 §2，不伪装成数据来源。
- source_sha256：无字节可算，故 null；原因见 §2（直连超时、浏览器文本层抓取失败）。

## 7. 给主代理的下一步（精确动作，不含猜测）

1. **真浏览器任务（主代理派发，本路子代理无真浏览器能力）：** 打开 NowGoal 解放者杯联赛页，记录页面/JS 中出现的 sclass 编号；或打开一场已知解放者杯比赛的 NowGoal 1x2 页，记录其 matchId 与 `game=Array` 结构是否与荷甲一致。拿到 sclass 后方可构造赛程 JSON 地址。
2. **可直连环境重跑：** 在能直连 nowgoal1.top / nowgoal50.com 的环境中，用上一单脚本逻辑（Referer + UA、gzip 解压、0.8 秒间隔）先以单季、单场做探针，确认赛季 JSON 年份写法与 sclass 后再批量；本机 VM 不宜再重复撞墙。
3. **语义复核前置：** 批量前先确认 1x2 JS 中 Initial/Current 列的源内定义；Initial 行一律记 phase=initial_first_capture（不得记 true opening），Current 行只有在源明确定义为赛前收盘时才记 closing，否则记 unspecified_current。
4. **不要做的事：** 不要按队名把 FBref/SoccerAssociation 行指派给 NowGoal 观测；不要用荷甲的 bookmaker 清单冒充解放者杯覆盖；不要猜测 sclass 或赛季路径。

## 8. 合规声明

- 本路只做赔率证据探查，未做预测，未返回比分、进球、赛果、晋级、概率、模型方向等任何赛后字段；nowgoal_odds_rows.jsonl 中无此类字段（文件为空）。
- 未付费、未碰任何付费额度、未猜 URL、未编赔率值。
- 未写 repo/responses/，那是主代理的事。
