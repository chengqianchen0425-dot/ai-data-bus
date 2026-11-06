# 奥地利足球超级联赛（Austrian Bundesliga）方法上下文报告

**请求**：ai-data-bus req-20261106-001（2026-11-06 发出）
**范围**：2012/2013–2025/2026，共 14 季；2026/2027 进行中（仅 42 场），已按请求排除
**核查日期**：2026-11-06（北京时间）
**口径**：只取足球事实，不含任何模型字段；只做赛前事实，不碰比分（赛果字段仅在 Q3/Q1 备注中引用赛季最终名次作背景，不输出逐场比分）／赔率值／预测。**禁止用日期或比分推断赛制**；每条赛制结论均注来源与获取时间，无源写 null。

## 交付物

| 文件 | 内容 | SHA-256 |
|---|---|---|
| `austrian_2025_26_rounds.csv` | 2025/2026 逐场表，192 行联赛＋表头 | `01e0d5b48980a6a40766803a9216d544d9fc8a1b2a68ebede2bc497321c960e4` |
| `austrian_format_clubs.md`（C 路） | Q1 逐季表＋Q3 十二队表＋Q6 说明 | — |
| `austrian_2025_26_rounds_notes.md`（D 路） | Q2／Q4／Q5 说明＋未覆盖清单 | — |
| `austrian_format_clubs_sources.md`（C 路） | 来源清单与未覆盖清单 | — |
| 本文件 | 合并报告（Q1–Q6） | — |

---

## Q1 逐季赛制（2012/2013–2025/2026）

| 赛季 | 球队数 | 官方轮次总数 | 每对交手次数 | 分裂制 | 积分减半 | 来源 |
|---|---|---|---|---|---|---|
| 2012/13 | 10 | 36 轮 | 4 次（主 2＋客 2） | 否 | 无 | simple.wikipedia 赛季页 |
| 2013/14 | 10 | 36 轮 | 4 次（主 2＋客 2） | 否 | 无 | simple.wikipedia 赛季页 |
| 2014/15 | 10 | 36 轮 | 4 次（主 2＋客 2） | 否 | 无 | EN Wikipedia 赛季页（抓取 2026-09-24 02:29 UTC；见方法注记） |
| 2015/16 | 10 | 36 轮 | 4 次（主 2＋客 2） | 否 | 无 | EN Wikipedia 赛季页（抓取 2026-09-09 11:03 UTC；见方法注记） |
| 2016/17 | 10 | 36 轮 | 4 次（主 2＋客 2） | 否 | 无 | simple.wikipedia 赛季页 |
| 2017/18 | 10 | 36 轮 | 4 次（主 2＋客 2） | 否 | 无 | simple.wikipedia 赛季页 |
| 2018/19 | 12 | 32 轮（常规赛 22＋决赛轮 10） | 常规赛每对 2 次；决赛轮同组再 2 次（同组对手全季 4 次，异组对手 2 次） | 是 | 有（减半，向下取整） | ÖFBL 官网 Ligaformat 页（2026-11-06 10:56 UTC 当日抓取）；bundesliga.at 2016-12-02 改革细则 |
| 2019/20 | 12 | 32 轮（同上） | 同上 | 是 | 有（减半，向下取整） | EN Wikipedia 2019–20 赛季页（抓取 2026-09-16）；全季 192 场 |
| 2020/21 | 12 | 32 轮（同上） | 同上 | 是 | 有（减半，向下取整） | ÖFBL 官网 Ligaformat 页（确认此赛制自 2018/19 起施行） |
| 2021/22 | 12 | 32 轮（同上） | 同上 | 是 | 有（减半，向下取整） | 同上 |
| 2022/23 | 12 | 32 轮（同上） | 同上 | 是 | 有（减半，向下取整） | 同上 |
| 2023/24 | 12 | 32 轮（同上） | 同上 | 是 | 有（减半，向下取整） | 同上 |
| 2024/25 | 12 | 32 轮（同上） | 同上 | 是 | 有（减半，向下取整） | 同上 |
| 2025/26 | 12 | 32 轮（同上） | 同上 | 是 | 有（减半，向下取整；**本季为最后一季**） | 德语维基 2025/26 赛季页（抓取 2026-08-30）；bundesliga.at 2025/26 赛季指南；全季 192 场＋3 场附加赛 |

