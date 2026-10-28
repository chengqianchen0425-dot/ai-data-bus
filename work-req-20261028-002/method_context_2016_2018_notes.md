# Veikkausliiga 2016–2018 · 赛前背景证据说明（req-20261028-002 A 路）

交付：`method_context_2016_2018.jsonl`（594 行，每行一个场次）＋本文件。
范围：仅芬兰顶级联赛 Veikkausliiga 2016、2017、2018 三季；芬兰杯、欧战、友谊赛、其他级别一律排除。
只含赛前事实：不含比分、赛果、积分榜、观众数、裁判、盘口、预测、分析模型输出（全文扫描：比分形字符串 0 命中、禁字段键 0 个）。

## 0. 关键前提：请求方 CSV 不可用（未闭合项）

- 请求方指定的身份 CSV（Windows 路径 `D:\奇门斗数\work\veikkausliiga-fin-20260927\...method_context_request_fixtures_20261028.csv`，
  SHA-256 `9de8b8fac5fcdebbc51e1df99f9a5fe329e3149f3deacc2dfcc4105cd9a4c093`）在本 VM 上不存在、无法读取。
- 因此本交付**绝不声称**与该 CSV 精确对应。行键为 `season|match_date|home_team|away_team`
  （与 req-20261006-004 的 fixture_key 格式一致），每行 `csv_join_status="csv_unavailable_on_this_vm_derived_from_public_schedule"`。
- 最终 CSV 精确联结是**未解决项**，需请求方上传 CSV 或确认派生集后才能闭合，不许伪造对应关系。
- 本单 2016–2018 赛季不在 req-20261006-004 覆盖内；同目录上一轮文件（2022–2026 等）仅作背景参考，未复制任何行。

## 1. 按赛季计数

| 赛季 | expected | discovered | complete | partial | conflict | unavailable | blocked | missing |
|---|---|---|---|---|---|---|---|---|
| 2016 | 198 | 198 | 165 | 20 | 13 | 0 | 0 | 0 |
| 2017 | 198 | 198 | 86 | 10 | 102 | 0 | 0 | 0 |
| 2018 | 198 | 198 | 122 | 15 | 61 | 0 | 0 | 0 |
| 合计 | 594 | 594 | 373 | 45 | 176 | 0 | 0 | 0 |

- expected＝12 队 × 33 轮 ÷ 2＝198 场/季；三季去重后唯一数均为 198，偏差 0。
- 日期范围：2016-04-02～2016-10-23；2017-04-05～2017-10-28；2018-04-07～2018-10-27。
- 每季核对：每队 33 场、66 个球队对各交手恰好 3 次、FBref Wk 1–33 每轮恰好 6 行、Venue 空白 0、Time 缺失 0。
- 行状态定义：`conflict`＝轮次标签冲突行（见 §4）；`partial`＝场馆身份未完全解析（neutral 或无坐标）；
  `complete`＝场馆已确认/已判定 moved 且有坐标；`unavailable`＝Venue/Time 空白（本单为 0）；
  `blocked`＝页面不可读致整行缺失（本单为 0；FBref 字节被拦截只影响 provenance，不影响行本身）。

## 2. 赛制结论：不是双循环（double round robin）

**结论：2016、2017、2018 三季均为 33 轮结构（每队 33 场、每对球队交手 3 次），不是双循环。**

依据（三项可观测结构，缺一不可；赛季页未找到 "triple round-robin" 的散文原句，结论建立在结构上）：

1. 维基赛季页 Results 一节结构：三季页面均分为 "Matches 1–22" 与 "Matches 23–33" 两段
   （22 场＝双循环打完后的分段点，之后再打 11 轮；证据文件 `evidence/wiki_2016.html`、
   `evidence/wiki_2017.html`、`evidence/wiki_2018.html`，SHA-256 见 §6）。
2. FBref Wk 取值 1–33，每轮 6 场（见 §1 核对）。
3. 每队 33 场、每对球队 3 次交手（见 §1 核对）。
4. 每队 33 场是观测计数，不用于推断 meeting_number（见 §3）。

