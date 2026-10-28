# req-20261028-002 · 2024 赛季（Veikkausliiga）交叉核对与缺口填补说明

> 范围铁律：本文件只含赛前事实（身份、日期、开球时间、轮次位置、场馆、俱乐部身份）。
> 比分、赛果、赛后状态、积分榜名次细节、盘口、预测一律不写、不用于推断。
> 唯一涉及“名次”的表述是附加赛参赛资格规则（第 4 至第 8 名参赛、第 4 名直通决赛）
> 与升降级附加赛对阵资格（联赛第 11 名 vs 次级联赛第 2 名），均来自赛制说明本身，
> 不含任何一场比赛的结果。

## 1. 计数

| 指标 | 数值 |
|---|---|
| expected（-004 基线 2024 行数） | 169 |
| discovered（本轮输出行数） | 169 |
| complete（严格口径：官方轮次＋meeting_number＋UTC＋场馆全部齐备） | 0 |
| partial | 167 |
| conflict（场馆两源冲突，venue_verified 置空） | 2 |
| unavailable（行级） | 0 |
| blocked（行级） | 0 |
| missing（本轮新发现的缺失场次） | 0 |
| -004 沿用行数（fixture_key 逐字沿用） | 169 |
| -004 覆盖行数（开球时间覆盖 7 场附加赛；场馆 verified 异于候选 7 场易地＋2 场冲突标记） | 7（时间）/ 9（场馆状态变化） |
| 新增行数（-004 之外新发现的场次） | 0 |
| 轮次填补数（-004 null → 本轮填 series_or_phase） | 7 / 7（见 §2） |
| 官方数字轮次仍缺 | 7（附加赛无官方 KIERROS 编号；联赛 162 场的 1–27 仍为非官方交叉源，未升级） |
| 场馆场次级确认数 | 169 / 169 有 FBref 场次级 Venue 列对照；其中 ground 一致 confirmed 160 场、易地 moved 7 场、冲突 conflict 2 场 |
| meeting_number 可填 | 0 / 169（全部 null＋unavailable，见 §5） |

说明 complete=0 不是工作失败，而是严格口径的结果：没有任何一行的官方轮次
（official KIERROS）得到官方源逐场核实，且 meeting_number 全缺；把任何一行标
complete 都会夸大证据等级。

## 2. 7 场 null 轮次核实结果（全部填补位置，0 场仍缺位置）

原假设“欧战附加赛”只对了 5 场；另 2 场是另一项附加赛。两类附加赛分开记：

### 2a. Conference League play-off（欧战附加赛）——5 场

赛制（源：Wikipedia《2024 Veikkausliiga》Play-offs 节＋FBref 赛程表 Round 列交叉，
非官方源；官方赛制文件本轮未取得）：
- 联赛第 4 至第 8 名参赛，第 4 名直通决赛；
- 1/4 决赛与半决赛单场、排名较高者主场；决赛两回合。

| 场次 | 位置 | 开球（本地/UTC） |
|---|---|---|
| 2024-10-23 Haka vs Inter Turku | Quarter-final，单场 | 18:00 Europe/Helsinki / 15:00 UTC |
| 2024-10-23 VPS vs Gnistan | Quarter-final，单场 | 18:00 / 15:00 UTC |
| 2024-10-26 Haka vs Gnistan | Semi-final，单场 | 17:00 / 14:00 UTC |
| 2024-10-30 Haka vs SJK | Final，leg 1 of 2 | 18:00 / 16:00 UTC |
| 2024-11-02 SJK vs Haka | Final，leg 2 of 2 | 14:30 / 12:30 UTC |

UTC 换算方法：2024 年欧盟夏令时于 10 月 27 日结束；10 月 23/26 日为 EEST
（UTC+3），10 月 27 日起为 EET（UTC+2），本地时间减相应偏移。
-004 旧开球时间（16:00 / 16:00 / 15:00 / 16:00 / 12:30）已覆盖并在 JSONL
每行 kickoff_note 中注明旧值、新值、新证据；旧值语义见 §6。

### 2b. Veikkausliiga 升降级附加赛——2 场

赛制（源：同上 Wikipedia Play-offs 节＋FBref 单列竞赛
Finnish 1/2 Relegation/Promotion play-offs）：
Veikkausliiga 第 11 名（Lahti）vs 2024 Ykkösliiga 第 2 名（Jaro），
两回合决 2025 赛季最后一个顶级联赛席位。

| 场次 | 位置 | 开球（本地/UTC） |
|---|---|---|
| 2024-10-23 Jaro vs Lahti | Final，leg 1 of 2 | 18:30 / 15:30 UTC |
| 2024-10-27 Lahti vs Jaro | Final，leg 2 of 2 | 16:00 / 14:00 UTC |

