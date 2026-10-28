# req-20261028-003 说明：Veikkausliiga 精确 868 场身份联结（-002 的纠正单）

## 1. 输入核验（先于联结）

- 身份 CSV：`repo/work-req-20261028-003/fixture_identity_input.csv`，869 行（表头＋868 行），UTF-8 BOM 前缀、LF 行尾。
  - 按 LF 存储的 SHA-256：`e93a940b543f7257154166dc220295cc92b8d8f2fe4b46c1c347ac6564d0cf51`（与任务所述一致）。
  - 恢复 CRLF＋BOM 后 SHA-256：`9de8b8fac5fcdebbc51e1df99f9a5fe329e3149f3deacc2dfcc4105cd9a4c093`（与请求所称一致）。**内容已确认同一，仅行尾转换。**
  - 读 CSV 用 utf-8-sig，否则首列名带 BOM 读错；输出行的 CSV 身份字段（fixture_key、season、match_date、home_team、away_team、api_fixture_id）逐字照抄，BOM 不带入值。
  - CSV fixture_key 格式：`veikkausliiga|赛季|日期|小写缩写`（如 `veikkausliiga|2016|2016-08-07|hjk|lahti`）；fixture_key 缩写与 home_team／away_team 列逐行一致（缩写＝队名去空格小写，868／868），但与合并行键格式不同，**禁止字符串直连**。
  - CSV 无重复 fixture_key、无重复 api_fixture_id；868 行按赛季：2016：34、2017：83、2018：108、2019：68、2020：68、2021：109、2022：116、2023：112、2024：89、2025：66、2026：15。
- -004 行工件：`repo/work-req-20261006-004/req-20261006-004-rows.json`（1,131 行，2019–2025）。
- -002 合并行：`work-req-20261028-002/method_context_rows_merged.jsonl`（1,902 行，2016–2026）＋`merge_notes.md`（合并口径以该文件为准，本单不再改写）。

## 2. 联结方法（联结键＋别名表＋验证）

- 联结键：**（season, match_date, home_team, away_team）**，队名经赛季别名表映射。CSV 队名是短名（如 HJK、Lahti、PS Kemi），合并行队名按季／按路写法差异极大（见 §3 别名表全文）。
- 命中规则：别名映射后的主客队在同季同日合并行中**恰好命中唯一一对**才算联结；0 命中或 ≥2 命中一律记 unresolved，证据字段全 null，行本身不删除、不新增场次、不凭印象选。
- 别名表推导与验证（非凭印象）：
  1. 每季 CSV 短名集合与合并行队名集合先对齐（字符串关系：全等／去 FC 前缀／括号内短名／城市前缀／首字母缩写，如 Helsinki IFK→HIFK、Kuopion PS→KuPS、Turun Palloseura (TPS)→TPS）。
  2. 同日同季共现消歧：对每行 CSV，映射后应在同季同日合并行中恰好命中唯一一对。
  3. 唯一性反证：对每个（赛季，短名），逐一试该季其他全部合并行队名作为替代映射——**没有任何一个替代映射能对其全部行同样给出恰一命中**（歧义项 0 个）。即别名表被数据唯一确定，不是猜出来的。
  4. 单射复核：没有一行合并行被两行 CSV 同时认领（0 次重复认领）。
- -004 交叉优先：2019–2025 的联结行先标 matched_004_fixture_key（合并行 B／C 路的键与 -004 键逐字同一，623／623 全部在 -004 文件中找到，失败 0）；另附 -004 原值快照（date、kickoff、时区、official_round、venue、city），使 -002 的修正（开球 ＋2h、2020 日期纠正、Gnistan 火灾易地）在行内可见。2016–2018、2026 共 240 行标 out_of_004_scope（-004 只覆盖 2019–2025）。

## 3. 别名表全文（CSV 短名 → 合并行队名，按赛季）