## 3. meeting_number：可填数 0（全季全部 null）

- **可填数：0 / 594。** 全部行 `meeting_number=null`。
- 理由（统一）：没有权威源明确定义 meeting_number；从日期顺序、CSV 顺序、球队出现次数、比分、
  积分榜、盘口推断均被任务明令禁止。33 轮结构只说明"第几次交手"存在 1–3 的可能取值，
  不等于任何一场的 meeting_number 定义——不猜。
- 尝试源：FBref 赛程页（只有 Wk，无 meeting_number 定义）、维基赛季页（只有 Matches 1–22/23–33 分段，
  无 meeting_number 定义）。联赛官方轮次记录的交叉核对属待办（见 §7）。

## 4. 轮次标签冲突（official_round 一律 FBref Wk 原值，绝不改写）

`official_round` 写为 `Matchweek N (FBref)`，N 为 FBref Wk 原值。**Fixture 集合完整，但 FBref 的 Wk 标签
在 2017/2018 季不可直接当作联赛官方轮次。** 两类冲突要区分：

### 4.1 2016：仅日期顺序异常（13 行；Wk 组本身是合格轮次）

- 每组 Wk 恰好 12 支球队各出现一次，轮次构成合格；异常只是个别行日期落在别轮的日期簇之外
  （补赛/提前场次式呈现），原值保留。
- A 组 Wk 33（6 行）：2016-04-02 HJK–IFK Mariehamn、2016-04-02 PK–35–RoPS（赛季首日即标 33）、
  2016-07-02 Ilves–SJK、2016-07-03 Lahti–KuPS、2016-07-03 Kemi Kings–Helsinki IFK、2016-07-04 Inter–VPS。
- B 组（7 行）：2016-06-23 Kemi–RoPS（Wk 10）、2016-06-28 VPS–Ilves（Wk 2）、2016-06-28 Inter–SJK（Wk 16）、
  2016-06-29 Lahti–Kemi（Wk 2）、2016-07-13 VPS–PK–35（Wk 14）、2016-08-24 Ilves–RoPS（Wk 3）、
  2016-08-24 HJK–PK–35（Wk 28）。

### 4.2 2017：Wk 1–17 的轮次构成被破坏（102 行）

- Wk 1–17 共 17 组、每组 6 行，但组内球队出现重复、另有球队缺席（例如 Wk 1：VPS、SJK、Lahti 各出现两次，
  Inter、KuPS、RoPS 缺席）。经对 FBref 原页抽查复核，转录与原页一致——是源数据标签问题，不是转录错误。
- 因此 Wk 1–17 全部 102 行标 `round_label_conflict=true`（含分季代理列出的 12 行日期顺序异常，
  均落在这些周内，已合并、不重复计数）。Wk 18–33 构成合格。
- 2017 代理另注：Wk 1 中 Lahti 出现两次、Wk 12 中 KuPS 出现两次，均为上述构成破坏的一部分，原值保留。

### 4.3 2018：Wk 3–10、19–20 构成被破坏＋4 行呈现异常（61 行）

- 构成破坏周：Wk 3、4、5、6、7、8、9、10、19、20（10 组 × 6 行＝60 行）。
- 呈现异常（4 行，其中 3 行已落在破坏周内，不重复计数；仅 Wk 23 行新增）：
  Wk 8 2018-05-29 HJK–SJK（页内出现在 Wk 11 之后）、Wk 3 2018-08-29 Ilves–IFK Mariehamn（滞后约 4 个月）、
  Wk 8 2018-09-26 Inter–Lahti、Wk 23 2018-09-26 Ilves–HJK（同日、页内在 Wk 30 之前）。
- 合计冲突行 61 行（60＋1）。

## 5. 开球时间口径

