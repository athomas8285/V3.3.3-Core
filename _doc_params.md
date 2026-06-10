# V3.3.3-Core 核心参数说明书

> 系统版本：Rev1.15（2026世界杯专属版）
> 基于 config.py · ddi.py · fit_score.py · rating.py · monte_carlo.py · lambda_calc.py
> 最后更新：2026-06-10
> 数据基础：2024-2026 解放者杯 280 场 + 各联赛历史数据

---

## 一、联赛平均 xGA（预期失球）参考值

config.py：LEAGUE_AVG_XGA

| 联赛 | xGA | 联赛 | xGA | 联赛 | xGA |
|------|-----|------|-----|------|-----|
| 英超 | 1.40 | 西甲 | 1.35 | 意甲 | 1.25 |
| 德甲 | 1.35 | 法甲 | 1.30 | 荷甲 | 1.45 |
| 巴甲 | 1.30 | 阿甲 | 1.25 | 墨超 | 1.30 |
| 美职联 | 1.45 | 日职 | 1.35 | 韩K | 1.25 |
| 澳超 | 1.50 | 葡超 | 1.25 | 苏超 | 1.35 |
| 瑞典超 | 1.40 | 挪超 | 1.45 | 比甲 | — |
| 智利甲 | 1.30 | 哥伦甲 | 1.30 | 秘鲁甲 | 1.35 |
| 厄瓜多尔甲 | 1.20 | 乌甲 | 1.15 | 巴拉圭甲 | 1.15 |
| 玻利维亚甲 | 1.20 | 委内瑞拉超 | 1.45 | 芬超 | 1.35 |
| 葡甲 | 1.30 | **默认** | **1.35** | — | — |

**用途**：λ 计算时分母，衡量"联赛基线失球水平"。强联赛（英超/德甲）xGA 较高反映整体进攻效率；防守型联赛（意甲/阿甲）xGA 较低。

---

## 二、跨联赛兑换系数

config.py：LEAGUE_EXCHANGE_RATE

基于 2024+2025+2026 解放者杯 280 场比赛的对战数据拟合，用于不同联赛球队相遇时的 λ 修正。

| 原始联赛 | 兑换系数（→巴甲基线） | 含义 |
|---------|---------------------|------|
| 巴甲 | 0.89 | 基线联赛（自身无需兑换） |
| 阿甲 | 0.94 | 接近巴甲水平 |
| 哥伦甲 | 0.97 | 略低于巴甲 |
| 乌甲 | 0.96 | 略低于巴甲 |
| 巴拉圭甲 | 1.01 | 接近巴甲 |
| 厄瓜多尔甲 | 1.02 | 接近巴甲 |
| 智利甲 | 1.05 | 略高于巴甲（高原/客场因素） |
| 委内瑞拉超 | 1.08 | 明显高于巴甲 |
| 秘鲁甲 | 1.09 | 明显高于巴甲 |
| 玻利维亚甲 | 1.14 | 最高（高原主场显著加成） |

**公式**：λ_adjusted = λ_raw × exchange_rate
**场景**：巴甲球队 vs 玻利维亚甲球队 → 巴甲 λ × 1.14

---

## 三、λ 估计算子

lambda_calc.py：calc_initial_lambda()

### 3.1 标准公式（有 xG 数据）

`
λ_h = (home_xg × away_xga) / league_avg_xga
λ_a = (away_xg × home_xga) / league_avg_xga
`

| 变量 | 含义 | 来源 |
|------|------|------|
| home_xg | 主队场均预期进球 | 联赛数据 / API |
| away_xga | 客队场均预期失球 | 联赛数据 / API |
| league_avg_xga | 联赛平均失球 | LEAGUE_AVG_XGA |

### 3.2 替代公式（无 xG 数据）

lambda_calc.py：calc_initial_lambda_alt()

`
λ_h = (home_goals × away_goals_conceded) / (league_avg_goals × league_avg_xga)
λ_a = (away_goals × home_goals_conceded) / (league_avg_goals × league_avg_xga)
`

