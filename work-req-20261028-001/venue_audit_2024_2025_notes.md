# D 路审计说明：Eliteserien 2024–2025 实际比赛日场馆审计（480 场）

## 1. 计数（按赛季）

| 赛季 | expected | discovered | confirmed | neutral | moved | conflict | unavailable | blocked | missing |
|---|---|---|---|---|---|---|---|---|---|
| 2024 | 240 | 240 | 236 | 4 | 0 | 0 | 0 | 0 | 0 |
| 2025 | 240 | 240 | 240 | 0 | 0 | 0 | 0 | 0 | 0 |
| 合计 | 480 | 480 | 476 | 4 | 0 | 0 | 0 | 0 | 0 |

- expected：基线 `fixtures_2018_2025.jsonl` 中 season=2024 或 2025 的行数。
- discovered：NFF 官方赛历中按（赛季、轮次、主队、客队、日期）成功匹配到基线行的场次数，480/480，无一遗漏。
- 坐标覆盖：480/480 行有经纬度；18/18 个场馆站点有坐标（见 §5）。

## 2. 状态判定规则（先于计数定死，事后未改）

- **confirmed**：NFF 官方 Bane 所在站点 == 基线 venue 所在站点（站点按 §4 的同址别名组归并，不按字符串相等）。
- **neutral**：核实场馆站点 ≠ 主队本赛季常规 Bane（该队该赛季 NFF Bane 的众数）且 ≠ 客队本赛季常规 Bane。
- **moved**：保留给核实场馆站点 == 客队常规 Bane 的情形（场地互换类）；本轮 0 场。
- **conflict**：保留给 NFF 与基线在站点层面不一致的情形；本轮 0 场。FBref 与 NFF/基线的不一致（见 §6）因 FBref 为非官方层级且 NFF+基线一致，不单独计为 conflict，但全部作为候选保留在行内，不静默丢弃。
- **unavailable / blocked / missing**：本轮 0 场——NFF 赛历两季均可下载且全部匹配，无需动用这两个状态。
- 俱乐部默认主场在本交付中只出现在 neutral 行的候选里，标注为“俱乐部默认主场候选，非本场确认”，从未被用作核实场馆。

## 3. Neutral 4 场（全部 2024 赛季，NFF 与基线一致，均为偏离主队常规主场）

| 场次 | 日期 | 核实场馆（NFF Bane 原文） | 主队常规 Bane | 客队常规 Bane |
|---|---|---|---|---|
| 2024 R1 KFUM Oslo vs Ham-Kam | 2024-04-02 | Intility Arena | KFUM-Arena（13 场） | Briskeby（15 场） |
| 2024 R3 KFUM Oslo vs Stromsgodset | 2024-04-16 | Intility Arena | KFUM-Arena（13 场） | Marienlyst stadion（15 场） |
| 2024 R13 Kristiansund BK vs Fredrikstad | 2024-07-08 | Aker stadion | Nordmøre stadion（13 场） | Fredrikstad stadion（15 场） |
| 2024 R17 Kristiansund BK vs Lillestrom | 2024-08-04 | Aker stadion | Nordmøre stadion（13 场） | Åråsen stadion（15 场） |

其余俱乐部每赛季均只有单一 NFF Bane（每队 15 个主场全在同一 Bane），因此不存在其他偏离常规主场的场次。

## 4. 同址别名组（字符串不同、同一站点，不算不同场馆、不算冲突）

NFF 字符串与基线字符串不同的行共 148 行，全部落在以下同址组内：