- `kickoff_local`＝FBref Time 列的第一个时刻（全季 594 行均有，无缺失）。
- `kickoff_timezone`、`kickoff_utc` 一律 null：FBref 未公布 Time 列的时区名或 UTC 偏移，不做
  Europe/Helsinki 换算断言、不生成 UTC 值。
- 2016 抓取文本中 Time 单元格曾渲染为 "18:30 (08:30)" 形式：括号内第二个时刻是抓取方时区的换算值，
  不是源字段，绝不记录。抽查一致性（仅作支撑说明，不作源断言）：若第一个时刻为赫尔辛基夏令时（UTC+3），
  则 18:30→15:30 UTC→08:30 PDT、16:00→13:00 UTC→06:00 PDT，与括号值吻合；但源未声明时区，故字段仍置 null。

## 6. 场馆：场次级确认数与解析表

场馆状态计数（按行）：

| 赛季 | confirmed | moved | neutral | 合计 |
|---|---|---|---|---|
| 2016 | 152 | 22 | 24 | 198 |
| 2017 | 175 | 9 | 14 | 198 |
| 2018 | 173 | 4 | 21 | 198 |
| 合计 | 500 | 35 | 59 | 594 |

- `confirmed`＝场次级 FBref 场馆名经场馆文章解析出城市与坐标，且与俱乐部赛季 listed 主场为同一物理场地
  （含已确认的赞助更名：Sonera Stadium＝Telia 5G -areena＝Bolt Arena；Hietalahti Stadium＝Elisa Stadion）。
- `moved`＝场次级场馆与赛季 listed 主场为不同物理场地（场次级证据在先，listed 主场只是候选对照）。
- `neutral`＝场馆身份未完全解析（同综合体不同球场、别名未确认、无坐标来源），不做确认、不做 moved 断言。
- **俱乐部默认主场或赛季场馆表本身不是场次级确认**：没有本场直接证据时 verified 场馆置 null、状态标
  unavailable/blocked——本单 FBref 每场均有 Venue 原文，故无 unavailable 行；但 listed 主场从未被用作
  场次级顶替（moved/neutral 行的 canonical 均来自场次级场馆名本身的解析）。

### 6.1 场馆解析表（25 个 FBref distinct 场馆名）

