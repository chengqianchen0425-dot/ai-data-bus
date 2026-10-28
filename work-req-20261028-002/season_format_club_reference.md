# Veikkausliiga 2016–2026 赛制与俱乐部身份参考表（req-20261028-002 D 路）

> 用途：供其他路与请求方复核 2016–2026 各季赛制与俱乐部身份，不替其他路填数。
> 红线：本文件不含任何比分、赛果、积分、排名数值、射手、赛后状态与预测判断。升降级只表述为升入/降级/附加赛升入/附加赛留级/附加赛降级，不写名次数值。名字相似绝不合并；更名/合并无源写“未核实”。
> 2026 赛季场次明细见 method_context_2026.jsonl（177 行）与 method_context_2026_notes.md；本文件 2026 节只写赛制、俱乐部与交接事实。

---

# 2026 赛季

## 赛制表

| 项目 | 内容 | 来源 |
|---|---|---|
| 参赛队数 | 12 队 | Wikipedia 2026 赛季球队表；Flashscore 预览“All 12 teams” |
| 常规赛 | 双循环，每队与其余各队交手两次，共 22 轮 | Sportmonks 赛制页；topscorersfootball 轮次 1–22 |
| 分裂 | 常规赛后分为冠军组（6 队）与保级组（6 队） | Sportmonks 赛制页；Wikipedia 2026 赛季页章节结构（Regular season / Championship round / Relegation round） |
| 冠军组 | 双循环再赛 10 场，每队总计 32 场；轮次 23–32 | Sportmonks 赛制页；轮次表实测（每轮 3 场 × 10 轮） |
| 保级组 | 单循环再赛 5 场，每队总计 27 场；轮次 23–27 | Sportmonks 赛制页；轮次表实测（每轮 3 场 × 5 轮） |
| 赛季起止 | 2026-04-04 至 2026-11-08 | topscorersfootball 赛季页；Flashscore 预览 |
| 赛季状态（截至 2026-10-28） | 进行中、未完赛：常规赛与保级组轮次已完，冠军组剩 30–32 轮 9 场（日期已发布，2026-10-28 至 2026-11-08） | 轮次表（177 场全有日期与轮次）；本单不写剩余场次的任何赛果与状态词 |
| 联赛总场次 | 177 场（132 + 15 + 30） | 轮次表逐场计数，与结构算式一致 |
| 附加赛 | Wikipedia 2026 赛季页另有 "Veikkausliiga play-off" 一节（两回合），属联赛附加赛类别，不计入 177 场联赛场次，本单不展开 | Wikipedia 2026 赛季页章节结构 |

## 2026 参赛俱乐部（12 队）与赛季球场、建队年份

| 俱乐部（常用名） | 城市 | 赛季球场（2026 赛季表，非本场确认） | 建队年份 natal_year | 备注 |
|---|---|---|---|---|
| AC Oulu | Oulu | Raatti Stadium（竞争候选：Heinäpää Stadium，俱乐部页称 2026–present） | 2002 | 主场名冲突，见 method_context_2026_notes.md §4 |
| FC Inter Turku | Turku | Veritas Stadion（与 TPS 共用） | 1990 | |
| FC Lahti | Lahti | Lahti Stadium（俱乐部页赞助名 Toolpoint Arena） | 1996 | 2026 升班队（见交接） |
| FF Jaro | Jakobstad (Pietarsaari) | Project Liv Arena（旧名 Jakobstads Centralplan，是否更名/新球场未证实） | 1965 | 球场坐标未确认 |
| HJK | Helsinki | Bolt Arena（俱乐部页通用名 Töölö Football Stadium） | 1907（1907-06-19） | |
| IF Gnistan | Helsinki (Oulunkylä) | Markku.fi Areena（竞争候选：Mustapekka Areena、Oulunkylä Football Stadium） | 1924 | 主场名冲突；2024 季为顶级联赛首季（见 2023 节顶替事实） |
| IFK Mariehamn | Mariehamn | Wiklöf Holding Arena | 1919 | 球场坐标未确认；IANA 时区 Europe/Mariehamn |
| Ilves | Tampere | Tammelan Stadion | 1931 | 多项目俱乐部；足球场以赛季表为准 |
| KuPS | Kuopio | Väre Areena（场次列表通用名 Kuopio Football Stadium） | 1923 | 球场坐标未确认（两地理编码结果不一致） |
| SJK | Seinäjoki | OmaSP Stadion | 2007（2007-11-05，由 TP-Seinäjoki 与 Sepsi-78 合并成立） | |
| TPS | Turku | Veritas Stadion（与 Inter 共用） | 1922 | 2026 升班队（附加赛胜者，见交接） |
| VPS | Vaasa | Hietalahti Stadium（场次列表赞助名 Elisa Stadion） | 1924 | 仅名称冲突，地址同一 |

建队年份来源：Wikipedia 各俱乐部页 infobox Founded 行（字节哈希见 method_context_2026_notes.md §8）。competition_entry_year（本单口径：以升班身份进入 2026 赛季的年份）仅 Lahti、TPS 为 2026，其余 10 队为 null（首次顶级赛季未核实，不拿建队年份冒充）。

## 2025→2026 升降级交接

- 降出：FC Haka（直接降级）；KTP（升降级附加赛失利降级，附加赛对手为 TPS）。
- 升入：FC Lahti（2025 Ykkösliiga 升入）；TPS（通过升降级附加赛升入，附加赛对手为 KTP）。
- 来源：Wikipedia 2026 赛季页 Team changes 节；Wikipedia 2025 Ykkösliiga 联赛表升入/附加赛标注；Flashscore 2026 预览称 Lahti 与 TPS 为 promoted sides。三者一致。

