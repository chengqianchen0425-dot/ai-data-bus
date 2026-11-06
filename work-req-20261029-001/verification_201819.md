# req-20261029-001 B 路独立验证报告：德甲 2018-19 赛季 306 场开球证据

- 验证方：B 路（独立验证与审计，不重复 A 路提取）
- 验证时间：2026-11-06（CST）
- 基线：req-20261003-007（306 行，`responses/req-20261003-007.json`）
- A 路交付物：`bundesliga_201819_kickoff_rows.jsonl`（306 行，SHA-256 `f34222a35bc03178f195edab6153d4183047677adc41ead913ea27722b11f2dd`）
- 本文件方法：全部结论由 B 路独立重算／重下载／重转录得出，不抄 A 路结论；差异两值并存，不自动取舍。

## 结论先行

- **D1.csv 找到了**（推翻任务简报前提，也推翻 A 路 unresolved U-02）：`~/workspace/ai-inbox/work-bundesliga-014/raw/D1-1819.csv`，SHA-256 与请求所引值**逐字节一致**（`f03ee41b741aca9c43cbafb800bbc6f01ca9d7ed19c1a9dd4c309389280cfe11`）。精确比对已完成，不是 pending：D1 vs -007 键／日期 0 差异；D1 vs FBref 日期 0 差异。
- **5 个候选 URL 全部独立验证通过**：4 份 DFL PDF 均 HTTP 200、真实 PDF，B 路独立下载的哈希与 A 路 evidence/ 文件逐字节一致；公告页 HTTP 200 但**本身不含逐场开球**（仅 3 个示例），其所链官方 PDF `BL-MD-22-28.pdf` 是逐场源——**22–28 轮替代官方源成立**，A 路 63 行改用该 PDF 正确。
- **第二源比对（FBref 全表转录 306 行＋worldfootball＋B 路独立 PDF 解析）**：除已知冲突 Frankfurt–Mainz 外，**新增冲突 0**。FBref vs -007 请求键日期 0 差异、开球 305/306 一致；FBref vs D1 日期 306/306 一致；B 路独立 PDF 解析 vs -007 轮次／开球 0 差异。
- **唯一冲突仍是 Frankfurt–Mainz（第 33 轮）**，但定性有进展：三源（FBref＋D1＋worldfootball 赛程总表）一致证明该场**实际在 12/05/2019 周日 18:00 进行**，DFL 29–34 PDF（2019 年 3 月公布）所载 11.05.2019 周六 15:30 是**公布时排期、赛后被改期**，不是任一源的数据错误。两值继续并存，待请求方裁决。
- **A 路审计结论：通过**。306 行、0 重复键、source_sha256 5/5 PDF 逐字节重算全符、时区全行 Europe/Berlin 且 UTC 换算独立重算 0 错误、field_locator 306/306 指向具体 PDF 行。**但 A 路 notes 有两处文字须纠正**（数据本身不受影响）：① U-02 称 D1.csv 不存在——错误，文件存在且 B 路已比对完；② §4 称“FBref 与 DFL 公布值全面一致、赛季中未发生事后变更”——错误，与其自身 §5 矛盾，Frankfurt–Mainz 正是一例事后改期。

## 1. 基线缺口：D1.csv（任务 1）

| 项 | 结果 |
|---|---|
| 搜索 | 全盘搜索后找到：`~/workspace/ai-inbox/work-bundesliga-014/raw/D1-1819.csv` |
| SHA-256 | `f03ee41b741aca9c43cbafb800bbc6f01ca9d7ed19c1a9dd4c309389280cfe11`——与请求所引值**完全一致** |
| 行数 | 307 行（表头＋306 场） |
| D1 vs -007 | 独有键 0／0，重复键 0；按（主队，客队）键日期逐行比对，**0 差异** |
| D1 vs FBref | 日期 **306/306 一致**（见 §3） |
| 结论 | 任务简报“本机只有 2024/25、2025/26 的 D1.csv 副本”前提不成立；D1.csv 精确比对**已完成**，不是 pending。A 路 unresolved_queue U-02 应标记为已解决／被取代，不再是未解决项。 |

