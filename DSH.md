# DSH 接入 ai-data-bus（DeepSeek Harness 侧）

> 镜像 Codex 的对接方式：同一个 GitHub 私有仓库 `ai-data-bus` 做中转，`requests/` 发单、`responses/` 收单。用 `target` 字段分 lane，互不干扰。

## 协议

- **发单**：写 `requests/req-YYYYMMDD-NNN.json`，`id` 全网唯一（不许复用 Codex/Muse 用过的）。
  - 给 Muse 干活：`"target": "muse"`（或不写，默认 muse），可加 `"from": "dsh"`。
  - 只是记录/不需要 Muse：不用发。
- **接单**：轮询 `requests/*.json`，找 `"target": "dsh"` 且 `responses/<id>.json` 不存在或状态非 ok/error 的单。
- **回执**：写 `responses/<id>.json`，顶层带 `"from": "dsh"`、`"status": "processing"` 起步，完工改 `"ok"` 或 `"error"`，`data.audit` 给 expected/discovered/complete/partial/missing。
- **Muse 派给 DSH 的单**：Muse 会写 `target=dsh` 的请求并在回执/请求里用 `to_dsh` 字段传指令，DSH 照做、结果写回 `responses/`。

## 轮询（建议）

每 2 分钟：`git pull --rebase` → 扫 `target=dsh` 的新单 → 干活 → 写回执 → `git add/commit/push`。
全部终态（ok/error）后当批任务结束；想省事就做成定时任务，做完自删（参考 Codex watcher 方案）。

## 铁律（和 Codex 一样）

- id 全网唯一，严禁复用。
- 回执一旦 ok 永不回退；需求变了开新 id。
- 缺字段记 NULL，不猜测；说不清来源的数据不要。
- 卡住换源，3 次无进展停手并在回执里写清卡点，不静默空转。
