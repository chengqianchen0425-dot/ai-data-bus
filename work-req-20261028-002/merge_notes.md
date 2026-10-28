# req-20261028-002 合并说明（主代理合并，四路归一）

## 1. 合并结果

- 合并文件：`method_context_rows_merged.jsonl`，**1,902 行，0 重复 fixture_key**，SHA-256 `4e8c2029294752bf2054d74efe34b902ed626193ceee9241473729ec7e79581b`
- 四路行数：A 2016–2018：594；B 2019–2021：456；C 2022–2025：675；D 2026：177。合计 1,902。
- 与 -004 的关系：B＋C＝1,131 行，恰等于 -004 全量（行键逐字沿用，新增 0、删除 0）；A＋D 为 -004 范围外的新季（2016–2018、2026）。
- **1,902 ≠ 请求 CSV 的 868**：868 是请求方 Windows 机器上那份 CSV（incremental_2019_2026）的候选集，本 VM 上该 CSV 不存在、无法读取，因此无法标出 868 属于 1,902 中的哪几行。本合并文件是 2016–2026 公开宇宙全集（超集），供请求方拿到 CSV 后直接联结，无需返工。绝不声称已覆盖 868。

## 2. 统一口径（与各路原标签不一致处，合并时已按本节改写，原标签保留在 *_route 字段）

### 2.1 venue_status 归一（请求枚举：confirmed / neutral / moved / conflict / unavailable / blocked）

| 合并值 | 行数 | 构成 |
|---|---|---|
| confirmed | 1,598 | A 500＋B 448＋C 650。含义：场次级 FBref Venue 列证据（二级来源），**不是官方确认**（venue_official_confirmation 全库 0 行 true） |
| moved | 59 | A 35＋B 8＋C 16。场次级场馆 ≠ 俱乐部赛季 listed 主场，均有场次级证据 |
| unavailable | 175 | A neutral 59（场馆身份未完全解析：同综合体不同球场／别名未确认／无坐标）＋D neutral 116（Wikipedia 2026 赛季球场表候选，无场次级证据）。原标签保留在 venue_status_route |
| conflict | 70 | C 9（2024 2＋2025 Jaro 7，verified null）＋D 61（Oulu／Gnistan／VPS／Jaro 名称竞争，无一选边） |
| neutral（已验证中立场） | 0 | 本轮没有任何一行拿到“中立场已验证”证据；各路的 neutral 均非此义，已按上表归一，不得误读 |
| blocked（行级） | 0 | FBref 字节拦截是证据层问题（见 §5），行数据均经文本层获得，不记行级 blocked |

### 2.2 meeting_number：全库 null（1,902／1,902）

- 无任何权威源定义 meeting_number；日期顺序、CSV 顺序、球队出现次数、比分、积分榜、盘口推断全部禁用，各路均遵守。
- D 路的 169 个“赛程内顺序计数”**没有**写进 meeting_number（其 basis 自述就是 unordered pair occurrence index，正是请求禁用的推断口径），仅保留在 `meeting_number_schedule_order_count_unverified` 字段供参考，附明确警告不得当作 meeting_number 用。
- D 路另 8 行（KuPS–Oulu、HJK–Inter Turku 各 4 场）因提前进行导致轮次顺序与日期顺序计数相反，两种计数都不采信，记 `meeting_number_count_disagreement=true`。

### 2.3 official_round：全部非官方措辞

- 1,769 行有轮次值，133 行 null（2021 1＋2022 132）。
- 全部轮次值的 official_round_is_official=false：来源分别是 Soccerway 分组（-004 沿用）、worldfootball 分组、FBref Wk 标签、topscorersfootball 标签，**没有一行是联赛官方 KIERROS 措辞**。官方轮次记录至今未拿到（veikkausliiga.com／Tulospalvelu 为 JS 渲染，本轮无真浏览器能力）。
- 2022 常规赛 132 行轮次仍缺：WorldFootball 分页经实证只是展示分块（“6. Round”标题内含横跨 Wk21＋Wk22 的 12 场），FBref Wk 桶也不是干净轮次划分（Wk7 含 KuPS 两次且无 Ilves），一律不升级，只记 fbref_week_bucket。下一步最可行源：真浏览器读 Soccerway ROUND 分组。
- 2021 轮次填补 131／132：FBref Wk 体系经 2020 年 127／127 等价性＋2021 年 Wk 分组全量校验（21／22 组恰为 6 场 12 队）佐证；仅 2021-09-14 Ilves–HIFK 留空（FBref 标 Wk14 但与分组完整性冲突：Wk14 不含它已满 6 场，Wk19 缺的恰好就是这一对），记 conflict 不改写。

