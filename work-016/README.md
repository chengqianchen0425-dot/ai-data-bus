# work-016 行级证据说明（req-20261002-016：MLS 2018–2020 常规赛）

构建时间：2026-10-02 17:28–17:45 CST（UTC 09:28–09:45）
数据来源：ESPN 公开记分板 API `site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard?dates=YYYYMMDD`
（league slug `usa.1` = MLS；event.season.slug == "regular-season" 才收录）

## 文件

| 文件 | 内容 |
|---|---|
| `mls-2018-regular-season-fixtures.csv` | 391 行（全部 full_time） |
| `mls-2019-regular-season-fixtures.csv` | 408 行（全部 full_time） |
| `mls-2020-regular-season-fixtures.csv` | 302 行：292 full_time + 3 postponed（从未补赛）+ 7 canceled |
| `audit-per-season.json` | 逐季 audit 统计 |
| `day-sha-manifest.json` | 逐日原始 JSON 的 sha256（前 16 位）清单 |
| `tz-lookup.md` | 场馆城市→IANA 时区派生映射说明 |
| `unresolved-queue.md` | 未解决队列（10 场 2020 未打比赛 + 数据说明） |
| `README.md` | 本文件 |

## 列说明

- `season` / `date_local` / `kickoff_local` / `kickoff_utc`：kickoff_local 由 ESPN 的 UTC 时间经 zoneinfo 按场馆城市时区换算（含夏令时）
- `provider_fixture_id`：ESPN event id
- `stable_match_key`：`mls-<season>-<主缩写>-<客缩写>-<本地日期YYYYMMDD>`
- `official_stage`：固定 "Regular Season"；`official_round`：MLS 常规赛无编号轮次 → NULL
- `venue` / `venue_city` / `venue_city_raw`：ESPN 原样返回（注意：2020 年后改名球场在 ESPN 当前数据中以新名出现，如 Red Bull Arena→"Sports Illustrated Stadium"、CenturyLink Field→"Lumen Field"，未做历史名归一化，属 ESPN 当前数据原貌）
- `status`：full_time / postponed / canceled（ESPN STATUS_FULL_TIME/POSTPONED/CANCELED）
- `row_note`：`venue_override:<venue>`（场地非常规主场——2020 年 COVID 期间 55 行中立/借用场地；2018 3 行、2019 1 行），`tz_unmapped:<city>`（无城市未映射）
- `source_url` / `final_url`：逐日记分板 URL；`retrieved_at`：该日 JSON 文件实际下载时间；`field_locator`：`scoreboard.events[<id>].competitions[0]`；`source_sha256`：该日原始 JSON 的 sha256 前 16 位

## 收录范围核对（identity-matched）

- 2018：expected 391 / discovered 391 / identity_matched 391，季后赛 slug（knockout/semifinals）已排除，missing 0
- 2019：expected 408 / discovered 408 / identity_matched 408，missing 0
- 2020：expected 292 / discovered 292 full_time / identity_matched 292；另 10 场已安排但未打（3 postponed + 7 canceled），见 unresolved-queue.md
- 2020 MLS is Back 锦标赛小组赛阶段 36 场计入 regular-season（ESPN slug 即 regular-season），淘汰赛阶段（round-of-16 起）与 All-Star 赛已排除——符合"仅常规赛 + 官方计入常规赛积分"口径；淘汰赛未计入常规赛积分故排除
- 2024/2025（req-20261002-004 已回传）未重复；Football-Data closing 赔率未重抓；无 Qimen/九宫/模型/赔率字段

## 已知局限

1. 2020 的 3 场 postponed（Nashville/Dallas 退赛 MLS is Back）无 venue/kickoff（ESPN 未提供），记 partial
2. 2020 的 7 场 canceled 保留整行（有 venue 与原定 kickoff），记 partial
3. venue 名称为 ESPN 当前数据原貌，2020 后改名的球场以新名出现（见上）
