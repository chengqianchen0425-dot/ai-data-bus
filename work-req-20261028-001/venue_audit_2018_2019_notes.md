# Eliteserien 2018–2019 实际比赛日场馆审计说明（req-20261028-001 A 路）

## 1. 按赛季计数

| 赛季 | expected | discovered | confirmed | neutral | moved | conflict | unavailable | blocked（行级） | missing |
|---|---|---|---|---|---|---|---|---|---|
| 2018 | 240 | 240 | 239 | 0 | 0 | 1 | 0 | 0 | 0 |
| 2019 | 240 | 240 | 240 | 0 | 0 | 0 | 0 | 0 | 0 |
| 合计 | 480 | 480 | 479 | 0 | 0 | 1 | 0 | 0 | 0 |

- confirmed 的构成：465 场为“多源一致”（基线与独立逐场源归一化后同地）；14 场为“裁决确认”（2018 Rosenborg 主场，见 §4；FBref 的 Abrahallen 主张被有理由驳回，候选仍保留在行内）。
- moved = 0：没有任何一场被确认为在非主队主场举行。唯一的异地候选（Ranheim–Brann 的 Aker Stadion）未获裁决，记 conflict，不记 moved。
- neutral = 0：没有任何一场被确认为中立场地。
- blocked（行级）= 0：每一场至少有一个独立逐场源（FBref Venue 列）可用。但**源级 blocked 存在**：NFF 官方 2018 正赛数据本轮 blocked（见 §3），2018 行没有官方逐场证据，只有 FBref 非官方逐场证据 + 基线。
- missing = 0：480 个 record_key 全在输出文件中，无缺失、无多余。

## 2. 证据源清单（优先级按任务：NFF 官方 > 俱乐部/场馆官方 > 其他公开赛程页）

| 证据 | 覆盖 | 字段定位 | 说明 |
|---|---|---|---|
| NFF fotball.no 官方赛季表（tournamentId=164089，2019） | 2019 全量 240/240 | `Alle kamper` 全表 Bane 列；单场页抽查 `Stadion:` 与 Bane 一致 | 官方逐场证据。Bane 值恰好 16 个、每队全季同一值，这是整表读完后观察到的性质，不是事先拿主场表代填。无城市列，故城市不从 NFF 补。 |
| FBref 赛程表 Venue 列（非官方，逐场） | 2018 240/240、2019 240/240 | 赛程表 Venue 列 | 独立逐场证据，但非官方。无城市列，故城市不从 FBref 补。2019 第二张表逐场值与首表一致；2019 升降级附加赛行不在基线内，已排除。 |
| 基线 api-football fixture.venue（被审计对象） | 480/480 | method_context.venue_name / venue_city | 即 source_venue。单方不构成 confirmed，必须有独立逐场源归一化一致（或裁决）才确认。 |
| Nominatim / OpenStreetMap（坐标） | 19 个场地（18 个确认场地 + 1 个竞争候选） | 搜索 JSON 首个 leisure/stadium-or-pitch 结果 | 实字节下载（走代理 curl），每份 JSON 存 evidence/nominatim/ 并算 SHA-256。坐标是场馆级，不是场次级。 |

城市口径：FBref 与 NFF 表均无城市列，因此 verified_actual_matchday_venue_city 一律沿用同一场地基线城市，并已用 Nominatim display_name 的 locality 交叉核对（18 场地均一致）；行内已注明城市来源，不冒充为 FBref/NFF 所载。

## 3. 未覆盖清单

- **NFF 官方 2018 正赛：blocked，0 场。** 轻量搜索只命中升降级附加赛（tournamentId=163384，不可误作正赛入口）与 G19 青年组（161695），正赛 tournamentId 不可发现；沿用前序 retry_after=2026-11-19，本轮未硬试、未猜 ID。
- **NFF / FBref 城市列：全部缺失。** 两源逐场表均无城市字段，城市只来自基线 + 坐标证据（见 §2）。
- **2018 官方逐场证据缺口**：2018 行的 confirmed 建立在 FBref（非官方）+ 基线 + 裁决理由上，没有官方背书；若需官方级确认，须等 2026-11-19 后重探 NFF 2018 入口。
- **其余无未覆盖**：FBref 两季、NFF 2019、坐标 19 场地全部齐全。

