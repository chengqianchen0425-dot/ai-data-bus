# NowGoal 存档审计：match 1552084（Heerenveen vs Excelsior，2019-03-30）

审计对象（固定身份，任务给定，不扩展到其它场次）：
- fixture_key：`eredivisie-2018-19-2019-03-30-heerenveen-excelsior`
- provider_fixture_id：619161520；league_id：137325260；赛季 2018/19
- 开球：2019-03-30 20:45 Europe/Amsterdam ＝ **2019-03-30T19:45:32Z**（任务给定值；当日阿姆斯特丹为 CET＝UTC+1，20:45 CET＝19:45 UTC，秒数取任务给定值，不另行推导）
- 审计目标：Pinnacle 十进制 1X2 开盘报价，且其有效捕获／更新时间**严格早于 2019-03-30T19:45:32Z**

## 1. 存档记录逐字摘录（未改写、未升格）

来源文件：`~/workspace/ai-inbox/repo/work-req-20261010-003/nowgoal_1819_pinnacle_opening.jsonl`，第 57 行。
该行字节 SHA-256（审计人实算，非存档自带字段）：`4678415d2c85972478a89247052bc169f70623d014f459ee1558f6fc7c39d055`

```json
{"fixture_key":"eredivisie-2018-19-2019-03-30-heerenveen-excelsior","bookmaker":"pinnacle","home":1.7,"draw":4.05,"away":4.77,"recorded_at":"2019-03-31T03:45:00+08:00","field_semantics":"true_opening","source_url":"https://www.nowgoal831.com/1x2-odds/1552084","final_url":"https://www.nowgoal831.com/1x2-odds/1552084","retrieved_at":"2026-10-10T06:44:35Z","field_locator":"1x2-odds/1552084 Initial视图 Pinnacle行 HW/D/AW列与Last Updated列"}
```

逐字段读出（仅转述，不改值）：
- bookmaker：pinnacle
- home／draw／away（十进制）：1.70／4.05／4.77
- recorded_at：2019-03-31T03:45:00+08:00
- field_semantics（存档原标）：true_opening —— **见 §3，该标签是已确立的误标，本审计不继承**
- source_url＝final_url：https://www.nowgoal831.com/1x2-odds/1552084
- retrieved_at：2026-10-10T06:44:35Z
- field_locator：1x2-odds/1552084 Initial 视图 Pinnacle 行 HW/D/AW 列与 Last Updated 列

同批次审计说明（`nowgoal_1819_audit.md` 原文要点，转述）：
- recorded_at 系 Initial 视图 “Last Updated” 列转 ISO+08:00；
- 批次方法论自述：NowGoal 的 “initial” 初指 Last Updated 时间部分非常接近甚至晚于开球时间；其 “initial” 实为数据流对初指的首次捕获／刷新记录，**不等同于 Pinnacle 真实市场开盘时刻**；gameDetail 显示部分比赛 Pinnacle 最早变动记录早于 Initial 视图的 Last Updated；
- 但本场存档中**只有 Initial 行，没有 gameDetail 最早变动记录**，因此本场不存在比 Last Updated 更早的存档内时间戳。

## 2. 三段时间语义分析（必须区分的三者）

### (a) 归档时间（retrieval time）
- 值：2026-10-10T06:44:35Z（存档行 retrieved_at）。
- 语义：2026 年批次抓取时页面被读取的时刻。
- 与开盘无关：它只证明 2026 年时页面上曾有这样一行，不证明 2019 年任何时刻的报价状态。

### (b) 页面更新时间（page update time，即 Last Updated）
- 值：2019-03-31T03:45:00+08:00 ＝ **2019-03-30T19:45:00Z**（+08:00 换算，分钟精度，无秒位）。
- 语义：NowGoal 数据流对该 Initial 行的最后一次更新／刷新显示时刻（按批次方法论：首次捕获／刷新记录）。
- 关键缺陷有二：
  1. **分钟精度**：Last Updated 列只给到分钟。真实更新瞬间落在 [19:45:00Z，19:45:59Z] 区间内（若为截断显示）或该分钟前后（若为四舍五入显示），两种读法下该区间都**横跨开球秒 19:45:32Z**。因此仅凭此值无法判定更新瞬间在开球秒之前还是之后。
  2. **不是报价有效时间**：页面更新时刻 ≠ 该组赔率在 Pinnacle 市场上生效的时刻。Initial 行给出的是“首次捕获到的值”，页面本身没有声明 Pinnacle 是何时首次挂出 1.70／4.05／4.77 的。

