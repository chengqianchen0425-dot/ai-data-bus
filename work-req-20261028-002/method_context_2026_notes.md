# method_context_2026_notes.md — req-20261028-002 D 路（Veikkausliiga 2026 赛季 + 方法上下文）

## 0. 口径与禁令遵守声明

- 只做赛前事实：本文件与 method_context_2026.jsonl、season_format_club_reference.md 中不含任何比分、赛果、积分、排名、赛后状态、分析模型输出与预测判断。行内出现 "topscorersfootball" 只是来源站域名（该站名含 scorers 一词），行中没有任何比分值字段；"results disagree" 指地理编码结果不一致，不是比赛结果。
- 不写任何本地项目文件或正式记录：交付物仅为本工作目录下的三份 D 路文件。
- 身份 CSV：请求方指定的 Windows 路径 CSV 在本 VM 上不存在、无法读取。每行键为 `season|match_date|home_team|away_team`，`csv_join_status="csv_unavailable_on_this_vm_derived_from_public_schedule"`；绝不声称与 CSV 精确对应，绝不模糊匹配。
- Provenance：上一单 req-20261006-004 的 source_sha256 是描述符哈希，本单明令无效。本单行内 source_sha256 只有两种诚实状态：(a) 真实源字节哈希——topscorersfootball 全量赛程 HTML（154,635 字节，SHA-256 见下）与 Wikipedia 2026 球队表 HTML（字节哈希见下）；(b) null 并注明原因（Flashscore 预览为浏览器文本层、无字节；俱乐部页哈希只在行外哈希表列出，行内不冒充）。

## 1. 2026 计数（expected / discovered / complete / partial / unavailable / blocked / conflict / missing）

- expected：本单不预设“应有场次”总数作为目标。事后结构算式（仅作核对，不作预设分母）：12 队常规赛双循环 132 场 + 保级组单循环 15 场 + 冠军组双循环 30 场 = 177 场。
- discovered：177 行（topscorersfootball "All matches" 全量，轮次 1–22 常规赛各 6 场、轮次 23–27 保级组各 3 场、轮次 23–32 冠军组各 3 场），与结构算式 177 一致。
- complete：110 行（赛季/日期/对阵/轮次标签/阶段齐全，且 meeting_number 无歧义；注意：complete 不代表场馆已确认或开球时间已确认，那两项另行计数）。
- partial：59 行（场馆名存在竞争候选，见 §4）。
- conflict：8 行（meeting_number 因轮次顺序与日期顺序不一致而置 null 的两对球队的全部 8 场比赛，见 §3）。
- unavailable：以下字段全量或大面积缺失，均记 null 而非推断——
  - 开球时间：171/177 行为 null（源只给日期）；仅第 1 轮 6 场有时间（Flashscore 预览，CEST 标签，见 §5）。
  - 场馆场次级确认：177/177 行为 null（无任何一场的场馆本场证据；场馆一律为赛季表候选）。
  - 场馆经纬度：42/177 行为 null（Jaro、KuPS、Mariehamn 三队主场坐标未确认，见 §4）。
  - competition_entry_year：除 2026 升班两队外全部为 null（首个顶级赛季未核实，见 §6）。
- blocked：1 项——worldfootball.net 全量赛程页在本轮返回 HTTP 403（未重试、未绕过，见 §7），该源未覆盖；Veikkausliiga 官方赛程文件本轮未检索到可下载版本，记为未覆盖（官方轮次措辞因此未作主张），不计入 blocked。
- missing：赛程本身无缺失场次（177/177 均有日期与轮次）；缺失的是字段，不是场次（见 unavailable）。

## 2. 2026 赛季是否已开赛、赛程是否完整发布

- 已开赛：是。赛季 2026-04-04 至 2026-11-08（多源一致：topscorersfootball 赛季页、Flashscore 预览、Sportmonks 赛制页）。
- 进行中、未完赛：截至 2026-10-28，常规赛（22 轮）与保级组（27 轮）已打完轮次表所列场次；冠军组进行到第 29 轮，剩余第 30、31、32 轮共 9 场，日期为 2026-10-28、2026-10-29、2026-11-01、2026-11-02、2026-11-08（已发布日期，未进行）。本文件不写这些场的任何赛果与状态词，只写“已发布日期”。
- 赛程完整性：赛程已完整发布——177 场全部有日期与轮次标签；没有用往季推断任何一场。另注意：Wikipedia 2026 赛季页另有 "Veikkausliiga play-off" 一节（两回合附加赛），属于联赛附加赛类别，不计入本单 177 场联赛场次，也不展开。
- 赛制（2026，源依据）：12 队；常规赛双循环 22 场/队；前 6 名进冠军组再双循环 10 场/队（合计 32 场/队）；后 6 名进保级组再单循环 5 场/队（合计 27 场/队）。来源：Sportmonks 赛制页（字节哈希见 §8）与 Flashscore 预览（"first of 22 rounds in the regular season, before the league splits into two for another 10 rounds"——注意该句的 "another 10 rounds" 指冠军组轮次总数，与保级组 5 轮并存，不冲突）。

