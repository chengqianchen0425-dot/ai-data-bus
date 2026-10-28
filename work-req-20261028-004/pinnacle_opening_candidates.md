# Pinnacle 开盘候选表：eredivisie-2018-19-2019-03-30-heerenveen-excelsior

审计目标：Pinnacle 十进制 1X2 开盘报价，且其有效捕获／更新时间**严格早于 2019-03-30T19:45:32Z**（开球 20:45 Europe/Amsterdam）。
本轮核查时间：2026-10-28（UTC），文本层核查；实时浏览器核查不在本轮能力内，由主代理另行安排。

## 1. 合格候选表（空表）

| # | source | Pinnacle 1X2（十进制） | 有效时间戳 | 时间戳语义 | 证据字节 SHA-256 |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

**结论：本轮文本层核查未找到任何满足“Pinnacle＋十进制 1X2＋开盘语义＋严格开球前有效时间戳＋页面级证据”的候选。**
NowGoal Initial 行（1.70／4.05／4.77）不进入本表，理由见 `nowgoal_audit_1552084.md` §4（分钟精度时间戳横跨开球秒、Last Updated 不是报价有效时间、存档 true_opening 标签已否定）。

## 2. 尝试源清单（全部未产出合格候选，含原因）

### 2.1 NowGoal 存档行（审计对象，非候选）
- source_name：NowGoal（库内存档，2026-10-10 批次）
- source_url＝final_url：https://www.nowgoal831.com/1x2-odds/1552084
- retrieved_at（存档）：2026-10-10T06:44:35Z
- field_locator：1x2-odds/1552084 Initial 视图 Pinnacle 行 HW/D/AW 列与 Last Updated 列
- timestamp semantics：recorded_at＝Initial 视图 Last Updated 列（分钟精度，2019-03-31T03:45:00+08:00＝2019-03-30T19:45:00Z）；是页面／数据流更新时刻，不是报价有效时刻；存档 field_semantics＝true_opening 已否定，正确语义为 initial_first_capture
- 证据字节 SHA-256：`4678415d2c85972478a89247052bc169f70623d014f459ee1558f6fc7c39d055`（存档行实算，见审计文件 §1）
- 结果：**拒绝**——无法确立严格开球前（详见审计文件 §4）。

### 2.2 NowGoal 实时页（文本层复核）
- source_name：NowGoal 实时页
- source_url＝final_url：https://www.nowgoal831.com/1x2-odds/1552084
- retrieved_at：2026-10-28T11:38:00Z（页面抓取戳：2026-10-28 11:38 UTC）
- field_locator：1x2 Odds 表（Bookmakers／HW／D／AW／Last Updated 列）
- timestamp semantics：无——文本层仅返回表骨架，全部赔率单元格为空（JS 渲染表，文本层无值）
- 证据字节 SHA-256：null（文本层抓取不产生原始字节捕获；描述或 URL 的哈希不算证据哈希）
- 结果：**无值**——文本层无法复核 Initial 行；JS 表核查需实时浏览器， deferred。

### 2.3 NowGoal 底层数据接口（文本层尝试，403）
- source_name：NowGoal 1x2 数据接口（批次方法论提及的 //1x2.nowgoal26.com/{matchId}.js）
- source_url：https://1x2.nowgoal26.com/1552084.js
- retrieved_at：2026-10-28T11:39:00Z（UTC，尝试时刻）
- field_locator：不适用（未返回内容）
- timestamp semantics：无
- 证据字节 SHA-256：null（HTTP 403，未取得字节；按指令不重试、不换端点绕过）
- 结果：**未取到**——上游拒绝访问（HTTP 403），本轮不再尝试。

### 2.4 BetExplorer（本场赔率历史页未定位）
- source_name：BetExplorer
- source_url：未定位（公开搜索两轮未返回本场 BetExplorer 赔率页 URL；**不猜测 URL**）
- final_url：不适用
- retrieved_at：2026-10-28T11:37:00Z（UTC，搜索时刻）
- field_locator：不适用
- timestamp semantics：无
- 证据字节 SHA-256：null（未定位到页面，无字节可算）
- 结果：**未定位**——BetExplorer 本场赔率历史表需 JS／站内定位，文本层搜索未找到；核查 deferred 至实时浏览器。未从其它聚合页的无署名赔率快照推断 BetExplorer 内容。

### 2.5 SoccerPunter（本场 H2H 页已读；赔率历史页未取到）
- source_name：SoccerPunter
- source_url＝final_url：https://www.soccerpunter.com/head-to-head-stats/away/12946/1053/1652/SC-Heerenveen-vs-Excelsior-in-Netherlands-Eredivisie-2018-2019
- retrieved_at：2026-10-28T11:37:00Z（UTC；页面自身抓取戳：2026-07-13 23:17 UTC）
- field_locator：H2H 页 “1x2 odds” 快照区（文本层）
- timestamp semantics：无——该快照无博彩公司署名、无时间戳、为美式格式单值快照，不是赔率历史、不是开盘
- 证据字节 SHA-256：null（文本层抓取无原始字节捕获）
- 结果：**拒绝**——无署名、无时间戳的快照不能作为 Pinnacle 开盘证据；数值本身不予引用（避免无署名值被误作候选）。
- 补充：SoccerPunter 本场赔率历史（odds movement）页 URL 在三轮搜索中未定位到本场（返回的 live-odds 页均属其它场次）；且按站内文本，赔率历史与逐日波动为 Platinum 会员专属、Pinnacle 列为 Premium——文本层不可取，核查 deferred 至实时浏览器／会员通道（本轮不登录、不购买）。

