# V3.3.3-Core 分析系统说明书

> 系统版本：Rev1.15（2026世界杯专属版）
> 技术栈：Python 3 + Flask + SQLite + Vanilla JS
> 最后更新：2026-06-10

---

## 一、系统概述

V3.3.3-Core 是一套面向**竞彩/亚盘**的足球赛事量化分析系统，以泊松λ模型为核心驱动力，结合蒙特卡洛模拟、DDI资金流偏差分析、多维度贴合度评分和风控降级体系，输出方向评级（S/A/B/C）及配套投注方案。

系统同时承载 **2026世界杯专属模块**，含小组赛程日历、48场积分榜（12组×4队）、淘汰赛对阵图及倒计时首页。

---

## 二、系统架构

### 2.1 整体架构

`
┌─────────────────────────────────────────────────────────┐
│                    前端层 (Vanilla JS)                    │
│   index.html · charts.js · live.js                     │
│   6视图：首页/赛程/积分/淘汰赛/赔率/Top                  │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP (JSON API)
┌────────────────────▼────────────────────────────────────┐
│                  API层 (Flask, app.py)                    │
│   /api/latest · /api/analyze · /api/live/recalibrate    │
│   /api/review · /api/history · /api/plan                │
│   /api/doc/sections · /api/wc/schedule                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                 分析引擎层 (Python)                       │
│  run_all.py → lambda_calc → monte_carlo → ddi           │
│             → fit_score → rating → review               │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│               数据存储层                                  │
│  framework.db(SQLite) · data/*.json(JSON)              │
└─────────────────────────────────────────────────────────┘
`

### 2.2 模块依赖关系

`
parser.py (原始数据解析)
    ↓
factors.py (因子计算)
    ↓
lambda_calc.py (泊松λ估计算子)
    ↓
monte_carlo.py (蒙特卡洛模拟引擎)
    ↓
ddi.py (盘口偏差分析 / 校准)
    ↓
fit_score.py (多维度贴合度评分)
    ↓
rating.py (等级评定 / 方向判定)
    ↓
app.py (API 聚合 / 前端展示)
`

### 2.3 数据采集层

| 模块 | 数据源 | 方式 | 产出 |
|------|--------|------|------|
| fetch_jczq.py | 中国竞彩网 | HTTP API | raw_jczq.json（比赛列表 + SP赔率 + 让球盘） |
| fetch_form.py | SofaScore | Playwright | 近期战绩 + 阵容 + 伤停 |
| parser.py | — | 文本解析 | locked_data.json（标准化比赛数据） |
| enrich_odds.py | 竞彩网 | API | 赔率增量同步到 match_info / locked_data |
| build_wc_data.py | — | 内置数据 | wc_schedule.json（48场小组赛 + 赔率） |

---

## 三、核心分析管道

### 3.1 管道流程

`
locked_data.json
    │
    ▼ Step 1 ─── lambda_calc.calc_initial_lambda()
    │            λ_h = xG_h × xGA_a / league_avg_xGA
    │            λ_a = xG_a × xGA_h / league_avg_xGA
    │            跨联赛时 × LEAGUE_EXCHANGE_RATE 修正
    │
    ▼ Step 2 ─── run_all.apply_factors()
    │            伤停修正 (λ×) → 伤停Boost → 战意修正
    │            → 压力修正(减半) → 松懈惩罚(0.08)
    │            → 海拔加成(≥2500m → +0.15)
    │
    ▼ Step 3 ─── MonteCarloEngine.run()
    │            泊松2000次抽样 → Bootstrap收敛校验
    │            → 物理概率 + 竞彩盘口概率 + TOP3比分
    │
    ▼ Step 4 ─── ddi.py
    │            calc_market_prob() → calc_ddi()
    │            → apply_calibration() → apply_away_cold_treatment()
    │
    ▼ Step 5 ─── fit_score.py
    │            7维度评分(满分11→归一化10)
    │            → 否决规则(熔断/备份)
    │
    ▼ Step 6 ─── rating.py
    │            determine_direction() → determine_rating()
    │            → check_wind_control(降级)
    │
    ▼ 输出 data/*.json
`

