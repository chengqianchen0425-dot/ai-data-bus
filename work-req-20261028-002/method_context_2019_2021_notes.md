# req-20261028-002 B 路说明（Veikkausliiga 2019–2021 交叉核对 + 缺口填补）

> 交付：`method_context_2019_2021.jsonl`（456 行，SHA-256 `6b953bcfa88f75240b7f1465703205b57603c78cd3819de6d8185fe353b54ffa`）
> 本文件只写赛前事实：无比分、无赛果、无赛后状态、无积分榜、无预测、无盘口数据。
> `venue_status="confirmed"` 在本交付中的含义：FBref 场次级 Venue 列与 -004 赛季主场映射在别名归一化后一致（或为同城换场，见下），
> 属于二级来源的场次级确认，**不是**官方（联赛/俱乐部）确认；`venue_official_confirmation` 因此在全部 456 行均为 `false`，不得把 "confirmed" 误读为官方确认。

## 1. 按赛季计数

| 赛季 | expected | discovered | complete | partial | conflict | unavailable（字段级） | blocked | missing（填补后） |
|---|---|---|---|---|---|---|---|---|
| 2019 | 162 | 162 | 162 | 0 | 0 | meeting_number 162；competition_entry_year 162 | 0 | 0 |
| 2020 | 132 | 132 | 128 | 0 | 4 | meeting_number 132；competition_entry_year 132 | 0 | 0 |
| 2021 | 162 | 162 | 161 | 0 | 1 | meeting_number 162；competition_entry_year 162 | 0 | 轮次 1（见 §4） |
| 合计 | 456 | 456 | 451 | 0 | 5 | meeting_number 456；competition_entry_year 456 | 0 | 轮次 1 |

- complete 定义：date + kickoff + venue + official_round 四项齐全（meeting_number 按规则全空，不计入完整性）。
- conflict 定义：仅指个体异常（日期误标、非系统性时间分歧、轮次标签冲突），见 §6；2019/2021 两季系统性的 +2h 开球时间重标
  是经 100% 非空行验证的统一源语义纠正，逐行记在 `kickoff_change`，不单独列为 conflict（否则 283 行都会是 conflict，计数失去意义）。

## 2. -004 交叉结果：沿用 / 覆盖 / 新增

- 沿用：456 行全部沿用 -004 `fixture_key`（含 2 行日期纠正行，键保留原 -004 日期 token 以保联结，纠正值见 `date_004_old`）；新增 0 行，删除 0 行。
- 覆盖（字段级，-004 非空旧值被替换）：
  - 开球时间替换 283 行：2019 年 132 行、2021 年 147 行（系统性 +2h，见 §3）、2020 年 4 行（个体异常，见 §6）。
  - 日期纠正 2 行（2020 年，见 §6）；场馆实际地面更换 25 行（8 行 moved + 17 行同城换场，见 §5）。
  - 至少含 1 项实质更换的行：293 行（2019：132；2020：14；2021：147）。
- 填补（-004 为 null 的字段）：
  - 开球时间填补 116 行（2019：30；2020：71；2021：15）；开球时间与 -004 一致 57 行（全部在 2020 年）。
  - 日期填补 4 行（2020 年 4 行日期缺失行，见 §6）。
  - 轮次填补 136 行（2021 年 131 行 + 2020 年 5 行，见 §4）；轮次沿用 319 行（2019：162；2020：127；2021 系列 30）。
- 场馆别名/大小写归一化 140 行（同地面不同名，如 Bolt Arena = Telia 5G -areena、Väre Areena = Savon Sanomat Areena、
  Raatin Stadion = Raatti Stadion、Ratinan stadion = Tampere Stadium，及 OmaSp/OmaSP 等大小写差异）；场馆名与 -004 逐字一致 291 行。

## 3. 开球时间：-004 在 2019/2021 年是英国时钟值误标为赫尔辛基时间；2020 年无此系统偏差