### 2.6 Corner-stats（本场页已读；赔率表为空）
- source_name：Corner-stats
- source_url＝final_url：https://corner-stats.com/heerenveen-excelsior-30-03-2019/eredivisie-netherlands/match/241675
- retrieved_at：2026-10-28T11:38:00Z（UTC，搜索返回时刻）
- field_locator：页内 Odds 表（Bookmaker／Date／1／X／2 列）
- timestamp semantics：无——文本层中该表仅有表头，无任何博彩公司行
- 证据字节 SHA-256：null（文本层抓取无原始字节捕获）
- 结果：**空表**——无 Pinnacle 行可取。

### 2.7 TipsterArea／PrimaTips 等聚合快照（已见，拒绝）
- source_name：TipsterArea、PrimaTips（搜索返回的聚合页）
- source_url：搜索返回的对应聚合页（本场 H2H／贴士页）
- retrieved_at：2026-10-28T11:36:00Z（UTC，搜索时刻）
- field_locator：H2H 表／Coefficients 快照区
- timestamp semantics：无——单值快照，无博彩公司署名、无时间戳、无开盘语义
- 证据字节 SHA-256：null（文本层搜索摘要，无原始字节捕获）
- 结果：**拒绝**——无署名快照不能证明 Pinnacle 开盘；数值不予引用；不以别家赔率、市场共识推断 Pinnacle 开盘。

### 2.8 OddsPortal（仅来源盘点，零提取）
- source_name：OddsPortal
- source_url：不适用（本轮未打开、未抓取任何 OddsPortal 页面）
- retrieved_at：不适用
- field_locator：不适用
- timestamp semantics：不适用
- 证据字节 SHA-256：null（零提取）
- 结果：**盘点-only**——OddsPortal 一般具有本场赔率历史页，但其条款 §2.11 禁止未经书面同意的 scraping／aggregation；本轮不做任何自动化批量提取；核查 deferred 至主代理安排的合规通道（实时浏览器／书面同意后的提取）。

### 2.9 Football-Data（任务给定线索，非候选）
- source_name：Football-Data（任务给定线索，本轮未重新抓取）
- source_url：不适用（线索给定，未独立核验）
- retrieved_at：不适用
- field_locator：Pinnacle pre_closing／closing 列（任务给定）
- timestamp semantics：其自身语义说 pre_closing 不是真实开盘；closing 为收盘方向值
- 证据字节 SHA-256：null（未重新抓取，无字节）
- 结果：**拒绝作替代**——pre_closing（1.62／4.43／5.15）与 closing（1.60／4.74／4.96）均不是开盘；仅作审计线索记录于审计文件 §5。

## 3. 硬禁令执行记录（本轮未调用）

| 禁止项 | 执行情况 | 原因 |
|---|---|---|
| FiveDollar | 未调用 | 该场 Pinnacle 已空数组且达 20 次上限；任务硬禁令 |
| API-Football 赔率 | 未调用 | 赔率仅保留 7 天，对 2019 年场次无用 |
| 购买／登录／密钥／付费 API | 全部未用 | 任务禁令；SoccerPunter Platinum／Premium 内容未尝试解锁 |
| 比分／赛果／积分榜／预测／模型输出 | 全部未碰、未写入 | 任务禁令；本文件与审计文件均不含上述内容 |
| repo/responses/ | 未写 | 主代理职责；本交付仅在 work-req-20261028-004/ 内 |

## 4. 剩余缺口（需主代理／请求方后续安排）

1. **实时浏览器核查**：NowGoal 1x2-odds/1552084 的 Initial 视图与 gameDetail 逐笔变动（含秒级／分钟级时间戳的首条 Pinnacle 记录）——文本层只能看到表骨架，JS 表必须走真浏览器；若 gameDetail 首条变动时间戳严格早于 2019-03-30T19:45:32Z 且对应值可确认为开盘首值，方可改判。
2. **BetExplorer／SoccerPunter 本场赔率历史页**：需站内定位＋JS 渲染（SoccerPunter 另涉 Platinum／Premium 门槛，需合规通道）。
3. **OddsPortal**：需合规通道（书面同意或实时浏览器人工查看），本轮零提取。
4. **Pinnacle 官方开盘声明**：本轮无任何官方开盘时间证据；若请求方持有 Pinnacle 官方开盘记录，可直接裁决。
