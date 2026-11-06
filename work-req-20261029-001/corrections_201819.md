# req-20261029-001 纠正记录（主代理，2026-11-06）

本文件纠正 A 路 notes 中的两处文字错误。数据本身不受影响（306 行值与 B 路独立解析 0 差异）。

## 纠正 1：D1.csv 在本 VM 上存在（A 路 U-02 错误）

- A 路 notes §6 与 unresolved_queue U-02 称“请求所引本地 D1.csv 在本 VM 上不存在（本机只有 2024/25、2025/26 的 D1.csv 副本）”。
- **错误**。B 路在 `~/workspace/ai-inbox/work-bundesliga-014/raw/D1-1819.csv` 找到该文件，SHA-256 与请求所引值逐字节一致（`f03ee41b741aca9c43cbafb800bbc6f01ca9d7ed19c1a9dd4c309389280cfe11`），306 行＋表头。
- 主代理已独立复核：D1 306 行与 -007 306 行的 (日期, 主队, 客队) 键双向差集均为 0；D1 与 FBref 日期 306/306 一致。
- 处理：U-02 标记为 resolved_superseded（见 unresolved_queue.jsonl）。主代理 processing 回执中“D1.csv 精确比对列为未解决项”的说法一并作废——精确比对已完成，0 差异。

## 纠正 2：Frankfurt–Mainz 是公布后改期，不是“无事后变更”（A 路 notes §4 错误）

- A 路 notes §4 称“FBref 与 DFL 全面一致、无事后变更”。
- **错误**，且与其自身 §5 矛盾。正确表述：305/306 一致，唯一分歧为一例已记录的改期——DFL 官方 PDF（2019 年 3 月公布）排期第 33 轮九场同在周六 2019-05-11 15:30；实际比赛被移至周日 2019-05-12 18:00（FBref、D1.csv、worldfootball 三方一致；改期原因本轮未查证，不作断言）。
- 处理：两值继续并存，待请求方裁决下游 fixture_key 用 12/05/2019 还是 11/05/2019（见 conflicts_201819.jsonl，U-01）。