### 3.2 λ 计算 (lambda_calc.py)

**标准公式：**
`
λ_h = home_xg × away_xga / league_avg_xga
λ_a = away_xg × home_xga / league_avg_xga
`

**无 xG 替代公式 (calc_initial_lambda_alt)：**
`
λ_h = (home_goals × away_goals_conceded) / (league_avg_goals × league_avg_xga)
λ_a = (away_goals × home_goals_conceded) / (league_avg_goals × league_avg_xga)
`

**未来函数检测 (validate_temporal_integrity)：**
检查 match_info 中的 xG/战绩数据是否可能包含未来信息（如赛前不可知的赛后数据）。触发时降级数据置信度并标记警告。

### 3.3 联赛平均 xGA 参考 (config.py)

| 联赛 | xGA | 联赛 | xGA |
|------|-----|------|-----|
| 英超 | 1.40 | 西甲 | 1.35 |
| 巴甲 | 1.30 | 阿甲 | 1.25 |
| 德甲 | 1.35 | 意甲 | 1.25 |
| 法甲 | 1.30 | 荷甲 | 1.45 |
| 日职 | 1.35 | 韩K | 1.25 |
| 澳超 | 1.50 | 美职联 | 1.45 |
| 墨超 | 1.30 | 葡超 | 1.25 |
| 默认 | 1.35 | — | — |

### 3.4 跨联赛兑换系数

基于 2024-2026 解放者杯 280 场比赛拟合：

| 联赛 | 系数 | 联赛 | 系数 |
|------|------|------|------|
| 巴甲→阿甲 | 0.89 | 阿甲→巴甲 | 0.94 |
| 智利甲→巴甲 | 1.05 | 秘鲁甲→巴甲 | 1.09 |
| 玻利维亚甲→巴甲 | 1.14 | 厄瓜多尔甲→巴甲 | 1.02 |
| 哥伦甲→巴甲 | 0.97 | 乌甲→巴甲 | 0.96 |

---

## 四、因子修正系统

### 4.1 因子参数格式 (factor_params.json)

`json
{
  "id": "206",
  "home": "川崎前锋",
  "injury_home": 0,
  "injury_away": 0,
  "injury_home_boost": 0,
  "injury_away_boost": 0,
  "motivation_home": 0,
  "motivation_away": 0,
  "pressure_home": false,
  "pressure_away": false,
  "slack_home": false,
  "slack_away": false,
  "altitude_home": 0,
  "altitude_away": 0
}
`

### 4.2 因子修正顺序 (apply_factors)

| 步骤 | 因子 | 公式 | 约束 |
|------|------|------|------|
| 1 | 伤停核心 | λ × (1 + injury) | INJURY_CORE_MAX = 0.20 |
| 2 | 伤停轮换 | λ × (1 + injury_boost) | INJURY_ROTATION_MAX = 0.05 |
| 3 | 战意修正 | λ × (1 + motivation) | CAP_PLAYOFF = 0.05 / CAP_REGULAR = 0.15 |
| 4 | 反转检测 | 战意与λ方向相反时战意值减半 | — |
| 5 | 压力修正 | 高压比赛战意值再减半 | — |
| 6 | 松懈惩罚 | λ × (1 - 0.08) | SLACK_PENALTY = 0.08 |
| 7 | 海拔加成 | λ × (1 + altitude) | ALTITUDE_THRESHOLD = 2500m / BONUS = 0.15 |

---

## 五、蒙特卡洛模拟 (monte_carlo.py)

### 5.1 引擎参数

| 参数 | 值 | 说明 |
|------|-----|------|
| MONTE_CARLO_RUNS | 2000 | 默认泊松抽样次数 |
| HALF_TIME_RATIO | 0.44 | 半场占全场比例 |
| 收敛阈值 | std < 0.01 | Bootstrap 100次校验 |
| 最大次数 | 10000 | 未收敛时逐步增加 |
| 置信区间 | 95% | ci_home / ci_draw / ci_away |

### 5.2 输出数据

