# Veikkausliiga 2023 交叉核对 + 缺口填补 — season_2023 说明（req-20261028-002）

> 只含赛前事实。比分、赛果、积分榜全文、盘口、预测一律未写、未用于推断。
> 俱乐部“赛季末行政身份”（KTP 降级、Honka 降级）是任务第 6 项明确要求的身份事实，
> 与单场比赛结果无关；附加赛名次仅用于说明附加赛入围资格（赛前种子顺位），不写附加赛胜负。

## 1. 计数

| 口径 | 数 |
|---|---|
| expected（-004 基线 2023 行） | 167 |
| discovered（本轮交付行） | 167 |
| complete（除 meeting_number 外全部可填字段齐全） | 165 |
| conflict（场馆存在竞争候选，见 §6） | 2 |
| partial（行级） | 0 |
| unavailable（行级） | 0 |
| blocked（行级） | 0 |
| missing（轮次/系列填补后仍缺） | 0（轮次/系列层面）；见下方字段级仍缺 |
| -004 沿用行 | 167（身份、日期、主客队全部沿用，零覆盖） |
| -004 覆盖行（开球时间系统性覆盖，见 §5） | 167（时钟值 +2h；旧值逐行保留在 `kickoff_old_req20261006-004`） |
| 新增场次 | 0 |
| 轮次填补（5 场 null → 附加赛阶段） | 5 |
| 场馆场次级确认（FBref 场次级行，非官方页） | 165 确认 + 2 易地 = 167 行均有场次级场馆证据 |
| 场馆官方级确认（联赛/俱乐部比赛页） | 0 |
| meeting_number 填补 | 0 / 167，全部 `unavailable` |

字段级仍缺（诚实口径，不混入行级计数）：
- 官方 KIERROS（官方轮次）：167 / 167 仍缺官方源。162 行轮次值沿用 -004 的
  WorldFootball 分组（`official_round_source=worldfootball_matchday_non_official`），
  5 行附加赛阶段由 FBref + Wikipedia 交叉源填补（`official_round_source` 明确标非官方）。
- meeting_number：167 / 167 `unavailable`（尝试源见 §7）。
- 官方芬兰语附加赛名：任务假设名 Eurolopputurnaus 本轮未在官方源核实，
  交付中一律只用英文名 Conference League play-off，不把假设名当已核实结论。

## 2. 5 场 null 轮次核实结果（全部填补，0 场仍缺阶段）

结论：假设成立——5 场确为 2023 年欧协联附加赛（Conference League play-offs），
奖品为剩余 1 个欧协联第一轮资格赛名额（赛前规则，Wikipedia 赛季页 Play-offs 节）。

| 日期 | 场次 | 阶段（本轮填补值） | 赛制 |
|---|---|---|---|
| 2023-10-25 | Honka vs Inter Turku | Conference League play-offs — Quarter-finals | 四分之一决赛，单场 |
| 2023-10-25 | SJK vs AC Oulu | Conference League play-offs — Quarter-finals | 四分之一决赛，单场 |
| 2023-10-28 | Honka vs AC Oulu | Conference League play-offs — Semi-final | 半决赛，单场 |
| 2023-11-01 | Honka vs VPS | Conference League play-offs — Final, leg 1 | 决赛第 1 回合 |
| 2023-11-05 | VPS vs Honka | Conference League play-offs — Final, leg 2 | 决赛第 2 回合 |

赛制（源：Wikipedia 2023 赛季页 Play-offs 节，curl 实下载，
sha256 `a0643547005eb91cf8fd75f9add38f26539144c3ee61f4b11bd666fe9e3d3e75`；
FBref 赛程表 Round 列独立一致）：
- 参赛 5 队为联赛最终名次第 3–7 名：VPS（第 3）、SJK（第 4）、Honka（第 5）、
  Inter Turku（第 6）、AC Oulu（第 7，即保级组第 1）。
- 第 3 名 VPS 直通决赛；其余 4 队打四分之一决赛（Honka–Inter、SJK–Oulu），
  胜者打半决赛（Honka–Oulu），半决赛胜者打决赛对 VPS。
- 四分之一决赛、半决赛单场（名次较高者主场）；决赛两回合。
- 附加赛阶段不属于 1–27 联赛轮次，因此 `official_round` 填阶段名而非数字，
  且绝不从日期顺序推断为“第 28 轮”之类。

