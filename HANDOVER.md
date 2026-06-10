# V3.3.3-Core 项目完整交接文档

> 项目路径: D:\V3.3.3-Core
> 最后活跃: 2026-06-09
> Python 3 + Flask + SQLite

---

## 一、项目定位

足球赛事量化分析系统，竞彩/亚盘方向预测。
工作流：采集数据 → 蒙特卡洛模拟 → 物理概率 → DDI资金流偏差 → 贴合度评分 → 评级 → 前端展示。

---

## 二、启动方式

`
cd D:\V3.3.3-Core
python app.py
# 浏览器打开 http://localhost:5000
`

主页面有 5 个版本迭代（/v1 ~ /v5），当前主入口是 /（index.html）。

---

## 三、核心架构

### 3.1 Flask 后端（app.py）

26 个路由，分为三类：

**JSON API（12个）：**
- GET /api/latest — 加载最新预测数据
- POST /api/parse — 解析原始数据
- POST /api/analyze — 分析 factor_params
- POST /api/review — 提交复盘
- GET /api/reviews — 获取复盘记录
- POST /api/live/recalibrate — 临场重校
- GET /api/live/info — 实时信息
- GET /api/history/runs — 历史运行统计
- GET /api/history/matches — 按日期查历史比赛
- GET /api/v2/data — V2 数据
- GET /api/backtest/runs — 回测数据
- GET /api/doc/sections — 文档章节
- GET /api/plan/<level> — 方案推荐

**页面路由（12个）：**
/ /test /full_test /debug /v1 /v2 /v3 /v4 /v5 /plan/<level>
/bak /pre_reorder /v4_backup /v4_clean

**JS 文件服务（2个）：** /charts.js /live.js

### 3.2 数据库（database.py + framework.db）

SQLite，两张核心表：
- **runs** — 每次运行记录（date, run_type, factor_params, total_matches, hit_count, avg_fit_score）
- **matches** — 单场分析记录（50+字段：主客队、lambda值、物理/市场/校准概率、DDI、贴合度、评级、方向、比分、命中等）

### 3.3 前端（templates/index.html + charts.js）

单页应用，Vanilla JS 渲染。功能：
- 赛事评分表格（评级、lambda值、DDI、S7分数）
- 点击展开详情（lambda差值、S7说明、诱盘分析、风险提示）
- 图表（lambda对比柱状图、物理概率 vs 市场概率对比）
- v4/v5 是当前最新迭代版本

### 3.4 数据目录（data/）

存放所有 JSON 数据，结构：
- data/input/ — 输入（locked_data.json + factor_params.json）
- data/output/ — 每次 pipeline 输出（按 run_id 子目录）
- data/processed/ — 已处理的输入档案
- data/archive/ — 归档

核心数据文件：
- locked_data.json, factor_params.json — 原始输入
- match_info.json — 标准化比赛信息
- monte_carlo_result.json — MC模拟结果
- ddi_result.json — DDI资金流偏差
- fit_score_result.json — 贴合度评分
- rating_result.json — 评级和方向
- ai_judgment.json — AI综合判断
- review.json — 复盘数据

---

## 四、核心计算模块

| 模块 | 职责 |
|---|---|
| config.py | 全局参数（联赛xGA、兑换系数、MC参数、DDI参数、因子上限） |
| lambda_calc.py | lambda值计算 |
| monte_carlo.py | 蒙特卡洛引擎 |
| ddi.py | DDI资金流偏差/校准 |
| fit_score.py | 贴合度评分（含否决规则） |
| rating.py | 评级/方向判定 |
| parser.py | 原始文本解析 |
| pipeline.py | 自动分析管道 |
| auto_pipeline.py | 一键全流程（Rev1.15） |
| run_all.py | 完整运行脚本 |
| live_ddi.py | 临场SP重校引擎 |
| plan_engine.py | 方案推荐（单关/串关策略） |
| backtest.py | 回测模块 |
| review.py | 复盘模块 |
| database.py | SQLite ORM层 |
| enrich_odds.py | 赔率增补 |
| fetch_jczq.py / fetch_form.py | 数据采集 |

---

## 五、运行流程

1. 获取 locked_data.json + factor_params.json
2. 放入 data/input/ 或手动触发 auto_pipeline.py
3. pipeline 依次执行：lambda_calc → monte_carlo → ddi → fit_score → rating → ai_judgment
4. 结果写入 data/*.json
5. 刷新前端首页（/），自动加载最新数据

---

## 六、已知状态 & 待处理事项

1. **app.py 第364-366行有重复的 v4_edit 定义**（/v5 路由后跟了一个多余的 v4_edit），功能无影响但需清理。
2. **备份/历史版本较多**：v1_old/v2_old/v3_old + v4_backup/v4_clean + bak/pre_reorder，可清理。
3. **根目录大量一次性调试脚本**（do_fix*.py, add_*.py, find_*.py, _fix*.py 等），已不再使用，可归档。
4. **framework.db 含历史 runs 和 matches 数据**，可直接用于复盘统计。
5. **static/** 目录有 bg1.png / bg2.png 两张背景图。

---

## 七、快速导航

| 文件 | 路径 |
|---|---|
| Flask服务器 | D:\V3.3.3-Core\app.py |
| 配置 | D:\V3.3.3-Core\config.py |
| 数据库 | D:\V3.3.3-Core\database.py |
| 自动管道 | D:\V3.3.3-Core\auto_pipeline.py |
| 前端主模板 | D:\V3.3.3-Core\templates\index.html |
| 前端JS | D:\V3.3.3-Core\templates\charts.js |
| 前端实时JS | D:\V3.3.3-Core\templates\live.js |
| 数据目录 | D:\V3.3.3-Core\data\ |
| 方案引擎 | D:\V3.3.3-Core\plan_engine.py |
| 临场重校 | D:\V3.3.3-Core\live_ddi.py |
| 回测 | D:\V3.3.3-Core\backtest.py |
| 复盘 | D:\V3.3.3-Core\review.py |
| 数据采集 | D:\V3.3.3-Core\fetch_jczq.py |
| 赔率增补 | D:\V3.3.3-Core\enrich_odds.py |