| 赛季 | 别名映射 |
|---|---|
| 2016 | HIFK→Helsinki IFK；HJK→HJK Helsinki；Ilves→Ilves；Lahti→Lahti；Mariehamn→IFK Mariehamn；PS Kemi→Kemi Kings；SJK→SJK；VPS→VPS |
| 2017 | HIFK→Helsinki IFK；HJK→HJK Helsinki；Ilves→Ilves；Inter Turku→Inter Turku；KuPS→KuPS；Lahti→Lahti；Mariehamn→IFK Mariehamn；PS Kemi→Kemi Kings；SJK→SJK；VPS→VPS |
| 2018 | HJK→HJK Helsinki；Honka→FC Honka；Ilves→Ilves；Lahti→Lahti；Mariehamn→IFK Mariehamn；PS Kemi→Kemi Kings；SJK→SJK；TPS→TPS；VPS→VPS |
| 2019 | HIFK→Helsingfors IFK；HJK→HJK Helsinki；Honka→FC Honka；Ilves→Ilves Tampere；Lahti→FC Lahti；Mariehamn→IFK Mariehamn；SJK→SJK Seinäjoki；VPS→Vaasan PS |
| 2020 | HIFK→Helsingfors IFK；HJK→HJK Helsinki；Haka→Haka Valkeakoski；Honka→FC Honka；Ilves→Ilves Tampere；Lahti→FC Lahti；Mariehamn→IFK Mariehamn；SJK→SJK Seinäjoki；TPS→TPS Turku |
| 2021 | AC Oulu→AC Oulu；HIFK→Helsingfors IFK；HJK→HJK Helsinki；Haka→Haka Valkeakoski；Honka→FC Honka；Ilves→Ilves Tampere；KTP→KTP；Lahti→FC Lahti；Mariehamn→IFK Mariehamn；SJK→SJK Seinäjoki |
| 2022 | AC Oulu→AC Oulu；HIFK→Helsingfors IFK；HJK→HJK Helsinki；Haka→Haka Valkeakoski；Honka→FC Honka；Ilves→Ilves Tampere；Inter Turku→Inter Turku；Lahti→FC Lahti；Mariehamn→IFK Mariehamn；SJK→SJK Seinäjoki；VPS→Vaasan PS；**TPS→（无合并行队名，2022 年 TPS 不在顶级联赛，见 §5 零命中行）** |
| 2023 | AC Oulu→AC Oulu；HJK→HJK；Haka→Haka；Honka→Honka；Ilves→Ilves；KTP→KTP；Lahti→Lahti；Mariehamn→Mariehamn；SJK→SJK；VPS→VPS（合并行本季即用短名，全等） |
| 2024 | AC Oulu→AC Oulu；Gnistan→Gnistan；HJK→HJK；Haka→Haka；Ilves→Ilves；Lahti→Lahti；Mariehamn→Mariehamn；SJK→SJK；VPS→VPS（全等） |
| 2025 | AC Oulu→AC Oulu；Gnistan→Gnistan；HJK→HJK；Haka→Haka；Ilves→Ilves；KTP→KTP；Mariehamn→Mariehamn；SJK→SJK；VPS→VPS（全等） |
| 2026 | AC Oulu→AC Oulu；Gnistan→IF Gnistan；HJK→HJK Helsinki；Ilves→Ilves；Lahti→FC Lahti；Mariehamn→IFK Mariehamn；SJK→SJK Seinäjoki；TPS→Turun Palloseura (TPS)；VPS→Vaasan Palloseura (VPS) |

- **别名表有无歧义项：无。** 唯一性反证 0 项歧义（见 §2 第 3 步）。注意两处跨季同名不同映射（HIFK：2016–2018→Helsinki IFK，2019–2022→Helsingfors IFK；PS Kemi 仅 2016–2018 出现→Kemi Kings），均按赛季分开，不可跨季混用。
- 脚本：`join_868.py`（可复跑，含 -004 对应校验、单射复核、唯一性反证）。

## 4. 联结结果与按赛季计数

- **恰一命中 863 行、零命中 5 行、多命中 0 行**（合计 868）。
- 输出：`method_context_rows_868.jsonl`（恰 868 行，与 CSV 同顺序），SHA-256 `0e10f60e21419766e3bfd4ab72b421f2005d03b07a3170ed3b6e547d9135be8d`。
- 按赛季计数（expected＝CSV 行数；discovered＝恰一命中；complete／partial／conflict 取联结到的合并行 row_status_merged；missing＝expected－discovered；unavailable／blocked 均为 0）：

