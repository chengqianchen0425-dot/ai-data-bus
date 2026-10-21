# req-20261021-001 交付报告：Copa Libertadores 2018–2025 行级 pre-match fixture 数据集

## 结论先行

- **行级 fixture 共 2,506 行，按源分开保存，未做跨源单行合并。** 其中只有 **38 行是 CONMEBOL 官方 PROGRAMA PDF 的 pre-match 合格行**；其余 2,468 行是候选源行（FBref、SoccerAssociation），它们的页面本身是赛后修订/结果页，按请求 Q3 的严格规则**不能算作开球前发布的 pre-match 源**，只能作候选 fixture 上下文。
- **不要把 2,506 行当成 2,506 场比赛。** 三源覆盖的是同一批比赛的不同呈现：FBref 唯一场次 1,241 场，SoccerAssociation 1,227 行，官方 38 行。跨源队名写法差异太大（缩写、州码、改名、同名 Nacional），按队名强行拼成单行会造假身份，故按源分开是本单最诚实的结构。
- **expected（应有场次数）全程 null。** 本单没有任何权威源公布各季/各阶段应有场次数，1,241、1,227 等都是“发现数”，不是“应有数”，不得用作分母算覆盖率。

## 按源 × 赛季行数

| 赛季 | CONMEBOL 官方 | FBref 呈现 | FBref 唯一 | SoccerAssociation | RSSSF 阶段行 |
|---|---|---|---|---|---|
| 2018 | 0 | 282 | 156 | 150 | 15 |
| 2019 | 0 | 280 | 155 | 155 | 15 |
| 2020 | 0 | 280 | 155 | 155 | 15 |
| 2021 | 0 | 280 | 155 | 155 | 15 |
| 2022 | 30 | 280 | 155 | 147 | 15 |
| 2023 | 0 | 280 | 155 | 155 | 15 |
| 2024 | 8 | 280 | 155 | 155 | 15 |
| 2025 | 0 | 280 | 155 | 155 | 0 |
| 合计 | 38 | 2,242 | 1,241 | 1,227 | 105 |

## 对账算术（全部闭合）

- FBref：2,242 次呈现 → 按 (season, date, time, home, away) 源内去重 → **1,241 唯一场次**；1,001 次重复呈现，每组恰好重复 2 次（All Rounds 表 + 阶段分表），时间/球场在重复组内完全一致，唯一差别是小组赛分表行 round 为 null（已用同页 All Rounds 行的 Group stage 补齐，同源非冲突补全）。
- FBref 与 SoccerAssociation 按阶段逐项相等，**只差两处**：2018 第二资格赛 SA 页内只有 10 行（他季 16 行），2022 第三资格赛 SA 页 429 被墙 0 行；14 = 6 + 8，恰好等于两源总数差（1,241 − 1,227）。
- 官方 38 行按阶段落在 FBref/SoccerAssociation 的对应阶段数上：2022 三轮资格赛 6/16/8、2024 四分之一决赛 8。
- FBref leg 非空 466 行 = 资格赛 240 + 淘汰赛两回合 224 + 2018 决赛两回合 2；2019–2025 单场决赛 leg 为 null（源内无 Leg 标注，不据此推断单场属性）。
- RSSSF 105 行是**阶段结构行，不是逐场行**（无主客队），只用于核对阶段划分存在性，不得计入场次。

## 官方覆盖（纠正上一路审计的算术错误）

- 官方 PROGRAMA PDF 覆盖 **4 / 64 个赛季×阶段组合**（8 季 × 8 阶段），不是 A 路审计写的 4/56；**缺 60 个组合，不是 52 个**（A 路列出的缺失清单本身是 60 项，总数写错了，本单按 64/4/60 纠正）。
- 已验证的 3 份 PDF：2022 Fase 1/2（版本 28/01/2022）、2022 Fase 3（版本 04/03/2022）、2024 Cuartos（页眉 26/8/2024），版本日期均早于各自全部开球日，version_eligibility=confirmed。
- 官方行口径：source_fixture_id 是 PDF 内 # 列，**只在该阶段文档内有效，不假设跨文档全局唯一**；2022 Grupo 列是资格赛 slot 编码（E/C/G），不是小组赛字母；2024 Llave S1–S4 是淘汰赛对阵编号；6 行 Fase 2 行在版本发布时对手还是占位符 E1/E2/E3（胜者未产生），原文保留、绝不回填真实队名；3 行 partial（球场或本地时间为 A definir/空）。
- 2022 Fase 1/2 PDF 页脚注：球场为俱乐部申报、待 CONMEBOL 最终确认。

