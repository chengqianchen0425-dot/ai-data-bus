# req-20261006-006 heartbeat

## 2026-10-07 08:45 +08:00 — 启动
- 长轮 deep_research 启动。用户授权：长轮（数小时可）＋降级标准（aggregate 证据可接受、字段可放宽、门槛可降低）。
- request_sha=1b9f1c2961eaeb3b 已校验一致。dp_used=false。
- 起点：008 回执已有 venue_by_season（8 季）＋stadium_coords（31 球场）；352 fixtures 已从请求单提取。
- 本轮计划：重抓 4 季 en.wikipedia Stadia and locations 表（尤其 2021/22，当时是前后季交叉推导）→ 补球场坐标缺口 → 按 fixture_key 展开 352 行 → 分片落盘 → 异地赛抽样复核 → 写 ok 回执。

## 2026-10-07 09:00 +08:00 — 四季球场表复核完成
- 2022/23、2023/24、2024/25 三季 en.wikipedia "Stadia and locations" 表已重抓复核，与 008 crosswalk 一致（3 处球场别名已记录：Chaves/Moreirense/Famalicão）。
- 2021/22 季页面经 API 确认：该节只有位置地图、无球场表；沿用 008 的 2020/21+2022/23 交叉推导（18 队主场无变更记录），属用户授权的 aggregate 证据。
- 4 季页面 HTML 已存档 work-req-20261006-006/wiki-*.html，sha256 已取。

## 2026-10-07 09:15 +08:00 — 352 行展开完成
- 352/352 行全部带 venue＋venue_city＋WGS84＋provenance；unresolved 0 行，无 NULL。
- 分片：shard-2021-22.json（79）、shard-2022-23.json（102）、shard-2023-24.json（70）、shard-2024-25.json（101）。
- 25 个需用球场坐标全覆盖（008 Nominatim 2026-10-03，29/29 命中）。

## 2026-10-07 09:25 +08:00 — 异地赛抽样复核完成
- B-SAD 2021/22→Estádio Nacional：独立赛报多场确认（vs Benfica 0-7、vs Porto、vs Sporting，Oeiras）。
- AVS 2024/25→Estádio do CD Aves：wildstat 多场确认（vs Casa Pia/Sporting/Estrela/Benfica，Vila das Aves）。
- Casa Pia 2024/25→Estádio Municipal de Rio Maior：3 独立源（sportradar/skysports/sportinglife）确认 2024-12-08 vs AVS 在 Rio Maior；wildstat 的 Pina Manique 记录为误标。
- 结论：映射成立，无需修正。

## 2026-10-07 09:35 +08:00 — 回执已 push
- responses/req-20261006-006.json status=ok 已推送（commit 79a04f2），352/352 行，audit 全 complete，unresolved_queue 为空。
- to_codex 已注明用户授权的降级标准；retrieved_at 时区笔误已修正说明。
- request_sha=1b9f1c2961eaeb3b 写前重验一致。dp_used=false。