## 3. meeting_number：可填 169 行，不可填 8 行

- 方法：无任何来源发布 meeting_number 字段（meeting_number_published 全行为 false）。本单 filling 采用“已发布赛程内的无歧义顺序计数”：按轮次顺序数同一对球队的第几次相遇；仅当轮次顺序与日期顺序两种计数一致时才填，否则置 null。
- 可填：169 行（36 对常规赛后不再相遇的球队各 2 次；15 对冠军组球队各 4 次；15 对保级组球队各 3 次；共 66 对 = C(12,2)，全部对局均有记录）。
- 不可填：8 行，两对球队——
  - KuPS vs Oulu（4 场）：轮次顺序为 Round 5（2026-05-02，Oulu 主场）→ Round 14（2026-04-22，KuPS 主场）→ Round 26（2026-10-08）→ Round 31（2026-11-01）；日期顺序则为 04-22 → 05-02 → 10-08 → 11-01。两种计数对前两场给出相反的 1/2。
  - HJK vs Inter Turku（4 场）：轮次顺序为 Round 11（2026-06-17）→ Round 14（2026-04-29）→ Round 23（2026-09-09）→ Round 30（2026-10-29）；日期顺序则为 04-29 → 06-17 → 09-09 → 10-29。同样前两场相反。
  - 成因说明（不裁决）：后一轮次的比赛在更早日期进行，符合“提前进行”（brought forward）的赛程安排，但本轮未取得官方提前说明，故两种计数都不采信，8 行 meeting_number 全部 null，轮次与日期原文双双保留。
- 另有 2 场日期早于第 13 轮的同类提前场次（Ilves vs Inter Turku Round 15，2026-05-20；KuPS vs Jaro Round 15，2026-05-20）不影响本对球队内部的计数顺序（轮次顺序与日期顺序一致），故 meeting_number 正常填写，但日期-轮次错位现象记在此处备查。

## 4. 场馆：场次级确认 0 场；赛季表候选 + 竞争候选清单

- 场馆场次级确认数：0/177。所有行的 venue_verified 均为 null；venue_name_candidate 一律来自 Wikipedia 2026 赛季球队表（赛季级表），不是本场证据。
- venue_status neutral（116 行）：Inter/TPS 共用 Veritas Stadion（Turku）、HJK Bolt Arena（Helsinki）、Ilves Tammelan Stadion（Tampere）、SJK OmaSP Stadion（Seinäjoki）、Lahti Lahti Stadium、Mariehamn Wiklöf Holding Arena（名称无争议，坐标未确认）。
- venue_status conflict（61 行，名称竞争，不选边）：
  - AC Oulu（主场比赛）：Raatti Stadium（2026 赛季表）vs Heinäpää Stadium（俱乐部页球场小节：Raatti 2011–2026、Heinäpää 2026–present）。2026 年内换主场是可能的，单场归属无法确定。
  - IF Gnistan：Markku.fi Areena（2026 赛季表）vs Mustapekka Areena（未来场次列表用名）vs Oulunkylä Football Stadium（俱乐部页通用名）。俱乐部页另载 2024 年 7 月 Mustapekka Areena 火灾报道，可作为更名背景线索，但本轮无单源证实三名同指一地，故不合并。
  - VPS：Hietalahti Stadium（2026 赛季表）vs Elisa Stadion（场次列表用名，Vaasa Rantamaantie 6，赞助名）。仅名称冲突，地址同一。
  - FF Jaro：Project Liv Arena（2026 赛季表）vs Jakobstads Centralplan（旧名）。是更名还是新球场，本轮无单源证实，不合并。
- 经纬度（WGS84，地理编码工具结果；仅 FULL_ADDRESS 高相关度结果才填入行内坐标）：
  - 已填：Raatti 65.01973, 25.46442；Veritas 60.443, 22.29045；Lahti Stadium 60.98279, 25.66243；Bolt Arena 60.1875, 24.92209；Mustapekka 地块（Gnistan 地面）60.23381, 24.96251；Tammelan 61.50028, 23.78538；OmaSP 62.77903, 22.81542；Elisa/Hietalahti 63.08551, 21.62855。
  - 未填（行内 null，候选保留在行内 venue_latlon_note）：Jaro（两个地理编码点不一致且均非球场确认匹配）、KuPS（62.82283, 27.60319 相关度 51 与 62.83599, 27.62325 相关度 79 不一致）、Mariehamn（Idrottsgatan 街道级点 60.10325, 19.93565 与市中心商业地址点 60.09788, 19.94165 均非球场确认匹配）。