| FBref 场馆名 | Canonical | 城市 | 坐标（WGS84） | 时区 | 状态驱动 |
|---|---|---|---|---|---|
| Telia 5G -areena | Töölö Football Stadium (Bolt Arena) | Helsinki | 60.1875, 24.9225 | Europe/Helsinki | 坐标 API（Bolt Arena 重定向） |
| Veritas Stadion | Kupittaa Football Stadium (Veritas Stadion) | Turku | 60.44277778, 22.29166667 | Europe/Helsinki | 坐标 API |
| Wiklöf Holding Arena | Wiklöf Holding Arena | Mariehamn | 60.10222222, 19.93527778 | Europe/Mariehamn | 坐标 API |
| Wiklöf Holding Arena konstgräs | Wiklöf Holding Arena（综合体；konstgräs＝人工草球场） | Mariehamn | 同上（综合体级） | Europe/Mariehamn | 球场级坐标未单列→neutral |
| Tammelan Stadion | Tammela Stadium | Tampere | 61.5003, 23.7853 | Europe/Helsinki | 坐标 API |
| Ratinan Stadion | Tampere Stadium (Ratina Stadium) | Tampere | 61.4925, 23.76416667 | Europe/Helsinki | 坐标 API |
| Savon Sanomat Areena | Kuopio Football Stadium | Kuopio | 62.88463, 27.6718 | Europe/Helsinki | 坐标 API |
| Väinölänniemen stadion | Väinölänniemen stadion | Kuopio | 62.88277778, 27.70055556 | Europe/Helsinki | 芬兰语维基坐标 API |
| Myyrmäen jalkapallostadion | Myyrmäen jalkapallostadion | Vantaa | 60.2621, 24.83818333 | Europe/Helsinki | 坐标 API |
| Rovaniemen Keskuskenttä | Rovaniemen keskuskenttä | Rovaniemi | 66.5, 25.72166667 | Europe/Helsinki | 芬兰语维基坐标 API |
| Raatin stadion | Raatti Stadium | Oulu | 65.01972222, 25.46583333 | Europe/Helsinki | 坐标 API |
| Sauvosaaren urheilupuisto | Sauvosaaren urheilupuisto | Kemi | 65.72972222, 24.56055556 | Europe/Helsinki | 芬兰语维基坐标 API（英文条目 65.729778, 24.560583 一致） |
| Sauvosaaren Takakenttä N | Sauvosaaren Takakenttä N（Sauvosaari 综合体后场） | Kemi | null | Europe/Helsinki | 综合体级城市、无球场级坐标→neutral |
| Kisapuisto | Kisapuisto（拉赫蒂体育公园） | Lahti | null | Europe/Helsinki | 无拉赫蒂 Kisapuisto 专条→neutral（见陷阱 1） |
| Lahden Stadion | Lahti Stadium | Lahti | 60.98305556, 25.63416667 | Europe/Helsinki | 坐标 API |
| Kaarlen kenttä | Kaarlen kenttä | Vaasa | 63.08277778, 21.64111111 | Europe/Helsinki | 坐标 API |
| Elisa Stadion | Hietalahti Stadium (Elisa Stadion) | Vaasa | 63.08527778, 21.62777778 | Europe/Helsinki | 重定向确认更名 |
| Jouppilanvuoren tekonurmi | Jouppilanvuoren tekonurmi | Seinäjoki | 62.78, 22.81194444 | Europe/Helsinki | 芬兰语维基坐标 API |
| Seinäjoen keskuskenttä | Seinäjoen keskuskenttä | Seinäjoki | 62.78194444, 22.85111111 | Europe/Helsinki | 坐标 API |
| OmaSP Stadion | OmaSP Stadion | Seinäjoki | 62.77861, 22.81472 | Europe/Helsinki | 坐标 API |
| Harjun stadion | Harjun stadion | Jyväskylä | 62.24472222, 25.74083333 | Europe/Helsinki | 坐标 API |
| Vaajakosken urheilukenttä | Vaajakosken urheilukenttä | Jyväskylä（Vaajakoski 区） | null | Europe/Helsinki | 无专条、无坐标；城市为 JJK 主场城市＋区属→neutral（moved 判定见注） |
| Tapiolan Urheilupuisto | Tapiolan urheilupuisto | Espoo | 60.1791, 24.7813 | Europe/Helsinki | 坐标 API |
| Paavo Nurmi Stadion | Paavo Nurmi Stadium | Turku | 60.4425, 22.26083333 | Europe/Helsinki | 坐标 API |
| City Sport Areena | City Sport Areena | Kemi | null | Europe/Helsinki | 城市有源、坐标无源（见 §6.3） |

- 时区说明：芬兰本土场馆为 Europe/Helsinki；Mariehamn（Åland）场馆为 Europe/Mariehamn
  （IANA 中 Åland 的独立区名，现行规则与 Europe/Helsinki 相同）。时区归属按场馆所在城市/地区判定，
  非按球队判定。
- Vaajakosken urheilukenttä 与 City Sport Areena 在行级判定为 moved（与 listed 主场为不同命名场地），
  但坐标为 null，故这些行计入 partial（见 §1 定义），不计入 complete。

### 6.2 moved 行一览（35 行，场次级场馆 ≠ 赛季 listed 主场）

- Kemi Kings 早季主场外移：2016-04-09、2016-04-17 对 SJK/IFK Mariehamn 在 Rovaniemen Keskuskenttä；
  2017-04-08 对 Helsinki IFK 在 Rovaniemen Keskuskenttä（Sauvosaari 赛季初不可用时的常见安排，属场次级原文）。