### 2.4 row_status_merged（统一规则，各路原 row_status 保留在 row_status_route）

- conflict：轮次标签冲突（A 176 行：2016 13＋2017 102＋2018 61）／场馆冲突（70 行）／B 路 2020 年 4 行开球·日期分歧。合计 251。
- complete：轮次＋已验证场馆（confirmed／moved＋坐标＋时区）＋开球三者齐全且无未决分歧。合计 1,188。
- partial：三者不全，或开球带未决系统分歧（C 2025 170 行）。合计 463。
- unavailable：0；blocked：0；missing：0（各季 expected＝discovered）。
- **故意不带入 merged conflict 的三类**：① C 路 2023-04-15 两行 moved（两源一致确立易地场馆，竞争候选保留在 venue_competing_candidates，route 标签原样保留）；② D 路 8 行 meeting_number 计数分歧（属 meeting_number 维度，不属字段冲突）；③ B／C 的 kickoff_conflict_note（那是变更日志：系统性 ＋2h 修正行全部带此注，B 自身 row_status 证明它们不算 conflict）。

### 2.5 开球时间：跨季口径不统一，绝不能直接横向比较（每行 kickoff_basis 为准）

- **-004 时间列系统性错误已实证**：2019、2021、2022、2023 四季 -004 时间恰为 FBref 本地时间 −2h（英国时钟值误标 Europe/Helsinki），本轮已按 FBref 值覆盖（2022 直接抽查 54／54、2023 直接比对 21／21，余下为模式延伸，残留风险已注）。
- **2020 年没有系统偏移**（57／61 行与 FBref 完全一致），未套 ＋2h，逐行采用 FBref 值。
- **2024 年仅 7 场附加赛覆盖**，联赛 162 行保留 -004 值并附冲突说明；**2025 年全部保留 -004 值**，FBref 系统性 ＋2h 分歧未裁决、UTC 全部 withheld——2025 开球是本轮最大的未决时间项（模式上很可能同样是 −2h，但未经 2025 季逐行证实，不擅自推广）。
- 2016–2018：FBref Time 列第一时刻，时区／UTC 一律 null（源未声明时区；2016 文本括号第二时刻是抓取方换算值，不记录）。
- 2026：171／177 行为 null（源只给日期）；仅第 1 轮 6 场有时间（Flashscore 预览，标注 CEST；芬兰实行 EEST＝UTC＋3，与 CEST＝UTC＋2 字面冲突，UTC 一律不换算）。

### 2.6 其他 -004 修正（本轮新发现）

- 2020 日期纠正 2 行（行键保留，旧值在 date_as_in_req20261006_004）：HIFK–RoPS（-004 2020-11-04 → 实际 2020-10-22，18:30→18:00，轮次补 21）；Honka–HJK（-004 2020-09-19 → 实际 2020-09-20，18:30→13:00，轮次 15 不变）。纠正后 2020 日期缺失 0、轮次缺失 0。
- 2024 Gnistan 火灾易地 7 场（2024-07-13 Mustapekka 主看台火灾后主场改 Bolt Arena，-004 映射对这 7 场是错的）。
- 2019 KPV 借用 OmaSP Stadion 8 场（跨城借用他队主场）；2019 Lahti Kisapuisto 5 场、Ilves Ratinan 2 场、2020 Ilves Ratinan 10 场为同城换场（与 -004 映射不一致，已修正）。
- 2022 年 4 月易地 7 场中 3 场仅 FBref 单源，标 implausible；2023 易地 2 场为 FBref＋Sky 两源一致。

## 3. 按赛季计数（merged status）