- IANA 时区：芬兰本土一律 Europe/Helsinki；Mariehamn 用 Europe/Mariehamn（Åland 专属 IANA 区，与 Helsinki 偏移相同 EET/EEST，此处只写区名，不换算具体偏移）。

## 5. 开球时间：仅第 1 轮 6 场有时间，且时区标签存疑

- 第 1 轮 6 场（2026-04-04）：Inter Turku vs VPS 12:00、HJK vs SJK 14:00、Ilves vs KuPS 16:00、Jaro vs Lahti 16:00、Mariehamn vs TPS 16:00、Gnistan vs Oulu 18:00。来源 Flashscore 预览 "The opening weekend" 一节，原文标注 "All times CEST"。
- 存疑点（故 kickoff_utc 全行 null）：CEST = UTC+2，而芬兰 4 月实行 EEST = UTC+3。若按 CEST 字面换算会得到 UTC 10:00/12:00/14:00/16:00，若按芬兰本地时间则为 UTC 09:00/11:00/13:00/15:00。来源未说明其 CEST 标签是否为站方显示时区惯例，故两种换算都不做，行内只保留原文时间与原文标签，并写明换算方法缺失。
- 其余 171 场：topscorersfootball 只给日期，无时间字段，kickoff_local_time 一律 null，绝不按“芬兰比赛多在 17:00/18:00”之类惯例补时间。

## 6. 俱乐部官方身份

- natal_year（founded，Wikipedia 俱乐部页 infobox Founded 行，行外哈希表见 §8）：AC Oulu 2002、FC Inter Turku 1990、FC Lahti 1996、FF Jaro 1965、HJK 1907（1907-06-19）、IF Gnistan 1924、IFK Mariehamn 1919、Ilves 1931、KuPS 1923、SJK 2007（2007-11-05，由 TP-Seinäjoki 与 Sepsi-78 合并成立）、TPS 1922、VPS 1924。
- lineage：仅 SJK 写合并事实（有源）；Ilves 注明多项目俱乐部、足球场以赛季表为准（俱乐部 infobox 的主场栏列的是冰球馆，不采用）；其余俱乐部 lineage 为 null（无合并主张，不写“单一血统”这种无法证实的话）。
- competition_entry_year 定义（本单口径，见行内 competition_entry_year_definition）：仅指“以升班身份进入 2026 赛季的年份”。Lahti 与 TPS = 2026（Flashscore 预览称二者为 promoted sides，Lahti 为二级冠军、TPS 为附加赛胜者；2025→2026 交接事实另见 season_format_club_reference.md）。其余 10 队该字段为 null——它们的首次顶级赛季本轮未用俱乐部史源核实，绝不拿建队年份冒充参赛年份。

## 7. 未覆盖与冲突清单（除 §3、§4 外）

- worldfootball.net 全量赛程页（https://www.worldfootball.net/all_matches/fin-veikkausliiga-2026/）本轮返回 HTTP 403，未重试、未换端点绕过；该源的轮次/时间/场馆信息因此未覆盖，不影响 177 场（topscorersfootball 已全覆盖）。
- Veikkausliiga 官方赛程文件（联赛官网 otteluohjelma）本轮未检索到可下载版本：官方轮次措辞、官方开球时间、官方场馆表因此全部未覆盖；行内 official_round 明确标注为 topscorersfootball 的轮次标签，不是官方措辞主张。
- topscorersfootball 的 "13 participants" 赛季摘要与 12 队实际名单冲突：12 队名单以赛季球队表与轮次表（每轮 6 场）为准，13 之说不采信（疑为摘要计数口误/含附加赛队伍，不深究）。
- Flashscore 预览称分裂后 "another 10 rounds"，与保级组实际 5 轮（轮次 23–27）表面不符：该句指冠军组轮次跨度（轮次 23–32），保级组 5 轮并存，两者不冲突，行内 stage_format 按轮次表实测书写。
- 2026 赛季球队表与俱乐部页的球场名差异（Raatti/Heinäpää、Markku.fi/Mustapekka、Hietalahti/Elisa、Project Liv/Centralplan）全部保留为竞争候选，未合并、未选边（见 §4）。

## 8. 来源与证据字节哈希表

