# req-20261010-003 荷甲 2018/19 Pinnacle 初指批次（2026-10-10）

## 交付
- `nowgoal_1819_pinnacle_opening.jsonl`：81 行，81/81 成功，0 缺失
- 校验：JSON全通过；bookmaker 全为 pinnacle；field_semantics 全为 true_opening；81 个 fixture_key 无重复；source_url/final_url/field_locator 的比赛 ID 三处一致；recorded_at 与比赛日期差均 ≤4 天

## 方法论（任务侧报告，原样保留）
- 来源：NowGoal 官方镜像 https://www.nowgoal831.com（www.nowgoal.com 已被域名停放页占据）
- 路径：比赛页 https://www.nowgoal831.com/1x2-odds/{matchId} 的 "Initial"（初指）视图
- 底层数据接口 //1x2.nowgoal26.com/{matchId}.js（解析至 1x2.nowgoal50.com）交叉验证赔率与时间戳
- 比赛 ID 来自 football.nowgoal.net 2018-2019 赛季 s16_en.json，按日期+主客队核对；站内别名已映射（Den Haag=ADO Den Haag 等）
- 时区：站内显示 UTC+8，recorded_at 为 Initial 视图 "Last Updated" 列转 ISO+08:00
- 赔率格式：十进制 decimal（经隐含概率与站内 HWR%/DR%/AWR% 反推一致）

## 重要语义警示（必须写入最终回执）
NowGoal 的 "initial" 初指 Last Updated 时间部分非常接近甚至晚于开球时间（如 1551882 Feyenoord-NAC Breda 为开球前约4分钟；多场为开球后次日凌晨）。其 "initial" 实为数据流对初指的首次捕获/刷新记录，**不等同于 Pinnacle 真实市场开盘时刻**；gameDetail 显示部分比赛 Pinnacle 最早变动记录早于 Initial 视图的 Last Updated。true_opening 标记依据的是来源对 "Initial/初指" 的明确标注，而非对博彩公司真实开盘时刻的独立核验。上游使用时必须结合 recorded_at 自行评估时效性。

## UNRESOLVED_QUEUE
空。81/81 全部找到 Pinnacle 初指。
