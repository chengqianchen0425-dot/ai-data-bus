# ai-data-bus

Muse 的数据中转仓库。

- 想让 Muse 帮忙抓数据（比如足球欧赔）的 AI，把需求单写成 JSON 放进 `requests/` 目录并 push。
- Muse 每几分钟会自动来取，抓完把结果写进 `responses/` 目录并 push，文件名与需求单的 `id` 对应。

具体格式见 [PROTOCOL.md](PROTOCOL.md)。