- Kemi Kings 在 City Sport Areena（Kemi）：2017-04-22 对 SJK、2017-05-06 对 KuPS。
- Raatin stadion（Oulu）共 5 行：Kemi Kings 主场 4 行（2016-04-29 对 HJK、2016-05-07 对 Ilves、
  2018-05-07 对 HJK、2018-05-13 对 TPS）＋ RoPS 主场 1 行（2016-05-13 对 KuPS，罗瓦涅米球队在奥卢的
  printed 场地，原因未核实，原值保留）。
- SJK 早季场地：Jouppilanvuoren tekonurmi（2016 季 2 行）、Seinäjoen keskuskenttä（2016 季 5 行），
  对照 listed 主场 OmaSP Stadion（2016 季中启用）。
- KuPS 在 Väinölänniemen stadion（2016 季 1 行）对照 Savon Sanomat Areena。
- Ilves 在 Ratinan Stadion（2017 季 3 行）对照 Tammelan Stadion。
- VPS 在 Kaarlen kenttä（2016 季 5 行）对照 Hietalahti/Elisa Stadion。
- JJK 在 Vaajakosken urheilukenttä（2017 季 3 行）对照 Harjun stadion。
- TPS 在 Paavo Nurmi Stadion（2018 季 2 行）对照 Veritas Stadion。
- 2016-08-26/27 三行跨城 printed 场馆（原因未核实，原值保留，moved＋附注）：
  2016-08-26 PK–35–Kemi Kings 在 Telia 5G -areena；2016-08-27 Helsinki IFK–SJK 在 Veritas Stadion（图尔库）；
  2016-08-27 Inter Turku–Ilves 在 Myyrmäen jalkapallostadion（万塔）。
  另有一行同类：2016-06-28 VPS–Ilves 在 Lahden Stadion（拉赫蒂），同时为 Wk 2 日期顺序异常行。
- 其余 moved 行均为上述模式的重复场次（同一球队在同一替代场地的多场比赛）。

### 6.3 坐标/身份未解析清单（neutral 行的来源）

- Kisapuisto（23 行，拉赫蒂主场）：城市 Lahti（主场俱乐部城市＋公园名），坐标 null。
- Sauvosaaren Takakenttä N（24 行，Kemi 后场）：城市 Kemi（综合体级），坐标 null。
- Wiklöf Holding Arena konstgräs（1 行）：坐标为综合体级，球场级未单列。
- Lahden Stadion 对照 2016 listed 主场 "Lahden kisapuisto"（11 行）：两者均指向 Kisapuisto 区域，
  但无场馆文章确认别名，故既不断言 confirmed、也不断言 moved，标 neutral。
- City Sport Areena（2 行）：城市 Kemi 有源（Merilappi United 场馆表 "City Sport Areena, Kemi"；
  SoccerPunter 对 2017 PS Kemi–SJK 一场的场馆标注 "City Sport Areena (Kemi)"），坐标无源。

### 6.4 解析时避开的两个陷阱

1. **Kisapuisto 同名陷阱**：英文维基 "Kisapuisto" 条目坐标（61.0577, 28.2288）位于拉彭兰塔（Lappeenranta），
   不是拉赫蒂——已明确弃用，未写入任何行。
2. **Elisa Stadion 误匹配**：opensearch 初筛曾返回瑞士 "Eisstadion Davos"（46.7986, 9.8263）——已弃用；
   最终用精确标题 "Elisa Stadion" 查坐标 API，得重定向至 Hietalahti Stadium（63.0852, 21.6277，与 VPS
   赛季页位置图一致），确认更名关系。

## 7. 俱乐部官方身份（15 家，FBref 标签 →  canonical）

