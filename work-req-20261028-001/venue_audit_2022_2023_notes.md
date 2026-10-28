# Eliteserien 2022–2023 实际比赛日场馆审计 · 说明文件（req-20261028-001 C 路）

## 1. 计数（按赛季）

| 赛季 | expected | discovered | confirmed | neutral | moved | conflict | unavailable | blocked | missing |
|---|---|---|---|---|---|---|---|---|---|
| 2022 | 240 | 240 | 240 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2023 | 240 | 240 | 240 | 0 | 0 | 0 | 0 | 0 | 0 |
| **合计** | **480** | **480** | **480** | **0** | **0** | **0** | **0** | **0** | **0** |

- 480 行全部齐全，record_key 与基线一一对应（逐行比对联结字段 0 处差异）。
- 全部 480 行 `venue_status = confirmed`，但核验层级一律为
  `non_official_dual_source`（非官方双源一致），**不是 NFF 官方确认**——见 §5。
- 未发现任何一场偏离主队常规球场：无 moved、无 neutral、无 conflict 行。
  状态判定方法是把每场有证据的场馆与该队全部主场有证据场馆集合及对手球场集合比对，
  未从赛果、积分榜、赔率、另一场比赛推断任何状态。

## 2. 交付文件

- `venue_audit_2022_2023.jsonl`：480 行，每行一个 record_key。
  联结字段（record_key、season、local_date、home_team、away_team、kickoff_local、
  round、round_label、provider_fixture_id）与基线 venue 字段全部逐字复制，程序比对 0 差异。
- 本文件：计数、证据源、未覆盖与冲突清单。
- 证据目录 `evidence/`：Nominatim 原始 JSON（`nominatim/*.json`）＋查询日志
  （`nominatim/query_log.json`，含每次查询的 retrieved_at，Asia/Shanghai +08:00）
  ＋地理编码脚本（`geocode.py`、`geocode2.py`）＋本审计构建脚本
  （`build_venue_audit_2022_2023.py`）。
- 本路未写 `repo/responses/`（主代理的事）。

## 3. 证据源清单

### 3.1 身份基线（绝不改动）

`~/workspace/ai-inbox/repo/work-req-20261017-002/fixtures_2018_2025.jsonl` 中
season=2022 或 2023 的 480 行，抽取为 `baseline_480.json`。
每行基线 venue 来自 api-football fixture.venue（来源拼写保留），基线 venue 无空值。

### 3.2 FBref 赛程表 Venue 列（非官方，可作候选证据）

| 赛季 | URL | 文本层页面 ID | 文本层抓取日期 |
|---|---|---|---|
| 2022 | https://fbref.com/en/comps/28/2022/schedule/2022-Eliteserien-Scores-and-Fixtures | 677758559027529054 | 2026-09-04 |
| 2023 | https://fbref.com/en/comps/28/2023/schedule/2023-Eliteserien-Scores-and-Fixtures | 1143704444911427442 | 2026-10-19 |

- 两季第一张表均已完整读完：2022 表含 240 场联赛＋2 行挪威甲乙升降级附加赛；
  2023 表含 240 场联赛＋2 行升降级附加赛。**附加赛行不在基线内，已排除。**
- 关键规律：FBref 中每支主队全季场馆恒定。输出文件中的 FBref 值即该队该季恒定值；
  若有任何一场偏离，恒定性即被打破——完整阅读中未见偏离。
- FBref 文本层无可下载字节，故 `fbref_evidence_sha256` 置 null（已注明原因，非编造）。

FBref 队季场馆恒定值（基线 home_team 原文拼写）：

