# Eliteserien 2020–2021 实际比赛日场馆审计说明（B 路，480 场）

- 基线：`~/workspace/ai-inbox/repo/work-req-20261017-002/fixtures_2018_2025.jsonl` 中 season=2020 或 2021 的 480 行。
  联结字段（record_key、season、local_date、home_team、away_team、kickoff_local、round、round_label、provider_fixture_id）
  全部从基线逐字复制，脚本逐行校验通过；基线场馆字段（method_context venue_name/venue_city/venue_lat/venue_lon）
  同样逐字抄入 source_venue_*/baseline_venue_*，未修改、未重新推导。
- 输出：`venue_audit_2020_2021.jsonl`（480 行，每行一个 record_key）。本文件不含任何比分、赛果、赔率、
  积分榜、预测、奇门相关字段；坐标全部是场馆级的，不是场次级的。

## 1. 按赛季计数

| 赛季 | expected | discovered | confirmed | neutral | moved | conflict | unavailable | blocked（行级） | missing |
|---|---|---|---|---|---|---|---|---|---|
| 2020 | 240 | 240 | 240 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2021 | 240 | 240 | 240 | 0 | 0 | 0 | 0 | 0 |
| 合计 | 480 | 480 | 480 | 0 | 0 | 0 | 0 | 0 | 0 |

- confirmed 的构成：480 场全部为“双逐场源归一化后同地”——基线 api-football fixture.venue 与 FBref
  赛季表 Venue 列逐场核对后指向同一物理场馆（ground_id 一致）。39 场存在名称差异（见 §4），
  属于同一场馆的不同名称（通用名／赞助名／更名），不计入 conflict。
- neutral = 0：没有任何一场被确认为在中立场地举行。
- moved = 0：没有任何一场被确认为在非主队主场举行。2020 赛季空场／易地传闻未作任何推断：
  两源的场馆记录在全部 480 场均与主队当季常规主场一致，无直接证据支持任何一场 moved。
- blocked（行级）= 0：每一场至少有两个逐场源（基线＋FBref Venue 列）可用。但**源级 blocked 存在**：
  NFF 官方 2020/2021 赛季数据本轮 blocked（见 §3），480 行均无官方逐场证据，只有基线＋FBref
  非官方逐场证据；行内 confirmation_tier 已如实标注为 two_per_fixture_sources_agree_on_ground。
- missing = 0：480 个 record_key 全在输出文件中，无缺失、无多余。

## 2. 证据源清单（优先级按任务：NFF 官方 > 俱乐部／场馆官方 > 其他公开赛程页）

| 证据 | 覆盖 | 字段定位 | 说明 |
|---|---|---|---|
| 基线 api-football fixture.venue（method_context venue_*） | 480/480 | venue_name／venue_city／venue_lat／venue_lon，逐场 | 逐场源，但其场馆名称并非在所有赛季都是比赛日当时的名称（见 §4）；其坐标为另一地理编码器的取点（见 §5）。 |
| FBref 赛季赛程表 Venue 列（非官方，逐场） | 480/480 | 每季页第一张赛程表 Venue 列，按 (local_date, home_team, away_team) 匹配 | 当季 contemporaneous 的场馆名；2020 页文本层快照 2026-08-12 07:19 UTC，2021 页 2026-08-12 22:49 UTC；浏览器文本层无源 HTTP 状态、无字节哈希，一律记 null 并注明原因，不编造。 |
| Wikipedia 挪威足球场列表（场馆级） | 18/18 个场馆 | Stadium／City／Home team 列 | 仅用于场馆级交叉核对（俱乐部—场馆—城市归属），不是逐场证据；当前名称与 2020/2021 当时名称有 6 处不同（见 §4），均按更名处理，不作竞争场馆。 |
| OpenStreetMap Nominatim 搜索 JSON（场馆级坐标） | 18/18 个场馆 | name／class／type／lat／lon／display_name | 坐标源；证据字节已实际下载并计算 SHA-256，见 geo_evidence/；坐标是场馆级的，不是场次级的。 |
| NFF 官方 fotball.no | 0/480（源级 blocked） | — | 2020/2021 tournamentId 在既往工作（req-20261018-001）中已证实不可发现，retry_after 2026-11-19；本轮未在到期前重撞。 |

## 3. 未覆盖清单