| FBref 标签 | Canonical | Founded（信息框原文） | 赛季 listed 主场（候选对照） |
|---|---|---|---|
| HJK Helsinki | Helsingin Jalkapalloklubi (HJK) | 19 June 1907 | Sonera Stadium（2016）/ Telia 5G -areena（2017–2018） |
| Helsinki IFK | HIFK Fotboll | 1897 | 同上（与 HJK 共用赫尔辛基主场） |
| IFK Mariehamn | IFK Mariehamn | 1919 | Wiklöf Holding Arena |
| Ilves | FC Ilves | 1931 | Tammelan Stadion |
| Inter Turku | FC Inter Turku | 1990 | Veritas Stadion |
| Kemi Kings | Palloseura Kemi Kings (PS Kemi) | 1999（见 §7.1） | Sauvosaaren Urheilupuisto |
| KuPS | Kuopion Palloseura | 1923 | Savon Sanomat Areena |
| Lahti | FC Lahti | 1996 | Lahden kisapuisto（2016）/ Lahden Stadion（2017–2018） |
| PK–35 | PK-35 Vantaa (men) | 2008（沿革见 §7.2） | Myyrmäen jalkapallostadion |
| RoPS | Rovaniemen Palloseura | 1950 | Rovaniemen keskuskenttä |
| SJK | Seinäjoen Jalkapallokerho | 5 November 2007（合并时代俱乐部） | OmaSP Stadion |
| VPS | Vaasan Palloseura | 1924 | Hietalahti Stadium（2016）/ Elisa Stadion（2017–2018，同场更名） |
| JJK（2017） | Jyväskylän Jalkapalloklubi | 2000 (1992)（原文照抄，未解读） | Harjun stadion |
| FC Honka（2018） | FC Honka | 1957 | Tapiolan Urheilupuisto |
| TPS（2018） | Turun Palloseura | 1922 | Veritas Stadion（与 Inter 共用） |

- `competition_entry_year` 的处理：任务表述"（该季）"存在歧义，本交付同时给两层——
  `season_entry.type`（promoted_champions / promoted_playoff / continuing）与 `entry_season`
  （仅升级/附加赛胜出的俱乐部填入该季年份；其余填 null 并注明"首个顶级赛季年份未从所用源确立"，
  不把"参赛季年"等同于"首次顶级年份"）。行级 `season_entry` 字段即此结构。
- 升降级事实（维基赛季页 Teams 一节，均有字节证据）：
  - 2016 季进入：PS Kemi（Ykkönen 2015 冠军升级）；2015 垫底 FF Jaro 降级；第 11 名 KTP 附加赛 3–2 负于 PK-35 Vantaa 失去席位。
  - 2017 季进入：JJK（Ykkönen 2016 冠军升级）；2016 垫底 PK-35 Vantaa 降级；第 11 名 Inter 附加赛 2–0 胜 TPS 保级。
  - 2018 季进入：TPS（Ykkönen 2017 冠军升级）、FC Honka（附加赛胜第 11 名 HIFK）；2017 垫底 JJK 降级。
  - 2018 季后降级：未用 2019 季页面核实，本交付不写。
- 更名/别名：赫尔辛基 Sonera Stadium→Telia 5G -areena（2016→2017 赛季页 listed 主场名变化＋场馆重定向一致）；
  瓦萨 Hietalahti Stadium→Elisa Stadion（同上）；拉赫蒂 Lahden kisapuisto→Lahden Stadion（赛季页名变化，
  但与 FBref 场次级 "Kisapuisto" 的别名关系未确认，见 §6.3）。

### 7.1 PS Kemi 身份冲突：已解决，不合并数字

- 词条标题 "Palloseura Kemi Kings" 重定向至 "Kemin Palloseura"（证据 `evidence/club_PSKemiKings.html`），
  该文信息框写 Kemin Palloseura、Founded 1932、主场 Sauvosaaren Urheilupuisto；同文历史一节写俱乐部
  于 1999-10-21 成立，Kemi Kings 由 KePS、KPT-85 与 Visan Pallo 合并而成。
- 解决：2016–2018 参赛俱乐部为 **Palloseura Kemi Kings，Founded 1999**——依据为 Kemi City FC 条目中的
  PS Kemi Kings 信息框（Founded 1999）＋历史正文（established on October 21, 1999，由三家合并），
  证据 `evidence/club_KemiCityFC.html`。1932 是前身 KePS 的数字，不是本俱乐部的数字，**绝不合并为单一数字**，
  行内 `lineage_note` 完整保留这一区分；原重定向文件作为"陷阱证据"附在 provenance 中。