-007 基线自查（B 路复核）：306 行，status 全 ok；source_sha256 全 null（306 行）；timezone 全 null（306 行）；来源分布：1–6 PDF 54 行、7–14 PDF 72 行、15–21 PDF 63 行、FBref `/2109/` URL 63 行（22–28 轮）、29–34 PDF 54 行。`official_match_date` 非空仅 Frankfurt–Mainz 一行（11/05/2019），`date_note` 同样仅此一行。

## 2. 五个候选 URL 独立验证（任务 2）

B 路逐个独立下载（curl 直连＋哈希重算），不抄 A 路结论。A 路 evidence/ 内同名文件哈希与 B 路独立下载值**逐字节一致**。

| # | 源 | URL | HTTP | 字节 | SHA-256（B 路独立下载） | 轮次／联赛行 | 逐场开球 |
|---|---|---|---|---|---|---|---|
| ① | DFL Ansetzungen 1–6 | `media.dfl.de/sites/3/2018/11/Bundesliga_2018-19_Spieltage_1-6.pdf` | 200 | 304723 | `1475b472…45743` | 1–6／54 行 | 有 |
| ② | DFL Ansetzungen 7–14 | `media.dfl.de/sites/3/2018/11/Bundesliga_2018-19_Spieltage_7-14.pdf` | 200 | 460469 | `40914ef8…fab64` | 7–14／72 行 | 有 |
| ③ | DFL Ansetzungen 15–21 | `media.bundesliga-gruppe.de/sites/2/2018/11/Bundesliga_2018-19_Spieltage_15-21-1.pdf` | 200 | 420296 | `6ee3f3e6…7029` | 15–21／63 行 | 有 |
| ④a | DFL 公告页 22–28 | `www.bundesliga-gruppe.de/aktuelles/dfl-terminiert-spiele-der-bundesliga-und-2-bundesliga-bis-zum-28-spieltag/` | 200 | 81922 | `235eda9c…6f79` | — | **无**：正文仅散文提及 3 个示例（Nürnberg–Dortmund 周一 20:30、Augsburg–Bayern 周五 20:30、Bayern–Dortmund 第 28 轮周六 18:30），无逐场表 |
| ④b | DFL Ansetzungen 22–28（公告所链 PDF） | `media.bundesliga-gruppe.de/sites/2/2018/12/BL-MD-22-28.pdf` | 200 | 508101 | `bfedcdc3…88174` | 22–28／63 行 | 有 |
| ⑤ | DFL Ansetzungen 29–34 | `media.dfl.de/sites/2/2019/03/Bundesliga_Spieltage_29-34.pdf` | 200 | 434986 | `7d309563…c8b` | 29–34／54 行 | 有 |
| 合计 | | | | | | 1–34／306 行（每轮 9 场） | |

- **④ 重点核查结论**：公告页本身不是逐场源；但其下载项“Spieltage 22 bis 28 der Bundesliga”指向官方 PDF ④b，该 PDF 4 页、覆盖 22–28 轮逐场开球。**22–28 轮替代官方源成立**，A 路将 -007 的 63 行 FBref 源全部升级为该 PDF 正确。
- PDF 解析细节：5 份 PDF 文本除联赛行外另含欧战、DFL 超级杯、德国杯等非联赛行，解析时按数字 Spieltag 列过滤；29–34 PDF 时间分隔符为冒号（15:30）而非其余 PDF 的点号（15.30），解析器须兼容两种；长主队名“Borussia Mönchengladbach”后栏间隔在 pdftotext 中压成单个空格，初版解析器曾漏 13 场主场比赛，修正版（按最长官方队名前缀切分）产出 306 行，0 重复，0 解析失败。

## 3. 第二源交叉核验（任务 3）

### 3.1 FBref：URL 核实