### 3.3 λ_diff 阈值体系

pp.py （doc/sections 原始内容）

| 阈值 | 信号强度 | 含义 |
|------|---------|------|
| \|λ_diff\| < 0.15 | 弱信号 | 两队实力接近，方向判定依赖DDI |
| 0.15 ≤ \|λ_diff\| < 0.30 | 弱→中过渡 | 模型有轻微倾向 |
| 0.30 ≤ \|λ_diff\| < 0.50 | 中等信号 | 模型倾向可信 |
| \|λ_diff\| ≥ 0.50 | 强信号 | 触发风控提示（方向警告检查） |
| \|λ_diff\| > 1.0 | 极强信号 | 方向与 λ 不一致时触发方向警告降级 |

### 3.4 未来函数检测

lambda_calc.py：alidate_temporal_integrity()

检查 match_info 中的 xG/战绩数据是否混合了赛后才可知的信息。
触发条件：数据时间戳 > 比赛开赛时间 / 战绩场次包含赛后比赛
后果：降级数据置信度（data_confidence = 'post_match'），贴合度评分对应扣分。

---

## 四、因子修正参数

config.py + un_all.py：pply_factors()

### 4.1 伤停因子

| 参数 | 值 | 说明 |
|------|-----|------|
| INJURY_CORE_MAX | 0.20 | 核心球员伤停最大影响系数 |
| INJURY_ROTATION_MAX | 0.05 | 轮换球员伤停最大影响系数 |

**公式**：λ_final = λ × (1 + injury_core + injury_rotation + injury_boost)
**示例**：核心前锋缺阵 → injury_home = 0.15 → λ_h × 1.15

### 4.2 战意因子

config.py：MOTIVATION_CAP_PLAYOFF = 0.05 · MOTIVATION_CAP_REGULAR = 0.15

| 场景 | 战意值 | 硬上限 |
|------|--------|--------|
| 保级战（主队） | 0.08 - 0.12 | CAP_REGULAR = 0.15 |
| 争冠战（主队） | 0.10 - 0.15 | CAP_REGULAR = 0.15 |
| 杯赛决赛 | 0.03 - 0.05 | CAP_PLAYOFF = 0.05 |
| 已保级+无欲无求 | -0.05 - 0 | 无正向上限 |

**反转检测**：当战意方向与 λ_diff 方向相反且 |λ_diff| > 0.3 时，战意值减半。
**压力修正**：高压比赛（pressure=true）战意值再减半。

### 4.3 松懈惩罚

config.py：SLACK_PENALTY = 0.08

**公式**：λ_h ×= (1 - 0.08)（当 slack_home = true）
**场景**：已提前出线 / 已降级 / 大比分领先后的松懈

### 4.4 海拔加成

config.py：ALTITUDE_THRESHOLD = 2500 · ALTITUDE_BONUS = 0.15

| 海拔 | 加成 | 示例球队 |
|------|------|----------|
| < 2500m | 无 | 绝大多数球场 |
| 2500m - 3600m | +0.15 | 玻利维亚拉巴斯(3630m) |
| ≥ 3600m | +0.15（上限） | 秘鲁库斯科(3400m) |

**公式**：λ_h ×= (1 + 0.15) 当 altitude_home > 0

---

## 五、蒙特卡洛模拟参数

config.py + monte_carlo.py

| 参数 | 值 | 说明 |
|------|-----|------|
| MONTE_CARLO_RUNS | 2000 | 默认泊松抽样次数 |
| HALF_TIME_RATIO | 0.44 | 半场进球占全场比例（用于半全场预测） |
| 收敛校验 | Bootstrap 100次 | 计算 std_home |
| 收敛阈值 | std < 0.01 | 满足即视为收敛 |
| 最大抽样 | 10000 次 | 未收敛时逐步增加至上限 |
| 置信区间 | 95% | 输出 ci_home / ci_draw / ci_away |

### 5.1 输出项