**赛制要点**：
- 2012/13–2017/18：10 队、36 轮、四循环（每对 4 次，主 2＋客 2），每队 36 场，全季 180 场，无分裂、无减半。
- 2018/19–2025/26：12 队。常规赛 Grunddurchgang 22 轮双循环（每对 2 次，主客各 1）；22 轮后分裂，前 6 名进冠军组 Meistergruppe，后 6 名进降级组 Qualifikationsgruppe，每组再双循环 10 轮（第 23–32 轮）；每队全季 32 场，全季 192 场＋欧战附加赛。
- **积分减半口径（已裁决）**：常规赛积分在分裂时减半带入决赛轮，**向下取整（abgerundet）**；被向下取整的俱乐部在积分相同时排名靠前（半分作为第一 tiebreak）。
- **减半起止**：**2018/19 起实行，2025/26 为最后一季；自 2026/27 起废除**（2026/27 全额积分带入 Finaldurchgang，见 bundesliga.at 2026/27 Spielbetriebsrichtlinien §3b；2026/27 本身在本单范围外）。
- **裁决依据（官方源）**：bundesliga.at 2025/26 赛季指南、ÖFBL 2016 改革细则（bundesliga.at 2016-12-02《Die Details der Ligareform》）、德语维基 2025/26 赛季页 Modus 节、Sky Sport Austria 2026-05-09；**实证**：2019/20 赛季减半实例——Salzburg 48→24、Hartberg 29→14、Austria Wien 25→12，全部向下取整。**冲突方（不采信）**：austriabuliwetten.com 与 statsultra.com 称“向上取整（45 分变 23）”，为二级博彩站说法，与官方源及实证冲突。
- **2014/15 措辞注记**：该赛季页 Mode 节字面写“每对交手 2 次（主客各 1）”，与 36 轮／每队 36 场／全季 180 场的算术矛盾；2015/16 赛季页明确写“Each team played twice at home and twice away against every other team”。以 2015/16 的明确表述＋六季一致的算术为准，判定为每对 4 次；2014/15 页措辞视为笔误／半程描述，不单独采信。
- **2019/20 备注**：COVID 2020 年 3 月停摆、6 月恢复、2020-07-04 完赛，192 场踢满，赛制未变；LASK 纪律扣 12 分（后减为 4 分），扣分在减半前执行，属纪律处罚，非赛制变更。Mattersburg 赛季后破产退出（2020-08-05），WSG Tirol 因此免于降级。
- **2025/26 备注**：冠军 LASK（自 1965 年以来首冠）；BW Linz 降级；降级组胜者 SV Ried（28 分），WAC 同分第二；附加赛 3 场（见 Q2）。

---

## Q2 2025/2026 逐场官方轮次（192 行）