---

# 2016–2025 赛季（以下为子任务草稿并入部分；已核验每季清单均为 12 队，链条与 2026 交接一致）

> 用途：供 ai-data-bus req-20261028-002 的 D 路主文件 `season_format_club_reference.md` 使用，不替其他路填数。
> 范围：只做赛前事实——每季赛制、参赛俱乐部清单、升降级 / 更名 / 破产顶替等身份事实。
> 红线执行说明：
>
> - 本文件不含任何比分、赛果、胜平负、积分、排名数值、射手、赛后状态与预测判断。俱乐部清单按字母顺序排列，与最终名次无关。
> - 升降级只表述为“直接升入 / 直接降级 / 通过升降级附加赛升入 / 通过升降级附加赛留级 / 通过升降级附加赛降级”，不写名次数值。
> - 名字相似绝不合并：不同俱乐部即使名字相近也分开列；更名 / 合并无源则写“未核实”，不推测。
> - 同一场升降级附加赛会在相邻两季各出现一次（上一季的“季末交接”与下一季的“季初变动”），系同一事件的两端表述，不是两次附加赛，合并时请勿重复计数。
> - 次级联赛名称注意：2024 年起，次级联赛改称 Ykkösliiga（新建的第二级），原 Ykkönen 降为第三级。此前赛季的次级联赛称 Ykkönen。两名不可混用。
> - 俱乐部名称以来源页的简称 / 常用名为准；同一俱乐部在不同来源页的名称变体（如 FC Inter Turku / Inter Turku、FC Lahti / Lahti、IFK Mariehamn / Mariehamn、HIFK / HIFK Fotboll、PS Kemi / PS Kemi Kings）在本文件统一用一个条目列出，并在“名称变体与身份冲突提示”中注明，不视为两家俱乐部，但也不以此断言更名。
>
> 来源标注口径：本单全部事实均取自公开网页文本层（browser.search / browser.open 的文本结果），未下载源文件字节，因此每条来源的 `source_sha256` 均为 `null`，并注明“文本层、无字节”。绝不以描述文字或 URL 的哈希冒充源哈希（上一单 req-20261006-004 的描述符哈希做法本单明令无效，未沿用）。

## 赛制变化节点总览（线索证实 / 证伪）

| 节点 | 线索 | 结论 |
|---|---|---|
| 2016–2018 | 疑似三循环 33 场 | **证实**。2016、2017、2018 各季来源页均写明：每队与其余各队交手三次（主场两次 / 客场一次，或主场一次 / 客场两次），每队共 33 场；无分裂。2016 年另有补充：上季前六名球队主场比赛为 17 场、其余六队为 16 场。 |
| 2019 起 | 疑似 22 轮 + 分裂后各 5 场 | **证实**。2019 季来源页“New league format”写明：常规赛每队互相对阵两次；常规赛后前六名进冠军组、后六名进保级组（原文称 Challenger Series）；两组各再赛 5 场，每队总计 27 场。另设欧战附加赛（见 2019 节）。 |
| 2020 | 疑似因故只打 22 轮、无分裂 | **证实，但需精确表述**：原定赛制仍是 2019 式分裂赛制，但 2020 年 10 月 28 日决定取消冠军组与保级组，常规赛 22 轮的结果即为最终结果。因此实际执行为“22 轮、无分裂”，而非赛前就定为无分裂赛制。取消原因来源页表述为芬兰的新冠疫情。 |
| 2021–2024 | 延续 22 轮 + 分裂后各 5 场 | **证实为延续**。联赛总述页写明：截至 2024 年，12 队先双循环常规赛，分裂后冠军组与保级组各再赛 5 场，每队总计 27 场；2019–2024 年间实行欧战附加赛。逐季欧战附加赛的具体对阵结构本单未逐一核对（见“未核实清单”）。 |
| 2025 起 | 疑似冠军组双循环（共 32 场）/ 保级组单循环（共 27 场） | **证实**。联赛总述页写明：2024 年 11 月末宣布废除欧战附加赛并更改赛制；2025 年起，22 轮双循环常规赛后，后六名打单循环保级组（每队总计 27 场），前六名打双循环冠军组（每队总计 32 场）。2025 季来源页的冠军组 / 保级组分组结构与该表述一致。 |

---

## 2016 赛季

### 赛制表

| 项目 | 内容 |
|---|---|
| 参赛队数 | 12 队 |
| 常规赛 | 三循环：每队与其余各队交手三次（主场两次 / 客场一次，或主场一次 / 客场两次） |
| 分裂 | 无 |
| 每队总场次 | 33 场 |
| 主场场次补充 | 上季前六名球队 17 个主场、其余六队 16 个主场 |
| 升降级附加赛 | 有：顶级联赛附加赛席位球队对阵次级联赛附加赛席位球队，两回合 |
| 欧战附加赛 | 无（2019 年前未见该机制；联赛总述称欧战附加赛实行于 2019–2024 年间） |

### 参赛俱乐部清单（12 队，按字母顺序）

- FC Inter Turku（图尔库）
- FC Lahti（拉赫蒂）
- HIFK（赫尔辛基）
- HJK（赫尔辛基）
- IFK Mariehamn（玛丽港）
- Ilves（坦佩雷）
- KuPS（库奥皮奥）
- PK-35 Vantaa（万塔）
- PS Kemi Kings（凯米；来源球场表作 PS Kemi）
- RoPS（罗瓦涅米）
- SJK（塞伊奈约基）
- VPS（瓦萨）