| 赛季 | expected | discovered | complete | partial | conflict | unavailable | blocked | missing |
|---|---|---|---|---|---|---|---|---|
| 2016 | 198 | 198 | 165 | 20 | 13 | 0 | 0 | 0 |
| 2017 | 198 | 198 | 86 | 10 | 102 | 0 | 0 | 0 |
| 2018 | 198 | 198 | 122 | 15 | 61 | 0 | 0 | 0 |
| 2019 | 162 | 162 | 162 | 0 | 0 | 0 | 0 | 0 |
| 2020 | 132 | 132 | 128 | 0 | 4 | 0 | 0 | 0 |
| 2021 | 162 | 162 | 161 | 0 | 1 | 0 | 0 | 0 |
| 2022 | 162 | 162 | 30 | 132 | 0 | 0 | 0 | 0 |
| 2023 | 167 | 167 | 167 | 0 | 0 | 0 | 0 | 0 |
| 2024 | 169 | 169 | 167 | 0 | 2 | 0 | 0 | 0 |
| 2025 | 177 | 177 | 0 | 170 | 7 | 0 | 0 | 0 |
| 2026 | 177 | 177 | 0 | 116 | 61 | 0 | 0 | 0 |
| 合计 | 1,902 | 1,902 | 1,188 | 463 | 251 | 0 | 0 | 0 |

## 4. 赛制（double_round_robin 指“整季为单一双循环”，非冠军组局部）

- 2016–2018：否，三循环（33 轮，每对 3 次）。依据：赛季页 Matches 1–22／23–33 两段结构＋FBref Wk 1–33＋对赛计数；赛季页无 triple round-robin 散文原句，结论建立在结构上。
- 2019：否，22 轮＋分裂后各 5 场（27 场／队）＋欧战附加赛。
- 2020：是，22 轮（分裂于 2020-10-28 决定取消，新冠疫情）。
- 2021–2022：否，22 轮＋分裂组单循环 5 场（27 场／队）。
- 2023：否，22 轮＋分裂组单循环 30＋附加赛 5（167 场）。
- 2024：否，22 轮＋分裂组单循环 30＋欧战附加赛 5＋升降级附加赛 2（169 场）。
- 2025–2026：否（整季混合），22 轮＋保级组单循环 15＋冠军组双循环 30（177 场）；2025 起欧战附加赛废除。
- 2026 赛季进行中、未完赛：常规赛与保级组轮次已完，冠军组剩 30–32 轮 9 场（日期已发布，2026-10-28 至 2026-11-08）；Wikipedia 赛季页的两回合联赛附加赛不计入 177 场联赛场次。

## 5. Provenance 状态（按请求新标准：描述或 URL 的哈希不算证据哈希）

- A 路（2016–2018）：FBref 源字节被 Cloudflare 拦截（curl 000、scrapling 403、curl_cffi 模拟 Chrome 仍 403，三路证实），594 行 FBref 证据为浏览器文本层转录，`provenance.fixture.source_sha256` 一律 null 并注明原因，挑战页哈希绝不用作行哈希。维基赛季页、俱乐部文章、场馆坐标 API 响应全部实际下载并算 SHA-256（已用 sha256sum 复验）。
- B／C 路：FBref 全表逐行转录并经脚本校验（B 456／456 精确匹配、零未匹配零多余）；Transfermarkt matchday、GSA gameweek 已证伪，不用作轮次源。
- D 路：赛程源字节 SHA-256 为真实下载文件哈希（topscorersfootball HTML 154,635 字节；Wikipedia 2026 球队表 HTML），不是描述符哈希；Flashscore 预览与俱乐部页行内哈希为 null 并注明原因。
- 上一单 -004 的描述符哈希做法本轮未沿用；凡本轮新增字段的字节哈希均为实采，拿不到写 null。

## 6. 俱乐部身份（有源事实，名字像绝不合并）