- 后续沿革（仅作身份注脚，不属本季事实）：母公司 2019-02 停运；新俱乐部 Kemi City FC 2019 年初成立；
  2022-02 恢复 PS Kemi 名。

### 7.2 PK-35 身份区分：绝不合并

- 2016 参赛的是 **PK-35 Vantaa（男子队）**：沿革 as Viipurin Pallokerho 1935、as Pallokerho-35 1948、
  as PK-35 Vantaa 2008；2016 年解散；主场 Myyrmäen jalkapallostadion（万塔）；坐标 60.2621, 24.8382。
- 现存赫尔辛基的 PK-35（男子队）是另一家俱乐部；维基标题 "PK-35" 本身只是消歧页（wikitext 仅 789 字符）。
- 行内 founded_year 取 2008（as PK-35 Vantaa），并完整保留 1935/1948 沿革链。

### 7.3 JJK founded 歧义：保留原文，不解读

- 信息框原文 "Founded 2000 (1992)" 照抄进 `founded_detail`，`founded_year` 置 null，不猜括号含义。
  该歧义不影响行状态（身份已映射、城市/场馆已解析），仅在俱乐部字段中标注。

## 8. Provenance 铁律执行情况

- **字节哈希（已实际下载并计算，证据在 `evidence/`）：**
  - 维基三季赛季页：`wiki_2016.html`（468,235 字节，SHA-256
    `f9813cf559773cda1665cc7177c625d22b4a024f7e6783a9b44c691b326f7025`）、
    `wiki_2017.html`（447,803 字节，`462e60e9942bf04d03fe1053bee703c3d7fa2c630146221b29512c93abf63efa`）、
    `wiki_2018.html`（410,718 字节，`95a918bde0b5069ae0e302605ae3e91c1f5f79b8802620822f5f8ecedc945970`）。
  - 15 家俱乐部文章：`evidence/club_articles.json`（文件＋SHA-256 索引）＋ `evidence/club_KemiCityFC.html`
    （SHA-256 `e2733296abea83575999546245bdc1c319744c368e16fb3db0f8da09357cfb7f`）＋
    `evidence/wikitext_PK35_Vantaa_men.json`（SHA-256 `27b913882e2fad1b7fc2c3be7b4a00dd7d819ee2dce616ba0366031e1cf0c016`）。
  - 场馆坐标 API 响应：`evidence/stadium_coords_*.json`（英文版）＋ `evidence/stadium_coords_fi_*.json`
    （芬兰语版），索引 `evidence/stadium_coords_evidence.json`（文件＋SHA-256）。行级 stadium provenance
    指向对应响应文件；542 行有坐标证据哈希（含 konstgräs 行，其哈希指向主竞技场综合体的坐标响应，
    行内已注明为综合体级），52 行（Kisapuisto 23、Takakenttä N 24、Vaajakoski 3、City Sport Areena 2）
    无坐标证据、哈希为 null 并注明原因。
- **字节哈希缺失（诚实置 null，绝不冒充）：**
  - FBref 全部 594 行：`provenance.fixture.source_sha256=null`。原因：curl 直连返回 000；
    scrapling（无代理）超时、加代理后 HTTP 403；curl_cffi 以 chrome120/chrome131 模拟仍为 Cloudflare
    "Just a moment..." 403（约 6,200 字节挑战页）。行一律走浏览器文本层转录，**挑战页哈希绝不用作行哈希**。
    这是本单最大障碍（见 §9）。
  - 上一单 req-20261006-004 的 source_sha256 是 provenance 描述符的哈希——本单未沿用该做法；
    凡本单声称"字节哈希"处均为真实下载字节的 SHA-256。
