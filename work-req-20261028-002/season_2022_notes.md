# 2022 Veikkausliiga — 交叉核对 + 缺口填补说明（req-20261028-002 执行 agent）

> 范围：只做赛前事实（日期、主客队、开球时间、轮次、赛制、场馆、俱乐部身份）。
> 比分、赛果、赛后状态、积分榜、盘口、预测一律不写、不用于推断。
> 本轮不写 `repo/responses/`，不碰其他赛季文件；交付仅 `season_2022.jsonl` + 本说明。

## 1. 计数

| 口径 | 数 |
|---|---|
| expected（-004 基线 2022 季） | 162 |
| discovered（本轮核对后联赛场次） | 162（与基线集合一致，无新增联赛场次） |
| complete | 0（见下：没有任何一行拿到官方轮次 + 官方场馆双重验证，故无一行标 complete） |
| partial | 162 |
| unavailable（行级） | 0 |
| blocked（行级） | 0 |
| conflict（行级状态） | 0（场馆字段级 moved 7 场、其中 implausible 标记 3 场，见 §5，不升为行级 conflict） |
| missing：official_round | 132（常规赛全部） |
| missing：meeting_number | 162（全部） |
| -004 沿用 | 身份（日期+主客队）162/162 未变；场馆候选 162/162 保留为 candidate；官方轮次 30/30 保留（系列赛 23–27，见 §3 保留理由与诚实限定） |
| -004 覆盖 | 开球时间 162/162（全部 +2 小时，见 §2）；场馆 match 级取值 7/162 由赛季主场映射改为 FBref 当场场馆（moved，见 §5） |
| 本轮新增行 | 0（FBref 赛程中的季后附加赛不在 162 联赛范围内，未加行，见 §7） |
| CSV 联结 | 162/162 `csv_join_status="matched_to_req-20261006-004_row_csv_join_pending"`；请求方指定身份 CSV 的 Windows 路径在本 VM 不存在、无法读取，故只按 -004 fixture_key 联结，unresolved 行 0（不做模糊匹配） |

## 2. 最大发现：-004 开球时间整列错 2 小时（162 场全部覆盖）

- -004 的 `kickoff`（标注 Europe/Helsinki）与 FBref 赛程表 Time 列逐场对比：
  54 场直接抽查（4 月–10 月常规赛 + 系列赛全覆盖）**54/54 恰好是 -004 + 2 小时**，无一例外。
- 独立锚点（Sky Sports，英国时间）换算后与 FBref 本地时间完全吻合：
  - HJK–Honka 2022-04-02：Sky 13:00 BST = 15:00 EEST = FBref 15:00；-004 为 13:00。
  - HIFK–VPS 2022-06-18：Sky 21:00 BST（结构化数据 `2022-06-18T21:00:00+01:00`）= 23:00 EEST = FBref 23:00；-004 为 21:00。
- 本轮 WorldFootball 文本层返回的赛程块（2022-09-01–11 段）时间同样比 FBref 本地时间晚 2 小时，
  与 -004 一致——说明 -004 时间继承自 WorldFootball 的英国时间显示，却被标注为 Europe/Helsinki。
- 处理：`kickoff_local` = -004 值 + 2 小时；`kickoff_timezone` = Europe/Helsinki；
  `kickoff_utc` = 本地 − 3 小时。全部 162 场日期都在 2022 年夏令时内
 （芬兰 EEST 2022-03-27–10-30，UTC+3），无跨日换算、无 EET 场次。
  换算方法逐行写在 `kickoff_timezone_method`；54 场有逐场 FBref 断言，
  其余 108 场是该均匀模式的延伸（方法已明示，不是静默推断）。
- 另有佐证：Wikipedia 季后附加赛时间明示 18:00 EEST，与 FBref 18:00 一致，
  证明 FBref 时间列就是场馆本地时间。

## 3. 轮次填补结果：官方填补 0 场；系列赛 30 场保留但未重新验证为官方

| 口径 | 数 |
|---|---|
| official_round 本轮新填（官方源） | **0** |
| official_round 仍缺 | 132（常规赛全部，`official_round_status="still_missing"`） |
| official_round 沿用 -004 | 30（系列赛 23–27，`official_round_status="from_req-20261006-004"`） |
| 非官方轮次标签（绝不升级为 official） | 系列赛：FBref 系列 Wk 1–5（22+Wk = 23–27）；常规赛：仅记 FBref 周次桶 `fbref_week_bucket`，**不是轮次** |