- `-007 所用 /2109/ 路径`（`fbref.com/en/comps/20/2109/schedule/2018-2019-Bundesliga-Scores-and-Fixtures`）与 `fbref.com/en/comps/20/2018-2019/schedule/2018-2019-Bundesliga-Scores-and-Fixtures` **内容相同**（同标题、同前 217 行逐行一致）：`/2109/` 是 FBref 赛季 id 路径，`/2018-2019/` 是赛季年份路径，两者均为当季有效路径，不存在“哪个才是正确路径”的问题。
- 直接 curl 不通（FBref 空回复、worldfootball 403），文本层经 browser.open 可用（页面抓取于 2026-10-31）。
- **时间列语义**：格式如 `20:30 (11:30)`，首值＝柏林本地时间，括号内＝美国太平洋时间；已按夏令时核对——8 月 CEST 与 PDT 差 9h、11 月 CET 与 PDT 差 8h、2019-03-10 美国夏令时开始后差 8h、2019-03-31 欧洲夏令时开始后差 9h，全表一致。比对一律用首值（柏林本地时间）。
- 页内第一表后另有重复渲染的第二表（同数据，Wk 1–9 已抽查一致）；另有两场德甲升降级附加赛（2019-05-23／27，Stuttgart–Union Berlin）——**非联赛场次，已排除**，不计入 306。

### 3.2 FBref 全表转录与比对

- 方法：browser.open 文本层逐页读完第一表 Wk 1–34（行 0–698），人工转录为 `fbref_201819_transcribed.csv`（306 行，字段 wk／date／time／home／away；队名按 FBref 显示），再脚本比对。转录自检：306 行、每轮恰 9 场、重复键 0、队名集合与 -007／D1 的 18 队完全一致。
- 队名映射（FBref→Football-Data 口径）：Bayern Munich 不变；Düsseldorf→Fortuna Dusseldorf；Hertha BSC→Hertha；Nürnberg→Nurnberg；Hannover 96→Hannover；Schalke 04 不变；Frankfurt→Ein Frankfurt；Gladbach→M'gladbach；Mainz 05→Mainz；其余不变。

| 比对对 | 键 | 差异数 | 详情 |
|---|---|---|---|
| FBref vs -007 match_date（请求键日期） | (round, home, away) | **0** | 全表一致 |
| FBref vs -007 kickoff_local | 同上 | **1** | 仅 Frankfurt–Mainz：FBref 18:00 vs -007 15:30 |
| FBref vs -007 official_match_date | 同上 | **1** | 仅 Frankfurt–Mainz：FBref 2019-05-12 vs 官方 2019-05-11（official_match_date 全库仅此一行非空） |
| FBref vs D1.csv 日期 | (home, away) | **0** | 306/306 一致 |
| FBref vs DFL PDF 日期／开球 | (round, home, away) | **1＋1** | 仅 Frankfurt–Mainz（日期＋开球各 1 条） |
| FBref-only／-007-only／D1-only 键 | — | **0／0／0** | 三方键集合完全同一 |

### 3.3 worldfootball.net

- 赛季页 `worldfootball.net/all_matches/bundesliga-2018-2019/` 文本层只给出赛程总表（Gameplan：每轮日期范围），无逐场行，只能作佐证，不能作逐场比对。
- 佐证价值：**Matchday 33 标注为 11.05.2019, 12.05.2019 两天**——第三源证实第 33 轮跨两天进行，与 FBref／D1 的 12/05 一致，与 DFL PDF 的“九场同在 11.05”不符。

### 3.4 B 路独立 PDF 解析 vs -007

- 独立解析 5 份 PDF 得 306 行（见 §2 解析细节）：轮次／开球分歧 **0**；唯一未匹配 PDF 行是 Frankfurt–Mainz（官方 11/05/2019）；用官方日期反查，-007 行在 PDF 中缺失 **0**。

## 4. 冲突清单（任务 3＋5）

全文见 `conflicts_201819.jsonl`（1 行）。**Frankfurt–Mainz 外的新冲突数为 0。**

| fixture_key | 轮次 | DFL 官方值（PDF 29–34，2019 年 3 月公布） | 第二源值 | -007／A 路行内处理 |
|---|---|---|---|---|
| `2018-19\|12/05/2019\|Ein Frankfurt\|Mainz` | 33 | 11.05.2019 周六 15:30（第 33 轮九场同开） | **2019-05-12 周日 18:00**（FBref 行：`33 \| Sun \| 2019-05-12 \| 18:00 (09:00) \| Frankfurt \| 0–2 \| Mainz 05`；D1 日期 12/05/2019；worldfootball 总表第 33 轮含 12.05） | match_date=12/05/2019、official_match_date=11/05/2019、kickoff_local=15:30、conflict_flag=date_key_vs_official、date_note 保留；两值并存，未自动取舍 |