注意：Jaro 不是 2024 Veikkausliiga 联赛参赛队（12 队联赛之外），
在本数据集仅以附加赛身份出现；13 支“主队”实为 12 支联赛队＋Jaro。

### 2c. 仍缺项

- 7 场的位置（series_or_phase）已全部填补，仍缺 0 场；
- 7 场的官方数字轮次（official KIERROS 编号）仍缺：附加赛在交叉源中
  只有阶段名、无数字轮次；official_round 字段填的是阶段名，
  official_round_source 标为 fbref_cross_check_non_official，
  official_round_is_official=false，不得误读为官方轮次。

## 3. 赛制结论（为什么是 169 场，不是 132 或 162）

源：Wikipedia《Veikkausliiga》Structure 节、《2024 Veikkausliiga》、
Soccerway 2025 赛季前瞻中的赛制复述、FBref 赛程表阶段列。

- 参赛队：12 队（10 支上赛季留队＋2 支升班马，见 §7）。
- 常规赛：12 队双循环（每对球队主客各 1 场），22 轮 × 6 场＝132 场。
  此阶段是双循环。
- 冠军/保级系列：常规赛后分两组（前 6 名冠军组、后 6 名保级组），
  组内单循环各 5 场（每队再赛 5 场），5 轮 × 6 场＝30 场。
  此阶段不是双循环；常规赛积分带入系列赛。
- 联赛合计：132＋30＝162 场，每队 27 场联赛——与 -004 的 1–27 轮、
  每轮 6 场完全吻合。
- 余下 7 场＝§2a 欧战附加赛 5 场＋§2b 升降级附加赛 2 场；
  162＋5＋2＝169，恰为 -004 行数，无多余、无缺失场次。
- 口径提醒：FBref 把升降级附加赛单列为另一竞赛（comp 203），
  其 Veikkausliiga 赛程表内只含 162＋5＝167 场；本数据集 169 场
  是把两类附加赛并入同一文件的计数，不应与 FBref 的 167 直接混用。

## 4. 轮次沿用说明（162 场联赛）

- 1–27 轮次值全部沿用 -004，不做任何改动；
- round_source 一律如实标为 worldfootball_matchday_non_official，
  official_round_is_official=false；
- 未升级原因：官方源（veikkausliiga.com、tulospalvelu.palloliitto.fi）
  本轮文本层不可达（见 §8）；FBref 的 Wk 列与 -004 轮次并不一致
  （如补赛场次 Wk 错位），不能用来“证实”官方轮次，故不升级；
- 任何从日期顺序推断轮次的做法均未采用。

## 5. meeting_number

全部 169 行：meeting_number=null，meeting_number_status="unavailable"。
尝试源：FBref 2024 赛程表、Wikipedia 2024 赛季页、WorldFootball
（-004 备注：文本层曾返回 403）。三者均无 meeting_number 定义或编号，
绝不从日期顺序、球队出现次数、比分、积分榜、盘口推断。

## 6. 开球时间＋时区＋源语义（重要冲突，如实保留）

- 7 场附加赛：开球本地时间已用 FBref 时间列覆盖 -004 值（旧值见 JSONL
  kickoff_note），UTC 按 §2a 换算方法给出。
- 162 场联赛：沿用 -004 开球时间，但发现系统性冲突，未批量修正：
  FBref 同一场次时间一律比 -004 晚 2 小时；抽查场 Gnistan–VPS
  （2024-08-04）有三方证据链：Tiketti 售票公告本地时间 18:30、
  FBref 18:30、-004 16:30，证明 FBref 值为本地时间、-004 值不是本地时间。
  但 FBref 页面本身未声明时区，批量把 162 场全部＋2 小时属于推断，
  故联赛行 kickoff_utc 置 null、kickoff_local 保留 -004 值并附冲突说明，
  视为“未最终核实”，需官方赛程页逐场复核（已列入 §9 待办）。
- 只有日期没有时间的源绝不猜时间：本轮所有时间均来自有明确时间的源。

## 7. 场馆：场次级升级结果（本季重点）

场馆名、城市、WGS84 经纬度、时区 Europe/Helsinki 见 JSONL；
坐标出处：-004 venue-coords.json（-004 地理编码结果），
除 Myyrmäki 候选（本轮 map.geocode 全地址结果）与
Ekenäs Centrumplan 别名坐标（本轮 map.geocode，见下）外均未重测。

### 7a. 计数