- **常规赛**：Grunddurchgang 第 1–22 轮，2025-08-01 至 2026-03-08，共 132 场。
- **分裂边界：第 22 轮结束后分裂，积分减半**。常规赛末轮 2026-03-08 六场同日进行。
- **分裂组**：Meistergruppe（冠军组，前 6 名：Sturm Graz、Red Bull Salzburg、LASK、Austria Wien、Rapid Wien、Hartberg）与 Qualifikationsgruppe（保级组，后 6 名：WSG Tirol、Altach、Ried、Wolfsberger AC、Grazer AK、BW Linz）各再打 10 轮（第 23–32 轮），每组 30 场；联赛总计 192 场。分裂后两组继续沿用第 23–32 轮编号，不重新编号。
- 末轮：冠军组 2026-05-17；保级组 2026-05-16。
- **唯一延期**：R4 Sturm Graz–WSG Tirol 原定 2025-08-24（Sturm 备战欧冠附加赛次回合 vs Bodø/Glimt），推迟至 2025-12-03 补赛；场地仍为默认主场 Merkur Arena（仅改期，不改场地）。
- **欧会杯附加赛（不属于联赛轮次，不在 CSV 内）**：半决赛 2026-05-19 Ried–Wolfsberger AC；决赛两回合 2026-05-22 Ried–Rapid Wien、2026-05-25 Rapid Wien–Ried。共 3 场，仅记录于此。
- **校验**：总行 192；常规赛每轮 6 场，分裂组每轮每组 3 场；每队 32 场（16 主／16 客）；(date, home, away) 无重复；日期范围 2025-08-01 → 2026-05-17。
- **来源与可信度**：主源 RSSSF Austria 2025/26 全量轮次表（`https://www.rsssf.org/tableso/oost2026.html`）；Simple Wikipedia 2025-26 赛季页核对 1–24 轮一致；bundesliga.at 赛季说明文（2025-07-31，确认第 22 轮后分裂、每组再打 10 轮）与决赛阶段赛程文确认分裂规则。**重要限定**：bundesliga.at 官方赛程页（/de/spielplan）文本层只有 JS 外壳、无赛程数据，官方轮次标签未逐场直接取自官方页；本表以 RSSSF＋Simple Wikipedia＋bundesliga.at 赛季说明文三重交叉为准。官方页逐场复核与开球时刻已列入未覆盖清单（U1/U2），实时浏览器复核正在进行，结果见最终回执补充。

---

## Q3 2025/2026 十二队生命周期

natal_year＝俱乐部成立年；competition_entry_year＝首次参加奥地利顶级联赛的赛季。两者不得混用。

