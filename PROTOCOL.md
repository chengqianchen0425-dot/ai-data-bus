# ai-data-bus 需求单协议（v1）

## 目录
- `requests/` — 需求方（Codex / DeepSeek / 人）写需求单，文件名 `<id>.json`
- `responses/` — Muse 写回执，文件名 `<id>.json`，与需求单的 `id` 对应

## 需求单格式

```json
{
  "id": "req-20261001-001",
  "type": "odds_1x2",
  "params": {
    "match_url": "https://live.nowscore.com/1x2/2789344.htm",
    "match": "曼联 vs 曼城（选填，帮助核对）",
    "companies": ["威廉希尔", "平博", "bet365"],
    "fields": ["初指", "即时"]
  },
  "created_at": "2026-10-01T20:05:00+08:00"
}
```

字段说明：
- `id`：全局唯一，建议 `req-YYYYMMDD-序号`。
- `type`：任务类型，v1 只支持 `odds_1x2`。
- `params.match_url`：必填。捷报网（live.nowscore.com/1x2/…）或足彩网（fenxi.zgzcw.com/…/bjop）的单场欧赔页链接。
- `params.companies`：中文常用名数组，如威廉希尔、平博、bet365、立博、必发。Muse 负责映射到网站上的脱敏显示名。
- `params.fields`：`["初指", "即时"]` 或其中之一，缺省为都要。

## 支持的类型（v1）
- `odds_1x2`：单场欧赔。返回每家公司的初指/即时主胜、平、客胜赔率。

## 回执格式

成功：
```json
{
  "id": "req-20261001-001",
  "status": "ok",
  "data": {
    "match": "曼彻斯特联 vs 曼彻斯特城",
    "kickoff": "2026-01-17 20:30",
    "odds": [
      {
        "company": "威廉希尔",
        "初指": {"home": 2.90, "draw": 3.60, "away": 2.20},
        "即时": {"home": 2.95, "draw": 3.55, "away": 2.18}
      }
    ]
  },
  "fetched_at": "2026-10-01T20:10:00+08:00"
}
```

失败：
```json
{"id": "req-20261001-001", "status": "error", "error": "原因一句话"}
```

## 规则
1. 发单前先看 `responses/` 里有没有同名回执，避免重复提交。
2. 一次一个文件、一个请求。
3. 回执约 5 分钟内产出；超时未出可换新 `id` 重发。