- NFF 官方逐场场馆确认：480 场全部缺失（源级 blocked，retry_after 2026-11-19）。官方确认补齐后，
  confirmation_tier 可从 two_per_fixture_sources_agree_on_ground 升级；本轮不以非官方源冒充官方确认。
- FBref 字节哈希：两季页均为浏览器文本层读取，无下载字节，source_sha256 一律 null（已注明原因）。
- FBref 页上每季各有 1 行非联赛附加赛行（不在 240 场基线内），已排除，未计入任何计数。
  FBref 页第二张表是第一张表的重复渲染，未重复计数。

## 4. 名称差异清单（39 场，同一场馆不同名称，不计 conflict）

| 情形 | 场次 | 基线名 | FBref 当季名 | 处理 |
|---|---|---|---|---|
| Sandefjord 2020：通用名 vs 当季赞助名 | 15 | Sandefjord Arena | Komplett.no Arena | verified 名取 FBref 当季名；基线名保留为候选 |
| Sandefjord 2021：后期名 vs 当季赞助名 | 15 | Release Arena | Komplett.no Arena | 同上；基线名保留为候选 |
| Haugesund 2021：赛季中赞助更名 | 9 | Haugesund Sparebank Arena | Haugesund Stadion | verified 名取 FBref 通用名；基线名保留为候选，并记更名证据：基线在 2021-05-24 至 2021-07-18 的 6 个主场用 Haugesund Stadion，2021-07-28 起的 9 个主场用 Haugesund Sparebank Arena，基线坐标完全相同；更名公告日期未核实 |

其余 441 场的基线名与 FBref 名逐字一致。另有 6 处“当前名 vs 当季名”差异（仅影响坐标源的查询名，
不影响场馆身份，均已在行内 alternate_name_note 说明，更名时间未核实，不作竞争场馆）：
Kristiansund Stadion（现 Nordmøre Stadion）、Komplett.no Arena（现 Jotun Arena）、
Sparebanken Sør Arena（现 Sparebanken Norge Arena）、SR-Bank Arena（现 Lyse Arena）、
Alfheim Stadion（现 Romssa Arena）、Consto Arena（Nominatim 无该名条目，以其旧名 Mjøndalen Stadion
的场地条目定位，Wikipedia Consto Arena 词条列明旧名 Mjøndalen Stadion 且坐标 59.7469, 10.0146 与该条目吻合）。

城市层级注记（非分歧）：基线城市 Bekkestua（Nadderud）与 Kjeller（Åråsen）分别是 Bærum、
Lillestrøm 市镇内的 locality；verified 城市取市镇级（Bærum、Lillestrøm），行内 city_note 已说明。

## 5. 场馆级坐标（18 个场馆，480/480 行携带）

- 坐标与共享场馆坐标表 `venue_coordinate_table.json` 对齐（该表已有的 17 个场馆取值完全一致；
  唯一新增 ground_id 为 COL＝Color Line Stadion，Ålesund，该场馆不在 2018/2019 赛季范围内）。
- match_quality 分布（按行）：exact_name 330 行、renamed_current_name 90 行、alias 30 行、
  same_ground_other_name 30 行。
- 基线坐标与 Nominatim 坐标的距离（同场馆不同地理编码器取点）：除 Sandefjord 外全部在 600 m 内
  （Brann 341 m、Sarpsborg 595 m、Nadderud 233 m 为街道级附近取点，记精度注记，不记身份分歧）。
  **Sandefjord 例外：基线坐标（59.17544, 10.21542）距 Nominatim 场馆点 4,720 m，不落在场馆上**；
  本审计采用 Nominatim 场馆点（59.1371935, 10.1795249），基线坐标保留在行内供比对。
  （该结论与 2018/2019 路的同项注记一致：基线点落在距球场约 4.7 km 的居民区。）
- 坐标证据文件：`geo_evidence/`（Nominatim 搜索 JSON 原始字节，含空返回与 fallback 查询的全部尝试记录，
  各文件 SHA-256 见行内 coordinate_provenance.evidence_sha256）。

## 6. 冲突清单

- 物理场馆冲突：0 项。基线与 FBref 在 480 场中无任何一场指向不同物理场馆。
- 名称冲突：0 项计入 conflict；39 场名称差异见 §4，均已按“同一场馆不同名称”处理，候选全部保留在行内。
- 城市分歧：0 项；Bekkestua／Kjeller 仅为 locality 与市镇的层级差异，见 §4。