### 为什么常规赛 132 场一个官方轮次都没填

按任务顺序尝试（详见 §8），没有任何一个官方源在本轮可读：
veikkausliiga.com 存档无可用链接（-004 记 HTTP 500）、Tulospalvelu 无深链且为 JS 应用、
Soccerway 文本层只剩导航（JS 门）、WorldFootball 分页是展示分块（下证）。
因此 132 场 `official_round` 保持 null，**绝不从日期顺序推断**。

### 为什么不把 FBref Wk 当轮次用（关键纠错）

FBref 的 Wk 列是“周次桶”，不是干净的轮次划分，实证：

- Wk7 含 KuPS 两次（2022-05-08 Mariehamn–KuPS、2022-05-12 KuPS–Haka），且无 Ilves；
- Wk9/Wk10 拆分不均（同日 2022-05-28 的 Oulu–SJK、Haka–Lahti 标 Wk9，
  Inter–Ilves 标 Wk10；两组合计各队出现 1–3 次不等）。
- 若把 Wk 当轮次，会系统性错标延期/提前场次。故 JSONL 中常规赛只给
  `fbref_week_bucket` + `round_non_official_source="fbref_week_bucket_only"`，
  并在每行 notes 中写明“不是轮次”。

### 系列赛 30 场保留的理由与诚实限定

- -004 的 23–27 与 FBref 系列 Wk 完全对应（22+Wk），且系列赛分区是干净的：
  冠军组 Wk1–5、保级组 Wk1–5 每周每队恰好出场一次。
- 日期交错不是错误：HJK–SJK 2022-09-18 属系列 Wk3（即 25 轮），是提前踢但保留原系列周次，
  与 2023 季“延期场保留原轮次”的先例一致。
- **限定**：FBref 与 WorldFootball 都不是官方源，所以本轮**没有**把这 30 场重新验证为官方 KIERROS；
  保留是按任务 §1“无更强反证不覆盖”，不是官方背书。`official_round_source` 已如实写为
  “-004（WorldFootball 分组）保留、本轮未重新验证为官方”。

## 4. 赛制结论（有源，不猜）

- **常规赛：双循环。** 12 队，每队 22 场（Wikipedia 常规赛表 Pld 均为 22），
  结果矩阵中每对球队主客两个方向各有一场（例 Haka–HJK 0–3、HJK–Haka 4–1），
  合计 12×22/2 = **132 场**。
- **系列赛：单循环（两组各 5 轮），不是双循环。** 常规赛后前 6 名进冠军组、后 6 名进保级组
  （Wikipedia 常规赛表第 1–6 名标注 Championship round、第 7–12 名标注 Relegation round）；
  两组表最终 Pld 均为 27 = 22 + 5；FBref 系列 Wk1–5 每组每周 3 场、每队每周 1 场，
  合计每组 15 场、两组 **30 场**。
- **总数：132 + 30 = 162 场，每队 27 场。** 所谓“不是标准双循环 132 场”，
  是因为 2022 赛季在双循环常规赛后加了单循环系列赛，不是常规赛本身少踢。
- **不要套用现行赛制**：Wikipedia Veikkausliiga 总条目现行描述
  （保级组单循环 27 场、冠军组双循环 32 场）是现行赛季口径，与 2022 年的 27 场不符，
  本报告不采用。
- 赛制源：Wikipedia 2022 赛季页常规赛表、冠军组表、保级组表 + FBref 系列 Wk 分区；
  官方赛制文件本轮未检索到（见 §8），故赛制结论标注为二级源支撑、非官方文件原文。

## 5. 场馆：场次级确认 155 场 + 易地 7 场；官方易地声明 0 份

- 赛季主场映射（Wikipedia 赛季球场表）与 -004 完全一致，12 队 11 座球场
  （HJK 与 HIFK 共用 Bolt Arena，赫尔辛基）：
  AC Oulu–Raatti Stadion（Oulu）、Haka–Tehtaan kenttä（Valkeakoski）、
  Honka–Tapiolan Urheilupuisto（Espoo）、Inter–Veritas Stadion（Turku）、
  Lahti–Lahden Stadion（Lahti）、HJK/HIFK–Bolt Arena（Helsinki）、
  IFK Mariehamn–Wiklöf Holding Arena（Mariehamn）、Ilves–Tampere Stadium（Tampere）、
  KuPS–Savon Sanomat Areena（Kuopio）、SJK–OmaSP Stadion（Seinäjoki）、VPS–Hietalahti（Vaasa）。