- `retrieved_at`：FBref 行用分季代理的抓取时间（2016：2026-10-28T16:26:16+08:00；
  2017：2026-10-28T16:26:00+08:00；2018：2026-10-28T16:25:49+08:00）；维基/俱乐部/场馆证据用文件
  mtime（+08:00）作为下载时间近似值。
- 每行 provenance 结构：fixture（FBref 文本层）＋ season_format（维基赛季页）＋ club_home ＋ club_away ＋
  stadium（坐标 API 或 null＋原因）。`field_locator` 逐项标明列/章节/响应字段。

## 9. 最大障碍与未覆盖/冲突清单

### 最大障碍

**FBref 源字节被 Cloudflare 拦截**：三路独立证实（curl 000、scrapling 403、curl_cffi 模拟 Chrome 仍 403），
全部 594 行 FBref 证据只能是浏览器文本层转录，无源字节哈希。比分/赛果列已在转录时删除，
但行级 provenance 永远缺一块——后续若需字节级审计，必须由有实时浏览器/合规下载通道的一方重抓，
本单子代理无此能力，不得谎称已访问。

### 未覆盖清单（pending_work）

1. 联赛官方轮次交叉核对：FBref Wk 标签在 2017（Wk 1–17）、2018（Wk 3–10、19–20）不可直接当作官方轮次；
   需联赛官方（Veikkausliiga / Palloliitto）轮次记录逐场核对后才能把 `official_round` 从 "Matchweek N (FBref)"
   升级为官方轮次；本单不擅自改写。
2. 场馆坐标补齐：Kisapuisto（拉赫蒂）、Sauvosaaren Takakenttä N、Vaajakosken urheilukenttä、
   City Sport Areena（4 个名、52 行）无坐标源；Wiklöf konstgräs 仅综合体级坐标。
3. 请求方 CSV 精确联结（见 §0）：需请求方上传 CSV 或确认派生集。
4. 2018 季后升降级：未核实，不写。
5. JJK founded 括号含义：未解读，保留原文。

### 冲突清单（已保留，未静默覆盖）

- 轮次标签冲突 176 行（2016：13；2017：102；2018：61），见 §4。
- PS Kemi 1932 vs 1999：已解决为 1999（KePS 数字另属），见 §7.1。
- PK-35 Vantaa vs 赫尔辛基 PK-35：两家俱乐部，绝不合并，见 §7.2。
- 场馆候选冲突：TPS 个别场次在 Paavo Nurmi Stadion（listed 主场 Veritas Stadion）→ moved；
  Lahti 全季 FBref 记 Kisapuisto（2016 listed 主场 Lahden kisapuisto）→ neutral（别名未确认）；
  2016-08-26/27 三行跨城 printed 场馆（原因未核实，原值保留）。
- 同名陷阱两起（均已弃用错误匹配）：Kisapuisto 拉彭兰塔同名条目、Elisa Stadion→Eisstadion Davos 误匹配。

## 10. 方法与文件

- 分季转录：三路并行子代理，各读 FBref 联赛赛程页全部文本行（2016：528 行；2017：491 行；2018：全页），
  只取 Wk/Day/Date/Time/Home/Away/Venue，删除 Score、Attendance、Referee、Match Report、Notes
  （含 "Match awarded" 等赛后信息）；去重键 (match_date, home_team, away_team)。
- 合并脚本：`merge_2016_2018.py`（本目录；可复跑，输入为三季 fbref_*.jsonl＋evidence/）。
- 中间文件：`fbref_2016_schedule_rows.jsonl`、`fbref_2016_notes.md`、`fbref_2017_schedule_rows.jsonl`、
  `fbref_2017_notes.md`、`fbref_2018_schedule_rows.jsonl`、`fbref_2018_notes.md`、`evidence/`（赛季页、俱乐部文章、
  场馆坐标响应、解析索引）、`merge_stats.json`。
- 未写 `repo/responses/`（主代理的事）；未购买、未登录、未使用任何密钥/凭证、未动用付费 API 额度。
