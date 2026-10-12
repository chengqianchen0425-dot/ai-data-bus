# Workstream C: 瑞士超 1,584 场历史 OPENING 1X2 赔率 — 源可用性调研

> req-20261012-002 Workstream C · 2026-10-12 · 子代理调研（仅 browser.search / browser.open，无真浏览器）
> 目标：为 2018/19–2025/26 瑞士超 1,584 场找**独立于 Football-Data 的 true opening 1X2**（优先 Pinnacle、Bet365）。

## 结论先行

**1,584 场全覆盖的 true opening 1X2，用免费、可文本抓取的源，在本环境做不到。**

- 数据本身存在的地方（OddsPortal、SoccerPunter）全部被墙/地域限制/付费墙挡住；
- 能免费打开的地方（Football-Data、GitHub 复刻库、BetExplorer/Bet365.us 残片）要么根本没有 opening 列，要么只有 closing；
- 唯一"可能有"的两条窄路（OddsPortal 欧版真浏览器、Win007 初指）都需要真浏览器＋欧洲出口 IP，超出本次任务范围。

Football-Data 的 pre-close（周五/周二采集快照）是最近的免费代理，但按请求语义**不许改名为 opening**。

## 逐源裁决

| 源 | 瑞士超有 true opening 1X2？ | 裁决 | 证据 |
|---|---|---|---|
| Football-Data SWZ.csv | 否 | source_missing | 官方 notes.txt：只有 pre-close + closing，无 opening 列（能力矩阵已登记） |
| OddsPortal | 有，但拿不到 | access_blocked | 档案回溯到 1998/99；单场页有分公司 opening+时间戳。但：①文本层只回 SEO 骨架（本次实测 `oddsportal.com/football/switzerland/super-league/` 仅 2 行标题）；②Cloudflare 墙；③本机房美国出口 IP 下全站只显示 bet365.us/BetMGM.us/DraftKings/FanDuel，欧版 Bet365/Pinnacle/WH 零覆盖（2026-10-10 浏览器级验证） |
| BetExplorer | 拿不到 | access_blocked | 本次实测瑞士场次页（Basel–Young Boys 2009）文本层只有骨架（比分/场馆/时间），赔率表为空；geo='us' 下仅 bet365.us closing，无 opening 标注；Pinnacle/WH 不存在（2026-10-10 验证） |
| TotalCorner | 拿不到 | access_blocked | 本次文本层直接 403；>365 天的比赛单场 odds 页只显示无公司归因的初盘/收盘摘要，完整分公司 tick 全 VIP 门控（2026-10-10 J1 20场试点 0 条可交付）；1,584 场全部 >365 天 |
| SoccerPunter | 有，但付费墙 | access_blocked | 瑞士超单场页明确写 "opening odds history … available exclusively to Platinum Members only"；免费层只显示公司名占位。用户铁律：不碰付费 |
| Bettors.club | 否 | source_missing | 文本层仅 tipster 预测页，无赔率历史/移动页（2026-10-03 证伪） |
| Tipsme(.hk) | 否 | source_missing | Close 列多为滚球终场赔率，不当赛前；5 场试点后降级 |
| GitHub xgabora/Club-Football-Match-Data | 否 | source_missing | 数据源就是 Football-Data.co.uk，同构，无 opening，非独立源 |
| GitHub ovignez-hash "Bookmaker Brain" | 否 | source_missing | 仅 Big 6（英/西/意/德/法/葡），无瑞士；且走 Gumroad 付费下载 |
| AiScore | 未验证 | partial/unverified | 预测页有"อัตราต่อรองเริ่มต้น"（opening odds）栏目（如 Basel–Young Boys 页显示 2.35/3.80/2.45），但公司归因不明、历史场次覆盖未验证、非档案型源。需真浏览器逐场核验 |
| Win007/NowScore（捷报网） | 未验证 | candidate | 维度映射=初指源；但赔率表 JS 渲染、文本层仅骨架；历史瑞士场次初指保留情况未验证。需真浏览器 |

## 10 场样本实测

样本（随机抽取，跨 2018/19、2021/22、2024/25）：

| # | 赛季 | 日期 | 对阵 | 尝试的独立源 | 结果 |
|---|---|---|---|---|---|
| 1 | 2018/2019 | 2019-05-12 | Luzern vs Grasshoppers | OddsPortal / BetExplorer / TotalCorner / SoccerPunter | 全部 blocked（墙/骨架/403/付费墙），无 opening 值 |
| 2 | 2018/2019 | 2018-09-02 | Luzern vs Grasshoppers | 同上 | 同上 |
| 3 | 2018/2019 | 2018-07-28 | Xamax vs Basel | 同上 | 同上 |
| 4 | 2018/2019 | 2018-11-24 | Xamax vs Zurich | 同上 | 同上 |
| 5 | 2021/2022 | 2021-11-07 | Basel vs St. Gallen | 同上 | 同上 |
| 6 | 2021/2022 | 2021-10-31 | Lausanne vs Luzern | 同上 | 同上 |
| 7 | 2021/2022 | 2021-09-25 | Servette vs Lausanne | 同上 | 同上 |
| 8 | 2024/2025 | 2025-04-12 | Zurich vs Basel | 同上 | 同上 |
| 9 | 2024/2025 | 2024-08-24 | Grasshoppers vs Sion | 同上 | 同上 |
| 10 | 2024/2025 | 2025-03-30 | Lausanne vs Luzern | 同上 | 同上 |

**样本结论：10/10 在免费文本层无任何独立源可给出 opening 1X2。** 这不是抽样运气问题——四个主要档案源的结构性 blocker（Cloudflare / geo-IP / 403 / 付费墙）与联赛无关，对 1,584 场一视同仁。

### 时间戳语义说明（诚实标注）
- 本次未从任何源取得可验证的 opening 值，因此**没有"这是不是真 opening"的待裁决样本**；
- 若后续走通 OddsPortal 欧版：其单场页 opening 格带时间戳 tooltip（如 "Opening Odds 1.83 @ 06.09 23:11"），语义为该公司首次挂牌价，可采信为 true opening；
- SoccerPunter 的 "opening odds" 为 Platinum 会员可见的初盘历史，语义可采信但付费墙外不可验证；
- Football-Data 的 pre-close（周五/周二采集）**不是** opening，不许混用。

## 能否做到 1,584 场全覆盖？

**在本环境 + 免费约束下：不能。** 诚实分级：

- **0% 可交付**（当前）：免费文本层无一源可出 opening。
- **理论可行、需加资源**：
  1. 真浏览器 + 欧洲出口 IP → OddsPortal 瑞士超 8 季单场页（分公司 opening + 时间戳）。这是唯一已证实"数据存在"的免费路径，但需解决 IP 地域问题（参考：西甲 39 场用欧洲区出口重跑的预案）。
  2. Win007 初指（需真浏览器验证历史保留）。
- **被用户铁律排除**：SoccerPunter Platinum（付费）。

## 建议

1. Workstream C 在当前约束下判为 **access_blocked（源端结构性阻挡），不是 pending_work**——不建议继续用文本层撞墙；
2. 若用户后续批准"欧洲出口真浏览器"资源，OddsPortal 是第一优先级（8 季×分公司 opening 全，单场页结构稳定）；
3. 在那之前，Q-opening 相关字段保持 NULL + `access_blocked`（带本报告链接），不要用 pre-close 冒充。

---
*方法：browser.search（4 轮）+ browser.open（4 次：OddsPortal 联赛页、BetExplorer 瑞士场次页、TotalCorner、SportsbookReview 线程）。未做真浏览器抓取，未尝试绕过任何墙/付费。*