### 季初变动（从上季进入本季）

- 升入：PS Kemi（次级联赛升入，顶替上季直接降级的 FF Jaro）；PK-35 Vantaa（通过升降级附加赛升入，顶替上季附加赛席位球队 KTP）。
- 降出（指上季季末离开顶级联赛）：FF Jaro（直接降级）；KTP（附加赛失利降级）。

### 季末交接（进入 2017 赛季）

- 直接降级：PK-35 Vantaa。
- 附加赛留级：FC Inter Turku（附加赛对手为 TPS，TPS 未能升入）。
- 2017 季升入球队见 2017 节“季初变动”。

### 来源行

- source_name：Wikipedia，2016 Veikkausliiga；field_locator：“Teams”节（季初变动文字、球场与位置表）及“Results”节三循环表述；source_url：https://en.wikipedia.org/wiki/2016_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：Wikipedia，Veikkausliiga（联赛总述）；field_locator：“Structure”节 2016 年赛制段落（12 队、三循环、33 轮、附加赛机制）；source_url：https://en.wikipedia.org/wiki/Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。

---

## 2017 赛季

### 赛制表

| 项目 | 内容 |
|---|---|
| 参赛队数 | 12 队 |
| 常规赛 | 三循环：每队与其余各队交手三次 |
| 分裂 | 无 |
| 每队总场次 | 33 场 |
| 升降级附加赛 | 有，两回合 |
| 欧战附加赛 | 无（同 2016 节） |

### 参赛俱乐部清单（12 队，按字母顺序）

- FC Inter Turku（图尔库）
- FC Lahti（拉赫蒂）
- HIFK（赫尔辛基）
- HJK（赫尔辛基）
- IFK Mariehamn（玛丽港）
- Ilves（坦佩雷）
- JJK Jyväskylä（于韦斯屈莱）
- KuPS（库奥皮奥）
- PS Kemi Kings（凯米）
- RoPS（罗瓦涅米）
- SJK（塞伊奈约基）
- VPS（瓦萨）

### 季初变动（从上季进入本季）

- 升入：JJK（次级联赛升入，顶替直接降级的 PK-35 Vantaa）。
- 留级：FC Inter Turku（上季季末附加赛留级，见 2016 节）。

### 季末交接（进入 2018 赛季）

- 直接降级：JJK Jyväskylä。
- 附加赛降级：HIFK（附加赛对手为 FC Honka，FC Honka 升入）。
- 2018 季升入球队见 2018 节“季初变动”。

### 身份事实补充（次级联赛，非顶级联赛本身）

- PK-35 Vantaa 在 2016 季末降入次级联赛后，宣布破产并退出次级联赛席位，该席位由 OPS 顶替。此事不改变 2017 顶级联赛清单，但合并 / 清理 PK-35 相关实体时须注意：2016 顶级联赛的 PK-35 Vantaa 与此后次级联赛中出现的 PK-35 在本文件不作同一实体认定，关系未核实。

### 来源行

- source_name：Wikipedia，2017 Veikkausliiga；field_locator：“Teams”节（季初变动文字、球场与位置表）、“Results”节三循环表述、“Relegation play-offs”节（FC Honka 对 HIFK）；source_url：https://en.wikipedia.org/wiki/2017_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：Wikipedia，2017 Ykkönen；field_locator：“Overview”节（PK-35 Vantaa 破产退出、OPS 顶替、JJK 升入顶级联赛）；source_url：https://en.wikipedia.org/wiki/2017_Ykkönen；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。

---

## 2018 赛季

### 赛制表

| 项目 | 内容 |
|---|---|
| 参赛队数 | 12 队 |
| 常规赛 | 三循环：每队与其余各队交手三次 |
| 分裂 | 无 |
| 每队总场次 | 33 场 |
| 升降级附加赛 | 有，两回合 |
| 欧战附加赛 | 无（同 2016 节） |

### 参赛俱乐部清单（12 队，按字母顺序）

- FC Honka（埃斯波）
- FC Inter Turku（图尔库）
- FC Lahti（拉赫蒂）
- HJK（赫尔辛基）
- IFK Mariehamn（玛丽港）
- Ilves（坦佩雷）
- KuPS（库奥皮奥）
- PS Kemi Kings（凯米）
- RoPS（罗瓦涅米）
- SJK（塞伊奈约基）
- TPS（图尔库）
- VPS（瓦萨）

### 季初变动（从上季进入本季）

- 升入：TPS（次级联赛升入，顶替直接降级的 JJK）；FC Honka（通过升降级附加赛升入，顶替附加赛降级的 HIFK）。

### 季末交接（进入 2019 赛季）

- 直接降级：PS Kemi Kings（来源页作 PS Kemi / PS Kemi Kings，同一条目）。
- 附加赛降级：TPS（附加赛对手为 KPV，KPV 升入）。
- 2019 季升入球队见 2019 节“季初变动”。

### 来源行

- source_name：Wikipedia，2018 Veikkausliiga；field_locator：“Teams”节（季初变动文字、球场与位置表）、“Results”节三循环表述；source_url：https://en.wikipedia.org/wiki/2018_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：Wikipedia，2019 Veikkausliiga；field_locator：“Teams”节（PS Kemi 直接降级、TPS 附加赛失利、KPV 升入）；source_url：https://en.wikipedia.org/wiki/2019_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。

---

## 2019 赛季

### 赛制表