`json
{
  "physical": { "home_win": 0.45, "draw": 0.28, "away_win": 0.27 },
  "jc_handicap": { "rang_sheng": 0.42, "rang_ping": 0.25, "rang_fu": 0.33 },
  "convergence": { "runs": 2000, "std_home": 0.008 },
  "top2_total_goals": ["3球", "4球"],
  "top2_half_full": ["胜胜", "平胜"],
  "top3_scores": ["1-0", "2-0", "1-1"],
  "top3_scores_prob": [0.12, 0.08, 0.07]
}
`

---

## 六、DDI 校准系统 (ddi.py)

### 6.1 市场概率计算

`python
def calc_market_prob(sp_home, sp_draw, sp_away):
    inv_h, inv_d, inv_a = 1/sp_home, 1/sp_draw, 1/sp_away
    s = inv_h + inv_d + inv_a
    return { "home_win": inv_h/s, "draw": inv_d/s, "away_win": inv_a/s }
`

### 6.2 DDI 偏差计算

`
DDI = P(物理) - P(市场)
正值 = 模型比市场更看好该结果
负值 = 市场比模型更看好该结果
`

### 6.3 校准参数

| 参数 | 值 | 说明 |
|------|-----|------|
| DDI_TRIGGER_THRESHOLD | 0.08 | 触发校准的偏差阈值 |
| DDI_AMPLITUDE_RATIO | 0.3 | 校准幅度 = \|DDI\| × 0.3 |
| DDI_AMPLITUDE_CAP | 0.05 | 校准幅度上限 |
| AWAY_COLD_TREATMENT | 0.08 | 附加赛/末轮客胜冷处理（-8%） |
| VBAL_DEFAULT | 0.15 | 资金流偏差默认值 |
| DDI_MISCALIBRATION_THRESHOLD | 0.005 | 误校准检测阈值 |

### 6.4 赔率动量修正 (apply_odds_momentum_correction)

基于初始 SP → 当前 SP 的变化方向，动态修正物理概率：
- 主胜赔率下降 → 主胜概率上调
- 客胜赔率下降 → 客胜概率上调

---

## 七、贴合度评分 (fit_score.py)

### 7.1 7维度评分体系

| 维度 | 满分 | 评分函数 | 说明 |
|------|------|----------|------|
| 1. 数据置信度 | 1.5 | score_data_confidence() | API/calc/infer 三级 |
| 2. 伤病可靠性 | 1.0 | score_injury_reliability() | 有确切伤停 vs 无数据 |
| 3. 动机清晰度 | 1.5 | score_motivation_clarity() | 战意明确度评分 |
| 4. 盘口偏差 | 2.5 | score_handicap_deviation() | λ偏差 + 盘口深度联合评分 |
| 5. 临场异动匹配度 | 0.5 | score_movement_match() | 盘口变化 vs 物理方向 |
| 6. 物理市场一致性 | 0.5 | score_path_consistency() | 物理概率与市场概率一致性 |
| 7. 赛事适配度 | 0.5 | score_event_adaptability() | 联赛/杯赛类型适配 |

**总分公式：**
`
raw_total = s1 + s2 + s3 + s4 + s5 + s6 + s7
final_total = (raw_total - s7_penalty) × opp_coef × NORMALIZE
`

其中 NORMALIZE 将满分 11 分归一化到 10 分。

### 7.2 否决规则 (apply_veto_rules)

| 规则 | 条件 | 后果 |
|------|------|------|
| 熔断 | fit_score < 4.0 | 评级降为 C / MELTDOWN |
| 备份 | fit_score < 6.0 | 评级降为 BACKUP |
| 伤停不明 | injury_confidence < 0.5 | 最终分 × 0.9 |
| 战意不明 | motivation_clarity < 0.5 | 最终分 × 0.9 |
| 赛事不匹配 | event_fit < 0.3 | 最终分 × 0.8 |

---

## 八、评级与方向判定 (rating.py)

### 8.1 方向判定

`python
determine_direction(physical_prob, jc_handicap_prob, lambda_diff, sp_draw)
`

算法：
1. 当 |λ_diff| < 0.2 且平局概率高时，检查市场是否认同平局（SP_draw < 3.20）
   - 市场不认同时，将 30% 的平局概率按比例分配给胜负