| 球队 | natal_year（成立） | competition_entry_year（首次顶级联赛） | 备注（名称／法人变更） |
|---|---|---|---|
| SCR Altach | 1929-12-26 | 2006/07 | 1929 年为 Turnerbund Altach 足球部；1937 年一度解散，1946-03-01 重组，1949-03-05 足球部独立为 SC Rheindorf Altach；2005/06 获乙级冠军升级 |
| Austria Vienna | 1911-03-15 | 1911/12 | 前身 Wiener Cricketer（1910-10-20），1910 年 12 月改 Wiener Amateur-SV，1926-11-28 改名 FK Austria Wien；从未降级；首场联赛维也纳德比 1911-09-08 |
| BW Linz | 1997-07-02 | 2023/24 | 继承解散的 FC Linz 传统（FC Linz 因财政困难与 LASK 合并后解散）；2022/23 获 2. Liga 冠军升级；2020/21 也夺冠但未申请顶级联赛牌照；2025/26 后降级 |
| Grazer AK | 1902-08-18 | 1951/52（原始实体）；现凤凰实体 2024/25 | 原俱乐部 2012 年解散；球迷凤凰俱乐部 Grazer AC 随后成立，2014-03-14 宣布为原 GAK 的延续；2019/20 回职业联赛（乙级），2024/25 升回奥甲（时隔 17 年）。原始实体顶级联赛 50＋季：1951–1974、1975–1990、1995–2007；首场顶级联赛 1951-08-26 客场对 LASK（1:2） |
| TSV Hartberg | 1946-04-29 | 2018/19 | 2017/18 乙级第二，牌照申诉成功后升级 |
| LASK | 1899-08-07 | 1940/41（Gauliga Ostmark 时代）；战后全国联赛首季 1949/50 | 1899 年为 Athletiksportklub Siegfried；足球部 1908 年冬成立，1919-09-14 定名 Linzer Athletik-Sport-Klub；1997 年 5 月与同城 FC Linz 合并（名 LASK Linz 至 2017 年），俱乐部名称／颜色／主席／会员不变，延续性保留；2012 年因牌照被撤降入第三级，2013 年 12 月由本地企业家财团接手，同一法人延续 |
| SV Ried | 1912-05-05 | 1995/96 | 1912 年为 Sportvereinigung Ried；地区联赛踢至 1991 年首次升入全国联赛；1995 年首次升入顶级联赛 |
| SK Rapid Wien | 1899-01-08 | 1911/12 | 起源 1897 年 Erster Wiener Arbeiter-Fußball-Club；1899-01-08 改名 Sportklub Rapid；赢得首届奥地利全国冠军 1911/12；从未降级 |
| FC Red Bull Salzburg | 1933-09-13 | 1953/54 | 1933 年为 SV Austria Salzburg；1950 年解散后同年重建；1953 年升入顶级联赛。2005-04-06 Red Bull GmbH 收购并 rebranding，Mateschitz 宣称“这是没有历史的新俱乐部”，网站一度称成立于 2005 年，后被奥地利足协责令删除该说法，1933 年历史恢复。2005 年传统球迷另立的 SV Austria Salzburg 为**另一家独立俱乐部**，与本队无关 |
| SK Sturm Graz | 1909-05-01 | 1941/42（Gauliga Ostmark 时代）；战后全国联赛首季 1949/50 | 1909 年为 Grazer Fußballclub Sturm；1941 年取得 Gauliga Ostmark 资格，1941/42 赛季中途退出，次季第 11 名降级；1949 年作为首支非维也纳球队进入奥地利全国联赛；2006-09-01 税务机关申请破产，同一法人延续 |
| WSG Tirol | 1930 | 1969/70 | Wattens 实体：SC Wattens（1930–53）、SV Wattens（1953–71）、WSG Wattens（1984–2019）、WSG Swarovski Tirol（2019–21）、WSG Tirol（2021–）。1969–71 踢顶级联赛；1971–84 与 FC Wacker Innsbruck 合并为 SSW Innsbruck（该合并队 5 次夺 Bundesliga），期间俱乐部保留独立身份与青训队，SSW 的冠军归合并实体、**不单独计入 WSG**；1984 年起恢复独立参赛；2019 年以 2018/19 乙级冠军身份重返 Bundesliga。**WSG Tirol 是 Wattens 实体，不是 Wacker Innsbruck**，同名不同法人绝不合并 |
| Wolfsberger AC | 1931 | 2012/13 | 1931 年创立；2007–12 与邻队 SK St. Andrä 合作参赛（WAC/St. Andrä），两家俱乐部保持独立法人；2011/12 以合作队身份夺 First League 冠军升级，合作随后解散，WAC 以独立俱乐部身份首次踢顶级联赛；2014/15 起冠名 RZ Pellets WAC（赞助名） |

**完成度**：natal_year 12/12、competition_entry_year 12/12，缺 0 项。来源均为 EN Wikipedia 俱乐部页（抓取时间 2026-09-08 至 2026-11-06 不等，逐队见 C 路文件）＋ GAK 俱乐部官网历史页（grazerak.at，2026-11-06 搜索抓取）。LASK 与 Sturm Graz 的首次顶级联赛均在 Gauliga Ostmark 时代（纳粹德国兼并时期），报告中同时给出战后全国联赛首季以便口径清晰；Grazer AK 按原始实体与凤凰实体双层标注。

---

## Q4 2025/2026 实际比赛场地：偏离默认主场的场次

**结论：仅 1 家俱乐部、4 场联赛主场偏离默认主场**，全部为 TSV Hartberg 因 Profertil Arena 改建，赛季初临时迁至 Datenpol Arena（Bundesstadion Südstadt，Maria Enzersdorf）。其余 188 场均为默认主场。

