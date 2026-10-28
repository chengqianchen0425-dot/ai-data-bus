# Veikkausliiga 2018 赛季赛程转录说明（FBref，req-20261028-002）

## 来源与方法
- 唯一赛程源：FBref 联赛赛程页 `https://fbref.com/en/comps/43/2018/schedule/2018-Veikkausliiga-Scores-and-Fixtures`
- 读取方式：浏览器文本层，分两段读完第 0–495 行（含表后说明段）；未使用直接下载。
- `source_sha256`：null。原因：FBref 直接下载被 Cloudflare 拦截（HTTP 403 challenge），本机未捕获任何字节，哈希绝不编造；见每行 `source_sha256_note`。
- `retrieved_at`：2026-10-28T16:25:49+08:00（实际读取页面时间）。
- 仅收联赛场次：该页本身即为 2018 Veikkausliiga 联赛页，未混入其他赛事。
- 字段口径：Wk / Day / Date / Time / Home / Away / Venue 照抄 FBref 原文；`kickoff_local` 取 Time 列的第一个（也是唯一）时刻。本次文本层所见 Time 值均为单一时刻，未出现括号内第二个时刻，因此无换算值需要剔除。
- 删除列：本输出及本说明均不含 Score、Attendance、Referee、Match Report、Notes 栏内容。
- `meeting_number`：全部 null，理由见每行 `meeting_number_reason`（无权威源定义该编号，禁止从日期顺序或交手次数推导）。
- `csv_join_status`：全部为 `csv_unavailable_on_this_vm_derived_from_public_schedule`——请求方身份 CSV 在本 VM 上不存在，本文件不声称与该 CSV 精确对应。

## 数量核对
- 呈现行数：198 行
- 去重后唯一场次：198 场
- 去重键：(match_date, home_team, away_team)；同一日期同一对球队的重复呈现：0 条
- 期望核对：12 队 × 33 轮 / 2 = 198 场；实际 198 场，偏差 0
- 日期范围：2018-04-07 至 2018-10-27
- 参赛队（FBref 原文，共 12 队）：FC Honka、HJK Helsinki、IFK Mariehamn、Ilves、Inter Turku、Kemi Kings、KuPS、Lahti、RoPS、SJK、TPS、VPS
- 行键格式：`2018|match_date|home_team|away_team`，即 `fixture_key`

## Wk 取值范围与分布
- Wk 取值范围：1–33，连续无缺号
- 每轮场次：每轮均为 6 场（33 × 6 = 198），与期望总数一致
- `official_round` 格式：`Matchweek N (FBref)`，N 为 FBref 的 Wk 原值

## Wk 异常行清单（原值保留，未“纠正”）
判定口径：某行日期远离同 Wk 其余场次的主日期簇，且在页面呈现顺序上出现在更晚轮次之后（属延期补赛式呈现）。符合此口径的共 4 行：

1. Wk 8，2018-05-29，HJK Helsinki vs SJK（主场：HJK Helsinki）
   - 同轮其余场次日期：2018-05-07、2018-05-13；本行在页面上出现在 Wk 11（2018-05-26）之后、Wk 12 之前。
2. Wk 3，2018-08-29，Ilves vs IFK Mariehamn（主场：Ilves）
   - 同轮其余场次日期：2018-04-18、2018-04-21；本行在页面上出现在 Wk 25 之后、Wk 26 之前，滞后约 4 个月。
3. Wk 8，2018-09-26，Inter Turku vs Lahti（主场：Inter Turku）
   - 同轮其余场次日期：2018-05-07、2018-05-13、2018-05-29（第 1 条）；本行在页面上出现在 Wk 29 之后、Wk 30 之前。
4. Wk 23，2018-09-26，Ilves vs HJK Helsinki（主场：Ilves）
   - 同轮其余场次日期：2018-08-11、2018-08-12；本行与第 3 条同日，在页面上出现在第 3 条之后、Wk 30 之前。

说明：除上述 4 行外，各轮内部数日跨度（如一周内分两天进行）不计为异常；4 行的 Wk 原值已全部保留，`official_round` 未改写。

## 缺失统计
- Venue 空白数：0（198 行均有 Venue 原文）
- Time 列缺失数：0（198 行均有开球时刻）
- Wk / Day / Date / Home / Away 缺失数：0

## 交付文件
- `fbref_2018_schedule_rows.jsonl`：198 行，每行一个场次
- `fbref_2018_notes.md`：本文件
