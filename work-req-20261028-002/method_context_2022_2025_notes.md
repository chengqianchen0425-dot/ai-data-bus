# req-20261028-002 C 路 notes：Veikkausliiga 2022–2025 交叉核对 + 缺口填补

## 0. 交付与口径（先读）

- 主文件：`method_context_2022_2025.jsonl` — 675 行，675 个唯一 fixture_key，SHA-256 `961264de395ca2140f4e8191a9921bf58ce30063503d7d6c43c5c21a2d1f8931`。
- 来源文件（分赛季，不改动）：`season_2022.jsonl`（162）、`season_2023.jsonl`（167）、`season_2024.jsonl`（169）、`season_2025.jsonl`（177），各附 `season_YYYY_notes.md`。
- 合并方式：四季文件原值拼接，按（season, date, fixture_key）排序，键取并集（缺失键补 null）；合并新增字段只有 4 个，全部在 §1.3 说明，不改动任何赛季 agent 的原值。
- 全程只做赛前事实：无比分、赛果、赛后状态、积分榜、盘口、预测字段（合并文件禁字段扫描：score/winner/prediction/odds/market 类键 0 命中）。
- CSV 联结硬缺口：请求方指定的身份 CSV（Windows 路径 `D:\奇门斗数\...method_context_request_fixtures_20261028.csv`，SHA-256 `9de8b8fac5fcdebbc51e1df99f9a5fe329e3149f3deacc2dfcc4105cd9a4c093`）在本 VM 上不存在、无法读取。因此 675 行全部沿用 -004 fixture_key 并标 `csv_join_status="matched_to_req-20261006-004_row_csv_join_pending"`；最终 CSV 精确联结是未解决项，须请求方上传 CSV 或确认后才能闭合。无任何模糊匹配。

## 1. 计数

### 1.1 按赛季计数（expected / discovered / missing）

| 赛季 | expected（-004 基线） | discovered（本轮） | missing | 新增行 |
|---|---|---|---|---|
| 2022 | 162 | 162 | 0 | 0 |
| 2023 | 167 | 167 | 0 | 0 |
| 2024 | 169 | 169 | 0 | 0 |
| 2025 | 177 | 177 | 0 | 0 |
| 合计 | 675 | 675 | 0 | 0 |

### 1.2 行状态（as-reported，⚠️ 四季口径不统一，见 §1.3）

| 赛季 | complete | partial | conflict | unavailable（整行） | blocked（整行） |
|---|---|---|---|---|---|
| 2022 | 0 | 162 | 0 | 0 | 0 |
| 2023 | 165 | 0 | 2 | 0 | 0 |
| 2024 | 0 | 167 | 2 | 0 | 0 |
| 2025 | 0 | 170 | 7 | 0 | 0 |
| 合计 | 165 | 499 | 11 | 0 | 0 |

⚠️ 口径警告：2023 季的 complete=165 是该季 agent 的宽松口径（即使 meeting_number 全缺、轮次全为非官方交叉源仍标 complete）；2024 季 agent 用严格口径（无官方轮次＋meeting_number 全缺即不标 complete，故 complete=0）。两季的 complete 不可直接比较。合并层面以 §1.4 的字段级计数为准，不以 row_status 汇总作结论。

### 1.3 合并新增字段（4 个，不改原值）

- `merge_source_file`：行来源分季文件。
- `venue_official_confirmation`：全部 675 行均为 False。含义：没有任何一行的场馆得到官方联赛/俱乐部比赛页确认；各季文件里 `venue_status="confirmed"` 的含义是 FBref 场次级 Venue 列与 -004 赛季映射一致（次级来源），不是官方确认。合并时特此澄清，不让 confirmed 字面被误读。
- `official_round_kind`：`numeric`（数字轮次，全部为非官方交叉源或 -004 沿用，见 §2）、`phase_label_non_official`（2023 附加赛 5 行、2024 附加赛 7 行：official_round 字段填的是阶段标签而非数字轮次）、null（2022 常规赛 132 行仍缺）。
- `kickoff_handling`：每季开球时间的处理方式常量（见 §5，三季口径不统一，原样并列，不抹平）。

### 1.4 合并层面字段级计数（结论以此为准）