- 2019 年：132 个非空 -004 时间全部恰为 FBref 本地时间 −2h，30 个空值由 FBref 填补，零例外。
- 2021 年：147 个非空 -004 时间全部恰为 FBref 本地时间 −2h，15 个空值由 FBref 填补，零例外。
- 机制与 C 路 2022 年结论一致：-004 的源链（WorldFootball）携带英国时钟时间却误标 Europe/Helsinki
  （BST=UTC+1 vs EEST=UTC+3，差 2 小时）；Soccerway feed epoch 换算验证（2021 年 10 月 5 场抽查）与 FBref 一致。
- 2020 年不同：61 个非空 -004 时间中 57 个与 FBref 完全一致，无系统 +2h 偏移；71 个空值由 FBref 填补；
  仅 4 行与 -004 分歧（2 行日期纠正附带时间纠正 + 2 行纯时间分歧，见 §6）。因此 2020 年**没有**套用 +2h 规则，逐行采用 FBref 时间。
- UTC 由 `zoneinfo` 从本地时间 + 场馆时区换算（EEST=UTC+3，EET=UTC+2；夏令时结束：2019-10-27、2020-10-25、2021-10-31 01:00 UTC；
  2021-10-31 的比赛已是 EET，如 AC Oulu–KTP 15:00 → 13:00 UTC，与 epoch 验证一致）。
- 特殊值：2019-06-29 RoPS–KPV 22:15（FBref 原值；-004 为 20:15，符合 +2h 规律，非独立异常，已在 `kickoff_note` 注明）。
- 场馆时区：除 IFK Mariehamn 主场（Wiklöf Holding Arena，Åland 专属 IANA 时区 Europe/Mariehamn；与赫尔辛基偏移相同）外全部为 Europe/Helsinki。
  本点与 C 路/venue-coords.json 的全 Europe/Helsinki  blanket 标注不同，特此说明；UTC 换算结果不受影响。
  Mariehamn 主场行数：2019 年 13 行、2020 年 11 行、2021 年 13 行。

## 4. 2021 轮次填补结果：131/132 行填补，1 行因标签冲突留空

- 填补源：FBref Wk 列。填补依据有二，缺一不可：
  1. 2020 等价性：-004 的 2020 年轮次（Soccerway 分组）与 FBref Wk 在全部 127 个非空行上完全一致（含 Jul 11–12 的 Wk11、
     Aug 18 的 Wk18、Oct 31 TPS–SJK 的 Wk18、Nov 1 Mariehamn–HJK 的 Wk21 等改期 outlier），即该轮次体系下改期比赛保留原轮次号。
  2. 2021 常规赛 Wk 分组完整性（脚本全量校验，非抽查）：22 个 Wk 分组中 21 组恰为 6 场、12 队各一次；唯 Wk14/Wk19 破缺（见下）。
- 系列轮 23–27 沿用 -004（6 场/轮：3 场冠军组 + 3 场降级组），FBref 系列 Wk 1–5 佐证（22+Wk），30 行无一不符。
- 破缺与处置（2021-09-14 Ilves Tampere vs Helsingfors IFK）：
  FBref 标 Wk14，但 Wk14 不含该场已有 6 场、12 队各一次；而 Wk19 只有 5 场，缺的恰好就是 Ilves + Helsingfors IFK 这一对。
  极可能是 FBref Wk 误标，但按任务"不推断轮次"规则不予改写：该行 `official_round=null`、`official_round_status="conflict"`、
  `fbref_week_bucket=14`，冲突证据写在 `round_non_official` 与 `notes`。该行计为 2021 年唯一 conflict 行。