| 同址组 | NFF 写法 | 基线写法 | 涉及行数 |
|---|---|---|---|
| Fredrikstad | Fredrikstad stadion | Nye Fredrikstad Stadion（2024）／Fredrikstad Stadion（2025） | 15（仅 2024 行字符串不同） |
| Viking | Lyse Arena（两季） | SR-Bank Arena（2024）／Lyse Arena（2025） | 15（仅 2024 行） |
| Ham-Kam | Briskeby | Briskeby Arena | 30 |
| Sarpsborg | Sarpsborg st KG | Sarpsborg Stadion | 30 |
| Kristiansund | Nordmøre stadion（两季） | Nordmøre stadion（2024）／Kristiansund Stadion（2025） | 15（仅 2025 行） |
| Haugesund | Haugesund Sparebank Arena（两季） | Haugesund Sparebank Arena（2024）／Haugesund Stadion（2025） | 15（仅 2025 行） |
| KFUM | KFUM-Arena | KFUM Arena | 28（仅连字符与空格之差） |

说明：Sarpsborg st KG（st KG = stadion kunstgress）是 NFF 对 Sarpsborg 全部 30 个主场的标准 Bane 写法，不是单场改动；其坐标按 Sarpsborg Stadion 综合体一级给出（见 §5）。城市拼写变体：同一 Aspmyra 站点基线城市 2024 年写 Bodo、2025 年写 Bodø；同一 Romssa 站点 2024 年写 Tromso、2025 年写 Tromsø；核实城市栏逐场照抄基线写法，不做统一改写。

## 5. 坐标（场馆级，不是场次级）

18 个站点全部有 WGS84 经纬度；每行坐标 provenance 均注明 coordinate_level=venue_site，即同一站点所有场次共用一组坐标，绝不写成“本场确认的坐标”。

| 站点 | 经纬度 | 坐标来源与匹配质量 |
|---|---|---|
| Aker Stadion, Molde | 62.7334015, 7.1480721 | Nominatim 文件，type=stadium |
| Aspmyra stadion, Bodø | 67.2766478, 14.3844344 | Nominatim 文件，type=stadium |
| Brann Stadion, Bergen | 60.3668333, 5.3574265 | Nominatim 文件，type=stadium |
| Briskeby, Hamar | 60.7955818, 11.0922051 | Nominatim 文件，type=stadium（Briskeby stadion） |
| Bryne stadion, Bryne | 58.72948, 5.64908 | map.geocode，FULL_ADDRESS relevance 100（POI 标注为 Trallfavegen 1 的 Stadion Bowling，街道地址即球场地址） |
| Fredrikstad stadion, Fredrikstad | 59.21333, 10.92816 | map.geocode，FULL_ADDRESS relevance 100（Fredrikstad Stadion, K. G. Meldahls vei 9） |
| Haugesund stadion, Haugesund | 59.4130886, 5.2795151 | Nominatim 文件，type=pitch（赞助名 Haugesund Sparebank Arena 查询返回空，改用同一综合体的 Haugesund stadion） |
| Intility Arena, Oslo | 59.9179048, 10.8066324 | Nominatim 文件，type=stadium |
| Jotun Arena, Sandefjord | 59.1371935, 10.1795249 | Nominatim 文件，type=pitch（见 Jotun 专项核查） |
| KFUM Arena, Oslo | 59.88863, 10.78208 | map.geocode，FULL_ADDRESS relevance 100（Kfum Arena, Ekebergveien 109） |
| Lerkendal Stadion, Trondheim | 63.4123264, 10.4044664 | Nominatim 文件，type=stadium |
| Lyse Arena, Stavanger | 58.9145955, 5.7309977 | Nominatim 文件，type=stadium（旧赞助名 SR-Bank Arena 查询返回空，改用现名 Lyse Arena） |
| Marienlyst stadion, Drammen | 59.7343801, 10.201551 | Nominatim 文件，type=stadium |
| Nordmøre stadion, Kristiansund | 63.1249251, 7.7182754 | Nominatim 文件，type=stadium |
| Romssa Arena, Tromsø | 69.6489185, 18.9343489 | Nominatim 文件，type=stadium |
| Sarpsborg Stadion 综合体, Sarpsborg | 59.2862886, 11.0977153 | Nominatim 文件，type=pitch（NFF Bane 的 KG 场地即该综合体内场地，无单独的场地级坐标） |
| Skagerak Arena, Skien | 59.211586, 9.5899848 | Nominatim 文件，type=sports（显示地址即 Skagerak Arena） |
| Åråsen Stadion, Kjeller | 59.9627403, 11.063566 | Nominatim 文件，type=pitch |

