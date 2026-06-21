# Agent A：数据采集

## 一、工作职责
每天竞彩网开盘后（北京时间 11:00），对当天销售的所有比赛完成 **8 大板块** 数据采集，写入数据库（framework.db）和相关 JSON 文件。对已完赛缺比分的比赛补录赛果。

不负责：预测分析、APP 同步、部署。

## 二、8 大数据板块

| # | 板块 | 数据源 | 自动化程度 | 写入位置 |
|---|------|--------|-----------|---------|
| 1 | 比赛基本信息（编号、对阵、时间、赛事） | 竞彩网 API | 全自动 | match_info.json + DB |
| 2 | 竞彩赔率（5 彩池：had/hhad/ttg/crs/hafu） | 竞彩网 API | 全自动 | raw_jczq.json + enrich 到 match_info |
| 3 | 亚洲盘口 | 竞彩网(HKJC) | 全自动(部分) | locked_data + match_info |
| 4 | 联赛赛季数据（xG/xGA 等） | SofaScore API | 半自动 | framework.db |
| 5 | 近期战绩 | SofaScore API (fetch_form.py) | 半自动 | framework.db |
| 6 | 伤停信息 | SofaScore | 需人工介入 | framework.db |
| 7 | 战意背景（小组形势等） | 手动分析 | 需人工介入 | ai_judgment.json |
| 8 | 特殊事项（中立场地、天气等） | 手动 | 需人工介入 | ai_judgment.json |

**全自动**：运行脚本即可完成，无需人工干预。
**半自动**：脚本能抓取原始数据，但部分字段可能需要人工校验。
**需人工介入**：当前没有自动化数据源，标为"缺失"等待人工补充。

## 三、工作目录
- 项目根目录：`D:\V3.3.3-Core`
- 数据库：`D:\V3.3.3-Core\framework.db`
- 竞彩网缓存：`D:\V3.3.3-Core\data\raw_jczq.json`
- 比赛信息：`D:\V3.3.3-Core\data\match_info.json`
- 锁定比赛：`D:\V3.3.3-Core\data\locked_data.json`
- 球队档案：`D:\V3.3.3-Core\data\team_profiles.json`
- 原始赛程：`D:\V3.3.3-Core\data\wc_schedule.json`

## 四、输入输出

### 竞彩网抓取
- 源：竞彩网 API（通过 `fetch_jczq.py`）
- 输出：`data/raw_jczq.json` + 写入 framework.db
- 覆盖板块：1（基本信息） + 2（赔率）

### 赔率数据注入
- 脚本：`enrich_odds.py`
- 覆盖板块：2 + 3（亚洲盘口）
- 将 raw_jczq 数据同步到 match_info.json 和 locked_data.json

### 赛果补录
- 从竞彩网历史数据获取比分（比分 + 半全场）
- 写入 DB：actual_score, half_full, hit 字段
- 同步更新 `data/match_info.json` 和 `data/rating_result.json`
- 获取不到则标记"赛果待人工"

### 联赛数据 / 近期战绩
- 脚本：`fetch_form.py`（SofaScore 近期战绩采集 via Playwright）
- 脚本：`fetch_sofascore_data.py`
- 覆盖板块：4 + 5
- 写入 framework.db（xg 系列字段）

### 预测期数据构建
- 脚本：`build_wc_data.py`
- 构建世界杯赛程数据，生成 wc_schedule.json

### 其他数据
- `data/team_profiles.json` — 48 支球队赛前档案（FIFA 排名/身价/联合会）
- `data/wc_schedule.json` — 世界杯赛程+赔率数据

## 五、工作流程

### 步骤 1：抓取竞彩网当天开盘比赛
```powershell
cd D:\V3.3.3-Core
python fetch_jczq.py
```
说明：通过竞彩网 API 获取所有在售比赛，5 彩池数据全部拉取。
当天需要预测的比赛 = 看编号前缀对应的销售日期（如"周六"对应今天）。

### 步骤 2：赔率数据注入
```powershell
python enrich_odds.py
```
将竞彩网数据同步到 match_info.json 和 locked_data.json。
注意：新版锁定比赛数据 vs 旧版格式兼容。

### 步骤 3：合并写入数据库
通过 `database.py` 接口将新比赛写入 framework.db：
- 按 match_id 对比，新增的插入，已有的跳过
- 如果同一比赛有多个赔率版本，保留最新版本

### 步骤 4：赛果补录
对 DB 中已开赛但缺少 actual_score 的比赛：
1. 优先从竞彩网历史数据获取
2. 获取不到则跳过，标记为"赛果待人工"
3. 同步更新到 match_info.json 和 rating_result.json

### 步骤 5：赛季数据/近期战绩采集（如需）
```powershell
python fetch_form.py
```
注意：SofaScore 可能被墙，如连接失败跳过，不影响其他步骤。

### 步骤 6：日志记录
在本文档末尾追加一条记录，格式见下方示例。

## 六、工作日志

### 2026-06-21
- 首次创建本文档。项目当前状态：
  - DB 已有 32 场已完赛（有比分）、12 场预测中（033-044）
  - 预测中比赛：周六033-036、周日037-040、周一041-044
  - 竞彩网当前开盘场次编号：037-048（含今天要预测的周日037-040）
  - 8 大板块中：板块 1/2/3 自动覆盖；4/5 半自动；6/7/8 需人工
  - 已完赛的 32 场均有比分和半全场（via 竞彩网 + 人工补充）
