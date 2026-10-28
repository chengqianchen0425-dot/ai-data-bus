# FBref 2018 Eliteserien 逐场场馆证据提取说明

> 本文件只做证据提取，不做最终裁决。`baseline_match` 采用字符串精确比对：
> FBref 场馆名与基线场馆名字符串完全相等记 `agree`，否则记 `differ`。
> 名称相近是否同一场馆、场馆差异是否成立，均留给裁决环节判定，本文件不改写任何比对结果。

## 来源与抓取

- 来源页 URL（预期 URL 一次打开即成功，无需站内搜索另找 URL）：
  `https://fbref.com/en/comps/28/2018/schedule/2018-Eliteserien-Scores-and-Fixtures`
- 抓取方式：`browser.open` 页面文本抓取（未用 curl，未登录，未用任何密钥/凭证，未动用 API-Football 付费额度）。
- 本次提取时间（`retrieved_at`，Asia/Shanghai）：2026-10-28T16:00:27+08:00。
- 抓取工具回显的页面存档戳：2026-08-30 11:33 UTC（仅为工具侧页面快照时间，不是本次提取时间）。
- 提取列：仅赛程表的 Venue 列，按 `(local_date + 主客队)` 配对；其余列未写入任何交付文件。
- FBref 赛程表无城市列，因此全部 240 行的 `fbref_venue_city` 均为 `null`（未用基线城市或场馆名推断城市）。

## 交付文件

- `fbref_venue_2018.jsonl`：240 行，每行一个 `record_key`，与基线 2018 年 240 行一一对应，无缺失、无多余。
- `evidence/fbref_2018_schedule_venue_only.md`：页面文本证据，仅含 local_date、FBref 主队、FBref 客队、Venue 列四列，共 240 行。
- 基线文件 `baseline_2018_2019.jsonl` 只读，未改动。

## 计数

| baseline_match | 计数 |
| --- | --- |
| agree | 150 |
| differ | 90 |
| no_fbref_value | 0 |
| page_unreachable | 0 |
| 合计 | 240 |

- 页可达，240 行的 Venue 列均有值，无空值、无 `page_unreachable` 行。

## 配对方法与队名归一化

- 配对键：基线 `local_date` + 归一化后的主客队；基线与 FBref 队名拼写不同时按以下映射归一化，JSONL 中同时保留 FBref 原文队名，报告中双方原文均列出。
- 改期场次已逐一核对日期：2018-04-11 的两场、2018-04-25 的两场，基线日期与 FBref 日期一致。

| 基线拼写（api-football 原文） | FBref 拼写 |
| --- | --- |
| Bodo/Glimt | Bodø/Glimt |
| Brann | Brann |
| Haugesund | Haugesund |
| Kristiansund BK | Kristiansund |
| Lillestrom | Lillestrøm |
| Molde | Molde |
| ODD Ballklubb | Odd |
| Ranheim | Ranheim |
| Rosenborg | Rosenborg |
| Sandefjord | Sandefjord |
| Sarpsborg 08 FF | Sarpsborg 08 |
| Stabaek | Stabæk |
| Start | Start |
| Stromsgodset | Strømsgodset |
| Tromso | Tromsø |
| Valerenga | Vålerenga |

## 配对不上的场次清单

- 无。240 行全部按 `(local_date + 主客队)` 配上 FBref 赛程行，无硬配、无按队名以外字段推断的场次。

## 截断场馆清单

- 无。240 个 FBref 场馆名均完整，无以 `...` 结尾的截断项。

## differ 明细（仅供裁决参考，不改变 baseline_match）

按字符串对分组，differ 共 90 行：

| 基线场馆名 | FBref 场馆名 | 行数 |
| --- | --- | --- |
| Alfheim | Alfheim Stadion | 15 |
| Nadderud | Nadderud Stadion | 15 |
| Sør Arena | Sparebanken Sør Arena | 15 |
| Åråsen | Åråsen Stadion | 15 |
| Lerkendal | Lerkendal Stadion | 1 |
| Lerkendal | Abrahallen | 14 |
| Ranheim Arena | EXTRA Arena | 14 |
| Ranheim Arena | Aker Stadion | 1 |

- agree 的 150 行分布：Aspmyra Stadion、Brann Stadion、Haugesund Stadion、Kristiansund Stadion、Aker Stadion（Molde 主场）、Skagerak Arena、Sarpsborg Stadion、Marienlyst Stadion、Intility Arena、Komplett.no Arena 各 15 行。
- FBref 场馆名出现频次：Aker Stadion 16（含下述 Ranheim 例外 1 行）、其余主场场馆各 15 行、EXTRA Arena 14 行、Abrahallen 14 行、Lerkendal Stadion 1 行。

## 需裁决方特别留意的逐场例外（原文照抄，未修正）

以下 2 行的 FBref Venue 值与该队其余主场的 Venue 值不同，均按页内原文写入 JSONL，未按“主队默认主场”改写：

1. `eliteserien-2018-r02-rosenborg-vs-kristiansund-bk`，2018-03-17，FBref 主队 Rosenborg vs Kristiansund，Venue 列原文为 `Lerkendal Stadion`（浏览器文本行 L26 附近；该队其余 14 个主场行 Venue 列均为 `Abrahallen`）。
2. `eliteserien-2018-r01-ranheim-vs-brann`，2018-04-25，FBref 主队 Ranheim vs Brann，Venue 列原文为 `Aker Stadion`（浏览器文本行 L114 附近；该队其余 14 个主场行 Venue 列均为 `EXTRA Arena`）。

- 其余 238 行的 Venue 值与该队主场行的常见 Venue 值一致，但每行仍是该行 Venue 列本身的取值，不是球队主场表推断。

## 限制与未做事项

- 未返回任何比分、赛果、赔率、积分榜、预测及相关字段；证据文件仅含 Venue 相关列。
- 未把主队默认主场当作本场证据；未对 differ 行做同一场馆与否的裁决。
- 本次为 FBref 单源逐场证据；如需交叉核验，需由裁决环节另取独立源比对。
