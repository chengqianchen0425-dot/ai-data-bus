# NFF 官方逐场场馆证据探查 — req-20261028-001

任务性质：只做证据探查与可达性报告，不做最终裁决。
方法：仅用页面文本抓取（browser.open），未用 curl、未登录、未购买、未使用任何密钥、
未动用 API-Football 付费额度。所有文件均不含比分列、赛果、赔率、积分榜数据。

## 结论一览

- 2019 赛季：官方页面可达，含逐场场馆字段，提取 **240 / 240** 场（基线 2019 全量）。
- 2018 赛季：**blocked**，本轮只做一次轻量确认，未找到正赛官方赛季入口，
  沿用前序 retry_after=2026-11-19（未到），提取 **0** 场，未用其他源补数。
- JSONL 总行数：240（全部为 2019；2018 为 0 行，不是遗漏，是 blocked 的如实记录）。

## 1. 2019 赛季（tournamentId=164089）

### 实际打开的官方页面

| 页面 | source_url = final_url | retrieved_at | 含逐场场馆字段 |
|---|---|---|---|
| 赛季主页（含 Alle kamper 全表） | https://www.fotball.no/fotballdata/turnering/hjem/?fiksId=164089 | 2026-10-28T15:59:00+08:00 | 有 |
| 单场页（抽查 corroboration） | https://www.fotball.no/fotballdata/kamp/?fiksId=7158761 | 2026-10-28T16:00:00+08:00 | 有 |
| 场馆页（抽查城市字段） | https://www.fotball.no/fotballdata/anlegg/hjem/?fiksId=8124 | 2026-10-28T16:00:00+08:00 | 无城市字段（见下） |

### 场馆字段定位（field_locator）

- 赛季主页 `Alle kamper` 表格的 **Bane** 列（表格列依次为：轮次、日期、星期、
  时间、主队、比分列、客队、Bane、场次编号）。比分列被有意排除，未转录进任何文件。
- 单场页的对应字段为 `Kampdetaljer` 下的 `Stadion:` 一项。
- 抽查 corroboration：单场页 fiksId=7158761（场次编号 99120001124，
  2019-08-03 Odd 对 Lillestrøm）的 `Stadion: Skagerak Arena`，
  与赛季全表同一场比赛行的 Bane 值一致，证明 Bane 列即逐场官方场馆字段。

### 提取计数与覆盖

- 全表共 30 轮 × 每轮 8 场 = 240 行，轮次编号与场次编号区间
  99120001001–99120001240 连续可读；JSONL 的 240 个 record_key
  与基线文件 2019 部分的 240 个 record_key 经程序校验完全一致（无多无少）。
- 每轮 8 场、每主队 15 个主场均齐全；无缺失场次。
- 场次编号未逐行转录进 JSONL（非任务要求字段；手工转录 240 个编号易引入
  差错，不如不写；record_key + local_date + 主客队原文已可唯一重定位到全表行）。

### 逐行读取的诚实说明（非“主队主场表代替”）

- 240 行是逐行读完的（分三段页面文本读完第 1–30 轮）。
- 全表出现的 Bane 字符串恰好 16 个，各自在全部出场中始终对应同一主队，
  未出现第 17 个偏离值（即没有某场临时换场的偏离行被读到）。
- 因此 JSONL 每行的场馆值就是该场比赛自己所在表行的 Bane 值；
  “同一主队全季同一 Bane”是整表读完后观察到的性质，不是事先拿球队主场表代填。
- 如后续复核发现某行 Bane 与本文件不符，以官方全表该行原文为准，本文件应据此修正。

### NFF 原文场馆名（16 个，各 15 场，原文大小写照录）

| NFF 主队原文 | NFF Bane 原文 |
|---|---|
| Bodø/Glimt | Aspmyra stadion |
| Brann | Brann stadion |
| Haugesund | Haugesund Sparebank Arena |
| Kristiansund | Nordmøre stadion |
| Lillestrøm | Åråsen stadion |
| Mjøndalen | Consto Arena |
| Molde | Aker stadion |
| Odd | Skagerak Arena |
| Ranheim TF | EXTRA Arena |
| Rosenborg | Lerkendal stadion |
| Sarpsborg 08 | Sarpsborg st KG |
| Stabæk | Gamle Nadderud stadion (inngang fra Haukeveien v/tennisbanen) |
| Strømsgodset | Marienlyst stadion |
| Tromsø | Romssa Arena |
| Viking | Lyse Arena |
| Vålerenga | Intility Arena |