| 项目 | 内容 |
|---|---|
| 参赛队数 | 12 队 |
| 常规赛 | 双循环：每队与其余各队交手两次，共 22 轮 |
| 分裂 | 常规赛后分为冠军组（6 队）与保级组（6 队，来源页称 Challenger Series）；两组各再单循环 5 场 |
| 每队总场次 | 27 场 |
| 升降级附加赛 | 有：保级组附加赛席位球队对阵次级联赛附加赛席位球队，两回合 |
| 欧战附加赛 | 有：保级组头名与冠军组第 4–6 名球队等先进行附加赛 tournament，胜者再与冠军组第 3 名球队进行附加赛 final，争夺最后一个欧战资格（结构表述引自来源页“New league format”节，不含对阵结果） |

### 参赛俱乐部清单（12 队，按字母顺序）

- FC Honka（埃斯波）
- FC Inter Turku（图尔库）
- FC Lahti（拉赫蒂）
- HIFK（赫尔辛基）
- HJK（赫尔辛基）
- IFK Mariehamn（玛丽港）
- Ilves（坦佩雷）
- KPV（科科拉）
- KuPS（库奥皮奥）
- RoPS（罗瓦涅米）
- SJK（塞伊奈约基）
- VPS（瓦萨）

### 季初变动（从上季进入本季）

- 升入：HIFK Fotboll（次级联赛升入，顶替直接降级的 PS Kemi Kings）；KPV（全称 Kokkolan Palloveikot，来源页作 Kokkolan Palloveikot；通过升降级附加赛升入，顶替附加赛降级的 TPS）。

### 季末交接（进入 2020 赛季）

- 直接降级：VPS。
- 附加赛降级：KPV（附加赛对手为 TPS，TPS 升入）。
- 2020 季升入球队见 2020 节“季初变动”。

### 来源行

- source_name：Wikipedia，2019 Veikkausliiga；field_locator：“New league format”节（双循环、分裂、欧战附加赛结构、保级组降级与附加赛机制）、“Teams”节（球场与位置表、季初变动文字）、联赛表注释（22 场后分裂为前六 / 后六）；source_url：https://en.wikipedia.org/wiki/2019_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：Wikipedia，2020 Veikkausliiga；field_locator：“Teams”节球场与位置表（用于交叉核对 2020 清单，见 2020 节）；source_url：https://en.wikipedia.org/wiki/2020_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。

---

## 2020 赛季

### 赛制表

| 项目 | 内容 |
|---|---|
| 参赛队数 | 12 队 |
| 常规赛 | 双循环：每队与其余各队交手两次，共 22 轮 |
| 分裂 | 原定分裂赛制，但 2020 年 10 月 28 日决定取消冠军组与保级组，常规赛 22 轮的结果即为最终结果；实际执行无分裂 |
| 每队总场次 | 22 场（实际执行；原定分裂后应为 27 场，未执行） |
| 取消原因（来源表述） | 芬兰的新冠疫情 |
| 升降级附加赛 | 有：顶级联赛附加赛席位球队 TPS 对阵次级联赛附加赛席位球队 KTP，KTP 升入（该附加赛的胜负归属引自 2021 季来源页“Teams”节文字） |
| 欧战附加赛 | 未核实（分裂取消后当季欧战附加赛是否举行，本单未核实，不推测） |

### 参赛俱乐部清单（12 队，按字母顺序）

- FC Haka（瓦尔凯阿科斯基）
- FC Honka（埃斯波）
- FC Inter Turku（图尔库）
- FC Lahti（拉赫蒂）
- HIFK（赫尔辛基）
- HJK（赫尔辛基）
- IFK Mariehamn（玛丽港）
- Ilves（坦佩雷）
- KuPS（库奥皮奥）
- RoPS（罗瓦涅米）
- SJK（塞伊奈约基）
- TPS（图尔库）

### 季初变动（从上季进入本季）

- 升入：FC Haka（次级联赛升入，顶替直接降级的 VPS）；TPS（通过升降级附加赛升入，顶替附加赛降级的 KPV）。

### 季末交接（进入 2021 赛季）

- 直接降级：RoPS。
- 附加赛降级：TPS（附加赛对手为 KTP，KTP 升入）。
- 2021 季升入球队见 2021 节“季初变动”。

### 来源行

- source_name：Wikipedia，2020 Veikkausliiga；field_locator：“Stadiums and locations”节球场与位置表（12 队清单）、“League table”节前取消分裂的说明文字（2020 年 10 月 28 日决定、22 轮后即为最终结果）；source_url：https://en.wikipedia.org/wiki/2020_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：Wikipedia，2021 Veikkausliiga；field_locator：“Teams”节（RoPS 直接降级、AC Oulu 升入、TPS 附加赛失利、KTP 升入）；source_url：https://en.wikipedia.org/wiki/2021_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。

---

## 2021 赛季

### 赛制表

| 项目 | 内容 |
|---|---|
| 参赛队数 | 12 队 |
| 常规赛 | 双循环：每队与其余各队交手两次，共 22 轮 |
| 分裂 | 常规赛后分为冠军组（6 队）与保级组（6 队）；两组各再单循环 5 场 |
| 每队总场次 | 27 场 |
| 升降级附加赛 | 有，两回合 |
| 欧战附加赛 | 有（联赛总述称 2019–2024 年间实行；本季具体对阵结构未逐一核对，见“未核实清单”） |

### 参赛俱乐部清单（12 队，按字母顺序）

- AC Oulu（奥卢）
- FC Haka（瓦尔凯阿科斯基）
- FC Honka（埃斯波）
- FC Inter Turku（图尔库）
- FC Lahti（拉赫蒂）
- HIFK（赫尔辛基）
- HJK（赫尔辛基）
- IFK Mariehamn（玛丽港）
- Ilves（坦佩雷）
- KTP（科特卡）
- KuPS（库奥皮奥）
- SJK（塞伊奈约基）

