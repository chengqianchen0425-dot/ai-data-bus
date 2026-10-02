# 场馆城市 → IANA 时区映射（派生参考，work-016）

ESPN 只给 UTC 时间（`scoreboard.events[<id>].date`）与 venue 地址城市。
行级 CSV 的 `local_timezone` 与 `kickoff_local` 由以下映射 + Python zoneinfo 派生（夏令时自动处理）。

| ESPN 城市（归一化后） | IANA 时区 |
|---|---|
| Toronto, Montreal | America/Toronto |
| Vancouver | America/Vancouver |
| Seattle, Portland, San Jose, Los Angeles, Carson, Stanford | America/Los_Angeles |
| Sandy, Salt Lake City, Commerce City | America/Denver |
| Kansas City, Frisco, Dallas, Houston, Bridgeview, Chicago, Saint Paul, Minneapolis, Nashville | America/Chicago |
| Columbus, Cincinnati, Orlando, Atlanta, Washington, Harrison, New York, Chester, Philadelphia, Foxborough, Miami, Fort Lauderdale, Boyds, Annapolis, East Hartford, Bay Lake | America/New_York |

归一化规则：
- ESPN `venue.address.city` 形如 "Houston, Texas" → 取逗号前
- "New York City" → "New York"；"Toyota Stadium"（ESPN 对 FC Dallas 主场填在城市字段）→ "Frisco"

例外：3 场 2020 postponed 行无 venue → `local_timezone` NULL，记 partial。
`venue_override` 标记不改变时区映射（按实际场地城市换算）。
