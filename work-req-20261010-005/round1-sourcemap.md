# req-20261010-005 round1 源地图（2026-10-10 17:30 CST）

## 请求摘要
J1 2018–2025 赛季，2670 场：fixture 身份 + 90分钟赛果 + BTTS 标签 + 1X2 证据（Bet365/Pinnacle/William Hill，语义相位标注）。

## 场次口径核验（已验证 ✓）
2670 = 306×5（2018/19/20/22/23，18队×34轮）+ 380×3（2021/24/25，20队×38轮）
来源：FBref J1 League Seasons 表（2021/2024/2025 为 20 队，其余 18 队；2020 疫情赛季 18 队 34 轮）。
请求 expected=2670 与该结构完全吻合。最终审计以 discovered 为准。

## 源能力（能力矩阵 + 本轮搜索层探测）
### 赛果/BTTS 维度
- FBref J1 赛季页（2018–2025 全覆盖；赛季页为服务端渲染表格，文本层可读）→ fixture 身份 + 90分钟比分 → BTTS 确定性推导（双方≥1=yes；任一0球=no；缺比分=unavailable）。fbref.com J1 League Seasons 已验证赛季结构。
- 备用：Flashscore archive（赛季归档）、FootyStats J1 fixtures。
- OpenFootball japan 仓库：本轮 api.github.com 探测 repos/openfootball/japan 返回 404，J1 覆盖待验证（不作为主路）。
- Football-Data.co.uk：无 J1（联赛清单无覆盖）。

### 历史赔率维度（Bet365 / Pinnacle / William Hill）
- TotalCorner：J1 单场 1X2 约回 2014（能力矩阵）；Pinnacle 带时间戳赛前 tick（J1 试点单场约 60，2026-10-02）；免费层仅 Oldest/Recent 双端点，无 true opening 标注。h2h 已 403 停手（保 IP），只碰单场 odds 页。
- SoccerPunter：J1 单场 livesoccerodds 页存在（如 2015 Gamba Osaka vs Sanfrecce Hiroshima 页已索引）；H 弹窗 tick 方法论已在 2021 意甲验证通过（逐条过滤、日期互换 bug 修正规则已沉淀）。
- OddsPortal / BetExplorer：美国出口 IP 下欧版三家 0 覆盖（2026-10-10 浏览器级验证，死路登记维持，本轮不再派）。
- telefootball.net：仅 bet365 单一快照、无开/即分列（证伪登记）。

## 下一轮路由（分站并行，按 2026-10-07 分工铁律）
- A路：FBref 批量 fixture+比分+BTTS（文本层/脚本，确定性）→ 目标 2670 行 fixture 身份全覆盖。
- B路：TotalCorner J1 单场 1X2 快照 + Pinnacle tick（真浏览器）。
- C路：SoccerPunter J1 逐公司 tick（真浏览器，H弹窗法）。
- B/C 需真浏览器，由主代理派 browser.spawn_task（hook worker 不派 JS 渲染任务；文本层对这些页不可达）。
- 数量口径：expected=2670 已结构验证；discovered<expected 则进 unresolved_queue（uq_class 分类），不编数。