- **定性**：这是**公布后改期**，不是任一源的录入错误。DFL 29–34 PDF 于 2019 年 3 月公布（排期时九场同在周六 15:30）；实际比赛被移至周日 18:00——FBref、D1、worldfootball 三方一致。改期原因本轮未查证，不作断言。
- **待裁决**：下游 fixture_key 应沿用请求键日期 12/05/2019，还是官方日期 11/05/2019，由请求方裁决；B 路与 A 路均不自动取舍。

## 5. A 路交付物审计（任务 4）

审计对象：`bundesliga_201819_kickoff_rows.jsonl`（306 行）＋`evidence/`（5 PDF＋公告 HTML＋hash_index.md＋pdftotext 文本）＋`bundesliga_201819_kickoff_notes.md`＋`unresolved_queue.jsonl`＋`parse_pdfs.py`／`build_rows.py`／`parse_audit.json`。

| 审计项 | 方法 | 结果 |
|---|---|---|
| 行数 306 | 计数 | ✅ 306 行 |
| 无重复键 | fixture_key／(round, home, away) 去重 | ✅ 0 重复 |
| source_sha256 为实采字节哈希 | 对 evidence/ 内 5 份 PDF 逐字节重算，逐行核对（**5/5 全验**，超任务要求的至少 2 个）；另与 B 路独立下载哈希交叉比对 | ✅ 0 错误、0 空值；5 个哈希与 B 路独立下载值逐字节一致（1475b472…／40914ef8…／6ee3f3e6…／bfedcdc3…／7d309563…） |
| 时区统一 Europe/Berlin | 全行检查 | ✅ 306/306 |
| 换算方法有记录 | kickoff_utc_method 非空检查＋内容 | ✅ 306/306 非空；方法写明 IANA 时区库、CET＝UTC+1（2019-03-31 02:00 前）／CEST＝UTC+2（之后）、UTC 值为派生换算非源值 |
| kickoff_utc 正确 | 用 zoneinfo 独立重算全部 306 行（含 2019-03-31 夏令时切换：03-29 20:30→19:30Z、03-30 15:30→14:30Z、03-31 15:30→13:30Z、03-31 18:00→16:00Z） | ✅ 0 错误；CET 163 行／CEST 143 行，与 notes 所称一致；无开球落在 03-31 02:00–03:00 不存在时段 |
| field_locator 指向 PDF 内具体行 | 逐行解析 verbatim 行（日期／时间／轮次／官方队名）并与行值核对；另子串检查 | ✅ 306/306 含官方主队名、客队名、日期、时间。注：审计脚本初版用“双空格切分主客队”的正则曾报 13 行 M'gladbach 主场行“不符”，系 pdftotext 在长队名后把栏间隔压成单个空格所致——locator 文本本身逐字正确，子串检查 306/306 通过，该 13 行不作问题项 |
| 行值 vs -007 | match_date／official_match_date／date_note／主客队／轮次／开球逐项比对 | ✅ 0 差异 |
| 行值 vs B 路独立 PDF 解析 | (round, home, away) 键日期／开球比对 | ✅ 0 差异 |
| 行值 vs FBref | 见 §3.2 | ✅ 除 Frankfurt–Mainz 外 0 差异；该场行内两值并存＋conflict_flag，处理正确 |
| 22–28 轮源升级 | source_url 分布：1–6 54 行、7–14 72 行、15–21 63 行、BL-MD-22-28.pdf 63 行、29–34 54 行 | ✅ FBref 源 0 行；-007 的 63 行 FBref 源全部升级为官方 PDF |
| source_tier／status | 全行检查 | ✅ source_tier 全 official_dfl；status 全 ok；conflict_flag 仅 Frankfurt–Mainz 一行 |
| 文件哈希与 notes 一致 | sha256sum 重算 | ✅ `f34222a3…11f2dd` 与 notes §1 所称一致 |
| 禁字段 | 比分／赔率／模型输出 | ✅ A 路 notes 自称扫描 0 命中；B 路行键检查无比分／赔率字段（本验证亦只做赛前事实） |

**审计结论：通过。** A 路数据交付物无实质问题。

### 5.1 A 路 notes 两处文字须纠正（数据本身不受影响）