| 赛季 | expected | discovered | complete | partial | conflict | unavailable | blocked | missing |
|---|---|---|---|---|---|---|---|---|
| 2016 | 34 | 34 | 31 | 3 | 0 | 0 | 0 | 0 |
| 2017 | 83 | 83 | 37 | 4 | 42 | 0 | 0 | 0 |
| 2018 | 108 | 108 | 63 | 11 | 34 | 0 | 0 | 0 |
| 2019 | 68 | 68 | 68 | 0 | 0 | 0 | 0 | 0 |
| 2020 | 68 | 68 | 66 | 0 | 2 | 0 | 0 | 0 |
| 2021 | 109 | 109 | 108 | 0 | 1 | 0 | 0 | 0 |
| 2022 | 116 | 111 | 21 | 90 | 0 | 0 | 0 | 5 |
| 2023 | 112 | 112 | 112 | 0 | 0 | 0 | 0 | 0 |
| 2024 | 89 | 89 | 88 | 0 | 1 | 0 | 0 | 0 |
| 2025 | 66 | 66 | 0 | 66 | 0 | 0 | 0 | 0 |
| 2026 | 15 | 15 | 0 | 9 | 6 | 0 | 0 | 0 |
| 合计 | 868 | 863 | 594 | 183 | 86 | 0 | 0 | 5 |

## 5. 零命中 5 行（全部 2022 年 10 月，联赛结束之后）

| fixture_key | 原因 |
|---|---|
| veikkausliiga\|2022\|2022-10-19\|sjk\|acoulu | 该日无任何合并行；合并行 2022 联赛宇宙止于 2022-10-16（第 27 轮） |
| veikkausliiga\|2022\|2022-10-20\|tps\|lahti | 同上；且 TPS 在合并行 2022 年无顶级联赛队名（次级联赛球队） |
| veikkausliiga\|2022\|2022-10-22\|acoulu\|vps | 同上 |
| veikkausliiga\|2022\|2022-10-26\|vps\|haka | 同上 |
| veikkausliiga\|2022\|2022-10-30\|haka\|vps | 同上 |

- 诊断（不构成联结依据）：这 5 行是 CSV 中仅有的、落在“当日零合并行”日期上的行；其余 863 行所在日期均有合并行。5 行的主客对在合并行 2022 年其他日期均存在（如 SJK–AC Oulu 在 2022-07-31、AC Oulu–VPS 在 2022-07-02），但日期不同——日期是联结键的一部分，**不许按对赛跨日期推断联结**，故仍记零命中。TPS–Lahti 2022-10-20 与升降级附加赛时间吻合，但本单不作此断言（其余 4 行在合并行联赛宇宙内也无解释），须请求方裁决：是附加赛／杯赛／其他赛事混入，还是日期有误。
- 多命中行：0 行（同日同季同对在合并行中从不重复出现，与合并文件 0 重复键一致）。

## 6. 键日期不一致的特例（不是联结错误，须向请求方明示）

- `veikkausliiga|2020|2020-09-20|honka|hjk` → 联结到合并行 `2020|2020-09-19|FC Honka|HJK Helsinki`。
  - 原因：-002 的 B 路对 2020 年 2 行日期纠正时**保留了 -004 原 fixture_key**（键内嵌 -004 的错误日期 2020-09-19），纠正值记在 match_date（2020-09-20）与 date_as_in_req20261006_004（2020-09-19）。联结键用的是 match_date（2020-09-20），与 CSV 日期一致，故正确命中；但输出的 matched_merged_fixture_key 键内日期（09-19）与 match_date（09-20）不一致——这是 -004 键保留策略的遗留，不是本单联结错误。行内同时可见：-004 开球 18:30 → 合并行开球 13:00 Europe/Helsinki（UTC 10:00），轮次 15 不变，该行 merged 状态为 conflict（B 路 2020 年分歧行之一）。
  - 另一纠正行 HIFK–RoPS（-004 2020-11-04 → 实际 2020-10-22）**不在 868 子集内**（CSV 2020 年无 RoPS 行），故本单不受其影响。

## 7. meeting_number（全库 null，不可误读）