## 字段口径（不按这些口径用，数据就会被误读）

- **kickoff_utc 只是 GMT 列的时刻字符串**（如 00:30），源未给 UTC 日期。GMT 时刻落在次日时，**绝不能把 match_date + GMT 时刻拼成完整 UTC 时间戳**。
- **official_round 的含义随源而异**：FBref = 小组赛 Wk（1–6），其余轮次为空；SoccerAssociation = 轮次码原文（Q1/R1 等）；CONMEBOL = Ida/Vuelta（与 leg 同义，leg 已统一译为 first/second，原文保留在 leg_verbatim）。
- **group_id**：只有官方 2022 行有 Grupo 值；FBref 全空；SoccerAssociation 的 Group 1–8 只存在 group_label_verbatim 里，**绝不映射为 A–H**。
- **tie_id**：只有官方 2024 Cuartos 行有 Llave（S1–S4）；其余全空。
- **city / country / source_timezone_text**：FBref、SoccerAssociation 页根本没有这些列，全空，不从球场或队名推断。
- **venue_latitude / venue_longitude**：全部 2,506 行为空，没有任何引用源直接提供坐标。
- **single_match_knockout / scoring_mode**：全部行为空。本单行级源没有逐场明确写出单场/两回合或计分赛制，不从“无 Leg 标注”反推单场。
- **FBref 球场截断**：111 次呈现（60 个唯一场次）的球场以 … 结尾，原文照抄、未补全。
- **SoccerAssociation 异常原文**：2020 年 4 行日期标题为不存在的 “31 September 2020”，match_date 置空、原文保留在 date_source_text；2020 R2/QF 各有 1 行首回合行码出现在次回合日期标题下，未重排；2021 R1 Group 6 有两个不同队伍同标 Nacional（站内仅以旗帜区分，旗帜不是任务字段），未强行区分。
- **source_sha256**：全部行为空。官方 PDF 因本机直连 cdn 超时未取得字节（走浏览器文本层读全文）；网页源无稳定字节哈希，均未编造。官方 sha256 待可直连环境重下补算（见 UQ）。

## 赛制上下文（仅作背景，不属于行级证据）

以下来自上一单 req-20261019-001 的源映射，不写入任何 fixture 行的赛制字段：2018 决赛为两回合（总比分 5:3、加时、伯纳乌）；2019 起决赛为单场；2020 赛季延期至 2021 年 1 月（半决赛 1 月 5–6 日）；2022 赛季因卡塔尔世界杯压缩（决赛 10 月 29 日瓜亚基尔）。如需把赛制写进行级字段，需另行逐场引用官方赛制文件。

## 未解决队列（13 项，见 unresolved_queue.json）

- source_missing：官方 60 个组合；SoccerAssociation C 页 8 季（PAGE ERROR，C 含义未确认）；RSSSF 2025 页未找到。
- pending_work：5 份被第三方引用证实存在但未找回 cdn 直链的官方 PDF（跟随维基引用链接是下一步）；2025 Planilla 裁判表是否计入官方源待请求方决定；2018 Q2 页完整性；FBref 球场截断补全；2020 无效日期 4 行的真实日期；官方 PDF sha256 重下补算。
- access_blocked：SoccerAssociation 2022 Q3 页（429），retry_after 2026-10-28。
- permanent_rule：经纬度；FBref/SoccerAssociation 的城市/国家/时区/小组字母/对阵 ID（源无此列、规则禁推断）；跨源队名拼合（须有权威俱乐部身份映射表才可做，本单不做）。

## 交付文件（repo/work-req-20261021-001/）

fixture_rows.jsonl（2,506 行，按源拼接）＋ fixture_rows_conmebol.jsonl / fixture_rows_fbref.jsonl / fixture_rows_soccerassoc.jsonl ＋ rsssf_stage_rows.jsonl（105 行阶段行）＋ audit.json ＋ unresolved_queue.json ＋ report.md（本文件）。回执 data.fixture_rows 与 fixture_rows.jsonl 内容一致。