- 与基线坐标的距离核查：17 个站点与基线坐标距离在 5 m–595 m 内；唯一例外是 Jotun Arena（见下）。
- **Jotun 专项核查**：本交付坐标（59.1371935, 10.1795249）与基线坐标（59.17544, 10.21542）相距 4.7 km。反查确认：本交付点落在 Nygårdsveien, 3221 Sandefjord，与公开的 Jotun Arena 地址（Nygårdsveien 82–86, 3221 Sandefjord）及公开坐标（59.13725, 10.17969，相距约 20 m）一致；基线点反查为 Søndre Kullerød 4B, 3241 Sandefjord，不是球场地址。因此本交付采用 Nominatim 点，基线点未被沿用，特此记录（基线坐标仅作核查参照，不作为本行 provenance）。
- **Nominatim 权限门说明**：本路自己发起的 Nominatim 请求被运行时权限门拦截（待用户批准与 openstreetmap.org 的信息共享），本路未绕过该门：已终止该请求进程；15 个站点的坐标改用本请求共享工作目录中已有的 Nominatim JSON 文件（由并行路捕获），本路逐文件重读字节、重选球场类结果、重算 SHA-256，provenance 中的 retrieved_at 为文件捕获时间（mtime），不是本路的请求时间；其余 3 个站点（Bryne、Fredrikstad、KFUM）改用 map.geocode 工具结果（无可下载字节，source_sha256 为 null 并注明原因，未编造）。如需本路自采的 Nominatim 字节，需用户先批准上述共享权限后重跑地理编码一步。

## 6. 证据源清单

1. **NFF fotball.no 官方赛历（第一优先级）**：Excel 下载
   - 2024：`https://www.fotball.no/footballapi/Calendar/DownloadTournamentExcelCalendar?tournamentId=192924&heading=Eliteserien`，17,159 字节，SHA-256 `a7d381958bb42ca41dbf1f9f2a41ed2fa8a76d8d9cd9813c70c83d4c6dcc9034`，下载时间 2026-10-28 15:59:10+08:00；赛季页标题核验为 Eliteserien 2024，tournamentId 192924 属实。
   - 2025：`https://www.fotball.no/footballapi/Calendar/DownloadTournamentExcelCalendar?tournamentId=199603&heading=Eliteserien`，17,236 字节，SHA-256 `03912ab721df60be95709ba9fccac95a923ae80c318341908a3a216144`，下载时间 2026-10-28 15:59:11+08:00；赛季页标题核验为 Eliteserien 2025，tournamentId 199603 属实。
   - 每行定位：sheet1 的 Runde / Dato / Hjemmelag / Bortelag / Bane / Kampnummer；Bane 即核实场馆名原文。源文件本身不在本交付目录内存放（其第六列超出本交付范围，已在解析时丢弃、从未存储或返回）；本交付目录内只存无该列的场馆摘录 `evidence/nff_venue_excerpt.json`（SHA-256 `ccaea9610a93f155c35651645cce1149479a876fa1e15c15aa1c5be278e25a57`），凭上述 URL 与 SHA 可重新下载核验。