| 维度 | 2022 | 2023 | 2024 | 2025 | 合计 |
|---|---|---|---|---|---|
| 数字轮次（numeric，全部非官方交叉源/-004 沿用） | 30 | 162 | 162 | 177 | 531 |
| 阶段标签轮次（phase_label，非官方） | 0 | 5 | 7 | 0 | 12 |
| 轮次仍缺（null） | 132 | 0 | 0 | 0 | 132 |
| meeting_number 已填 | 0 | 0 | 0 | 0 | 0 |
| 场馆 match 级取值（venue_verified 非 null） | 162 | 167 | 167 | 170 | 666 |
| 场馆 verified=null（冲突行） | 0 | 0 | 2 | 7 | 9 |
| 场馆官方确认 | 0 | 0 | 0 | 0 | 0 |
| 开球时间 present | 162 | 167 | 169 | 177 | 675 |
| kickoff_utc present | 162（换算） | 167（换算） | 7（仅附加赛） | 0（全部 withheld） | 343 |

## 2. -004 交叉结果：沿用 / 覆盖 / 新增

- 沿用：身份（日期、主客队）675/675 一字未改；fixture_key 675/675 逐字沿用。
- 覆盖（只在有更强证据时）：
  - 开球时间：2022 全季 162 行 +2h；2023 全季 167 行 +2h；2024 仅 7 场附加赛覆盖（联赛 162 行保留 -004 值并附冲突说明）；2025 全季保留 -004 值（UTC 全部 withheld）。覆盖总数 336 个时间值，旧值分别保留在各季的 `kickoff_004_old` / `kickoff_old_req20261006_004` 字段（2024 旧值见行内冲突说明）。
  - 场馆 match 级取值变化：2022 7 场 moved（赛季映射→当场场馆）；2023 2 场 moved；2024 7 场 moved（Gnistan 火灾易地）＋ 2 场标 conflict（verified 置空）；2025 7 场标 conflict（verified 置空，未改值）。
  - 轮次：2023 5 场、2024 7 场由 null 填为阶段标签（非官方，见 §3）；2022 常规赛 132 场仍 null；其余数字轮次全部沿用 -004 的 WorldFootball 分组并诚实重标为非官方交叉源，未升级为官方 KIERROS。
- 新增行：0。-004 之外的场次未发现、未添加。

## 3. 轮次填补结果与赛制结论（分季，全部有源）

### 2022：常规赛 132 场仍缺；赛制 162 = 132 + 30
- 常规赛双循环（12 队×22 场＝132 场）＋ 两组各单循环系列赛（6 队×5 场，每组 15 场，共 30 场）＝ 162 场，每队 27 场。2022 系列赛是单循环，不是双循环；不要套用现行“冠军组双循环 32 场”口径。
- 132 场 `official_round` 仍为 null（`still_missing`）。尝试源：veikkausliiga.com 存档（无可用链接，-004 记 HTTP 500）、Tulospalvelu（无深链且 JS 门）、Soccerway 文本层（只剩导航，待查 URL 已写入 season_2022_notes.md §8）、WorldFootball 分页（本轮实证确为展示分块：标题“6. Round”内含横跨 Wk21+Wk22 的 12 场比赛，不能当轮次）。
- FBref Wk 桶不能当轮次：Wk7 含 KuPS 两次且无 Ilves；Wk9/Wk10 拆分不均。常规赛只记 `fbref_week_bucket` 并标注“不是轮次”。系列赛 Wk1–5 则是干净分区（每组每周每队 1 次），与 -004 的 22+Wk＝23–27 完全对应——这是保留 30 场的理由，但仍不是官方复核。
- 下一步最可行源：真浏览器读 Soccerway ROUND 分组（2022 季 agent 建议）。

### 2023：5 场 null 全部填为阶段标签；赛制 167 = 132 + 30 + 5
- 5 场确为欧协联附加赛：四分之一决赛×2（10-25 Honka–Inter、SJK–Oulu）、半决赛×1（10-28 Honka–Oulu）、决赛两回合（11-01 Honka–VPS、11-05 VPS–Honka）；赛制为第 3 名 VPS 直通决赛、其余 4 队单场淘汰、决赛两回合。依据：Wikipedia 赛季页 Play-offs 节（curl 实字节哈希）＋ FBref Round 列，`official_round_source` 标非官方。
- 赛制：常规赛双循环 132 ＋ 冠军/保级组内单循环 30（轮次 23–27）＋ 附加赛 5 ＝ 167。常规赛是双循环，分组赛是单循环，整季不是纯双循环。Wikipedia 信息框 "Matches 132" 只计常规赛；第 11 名的升降级附加赛不在 167 行内。