## 4. 冲突清单（共 1 行级冲突 + 2 项场馆级注记）

### 4.1 行级冲突（verified 置 null，两边候选全保留）

- **eliteserien-2018-r01-ranheim-vs-brann（2018-04-25，Ranheim vs Brann）**：基线 Ranheim Arena（即 EXTRA Arena）vs FBref Aker Stadion（Molde）。2018 Ranheim 赛季页逐场写 EXTRA Arena、特鲁姆瑟，并注明本场原定 3 月 10 日、改期至 4 月 25 日；EXTRA Arena 在 4 月 2 日、15 日、28 日的 Ranheim 主场都在正常使用，未找到单场挪到 Molde 的原因；两边观众数与裁判相同，无法区分；FBref 三个页面（联赛表、对战表、比赛日志）同属一个数据源家族，只算一方证据。NFF 2018 blocked，无官方裁决。本行不记 moved（未确认异地），不记 confirmed。

### 4.2 裁决确认（14 场，confirmed，但驳回理由写进 conflict_note，候选不删除）

- **2018 Rosenborg 14 个主场（FBref 写 Abrahallen，基线写 Lerkendal）**：确认为 Lerkendal Stadion。驳回理由：① FBref 自身不一致——其欧战日志写 Rosenborg 主场为 Lerkendal Stadion，联赛表却写 Abrahallen，且联赛表里 2018-03-17 对 Kristiansund 一场写 Lerkendal Stadion；② Abrahallen 行的观众数为 Lerkendal 量级（最高约 21,201），而 Abrahallen 是室内训练馆，不可能容纳该量级观众；③ 2018 Rosenborg 赛季页逐场写主场为 Lerkendal Stadion；④ Rosenborg 主场即 Lerkendal Stadion（容量约 21,116）。另 1 场（2018-03-17 对 Kristiansund）FBref 与基线本来一致，直接确认。

### 4.3 场馆级坐标注记（不影响场馆身份，只影响坐标精度）

- **Komplett.no Arena（Sandefjord）坐标冲突**：基线坐标（59.17544, 10.21542）反查为居民区 Søndre Kullerød，离球场 4.7 公里；基线自带证据也标注该次地理编码 relevance=68、medium confidence（经由 Release Arena 别名）。本审计采用 Nominatim 球场坐标（59.1371935, 10.1795249，Jotun Arena 球场），基线坐标保留在行内供比对。
- **Brann（341m）、Sarpsborg（595m）、Nadderud（233m）**：基线点为街道级附近点位（Brann 靠近车站一侧街道、Sarpsborg 为 Enenda 街区），与球场为同一场地不同取点，记精度注记，不记身份冲突。其余场地基线与 Nominatim 距离均在 180m 内。

## 5. 名称归一化 / 别名表（只用于判定“同一物理场地”，原文拼写全部保留在行内）

