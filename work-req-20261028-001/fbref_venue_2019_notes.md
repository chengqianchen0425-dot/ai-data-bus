# FBref 2019 Eliteserien 逐场场馆证据提取 — 说明（req-20261028-001，证据提取，不做最终裁决）

## 来源与抓取

- 源页 URL（预期 URL 一次打开成功，无需站内搜索核实替代 URL）：
  `https://fbref.com/en/comps/28/2019/schedule/2019-Eliteserien-Scores-and-Fixtures`
- 抓取方式：页面文本抓取（browser.open），未登录、未购买、未使用任何密钥，未动用 API-Football 额度。
- 抓取/成表时间：`2026-10-28T16:00:49+08:00`（Asia/Shanghai；该值即 `fbref_venue_2019.jsonl` 各行 `retrieved_at`）。
- 提取列：仅赛程表 Date、Home、Away、Venue 四列。其他列一律未写入任何交付文件。
- 证据文件：`evidence/fbref_venue_2019_evidence.md`（240 行 Venue 表，与 jsonl 同源）。
- 基线文件只读未改动：`baseline_2018_2019.jsonl`（season=2019 取 240 行）。

## 计数（240 行齐全）

| baseline_match | 计数 |
|---|---|
| agree | 165 |
| differ | 75 |
| no_fbref_value | 0 |
| page_unreachable | 0 |
| 合计 | 240 |

- 配对不上的场次：无（0 场）。240 场全部按 (local_date + 主队 + 客队) 配上 FBref 首表行。
- 截断场馆：无（0 场）。全部 240 个 FBref 场馆名完整，无以 `...` 结尾者。
- FBref 城市：全部 240 行 `fbref_venue_city = null`，因该赛程表无城市列，页内无城市信息可取，未用基线城市反填。

## agree / differ 口径（本文件只做字符串比对，不裁决）

- agree = FBref 场馆名字符串与基线场馆名字符串完全相等。
- differ = 名字符串不同。本批 differ 全部是“主队 15 个主场全数同向不同”，无单场例外、无中立场异常：
  - 后缀型不同（3 组 × 15 场 = 45 场）：基线 `Alfheim` → FBref `Alfheim Stadion`；基线 `Nadderud` → FBref `Nadderud Stadion`；基线 `Åråsen` → FBref `Åråsen Stadion`。
  - 全名不同（2 组 × 15 场 = 30 场）：基线 `Isachsen Stadion` → FBref `Consto Arena`；基线 `Ranheim Arena` → FBref `EXTRA Arena`。
- differ 仅表示“两源场馆名字符串不同”，是否同一物理场馆、应以哪源为准，由主代理最终裁决，本任务不下结论。
- 其余 11 个基线场馆名与 FBref 逐场值完全一致（165 场）。

## 队名拼写归一化（配对用，报告中双方原文均保留）

配对前做归一化：去变音（ø→o、å→a、æ→ae）、去空格与 `/`、小写化；另加三条显式别名：

| 基线原文 | FBref 原文 |
|---|---|
| ODD Ballklubb | Odd |
| Kristiansund BK | Kristiansund |
| Sarpsborg 08 FF | Sarpsborg 08 |

其余队名经去变音后一一对应：Bodo/Glimt→Bodø/Glimt、Valerenga→Vålerenga、Lillestrom→Lillestrøm、Mjondalen→Mjøndalen、Stromsgodset→Strømsgodset、Tromso→Tromsø、Stabaek→Stabæk；Brann、Haugesund、Molde、Ranheim、Rosenborg、Viking 拼写相同。
jsonl 每行同时保留 `home_team_baseline / away_team_baseline` 与 `fbref_home_team / fbref_away_team`，供复核。

## 页结构说明与排除项

- 同一页含两张赛程表：首表与第二表逐场 Venue 值经抽查全程一致；jsonl 的 `field_locator` 以首表为准并注明第二表重复。
- 2019-12 的两场升降级附加赛行不在基线 240 行内，已排除，未计入。
- 部分轮次场次按实际日期分散在表中（如个别轮次场次落在其他月份日期），配对以 FBref 显示日期 + 主客队为准，不以轮次号配对；240 场日期与基线 `local_date` 全部吻合，无日期冲突。
- 本提取是 FBref 逐场 Venue 列本身，不是球队主场表推导；未把主队默认主场当作本场证据。

## 交付文件

- `fbref_venue_2019.jsonl`：240 行，每行一个 `record_key`，含 record_key、local_date、双方队名（基线原文与 FBref 原文）、baseline_venue_name、fbref_venue_name、fbref_venue_city、baseline_match、match_note、retrieved_at、field_locator、source_url、final_url。
- `evidence/fbref_venue_2019_evidence.md`：Venue-only 证据表（Date / Home / Away / Venue）。
- 未写 `repo/responses/`，那是主代理的事。