注意：-004 附带的 2023-matchday-labels.json 中这 5 场的 ECL-QF/SF/Final 标签
与本轮结论一致，但本轮填补依据是 Wikipedia + FBref 两个独立交叉源，
不是直接照抄标签文件。

## 3. 赛制结论：为什么是 167 场而不是 132 或 162

算式（源同上 Wikipedia 赛季页 Teams/分组表/Play-offs 节 + 赛程结构描述）：
- 常规赛：12 队双循环，每队 22 场 → 12×22/2 = **132 场**（轮次 1–22）。
- 分组赛：22 轮后分冠军组 6 队、保级组 6 队，组内单循环，每队再打 5 场 →
  12×5/2 = **30 场**（-004 轮次 23–27；每队联赛共 27 场）。
- 联赛合计：132 + 30 = **162 场**。
- 余下 **5 场** = 上述欧协联附加赛（四分之一决赛 2 + 半决赛 1 + 决赛 2），
  不计入联赛轮次，但计入本数据集的 167 行。
- 132 + 30 + 5 = **167**，与 -004 行数吻合。

“是否双循环”：分阶段回答——常规赛是双循环；分组赛是组内单循环；
整季不是纯双循环（每队联赛 27 场而非 22 场，且分组赛对手只交手一次）。
另注意两个易混口径，均不在 167 行内，不计入：
- Wikipedia 赛季页信息框 “Matches 132” 只计常规赛（且标注统计截至 10 月 9 日），
  不是整季总数，引用时须注明。
- 第 11 名球队参加的 Veikkausliiga/Ykkönen 升降级附加赛（对 Gnistan 的两回合）
  不属于本 167 行数据集，本轮未将其计入、也未写其结果。

## 4. 轮次与系列（162 行沿用 + 5 行填补）

- 轮次 1–22：`series_or_phase=Regular season`；轮次 23–27：
  主队属冠军组（HJK、KuPS、SJK、VPS、Honka、Inter Turku）为 Championship round，
  属保级组（AC Oulu、Haka、Lahti、Ilves、KTP、Mariehamn）为 Relegation round。
  分组归属以常规赛后分组表为准，非日期推断；组内对阵与分组一致（无跨组场次）。
- 轮次值本身沿用 -004（WorldFootball 分组），未找到官方 KIERROS 源逐场升级，
  因此 `official_round_source` 全部如实标非官方，绝不升级。

## 5. 开球时间：系统性覆盖（本轮最大发现，167 行全部覆盖）

问题：-004 的 `kickoff`（源自 football-data CSV）实际是**英国时钟时间**，
却被标注为 Europe/Helsinki，导致全部 167 行本地时间偏早 2 小时。
证据（均不涉及比分）：
- FBref 赛程表（文本层浏览全表）Time 列为场馆本地时间：其括号内太平洋时间
  与场馆本地时间换算一致（如 4 月 18:00 赫尔辛基 = 08:00 PDT；11 月 5 日
  16:00 赫尔辛基 = 06:00 PST），证明第一列确为本地时间。
- 逐行比对 21 行（常规赛 16 行 + 附加赛 5 行，含 :15/:30 分钟位与 8 月 30 日
  补赛场次）FBref 时间 = -004 时间 + 2h，**21/21 全中**，无一例外。
- 附加赛 5 场另有三方 UTC 瞬时交叉验证：FotMob/CapperTek/SportsMole 给出的
  UTC 瞬时换算为赫尔辛基本地时间后等于 FBref 值，不等于 -004 值；
  Wikipedia 附加赛节标注的英国时钟时间（误标 BST）数值上等于 -004 值，
  +2h 后等于 FBref 值——三方闭合。
- 覆盖方法：`kickoff_local = -004 时间 + 2h`；`kickoff_utc` 按芬兰夏令时换算：
  2023-10-29 之前 EEST（UTC+3），2023-10-29 起 EET（UTC+2）。
  旧值逐行保留在 `kickoff_old_req20261006-004`，日期、主客队零覆盖。