2. 比较胜平负与让球胜平负的最大概率
3. 让球项概率 > 非让球项最大概率时，选择让球方向
4. 若非让球最大概率 < 0.40，强制选择"平"
5. 方向警告：λ_diff > 1.0 时，方向与λ方向相反触发警告

### 8.2 评级标准

| 等级 | 条件 | 说明 |
|------|------|------|
| S | fit_score ≥ 8.0 + 稳定信号 + 无警告 | 最高置信度 |
| A | fit_score ≥ 6.0 + 无降级因素 | 高置信度 |
| B | fit_score ≥ 4.0 或存在风险降级 | 中等/低置信度 |
| C | fit_score < 4.0 或熔断 | 低置信度，强烈不建议 |

### 8.3 降级逻辑 (check_wind_control)

| 触发条件 | 降级幅度 |
|----------|----------|
| S7 心理扰动 ≥ 0.5 | 降 1 级 |
| λ_diff > 0.5 且让球 > 2.0 | deep_discount |
| 数据置信度为中(post_match) | 降 1 级 |
| 盘口中线偏差 (1.0-1.25) | 降 1-2 级 |
| 缺少 xG 数据 | 降 1 级 |
| 伤停源头不可靠 | 降 1 级 |

---

## 九、临场重校引擎 (live_ddi.py)

### 9.1 工作流程

`
用户输入新的 SP_home / SP_draw / SP_away
    │
    ▼ 重新计算 market_prob
    │
    ▼ 重新计算 DDI = P_physical - P_market
    │
    ▼ 重新校准 apply_calibration()
    │
    ▼ 重新评分 calc_fit_score()
    │
    ▼ 重新评级 determine_rating()
    │
    ▼ 输出 { before, after, changes }
`

### 9.2 首发确认机制

- 确认首发 → 常规流程
- 核心缺阵 → 固定扣分影响
- 未确认 → 保持原始数据

---

## 十、方案推荐引擎 (plan_engine.py)

### 10.1 过滤规则

| 条件 | 动作 |
|------|------|
| fit_score < 6.0 | 排除该比赛 |
| meltdown = true | 排除该比赛 |
| 评级 = C | 排除该比赛 |

### 10.2 可选投注项

- 胜平负
- 让球胜平负
- 总进球（top2_total_goals）
- 比分（top3_scores）
- 半全场（top2_half_full）

### 10.3 推荐方案

| 方案 | 内容 |
|------|------|
| 2.0 单关 | 仅总进球 / 比分 / 半全场 |
| 2.0 2串1 | 跨比赛任意搭配 |
| 3.0 3串1 | 跨比赛任意搭配 |

---

## 十一、数据库结构 (framework.db)

### 11.1 runs 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| date | TEXT | 运行日期 |
| created_at | TEXT | 创建时间 |
| factor_params | TEXT | JSON 字符串 |
| run_type | TEXT | 'live' 或 'backtest' |
| prediction_date | TEXT | 预测日期 |
| total_matches | INTEGER | 比赛总数 |
| hit_count | INTEGER | 命中数 |
| avg_fit_score | REAL | 平均贴合度 |

### 11.2 matches 表（50+ 字段）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| run_id | INTEGER FK | 所属运行批次 |
| match_id | TEXT | 比赛编号 |
| home / away | TEXT | 主客队 |
| event / match_time | TEXT | 赛事名 / 时间 |
| match_type / league | TEXT | 类型 / 联赛 |
| asian_handicap / jc_handicap | REAL / INT | 盘口 |
| lambda_h_final / lambda_a_final / lambda_diff | REAL | λ 值 |
| physical_home_win / draw / away_win | REAL | 物理概率 |
| market_home_win / draw / away_win | REAL | 市场概率 |
| ddi_home_win / draw / away_win | REAL | DDI 偏差 |
| calibrated_home_win / draw / away_win | REAL | 校准后概率 |
| fit_score / rating / direction | REAL / TEXT / TEXT | 评分 / 评级 / 方向 |
| downgrade_count / meltdown | INT | 降级计数 / 熔断标志 |
| scenario_type | TEXT | 场景类型 |
| top2_total_goals / top2_half_full / top3_scores | TEXT | JSON 数组 |
| s7_score / s7_reason | REAL / TEXT | 环境扰动 |
| trap_analysis / key_risk | TEXT | 诱盘分析 / 风险 |
| actual_score / half_time_score | TEXT | 实际比分 |
| half_full | TEXT | 半全场 |
| hit | INT | 是否命中 |
| diagnosis | TEXT | 复盘诊断 |