| 场地 | 基线名 | FBref 名 | NFF 2019 名 | 现用 OSM 名 |
|---|---|---|---|---|
| Bodø | Aspmyra Stadion | Aspmyra Stadion | Aspmyra stadion | Aspmyra stadion |
| Tromsø | Alfheim | Alfheim Stadion | Romssa Arena | Romssa Arena |
| Molde | Aker Stadion | Aker Stadion | Aker stadion | Aker Stadion |
| Bergen | Brann Stadion | Brann Stadion | Brann stadion | Brann Stadion |
| Haugesund | Haugesund Stadion | Haugesund Stadion | Haugesund Sparebank Arena | Haugesund stadion |
| Oslo | Intility Arena | Intility Arena | Intility Arena | Intility Arena |
| Mjøndalen | Isachsen Stadion | Consto Arena | Consto Arena | Mjøndalen stadion（Isachsen/Consto 在 OSM 无命中，以 Mjøndalen 镇球场为准，离基线点 55m） |
| Sandefjord | Komplett.no Arena | Komplett.no Arena | —（2019 降级不在 NFF 2019 表内） | Jotun Arena |
| Kristiansund | Kristiansund Stadion | Kristiansund Stadion | Nordmøre stadion | Nordmøre stadion |
| Trondheim | Lerkendal（2018）/ Lerkendal Stadion（2019） | Lerkendal Stadion（2018 仅 1 场；其余 14 场写 Abrahallen，见 §4.2） | Lerkendal stadion | Lerkendal Stadion |
| Drammen | Marienlyst Stadion | Marienlyst Stadion | Marienlyst stadion | Marienlyst stadion |
| Bærum | Nadderud | Nadderud Stadion | Gamle Nadderud stadion（括号内为入口方向说明，非另一场地） | Nadderud stadion |
| Ranheim | Ranheim Arena | EXTRA Arena | EXTRA Arena | Extra Arena |
| Stavanger | SR-Bank Arena | SR-Bank Arena | Lyse Arena | Lyse Arena |
| Sarpsborg | Sarpsborg Stadion | Sarpsborg Stadion | Sarpsborg st KG（KG = kunstgress，指 Sarpsborg Stadion 人造草坪场地，非另一球场、不记 moved） | Sarpsborg stadion |
| Skien | Skagerak Arena | Skagerak Arena | Skagerak Arena | Skagerak Arena |
| Kristiansand | Sør Arena | Sparebanken Sør Arena | —（2019 降级不在 NFF 2019 表内） | Sparebanken Norge Arena |
| Lillestrøm | Åråsen | Åråsen Stadion | Åråsen stadion | Åråsen Stadion |
| 竞争候选（未采用） | — | Abrahallen（Rosenborg 14 场） | — | Abrahallen（OSM 唯一命中为 Hommelvik/Malvik 体育中心，该命中与 FBref 所指是否为同一设施未核实；坐标仅作竞争候选注记） |

归一化规则：大小写、Stadion 后缀、赞助商前缀（Sparebanken、SR-Bank、Lyse、Extra、Consto、Jotun、Romssa）不改变场地身份；判定前先转写 ø→o、æ→ae、å→a（否则 Sør、Mjøndalen 等会误判为不同场地——本轮合并脚本初版即因此报错，已修正）。

## 6. 坐标覆盖

- 确认场地 18/18 有坐标（Nominatim 实字节 + SHA-256，见 venue_coordinate_table.json）。
- 竞争候选 Abrahallen 1/1 有坐标（同上，但身份未核实，见 §5 末行）。
- 冲突行（Ranheim–Brann）行级坐标置 null（两竞争场地坐标均在坐标表中：EXTRA Arena / Aker Stadion，不单方面指派）。
- 坐标一律是场馆级：同一场地所有场次共用同一坐标，不写成“本场确认的坐标”。

## 7. 合规与方法注记

- 未购买、未登录、未使用任何密钥/凭证、未动用 API-Football 付费额度。FBref 与 NFF 均为公开页面文本层读取；Nominatim 为公开地理编码接口（每请求间隔 1.2 秒）。
- 未返回任何比分、赛果、赔率、积分榜、预测、奇门/干支/门/星/神/五行解读、Snapshot、Outcome、Review、Gold 字段；FBref/NFF 证据文件只含日期、主客队、场馆列。
- 基线文件只读，未改动；联结字段（record_key、season、local_date、主客队原文、kickoff_local、round、round_label、provider_fixture_id）逐字复制，程序校验 0 偏差。
- 本工作目录 evidence/nominatim/ 内另有非本路文件（CamelCase 命名，如 Briskeby_Arena_Hamar.json、Color_Line_Stadion_Ålesund.json，时间戳与本路下载同时段）：那不是本路下载的，本路坐标证据只认小写 slug 文件 + nominatim_summary.json + abrahallen.json，未引用、未改动他人文件。
- 2018-04-11（2 场）与 2018-04-25（2 场）为改期场次，日期与基线一致，已按基线日期配对，未按原定轮次日期重排。