| 输出 | 格式 | 说明 |
|------|------|------|
| physical | {home_win, draw, away_win} | 物理概率（无让球） |
| jc_handicap | {rang_sheng, rang_ping, rang_fu} | 竞彩让球胜平负概率 |
| convergence | {runs, std_home} | 收敛状态 |
| top2_total_goals | ["3球", "4球"] | 最可能的 2 个总进球数 |
| top2_half_full | ["胜胜", "平胜"] | 最可能的 2 个半全场结果 |
| top3_scores | ["1-0", "2-0", "1-1"] | 最可能的 3 个比分 |
| top3_scores_prob | [0.12, 0.08, 0.07] | 对应比分的概率 |

---

## 六、DDI 校准参数

config.py + ddi.py

### 6.1 市场概率计算

`
P(home) = (1/SP_home) / (1/SP_home + 1/SP_draw + 1/SP_away)
`

反 SP 归一化，去除庄家抽水，得到公平市场概率。

### 6.2 DDI 偏差

`
DDI = P(物理) - P(市场)
`

| DDI 符号 | 含义 |
|----------|------|
| DDI > 0 | 模型比市场更看好该结果 |
| DDI < 0 | 市场比模型更看好该结果 |
| DDI ≈ 0 | 模型与市场一致 |

### 6.3 校准参数表

config.py 完整 DDI 参数：

| 参数 | 值 | 说明 |
|------|-----|------|
| DDI_TRIGGER_THRESHOLD | 0.08 | \|DDI\| 超过此值才触发校准 |
| DDI_AMPLITUDE_RATIO | 0.3 | 校准幅度 = \|DDI\| × 0.3 |
| DDI_AMPLITUDE_CAP | 0.05 | 单次校准幅度上限 |
| AWAY_COLD_TREATMENT | 0.08 | 附加赛/末轮客胜减少 8% |
| VBAL_DEFAULT | 0.15 | 资金流偏差默认值（Rev1.13修复DDI归零） |
| DDI_MISCALIBRATION_THRESHOLD | 0.005 | 误校准检测阈值 |
| D_KELLY_DEFAULT | 0.05 | Kelly 凯利默认比例 |

### 6.4 校准示例

| 场景 | DDI | 是否触发 | 校准幅度 | 校准后概率 |
|------|-----|---------|---------|-----------|
| 模型看好主胜 | +0.12 | ✅ > 0.08 | min(0.12×0.3, 0.05) = 0.036 | P_home + 0.036 |
| 市场过热主胜 | -0.15 | ✅ > 0.08 | min(0.15×0.3, 0.05) = 0.045 | P_home - 0.045 |
| 微弱偏差 | +0.03 | ❌ ≤ 0.08 | 不校准 | 保持原值 |

### 6.5 赔率动量修正

ddi.py：pply_odds_momentum_correction()

基于初始 SP 到当前 SP 的变化趋势：
- 初始 SP_home = 2.00 → 当前 SP_home = 1.85（下降 7.5%）→ 主胜概率上调
- 初始 SP_away = 3.50 → 当前 SP_away = 4.00（上升 14.3%）→ 客胜概率下调

---

## 七、贴合度评分参数

config.py + it_score.py

### 7.1 7维度满分与权重

| 维度 | 函数 | 满分 | 权重说明 |
|------|------|------|----------|
| 1. 数据完整度 | score_data_confidence | 1.5 | API数据/计算数据/推断数据三级 |
| 2. 伤停确定度 | score_injury_reliability | 1.0 | 确切伤停 vs 无数据 |
| 3. 战意清晰度 | score_motivation_clarity | 1.5 | 战意明确度 |
| 4. 盘口偏离合理性 | score_handicap_deviation | 2.5 | λ偏差 + 盘口深度 |
| 5. 临场异动匹配度 | score_movement_match | 0.5 | 盘口变化趋势 |
| 6. 物理市场一致性 | score_path_consistency | 0.5 | 物理vs市场方向 |
| 7. 赛事适配度 | score_event_adaptability | 0.5 | 联赛/杯赛类型 |

