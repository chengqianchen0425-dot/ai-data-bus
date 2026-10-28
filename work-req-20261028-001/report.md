# req-20261028-001 报告：Eliteserien 2018–2025 实际比赛日场馆与坐标溯源缺口审计

## 结论先行

- **1,920 / 1,920 行齐全，0 缺失。** 状态：confirmed 1,915、neutral 4、moved 0、conflict 1、unavailable 0、blocked（行级）0。
- **坐标 1,919 / 1,920 行**，唯一空坐标行就是那 1 行 conflict（两竞争场馆的坐标都在分路坐标表里，不单方面指派）。
- **必须分清 confirmed 的两档**：720 行有 NFF 官方背书（2019 赛季表 Bane 列、2024–2025 官方赛历 Excel），1,200 行只是双源（基线逐场 venue + FBref 逐场 Venue 列）一致，未经官方确认。两档在每行的 confirmation_tier 里写明了，绝不能把后者当成官方确认来用。
- **中立场只有 4 场，全在 2024**：KFUM Oslo 两场在 Intility Arena、Kristiansund BK 两场在 Aker stadion（Molde）。其余 1,915 场确认行全部是主队常规主场（含赞助更名后的当期名），没有一场被确认为异地（moved = 0）。
- **唯一 conflict**：2018-04-25 Ranheim vs Brann——基线与 Ranheim 赛季页说 EXTRA Arena，FBref 说 Molde 的 Aker Stadion，两边观众与裁判相同、无法区分，不记 moved，等 NFF 官方裁决。

## 1. 按赛季计数

| 赛季 | expected | discovered | confirmed | neutral | moved | conflict | unavailable | blocked | missing | 带坐标行 |
|---|---|---|---|---|---|---|---|---|---|---|
| 2018 | 240 | 240 | 239 | 0 | 0 | 1 | 0 | 0 | 0 | 239 |
| 2019 | 240 | 240 | 240 | 0 | 0 | 0 | 0 | 0 | 0 | 240 |
| 2020 | 240 | 240 | 240 | 0 | 0 | 0 | 0 | 0 | 0 | 240 |
| 2021 | 240 | 240 | 240 | 0 | 0 | 0 | 0 | 0 | 0 | 240 |
| 2022 | 240 | 240 | 240 | 0 | 0 | 0 | 0 | 0 | 0 | 240 |
| 2023 | 240 | 240 | 240 | 0 | 0 | 0 | 0 | 0 | 0 | 240 |
| 2024 | 240 | 240 | 236 | 4 | 0 | 0 | 0 | 0 | 0 | 240 |
| 2025 | 240 | 240 | 240 | 0 | 0 | 0 | 0 | 0 | 0 | 240 |
| 合计 | 1920 | 1920 | 1915 | 4 | 0 | 1 | 0 | 0 | 0 | 1919 |

身份基线校验：合并行与 req-20261017-002 台账的 record_key 集合 0 缺失、0 多余；local_date、kickoff_local、轮次、provider_fixture_id、主客队原文拼写 0 处差异。请求里提到的本地 Windows 证据副本（D 盘路径）本机够不着，用的是 repo 里同一份已接受台账。

## 2. 证据层级（confirmed ≠ 同一含金量）

- **官方档（720 行）**：2019——NFF tournamentId=164089 赛季表 `Alle kamper` 的 Bane 列，240/240 逐场提取，单场页抽查 `Stadion:` 一致；2024–2025——NFF 官方赛历 Excel（tournamentId 2024=192924、2025=199603，均核验赛季页标题），按赛季/轮次/主客队/日期与基线 480/480 零缺口匹配，站点层面 480/480 一致。
- **双源档（1,200 行，2018/2020/2021/2022/2023）**：基线 api-football 逐场 venue + FBref 逐场 Venue 列在同一物理场馆上一致（经名称归一化与更名证据裁决）。FBref 表是完整读完的（每季 240 场联赛行，附加赛行已排除），“队季恒定”是读完后的观察结论，不是拿主场表代填。2020 空场/易地传闻未作任何推断。
- **裁决档（2018 Rosenborg 14 个主场）**：FBref 联赛表写 Abrahallen，但 FBref 自身欧战日志写 Lerkendal、Rosenborg 赛季页逐场写 Lerkendal Stadion、Abrahallen 行的观众数是 Lerkendal 量级（最高约 21,201，室内训练馆不可能容纳）。裁决为 Lerkendal，Abrahallen 仍保留为行内竞争候选。这是有理由的裁决，不是官方确认。
- **城市口径弱项**：FBref 与 NFF 逐场表均无城市列，verified 城市沿用基线值（并用 Nominatim 地名 locality 交叉核对），城市的双源性弱于场馆名，已在行与分路 notes 里明示。

## 3. 名称与更名（原文拼写全部保留在行内）