### (c) 报价有效时间（quote validity time，即真正要证明的量）
- 值：**存档中不存在**。没有任何字段声明 1.70／4.05／4.77 于何时起在 Pinnacle 有效、有效至何时。
- 没有页面级证据（逐笔变动时间戳、带秒级时间戳的首条记录、Pinnacle 官方开盘声明）之前，报价有效时间无法从 (a) 或 (b) 推导出来。

### 数值对照（只作算术核对，不作推断）
- recorded_at（换算后）19:45:00Z 与开球 19:45:32Z 的名义差额：**32 秒**。
- 但因 (b) 为分钟精度，该 32 秒差额落在显示精度误差范围内，**不得以 32 秒差额推定“严格早于开球”**。若真实更新瞬间为 19:45:33Z–19:45:59Z，则反而晚于开球秒；若为 19:45:00Z–19:45:31Z，则早于开球秒——两种情形在现有证据下无法区分。

## 3. 存档标签纠正（不继承 true_opening）

- 存档行 field_semantics＝true_opening 是 2026-10-10 批次的旧标签。
- 已确立教训（2026-10-22）：NowGoal Initial ≠ 真实开盘；Initial 只是数据流首次捕获，应标 `initial_first_capture`，不得标 true_opening。
- 因此本审计对该行的正确语义标注为：**initial_first_capture（NowGoal Initial 视图首次捕获值），不是 Pinnacle 真实市场开盘**。存档原文照抄于 §1，语义以本节为准。

## 4. Initial 行裁决

**裁决：无法确立为严格开球前（UNVERIFIABLE AS STRICTLY PRE-KICKOFF）。**

理由（四项，任一即足以否决“严格开球前”认定）：
1. **时间戳精度不足**：唯一候选时间戳 recorded_at／Last Updated 为分钟精度（19:45:00Z），其真实瞬间区间横跨开球秒 19:45:32Z，无法确立严格早于。
2. **时间戳语义不对**：Last Updated 是页面／数据流更新时刻，不是报价有效时刻；Initial 标签本身不证明报价有效时间。
3. **无更早证据**：存档中无本场 gameDetail 最早变动记录；本轮文本层亦未找到带秒级／分钟级早于开球时间戳的 Pinnacle 首条记录（见 pinnacle_opening_candidates.md）。
4. **标签误标**：存档 true_opening 标签已被后续教训否定，不能作为开盘语义的证据。

**不属于本裁决的情形（明确排除）**：
- 不是“恰为开球”：没有任何证据表明该组报价的有效瞬间恰等于开球秒。
- 不是“早于开球”：32 秒名义差额在分钟精度误差内，不能推定。
- 不是“晚于开球”：同样无法证明晚于；裁决是“无法确立”，不是反向认定。

## 5. 交叉线索（审计线索，绝不作替代）

Football-Data（任务给定线索，本轮未重新抓取、不作独立核验）：
- Pinnacle pre_closing：1.62／4.43／5.15；closing：1.60／4.74／4.96。
- 其自身语义说 pre_closing 不是真实开盘，故只作审计线索，绝不作开盘替代。
- 仅作一致性注记，不作推断：NowGoal Initial 值（1.70／4.05／4.77）与上述两组值均不同；数值差异本身不能证明任何一组的开盘地位，不以别家赔率、市场共识、邻场推断 Pinnacle 开盘。

## 6. 本轮未做事项（诚实边界）

- 未调用 FiveDollar（该场 Pinnacle 已空数组且达 20 次上限，硬禁令）。
- 未调用 API-Football 赔率（仅保留 7 天，对 2019 年场次无用）。
- 未做实时浏览器核查（本审计 agent 无真浏览器能力；NowGoal／BetExplorer／SoccerPunter 的 JS 赔率表核查由主代理另行安排，本文件不谎称已做）。
- 未碰比分、赛果、积分榜、预测、模型输出；未购买、未登录、未使用任何密钥／凭证、未动用付费 API 额度；未写 repo/responses/。
- 未对 OddsPortal 做任何提取（仅来源盘点，见候选表；其条款 §2.11 禁止未经书面同意的 scraping／aggregation）。