2. **基线文件（第二证据）**：`~/workspace/ai-inbox/repo/work-req-20261017-002/fixtures_2018_2025.jsonl` 的 method_context.venue_name / venue_city；联结字段（record_key、season、local_date、home_team、away_team、kickoff_local、round、round_label、provider_fixture_id）全部逐字复制，未修改、未重新推导；基线赛季级 provenance SHA：2024 `bab76dff47e93d30c987d81e42d9f3727adbeb8e0cabaf638f04335d250c08af`，2025 `b104cfb7e6a02d7f93976d6961625d4e3ec427bb0fa04db7dd16e0232db9831f`。
3. **FBref 2024 赛程表 Venue 列（非官方，仅抽查 5 行）**：文本层读取 2026-10-28（页面爬取时间戳 2026-09-05 16:23 UTC），无字节故 source_sha256 为 null。
   - 2024 R3 KFUM Oslo vs Stromsgodset：FBref Intility Arena，与 NFF+基线一致。
   - 2024 R13 Kristiansund BK vs Fredrikstad：FBref Aker Stadion，与 NFF+基线一致。
   - 2024 R1 KFUM Oslo vs Ham-Kam：FBref KFUM Arena，与 NFF+基线（Intility Arena）不一致；作为竞争候选保留在该行内，NFF 官方优先级 + 基线佐证占优，该行仍计 neutral，不计 conflict（见 §2 规则）。
   - 2024 R7 Sandefjord vs Sarpsborg 08 FF：FBref Jotun Krøllgras；NFF 为 Jotun Arena——同一综合体内场地级写法，不算不同场馆。
   - 2024 R9 Stromsgodset vs Haugesund：FBref Marienlyst Kunstgress；NFF 为 Marienlyst stadion——同一综合体内场地级写法，不算不同场馆。
   - FBref 2025 赛程表未逐行抽查（NFF+基线已对 2025 全部 240 场一致，无需以非官方源复核）。
4. **坐标源**：见 §5（Nominatim 文件 15 站点 + map.geocode 3 站点）。

## 7. 未覆盖与冲突清单

- 未覆盖场馆：无（480/480 均有 NFF Bane 与基线场馆）。
- 未覆盖坐标：无（18/18 站点）。
- status=conflict：0 场。
- 保留但未采纳为核实值的竞争候选（行内可见，不静默丢弃）：
  - 2024 R1 KFUM Oslo vs Ham-Kam：FBref KFUM Arena（对 NFF+基线 Intility Arena）。
  - 2024 R7 Sandefjord vs Sarpsborg 08 FF：FBref Jotun Krøllgras（对 NFF Jotun Arena，同综合体）。
  - 2024 R9 Stromsgodset vs Haugesund：FBref Marienlyst Kunstgress（对 NFF Marienlyst stadion，同综合体）。
  - 全部 neutral 行的俱乐部常规主场候选（见 §3）。
  - 全部别名组内的基线写法（见 §4）。
- 待主代理决断的事项：
  - Nominatim 自采字节：需用户批准 openstreetmap.org 信息共享权限后，方可重跑本路地理编码以替换 §5 中 15 个站点的“复用文件”provenance（数值本身不受影响，仅 provenance 来源改变）；3 个 map.geocode 站点亦可同步改用 Nominatim。
  - FBref 2025 赛程表未抽查：如需与 2024 同等的抽查覆盖，可另派一轮只读抽查（本轮未做的原因见 §6 第 3 点）。

## 8. 合规声明

- 只输出场馆相关字段 + 联结字段；未返回 2026 赛季、赔率、比分、赛果、赛后状态、最终积分榜、赛前积分榜、任何奇门类解读、预测方向、概率，以及任务禁单所列的其余禁字段；未计算真太阳时；未写任何本地奇门项目文件。
- 未购买、未登录、未使用任何密钥/凭证、未动用 API-Football 付费额度；NFF 与 FBref 均为公开页面/文件，Nominatim 文件为共享工作目录已有捕获，map.geocode 为免密钥工具调用。
- 匹配方法：NFF 队名经以下映射归一后按（赛季、轮次、主队、客队、日期）匹配基线：Bodø/Glimt→Bodo/Glimt、Lillestrøm→Lillestrom、Strømsgodset→Stromsgodset、Tromsø→Tromso、Vålerenga→Valerenga、Sandefjord Fotball→Sandefjord、KFUM→KFUM Oslo、Kristiansund→Kristiansund BK、Odd→ODD Ballklubb、Sarpsborg 08→Sarpsborg 08 FF、HamKam→Ham-Kam；其余队名原文一致。匹配结果 480/480，无未匹配 NFF 行、无未匹配基线行。
- 行级校验：联结字段与基线逐字比对通过；record_key 集合与基线 480 行集合完全一致；禁字段/禁词扫描通过。