- 场次级对照完成：169 / 169（FBref Venue 列逐场对照）；
- confirmed（实际球场＝候选球场，含名变体）：160 场；
- moved（实际球场≠候选球场，已核实易地）：7 场；
- conflict（两源直接冲突，venue_verified 置空）：2 场；
- unavailable / blocked（场馆）：0 场。

### 7b. Gnistan：火灾易地是本季最大场馆修正

- 2024-07-13，Mustapekka Areena 主看台火灾，俱乐部宣布剩余赛季
  无法在该场进行（The Stadium Business 2024-07-17；Reuters 转述）。
- 剩余赛季临时主场：Bolt Arena（Töölö Football Stadium，赫尔辛基），
  证据：The Stadium Business 2024-07-22（剩余赛季在 Bolt Arena）
  ＋ Tiketti 2024-08-04 场次公告（Bolt Arena, Helsinki）
  ＋ FBref 该场 Venue 列。
- 受影响的 7 个 Gnistan 主场（venue_status=moved，venue_verified=Bolt Arena）：
  2024-08-04 vs VPS、2024-08-18 vs AC Oulu、2024-08-21 vs Mariehamn、
  2024-09-01 vs Ilves、2024-09-15 vs Mariehamn、2024-09-27 vs AC Oulu、
  2024-10-05 vs Lahti。
  -004 对这 7 场标 Mustapekka Areena 是错的，已修正。
- 火灾前 7 个 Gnistan 主场仍为 Mustapekka Areena（Oulunkylä Football Stadium）；
  FBref 6 月场次出现的 FAIR PAY Areena 是同一球场旧赞助名
  （球场史：2006 年 Fair Pay Areena，2017 年改名 Mustapekka），非另一球场。
- 许可背景（球场史源）：2024-02-22 确认 Gnistan 在 Oulunkylä 进行
  Veikkausliiga 比赛，按联赛要求装了灌溉系统、升级灯光、容量 1,100→2,200。

### 7c. Ekenäs：名变体已澄清，易地未证实，许可文件仍缺

- 三名同一球场：FBref 芬兰语名 Tammisaaren keskuskenttä、
  Wikipedia 赛季表 Ekenäs Centrumplan、-004 赞助名 Ekenäs Sparbank Arena；
  依据：bsportsfan 俱乐部页（Sparbank Arena 前称 Centrumplan）。
  其余 12 个 Ekenäs 主场按此同一球场确认（confirmed），坐标沿用 -004
  Sparbank 锚点（59.97706, 23.43948）；本轮 map.geocode 的 Centrumplan
  坐标（59.97345, 23.44287）与之约 0.4 公里，属同一球场不同测绘锚点，
  已并列记入 venue_candidates，不另立球场。
- 许可/达标问题：本轮未找到 Ekenäs 主场许可、豁免或改造工程的
  可靠来源；“升班马主场是否达标、有无易地”中的“有无易地”除下述
  冲突场外无证据，“是否达标”仍为开放项（§9）。
- 冲突场（非易地结论）：2024-04-21 Ekenas vs AC Oulu——
  FBref 称 Myyrmäen jalkapallostadion（万塔），Sportsmole 称
  Ekenas Centrumplan；两源冲突，venue_verified 置空，
  两个候选（含 Myyrmäki 全地址坐标 60.26024, 24.84279）全部保留。

### 7d. 其他队

- VPS：Lemonsoft Stadion＝Hietalahti Stadium（赞助名与通用名），
  同一球场，14 个主场 confirmed（-004 venue-coords 同球场备注佐证）。
- Jaro：Jakobstads Centralplan（FBref）＝Centralplan（Wikipedia 附加赛节），
  同一 Jakobstad 球场；俱乐部页现名 Project Liv Arena 为后期赞助名，
  不用于 2024 场次。
- Haka、Ilves、SJK、KuPS、HJK、Inter Turku、Lahti、AC Oulu、Mariehamn：
  FBref 场次级 Venue 列与 -004 候选一致（仅大小写/拼写差异，
  如 Raatin stadion），confirmed。

### 7e. 冲突清单（2 场，需官方比赛页裁决）

1. 2024-04-21 Ekenas vs AC Oulu：FBref Myyrmäki vs Sportsmole Centrumplan。
2. 2024-04-27 AC Oulu vs VPS：FBref＋Sky Sports Lemonsoft Stadion（瓦萨）
   vs Sportsmole Raatin stadion（奥卢）＋-004 Raatin 映射。
   两场均未采信任一方，venue_verified=null，venue_status=conflict。

## 8. 俱乐部官方身份（每队摘要，详见 JSONL home/away_club_identity）