---

## 十二、风控体系

### 12.1 熔断机制

当 it_score < FIT_SCORE_THRESHOLD_MELTDOWN (4.0) 时触发熔断：
- 评级设为 MELTDOWN / C
- 方案推荐引擎排除该比赛
- 前端展示红色熔断标记

### 12.2 环境扰动 (S7)

S7 分数反映赛场环境对预测可靠性的影响：

| S7 来源 | 典型值 | 影响 |
|---------|--------|------|
| 德比战 | 0.3 - 0.5 | 降 1 级 |
| 保级/争冠关键战 | 0.4 - 0.7 | 降 1 级 |
| 杯赛决赛 | 0.5 - 0.8 | 降 1 级 |
| 恶劣天气 | 0.2 - 0.4 | 轻微影响 |
| 球队内部动荡 | 0.3 - 0.6 | 降 1 级 |

### 12.3 诱盘分析

基于以下信号识别潜在诱盘：
- 物理概率与市场概率方向相反
- 赔率异常变动但基本面未变
- DDI 偏差超过阈值但方向不合理
- 市场热度与模型信号背离

---

## 十三、2026 世界杯专属模块

### 13.1 数据

- 48 场小组赛（6月12日 - 6月25日）
- 12 组 × 4 队
- 内置场地 / 时间 / 组别信息
- 竞彩赔率已同步到 wc_schedule.json

### 13.2 前端视图

| 视图 | 功能 | 状态 |
|------|------|------|
| 首页 | 倒计时（6月12日前）/ 当日赛事卡片（6月12日后）| ✅ |
| 小组赛程 | 日历 Grid，按日期分组，含场地/组别/时间 | ✅ |
| 积分榜 | 12组表格，分组翻页，排名彩色条 | ✅ |
| 淘汰赛 | 树状对阵图，SVG连线 | ✅ (demo) |
| 赔率 | — | ⬜ 待实现 |
| TOP | — | ⬜ 待实现 |

---

## 十四、API 参考

### 14.1 数据接口

| 端点 | 方法 | 说明 |
|------|------|------|
| /api/latest | GET | 今日比赛完整数据（5个JSON合并） |
| /api/analyze | POST | 提交因子参数运行全分析 |
| /api/review | POST | 提交复盘评分 |
| /api/reviews | GET | 获取最近50条复盘记录 |
| /api/live/info | GET | 临场信息（SP/方向/贴合度） |
| /api/live/recalibrate | POST | 临场 SP 重校 |
| /api/history/runs | GET | 历史运行统计 |
| /api/history/matches | GET | 按日期查历史比赛 |
| /api/plan/<level> | GET | 方案推荐（2.0 / 3.0） |
| /api/wc/schedule | GET | 世界杯赛程 + 赔率 |
| /api/doc/sections | GET | 文档章节 |

### 14.2 典型返回示例

`json
{
  "match_id": "206",
  "time": "2026-06-06 18:00",
  "home": "川崎前锋",
  "away": "广岛三箭",
  "direction": "让胜",
  "fit_score": 6.84,
  "rating": "B",
  "lambda_diff": 0.394,
  "ddi_home_win": 0.039,
  "top2_total_goals": ["3球", "4球"],
  "top2_half_full": ["胜胜", "平胜"],
  "top3_scores": ["1-0", "1-1", "0-1"]
}
`

---

## 十五、快速命令参考

`ash
# 启动服务
cd D:\V3.3.3-Core
python app.py

# 一键全流程（拉数据 + 分析）
python fetch_jczq.py && python auto_pipeline.py

# 智能生成因子 + AI 判断
python smart_factors.py

# 查看数据库
python -c "import database; database.init_db()"

# 回测
python backtest.py

# 构建世界杯数据
python build_wc_data.py
`

---

*文档结束 · V3.3.3-Core 分析系统 (Rev1.15)*
