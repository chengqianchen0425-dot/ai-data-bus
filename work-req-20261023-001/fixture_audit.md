# fixture_audit.md — req-20261023-001 A 路：Copa Libertadores 2018–2025 可审计 fixture 清单

- 审计日期：2026-10-23（北京时间）
- 主交付：`fixture_inventory.jsonl`（1,124 行）；源内工作文件：`conmebol_inventory.jsonl`（38 行）、`fbref_{YYYY}_textlayer.jsonl`（7 季）
- 核心口径：**按源分开保存，绝不跨源按队名拼合为单行**。2022 与 2024 季的赛季总数因此同时包含 FBref 行与 CONMEBOL 行（同一场比赛在两源各占一行），赛季总数不是去重后的场次数。
- 绝无比分/赛果/晋级/预测类字段：全文件禁字段扫描（score/goals/result/winner 类键）为 0 命中。
- 上一单（req-20261021-001）文件全程只作核对清单；本轮每一行都有本轮自己的证据（CONMEBOL 为下载字节，FBref 为本轮打开的页面文本层）。上一单行数不得作本轮覆盖率分母。

## 1. 总量与字节哈希覆盖率

| 口径 | 行数 |
|---|---|
| 总行数 | 1,124 |
| CONMEBOL 官方 PROGRAMA PDF（字节下载） | 38 |
| FBref 文本层（无字节） | 1,086 |
| complete | 1,062 |
| partial | 60（FBref 球场截断 57 + CONMEBOL “A definir” 3） |
| conflict | 2（2020 季开球时间与上轮读数冲突，见 §5） |
| unmatched / ambiguous（行级） | 0 / 0 |

**字节哈希覆盖率（分母必须明确）：**

| 分母 | 有字节哈希 | 覆盖率 |
|---|---|---|
| 全部 1,124 行 | 38 | 3.38% |
| CONMEBOL 子集 38 行 | 38 | 100% |
| FBref 子集 1,086 行 | 0 | 0% |

FBref 的 0% 是结构性结果，不是疏漏：该站对本机 curl 返回 Cloudflare 挑战页（HTTP 403）或空回复（HTTP 000），字节下载已证实不可行（见 §6），故 FBref 行一律 `source_sha256=null` 并注明“浏览器文本层、无字节”。探针日志中 FBref 挑战页的响应体哈希绝不能当作行哈希使用。

按赛季行数（源分开计数，含跨源重复）：2018 = 156；2019 = 155；2020 = 155；2021 = 155；2022 = 185（FBref 155 + CONMEBOL 30）；2023 = 155；2024 = 163（FBref 155 + CONMEBOL 8）；2025 = 0（本轮阻塞，见 §7）。

## 2. FBref 文本层：按赛季呈现与去重

FBref 各季页内赛程表分 All Rounds 表与阶段分表呈现同一场比赛两次；按 (match_date, kickoff_local, home, away) 源内去重为唯一场次，round 取非空值。

| 赛季 | 呈现行数（去重前） | 唯一场次 | 截断唯一场次（partial） | retrieved_at（UTC+8） |
|---|---|---|---|---|
| 2018 | 282 | 156 | 13 | 2026-10-23T21:25:43+08:00 |
| 2019 | 280 | 155 | 14 | 2026-10-23T21:26:14+08:00 |
| 2020 | 280 | 155 | 5 | 2026-10-23T21:26:11+08:00 |
| 2021 | 280 | 155 | 5 | 2026-10-23T21:24:57+08:00 |
| 2022 | 280 | 155 | 8 | 2026-10-23T21:25:20+08:00 |
| 2023 | 280 | 155 | 9 | 2026-10-23T21:25:00+08:00 |
| 2024 | 280 | 155 | 3 | 2026-10-23T21:26:16+08:00 |
| 2025 | 未取得（0 行） | 0 | — | 仅失败尝试时间 2026-10-23 21:24–21:25 CST |
| 合计（2018–2024） | 1,962 | 1,086 | 57 | — |