| 主队（基线拼写） | 2022 FBref | 2023 FBref |
|---|---|---|
| Aalesund | Color Line Stadion | Color Line Stadion |
| Bodo/Glimt | Aspmyra Stadion | Aspmyra Stadion |
| Brann | —（2022 不在顶级联赛） | Brann Stadion |
| Ham-Kam | Briskeby Arena | Briskeby Arena |
| Haugesund | Haugesund Stadion | Haugesund Stadion |
| jerv | J.J. Ugland Stadion - Levermyr | —（2023 降级） |
| Kristiansund BK | Kristiansund Stadion | —（2023 降级） |
| Lillestrom | Åråsen Stadion | Åråsen Stadion |
| Molde | Aker Stadion | Aker Stadion |
| ODD Ballklubb | Skagerak Arena | Skagerak Arena |
| Rosenborg | Lerkendal Stadion | Lerkendal Stadion |
| Sandefjord | Komplett.no Arena | Komplett.no Arena |
| Sarpsborg 08 FF | Sarpsborg Stadion | Sarpsborg Stadion |
| Stabaek | —（2022 不在顶级联赛） | Nadderud Stadion |
| Stromsgodset | Marienlyst Stadion | Marienlyst Stadion |
| Tromso | Alfheim Stadion | Alfheim Stadion |
| Valerenga | Intility Arena | Intility Arena |
| Viking | SR-Bank Arena | SR-Bank Arena |

### 3.3 更名时间线（公开来源，用于裁决命名差异为同一球场）

| 球场 | 更名时间线 | 结论 |
|---|---|---|
| Sandefjord | Komplett.no Arena 至 2019-11 撤赞助；2021-05-05 起 Release Arena；2023-09-05 起 Jotun Arena（Wikipedia "Sandefjord Arena" 条目；坐标 59.13725°N, 10.17969°E） | FBref 两季的 Komplett.no Arena 是过期旧名；基线 Release（至 2023-08-27）/ Jotun（自 2023-09-16 起）分段与时间线吻合 |
| Tromso | Alfheim Stadion 于 2023-03-29 更名为 Romssa Arena（NRK 2023-03-29 报道，Wikipedia 引用） | 2023 赛季首个主场 2023-04-10 在更名之后，故 2023 全季当期名为 Romssa Arena；FBref 2023 的 Alfheim 是旧名标签 |
| Haugesund | Haugesund Stadion 于 2021-05 更名为 Haugesund Sparebank Arena（FK Haugesund 2021-05-27 公告，6 年冠名；Nordic Stadiums 复述） | 2022–2023 当期名均为 Haugesund Sparebank Arena；FBref 的 Haugesund Stadion 是通用旧名标签 |
| Viking | Viking Stadion（2004–2018）→ SR-Bank Arena（2018-04–2024）→ Lyse Arena（2025-01 起）（Wikipedia "Viking Stadion"；StadiumDB） | 2022–2023 当期名为 SR-Bank Arena；Nominatim 当前标签 Lyse Arena 是 2025 年后新名，同一球场 |
| Jerv | FBref 自带 "J.J. Ugland Stadion - Levermyr" | Levermyr 为所在地后缀，与基线 "J.J. Ugland Stadion" 同一球场 |
| Stabaek / Nadderud | 基线 city 在 2023 季内由 Bekkestua（前 6 个主场）切换为 Bærum（2023-07-03 起）；Nominatim 定位显示 Nadderud stadion 位于 Bekkestua, Bærum | Bekkestua 是 Bærum 市镇内的地点，非换场；verified city 按基线逐行保留 |

**一般规律（本路重要发现）：FBref 的 Venue 列使用较旧/通用标签，基线使用比赛日当期冠名。
两者差异全部是命名变体，无一场是去了另一座球场。verified 实际比赛日场馆名一律取
比赛日当期名（本路 480 行中均等于基线名）；FBref 名全部保留为竞争性候选，未静默取舍。**

### 3.4 坐标源：OpenStreetMap Nominatim（免费，无密钥）

- 查询格式：`"<场馆名>, <城市>, Norway"`，限速约 1 请求/秒，规范 User-Agent。
- 21 次查询（含 3 次零结果重试，见 §6），查询日志 `evidence/nominatim/query_log.json`
  （检索时间 2026-10-28T16:03:53–16:04:35+08:00）。
- 每行输出含：Nominatim 坐标、display_name、class/type/importance、结果数、
  证据文件路径与**实际计算的 SHA-256**（构建时从磁盘字节重算）。
- 坐标是场馆级的，不是场次级的：同球场各行共用一次地理编码结果，
  输出中已注明“场馆级证据，非本场专属确认”。

## 4. 场馆级坐标覆盖

