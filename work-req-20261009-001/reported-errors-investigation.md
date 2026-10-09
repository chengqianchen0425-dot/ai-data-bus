# req-20261009-001 — 两处"已报告错误"的核查结论（2026-10-09 19:35 +08:00）

## 结论先行
两处错误均**无法复现**：q1-fixtures.json 的相关行与 football-data 源 **以及** SFL 官方赛程提取（sfl-patch chunks）逐字一致。按"禁猜测"铁律，**不修改这些行**；差异如实记录为已验证一致。

## 1) "2024/25 St. Gallen-Basel 重复行"
- q1 内 2024/25 St. Gallen↔Basel 共 3 行（12 队/33 轮+分组赛制下每对交手 3 次为正常值）：
  - 2024-10-20 Basel vs St. Gallen
  - 2024-12-08 St. Gallen vs Basel
  - 2025-02-22 St. Gallen vs Basel
- football-data SWZ-current.csv 三行完全一致（日期/时间/主客）。
- SFL 官方 chunk（chunk-2425-2526.csv）三行全部确认，各带独立 Spielnummer：
  - 2024-10-20 FC Basel 1893 vs FC St. Gallen 1879，Spielnummer 100416，Phase 1
  - 2024-12-08 FC St. Gallen 1879 vs FC Basel 1893，Spielnummer 100461，Phase 1
  - 2025-02-22 FC St. Gallen 1879 vs FC Basel 1893，Spielnummer 184443，Phase 2
- 无精确重复行（全文件 1,584 行唯一键零重复）。**"重复"指控不成立，数据保留。**

## 2) "2022/23 MD3/MD4 Zürich-Sion 错误"
- q1 内 2022/23 Zürich↔Sion 共 4 行（10 队/36 轮每对交手 4 次为正常值）：
  - 2022-08-07 Zurich vs Sion
  - 2022-10-30 Sion vs Zurich
  - 2023-02-05 Sion vs Zurich
  - 2023-04-30 Zurich vs Sion
- football-data SWZ-current.csv 四行完全一致。
- SFL 官方 chunk（chunk-2223.csv）四行全部确认（2022-08-07 / 2022-10-30 / 2023-02-05 / 2023-04-30，主客队一致）。
- 2022-10-30 与 2023-02-05 连续两场 Sion 主场看似"未交替"，但 SFL 官方赛程原文如此（同期 Sion 其他对阵亦有多处非交替，如连续 Basel 主场 2022-11-06/2023-02-11），属真实赛程编排特征，非数据错误。**指控不成立，数据保留。**

## 核查中发现的真冲突（第三方核查已完成）
- **对阵冲突（已解决，2026-10-09 第三方 9 源核验）**：2025-02-08 实为 **Lausanne vs Yverdon**（Lausanne 4-1，Matchday 23，Stade de la Tuilière）——sportradar、TNT Sports×3、Sky Sports、terrikon、Sports Mole、Sportalic、FotMob 九源一致。football-data 正确；**SFL chunk 的 '2025-02-08 FC Lausanne-Sport vs FC Lugano' 行为提取错位**（客队标错），其 Spielnummer 184428 实属 Lausanne-Yverdon 一战。sfl-enrichment-joined.json 已据此修正挂载（Spielnummer 184428 → Lausanne-Yverdon，附注说明）；chunk 中多出的第 5 个 Lausanne-Lugano 行即为该幽灵行（真实 Lausanne-Lugano 2024/25 共 4 战：2024-09-18、2024-12-15、2025-04-21、2025-05-18 冠军组）。
- **日期冲突（双值保留，未决）**：2018/19 St. Gallen vs Lugano，2019-03-16（football-data、Sports Mole、TipsterArea、matips、Statarea）vs 2019-03-17（SFL chunk、ESPN）。sfl-enrichment-joined.json 已挂 SFL Spielnummer 100302 并标注冲突未决，按冲突政策不二选一。