| 轮次 | 日期 | 主场 | 客队 | 实际场地 | 城市 | 来源 |
|---|---|---|---|---|---|---|
| R3 | 2025-08-16 | TSV Hartberg | FC Red Bull Salzburg | Datenpol Arena (Bundesstadion Südstadt) | Maria Enzersdorf | bundesliga.at R3 前瞻（列 DATENPOL ARENA）；kicker 直播：Hartberg 因 Profertil Arena 改建须在 Südstadt 踢三个月 |
| R5 | 2025-08-31 | TSV Hartberg | SK Rapid Wien | Datenpol Arena (Bundesstadion Südstadt) | Maria Enzersdorf | deradmiraner.at：Hartberg 在“Exil Südstadt”迎战 Rapid；三场计划 Südstadt 主场之一 |
| R7 | 2025-09-20 | TSV Hartberg | Wolfsberger AC | Datenpol Arena (Bundesstadion Südstadt) | Maria Enzersdorf | ligaportal.at 战报：2025-09-20 17:00，Datenpol Arena Maria Enzersdorf/Südstadt；官方第三场 Südstadt 主场 |
| R12 | 2025-11-01 | TSV Hartberg | FK Austria Wien | Datenpol Arena (Bundesstadion Südstadt) | Maria Enzersdorf | kicker Spielinfo：2025-11-01 17:00，Stadion Datenpol Arena (Bundesstadion Südstadt)；标题称“Südstadt 最后一场主场” |

**计划与实际的出入（不抹平）**：赛季初计划仅 3 场在 Südstadt（Salzburg、Rapid、WAC），改建原定 11 月 1 日完工；ligaportal（2025-09-20，R7 当日）称 R7 是“官方第三场、据称也是最后一场”Südstadt 主场；但改建未按期完工，R12（2025-11-01 vs Austria Wien）仍在 Südstadt，kicker 称其为“letztes Heimspiel in der Südstadt”。以实际赛程为准：**共 4 场**。ligaportal 的“最后一场”指当时计划，kicker 的“最后一场”指实际最后一场；两者口径不同，交付物保留这一出入，不擅自调和。

**回迁**：R14 2025-11-22 vs SV Ried 已回 Profertil Arena；官方揭幕为 2025-11-30 R15 vs SK Sturm Graz。

**已核查的非偏离**：Sturm／GAK 共用 Merkur Arena 属赛季默认安排（12 队 11 座球场，客户端已核验），不算偏离；WSG Tirol 主场 Tivoli Innsbruck 为默认主场；R4 Sturm–WSG 补赛仅改期、场地仍为默认主场 Merkur Arena；LiveScore 曾把 2025-11-01 一场误标为 Profertil Arena（过期数据），以 kicker（Datenpol Arena）为准。范围仅联赛 192 场，ÖFB 杯场次未查。

---

## Q5 开盘 1X2 赔率可得性（Pinnacle／Bet365，明确标注 opening）

| 来源 | 开盘可得？ | 证据（2026-11-06 文本层实测） | 门槛／限制 |
|---|---|---|---|
| Football-Data AUT.csv | **不能** | 仅含收盘列 PSCH／PSCD／PSCA（Pinnacle 收盘）及 B365H／B365D／B365A 等收盘列；schema 中无任何开盘列（客户端已确认）。本轮尝试直取标准路径：先 302、跟随重定向后 404，未能独立复核表头——结论以客户端确认为准，直取失败如实记录，不谎称已复核。 | 无（但无开盘列） |
| OddsPortal | **可能（待实时浏览器确认）** | 赛季页文本层 200、561KB，含 "Opening odds" 字符串；其自述称单场页可查 opening odds 与全部赔率变动，赛季结果可回溯至 2003/04。 | 条款 §2.11 禁止未经书面同意的 scraping／aggregation：只可单场合规查阅，不可批量抓取。是否需登录看完整历史，文本层未证实，须实时浏览器核实。 |
| BetExplorer | **未定（待实时浏览器确认）** | 赛季页文本层 200、122KB；帮助文本称可看往场 archive odds；文本层未检出 "opening" 字样、0 处 Pinnacle。 | 单场页是否有带 opening 标注的赔率列，文本层无法证实，须实时浏览器核实。 |
| NowGoal／Goaloo | **不能（开盘不可得）** | 有 Initial 列，但 Initial＝数据流首次捕获，不是真实开盘（req-20261028-004 已确立教训）。例：Goaloo 2026-04-05 Rapid–Sturm 页。逐笔时间戳可证明某报价早于开球，但标签是 Initial，不得标 opening。 | 无（但无 opening 标签） |
| SoccerPunter | **不能（付费墙）** | 赔率历史为 Platinum 会员专属，Pinnacle 列为 Premium（req-20261028-004 已确认）。 | 须登录／付费；本单不登录、不购买、不订阅。 |
| FBref／Sportradar／thefishy 等 | **不能** | 无公开开盘赔率数据。 | — |