**原始满分**：11 分（1.5+1.0+1.5+2.5+0.5+0.5+0.5+各分量）
**归一化**：inal = (raw_total - s7_penalty) × opp_coef × NORMALIZE（NORMALIZE = 10/11）

### 7.2 阈值体系

| 参数 | 值 | 说明 |
|------|-----|------|
| FIT_SCORE_THRESHOLD_MELTDOWN | 4.0 | 熔断阈值（低于此值评级自动 C） |
| FIT_SCORE_THRESHOLD_BACKUP | 6.0 | 备份阈值（低于此值触发风险提示） |
| OPPONENT_PREDICTABILITY_MIN | 0.90 | 对手可预测性系数下限 |

### 7.3 贴合度等级

| final_total | 等级 | 含义 |
|------------|------|------|
| ≥ 8.0 | 高贴合 | 模型信号强烈，数据完整 |
| ≥ 6.0 | 中等贴合 | 模型信号可用，需关注风险 |
| ≥ 4.0 | 低贴合 | 谨慎参考，可能存在未知因素 |
| < 4.0 | 熔断 | 数据不足或冲突，不建议采纳 |

### 7.4 否决规则

| 条件 | 扣分比例 | 说明 |
|------|---------|------|
| s7_penalty | 最大 1.0+ | S7心理扰动直接扣减 |
| opp_coef < 1.0 | 最大 -10% | 对手不可预测性扣分 |
| 伤停不明确 (s2 < 0.5) | ×0.9 | 伤停信息缺失 |
| 战意不明确 (s3 < 0.5) | ×0.9 | 战意信息缺失 |
| 赛事不匹配 (s7 < 0.3) | ×0.8 | 非典型赛事类型 |
| 附加赛/末轮 | s7_penalty ≥ 0.5 | 强制增加扰动扣分 |

---

## 八、评级参数

config.py + ating.py

### 8.1 评级标准

| 等级 | fit_score 要求 | 附加条件 | 含义 |
|------|---------------|---------|------|
| S | ≥ 8.0 | + 稳定信号 + 无方向警告 | 强烈推荐，最高置信度 |
| A | ≥ 6.0 | + 无降级因素（downgrade_count = 0） | 推荐，高置信度 |
| B | ≥ 4.0 | 或存在降级因素（downgrade_count ≥ 1） | 谨慎参考 |
| C | < 4.0 | 或熔断（meltdown = true） | 不推荐 |

### 8.2 风控降级参数

config.py：DEEP_HANDICAP_THRESHOLD = 2.0 · MID_HANDICAP_MIN = 1.0 · MID_HANDICAP_MAX = 1.25 · MID_HANDICAP_LAMBDA_DIFF = 0.5

| 触发条件 | 降级幅度 | 说明 |
|----------|---------|------|
| S7 ≥ 0.5 | -1 级 | 环境扰动（德比/保级/决赛） |
| λ_diff > 0.5 且让球 > 2.0 | deep_discount | 大深盘 + 实力差过大 |
| 数据置信度 = post_match | -1 级 | 数据来自赛后（不可用于实盘） |
| 盘口 1.0 - 1.25 中线偏差 | -1 到 -2 级 | 平半/半球盘口偏差 |
| 缺少 xG | -1 级 | 使用替代公式（降级） |
| 伤停信息来源不可靠 | -1 级 | 无确切伤停数据 |

### 8.3 方向参数

ating.py：determine_direction()

| 条件 | 判定规则 |
|------|---------|
| λ_diff < 0.2 | 检查市场是否认同平局（SP_draw < 3.20） |
| 不认同时 | 30% 平局概率重新分配给胜负 |
| 让球概率 > 非让球最大概率 | 选择让球方向 |
| 非让球最大概率 < 0.40 | 强制"平" |
| λ_diff > 1.0 且方向与 λ 相反 | 触发方向警告 |

---

## 九、赔率阈值

pp.py （原始 doc/sections 内容）