- 18 座球场（合并更名变体后）全部获得 Nominatim 坐标：**18/18**。
- 480 行全部带坐标：**480/480**，无 null。
- 各场馆行数：Color Line、Aspmyra、Briskeby、Haugesund Sparebank、Aker、Skagerak、
  Sarpsborg、Åråsen、Lerkendal、Marienlyst、Intility、SR-Bank 各 30 行；
  Release 24 行；J.J. Ugland、Kristiansund、Alfheim、Brann、Nadderud、Romssa 各 15 行；
  Jotun 6 行。

基线坐标与 Nominatim 坐标对比（同一球场，两源定位点差异）：

| 球场 | 行数 | 基线坐标 | Nominatim 坐标 | 差异 |
|---|---|---|---|---|
| Åråsen Stadion | 30 | 59.96273, 11.06365 | 59.9627403, 11.0635660 | 0.005 km |
| Aker Stadion | 30 | 62.73352, 7.14805 | 62.7334015, 7.1480721 | 0.013 km |
| Aspmyra Stadion | 30 | 67.27676, 14.38437 | 67.2766478, 14.3844344 | 0.013 km |
| Brann Stadion | 15 | 60.36619, 5.35136 | 60.3668333, 5.3574265 | 0.341 km |
| Briskeby Arena | 30 | 60.79356, 11.09418 | 60.7955818, 11.0922051 | 0.249 km |
| Color Line Stadion | 30 | 62.47027, 6.18723 | 62.4696703, 6.1885733 | 0.096 km |
| Haugesund Sparebank Arena | 30 | 59.41258, 5.27719 | 59.4130886, 5.2795151（以 Haugesund Stadion 查询命中） | 0.143 km |
| Intility Arena | 30 | 59.91799, 10.80533 | 59.9179048, 10.8066324 | 0.073 km |
| J.J. Ugland Stadion | 15 | 58.34550, 8.59170 | 58.3457607, 8.5921239（以 Levermyr Stadion 查询命中） | 0.038 km |
| Kristiansund Stadion | 15 | 63.12485, 7.71897 | 63.1257600, 7.7190380 | 0.101 km |
| Lerkendal Stadion | 30 | 63.41208, 10.40225 | 63.4123264, 10.4044664 | 0.114 km |
| Marienlyst Stadion | 30 | 59.73399, 10.20247 | 59.7343801, 10.2015510 | 0.067 km |
| Nadderud Stadion | 15 | 59.91923, 10.58034 | 59.9213185, 10.5804579 | 0.232 km |
| Release / Jotun Arena（Sandefjord） | 30 | 59.17544, 10.21542 | 59.1371935, 10.1795249（以 Jotun Arena 查询命中） | **4.720 km ⚠️** |
| Sarpsborg Stadion | 30 | 59.28322, 11.10629 | 59.2862886, 11.0977153 | 0.595 km |
| Skagerak Arena | 30 | 59.21218, 9.58932 | 59.2115860, 9.5899848 | 0.076 km |
| Alfheim / Romssa Arena（Tromso） | 30 | 69.64911, 18.93890 | 69.6489185, 18.9343489（以 Romssa Arena 查询命中） | 0.177 km |
| SR-Bank Arena（Viking） | 30 | 58.91393, 5.73128 | 58.9145955, 5.7309977（以 Viking Stadion 查询命中，当前标签 Lyse Arena） | 0.076 km |

**⚠️ 唯一坐标异常：Sandefjord。** 基线坐标（59.17544, 10.21542）与 Nominatim
（59.1371935, 10.1795249）相距 4.72 km；Wikipedia 记载的 Sandefjord Arena 坐标
（59.13725, 10.17969）与 Nominatim 几乎一致。两源对一源，基线该球场坐标存疑。
球场身份本身无争议（名称＋FBref＋更名时间线三方一致），仅坐标取值有分歧；
输出中两值并存（baseline_venue_lat/lon 与 venue_lat/lon_nominatim＋delta 字段），
下游如需单值坐标，建议采用 Nominatim 值。

## 5. 未覆盖与冲突清单

### 5.1 NFF 官方确认：0/480（本轮最大障碍）