**Q5 结论**：文本层范围内，**没有任何来源能干净地取得带 opening 标注的 Pinnacle／Bet365 赛前开盘 1X2**。最有希望的合规路径是 OddsPortal 单场页（自述含 opening odds＋赔率变动，可回溯至 2003/04），但须实时浏览器确认实际显示与登录门槛，且受 §2.11 约束不得批量抓取。铁律执行：凡只有 closing 或单一中间价的，一律标 unavailable；未把 closing 当 opening，未把单一中间价当区间；未批量抓取 OddsPortal，未登录、未购买、未动用任何付费 API 额度。

---

## Q6 更早赛季（2012/2013–2017/2018）

六季全部四循环（10 队、36 轮、每对 4 次、180 场），无非标准双循环赛季，无分裂、无减半。

**赛中变更清单：无赛中变更。** 逐条核查：
1. 无 COVID 中断（疫情影响的是 2019/20 赛季，范围外）。
2. 无球队中途退出（六季中没有球队在赛季进行中退出或被逐出；每季 180 场比赛全部完成）。
3. 无场次取消导致赛制更改（六季均按 36 轮完整执行）。
4. 唯一相关事件（赛季后，非赛中）：2015/16 赛季末，排名最后的 SV Grödig 本应降级，但赛季结束后退出职业足球（未申请 First League 牌照），降入地区联赛。该事件发生在赛季结束后，不改变当季赛制与场次。
5. 改革决策时间点：2016 年 12 月 2 日官方公布 2018/19 改革细则（bundesliga.at《Die Details der Ligareform》），但改革本身自 2018/19 才执行，2017/18 仍按旧制完整进行。

范围外补充（仅作 Q1 备注，不计入 Q6）：2019/20 COVID 停摆 3 月、恢复 6 月、7 月 4 日完赛，192 场踢满，赛制未变；LASK 纪律扣 12 分（后减为 4 分）；Mattersburg 2020-08-05 赛季后破产退出，WSG Tirol 免于降级。

---

## 审计（audit）

| 项 | expected | discovered | complete | partial | missing |
|---|---|---|---|---|---|
| Q1 逐季赛制（14 季） | 14 | 14 | 14 | 0 | 0 |
| Q2 2025/2026 逐场轮次＋阶段标识 | 192 | 192 | 192 | 0 | 0 |
| Q3 十二队 natal_year | 12 | 12 | 12 | 0 | 0 |
| Q3 十二队 competition_entry_year | 12 | 12 | 12 | 0 | 0 |
| Q4 偏离默认主场场次 | 4 | 4 | 4 | 0 | 0 |
| Q5 开盘可得性（逐源） | 6 源 | 6 源 | 4（不能／付费墙／无开盘列，已定论） | 2（OddsPortal、BetExplorer 待实时浏览器确认） | 0 |
| Q6 更早赛季四循环／变更 | 6 季 | 6 季 | 6 | 0 | 0 |