- 863 行联结行 meeting_number 全部 null（-002 已证实无权威定义）。
- D 路 169 个顺序计数中，868 子集命中 15 行（2026 子集 15 行全部有值，8 个计数分歧行 KuPS–Oulu／HJK–Inter 不在子集内），仅放进 `meeting_number_schedule_order_count_unverified` 参考字段并附警告：**不得当 meeting_number 用**（其 basis 自述就是球队出现次数计数，正是请求禁用的推断口径）。

## 8. 弱源字段清单（863 行联结行内统计）

| 字段／口径 | 弱源行数 | 说明 |
|---|---|---|
| official_round 为 null | 91 | 2022 常规赛 90＋2021-09-14 Ilves–HIFK 1（见 -002 U-02／U-03） |
| official_round 非官方措辞 | 772（其余全部） | 全部轮次值 official_round_is_official=false（Soccerway／worldfootball／FBref／topscorersfootball 标签，无一行联赛官方 KIERROS 措辞） |
| venue 官方确认 | 0／863 | venue_official_confirmation 全 false；confirmed 803＋moved 19 均为 FBref 二级来源 |
| venue 未验证／竞争 | 41 | unavailable 34（A 路身份未解析＋D 路赛季表候选）＋conflict 7（竞争候选，无一选边） |
| kickoff 为 null | 15 | 全部为 2026 子集行（源只给日期） |
| kickoff 未决分歧 | 66 | 全部为 2025 子集行（保留 -004 值、FBref 系统性 ＋2h、UTC withheld） |
| kickoff 分歧（已决／未决） | 2 | 2020 子集 2 行（HJK–Ilves、Honka–HJK，B 路分歧行） |
| round_conflict | 77 | 2017 42＋2018 34＋2021 1（FBref Wk 标签异常，原文保留） |
| competition_entry_year 为 null | 主队 860／863、客队 861／863 | 仅 2026 升班 Lahti／TPS 相关行有值（主队 3、客队 2）；其余一律 null 不猜 |
| 2016–2018 行字节 provenance | 225／225 为 null | FBref 源字节被 Cloudflare 拦截（curl 000／scrapling 403／curl_cffi 403），证据为浏览器文本层转录（见 -002 §5） |
| -004 对应 | 623 行 matched、240 行 out_of_004_scope | 2019–2025 联结行 -004 对应失败 0 行 |

## 9. 未解决队列

- `unresolved_queue_868.jsonl`：274 项（join_zero_hit 5＋carried_gap 269）。
  - 按维度：official_round 91、merged_conflict 86、kickoff 81（null 15＋分歧 66）、venue 41、join 5（同一行可含多维度，不重复计数行数）。
  - 按赛季：2022：95、2025：66、2017：46、2018：45、2026：15、2016：3、2020：2、2021：1、2024：1。
  - 系统项（不按行展开，见 §7／§8）：meeting_number 全库 null；official_round 全库非官方；venue 官方确认全库 0；competition_entry_year 绝大多数 null；2016–2018 行字节 provenance 全 null。
- 2022 年 90 行轮次缺失的下一步（沿用 -002 结论）：真浏览器读 Soccerway ROUND 分组；WorldFootball 分页与 FBref Wk 桶已证伪，不可再用。

## 10. 自验结果（脚本复核，全部通过）

- 输出行数＝868，与 CSV 同顺序，fixture_key 与 CSV 逐字节一致且顺序一致（逐行比对通过）。
- 无重复 fixture_key（868 唯一），无新增场次（输出 fixture_key 集合＝CSV 集合）。
- CSV 身份字段逐字照抄：season、match_date、home_team、away_team、api_fixture_id 逐行与 CSV 一致。
- 联结行 matched_merged_fixture_key 全部存在于 -002 合并文件（863／863）；2019–2025 联结行 -004 对应全部找到（623／623）。
- 单射复核：无合并行被两行 CSV 认领。
- 禁字段键扫描（比分／赛果／观众／裁判／进球／盘口／赔率／预测／积分／bookmaker／score／odds／prediction／standings／goals）：0 命中。
- 未写 repo/responses/；未购买、未登录、未使用任何密钥／凭证、未动用付费 API 额度。
- 输出文件 SHA-256：`0e10f60e21419766e3bfd4ab72b421f2005d03b07a3170ed3b6e547d9135be8d`。