- 2019 年轮次：全部沿用 -004（Soccerway 1–27）；FBref 2019 年 Wk 对常规赛为空、系列为 1–5，无增量信息。
- 2020 年轮次：127 行沿用 -004；5 行由 FBref Wk 填补（4 行日期缺失行 + HIFK–RoPS 纠正行，见 §6）。
- 全部轮次均为非官方（`official_round_is_official=null`）：官方 KIERROS 标签未获得（veikkausliiga.com 存档 HTTP 500、
  Tulospalvelu 纯 JS 应用且 API 被 Cloudflare 拦截；Transfermarkt matchday 与 GSA gameweek 均已证伪，见 §8）。

## 5. 场馆场次级确认数：456/456 行有 FBref 场次级证据；confirmed 448 行，moved 8 行

- 2021 年：162 行场馆在别名归一化后全部与 -004 映射一致（11 个不同 FBref 场馆名对应 12 队，HJK 与 HIFK 共用一馆；
  Ilves 全季主场为 Ratinan Stadion，即 -004 的 "Tampere Stadium"，同馆不同名）。无中立场/易地。
- 2019 年实际地面更换 15 行：
  - KPV 主场在 OmaSP Stadion（Seinäjoki，SJK 主场，另一城市）8 行：Apr 7（vs Ilves）、Apr 13（vs RoPS）、Apr 25（vs Mariehamn）、
    May 11（vs Lahti）、Jul 6（vs VPS）、Jul 20（vs SJK）、Jul 28（vs KuPS）、Aug 18（vs HJK）→ `venue_status="moved"`。
    其余 5 个 KPV 主场在 Kokkolan Keskuskenttä（May 20、Jun 16、Aug 31、Sep 21、Oct 19）→ confirmed。
  - Lahti 主场在 Kisapuisto（同城老球场）5 行：Apr 7、Apr 19、Apr 30、May 5、May 20 → confirmed + 换场说明
    （5 月 20 日之后 Lahti 主场均为 Lahden Stadion）。Kisapuisto 坐标不在 -004 venue-coords.json 中，
    本轮经 map.geocode 补得：Lahden Kisapuisto, Kartanonkatu, FI-15140 Lahti，60.98594, 25.64931，FULL_ADDRESS。
  - Ilves 主场在 Ratinan Stadion（同城）2 行：Apr 14（vs VPS）、Apr 26（vs Lahti）→ confirmed + 换场说明（此后为 Tammelan Stadion）。
- 2020 年实际地面更换 10 行：Ilves 主场在 Ratinan Stadion 10 行（Jul 1、Jul 17、Aug 1、Aug 15、Aug 22、Sep 13、Sep 19、Sep 27、Oct 18、Nov 4），
  唯一例外是 Aug 5 vs RoPS 在 Tammelan Stadion。-004 的 2020 年 Ilves 映射（Tammelan Stadion）因此对 10/11 个主场不成立，
  记 confirmed（场次级证实）+ 说明，不记 moved（同城换场，moved 保留给跨城借用他队主场，即 KPV→OmaSP 情形）。
- 其余 431 行场馆与 -004 映射一致（291 行逐字一致 + 140 行别名/大小写归一化）。
- 全部 19 个不同地面均有坐标（18 个来自 -004 venue-coords.json，Kisapuisto 本轮补得）；坐标精度见 `venue_coords_precision`。
- 易地原因未 sourcing：FBref 只给场馆名，不给原因；KPV 借用 OmaSP、Lahti/Ilves 同城换场的原因均未写入交付物，不得臆测。

## 6. 冲突清单（5 行，全部在 2020 年 4 行 + 2021 年 1 行）

1. `2020|2020-11-04|Helsingfors IFK|Rovaniemen PS` — 日期纠正：-004 日期 2020-11-04 → 2020-10-22（FBref 场次级行）；
   FBref 在 Nov 4 没有 HIFK–RoPS（Nov 4 六场均为他队，22 轮完整无此场），而 Oct 22 的 21 轮组含此场才完整；
   开球 18:30 → 18:00；轮次 null → 21（FBref Wk21）；场馆 Bolt Arena（FBref 名 Telia 5G -areena，同馆）confirmed。
   `fixture_key` 保留原 -004 键，`date_004_old="2020-11-04"`。2020 年纠正后日期缺失 0 行、轮次缺失 0 行。