截断口径：Venue 列原文以 `...` 结尾的照抄原文、不补全，标 `venue_truncated=true`，行 status=partial。2018 季唯一场次 156 场（非 155）是因为 2018 决赛为两回合（Finals 2 场），其余季决赛为单场 1 场。

## 3. CONMEBOL 官方 PROGRAMA PDF：按阶段计数

| 赛季 | 阶段（PDF 内原文） | 回合 | 行数 | complete | partial |
|---|---|---|---|---|---|
| 2022 | Fase 1 | Ida / Vuelta | 6（3+3） | 6 | 0 |
| 2022 | Fase 2 | Ida / Vuelta | 16（8+8） | 13 | 3（#9/#11/#14，见 §5） |
| 2022 | Fase 3 | Ida / Vuelta | 8（4+4） | 8 | 0 |
| 2024 | Cuartos de Final | IDA / VUELTA | 8（4+4） | 8 | 0 |
| 合计 | — | — | 38 | 35 | 3 |

下载字节（curl，HTTP 200，2026-10-23 21:23 CST）：

| 文件 | 字节 | sha256 |
|---|---|---|
| `fixture_evidence/conmebol_2022_fase12.pdf` | 194,980 | `54f9acdc5344759a5d0c1c373f64d7f8fc7d5ec047939c95655ec7d2d595e95c` |
| `fixture_evidence/conmebol_2022_fase3.pdf` | 155,797 | `83c0f73aa46d1b3030a1f2ed05d294f17e814bef3b33bc755b578c65d03941e2` |
| `fixture_evidence/conmebol_2024_qf.pdf` | 71,765 | `5569f5b2cf3421e23153582199d716fa5c037c8d4b185da498e51d2d81bc7334` |

三份哈希在探针轮次与下载轮次两次独立取得、完全一致。版本：2022 Fase 1/2 为 `Versión de 28/01/2022`、Fase 3 为 `Versión de 04/03/2022`、2024 Cuartos 页眉日期 26/8/2024（该 PDF 无 “Versión de” 字样）；三者均早于各自阶段的全部开球时间。

## 4. 按赛季 × 阶段 × 源：discovered / complete / partial / conflict

`official_stage` 为源原文照抄（2018 决赛原文为 `Finals`，其余季为 `Final`；审计表计入时 Finals 归入决赛阶段，但行内原文不改）。