### 2024：7 场 null 全部填为阶段标签；赛制 169 = 132 + 30 + 5 + 2
- 7 场不是同一附加赛：5 场欧战附加赛（Conference League play-off：1/4 决赛单场 Haka–Inter、VPS–Gnistan；半决赛单场 Haka–Gnistan；决赛两回合 Haka–SJK）＋ 2 场升降级附加赛（联赛第 11 名 Lahti vs 次级联赛第 2 名 Jaro，两回合；Jaro 不是 2024 联赛队，仅以附加赛身份出现）。
- 赛制：常规赛双循环 132 ＋ 冠军/保级组单循环 30 ＝ 162 场联赛 ＋ 5 场欧战附加赛 ＋ 2 场升降级附加赛 ＝ 169 场。

### 2025：轮次 1–32 全有值；赛制 177 = 132 + 15 + 30
- 常规赛双循环 22 轮 132 场；保级组 6 队单循环 5 周 15 场（每队止于 27 场）；冠军组 6 队双循环 10 周 30 场（每队止于 32 场）。
- 28–32 轮的 15 场全部是冠军组第 6–10 周，不是欧战附加赛、不是额外系列；每轮仅 3 场是因为保级组已在第 5 周（10 月 18 日）结束，只剩 6 支冠军组球队。23–27 轮每轮 6 场是冠军组一周＋保级组一周同窗口捆绑，逐场拆分已写入各行 `series_or_phase`。
- 展示轮次 ≠ 阶段周次 ≠ 日期顺序：如 28 轮 Ilves–KuPS（冠军组第 6 周，10 月 16 日）实际早于冠军组第 5 周（10 月 19 日）开球，属提前进行的场次、周次标签不变，未按日期重排。

### meeting_number（四季统一结论）
- 675/675 全部 null ＋ unavailable。无权威源定义该字段；FBref 的 Wk 是轮次标签，明确未挪用为 meeting number；绝无日期顺序/出场次数/比分/积分榜/盘口推断。尝试源见各季 notes（veikkausliiga.com、Tulospalvelu、Soccerway、WorldFootball、FBref 均无该字段）。

## 4. 场馆（match 级取值 vs 官方确认，两层分开）

- 官方确认：0/675（官方联赛/俱乐部比赛页确认 0 行）。这是本轮最大的结构性缺口，原因是官方源 JS 渲染且子代理无真浏览器能力。
- FBref 场次级 Venue 列取值：666 行有 venue_verified（2022 162、2023 167、2024 167、2025 170），9 行 verified=null（2024 冲突 2、2025 冲突 7）。
- 易地（moved，赛季映射→当场场馆）：
  - 2022 7 场 4 月易地（人工草）：Honka–Haka、Honka–SJK、Inter–Haka → Bolt Arena；Lahti–VPS、Oulu–Ilves → Lemonsoft Stadion；Inter–Oulu、Ilves–KuPS → Tehtaan kenttä。其中 Lahti–VPS、Inter–Oulu、Oulu–Ilves 标 implausible（主队在对方/第三方主场，仅 FBref 单源），需真浏览器复核官方比赛页。
  - 2023 2 场（均 FBref＋Sky Sports 两源一致）：2023-04-15 Honka–SJK 实际在 Myyrmäen jalkapallostadion（Vantaa，60.26024, 24.84279，本轮 geocode 全地址结果）；同日 Ilves–Inter 实际在 Tehtaan kenttä（Valkeakoski）。
  - 2024 7 场 Gnistan 火灾易地：2024-07-13 Mustapekka Areena 主看台火灾后，7 个剩余主场实际在 Bolt Arena（Töölö），-004 的 Mustapekka 映射对这 7 场是错的，已修正；火灾前 7 场仍为 Mustapekka（FBref 的 FAIR PAY Areena 是同一球场旧赞助名）。
- 冲突（verified 置空，未采信一方）：
  - 2024-04-21 Ekenas–AC Oulu（FBref 称万塔 Myyrmäki vs Sportsmole 称 Centrumplan）；2024-04-27 AC Oulu–VPS（FBref＋Sky 称瓦萨 Lemonsoft vs Sportsmole＋-004 称奥卢 Raatin）。
  - 2025 Jaro 7 月 25 日后主场 7 场：-004 Centralplan、FBref 的 "Länsikenttä TN"、维基新球场 Project Liv Arena（2025 年开放、首场男子比赛即 7 月 25 日 Jaro–VPS）三方竞争候选全部保留，未把 Länsikenttä TN 与新球场强行合并。