> 清单核对方法：由 2020 清单减去季末降级的 RoPS、TPS，加上季初升入的 AC Oulu、KTP 推导，并与 2021 季冠军组 / 保级组分组片段中出现的队名交叉核对一致。本季未在本单逐页打开球场与位置表，方法如实标注。

### 季初变动（从上季进入本季）

- 升入：AC Oulu（次级联赛升入，顶替直接降级的 RoPS）；KTP（通过升降级附加赛升入，顶替附加赛降级的 TPS）。

### 季末交接（进入 2022 赛季）

- 直接降级：KTP。
- 附加赛留级：AC Oulu（附加赛对手为 RoPS，RoPS 未能升入）。
- 2022 季升入球队见 2022 节“季初变动”。

### 来源行

- source_name：Wikipedia，2021 Veikkausliiga；field_locator：“Teams”节（季初变动文字）；source_url：https://en.wikipedia.org/wiki/2021_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：FBref，2021 AC Oulu 附加赛记录；field_locator：附加赛两回合记录（对手 RoPS、AC Oulu 胜出留级）；source_url：https://fbref.com/de/squads/9fc6bb9a/2021/AC-Oulu-Stats；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：Wikipedia，Veikkausliiga（联赛总述）；field_locator：“Structure”节（截至 2024 年的 22 轮 + 分裂后各 5 场、总计 27 场；2019–2024 年欧战附加赛）；source_url：https://en.wikipedia.org/wiki/Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。

---

## 2022 赛季

### 赛制表

| 项目 | 内容 |
|---|---|
| 参赛队数 | 12 队 |
| 常规赛 | 双循环：每队与其余各队交手两次，共 22 轮 |
| 分裂 | 常规赛后分为冠军组（6 队）与保级组（6 队）；两组各再单循环 5 场 |
| 每队总场次 | 27 场 |
| 升降级附加赛 | 有，两回合 |
| 欧战附加赛 | 有（联赛总述称 2019–2024 年间实行；本季具体对阵结构未逐一核对，见“未核实清单”） |

### 参赛俱乐部清单（12 队，按字母顺序）

- AC Oulu（奥卢）
- FC Haka（瓦尔凯阿科斯基）
- FC Honka（埃斯波）
- FC Inter Turku（图尔库）
- FC Lahti（拉赫蒂）
- HIFK（赫尔辛基）
- HJK（赫尔辛基）
- IFK Mariehamn（玛丽港）
- Ilves（坦佩雷）
- KuPS（库奥皮奥）
- SJK（塞伊奈约基）
- VPS（瓦萨）

> 清单核对方法：由 2021 清单减去季末直接降级的 KTP，加上季初升入的 VPS 推导，并与 2022 季冠军组 / 保级组分组片段中出现的队名交叉核对一致（AC Oulu 留级已由 2021 季末附加赛证实）。

### 季初变动（从上季进入本季）

- 升入：VPS（全称 Vaasan Palloseura；次级联赛升入，顶替直接降级的 KTP）。

### 季末交接（进入 2023 赛季）

- 直接降级：HIFK。
- 附加赛留级：FC Lahti（附加赛对手为 TPS，TPS 未能升入）。
- 2023 季升入球队见 2023 节“季初变动”。

### 来源行

- source_name：Wikipedia，2022 Veikkausliiga；field_locator：“Teams”节（KTP 直接降级、VPS 升入）；source_url：https://en.wikipedia.org/wiki/2022_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：FBref，2022 升降级附加赛记录；field_locator：附加赛记录（FC Lahti 对 TPS、FC Lahti 留级）；source_url：https://fbref.com/en/comps/203/2022/2022-Finnish-12-RelegationPromotion-Play-offs-Stats；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：Wikipedia，2023 Veikkausliiga；field_locator：“Teams”节升降级对照表（KTP 升入、HIFK 降出）；source_url：https://en.wikipedia.org/wiki/2023_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。

---

## 2023 赛季

### 赛制表

| 项目 | 内容 |
|---|---|
| 参赛队数 | 12 队 |
| 常规赛 | 双循环：每队与其余各队交手两次，共 22 轮 |
| 分裂 | 22 轮后分为冠军组与保级组；两组各再单循环 5 场 |
| 每队总场次 | 27 场 |
| 升降级附加赛 | 有，两回合 |
| 欧战附加赛 | 有（联赛总述称 2019–2024 年间实行；本季具体对阵结构未逐一核对，见“未核实清单”） |

### 参赛俱乐部清单（12 队，按字母顺序）

- AC Oulu（奥卢）
- FC Haka（瓦尔凯阿科斯基）
- FC Honka（埃斯波）
- FC Inter Turku（图尔库）
- FC Lahti（拉赫蒂）
- HJK（赫尔辛基）
- IFK Mariehamn（玛丽港）
- Ilves（坦佩雷）
- KTP（科特卡）
- KuPS（库奥皮奥）
- SJK（塞伊奈约基）
- VPS（瓦萨）

### 季初变动（从上季进入本季）

- 升入：KTP（次级联赛升入，顶替直接降级的 HIFK）。

### 季末交接（进入 2024 赛季）