| 赛季 | 源 | 阶段 | discovered | complete | partial | conflict |
|---|---|---|---|---|---|---|
| 2018 | FBREF-TEXTLAYER | First qualifying stage | 6 | 6 | 0 | 0 |
| 2018 | FBREF-TEXTLAYER | Second qualifying stage | 16 | 14 | 2 | 0 |
| 2018 | FBREF-TEXTLAYER | Third qualifying stage | 8 | 8 | 0 | 0 |
| 2018 | FBREF-TEXTLAYER | Group stage | 96 | 90 | 6 | 0 |
| 2018 | FBREF-TEXTLAYER | Round of 16 | 16 | 14 | 2 | 0 |
| 2018 | FBREF-TEXTLAYER | Quarter-finals | 8 | 6 | 2 | 0 |
| 2018 | FBREF-TEXTLAYER | Semi-finals | 4 | 3 | 1 | 0 |
| 2018 | FBREF-TEXTLAYER | Finals（原文，=决赛） | 2 | 2 | 0 | 0 |
| 2019 | FBREF-TEXTLAYER | First qualifying stage | 6 | 6 | 0 | 0 |
| 2019 | FBREF-TEXTLAYER | Second qualifying stage | 16 | 16 | 0 | 0 |
| 2019 | FBREF-TEXTLAYER | Third qualifying stage | 8 | 7 | 1 | 0 |
| 2019 | FBREF-TEXTLAYER | Group stage | 96 | 86 | 10 | 0 |
| 2019 | FBREF-TEXTLAYER | Round of 16 | 16 | 15 | 1 | 0 |
| 2019 | FBREF-TEXTLAYER | Quarter-finals | 8 | 7 | 1 | 0 |
| 2019 | FBREF-TEXTLAYER | Semi-finals | 4 | 3 | 1 | 0 |
| 2019 | FBREF-TEXTLAYER | Final | 1 | 1 | 0 | 0 |
| 2020 | FBREF-TEXTLAYER | First qualifying stage | 6 | 6 | 0 | 0 |
| 2020 | FBREF-TEXTLAYER | Second qualifying stage | 16 | 14 | 1 | 1 |
| 2020 | FBREF-TEXTLAYER | Third qualifying stage | 8 | 7 | 1 | 0 |
| 2020 | FBREF-TEXTLAYER | Group stage | 96 | 92 | 3 | 1 |
| 2020 | FBREF-TEXTLAYER | Round of 16 | 16 | 16 | 0 | 0 |
| 2020 | FBREF-TEXTLAYER | Quarter-finals | 8 | 8 | 0 | 0 |
| 2020 | FBREF-TEXTLAYER | Semi-finals | 4 | 4 | 0 | 0 |
| 2020 | FBREF-TEXTLAYER | Final | 1 | 1 | 0 | 0 |
| 2021 | FBREF-TEXTLAYER | First qualifying stage | 6 | 6 | 0 | 0 |
| 2021 | FBREF-TEXTLAYER | Second qualifying stage | 16 | 16 | 0 | 0 |
| 2021 | FBREF-TEXTLAYER | Third qualifying stage | 8 | 8 | 0 | 0 |
| 2021 | FBREF-TEXTLAYER | Group stage | 96 | 93 | 3 | 0 |
| 2021 | FBREF-TEXTLAYER | Round of 16 | 16 | 15 | 1 | 0 |
| 2021 | FBREF-TEXTLAYER | Quarter-finals | 8 | 7 | 1 | 0 |
| 2021 | FBREF-TEXTLAYER | Semi-finals | 4 | 4 | 0 | 0 |
| 2021 | FBREF-TEXTLAYER | Final | 1 | 1 | 0 | 0 |
| 2022 | CONMEBOL-PROGRAMA | Fase 1 | 6 | 6 | 0 | 0 |
| 2022 | CONMEBOL-PROGRAMA | Fase 2 | 16 | 13 | 3 | 0 |
| 2022 | CONMEBOL-PROGRAMA | Fase 3 | 8 | 8 | 0 | 0 |
| 2022 | FBREF-TEXTLAYER | First qualifying stage | 6 | 6 | 0 | 0 |
| 2022 | FBREF-TEXTLAYER | Second qualifying stage | 16 | 16 | 0 | 0 |
| 2022 | FBREF-TEXTLAYER | Third qualifying stage | 8 | 8 | 0 | 0 |
| 2022 | FBREF-TEXTLAYER | Group stage | 96 | 90 | 6 | 0 |
| 2022 | FBREF-TEXTLAYER | Round of 16 | 16 | 14 | 2 | 0 |
| 2022 | FBREF-TEXTLAYER | Quarter-finals | 8 | 8 | 0 | 0 |
| 2022 | FBREF-TEXTLAYER | Semi-finals | 4 | 4 | 0 | 0 |
| 2022 | FBREF-TEXTLAYER | Final | 1 | 1 | 0 | 0 |
| 2023 | FBREF-TEXTLAYER | First qualifying stage | 6 | 6 | 0 | 0 |
| 2023 | FBREF-TEXTLAYER | Second qualifying stage | 16 | 16 | 0 | 0 |
| 2023 | FBREF-TEXTLAYER | Third qualifying stage | 8 | 8 | 0 | 0 |
| 2023 | FBREF-TEXTLAYER | Group stage | 96 | 87 | 9 | 0 |
| 2023 | FBREF-TEXTLAYER | Round of 16 | 16 | 16 | 0 | 0 |
| 2023 | FBREF-TEXTLAYER | Quarter-finals | 8 | 8 | 0 | 0 |
| 2023 | FBREF-TEXTLAYER | Semi-finals | 4 | 4 | 0 | 0 |
| 2023 | FBREF-TEXTLAYER | Final | 1 | 1 | 0 | 0 |
| 2024 | CONMEBOL-PROGRAMA | Cuartos de Final | 8 | 8 | 0 | 0 |
| 2024 | FBREF-TEXTLAYER | First qualifying stage | 6 | 5 | 1 | 0 |
| 2024 | FBREF-TEXTLAYER | Second qualifying stage | 16 | 16 | 0 | 0 |
| 2024 | FBREF-TEXTLAYER | Third qualifying stage | 8 | 8 | 0 | 0 |
| 2024 | FBREF-TEXTLAYER | Group stage | 96 | 94 | 2 | 0 |
| 2024 | FBREF-TEXTLAYER | Round of 16 | 16 | 16 | 0 | 0 |
| 2024 | FBREF-TEXTLAYER | Quarter-finals | 8 | 8 | 0 | 0 |
| 2024 | FBREF-TEXTLAYER | Semi-finals | 4 | 4 | 0 | 0 |
| 2024 | FBREF-TEXTLAYER | Final | 1 | 1 | 0 | 0 |
| 2025 | — | 全部阶段 | 0 | 0 | 0 | 0 |