| 主胜赔率范围 | 分类 | DDI 校准影响 |
|-------------|------|-------------|
| < 1.80 | 超热门 | 校准幅度减半，防止过度反应 |
| 1.80 - 2.49 | 热门区间 | 正常 DDI 校准 |
| 2.50 - 3.50 | 中等赔率 | 正常 DDI 校准 |
| 3.50 - 5.00 | 冷门区间 | 校准幅度 × 1.2，倾向捕捉冷门 |
| > 5.00 | 超冷门 | 冻结校准（DDI 信号不可靠） |

---

## 十、数据库字段参数

### 10.1 runs 表

| 字段 | 类型 | 取值范围 |
|------|------|----------|
| run_type | TEXT | 'live'（实盘） / 'backtest'（回测） |
| total_matches | INTEGER | 1 - 50（单批次比赛数） |
| hit_count | INTEGER | 0 - total_matches（命中数） |
| avg_fit_score | REAL | 0.0 - 10.0（平均贴合度） |

### 10.2 matches 表关键字段

| 字段 | 类型 | 取值范围 |
|------|------|----------|
| lambda_diff | REAL | -3.0 - 3.0（λ差值） |
| ddi_home_win | REAL | -0.5 - 0.5（DDI偏差） |
| fit_score | REAL | 0.0 - 10.0（贴合度） |
| rating | TEXT | 'S' / 'A' / 'B' / 'C' / 'MELTDOWN' |
| downgrade_count | INTEGER | 0 - 5（降级次数） |
| meltdown | INTEGER | 0 / 1（是否熔断） |
| hit | INTEGER | 0 / 1（是否命中） |
| s7_score | REAL | 0.0 - 1.5（环境扰动） |

---

## 十一、参数速查表

| 参数 | 文件 | 值 |
|------|------|-----|
| MONTE_CARLO_RUNS | config.py | 2000 |
| HALF_TIME_RATIO | config.py | 0.44 |
| DDI_TRIGGER_THRESHOLD | config.py | 0.08 |
| DDI_AMPLITUDE_CAP | config.py | 0.05 |
| DDI_AMPLITUDE_RATIO | config.py | 0.3 |
| AWAY_COLD_TREATMENT | config.py | 0.08 |
| VBAL_DEFAULT | config.py | 0.15 |
| MOTIVATION_CAP_PLAYOFF | config.py | 0.05 |
| MOTIVATION_CAP_REGULAR | config.py | 0.15 |
| INJURY_CORE_MAX | config.py | 0.20 |
| INJURY_ROTATION_MAX | config.py | 0.05 |
| SLACK_PENALTY | config.py | 0.08 |
| ALTITUDE_BONUS | config.py | 0.15 |
| ALTITUDE_THRESHOLD | config.py | 2500 m |
| FIT_SCORE_THRESHOLD_MELTDOWN | config.py | 4.0 |
| FIT_SCORE_THRESHOLD_BACKUP | config.py | 6.0 |
| OPPONENT_PREDICTABILITY_MIN | config.py | 0.90 |
| DEEP_HANDICAP_THRESHOLD | config.py | 2.0 |
| MID_HANDICAP_MIN | config.py | 1.0 |
| MID_HANDICAP_MAX | config.py | 1.25 |
| MID_HANDICAP_LAMBDA_DIFF | config.py | 0.5 |
| D_KELLY_DEFAULT | config.py | 0.05 |
| DDI_MISCALIBRATION_THRESHOLD | config.py | 0.005 |
| 联赛默认 xGA | config.py | 1.35 |
| NORMALIZE（满分归一化） | fit_score.py | 10/11 |
| 收敛阈值 std | monte_carlo.py | 0.01 |
| 95% 置信区间 | monte_carlo.py | ci95% |
| 收敛校验次数 | monte_carlo.py | 100 (Bootstrap) |
| 最大抽样次数 | monte_carlo.py | 10000 |

---

*文档结束 · V3.3.3-Core 核心参数说明书 (Rev1.15)*