- 直接降级：KTP。
- 附加赛留级：IFK Mariehamn（附加赛对手为 Gnistan；Gnistan 虽附加赛失利，但随后因 FC Honka 破产被取消资格而通过补充许可程序升入，见下条）。
- 破产 / 顶替（关键身份事实）：FC Honka 因财务问题被取消顶级联赛资格（来源页表述为破产 / 财务问题导致降级）；其顶级联赛名额由 Gnistan 通过补充许可程序顶替。Gnistan 此前为次级联赛球队，2024 季为其顶级联赛首季。FC Honka 降级后的去向层级，来源页有“降入 Kakkonen”的表述，本文件不以此作为 Gnistan 顶替机制之外的独立断言，见“未核实清单”。
- 2024 季升入球队见 2024 节“季初变动”。

### 来源行

- source_name：Wikipedia，2023 Veikkausliiga；field_locator：“Teams”节（12 队、22 轮后分裂、球场与位置表、升降级对照表 KTP / HIFK）、赛季概述段（IFK Mariehamn 附加赛留级、KTP 直接降级、FC Honka 因财务问题被取消资格）；source_url：https://en.wikipedia.org/wiki/2023_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：Wikipedia，2024 Veikkausliiga；field_locator：“Team changes”节（EIF 升入、Gnistan 因 FC Honka 破产被取消资格而升入）；source_url：https://en.wikipedia.org/wiki/2024_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：Wikipedia，IF Gnistan；field_locator：俱乐部历史段（2023 季次级联赛附加赛失利后，因 FC Honka 破产而通过补充许可程序获得顶级联赛执照，2024 季为顶级联赛首季）；source_url：http://en.wikipedia.org/wiki/IF_Gnistan；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。

---

## 2024 赛季

### 赛制表

| 项目 | 内容 |
|---|---|
| 参赛队数 | 12 队 |
| 常规赛 | 双循环：每队与其余各队交手两次，共 22 轮 |
| 分裂 | 常规赛后分为冠军组（6 队）与保级组（6 队）；两组各再单循环 5 场 |
| 每队总场次 | 27 场 |
| 升降级附加赛 | 有：顶级联赛附加赛席位球队对阵次级联赛（Ykkösliiga）附加赛席位球队，两回合 |
| 欧战附加赛 | 有（联赛总述称 2019–2024 年间实行；2024 季来源页冠军组 / 保级组表亦出现欧战附加赛席位表述；具体对阵结构未逐一核对，见“未核实清单”） |

### 参赛俱乐部清单（12 队，按字母顺序）

- AC Oulu（奥卢）
- Ekenäs IF（EIF，拉塞博格 / 埃克奈斯）
- FC Haka（瓦尔凯阿科斯基）
- FC Inter Turku（图尔库）
- FC Lahti（拉赫蒂）
- HJK（赫尔辛基）
- IF Gnistan（赫尔辛基）
- IFK Mariehamn（玛丽港）
- Ilves（坦佩雷）
- KuPS（库奥皮奥）
- SJK（塞伊奈约基）
- VPS（瓦萨）

### 季初变动（从上季进入本季）

- 升入：EIF（次级联赛升入，顶替直接降级的 KTP）；IF Gnistan（因 FC Honka 破产被取消资格，通过补充许可程序顶替升入，见 2023 节）。
- 说明：2024 季来源页称“十队留队、两队升入”，与本清单的变动一致；FC Honka 不在 2024 清单中，不是因为当季附加赛失利，而是季前资格取消。

### 季末交接（进入 2025 赛季）

- 直接降级：EIF（降入 Ykkösliiga）。
- 附加赛降级：FC Lahti（附加赛对手为 FF Jaro，FF Jaro 升入）。
- 2025 季升入球队见 2025 节“季初变动”。

### 身份事实补充（次级联赛，非顶级联赛本身）

- HIFK 在 2023 季处于次级联赛，季后因破产解散（来源页次级联赛表注“Club folded”）。HIFK 与 2016–2022 季顶级联赛的 HIFK 为同一名称条目，但本单未核实其法人 / 执照连续性，合并时请勿仅凭同名认定为同一实体存续，关系记“未核实”。

### 来源行

- source_name：Wikipedia，2024 Veikkausliiga；field_locator：“Teams”节（12 队构成文字）、“Team changes”节（EIF / Gnistan 升入、KTP 降出、季末 EIF 直接降级、FC Lahti 附加赛负于 FF Jaro 降级）、“Stadiums and locations”节球场与位置表；source_url：https://en.wikipedia.org/wiki/2024_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：Wikipedia，2023 Ykkönen；field_locator：升级组联赛表注释（HIFK 注“Club folded”）及概述段（HIFK 季后因破产解散）；source_url：https://en.wikipedia.org/wiki/2023_Ykkönen；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：Wikipedia，2025 Veikkausliiga；field_locator：“Team changes”节（KTP / FF Jaro 升入、EIF / FC Lahti 降出）；source_url：https://en.wikipedia.org/wiki/2025_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。

---

## 2025 赛季

### 赛制表

| 项目 | 内容 |
|---|---|
| 参赛队数 | 12 队 |
| 常规赛 | 双循环：每队与其余各队交手两次，共 22 轮 |
| 分裂 | 22 轮后分为冠军组（6 队）与保级组（6 队）；冠军组双循环再赛 10 场，保级组单循环再赛 5 场 |
| 每队总场次 | 冠军组球队 32 场；保级组球队 27 场 |
| 升降级附加赛 | 有：顶级联赛附加赛席位球队对阵次级联赛（Ykkösliiga）附加赛席位球队，两回合 |
| 欧战附加赛 | 无（2024 年 11 月末宣布自 2025 年起废除） |

### 参赛俱乐部清单（12 队，按字母顺序）