残留风险（必须向主代理明示）：其余 146 行的 +2h 覆盖依据为同一系统性模式；
FBref 全表虽已在文本层浏览，但因 FBref curl 被拒（本机返回 000，无字节），
未能机器转录逐行核对。若个别场次 -004 时间本身就是本地时间，该行会被误改 2 小时。
建议主代理在下游把本文件当权威时间使用前，对剩余 146 行做一次机器级 FBref 复核。
本轮交付已把这一风险写进每行 `provenance.kickoff.note`，不隐瞒。

## 6. 场馆：场次级确认 167 行，官方级 0 行

- 165 行：FBref 场次级 Venue 列与 -004 赛季主场映射一致（仅名称变体/别名，
  非位置冲突，均保留在 `venue_candidates`）：VPS 的 Hietalahti / Elisa Stadion /
  Lemonsoft Stadion 为同一 Vaasa 场馆；KuPS 的 Savon Sanomat Areena = Väre Areena（更名）；
  HJK 的 Telia 5G -areena = Bolt Arena（更名）；Ilves 的 Tampere Stadium = Ratinan stadion。
  `venue_status=confirmed` 在此仅指“场次级交叉源指名该场馆”，不是官方确认；
  官方级确认数为 0，已在每行 provenance 中注明。
- 2 行易地（`venue_status=moved`，行级 `row_status=conflict`，竞争候选全部保留）：
  - 2023-04-15 Honka vs SJK：场次级场馆为 Myyrmäen jalkapallostadion（Vantaa，
    60.26024, 24.84279，本轮 map.geocode 全地址结果；Sky Sports 称 ISS Stadion，
    为同一场馆的冠名），不是赛季主场 Tapiolan Urheilupuisto。
    SportsMole 仍列 Tapiolan（保留为竞争候选）。
  - 2023-04-15 Ilves vs Inter Turku：场次级场馆为 Tehtaan kenttä（Valkeakoski，
    61.2665, 24.02617，沿用 -004 坐标），不是赛季主场 Ratinan stadion。
    SportsMole 列 Tammelan Stadion（保留为竞争候选）。
  - 两场易地均有 FBref + Sky Sports 两源一致，SportsMole 一源相异，故按两源采纳、
    异源保留，不作单源独断。
- 坐标出处：除 Myyrmäki 外全部沿用 -004 venue-coords.json（地理编码结果，
  注明出处、不是字节哈希）；场馆 IANA 时区全部为 Europe/Helsinki。
- 附加赛 5 场场馆：与 -004 映射一致（Honka 主场 Tapiolan、SJK 主场 OmaSP、
  VPS 主场 Lemonsoft；Wikipedia 附加赛节对 VPS 主场写作 Hietalahti Stadium，
  为同一场馆别名，已记入候选）。

## 7. 俱乐部官方身份（12 队，主客队各一，见 jsonl 内 `home_club_identity` / `away_club_identity`）

建队年（本轮俱乐部 Wikipedia 页 infobox 文本抽取；字节未保留，sha256=null）：
AC Oulu 2002；HJK 1907-06-19；Haka 1934；Honka 1957；Ilves 1931（体育俱乐部建队年，
足球分部独立建队年本轮未单独核实，不得替换使用）；Inter Turku 1990；
KTP 1927-09-22；KuPS 1923；Lahti 1996；Mariehamn 1919；SJK 2007-11-05；VPS 1924。

特别注意 KTP：2023 季唯一升班马（2022 Ykkönen 冠军升入；HIFK 降出）。
身份沿革关键点：2013 年 12 月 FC KooTeePee 采用 KTP 之名，合并后俱乐部自 2014 起
保留 KooTeePee 的 Ykkönen 席位——不得把更早的 KTP 破产史直接等同于现俱乐部，
也不得把 KTP 与其他 Kotka 球队合并。Lahti（1996）与 SJK（2007）的前身/合并对象
本轮未核实，一律留空、不猜。名字相似绝不合并（如 Inter Turku ≠ TPS；
AC Oulu ≠ OLS）。

## 8. meeting_number：167 / 167 unavailable

仅当权威源明确定义或可无推断联结官方轮次记录时才填；本轮两者皆无。
尝试过的源：veikkausliiga.com（本轮 curl 返回 000，不可达）；
tulospalvelu.palloliitto.fi（200 但仅返回 2597 字节 JS 壳，无批量数据）；
WorldFootball、FBref、Wikipedia 2023 赛季页（均无 meeting_number 字段）。
绝不从日期顺序、球队出现次数、比分、积分榜、盘口推断。

