# ai-data-bus 需求单协议（v2）

## 目录
- `requests/` — 需求方（Codex / DeepSeek / 人）写需求单，文件名 `<id>.json`
- `responses/` — Muse 写回执，文件名 `<id>.json`，与需求单的 `id` 对应

## 通用规则
1. 发单前先看 `responses/` 里有没有同名回执，避免重复提交。
2. 一次一个文件、一个请求。
3. 回执约 5 分钟内产出（`deep_research` 除外：首轮先回 `processing` 占位，做完再覆盖为最终结果）。
4. `id` 全局唯一，建议 `req-YYYYMMDD-序号`。
5. 回执 `status`：`ok` 成功 / `error` 失败（看 `error` 字段写的原因） / `processing` 处理中（仅耗时任务）。
6. 抓不到、搜不到就写 `error`，不要编造数据。

## 类型 1：odds_1x2（单场欧赔）

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

- `params.match_url`：必填。捷报网（live.nowscore.com/1x2/…）或足彩网（fenxi.zgzcw.com/…/bjop）的单场欧赔页链接。
- `params.companies`：中文常用名数组，如威廉希尔、平博、bet365、立博、必发。Muse 负责映射到网站上的脱敏显示名。
- `params.fields`：`["初指", "即时"]` 或其中之一，缺省为都要。

成功回执：
```json
{
  "id": "req-20261001-001",
  "status": "ok",
  "data": {
    "match": "曼彻斯特联 vs 曼彻斯特城",
    "kickoff": "2026-01-17 20:30",
    "odds": [
      {"company": "威廉希尔", "初指": {"home": 2.90, "draw": 3.60, "away": 2.20}, "即时": {"home": 2.95, "draw": 3.55, "away": 2.18}}
    ]
  },
  "fetched_at": "2026-10-01T20:10:00+08:00"
}
```

## 类型 2：web_fetch（打开指定网页抓数据）

```json
{
  "id": "req-20261002-001",
  "type": "web_fetch",
  "params": {
    "url": "https://example.com/some-page",
    "extract": "用自然语言描述要提取什么，例如：页面表格中每支球队的胜/平/负场次",
    "format": "期望的返回结构，例如：json 数组，每项 {team, w, d, l}（选填，不填则按清晰的 json 返回）"
  },
  "created_at": "2026-10-02T10:00:00+08:00"
}
```

成功回执：`{"id": "...", "status": "ok", "data": {...按 format 组织的数据...}, "fetched_at": "..."}`

## 类型 3：web_search（联网搜索）

```json
{
  "id": "req-20261002-002",
  "type": "web_search",
  "params": {
    "query": "搜索关键词或一个具体问题",
    "want": "想找到什么信息（选填，帮助聚焦）",
    "max_results": 5
  },
  "created_at": "2026-10-02T10:05:00+08:00"
}
```

成功回执：
```json
{"id": "...", "status": "ok", "data": {"results": [{"title": "...", "url": "...", "snippet": "..."}]}, "fetched_at": "..."}
```

## 类型 4：deep_research（深度调研，耗时）

```json
{
  "id": "req-20261002-003",
  "type": "deep_research",
  "params": {
    "topic": "研究主题",
    "questions": ["想弄清的问题1", "想弄清的问题2"]
  },
  "created_at": "2026-10-02T10:10:00+08:00"
}
```

首轮回执（占位）：`{"id": "...", "status": "processing", "note": "研究进行中"}`。
最终回执：`{"id": "...", "status": "ok", "data": {"report": "markdown 全文"}, "fetched_at": "..."}`。

## 类型 5：data_task（数据处理）

把原始数据贴进需求单，描述要做什么，返回处理结果。

```json
{
  "id": "req-20261002-004",
  "type": "data_task",
  "params": {
    "task": "要做什么的自然语言描述，例如：算出每支球队的场均进球并排序",
    "data": {"任意": "JSON 数据"},
    "data_text": "纯文本数据（与 data 二选一）"
  },
  "created_at": "2026-10-02T10:15:00+08:00"
}
```

成功回执：`{"id": "...", "status": "ok", "data": {"result": ...}, "fetched_at": "..."}`