- founded 年份：A 路 15 家全部有源映射（含 PS Kemi 冲突裁决：1999，1932 属前身 KePS，绝不合并；PK-35 Vantaa（2008 沿革、2016 解散）与现存赫尔辛基 PK-35 是两家俱乐部，绝不合并；JJK "2000 (1992)" 原文照抄、不解读）。
- competition_entry_year：本轮大多 null（B 路 16 队全空：infobox 只给 founded year；C 路多队未核实）；D 路仅 2026 升班两队有值（Lahti、TPS 2026；交接：Haka 直接降级、KTP 附加赛失利降级，三源一致）。
- 关键身份事实：PK-35 Vantaa 破产退出次级联赛席位由 OPS 顶替；FC Honka 破产被取消资格、名额由 Gnistan 通过补充许可程序顶替；HIFK 2023 季后在次级联赛因破产解散。
- 未核实（同名绝不合并）：PK-35 Vantaa 与此后次级联赛 PK-35 的实体关系、HIFK 法人连续性、FC Honka 被取消资格后的去向层级；2018 季后降级未核实；2021–2024 各季欧战附加赛具体对阵结构未逐一核对；2020 分裂取消后欧战附加赛是否举行未核实；2021、2022 季清单采用“上季清单 ± 升降级变动＋分组片段交叉核对”推导、未逐页打开该两季球场表直证。

## 7. 未解决队列（fixture_key 级为主，另含系统项）

- U-01 pending_work：meeting_number 全库 1,902 行 null。无权威定义源；D 路 169 个顺序计数仅供参考，不可当作 meeting_number。
- U-02 pending_work：2022 常规赛 132 行 official_round null（见 §2.3，下一步：真浏览器读 Soccerway ROUND 分组）。
- U-03 conflict：2021-09-14 Ilves–HIFK 轮次（FBref Wk14 与分组完整性冲突）。
- U-04 conflict：2017（102 行）＋2018（61 行）＋2016（13 行）FBref Wk 标签异常，需官方轮次记录升级。
- U-05 系统项：场馆官方确认 0／1,902。全部场馆确认均为 FBref 二级来源或赛季表候选。
- U-06 conflict：场馆竞争 70 行（C 9＋D 61，见 §2.1）。
- U-07 unavailable：场馆未验证 175 行（A 59 身份／坐标未解析＋D 116 赛季表候选）。
- U-08 conflict（非行项）：2023 标签文件主客颠倒 1 条——标签文件 168 键中“2023-04-30 KuPS 主场 vs Mariehamn”与 -004／FBref 的同日“Mariehamn 主场 vs KuPS”不一致，未作新场次，需官方赛程页裁决主客。
- U-09 pending_work：2026 开球 171／177 行 null（仅第 1 轮 6 场有时间，CEST／EEST 字面冲突未换算）。
- U-10 pending_work：2025 开球 170 行未决系统分歧（保留 -004、FBref 系统性 ＋2h、UTC withheld）。
- U-11 pending_work：CSV 精确联结全库 pending（请求 CSV 本 VM 不存在；1,902 为超集，868 子集待请求方上传 CSV 或确认派生集后联结）。
- U-12 pending_work：俱乐部 competition_entry_year 大多 null（见 §6）。
- U-13 access_blocked：2016–2018 FBref 行字节 provenance（Cloudflare 403，三路证实）；2026 worldfootball.net 全量页 HTTP 403（未重试、未绕过）；veikkausliiga.com／Tulospalvelu 官方源 JS 渲染（本轮无真浏览器能力）。无 retry_after 承诺——官方源需真浏览器任务另行安排。
- U-14 系统项：2026 赛季进行中，冠军组 30–32 轮 9 场日期已发布但未完赛；本交付只含赛前事实，不含任何比分／赛果／积分／预测。

## 8. 合并脚本与复核

- 合并脚本：`merge_20261028_002.py`（可复跑，含重复键断言、禁字段键扫描：比分／赛果／观众／裁判／进球／盘口／预测／积分键 0 个）。
- 交叉复核：venue_status 合并计数（confirmed 1,598＝A 500＋B 448＋C 650；moved 59＝A 35＋B 8＋C 16；unavailable 175＝A 59＋D 116；conflict 70＝C 9＋D 61）与各路汇报逐项对上；merged complete／partial／conflict（1,188／463／251）与各路 row_status 经口径说明后对上（差异处见 §2.4）。
- 各路原文件、notes、evidence、season 分季文件全部保留在 work-req-20261028-002/ 内，未改动。