- 别名归一（同一球场不同名，不算冲突，依据 -004 venue-coords.json 备注）：
  Lemonsoft Stadion = Hietalahti = Elisa Stadion（VPS）、Väre Areena = Savon Sanomat Areena（KuPS）、
  Ratinan Stadion = Tampere Stadium（Ilves）、Raatin stadion = Raatti Stadion（Oulu）、
  Wiklöf Holding Arena konstgräs = Wiklöf Holding Arena（Mariehamn）。
- **confirmed 155 场**：FBref 当场场馆经别名归一后与赛季主场映射一致
  （二级源场次级 + 赛季映射双重一致；**不是**官方比赛页确认，行内已注明）。
- **moved 7 场**（全部在 4 月，天然草未就绪期的人工草易地模式）：
  2022-04-07 Honka–Haka → Bolt Arena（赫尔辛基；Forebet 独立列出 Bolt Arena，第二源佐证）；
  2022-04-08 Lahti–VPS → Lemonsoft Stadion（Vaasa）⚠；
  2022-04-09 Inter–Oulu → Tehtaan kenttä（Valkeakoski）⚠；
  2022-04-09 Ilves–KuPS → Tehtaan kenttä（Valkeakoski）；
  2022-04-17 Inter–Haka → Bolt Arena（赫尔辛基）；
  2022-04-17 Oulu–Ilves → Lemonsoft Stadion（Vaasa）⚠；
  2022-04-25 Honka–SJK → Bolt Arena（赫尔辛基）。
  ⚠ = implausible 标记：主队在对方/第三方主场踢球，仅 FBref 单源场馆列支撑，
  未检索到官方易地声明，需主代理真浏览器复核官方比赛页后再定。
  7 场的旧映射全部保留在 `venue_candidates` 中，未被删除。
- 坐标：全部沿用 -004 venue-coords.json（地理编码结果，注明出处），
  易地球场坐标按当场球场取（Bolt Arena 60.1875, 24.92209；Tehtaan kenttä 61.2665, 24.02617；
  Lemonsoft Stadion 按 Elisa Stadion 63.08551, 21.62855，同一球场）。
  场馆时区一律 Europe/Helsinki。
- **场馆场次级确认数汇报口径**：match 级取值 162/162（155 confirmed + 7 moved），
  其中官方比赛页/俱乐部易地声明确认 **0 场**——这是本轮最大缺口之一。

## 6. 俱乐部官方身份（每行主客队各一，见 JSONL 内 `home_club_identity` / `away_club_identity`）

- 有源事实（Wikipedia 2022 赛季页）：
  - VPS：以 2021 Ykkönen 冠军身份升入 2022（缺席两年后回归）；KTP 2021 垫底降级离场。
  - HIFK：2022 季末降级至 Ykkönen（赛季信息框 + 保级组表 R 标注）。
  - 分组：冠军组 HJK、KuPS、Honka、Haka、Inter、SJK；保级组 AC Oulu、Ilves、IFK Mariehamn、VPS、Lahti、HIFK。
  - HJK 建队 1907 年（本轮检索 Wikipedia HJK 页确认；全名 Helsingin Jalkapalloklubi）。
- **Helsingfors IFK ≠ IFK Mariehamn**：前者赫尔辛基、Bolt Arena；后者 Mariehamn、Wiklöf Holding Arena，
  赛季球场表即分列两行，绝不合并。两队在 2022 年各 27 场、交手记录分开。
- 其余 11 队建队/沿革年、更名、前身、合并：**本轮未逐队核实，一律 null +“本轮未核实，不猜”**，
  不把训练知识写成事实。升降级除 VPS/HIFK/KTP 三项外亦无新增断言。

## 7. 未覆盖与冲突清单

- 未覆盖（official_round）：132 场常规赛（§3）；meeting_number：162 场全部（无权威定义源，
  不从日期顺序、球队出现次数、比分、积分榜、盘口推断）。