- 2023 的 tournamentId=186850 已知，但旧 fotballdata URL 模式已死：
  `fotballdata/turnering/tabell/?tournamentId=186850` 返回 301 后落到 SPA 壳页 404
  （证据：`evidence/nff_2023_terminliste.html`，61,617 字节，404 壳页面；
  `evidence/nff_2023_tabell.html`）。文本层无法拿到逐场官方场馆。
- 2022 的 tournamentId 经两次搜索未发现 fotball.no 赛事页，**未照抄 2023 的编号、
  未猜测编号**。
- 因此本路所有 confirmed 行的核验层级均为“非官方双源一致（基线 api-football
  ＋ FBref）”，绝不声称为 NFF 官方确认。如需官方层，需主代理走真浏览器任务
  或另寻 NFF 新站 API/页面结构（不在本路能力内，已如实记 blocked 原因，
  但因每行已有双源非官方证据，行状态仍为 confirmed 而非 blocked——
  blocked 在此仅指“官方源不可达”这一证据层缺失，见本节说明）。

### 5.2 命名冲突：0 项（全部已裁决为同一球场）

- 全部命名差异见 §3.3（Sandefjord、Tromso、Haugesund 三组 FBref 旧名标签；
  Viking 的 Nominatim 当前标签 Lyse Arena；Jerv 的 Levermyr 后缀；
  Nadderud 的 Bekkestua/Bærum 地点-市镇关系）。
- 无任何一场基线与 FBref 指向不同球场，无 conflict 行。

### 5.3 零结果的 Nominatim 查询（3 次，均已用别名重试命中）

| 零结果查询 | 重试查询 | 结果 |
|---|---|---|
| Haugesund Sparebank Arena, Haugesund | Haugesund Stadion, Haugesund | 3 条，首条即该球场 |
| J.J. Ugland Stadion, Grimstad | Levermyr Stadion, Grimstad | 2 条，首条即该球场 |
| SR-Bank Arena, Stavanger | Viking Stadion, Stavanger | 1 条，当前标签 Lyse Arena（2025 年后新名，同一球场） |

零结果 JSON 文件与 SHA-256 同样存档于 `evidence/nominatim/` 并在各行
`coordinate_provenance.zero_result_queries_for_this_ground` 中引用。

### 5.4 其他

- 无 missing 行（expected 480 = discovered 480）。
- 无 unavailable 行（每行均有基线＋FBref 双源逐场证据）。
- 本路未动用任何付费 API 额度（API-Football 额度一律未动）；未购买、未登录、
  未使用任何密钥/凭证。
- 严格排除项遵守情况：输出中无 2026 赛季、无赔率、无比分/赛果、无积分榜、
  无奇门/干支/预测/概率/Snapshot/Outcome/Review/Gold 字段（程序检查 0 命中）；
  未计算真太阳时；未写任何本地奇门项目文件。

## 6. 方法与诚实说明（供合并方判断）

1. **FBref 转录方式**：FBref 值按“队季恒定值”转录，而非把 480 个 FBref 表格行
   逐行手工抄入——因为完整阅读证实每队全季恒定，且无一场偏离。
   恒定值转录比逐行抄写更不易出错，但方法上属于“队季级归约”；
   每行仍保留 FBref 源 URL 与页面 ID，合并方可复核。
2. **verified 名取值**：取比赛日当期名（更名时间线裁决），基线名在本路 480 行中
   恰好全部等于当期名；FBref 名全部作为竞争性候选保留。
3. **verified city 取值**：取基线逐行 city（含 Nadderud 的 Bekkestua/Bærum 分段），
   FBref 表不带 city 列，故 city 的第二源为空——city 字段的双源性弱于 name 字段，
   已如实说明。
4. **坐标**：场馆级，非场次级；Nominatim 首条结果，未做人工选点修正。
   除 Sandefjord 外，两源差异均 ≤0.6 km，属同一球场定位点正常浮动。
5. **状态口径**：confirmed 要求该场次有直接证据——本路每行均有基线逐场 venue
   与 FBref 逐场 Venue 列两项直接证据且球场身份一致；更名变体须有更名证据支撑
   方算同一球场（§3.3）。NFF 官方层缺失以 verification_level 字段明示，
   不混入 status 计数。