- AC Oulu（奥卢）
- FC Haka（瓦尔凯阿科斯基）
- FC Inter Turku（图尔库）
- FF Jaro（雅各布斯塔德）
- HJK（赫尔辛基）
- IF Gnistan（赫尔辛基）
- IFK Mariehamn（玛丽港）
- Ilves（坦佩雷）
- KTP（科特卡）
- KuPS（库奥皮奥）
- SJK（塞伊奈约基）
- VPS（瓦萨）

### 季初变动（从上季进入本季）

- 升入：KTP（次级联赛 Ykkösliiga 升入，顶替直接降级的 EIF）；FF Jaro（通过升降级附加赛升入，顶替附加赛降级的 FC Lahti）。
- 注意：2025 季来源页“Team changes”表头误写“2024 Ykkönen”，但正文与 2024 季来源页一致表明当季次级联赛已为 Ykkösliiga；本文件按 Ykkösliiga 表述，表头笔误如实标注于此。

### 季末交接（进入 2026 赛季，见文末专节）

- 直接降级：FC Haka（降入 Ykkösliiga）。
- 附加赛降级：KTP（附加赛对手为 TPS，TPS 升入）。
- 2026 季升入球队：FC Lahti、TPS（见“2025→2026 升降级交接”专节）。

### 来源行

- source_name：Wikipedia，2025 Veikkausliiga；field_locator：“Teams”节（12 队构成文字）、“Team changes”节（KTP / FF Jaro 升入、EIF / FC Lahti 降出）、“Stadiums and locations”节球场与位置表、“Regular season”节（22 轮常规赛分组）、“Championship round”节（冠军组球队总场次结构）、“Relegation round”节（保级组球队总场次结构）、“Veikkausliiga play-off”节（KTP 对 TPS 的附加赛对阵）；source_url：https://en.wikipedia.org/wiki/2025_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：Wikipedia，Veikkausliiga（联赛总述）；field_locator：“Structure”节（2024 年 11 月末宣布废除欧战附加赛、2025 年起冠军组双循环 32 场 / 保级组单循环 27 场）；source_url：https://en.wikipedia.org/wiki/Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。

---

## 2025→2026 升降级交接（2026 赛季本身不在本单范围）

- 降出顶级联赛（进入 2026 Ykkösliiga）：FC Haka（直接降级）；KTP（升降级附加赛失利降级，附加赛对手为 TPS）。
- 升入顶级联赛（进入 2026 Veikkausliiga）：FC Lahti（2025 Ykkösliiga 升入）；TPS（通过升降级附加赛升入，附加赛对手为 KTP）。
- 核实说明：任务提示“2025 季末升入 2026 的两队 FC Lahti 与 TPS 已有公开报道”已由本单独立核实——2026 季来源页“Team changes”节写明升入球队为 FC Lahti 与 TPS、降出球队为 FC Haka 与 KTP；2025 Ykkösliiga 来源页亦显示 FC Lahti 为升入球队、TPS 为附加赛升入球队。两者一致。
- 本单不写 2026 赛季赛制与俱乐部清单（主 agent 已做），此处只写交接事实。

### 来源行

- source_name：Wikipedia，2026 Veikkausliiga；field_locator：“Teams”节 / “Team changes”表（FC Lahti、TPS 升入；FC Haka、KTP 降出；联赛由十队留队加两队升入构成）；source_url：https://en.wikipedia.org/wiki/2026_Veikkausliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。
- source_name：Wikipedia，2025 Ykkösliiga；field_locator：联赛表升入 / 附加赛标注（FC Lahti 升入、TPS 附加赛升入）；source_url：https://en.wikipedia.org/wiki/2025_Ykk%C3%B6sliiga；retrieved_at：2026-10-28 16:14 Asia/Shanghai；source_sha256：null（文本层、无字节）。

---

## 名称变体与身份冲突提示（合并时必读）

- 同城不同队，绝不合并：图尔库有 FC Inter Turku 与 TPS 两队；赫尔辛基有 HJK、HIFK、IF Gnistan（Gnistan 仅 2024–2025 季在顶级联赛清单中）。同城不等于同队。
- 首字母相近不同队，绝不合并：KTP（科特卡）与 KPV（科科拉）为两家不同俱乐部；KTP 出现于 2016（降出）、2021、2023、2025 季清单，KPV 仅出现于 2019 季清单。
- 名称变体（同一季内同一条目，不视为两队）：FC Inter Turku / Inter Turku；FC Lahti / Lahti；IFK Mariehamn / Mariehamn；HIFK / HIFK Fotboll；PS Kemi / PS Kemi Kings；FC Honka / Honka；FF Jaro / Jaro；Ekenäs IF / EIF；IF Gnistan / Gnistan。
- PK-35 冲突：2016 顶级联赛条目为 PK-35 Vantaa；此后次级联赛出现的 PK-35 与 PK-35 Vantaa 是否为同一实体，本单未核实，本文件不合并、不认定。
- HIFK 存续：2016–2022 季顶级联赛的 HIFK 与 2023 季次级联赛后解散的 HIFK 是否为同一法人 / 执照连续体，本单未核实，不认定。
- FC Honka 去向层级：2023 季末 FC Honka 被取消资格后降入哪一级，来源页有“Kakkonen”表述，但与 Gnistan 顶替机制的来源表述侧重点不同；本文件只断言“被取消顶级联赛资格、名额由 Gnistan 顶替”，去向层级记未核实。
- 2016–2025 顶级联赛参赛俱乐部之间，除上述破产 / 资格取消 / 席位顶替外，本单未核实到更名或合并案例；如 D 路需写更名 / 合并史，请另行核源，不得由同名推断。