注：Q2 的 192 行 complete 指轮次＋阶段标识＋日期＋主客队齐全；其来源为 RSSSF 主源＋双交叉，官方页逐场标签未直接取自官方页（见 U1），不影响行级完整计数，但来源等级在报告中如实降级说明。Q5 的 2 个 partial 待实时浏览器结果，见最终回执补充。

## 未解决队列（unresolved_queue）

见 `unresolved_queue.jsonl`（本目录）。分类（uq_class）：

- **U1（pending_work）**：官方赛程页逐场轮次标签——bundesliga.at/de/spielplan 文本层只有 JS 外壳；实时浏览器复核已派发，结果待补。
- **U2（pending_work）**：开球时刻（kickoff time）——CSV 只有比赛日；RSSSF 只给日期；须实时浏览器读 bundesliga.at。
- **U3（pending_work）**：OddsPortal／BetExplorer 单场页 opening 显示与登录门槛——文本层无法证实；实时浏览器核查已派发，结果待补。
- **U4（pending_work，低优先级）**：Football-Data AUT.csv 表头独立复核——本轮直取标准路径 404，未能独立复核；结论依赖客户端确认；不影响“无开盘列”结论（schema 本身无开盘列）。
- **U5（pending_work）**：2018/19–2024/25 七季未逐季重抓独立赛季页——赛制由 ÖFBL 官网 Ligaformat 页一句话覆盖（“自 2018/19 赛季起按此赛制进行”），属官方一手陈述；如需逐季独立佐证可补抓各季德语维基赛季页。
- **U6（pending_work，低优先级）**：2014/15、2015/16 两季的 EN Wikipedia 证据为 2026-09-24／2026-09-09 的缓存抓取，非 2026-11-06 当日新抓（C 路报告中“本轮新抓”措辞不准确，已在此合并报告中纠正）；历史赛季页内容静态，结论不受影响；如请求方要求当日检索戳，可重新抓取。
- **范围外（out_of_scope）**：2026/2027 赛季（进行中，按请求排除）；欧会杯附加赛 3 场（不属于联赛轮次，仅在 Q2 记录）；ÖFB 杯场次场地（未查）。

## 方法与局限

- 官方源优先：ÖFBL 官网（oefbl.at）Ligaformat 页与 bundesliga.at 赛季指南／改革细则为赛制与减半口径的裁决源；赛季页（EN／德语维基）为逐季场次与事件的佐证源；俱乐部页（EN 维基）＋俱乐部官网（grazerak.at）为 Q3 的来源；RSSSF 全量轮次表为 Q2 逐场表的主源。
- 2014/15、2015/16 两季的 EN Wikipedia 证据抓取时间为 2026-09-24／2026-09-09（缓存），非 2026-11-06 当日；其余赛季页抓取时间见 C 路 sources 文件（2026-09-08 至 2026-11-06 不等）。历史赛季页内容静态，结论不受影响；措辞已在此合并报告中如实纠正。
- 2018/19–2024/25 七季未逐季重抓赛季页（见 U5）。
- 客户端已解决项未重复抓：12 队 11 座球场名称／城市已核验、场馆 WGS84 已核验、时区 Europe/Vienna、90 分钟赛果由 AUT.csv 提供、收盘 1X2 仅 AUT.csv 的 PSCH／PSCD／PSCA 列。
- 未购买、未登录、未使用任何密钥／凭证、未动用任何付费 API 额度；未批量抓取 OddsPortal（条款 §2.11）；未写 repo/responses/（主代理的事）。

---

## 实时浏览器复核补充（2026-11-06 19:00–19:04 CST，主代理派发）

### 官方赛程页（U1 已解决）