注意：`Sarpsborg st KG` 与 Stabæk 的括号长串均按官方原文照录，未改写为通用名。
基线场馆名与 NFF 原文在 210 / 240 行上字符串不同（多为冠名/时代命名/大小写差异，
如 Ranheim：基线 Ranheim Arena vs NFF EXTRA Arena；Tromsø：基线 Alfheim vs NFF
Romssa Arena；Viking：基线 SR-Bank Arena vs NFF Lyse Arena；Mjøndalen：基线
Isachsen Stadion vs NFF Consto Arena），本文件一律以 NFF 原文为准，未用基线名覆盖。

### nff_venue_city 为何全为 null

- 赛季全表只有 Bane 列，没有城市列；单场页只有 Stadion 一项，没有城市；
  场馆页（以 Skagerak Arena 页抽查）的文本层同样没有城市/地址字段。
- 因此城市一律记 null，不用基线城市或其他源补填（那不是 NFF 逐场证据）。

## 2. 2018 赛季（轻量确认一次，blocked）

- 本轮尝试（仅一次，未反复撞墙）：网页搜索
  `fotball.no Eliteserien 2018 turnering hjem fiksId`（2026-10-28）。
- 结果：fotball.no 命中中没有 2018 Eliteserien 正赛赛季页——
  仅有 `Kvalifisering Eliteserien 2018`（tournamentId=163384，升降级附加赛，
  不是正赛，不可误作 2018 赛季入口）与 `G19 Elite 2018`（tournamentId=161695，
  青年组），其余为非 NFF 来源（按任务要求一律忽略，未用于补数）。
- 未猜测 tournamentId、未重复前序已做过的 fiksId 邻域试探
  （前序 req-20261018-001 已做站内搜索、sitemap、API 试探、JS 包分析、
  搜索引擎检索、邻域试探六路，均未发现；本轮不再重撞同一堵墙）。
- 结论：2018 沿用 blocked，retry_after=2026-11-19（未到）；JSONL 中 2018 为 0 行。
  到期后可重试搜索引擎发现，或从 NFF 年度回顾编辑页获得带 fotballdata 链接的入口。

## 3. 尝试过的 URL 清单与失败/成功表现

| URL / 动作 | 表现 |
|---|---|
| https://www.fotball.no/fotballdata/turnering/hjem/?fiksId=164089 | 成功：2019 赛季页全文可读，Alle kamper 全表 240 行含 Bane 列 |
| https://www.fotball.no/fotballdata/kamp/?fiksId=7158761 | 成功：单场页 Kampdetaljer 含 Stadion 字段，与全表行一致 |
| https://www.fotball.no/fotballdata/anlegg/hjem/?fiksId=8124 | 成功打开，但文本层无城市字段，故城市记 null |
| 网页搜索 fotball.no Eliteserien 2018 turnering | 未找到 2018 正赛赛季页；仅附加赛（163384）与青年组（161695）命中 |

## 4. 交付文件

- `nff_venue_2018_2019.jsonl`：240 行，全部为 2019；
  每行含 record_key、local_date、nff_home_team、nff_away_team、nff_venue_name、
  nff_venue_city（null）、source_url、final_url、retrieved_at、field_locator。
- `nff_venue_notes.md`：本文件。
- `evidence/nff_2019_venue_table.csv`：与 JSONL 同内容的赛程/场馆证据表
  （仅 record_key、local_date、主客队原文、场馆名、source_url 五类列，无比分列）。

## 5. 最大障碍

- 2019 无障碍：官方全表文本层可直接读完，逐场场馆字段完整。
- 真正的障碍只在 2018：正赛 tournamentId 至今无法通过合规手段发现，
  且 retry_after=2026-11-19 未到，本轮按规则不得硬试；2018 的 240 场
  只能等到期后重发现，或由其他官方路径（非 NFF 逐场证据不在本任务范围）解决。