## 9. CSV 联结

请求方指定的身份 CSV（Windows 路径）在本 VM 不存在、无法读取。
因此：与 -004 行能对上的 167 场全部沿用 -004 fixture_key，
`csv_join_status=matched_to_req-20261006-004_row_csv_join_pending`；
对不上的场次 0 场模糊匹配。另有 1 条标签文件差异未作新场次（见 §10）。

## 10. 未覆盖与冲突清单

1. 官方 KIERROS：167 行均无官方源（见 §1、§4）。
2. meeting_number：167 行均无源（见 §8）。
3. 官方级场馆确认：167 行均为 0（仅场次级交叉源，见 §6）。
4. 官方芬兰语附加赛名 Eurolopputurnaus：未核实，不使用。
5. 场馆竞争候选 2 行：Honka–SJK（Tapiolan vs Myyrmäki，采纳后者）、
   Ilves–Inter（Ratinan/Tammelan vs Tehtaan kenttä，采纳后者），异源均已保留。
6. 俱乐部信息未核实项：Ilves 足球分部独立建队年；Lahti、SJK 合并对象；
   其余俱乐部合并/更名前身（除 KTP 2013 年更名外）——均留空。
7. 开球时间残留风险：146 行未机器逐行复核（见 §5），需主代理复核后方可当权威时间用。
8. 标签文件差异 1 条：-004 附带标签文件（168 条归一化键）中有一条
   “2023-04-30 KuPS 主场 vs Mariehamn”，与 -004/FBref 的同日
   “Mariehamn 主场 vs KuPS”主客颠倒。本轮不作新场次、不模糊匹配，
   记为 unresolved 标签差异；若主代理认定标签文件有误，应由标签文件方修正，
   本文件不擅自改动主客队。

## 11. 尝试过但失败的源

- veikkausliiga.com：本轮 curl 000，不可达（与 -004 记载的官网档案 500 问题一致方向，
  本轮未拿到任何官方轮次页）。
- tulospalvelu.palloliitto.fi：200 但仅 JS 壳（2597 字节），无批量提取路径；
  其 API 在 -004 已记为 Cloudflare 拦截，本轮未重复撞 API。
- WorldFootball 文本层：-004 已记 curl 403；本轮未复取，轮次沿用 -004 记录，
  sha256=null（绝不复用 -004 的描述符哈希）。
- FBref curl：本机返回 000、无字节；本轮 FBref 证据全部来自浏览器文本层，
  因此全部 FBref 字段 sha256=null + 注明“文本层、无字节”。
- Soccerway 2023 结果页：本轮 curl 200（819,252 字节，sha256
  `f3ff6b45c0cf22afa9ed2cbc9567a0c16078fc1e3589128012605d512917a869`），
  但其 ROUND 分组同样为非官方交叉源，未用于升级官方轮次，故不列为轮次证据。
- 官方芬兰语附加赛规则页（palloliitto/veikkausliiga 2023 赛季规则）：检索未命中
  可直接引用的官方条文，赛制依据退为 Wikipedia + FBref 交叉源，已如实标注。

## 12. Provenance 铁律执行情况

- 每个非 null 字段均有 `provenance` 字段级对象：source_url、final_url、
  retrieved_at（+08:00）、field_locator、source_name 齐全。
- source_sha256 仅在真正 curl 下载到字节时填写：本轮唯一实字节哈希为
  Wikipedia 2023 赛季页 `a0643547005eb91cf8fd75f9add38f26539144c3ee61f4b11bd666fe9e3d3e75`
 （371,071 字节，2026-10-28T16:12:46+08:00 下载）；其余全部 null +
  注明“文本层、无字节”或“沿用-004，描述符哈希不复用”。
- -004 的 source_sha256 一律未复用（-004 式哈希为描述符，非源证据哈希）。
- 坐标 sha：无；-004 venue-coords.json 与本轮 geocode 结果均注明为地理编码出处。

## 13. 交付文件

- `season_2023.jsonl`：167 行，每行含任务要求的全部字段（含 `kickoff_old_req20261006-004`
  与 `meeting_number_attempted_sources` 两个审计附加字段）。
- `season_2023_notes.md`：本文件。
- 未写 repo/responses/，未动其他赛季文件，未购买、未登录、未使用任何密钥/付费额度。