- 冲突/存疑：
  1. 开球时间：-004 整列与本地时间差 2 小时（已覆盖修正，§2）。
  2. 场馆易地 7 场，其中 3 场 implausible 标记（§5）。
  3. -004 系列赛 23–27 的“官方”标签源自 WorldFootball 分组，本轮未获官方源复核（保留 + 限定，§3）。
  4. FBref Wk 不能当轮次（§3）——下游绝不能把 `fbref_week_bucket` 当 official_round 用。
  5. 范围外附加赛未入表：FBref/Wikipedia 所列欧会杯附加赛（Inter–VPS、SJK–Oulu、Oulu–VPS、
     VPS–Haka 两回合）及 Lahti–TPS 升降级附加赛两回合均不在 162 联赛场次内，未加行、不计入计数。
- 身份冲突：无。-004 的 162 组（日期、主客队）与 FBref 全表、WorldFootball 2022-09 赛程块逐项一致；
  每队总出场 27 场、主场 13/14 场、无重复（日期+主客队）——均经脚本断言。

## 8. 尝试过但失败 / 受限的源（供主代理真浏览器跟进）

| 源 | 本轮结果 | 跟进建议 |
|---|---|---|
| veikkausliiga.com 官方存档 | 检索未返回可用存档链接；-004 记存档 HTTP 500 | 主代理真浏览器 / 官方 API 跟进；拿到 KIERROS 分组后方可把 132 场标 official |
| Tulospalvelu（tulospalvelu.palloliitto.fi） | 检索未返回深链；JS 应用，文本层不可读；-004 记其 API 被 Cloudflare 拦截 | 同上；不要再派文本层子代理撞 JS 门 |
| Soccerway ROUND N 分组 | 常规赛页与 Results 页文本层只剩导航（JS 门），分组不可读。已确认的待查 URL：`https://us.soccerway.com/national/finland/veikkausliiga/2022/regular-season/r66785/`、`https://us.soccerway.com/finland/veikkausliiga-2022/results/` | 主代理真浏览器任务读取 ROUND 分组；这是常规赛轮次最可行的非官方交叉源 |
| WorldFootball matchday 分页 | 文本层本次返回了缓存赛程块（2025-06-02 抓取），标题 “6. Round” 内含 2022-09-01–11 的 12 场比赛，横跨 FBref Wk21 + Wk22——**实证分页是展示分块、不是官方 KIERROS**；故不用它填官方轮次；其时间列亦佐证 §2 的时区结论 | 不再用 WorldFootball 分页标轮次；仅作身份交叉核对 |
| FBref 赛程表 | 全表可读（2026-09-01 抓取）；时间、场馆、系列赛 Wk 可用；常规赛 Wk 不可用作轮次（§3） | 已用尽文本层价值 |
| Wikipedia 2022 赛季页 | 全文可读（2026-08-30 抓取）；球场表、常规赛/系列赛表、附加赛 EEST 时间可用 | 二级源；赛制与身份以此为准、官方文件待补 |
| Sky Sports / Forebet | 仅作时间锚点（2 场）与 Honka–Haka 场馆佐证（1 场） | 不作为轮次源 |

## 9. Provenance 铁律执行情况

- 每个非 null 字段均附 `provenance`（字段级来源对象：source_url、final_url、
  retrieved_at `2026-10-28T16:16:00+08:00`、field_locator、source_name）。
- `source_sha256` **全部 null**：本轮全部为文本层抓取、无字节下载，
  逐行注明“文本层、无字节”；**没有复用 -004 的描述符哈希冒充源证据哈希**，
  -004 的旧时间、旧轮次值仅作为“旧值”字段保留，不作为证据。
- 坐标出处：-004 venue-coords.json（地理编码结果），JSONL 内 `venue_coords_source` 逐行注明。
- 文本层页面自身的抓取时间与本轮检索时间不同处（如 FBref 2026-09-01、Wikipedia 2026-08-30、
  WorldFootball 2025-06-02 缓存），已在 §8 与行内 locator 中区分，不混为“今日实测”。

## 10. 交付文件

- `season_2022.jsonl`：162 行，每行含任务要求的全部字段 + `round_non_official`、
  `fbref_week_bucket`、`series_week_fbref`、`kickoff_004_old`、`kickoff_change`、
  `kickoff_timezone_method`、`venue_verified_city`、`venue_coords_source` 等辅助字段。
- 本说明 `season_2022_notes.md`。
- 构建脚本在 `/tmp/build2022.py`（临时稿，不在交付目录内）；交付目录内其他赛季文件未动。