2. `2020|2020-09-19|FC Honka|HJK Helsinki` — 日期纠正（本轮新发现，-004 之外第二处误标）：-004 日期 2020-09-19 → 2020-09-20；
   FBref 在 Sep 19 没有 Honka–HJK（Sep 19 三场为 Inter–SJK、HIFK–Mariehamn、Ilves–Haka），Sep 20 13:00 在 Tapiolan 有此场；
   开球 18:30 → 13:00；轮次 15 不变（FBref Wk15 == -004 round 15）；`date_004_old="2020-09-19"`。
3. `2020|2020-07-25|HJK Helsinki|Ilves Tampere` — 纯时间分歧：-004 17:00 → FBref 18:30；日期与轮次（5）不变；FBref 值已采用。
4. `2020|2020-08-09|Rovaniemen PS|IFK Mariehamn` — 纯时间分歧：-004 18:30 → FBref 17:00；日期与轮次（8）不变；FBref 值已采用。
5. `2021|2021-09-14|Ilves Tampere|Helsingfors IFK` — 轮次标签冲突（见 §4）：FBref Wk14 与分组完整性冲突，轮次留空 + conflict。

## 7. 2020 年 4 行日期缺失填补（-004 键保留 UNKNOWN token，填补值进 `date` 字段）

| -004 键 | 填补日期 | 开球（FBref 本地） | 场馆（FBref） | 轮次（FBref Wk） | 簇一致性 |
|---|---|---|---|---|---|
| Ilves Tampere vs Rovaniemen PS | 2020-08-05 | 18:30 | Tammelan Stadion | 7 | -004 的其余 Aug 5–6 比赛已是 7 轮 |
| Rovaniemen PS vs Ilves Tampere | 2020-07-21 | 18:30 | Rovaniemen Keskuskenttä | 4 | -004 的其余 Jul 22 比赛已是 4 轮 |
| TPS Turku vs FC Lahti | 2020-07-25 | 17:00 | Veritas Stadion | 5 | -004 的 Jul 25 HJK–Ilves 已是 5 轮 |
| TPS Turku vs Ilves Tampere | 2020-07-07 | 18:30 | Veritas Stadion | 2 | -004 的 Jul 7 KuPS–Inter 已是 2 轮 |

轮次填补的前提是 §4 的 FBref Wk 轮次体系验证；填补的轮次均标注 `filled_from_fbref_wk`，非足协签发。

## 8. 赛季格式（有源依据，非推断）

- 2019：常规赛双循环（每队互赛两次）+ 前 6 名冠军组、后 6 名挑战组；27 轮 = 22 常规赛 + 5 系列；162 场 = 132 + 30；每队 27 场。
  （英文 Wikipedia 2019 赛季页赛制文字 + FBref 系列分组标签一致。）
- 2020：22 轮 × 6 场 = 132 场，无系列轮。-004 与英文 Wikipedia 2020 赛季页章节结构一致（无系列轮）。
  注意区分：Wikipedia 提到的一项原定 5 队欧协联资格赛因故取消、名额按常规赛排名授予，那是另一项赛事，
  不是冠军/降级系列赛，不得与"无系列轮"混淆。
- 2021：常规赛 22 轮 + 系列 5 轮 = 27 轮；162 场 = 132 常规赛 + 30 系列（冠军组与降级组各 6 队单循环，各 15 场）。
  -004 系列轮 23–27（每轮 6 场：3 冠军组 + 3 降级组）与该结构一致。

## 9. 俱乐部身份

