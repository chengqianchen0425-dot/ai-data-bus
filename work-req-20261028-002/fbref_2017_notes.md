# Veikkausliiga 2017 赛季赛程转录说明（FBref，联赛 only）

- 唯一赛程源：https://fbref.com/en/comps/43/2017/schedule/2017-Veikkausliiga-Scores-and-Fixtures
- 读取方式：浏览器文本层，分两页读完该页全部 491 行（第 1 页 0-265 行，第 2 页 265-491 行）；未只读第一页。
- 读取时间：2026-10-28T16:26:00+08:00
- 交付文件：`fbref_2017_schedule_rows.jsonl`（本说明的姊妹文件）
- 写入原则：只写任务指定的赛程字段；源表其余列一律未写入本输出（无任何赛果类数值、无观众数、无裁判名）。
- Time 列处理：文本层中每行 Time 均只显示单一时刻，无括号内第二时刻，故 kickoff_local 即该时刻原文；绝无把换算值当作源时间。

## 计数核对

- 呈现行数：198
- 去重后唯一场次：198（去重键为 (match_date, home_team, away_team)；重复呈现 0 行，删除 0 行）
- 期望场次核对：12 队 × 33 轮 / 2 = 198 场；实际 198 场，偏差 0，完全吻合。
- 日期范围：2017-04-05 至 2017-10-28
- 参赛队（FBref 原文，共 12 队）：HJK Helsinki、Helsinki IFK、IFK Mariehamn、Ilves、Inter Turku、JJK、Kemi Kings、KuPS、Lahti、RoPS、SJK、VPS
- Wk 取值范围：1-33，每轮恰好 6 场（33 × 6 = 198），无缺轮、无超额轮。
- Venue 空白数：0（198 行均有 Venue 原文）
- Time 列缺失数：0（198 行均有开球时刻）

## 行键与特殊字段

- 行键：`2017|match_date|home_team|away_team`，即 JSONL 中的 fixture_key。
- official_round：FBref 的 Wk 原值，格式为 "Matchweek N (FBref)"。
- meeting_number：一律 null。理由："no authoritative source defines meeting_number; deriving it from date order or team appearance counts is forbidden by the task"。绝未从轮次顺序或交手次数推断。
- csv_join_status：每行均为 `csv_unavailable_on_this_vm_derived_from_public_schedule`（请求方身份 CSV 在本 VM 上不存在，绝不声称与该 CSV 精确对应）。
- source_sha256：一律 null。原因：FBref 直接下载被 Cloudflare 拦截（HTTP 403 challenge），本季行一律走浏览器文本层，未捕获任何源字节，哈希绝不编造。见 JSONL 每行的 source_sha256_note。

## Wk 异常清单（原值保留，一律未“纠正”）

判定口径（事先定好，只列符合任一情形的行，不逐行主观改轮次）：
(a) 该行是其 Wk 中唯一一行的日期比同轮其余各行早 ≥3 天；
(b) 该行在表中的呈现顺序打破了轮次单调性（后一轮的行出现在前一轮的行之前）；
(c) 该行是其 Wk 的尾行，且日期与下一轮的首行日期相同（跨轮同日收尾）。

共 12 行：

1. 2017-04-30，Wk 5，IFK Mariehamn vs VPS——同轮其余 5 行均为 2017-05-06，早 6 天（情形 a）。
2. 2017-05-06，Wk 6，JJK vs Inter Turku——同轮其余行在 2017-05-11/12，早 5 天（情形 a）。
3. 2017-05-06，Wk 5，Helsinki IFK vs RoPS——表中呈现顺序位于 Wk 6 首行之后（情形 b，同日）。
4. 2017-05-12，Wk 7，SJK vs JJK——同轮其余行均为 2017-05-19，早 7 天（情形 a）。
5. 2017-05-19，Wk 8，SJK vs RoPS——同轮其余行在 2017-05-23/24，早 4 天（情形 a）。
6. 2017-05-24，Wk 9，KuPS vs SJK——同轮其余行均为 2017-05-27，早 3 天（情形 a）。
7. 2017-05-27，Wk 10，SJK vs IFK Mariehamn——同轮其余行均为 2017-05-31，早 4 天（情形 a）。
8. 2017-05-31，Wk 11，Inter Turku vs Lahti——同轮其余行在 2017-06-03/04，早 3 天（情形 a）。
9. 2017-06-04，Wk 12，KuPS vs IFK Mariehamn——同轮其余行在 2017-06-14/15/16，早 10 天，为全季最大间隔（情形 a）。
10. 2017-06-21，Wk 13，Inter Turku vs KuPS——Wk 13 尾行落在 Wk 14 首行同日（2017-06-21）（情形 c）。
11. 2017-06-26，Wk 14，RoPS vs Ilves——Wk 14 尾行落在 Wk 15 首行同日（2017-06-26）（情形 c）。
12. 2017-07-08，Wk 17，Inter Turku vs JJK——同轮其余行在 2017-07-16/17，早 8 天（情形 a）。

总体判断：FBref 的 Wk 不是严格按日期切分的轮次——边界日期（2017-05-06、05-12、05-19、05-24、05-27、05-31、06-04、06-21、06-26、07-08）上均有两轮同日开赛，属系统性呈现方式而非个别笔误；上述 12 行的 Wk 原值已全部保留，未作任何改写。

## 原值保留的其他现象（未合并、未修正）

- 按 FBref 原文，Wk 1 中 Lahti 出现两次（2017-04-05 对 SJK、2017-04-08 对 Ilves），Wk 12 中 KuPS 出现两次（2017-06-04 对 IFK Mariehamn、2017-06-14 对 VPS）。照抄原文，不合并、不判错。
- Venue 原文含特殊写法均照抄，例如 "Telia 5G -areena"（原文即含空格与连字符）、"Wiklöf Holding Arena konstgräs"（仅 2017-07-22 一行带 konstgräs 后缀）。

## 未做事项

- 未写 repo/responses/；未写任何赛果类内容；未声称与请求方 CSV 精确对应；未推断 meeting_number。