## 5. 与上一单的核对差异（上一单只作清单，差异全部有本轮证据支撑）

### 5.1 CONMEBOL：仅 4 处差异，全部是 #9/#11/#14 的 “A definir” 列位置纠正

本轮用 `pdftotext -layout` 字符位置实测（Fase 1/2 PDF 表头列位置：Ciudad=28、País=39、Estadio=68、Hora Local=98、GMT=114）：

| 行 | 本轮读法（列位置证据） | 上一单读法 |
|---|---|---|
| 2022 Fase 2 Ida #9（E2 vs Univ. Católica，2022-02-23） | city=“A definir”（列 28）、country=null（País 列为空）、venue=“A definir”（列 68）、kickoff_local=“18:15” | city/country=“A definir”、venue=null |
| 2022 Fase 2 Ida #11（E1 vs Universitario，2022-02-23） | city=“A definir”、country=null、venue=“A definir”、kickoff_local=null（源文本为 “A definir”，另存于 `kickoff_local_source_text`，不得把占位词写成时间） | city/country/venue 全为 “A definir” |
| 2022 Fase 2 Vuelta #14（E3 vs Atlético Nacional，2022-02-24） | 同 #11 | 同 #11 |

其余 34 行与上一单逐字段一致（队名、日期、时间、球场、城市、国家、Grupo/Llave 全部一致）。上一单的读法不得沿用。

其他 CONMEBOL 转录口径（本轮已定）：
- `source_fixture_id` 为 PDF 内 `#` 列，只在该阶段文档内有效，不假设跨文档全局唯一。
- 2022 行只填 `group_id`（Grupo 列 E1–E3、C1–C8、G1–G4，属资格赛 slot 编码，不是小组赛字母）；2024 行只填 `tie_id`（Llave 列 S1–S4）；另一字段为 null。
- `kickoff_utc` 只取 GMT 列的时刻字符串（如 00:30、22:15）；源未给 UTC 日期，绝不能与 match_date 拼成完整 UTC 时间戳。
- `source_timezone_text` 全为 null：源只写 “Hora Local”，未标注任何时区名称/偏移；GMT 列是第二时间列，不是本地时间的时区标签。
- 2022 Fase 2 中 6 处 Fase 1 胜者占位符 E1/E2/E3 原文保留（版本发布时胜者尚未产生），绝不回填真实队名。
- 2024 队名后的种子数字原文保留（如 Flamengo11、Peñarol10、Fluminense4、Atlético Mineiro2、São Paulo5、Botafogo14），其含义不解读。转录技术说明：`pdftotext -layout` 会把 #144/#146/#149 的种子数字落到单独一行，本轮用 `-raw` token 流把种子数字重新贴回队名（行内附 `team_label_note`）；经校验，贴回后的队名与 layout 队名在剥离种子数字后完全一致。
- 2022 Fase 1/2 PDF 页脚注：俱乐部申报球场、待 CONMEBOL 最终确认。

### 5.2 FBref：身份集合基本一致，3 类差异