1. **unresolved_queue U-02 错误**：notes §6 与 U-02 称“请求所引本地 D1.csv 在本 VM 上不存在（本机只有 2024/25、2025/26 副本）”。**不成立**。B 路已找到该文件（`~/workspace/ai-inbox/work-bundesliga-014/raw/D1-1819.csv`，SHA-256 与请求所引值逐字节一致），并完成精确比对（§1）。U-02 应标记为**已解决／被取代**，不应再列为未解决项。
2. **notes §4 一句话错误**：“FBref 实际赛程值与 DFL 公布值全面一致，说明公布开球在赛季中未发生事后变更”。**不成立**，且与其自身 §5 矛盾：FBref／D1／worldfootball 三方一致显示 Frankfurt–Mainz 实际在 12/05/2019 周日 18:00 进行，而 DFL 29–34 PDF（2019 年 3 月公布）为 11.05.2019 周六 15:30——这正是一例**公布后改期**。正确表述应为：305/306 场一致，唯一分歧为一例已记录的改期，两值并存待裁决。

## 6. 未解决项（B 路口径）

| # | 项 | 状态 |
|---|---|---|
| U-01 | Frankfurt–Mainz：下游 fixture_key 用 12/05/2019 还是 11/05/2019 | **未解决**，待请求方裁决（A 路 U-01 同项，B 路同意其“两值并存、不自动取舍”处理） |
| U-02（A 路） | D1.csv 精确比对 | **已由 B 路解决**：文件存在、哈希一致、比对 0 差异（§1）。A 路 U-02 应予关闭 |
| — | 其余 | 无。FBref 外新增冲突 0；A 路审计通过；5 源全部验证通过 |

## 7. 方法与局限

- FBref 为文本层转录（browser.open，页面抓取于 2026-10-31），非源字节：转录行无源字节 SHA-256；但转录后经三重自检（306 行、每轮 9 场、队名集合与 -007／D1 完全一致）且与 -007／D1／PDF 三方比对 0 差异（除已知冲突），转录错误概率已压至最低。任何一条转录差错都会表现为一处假差异——本轮除 Frankfurt–Mainz 外无假差异出现。
- FBref 页内第二表为重复渲染，仅抽查 Wk 1–9 与第一表一致，未逐行转录；第一表已完整覆盖 306 场联赛行。
- worldfootball.net 文本层仅提供赛程总表日期范围，未作逐场比对，仅作第 33 轮跨两天的佐证。
- 未购买、未登录、未使用任何密钥／凭证、未动用付费 API 额度；未写 repo/responses/；只做赛前事实，未碰比分／赔率／模型输出。
- B 路工作文件（转录表与比对／审计脚本）随本报告存放于同一工作目录，供复核：`fbref_201819_transcribed.csv`、`compare_fbref.py`、`audit_a.py`、`parse_pdfs2.py`、`pdf_vs_007.json`。

## 附录：B 路独立验证证据清单

| 证据 | 位置／值 |
|---|---|
| D1.csv | `~/workspace/ai-inbox/work-bundesliga-014/raw/D1-1819.csv`，SHA-256 `f03ee41b741aca9c43cbafb800bbc6f01ca9d7ed19c1a9dd4c309389280cfe11` |
| 5 份 DFL PDF（B 路独立下载哈希） | 1475b472…45743／40914ef8…fab64／6ee3f3e6…7029／bfedcdc3…88174／7d309563…c8b |
| 公告页 HTML（B 路独立下载哈希） | `235eda9c05eff752e4d9a353eae1cf76bc53cfa4fa3316bcf10b29bc1a236f79`（81922 字节） |
| FBref 页 | `fbref.com/en/comps/20/2018-2019/schedule/2018-2019-Bundesliga-Scores-and-Fixtures`（与 `/2109/` 路径内容相同；抓取于 2026-10-31） |
| worldfootball 赛季页 | `worldfootball.net/all_matches/bundesliga-2018-2019/`（抓取于 2026-08-01；仅 Gameplan 级） |
| A 路交付物哈希 | `bundesliga_201819_kickoff_rows.jsonl` SHA-256 `f34222a35bc03178f195edab6153d4183047677adc41ead913ea27722b11f2dd` |