同一物理场馆的归一化只用于判定身份，不改写原文：Alfheim = Romssa Arena（2023-03-29 更名）；Isachsen = Consto Arena；Ranheim Arena = EXTRA Arena；SR-Bank Arena = Viking Stadion = Lyse Arena（Lyse 自 2025 起）；Sør Arena = Sparebanken Sør Arena = Sparebanken Norge Arena；Kristiansund Stadion = Nordmøre stadion；Komplett.no Arena（至 2019-11）→ Release Arena（2021-05-05）→ Jotun Arena（2023-09-05）；Haugesund Stadion → Haugesund Sparebank Arena（2021-05，基线内有干净切分：Stadion 至 2021-07-18、Sparebank Arena 自 2021-07-28，公告日期未核实）；Sarpsborg st KG = Sarpsborg Stadion 人造草坪场地（不是另一球场，不记 moved）。FBref 多季使用过期赞助旧名，verified 名取比赛日当期名。
合并文件里 verified（场馆名，城市）字符串 distinct 计 49 个——这是拼写变体数（大小写、æ/ø/å 转写、locality 与市镇两种城市写法、赞助更名），不是 49 座物理球场；分路各报每两季 18 座物理站点，8 季主客队共 24 支俱乐部，另加 Intility Arena 与 Aker stadion 两座中立场。

## 4. 坐标（场馆级，不是场次级确认）

- 来源：OpenStreetMap Nominatim 搜索 JSON（场馆级地理编码，同一球场各场共用）；多数场馆有实字节 + 重算 SHA-256。
- **基线坐标异常（Sandefjord / Jotun Arena，三路独立一致）**：基线（59.17544, 10.21542）与 Nominatim 场馆点（59.1371935, 10.1795249）相距 4.72 km；Nominatim 点与公开球场地址（Nygårdsveien 82–86）及公开坐标（59.13725, 10.17969）一致，基线点反查为 Søndre Kullerød 民宅地址。合并行采用 Nominatim 点，基线值保留在行内供比对。其余场馆基线与 Nominatim 差均在 0.6 km 内（Brann 341 m、Sarpsborg 595 m、Nadderud 233 m），属街道级取点差异，记精度注记、不算身份冲突。
- 例外：D 路 3 座场馆（Bryne、Fredrikstad、KFUM）因 D 路自采 Nominatim 请求被运行时权限门拦截（未绕过），坐标来自地图工具结果、无可下载字节，source_sha256 置 null 并注明原因；数值本身不受影响，如需字节级 provenance 须批权限后重采。FBref 文本层证据同样无字节，SHA 置 null、不编造。

## 5. 未解决队列（unresolved_queue.json，10 项）

- UQ-01（conflict）：2018-04-25 Ranheim vs Brann，待 NFF 官方裁决，在此之前不记 moved。
- UQ-02（access_blocked）：2018/2020/2021 的 NFF tournamentId 不可发现，retry_after=2026-11-19，到期前不重撞。
- UQ-03（access_blocked）：2022 tournamentId 两次搜索未发现，未猜测。
- UQ-04（access_blocked）：2023 tournamentId=186850 已知，但旧 fotballdata URL 已死（301 后落到 404 SPA 壳页，已存档 61,617 字节壳页为证），须走实时浏览器探新站结构。
- UQ-05（ambiguous）：Sandefjord 基线坐标 4.72 km 偏差的来源（哪次地理编码、什么输入串）未重建；下游用 Nominatim 点。
- UQ-06（ambiguous）：Bryne/Fredrikstad/KFUM 三馆坐标无字节 provenance（见上）。
- UQ-07（ambiguous）：FBref 文本层证据无字节 SHA。
- UQ-08（pending_work）：1,200 行双源档升官方档，需 UQ-02/03/04 的 NFF 源到位后重验并改 confirmation_tier，不得提前改标。
- UQ-09/UQ-10（permanent_rule）：奇门/真太阳时/预测字段禁出（本地管线自算）；俱乐部默认主场禁作单场证据（本交付无一行以此为唯一证据）。

## 6. 交付文件清单（随回执 commit）

fixture_venue_rows.jsonl（1,920 行，SHA-256 见 audit.json）、audit.json、unresolved_queue.json、report.md（本文件）、分路文件 venue_audit_2018_2019.jsonl / venue_audit_2020_2021.jsonl / venue_audit_2022_2023.jsonl / venue_audit_2024_2025.jsonl 及各路 notes、venue_coordinate_table.json、geo_evidence/ 与 evidence/nominatim/（Nominatim 原字节）。
合规：未购买、未登录、未使用任何凭证、未动用 API-Football 付费额度；未写本地奇门项目文件；禁字段扫描（比分/赔率/积分榜/奇门/预测/Snapshot/Outcome/Review/Gold 类字段名）0 命中；真太阳时未算。