- 建队年只写本轮有源的：Ekenäs IF 1905、IF Gnistan 1924、
  FC Haka 1934、FF Jaro 1965-12-18、FC Lahti 1996（11 月合并成立）、
  AC Oulu 2002、SJK 2007；其余 6 队（HJK、Ilves、Inter Turku、KuPS、
  Mariehamn、VPS）本轮未核实，founded_year 置 null，绝不凭记忆填。
- 升班马（有源）：Ekenäs IF——2023 Ykkönen 冠军，时隔 90 年重返顶级联赛；
  IF Gnistan——2023 Ykkönen 第 2 名，因 FC Honka 破产被降级而递补，
  队史首次顶级联赛赛季。两人身份不同，绝不合并（冠军直升 vs 递补）。
- 降级/更名/前身（有源）：FC Lahti 1996 年 11 月由 FC Kuusysi 与
  Reipas Lahti 合并成立，承接 Kuusysi 的 Ykkönen 席位；2024 年作为联赛
  第 11 名参加升降级附加赛（对手 Jaro）后降级；Ekenäs IF 2024 年
  第 12 名降级（Wikipedia 赛季页 Team changes 节）。
- 名字相似绝不合并：-004 的 ASCII 名（Ekenas、Gnistan、Mariehamn 等）
  与 FBref/Wikipedia 全名（Ekenäs IF、IF Gnistan、IFK Mariehamn 等）
  已在 identity 对象中并列，不做身份合并推断。

## 9. 未覆盖与冲突清单（待主代理／真浏览器跟进）

1. 官方轮次：联赛 162 场的官方 KIERROS 编号未取得；附加赛 7 场的
   官方数字轮次不存在于交叉源。需 veikkausliiga.com 或
   tulospalvelu.palloliitto.fi 的真浏览器／官方档案核查。
2. 联赛 162 场开球本地时间：FBref 与 -004 系统性差 2 小时（§6），
   需官方赛程页逐场复核后才能批量修正并补 kickoff_utc。
3. 场馆冲突 2 场（§7e）：需官方比赛页裁决实际球场。
4. Ekenäs 主场许可／达标文件：未找到来源，开放项。
5. 6 队建队年未核实（HJK、Ilves、Inter Turku、KuPS、Mariehamn、VPS）：
   需俱乐部官方页或 Wikipedia 俱乐部页逐个核实。
6. meeting_number：无定义来源，需请求方明确该编号的定义与来源，
   否则永久 unavailable。
7. CSV 联结：请求方身份 CSV（Windows 路径）本 VM 不存在；
   全部 169 行 csv_join_status="matched_to_req-20261006-004_row_csv_join_pending"，
   未做任何模糊匹配；待主代理提供 CSV 后再联结。

## 10. 尝试过但失败／受限的源

- veikkausliiga.com（含 2024 官方比赛页，如 Gnistan–VPS 4.8.2024
  的 otteluseuranta 页在搜索结果中出现，但文本层未取得可用于
  逐场核对的结构化字段）：JS 渲染，子代理无真浏览器能力，
  未作为本轮字段证据；已列入真浏览器跟进项。
- tulospalvelu.palloliitto.fi：JS-only 应用，文本层不可达
  （与 -004 结论一致）。
- WorldFootball.net 轮次页：-004 备注文本层曾返回 403；
  本轮未重复撞墙，沿用 -004 的非官方分组标签，不升级。
- Wikipedia 赛季页：可达，但其 2024 赛季球场表为赛季级映射，
  不能作为场次级证据；附加赛节与 Team changes 节用作交叉源，
  非官方源。

## 11. Provenance 铁律执行情况

- 每个非 null 字段均有 provenance 对象（source_url、final_url、
  retrieved_at=2026-10-28T16:14:41+08:00、field_locator、source_name）；
- source_sha256 全部为 null：本轮均为文本层抓取、无字节下载；
  -004 的描述符哈希一律未继承、未冒充源证据哈希；
- 坐标：-004 venue-coords.json 注明出处（非字节哈希），
  Myyrmäki 与 Centrumplan 别名坐标注明本轮 map.geocode 来源；
- 覆盖处：7 场附加赛开球时间、7 场 Gnistan 易地场馆、2 场冲突标记
  均在 JSONL kickoff_note / notes 中注明旧值、新值、新证据。

## 12. 文件

- `season_2024.jsonl`：169 行，每行一个场次（字段见任务清单，
  另含 kickoff_note、official_round_is_official、meeting_number_note、
  csv_join_note 等辅助字段）。
- `season_2024_notes.md`：本文件。