---

## 未核实清单

1. 2021、2022、2023、2024 各季欧战附加赛的具体对阵结构：联赛总述只证实 2019–2024 年间实行欧战附加赛、2025 年起废除；2019 季结构已核实，2024 季来源页亦出现欧战附加赛席位表述，但其余各季的对阵细节本单未逐一核对，D 路如需写细则须另核源。
2. 2020 季欧战附加赛是否举行：分裂取消后，来源页未说明欧战附加赛去向，本单记未核实，不推测为“取消”或“照常”。
3. 2021、2022 季俱乐部清单的直接球场表核对：本单采用“上季清单 ± 升降级变动 + 分组片段交叉核对”的推导方法，未逐页打开该两季的球场与位置表；如 D 路要求逐季球场表直证，须补核。
4. 各俱乐部全称展开：除来源页球场表中明确给出的全称（如 Kuopion Palloseura、Vaasan Palloseura、Seinäjoen Jalkapallokerho、Kokkolan Palloveikot）外，其余简称的全称展开本单未逐一核对，清单以简称 / 常用名为准。
5. PK-35 Vantaa 与此后次级联赛 PK-35 的实体关系：未核实。
6. HIFK 的法人 / 执照连续性（顶级联赛时期与 2023 季后解散之间）：未核实。
7. FC Honka 2023 季末被取消资格后的去向层级：来源表述不完全一致，记未核实（仅断言取消资格与 Gnistan 顶替）。
8. 2016–2025 年间各俱乐部主场、球场容量等场地事实：非本单任务必需，未逐季核对，D 路如需请另核源；本文件所写城市名仅用于同城区分，取自各季球场与位置表。
9. 2025 季来源页“Team changes”表头将次级联赛误写为“2024 Ykkönen”一事：正文与 2024 季来源页支持 Ykkösliiga 表述，但该表头笔误本身未向联赛官方二次核实，D 路引用时请以正文与联赛总述为准。

---

## 来源清单

| # | source_name | source_url | field_locator（页内位置） | retrieved_at | source_sha256 |
|---|---|---|---|---|---|
| S1 | Wikipedia，2016 Veikkausliiga | https://en.wikipedia.org/wiki/2016_Veikkausliiga | Teams 节、Results 节 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S2 | Wikipedia，2017 Veikkausliiga | https://en.wikipedia.org/wiki/2017_Veikkausliiga | Teams 节、Results 节、Relegation play-offs 节 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S3 | Wikipedia，2017 Ykkönen | https://en.wikipedia.org/wiki/2017_Ykkönen | Overview 节 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S4 | Wikipedia，2018 Veikkausliiga | https://en.wikipedia.org/wiki/2018_Veikkausliiga | Teams 节、Results 节 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S5 | Wikipedia，2019 Veikkausliiga | https://en.wikipedia.org/wiki/2019_Veikkausliiga | New league format 节、Teams 节、联赛表注释 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S6 | Wikipedia，2020 Veikkausliiga | https://en.wikipedia.org/wiki/2020_Veikkausliiga | Stadiums and locations 节、League table 节前取消分裂说明 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S7 | Wikipedia，2021 Veikkausliiga | https://en.wikipedia.org/wiki/2021_Veikkausliiga | Teams 节 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S8 | FBref，2021 AC Oulu 附加赛记录 | https://fbref.com/de/squads/9fc6bb9a/2021/AC-Oulu-Stats | 附加赛两回合记录 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S9 | Wikipedia，2022 Veikkausliiga | https://en.wikipedia.org/wiki/2022_Veikkausliiga | Teams 节 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S10 | FBref，2022 升降级附加赛记录 | https://fbref.com/en/comps/203/2022/2022-Finnish-12-RelegationPromotion-Play-offs-Stats | 附加赛记录（FC Lahti 对 TPS） | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S11 | Wikipedia，2023 Veikkausliiga | https://en.wikipedia.org/wiki/2023_Veikkausliiga | Teams 节、赛季概述段 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S12 | Wikipedia，2023 Ykkönen | https://en.wikipedia.org/wiki/2023_Ykkönen | 升级组联赛表注释、概述段 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S13 | Wikipedia，IF Gnistan | http://en.wikipedia.org/wiki/IF_Gnistan | 俱乐部历史段 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S14 | Wikipedia，2024 Veikkausliiga | https://en.wikipedia.org/wiki/2024_Veikkausliiga | Teams 节、Team changes 节、Stadiums and locations 节 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S15 | Wikipedia，2025 Veikkausliiga | https://en.wikipedia.org/wiki/2025_Veikkausliiga | Teams 节、Team changes 节、Stadiums and locations 节、Regular season / Championship round / Relegation round 节、Veikkausliiga play-off 节 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S16 | Wikipedia，Veikkausliiga（联赛总述） | https://en.wikipedia.org/wiki/Veikkausliiga | Structure 节（2016 年赛制、截至 2024 年赛制、2019–2024 欧战附加赛、2025 年改制） | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S17 | Wikipedia，2026 Veikkausliiga | https://en.wikipedia.org/wiki/2026_Veikkausliiga | Teams 节 / Team changes 表 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |
| S18 | Wikipedia，2025 Ykkösliiga | https://en.wikipedia.org/wiki/2025_Ykk%C3%B6sliiga | 联赛表升入 / 附加赛标注 | 2026-10-28 16:14 Asia/Shanghai | null（文本层、无字节） |

> 说明：本单未购买、未登录、未使用任何密钥 / 凭证 / 付费 API；全部来源均为公开网页文本。未遇到 403 拦截，无需换源记录。