- topscorersfootball 全量赛程（行内 fixture_source）：https://www.topscorersfootball.com/veikkausliiga/standing-and-matches-2026 ，检索 2026-10-28T16:12:00+08:00，证据 evidence/topscorers_2026.html（154,635 字节），SHA-256 ac4bc404ce6e3bbe8f3b75aa017fe0990c71d1277c6fbf09dd314bb074e996a2。注意：该原始捕获含赛后字段，行内已全部剥离；原始文件仅作审计证据留存。
- Wikipedia 2026 赛季球队表（行内 venue_source）：https://en.wikipedia.org/wiki/2026_Veikkausliiga ，检索 2026-10-28T16:13:00+08:00，证据 evidence/wiki_2026_veikkausliiga.html，SHA-256 792e4fd6bdc69b995a07e6e31503d89f7abb0730e8146d218ebd118b0904256d。
- Sportmonks 赛制页（赛制依据）：https://www.sportmonks.com/glossary/finnish-veikkausliiga/ ，检索 2026-10-28T16:13:00+08:00，证据 evidence/sportmonks_veikkausliiga_format.html，SHA-256 2e9c19dfe0ac411745cbeaafb11b21d1731e09d32d9ba4e7f17c1a684858f7d5。内容要点：12 队、常规赛各 22 场、冠军组再双循环 10 场/队、保级组再单循环 5 场/队。
- Flashscore 预览（第 1 轮时间 + 升班队）：https://www.flashscore.co.ke/news/soccer-veikkausliiga-veikkausliiga-2026-season-preview-kups-title-again-or-can-hjk-bounce-back/OSSLRfPG/ ，浏览器文本层读取 2026-10-28T16:13:00+08:00，source_sha256 null（文本层、无字节）。
- 俱乐部页（founded 年份，行外哈希表；行内只写年份与页名，不冒充行内哈希）：
  - AC Oulu：https://en.wikipedia.org/wiki/AC_Oulu ，SHA-256 cabde55cb42b81db3b5407683492fdfee782366d25d85e25bff9aad22d7c6bc8
  - FC Inter Turku：https://en.wikipedia.org/wiki/FC_Inter_Turku ，SHA-256 eaf4c22bfeac7ab0b71bc57e9bae090db21b35605d90e4c6c7a661e3c2c78952
  - FC Lahti：https://en.wikipedia.org/wiki/FC_Lahti ，SHA-256 bb5460af15f694e1d4e6c927bcbb7cf94318b15fca8a7faef33b5d6091ca6307
  - FF Jaro：https://en.wikipedia.org/wiki/FF_Jaro ，SHA-256 1c4f778b64655315c8bf5ef213e7c94fd30782535829e181585a001cfee9aa4b
  - HJK：https://en.wikipedia.org/wiki/HJK_Helsinki ，SHA-256 69241fb1470b085c53f7a1302946a3a0ac4d837f028d2ca82bae23ddd0bd2dac
  - IF Gnistan：https://en.wikipedia.org/wiki/IF_Gnistan ，SHA-256 c79630d449739ef9bffb30d64815be894c6592d7dffde27a214c7b08c3ddf29d
  - IFK Mariehamn：https://en.wikipedia.org/wiki/IFK_Mariehamn ，SHA-256 2b9ef1d3764c442f0f8bf4454201ef3baf7ef1dba8595b4b8417928eaf08435c
  - Ilves：https://en.wikipedia.org/wiki/Ilves ，SHA-256 6bd4e51709288cac819222fcaca5dd628c9a0e3fa48ef965fe118ae722adb2a9  （注：该页为多项目俱乐部总页，足球场信息以赛季表为准）
  - KuPS：https://en.wikipedia.org/wiki/Kuopion_Palloseura ，SHA-256 fb47b928c3e3eac5a146a7f96cae71d07ca34c1c93f30ad493f2d480923b6caa
  - SJK：https://en.wikipedia.org/wiki/Seinäjoen_Jalkapallokerho ，SHA-256 695bcc25eb59c38cdf9d3d3e54d579056f5d58b11c660bcad24f26d34be05366
  - TPS：https://en.wikipedia.org/wiki/Turun_Palloseura ，SHA-256 a19055a7a3c99f8db184eac5fa6c64995752ccc67d201855e9c768159cef0226
  - VPS：https://en.wikipedia.org/wiki/Vaasan_Palloseura ，SHA-256 180ac17682ad25571404bee138d90aed3ab50148a4f225708be056ccdc5de8c4
- 地理编码：map.geocode 工具结果（行内 venue_latlon_note 标注匹配等级与相关度）；Jaro/KuPS/Mariehamn 的未确认候选见 §4，不填入行内坐标。
