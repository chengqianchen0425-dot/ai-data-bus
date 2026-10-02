# 未解决队列（UNRESOLVED_QUEUE）—— req-20261002-016

## U1–U3：2020 MLS is Back 锦标赛因退赛从未补赛的 3 场（postponed）

ESPN 记为 `season.slug=regular-season`、`status=STATUS_POSTPONED`，venue 字段为空（ESPN 未提供），
属于"锦标赛小组赛阶段计入常规赛"的原定赛程，因 Nashville SC 与 FC Dallas 退出锦标赛从未举行、也未补赛。
整行保留在 `mls-2020-regular-season-fixtures.csv`（status=postponed），kickoff/venue 为 NULL → partial。

| id | 原定日期 | 对阵 | provider_fixture_id |
|---|---|---|---|
| U1 | 2020-07-09（UTC） | Nashville SC vs Chicago Fire FC | 571506 |
| U2 | 2020-07-10（UTC） | FC Dallas vs Vancouver Whitecaps FC | 571509 |
| U3 | 2020-07-21（UTC） | FC Dallas vs San Jose Earthquakes | 571534 |

精确的 event id / stable_match_key 请见 CSV 中 `status=postponed` 的三行。
交叉验证：Wikipedia "2020 Major League Soccer season" 记常规赛共 292 场（已排除未打场次），
与本 CSV 的 292 full_time 一致。

## U4–U10：2020 COVID 期间取消的 7 场（canceled）

保留整行（status=canceled），venue 与原定 kickoff 有值 → partial。

| 原定日期 | 对阵 | 场地 |
|---|---|---|
| 2020-10-08 | Colorado Rapids vs LAFC | Dick's Sporting Goods Park |
| 2020-10-10 | Colorado Rapids vs LA Galaxy | Dick's Sporting Goods Park |
| 2020-10-12 | FC Dallas vs Minnesota United FC | Toyota Stadium |
| 2020-10-15 | Seattle Sounders FC vs Colorado Rapids | Lumen Field（2020 年时称 CenturyLink Field） |
| 2020-10-19 | Colorado Rapids vs Real Salt Lake | Dick's Sporting Goods Park |
| 2020-10-22 | Colorado Rapids vs Sporting Kansas City | Dick's Sporting Goods Park |
| 2020-11-02 | Sporting Kansas City vs Minnesota United FC | Children's Mercy Park |

## 2020 kickoff 交叉核对状态

前轮（09:23 CST 前）称有 77 行缺 kickoff（FBref/worldfootball 403）。
本轮从 ESPN 独立重建后：292 场 full_time 的 kickoff 全部恢复（0 缺失）。
母代理已派发真浏览器任务读取 mlssoccer.com 2020 官方赛程归档做交叉核对；
待结果返回后对比 ESPN kickoff（冲突按上限带回），再写最终 ok 回执。
若官方源不可读，以 ESPN 数据为准（kickoff 字段 complete），unresolved 仅保留上列 10 场。