- **2018 / 2021 / 2022 / 2024**：按 (match_date, kickoff_local, home, away) 的唯一场次集合与上一单完全一致，零新增、零缺失、零不一致。
- **2019 / 2023**：场次身份集合完全一致；唯一差异是转录格式——本轮 `kickoff_local` 保留 Time 列完整原文（含括号内第二时刻，如 `18:30 (15:30)`、`19:00 (16:00)`），上一单只保留首个时刻。剥离括号部分后，两轮 155 场全部一致。括号内第二时刻的含义未解读（行内附 `kickoff_local_note`）。
- **2020：2 处真实时间冲突**（行 status=conflict，行内附 `conflict_note`；本轮值保留为行值，未用上轮值覆盖）：
  - 2020-02-05 Universitario pe vs Cerro Porteño py（Second qualifying stage）：本轮 17:15，上轮 19:15。本轮读数出处为该季页面文本层 L350。
  - 2020-09-16 Bolívar bo vs Palmeiras br（Group stage）：本轮 20:30，上轮 21:30。本轮读数在本轮页面内出现两次且一致（All Rounds 表 L104 与小组赛分表 L503），为本轮读数提供页内佐证，但两轮读数仍不一致，故仍记 conflict、不直接改判上轮为错。
  - 其余 153 场一致。冲突最终裁决需重新打开该季页面核对，本轮未裁决。
- **2018 决赛阶段名**：本轮照抄 FBref Round 列原文 `Finals`（两回合决赛 2 场），上一单归一化为 `Final`。行内保留原文，审计计数时 Finals 归入决赛阶段。
- **文本层乱码处理（同页内补全，不计入截断）**：2019-05-08 Grêmio 主场一行与 2021-05-26 Boca Juniors 对 The Strongest 一行的球场在 All Rounds 表文本层中显示乱码，同一页面小组赛分表中渲染正常；本轮采用同页分表中的完整写法，该两行不计入截断行数（2019 截断仍为 14 行、2021 截断仍为 5 行）。

## 6. 字节下载障碍实录（curl 探针，2026-10-23 21:22–21:23 CST）

- 对照探针 `https://example.com`：HTTP 200、577 字节、耗时约 25.4 秒——本机 shell 通道当时并非全断，只是缓慢。
- FBref 8 季赛程页：2019/2020/2021/2022/2025 为 HTTP 403（Cloudflare 挑战页，响应头含 `Cf-Mitigated: challenge`，不是赛程数据）；2018/2023/2024 为 HTTP 000、0 字节（curl exit 52 空回复）；2024 在首次探针为 403、探针轮次为 000——字节通道不稳定、间歇性被挑战。结论：FBref 字节下载不可行，走文本层后备。挑战页响应体不得作为 fixture 证据保存：探针日志只记状态、curl exit 码、返回体哈希与 120 字符首部片段（仅用于识别其为挑战页），行哈希绝不用它。
- CONMEBOL 3 份 PDF：首次探针 2024 四分之一决赛 PDF 为 CloudFront 403（919 字节错误页），但探针轮次中 3 份 PDF 全部 HTTP 200 并下载成功——CONMEBOL 字节下载为间歇性 CloudFront 拦截，不宜据此断言该站已稳定开放；本轮下载到的字节已验真为 PDF（`%PDF-1.6` / `%PDF-1.7`，各 1 页），故本轮 38 行的哈希有效。

## 7. 未覆盖清单（unresolved 队列）

### 7.1 FBref 2025 赛季整季未覆盖（access_blocked，本轮阻塞）

- 目标 URL：`https://fbref.com/en/comps/14/2025/schedule/2025-Copa-Libertadores-Scores-and-Fixtures`
- 本轮尝试：2026-10-23 21:24–21:25 CST，浏览器文本层打开失败，未返回任何页面文本；错误原文 `browser.open failed: The requested URL was not found / failure_stage=source_fetch, kind=upstream_fetch_failed`（无源 HTTP 状态）。按指令未重试同一请求、未改用 curl、未改用其他端点绕过。
- 结果：`fbref_2025_textlayer.jsonl` 为空文件（0 行），表示“本轮阻塞、未转录”，不是“2025 赛季 0 场比赛”。上一单的 2025 季 155 行只作核对清单，绝不复制为本轮交付。
- 后续：需主代理另派一次 2025 文本层重读（或等该页文本层恢复后重派）；本轮不再撞墙。