- founded_year（natal/lineage year）：16 队全部经各队英文 Wikipedia infobox wikitext（Wikipedia API，2026-10-28 下载，
  文件 `evidence/club_*.wikitext`）逐一核验：HJK 1907、HIFK 1897、IFK Mariehamn 1919、Ilves 1931、Inter Turku 1990、
  KuPS 1923、SJK 2007、VPS 1924、FC Honka 1957、FC Lahti 1996、KPV 1930、RoPS 1950、Haka 1934、TPS 1922、AC Oulu 2002、KTP 1927。
- competition_entry_year（该队首次参加 Veikkausliiga 的赛季）：全部 null + unavailable——infobox 只给 founded year，
  首秀赛季研究为待办项，不得用 founded year 替代。
- 升降级/更名/前身/合并：本轮未发现需单列的有源事实（除 RoPS 名称变体外，见下）；名字相似绝不合并。
- RoPS 名称变体：2019 年 -004 行为 "Rovaniemi PS"，2020 年为 "Rovaniemen PS"，同一俱乐部（RoPS，1950），行不合并，身份说明已标注。
- 分组：2019 冠军组 {Inter Turku, KuPS, Ilves, HJK Helsinki, FC Honka, IFK Mariehamn}，挑战组 {Helsingfors IFK, SJK Seinäjoki, FC Lahti, Rovaniemi PS, Vaasan PS, KPV Kokkola}；
  2021 冠军组 {HJK Helsinki, KuPS, SJK Seinäjoki, Inter Turku, Ilves Tampere, Helsingfors IFK}，降级组 {FC Lahti, KTP, Haka Valkeakoski, FC Honka, IFK Mariehamn, AC Oulu}；
  2020 无分组（`split_group_2020=null`，`series_or_phase=regular_season`）。
- `stadium_<YYYY>_season_mapping` 逐字沿用 -004 赛季映射（含 2019 年 "OmaSp Stadion"/"Lahden stadion" 等原始大小写与 2021 年 Ilves 的 "Tampere Stadium"）。

## 10. meeting_number：全部 456 行 null + unavailable

尝试源：官方赛程（veikkausliiga.com 存档 HTTP 500）、Tulospalvelu（纯 JS 应用，API 被 Cloudflare 拦截）、Soccerway ROUND 分组、FBref Wk 列——
均不定义 meeting_number。绝不从日期顺序、CSV 顺序、球队出现次数、比分、积分榜、盘口推断。尝试源逐行记在 `meeting_number_attempts`。

## 11. Provenance 政策

- 每个非 null 字段的 provenance 对象含 source_url、final_url、retrieved_at（带时区）、field_locator、source_name、source_sha256。
- FBref 字段：直接 curl 返回 403，值来自浏览器文本层，无可捕获字节，故 `source_sha256=null` + `sha256_note` 说明
  （"text layer only, no bytes downloaded; null per provenance rule, not a descriptor hash"），附页面 URL、爬取日期与表内位置作为 locator。
  FBref 页面：2021 年表爬取于 2026-08-27 05:07 UTC（879 行文本，第 0–413 行为全部 162 场联赛 + 2 场降级附加赛）；
  2019 年表爬取于 2026-09-05 12:13 UTC（808 行，第 0–371 行为全部 162 场联赛 + 欧联附加赛 + 降级附加赛）；
  2020 年表爬取于 2026-09-05 10:35 UTC（683 行，第 0–324 行为全部 132 场联赛 + 2 场降级附加赛）。
  各表后半部分为去 Round/Wk 列的重复表，未使用。附加赛场次不在 -004 的 456 行内，一律未新增为行。
- 2020 年 FBref URL 由 2019/2021 年 URL 的年份 token 构造，启用前以返回页标题 "2020 Veikkausliiga Scores & Fixtures" 验真，特此说明。
- -004 的 `source_sha256` 是 provenance 描述符哈希，不是源证据哈希，本交付不继承为证据；沿用轮次的 provenance 引用 -004 行自身的
  source_url/source_name/retrieved_at（2026-10-06），填补轮次的 provenance 引用 FBref。
