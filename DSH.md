# DSH 接入 ai-data-bus（DeepSeek Harness 侧）

> 镜像 Codex 的对接方式：同一个 GitHub 私有仓库 `ai-data-bus` 做中转，`requests/` 发单、`responses/` 收单。用 `target` 字段分 lane，互不干扰。

## 部署步骤（4 步）

1. **clone 仓库到本地**（建议单独一个目录，别和 Codex 的 clone 共用，避免互相踩）：
   `git clone https://github.com/chengqianchen0425-dot/ai-data-bus.git d:\ai-data-bus-dsh`
2. **git 免密推送**：本机如已给 Codex 配过 credential helper，直接复用；没有就配一次。
3. **DSH 里新建定时任务**：
   - 名称：`ai-data-bus-dsh-lane`；周期：每 2 分钟；工作区：上一步的目录
   - 模式：极简模式（纯终端，最省 token）；文件写入授权给该目录
   - 提示词用下面这段（原样贴）：
4. **测试**：让 Muse 发一个 `target=dsh` 的测试单，看 DSH 能不能接住、写回执、push。

## 定时任务提示词（原样贴进 DSH）

```
你是 ai-data-bus 的 DSH 取件员，每轮只做以下事：

1. cd 到工作区，git pull --rebase
2. 扫描 requests/*.json：找 target=dsh 且（responses/<id>.json 不存在，或 status=processing 且超过 15 分钟没更新）的单
3. 没活 → 直接结束，不做任何多余事
4. 有活 → 读请求全文 → 干活 → 写 responses/<id>.json（顶层 from: dsh；先写 status=processing 占位并 push，完工改 ok/error；data.audit 给 expected/discovered/complete/partial/missing 五个数）
5. git add/commit/push

铁律：id 全网唯一不复用；ok 永不回退；缺字段记 NULL 不猜测；说不清来源的数据不要；同一单连续 3 轮无实质进展就停手，回执写清卡点，不静默空转。
```

## 协议（备查）

- **发单**：写 `requests/req-YYYYMMDD-NNN.json`，`id` 全网唯一（不许复用 Codex/Muse 用过的）。
  - 给 Muse 干活：`"target": "muse"`（或不写，默认 muse），可加 `"from": "dsh"`。
- **回执**：`responses/<id>.json`，顶层带 `"from": "dsh"`。
- **Muse 派给 DSH 的单**：Muse 会写 `target=dsh` 的请求，指令放 `to_dsh` 字段，DSH 照做、结果写回 `responses/`。

## 省 token 说明

- 没活的轮次只有一次 git pull + 目录扫描，极简模式下 token 开销极小。
- 有活才进入正常干活流程；任务切小，一单一回执。