- 官方 bundesliga.at 赛程页（`https://www.bundesliga.at/de/spielplan/saison-2025-2026`，站内赛季选择器切换到 2025/2026）在实时浏览器中**真实渲染逐轮数据，不是仅有 JS 外壳**。D 路“文本层只有 JS 外壳”的结论仅适用于文本层抓取，实时浏览器可读。
- 分界确认：常规赛止于第 22 轮（2026-03-08 周日，6 场同日 17:00）；自第 23 轮起积分榜分为两组，分组轮次为第 23–32 轮；第 32 轮为 2026-05-16–17。第 33–35 轮各仅 1 场（2026-05-19 Ried 2:1 WAC；05-22 Ried 2:1 Rapid；05-25 Rapid 3:0 Ried），赛程页未给这三轮标注阶段名——与 D 路“附加赛 3 场不属于联赛轮次”的处理一致。
- 阶段名原文：积分榜第 23 轮与第 32 轮的分组标题为 “MEISTERGRUPPE” 与 “QUALIFIKATIONSGRUPPE”；赛程（Spielplan）视图本身全文检索 “Grunddurchgang”“Meistergruppe”“Qualifikationsgruppe” 均无匹配，分组名称只出现在积分榜视图中。
- 减半口径佐证：积分榜脚注原文含 “jener Klub ist vorzureihen, bei dem nach dem Grunddurchgang bei Punktehalbierung abgerundet wurde”（常规赛后积分减半时被向下取整的俱乐部排名靠前）——与 Q1“向下取整”裁决一致，官方原文佐证。

### 开盘赔率单场页核查（U3 已解决）

样本场：Sturm Graz–SK Rapid，2026-05-17，2:0（未登录、未付费、未订阅、未批量抓取，各站只看这一场）。

- **OddsPortal：开盘可得（bet365，点按查看，无需登录）**。单场页（`https://www.oddsportal.com/football/h2h/rapid-vienna-rejcUFSs/sturm-graz-zsktjfsD/#4UFHgV5s`）默认 1X2 表只有 Bookmakers／1／X／2／Payout 列，无 “Opening odds” 静态列；点击 bet365 主胜赔率后弹出 “ODDS MOVEMENT” 提示框，原文 “Opening odds: 11 May, 16:00 2.05”，另显示 “17 May, 20:01 2.05 0.00”。页面右上角仍显示 LOGIN 按钮，未登录状态下内容完整可见。**Pinnacle：该场 “All Bookies” 1X2 表中未出现**（列出的为 1xBet、22Bet、888sport、bet-at-home、bet365、Betfury、BetInAsia、Bets.io、Betsson、Cloudbet、GGBET、Megapari、Melbet、Rainbet、Roobet、Stake.com，另有 Betfair Exchange）。单场证据，不推广为“Pinnacle 从不在 OddsPortal 奥甲出现”。
- **BetExplorer：开盘不可得**。单场页（`https://www.betexplorer.com/football/austria/bundesliga-2025-2026/sturm-graz-rapid-vienna/4UFHgV5s/`）只有 “Odds Comparison (1X2)” 表（Bookmakers／1／X／2），每家仅一个赔率值、旁有升降箭头，无开盘赔率数值、无 “Opening” 字样、无 archive odds 专区或标签；悬停 bet365 赔率无提示框；点击 bet365 赔率新开 bet365 联盟链接并返回 500 错误，未产生开盘赔率弹窗。**Pinnacle 同样未出现**。页脚原文：“Betting odds service provided in cooperation with OddsPortal.com”。
- **Q5 修正结论**：OddsPortal 单场页可合规查看 bet365 开盘（逐场点按、无需登录；受 §2.11 约束不得批量抓取）；Pinnacle 在样本场两站均未出现，Pinnacle 开盘本轮仍为 unavailable；BetExplorer 无开盘显示。NowGoal／Goaloo 的 Initial ≠ opening、SoccerPunter 付费墙的结论不变。

### U2 说明

Q2 请求本身只要求逐场 official_round＋阶段标识，不要求开球时刻；开球时刻未逐场提取，仍列为未覆盖（U2），不影响 Q2 交付。