- Wikipedia 赛季页为 curl 下载字节（SHA-256：2019 `46a2b67982b1b4f5a3f202480577c2d36af0c292887d96ee5f70b193577be767`；
  2020 `f5356c54367337009defcd184c14502c8e96f75f3f341eb6a0ef6f41d49787e4`；
  2021 `3908c26c5b8035cc4f89dbbd6ccd730e6d2714b42e420707d4aa6067d14e53f3`），仅用于赛制文字与球场表，绝不挖掘其比分矩阵。
- Schema：采用 C 路（2022–2025）53 键结构，减 `merge_source_file`（合并步骤后加），加 `date_004_old`（仅 2 行纠正行非空，其余 null）；
  合并时取键并集、缺失键填 null。C 路文件（`method_context_2022_2025.jsonl`，675 行）未动。

## 12. 未覆盖清单（open items）

1. **CSV 精确联结（待请求方）**：请求方指定的身份 CSV（Windows 路径）在本 VM 上不存在、无法读取。
   全部 456 行标 `csv_join_status="matched_to_req-20261006-004_row_csv_join_pending"`；未做任何模糊匹配；
   最终联结须请求方上传 CSV 或确认后才能闭合。
2. **官方 KIERROS 标签（待官方源）**：全部轮次均为非官方交叉源（Soccerway 分组 / FBref Wk 验证体系），
   官方标签需 veikkausliiga.com 存档、Tulospalvelu 或主代理安排的真浏览器读取。
3. **官方（联赛/俱乐部页）场馆确认（无）**：全部 456 行 `venue_official_confirmation=false`；FBref 场次级证据为二级来源。
4. **competition_entry_year（待研究）**：16 队全部 null，infobox 不提供，须另查首秀赛季。
5. **meeting_number 定义（无源）**：全部 null，见 §10。
6. **易地原因（未 sourcing）**：KPV 借用 OmaSP、Lahti/Ilves 同城换场的原因未查到有源说法，不写入。
7. **2021-09-14 Ilves–HIFK 轮次（冲突留空）**：见 §4，需官方轮次表或第二独立轮次源裁决。

## 13. 已证伪 / 死路（不再重派，需新证据才重启）

- Transfermarkt matchday ≠ 官方轮次（2021 年两度证伪：赛程页 MD10 混装 Apr 24 与 Jul 4–5 两批比赛、Apr 25 比赛缺席；
  KuPS 赛程页 matchday 顺序非时间顺序；赛季 id 规则：日历年 = saison_id 年 −1）。不得用于 official_round。
- GSA gameweek ≠ 官方轮次（gw1 = Jun 14–15 比赛；gw2 混装 Jun 18 与 Sep 18–19；gw22 = Sep 11 比赛；既非时间顺序亦非联赛轮次）。
- FBref Wk 对 2022 年已证实破缺（C 路：Wk7 含 KuPS 两次、无 Ilves；Wk9/Wk10 分割不均）——本轮 2021 年 Wk 全量校验正为此而做，
  结果为仅 Wk14/Wk19 一处破缺（见 §4），其余 21 组完整。
- Soccerway live stage URL 重定向至赛季结果页（仅含系列轮 23–27 的 feed）；Wayback Machine 对 Soccerway 2021 常规赛页有快照
  （2021-01-28，赛季前）但抓取被 429 数据中心 IP 拦截（access_blocked）；Arquivo.pt 对该 URL 零结果。
- WorldFootball.net spieltag 页文本抓取 403（按开发指令不再重试）；其 all_matches 文本层仅可作日期/时间交叉参考，其 Round 分块为展示分块，非 KIERROS。
- 芬兰语 Wikipedia 赛季条目无逐轮比赛列表（"kierros" 命中仅为欧战导航）；Sofascore API 403 challenge；Flashscore 结果页纯 JS 无文本层数据；
  veikkausliiga.com 直连超时；FBref 直接 curl 403（故走浏览器文本层，见 §11）。