- 名变体澄清（同一球场，不作新场馆）：2024 Ekenäs：Tammisaaren keskuskenttä ＝ Ekenäs Centrumplan ＝ Ekenäs Sparbank Arena（12 场）；但主场许可/达标文件未找到，仍为开放项。
- 坐标与时区：坐标除 2023 Myyrmäki 外沿用 -004 venue-coords.json（18 球场地理编码结果，注明出处）；场馆 IANA 时区全部 Europe/Helsinki（芬兰境内场馆）。

## 5. 开球时间与时区（三季口径不统一，原样并列）

| 赛季 | 本轮处理 | 证据强度 | 残留风险 |
|---|---|---|---|
| 2022 | 162 行全部 +2h；UTC 按 EEST UTC+3 换算（全部日期在夏令时内） | 54 场直接抽查 54/54 恰为 -004+2h（4–10 月常规赛＋系列赛全覆盖）；Sky Sports 英国时间锚点换算吻合（HJK–Honka 13:00 BST＝15:00 EEST；HIFK–VPS 21:00 BST＝23:00 EEST）；WorldFootball 时间列同样比本地晚 2h | 其余 108 行为均匀模式的明示延伸，未逐场断言 |
| 2023 | 167 行全部 +2h；UTC 按 EEST UTC+3 / 2023-10-29 起 EET UTC+2 换算 | 21 行逐行比对 21/21 恰为 -004+2h；FotMob/CapperTek/SportsMole 的 UTC 瞬时、Wikipedia 英国时钟时间三方闭合 | 其余 146 行为系统性模式覆盖（FBref curl 本机返回 000、无字节，未能机器逐行转录），建议下游使用前做一次机器级 FBref 复核 |
| 2024 | 联赛 162 行保留 -004 值并附冲突说明，kickoff_utc 置 null；仅 7 场附加赛用 FBref 本地时间覆盖并按 EEST/EET 换算 | 抽查 Gnistan–VPS 以 Tiketti 本地 18:30 ＝ FBref 18:30 ≠ -004 16:30，证明 -004 值不是本地时间；但 FBref 页面未声明时区 | 联赛 162 场未批量修正，-004 值与 FBref 值相差 2h 的冲突未裁决 |
| 2025 | 全部保留 -004 值；kickoff_utc 全部 withheld | FBref 时间在全部抽查中系统性比 -004 快 2 小时（分钟完全一致），且 FBref 未声明时区，无法判断哪方为本地时间 | 换算会掩盖冲突，故不换算；-004 值是否为本地时间未证实 |

共同结论：-004 的开球时间列存在系统性 2 小时偏差（英国时钟值被误标为 Europe/Helsinki），四季 agent 各自独立发现同一模式；但四季的修正策略不同，合并时不统一改写，下游使用前必须按上表分季处理，绝不能把四季时间当作同一口径直接比较。

## 6. 俱乐部官方身份（分季摘要，缺失一律 null 不猜）

- 2022：VPS 2021 Ykkönen 冠军升入 2022、KTP 降级离场、HIFK 季末降级、HJK 建队 1907 有源；Helsingfors IFK 与 IFK Mariehamn 明确为不同俱乐部；其余 11 队建队年本轮未核实、一律 null。
- 2023：12 队建队年已核（KTP 1927-09-22，2023 唯一升班马、2022 Ykkönen 冠军；2013 年 12 月 FC KooTeePee 更名 KTP 并保留席位是关键沿革点）；Ilves 足球分部独立建队年、Lahti/SJK 合并对象未核实，留空。
- 2024：有源建队年只写 7 队（Ekenäs 1905、Gnistan 1924、Haka 1934、Jaro 1965-12-18、Lahti 1996 合并成立、AC Oulu 2002、SJK 2007），其余 6 队 null；升班马区分清楚（Ekenäs 冠军直升、时隔 90 年；Gnistan 第 2 名因 Honka 破产递补、队史首季）。
- 2025：升入 KTP（2024 Ykkösliiga 冠军，缺席一季后回归）、Jaro（2024 附加赛胜者，缺席九年后回归）；降出 EIF（2024 垫底，单季后降级）、Lahti（2024 附加赛负者，13 年顶级生涯结束）。KTP 建队年：2023 季已核 1927-09-22，2025 季 agent 抓到消歧义页未核实——以 2023 季的有源值为准，2025 季的未核实不覆盖它；Ilves 1931 仅为体育俱乐部年（2025 季 agent 抓到的是冰球条目），足球分部年份仍未核实。