### 7.2 CONMEBOL 官方 PROGRAMA PDF：60 / 64 个赛季 × 阶段组合未覆盖（source_missing 倾向，但未穷尽全网）

阶段口径：每季 8 个阶段（第一/第二/第三资格赛、小组赛、16 强、8 强、半决赛、决赛），8 季共 64 个组合；本轮官方字节覆盖 4 个组合（2022 第一/第二/第三资格赛、2024 八强），缺 60 个：

- 2018：全部 8 个组合未覆盖；2019：全部 8 个；2020：全部 8 个；2021：全部 8 个。
- 2022：小组赛、16 强、8 强、半决赛、决赛 5 个未覆盖（资格赛三阶段已覆盖）。
- 2023：全部 8 个组合未覆盖。
- 2024：除八强外 7 个未覆盖（第一/第二/第三资格赛、小组赛、16 强、半决赛、决赛）。
- 2025：全部 8 个组合未覆盖。
- 注意：上一单 A 路审计曾写 4/56，是算术错误；正确分母为 64（8 季 × 8 阶段），不得沿用 4/56。

### 7.3 其他未决项

- 2020 季 2 处开球时间冲突（§5.2）：待重开页面裁决，本轮未裁决。
- FBref 全部 1,086 行的字节哈希缺口：源站 Cloudflare 拦截所致，非本轮遗漏；若未来该站字节通道恢复，可补下载并回填哈希（行身份已用文本层固定）。
- SoccerAssociation 源：本单未重做（上一单 1,227 行为文本层、无字节）；若主代理需要三源并行审计，需另派该源的本轮重读任务。

## 8. 证据文件清单（`fixture_evidence/`）

- `conmebol_2022_fase12.pdf`、`conmebol_2022_fase3.pdf`、`conmebol_2024_qf.pdf`：下载到的源字节（见 §3 字节与哈希）。
- `curl_probe_log.json`：11 条 curl 探针记录（8 个 FBref 季 URL + 3 个 CONMEBOL PDF URL，含 HTTP 状态、curl exit 码、返回体哈希与 120 字符首部片段）。警告：其中 FBref 挑战页/空回复的哈希不是 fixture 数据哈希，绝不能用作行哈希；首部片段仅用于识别挑战页，不含赛程数据。
- `fbref_{YYYY}_textlayer_note.txt`（2018–2025 各一份）：各季文本层说明（URL、打开时间、文本层、无字节、呈现行数、唯一场次数、截断行数、与上一单核对差异）。2025 说明记录的是阻塞经过与空文件含义。
- `conmebol_note.txt`：CONMEBOL 转录技术说明（layout/raw 分工、A-definir 列位置证据、种子数字处理、版本日期）。
- `README.txt`：证据目录总说明与探针日志警告。
- 内部工作文件（不在证据目录内，但为审计链一部分）：`build_conmebol.py`（CONMEBOL 纯 layout 解析脚本，含 2024 种子数字 raw 回贴逻辑）、`conmebol_inventory.jsonl`（38 行源内文件）、`fbref_{YYYY}_textlayer.jsonl`（7 季源内文件）。

## 9. 字段语义铁律（本单沿用，不得继承错误标签）

- 官方开球时间戳：仅源明确发布时填；FBref 只有 Time 列时刻（无日期外的时区/UTC 信息），`kickoff_utc` 为 null；CONMEBOL 的 `kickoff_utc` 只是 GMT 列时刻字符串、无 UTC 日期。
- 时区/UTC 偏移：仅源明确发布时填；本轮全部 1,124 行 `source_timezone_text` 均为 null（FBref 无时区标注；CONMEBOL “Hora Local” 未标注时区名/偏移）。
- 官方阶段/轮次：仅源明确发布时填；FBref 小组赛 `official_round` 为 Wk 值 1–6，其余为 null；2023 季小组赛分表行本身无 Round 列，分表行 round 保持 null 再与 All Rounds 行合并取非空值，绝不按分表语境推断填 Group stage。
- 缺失一律填 null 并分类，不推断、不回填、不跨源拼合。
