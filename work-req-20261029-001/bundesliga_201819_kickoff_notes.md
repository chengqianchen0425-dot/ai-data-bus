# req-20261029-001 A 路交付说明：德甲 2018-19 赛季 306 场官方开球证据（字节级 provenance 升级）

## 1. 交付

- `bundesliga_201819_kickoff_rows.jsonl` —— 306 行，SHA-256 `f34222a35bc03178f195edab6153d4183047677adc41ead913ea27722b11f2dd`
- `evidence/` —— 5 个 DFL 官方 PDF 字节文件＋DFL 公告 HTML＋`hash_index.md`（逐文件 HTTP 状态／字节数／SHA-256）＋pdftotext 解析文本
- `parse_pdfs.py`、`build_rows.py`、`parse_audit.json`（可复跑）
- 本文件（说明）＋ `unresolved_queue.jsonl`（见 §5）

## 2. 逐源覆盖表（5 个候选 URL 全部 200，全部实采字节）

| # | 源 | URL | HTTP | 字节 | SHA-256 | 联赛行 | 轮次 |
|---|---|---|---|---|---|---|---|
| ① | DFL Ansetzungen | media.dfl.de/sites/3/2018/11/Bundesliga_2018-19_Spieltage_1-6.pdf | 200 | 304,723 | 1475b472…45743 | 54 | 1–6 |
| ② | DFL Ansetzungen | media.dfl.de/sites/3/2018/11/Bundesliga_2018-19_Spieltage_7-14.pdf | 200 | 460,469 | 40914ef8…fab64 | 72 | 7–14 |
| ③ | DFL Ansetzungen | media.bundesliga-gruppe.de/sites/2/2018/11/Bundesliga_2018-19_Spieltage_15-21-1.pdf | 200 | 420,296 | 6ee3f3e6…7029 | 63 | 15–21 |
| ④a | DFL 公告（网页） | www.bundesliga-gruppe.de/aktuelles/dfl-terminiert-spiele-der-bundesliga-und-2-bundesliga-bis-zum-28-spieltag/ | 200 | 81,922 | 235eda9c…6f79 | —（非逐场源） | — |
| ④b | DFL Ansetzungen（公告所链 PDF） | media.bundesliga-gruppe.de/sites/2/2018/12/BL-MD-22-28.pdf | 200 | 508,101 | bfedcdc3…88174 | 63 | 22–28 |
| ⑤ | DFL Ansetzungen | media.dfl.de/sites/2/2019/03/Bundesliga_Spieltage_29-34.pdf | 200 | 434,986 | 7d309563…c8b | 54 | 29–34 |
| 合计 | | | | | | 306 | 1–34（每轮 9 场） |

- **④ 的核实结论**：公告本身是网页，只给示例开球（Nürnberg–Dortmund 周一 20:30、Augsburg–Bayern 周五 20:30、Bayern–Dortmund 第 28 轮周六 18:30），不是逐场源；但公告页内链的官方 PDF `BL-MD-22-28.pdf`（"Spieltage 22 bis 28 der Bundesliga"，19.12.2018）就是逐场官方源。本轮 22–28 轮 63 行全部改用该 PDF，**-007 的 63 行 FBref 源至此全部升级为官方源，不再保留 FBref 行**（每行 `source_upgrade_note` 写明升级过程与核验结果：开球与日期与 -007 值逐一相同）。
- 解析口径：只取 Spieltag 列为数字的联赛行（UEL／UCL／DFB／DFL-SC／UEFA／REL 等非联赛行全部排除）；队名按 18 支德甲球队官方德语名精确切分；解析过程曾漏 33–34 轮 18 行，原因是该 PDF 的时间分隔符是冒号（15:30）而非其它 PDF 的点号（15.30），已修正正则并复核 306／306 行无遗漏、无重复键、无无法解析行。
- 第 33 轮核验：第 33 轮 9 场全部 11.05.2019 周六 15:30，与 -007 记载一致。

## 3. 时区说明

- 全部行 `timezone="Europe/Berlin"`（IANA）。PDF 所载时间为德国当地墙钟时间。
- `kickoff_utc` 为换算值（方法写在每行 `kickoff_utc_method`）：用 IANA 时区库换算，2019-03-31 02:00 前 CET＝UTC+1、之后 CEST＝UTC+2；UTC 值是派生换算，绝不冒充源值。本季 306 行中 CET 163 行、CEST 143 行；无任何开球落在 03-31 02:00–03:00 不存在时段内。
- -007 回执的 306 行 timezone 全为 null、source_sha256 全为 null；本轮两项全部补齐（timezone 306／306，source_sha256 306／306 非 null）。

## 4. 与 -007 的交叉核验结果

- 身份键沿用 -007 格式（`2018-19|DD/MM/YYYY|Home|Away`，Football-Data 短队名照抄，包括 "Ein Frankfurt" 这一截断式短名，不擅自改名）。
- PDF 解析 306 行与 -007 306 行按（轮次、主队、客队）逐一对应：**开球 306／306 一致，日期 305／306 一致**。
- 唯一不一致就是已知冲突（见 §5），**无新冲突**。FBref 实际赛程值与 DFL 公布值全面一致，说明公布开球在赛季中未发生事后变更（PDF 为 2018 年 11 月／12 月／2019 年 3 月分批公布的 Ansetzungen；若赛季中有临时改期，FBref 实际值会与之不符——本轮未发现此类情况）。

## 5. 冲突清单（两值并存，不自动取舍）

| fixture_key | 冲突 | -007 已有处理 | 本轮处理 |
|---|---|---|---|
| `2018-19\|12/05/2019\|Ein Frankfurt\|Mainz` | Football-Data 日期 12/05/2019 vs DFL 官方 11.05.2019（第 33 轮，周六 15:30 九场同开） | `official_match_date="11/05/2019"`＋`date_note` 已记录 | 原样保留两值；行 `conflict_flag="date_key_vs_official"`；进 unresolved_queue（U-01） |

## 6. 基线说明（D1.csv）

- 请求所引本地 D1.csv（Windows 路径，SHA-256 f03ee41b…）在本 VM 上不存在（本机只有 2024/25、2025/26 的 D1.csv 副本，无 2018-19 版），故无法与该文件逐行比对。
- 本轮联结以（赛季、日期、主队、客队）＋官方 PDF 为准；D1.csv 精确比对列为未解决项 U-02（须请求方提交文件或确认派生集），未伪造任何对应关系。

## 7. 自验结果

- 行数 306，无重复键；`source_sha256` 非 null 306／306；`timezone` 非 null 306／306；官方源（`source_tier=official_dfl`）306／306；FBref 源 0 行；禁字段键（比分／赔率／模型／预测）扫描 0 命中。
- 未购买、未登录、未使用任何密钥／凭证、未动用付费 API 额度；未写 repo/responses/。