## 7. Provenance 铁律执行情况

- 实字节 SHA-256 仅见于：2023 季 Wikipedia 赛季页（curl 实字节）；2025 季 Wikipedia 赛季页、联赛结构页、各俱乐部页（curl 实字节）。其余全部字段 source_sha256 一律 null 并注明“文本层、无字节”或“-004 描述符哈希不复用”。
- -004 的 source_sha256 是 provenance 描述符的哈希，本轮明令其不是源证据哈希，合并文件不复用、不转述为证据哈希。
- 每个非 null 字段均附 source_url、final_url、retrieved_at（带时区）、field_locator、source_name（见各行 provenance 对象；赛季级事实的来源见各季 notes）。
- WorldFootball curl 本机曾返回 403、FBref curl 本轮实测 403/000，故这两源的证据只能是文本层，sha256 一律 null。

## 8. 未覆盖与冲突清单（合并 unresolved_queue）

| 编号 | 类别 | 内容 | 下一步 |
|---|---|---|---|
| U-01 | blocked（CSV） | 请求方身份 CSV 在本 VM 不存在；675 行精确联结 pending | 请求方上传 CSV 或确认派生集后闭合 |
| U-02 | unavailable | meeting_number 675/675 缺失（无权威源定义） | 官方赛程/竞赛规程中找明确定义；找不到则永久 null |
| U-03 | unavailable | 官方 KIERROS 数字轮次：2022 常规赛 132 场缺失；其余 543 个非 null 轮次值（531 个数字轮次＋12 个阶段标签）全部为非官方交叉源（WorldFootball 分组、FBref＋Wikipedia 交叉）或 -004 沿用，未经官方复核 | 真浏览器读 Soccerway ROUND 分组（2022 最可行）＋ veikkausliiga.com/Tulospalvelu 官方赛程页 |
| U-04 | unavailable | 场馆官方确认 0/675 | 真浏览器定向核查官方比赛页/俱乐部公告 |
| U-05 | conflict | 2024 场馆冲突 2 场（Ekenas–AC Oulu、AC Oulu–VPS，见 §4） | 真浏览器裁决 |
| U-06 | conflict | 2025 Jaro 7 月 25 日后主场 7 场三方候选（见 §4） | 真浏览器＋新球场启用报道复核 |
| U-07 | conflict | 开球时间系统性 2h 冲突（四季，见 §5）；2024 联赛 162 场未裁决，2025 全季未裁决 | 官方比赛页逐场复核；2023 146 行、2022 108 行模式延伸部分先做机器级 FBref 复核 |
| U-08 | conflict | 2023 标签文件主客颠倒 1 条：标签文件 168 键中 "2023-04-30 KuPS 主场 vs Mariehamn" 与 -004/FBref 的同日 "Mariehamn 主场 vs KuPS" 不一致（未作新场次） | 以官方赛程页裁决主客 |
| U-09 | blocked | 2022 易地 3 场标 implausible（Lahti–VPS、Inter–Oulu、Oulu–Ilves，仅 FBref 单源，主队在对方/第三方主场） | 真浏览器复核官方比赛页 |
| U-10 | unavailable | 2024 Ekenäs 主场许可/达标文件未找到 | 官方/俱乐部许可文件检索 |
| U-11 | unavailable | 俱乐部建队年缺失：2022 11 队、2023 Ilves 足球分部＋Lahti/SJK 合并对象、2024 6 队、2025 Ilves 足球分部 | 俱乐部官方史/维基俱乐部页逐队核实 |
| U-12 | blocked | veikkausliiga.com 存档（-004 记 HTTP 500）、Tulospalvelu（JS 门、无深链）、Soccerway 文本层（只剩导航）均不可达 | 真浏览器任务 |

## 9. 最大障碍（四季共同）

官方源不可达：veikkausliiga.com 与 Tulospalvelu 均为 JS 渲染、子代理无真浏览器能力，导致三件事无法在本轮闭合——官方 KIERROS 编号、开球时间的逐场官方复核、场馆冲突的裁决。以上全部列入 §8，需父代理安排真浏览器任务跟进。除此之外，本轮 675 行中没有需要请求方拍板购买或登录的事项（全程未购买、未登录、未用任何密钥/凭证、未动用付费 API 额度）。
