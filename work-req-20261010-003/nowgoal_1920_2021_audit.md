# req-20261010-003 荷甲 2019/20 + 2020/21 初指批次（2026-10-15，用户亲命"执行"提前重派）

## 交付
- `nowgoal_1920_opening.jsonl`：182 行（bet365 68 / william_hill 67 / pinnacle 47）
- `nowgoal_2021_opening.jsonl`：202 行（william_hill 69 / bet365 67 / pinnacle 66）
- 合计 384/384，0 缺失；UNRESOLVED_QUEUE 空
- 校验：JSON 全通过；(fixture_key, bookmaker) 384 唯一；三季合计 465/465 唯一；字段 11 项齐全；
  赔率 >1；recorded_at 全部落在比赛日前后 7 天内

## 方法论（与 2018/19 批次同源，改为纯静态抓取，无需真浏览器）
- 赛季赛程 JSON：`https://football.nowgoal1.top/jsData/matchResult/json/{2019-2020,2020-2021}/s16_en.json`
  （条目 `[matchId, sclassId, -1, 'YYYY-MM-DD HH:MM'(+08:00), homeId, awayId, score, ...]`；
  注意赛程时间为北京时间，匹配 fixture 的阿姆斯特丹当地日期需经 `Asia/Shanghai -> Europe/Amsterdam` 换算，
  跨午夜场次（如 2019-08-04 02:45+08:00 = 2019-08-03 20:45 CEST）否则差一天）
- 队名别名：Den Haag=ADO Den Haag、Ajax=AFC Ajax、FC Emmen=Emmen、Twente=FC Twente Enschede、
  Utrecht=FC Utrecht、For Sittard=Fortuna Sittard、Heerenveen=SC Heerenveen、Heracles=Heracles Almelo、
  Vitesse=Vitesse Arnhem、Waalwijk=RKC Waalwijk、Zwolle=PEC Zwolle
- 赔率接口：`https://1x2.nowgoal50.com/{matchId}.js`（需 Referer + UA，否则 000；
  gzip 压缩，需解压；`game=Array(...)` 每条 `id|oddsId|name|initH|initD|initA|...|lastUpdated(UTC)|...`，
  取 Initial 三列 + lastUpdated 转 +08:00）
- 博彩公司行匹配：Pinnacle / Bet 365 / William Hill（大小写+空格归一化）
- 215 个独立 matchId，384 个组合；抓取间隔 0.8s，无 429

## 重要语义警示（与 1819 批次一致，必须写入最终回执）
NowGoal 的 "initial" 为其数据流首次捕获/刷新记录，不等同于博彩公司真实市场开盘时刻；
true_opening 标记依据来源 "Initial/初指" 标注，上游须结合 recorded_at 自行评估时效性。

## UNRESOLVED_QUEUE
空。384/384 全部找到对应博彩公司初指。
