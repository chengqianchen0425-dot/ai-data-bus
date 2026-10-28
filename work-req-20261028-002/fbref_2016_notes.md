# Veikkausliiga 2016 赛季赛程转录说明（FBref，联赛 only）

## 来源与方法

- 唯一赛程源：FBref 联赛赛程页
  `https://fbref.com/en/comps/43/2016/schedule/2016-Veikkausliiga-Scores-and-Fixtures`
- 读取方式：浏览器文本层，528 行全部读完（L0–L528，含重复表头空行），未只读第一页。
  文本抓取层标注该页抓取于 2026-10-22 15:06 UTC；本转录实际读取时间为
  `2026-10-28T16:26:16+08:00`（见 JSONL 中 `retrieved_at`）。
- `source_sha256` 一律为 null，原因见 JSONL 中 `source_sha256_note`：
  FBref 直接下载被 Cloudflare 拦截（HTTP 403 challenge），本机未捕获任何字节，
  哈希绝不编造。
- 只收该联赛页本身的场次，未混入其他赛事。
- 排除列（本文件与 JSONL 中一律不存在）：比分列、观众数列、裁判列、
  赛报链接列、备注列。备注列中的任何赛后信息均未写入。
- 时间规则：Time 列只取第一个时刻（如 `18:30 (08:30)` 只取 `18:30`)；
  括号内第二个时刻是抓取方时区换算值，不是源字段，已丢弃。
- 队名、场地名均为 FBref 原文照抄，未归一化（含 `PK–35` 中的 en dash、
  `Telia 5G -areena` 中的空格）。
- 行键：`2016|match_date|home_team|away_team`（即 `fixture_key`）。
  去重键为 `(match_date, home_team, away_team)`：同一对球队一季交手多次，
  不同日期即不同场次，不得合并。
- `meeting_number` 全部为 null，理由见 JSONL 中 `meeting_number_reason`：
  无权威源定义 meeting_number，禁止从日期顺序或交手次数推断。
- `csv_join_status` 全部为
  `csv_unavailable_on_this_vm_derived_from_public_schedule`：
  请求方身份 CSV 在本 VM 上不存在，本转录绝不声称与该 CSV 精确对应。

## 数量核对

| 项目 | 数值 |
|---|---|
| 呈现行数（FBref 表格数据行） | 198 |
| 去重后唯一场次 | 198 |
| 去重删除的重复呈现 | 0（无同一日期同一对球队出现两次的情况） |
| 期望场次（12 队 × 33 轮 / 2） | 198 |
| 偏差 | 0，完全吻合 |
| 日期范围 | 2016-04-02 → 2016-10-23 |
| 参赛队数（主客队并集） | 12 |
| Venue 空白数 | 0（全部 198 行均有 Venue 原文） |
| Time 列缺失数 | 0（全部 198 行均有开球时刻） |

交叉验证（均与期望一致）：

- 每个 Wk 取值 1–33 各恰好 6 行（12 队 / 2），33 × 6 = 198。
- 每支球队各出场 33 次。
- 66 个无序球队对各交手恰好 3 次（66 × 3 = 198），符合 33 轮三循环结构。

## Wk 取值与异常清单

- Wk 取值范围：1–33（全部为 FBref 原值，`official_round` 写为
  `Matchweek N (FBref)`）。
- 赛季末轮为 Wk 32（2016-10-23，6 场）；Wk 33 在赛季末并未出现，
  其 6 行全部落在赛季初与赛季中（见 A 组），原值保留、未做“纠正”。

### A 组：Wk 33 异常行（共 6 行，主异常）

| 日期 | Wk 原值 | 主队 | 客队 | 异常说明 |
|---|---|---|---|---|
| 2016-04-02 | 33 | HJK Helsinki | IFK Mariehamn | 赛季首日之前无 Wk 1，却标 33 |
| 2016-04-02 | 33 | PK–35 | RoPS | 同上 |
| 2016-07-02 | 33 | Ilves | SJK | 夹在 Wk 14/16 之间，却标 33 |
| 2016-07-03 | 33 | Lahti | KuPS | 同上 |
| 2016-07-03 | 33 | Kemi Kings | Helsinki IFK | 同上 |
| 2016-07-04 | 33 | Inter Turku | VPS | 同上 |

### B 组：其他与日期顺序不一致的 Wk 值（共 7 行，原值保留）

以下各行 Wk 值落在主序列之外，可能为补赛/提前场次，不宜直接断定为源错误，
但同样逐行列出、原值保留、不擅自改写：

| 日期 | Wk 原值 | 主队 | 客队 | 位置说明 |
|---|---|---|---|---|
| 2016-06-23 | 10 | Kemi Kings | RoPS | 出现在 Wk 14 区块之后 |
| 2016-06-28 | 2 | VPS | Ilves | 出现在 Wk 14 区块之后 |
| 2016-06-28 | 16 | Inter Turku | SJK | 出现在 Wk 15 区块之前 |
| 2016-06-29 | 2 | Lahti | Kemi Kings | 出现在 Wk 14 区块之后 |
| 2016-07-13 | 14 | VPS | PK–35 | 出现在 Wk 15 区块之后 |
| 2016-08-24 | 3 | Ilves | RoPS | 出现在 Wk 22 区块之后 |
| 2016-08-24 | 28 | HJK Helsinki | PK–35 | 出现在 Wk 23 区块之前 |

Wk 异常行合计：A 组 6 行 + B 组 7 行 = 13 行；其余 185 行 Wk 值与日期顺序一致。

## Venue 说明

- Venue 列原文照抄、未归一化；赛季内多队使用过多个场地，
  因此非常见场地不等于错误，不做纠正。
- 以下 3 行的 printed 场地与主队在本文件中的最常见场地不同，
  原文保留、请下游复核（不改写）：
  - 2016-08-26，PK–35 对 Kemi Kings，printed 为 Telia 5G -areena
  - 2016-08-27，Helsinki IFK 对 SJK，printed 为 Veritas Stadion
  - 2016-08-27，Inter Turku 对 Ilves，printed 为 Myyrmäen jalkapallostadion

## 合规自查

- JSONL 中无比分值、无比分形字符串（已用 scoreline 模式校验，0 命中；
  队名 `PK–35` 中的 en dash 不属于比分）。
- 唯一出现 "Scores" 一词的位置是任务指定的 `field_locator` 字段中的
  FBref 页面标题原文，不含任何比分数据。
- 未写入 `repo/responses/`；未声称与请求方 CSV 精确对应。
