# V3.3.3-Core Project Complete Handoff
> 新窗口第一句话：读 D:\V3.3.3-Core\WORLD_CUP_HANDOFF.md
> 项目路径: D:\V3.3.3-Core
> Python 3 + Flask + SQLite + Vanilla JS 单页架构
> 最后活跃: 2026-06-10
> 系统定位: 足球赛事量化分析系统（竞彩/亚盘方向预测），含2026世界杯专属模块

---
## 一、启动方式

```bash
cd D:\V3.3.3-Core
python app.py
# 浏览器打开 http://localhost:5000
```

Flask 开发服务器，默认 127.0.0.1:5000，debug=True。

---
## 二、项目目录结构

```
D:\V3.3.3-Core\
├── app.py                         # Flask 服务器（26+ 路由）
├── config.py                      # 全局参数（联赛xGA、兑换系数、MC参数、DDI参数等）
├── database.py                    # SQLite ORM层（framework.db）
├── framework.db                   # SQLite 数据库（runs + matches 表）
├── auto_pipeline.py               # 一键全流程入口（Rev1.15）
├── run_all.py                     # 核心分析管道（lambda → MC → 结果输出）
├── smart_factors.py               # AI因子参数 + AI判断智能生成器
│
├── lambda_calc.py                 # Step 3: λ物理参数计算 + 未来函数检测
├── monte_carlo.py                 # Step 6: 泊松蒙特卡洛模拟（收敛验证版）
├── ddi.py                         # Step 7: DDI校准（纯偏差公式）
├── fit_score.py                   # Step 8: 贴合度评分（7维度）
├── rating.py                      # Step 9: 评级判定（S/A/B/C + 方向）
├── review.py                      # 复盘模块
├── plan_engine.py                 # 方案推荐（单关/串关策略引擎）
├── live_ddi.py                    # 临场SP重校引擎
├── backtest.py                    # 回测模块
│
├── parser.py                      # 原始文本解析
├── factors.py                     # 因子计算
├── fetch_jczq.py                  # 竞彩网数据采集（API）
├── fetch_form.py                  # SofaScore 近期战绩采集（Playwright）
├── enrich_odds.py                 # 竞彩网赔率同步到 match_info/locked_data
├── build_wc_data.py               # 世界杯赛程数据构建脚本
├── lambda_calc.py                 # λ值计算（含联赛跨兑换）
│
├── templates/
│   ├── index.html                 # ★ 主页面（单页应用，全部前端逻辑在此）
│   ├── charts.js                  # ★ 今日扫盘渲染引擎（卡片表格 + SVG图表）
│   ├── live.js                    # ★ 临场面板交互脚本
│   ├── plan.html                  # 方案推荐页面
│   ├── v1.html ~ v5.html          # 历史版本页面（迭代对照）
│   ├── debug.html / test.html     # 调试页面
│   └── 大量测试/备份HTML文件        # 可忽略
│
├── data/
│   ├── input/                     # 输入数据
│   ├── output/                    # 每次 pipeline 输出（按 run_id）
│   ├── processed/                 # 已处理的输入档案（用于回测）
│   ├── archive/                   # 归档
│   ├── locked_data.json           # ★ 核心输入：锁定比赛数据
│   ├── factor_params.json         # ★ 因子参数
│   ├── match_info.json            # ★ 标准化比赛信息
│   ├── monte_carlo_result.json    # ★ MC模拟结果
│   ├── ddi_result.json            # ★ DDI资金流偏差
│   ├── fit_score_result.json      # ★ 贴合度评分
│   ├── rating_result.json         # ★ 评级和方向
│   ├── ai_judgment.json           # ★ AI综合判断（S7/诱盘/风险）
│   ├── wc_schedule.json           # ★ 世界杯赛程+赔率数据
│   ├── raw_jczq.json              # 竞彩网原始API数据
│   └── all_results_detailed.json  # 详细历史结果汇总
│
├── static/
│   ├── bg1.png / bg2.png          # 背景图
│   └── flags/                     # 国家队国旗图片
│
├── versions_backup/               # v1/v2/v3 HTML备份
├── work/                          # 调试脚本
└── _template/                     # 可复用Web模板（独立app + data/templates）
```

---
## 三、页面框架（CSS架构 + 组件）

### 3.1 CSS 变量体系

页面深色主题，在 `:root` 中定义，所有组件引用变量：

```css
--bg: #080b14;              /* 最底层背景 */
--surface: #0c1021;         /* 卡片/面板表面 */
--surface-2: #111629;       /* 次级表面 */
--surface-h: #171d35;       /* hover状态 */
--t1: #e8edf5;              /* 主要文字 */
--t2: #8b95a9;              /* 次要文字 */
--t3: #5a6577;              /* 辅助文字 */
--green: #00e676;           /* 命中/在线 */
--red: #ef5350;             /* 错误/风险 */
--gold: #fbbf24;            /* 世界杯主题色/高亮 */
--cyan: #00e5ff;            /* 主色调（系统/科技感） */
--blue: #60a5fa;
--purple: #7c3aed;
--bd: rgba(0,229,255,.06);  /* 边框 */
--bd-h: rgba(0,229,255,.14);/* hover边框 */
--mono: "SF Mono","Cascadia Code","Consolas",monospace;
--sans: "Inter","SF Pro","Microsoft YaHei","PingFang SC",sans-serif;
```

body 使用全屏布局：`overflow:hidden; display:flex;`，背景图 `bg1.png`。

### 3.2 布局结构

```
┌─────────────────────────────────────────────────┐
│ .sd-wrap (250px)  │  .main (flex:1, overflow-y)  │
│   ┌─────────────┐  │  ┌─── view-content ───────┐  │
│   │ .sd-top     │  │  │ homeContent             │  │
│   │  logo+status│  │  │ scheduleContent (默认)   │  │
│   ├─────────────┤  │  │ standingsContent         │  │
│   │ .sd-body    │  │  │ bracketContent           │  │
│   │  nav        │  │  │ oddsContent              │  │
│   │  accordion  │  │  │ topContent              │  │
│   │  wc-sub     │  │  └─────────────────────────┘  │
│   ├─────────────┤  │                               │
│   │ .sd-footer  │  │                               │
│   └─────────────┘  │                               │
└─────────────────────────────────────────────────┘
```

侧边栏固定 250px，内容区自适应，滚动条极细风格。

### 3.3 核心组件

**侧边栏导航 (`.sd-nav-item` 类):**
- `data-nav` 属性映射视图（home/schedule/standings/bracket/odds/top）
- `.active` 高亮（左侧 3px cyan 边框）
- 折叠面板组件 `.acc`（含 acc-head + acc-body，通过 max-height 过渡动画）

**世界杯专属导航 (`.wc-sub-item` 类):**
- 金色主题（gold/amber）
- data-nav 映射同侧边栏

**视图切换系统:**
- `switchNav(nav)` 函数：切换 `.view-content` 显示/隐藏
- 每个视图一个 div，id = {nav}Content，class = "view-content"
- 默认加载后调用 switchNav('home')

### 3.4 页面视图

当前有 6 个视图（全部在 index.html 内，JS 渲染）：

| 视图 | 导航名 | 渲染函数 | 说明 |
|------|--------|----------|------|
| 系统首页 | home | renderHomePage() | 世界杯倒计时（6月12日前）/ 当日赛事（6月12日后）|
| 小组赛程 | schedule | renderCalendarView() | 按日期分组显示，含球场、组别、时间 |
| 积分榜 | standings | renderStandings() | 12组硬编码 demo 数据，表格显示 |
| 淘汰赛 | bracket | renderBracket() | 树状淘汰赛图，硬编码 demo 数据 |
| 赔率 | odds | — | 占位页面 |
| TOP | top | — | 占位页面 |

**首页组件 (hcc-)：**
- `hcc-container`：全屏居中容器，radial-gradient 背景
- `hcc-glow-orb`：浮动光晕（cyan + gold）
- `hcc-radar-sweep`：雷达扫描动画
- `hcc-grid-lines`：网格线背景
- `hcc-corner-bracket`：四角装饰
- `hcc-sysbar`：系统状态栏（SYS/TGT/VEN）
- `hcc-countdown`：倒计时（days/hours/min/sec），每秒更新
- `hcc-match-card`：揭幕战卡片（渐变边框，hover 发光）
- `hcc-particles`：Canvas粒子动画（80个粒子，上升+发光）

**今日赛事卡片 (home视图，6月12日后):**
- `.ht-card` 卡片布局，含时间、组别、球队（带国旗）、球场

**世界杯赛程视图 (`.wc-` 组件):**
- `.wc-date-group`：日期分组
- `.wc-match-card`：单场赛程卡片
- `.wc-m-time / .wc-m-group / .wc-m-home / .wc-m-away / .wc-m-venue`

**积分榜 (`.st-` 组件):**
- `.st-table`：12组表格，rank/team/mp/w/d/l/gf/ga/gd/pts
- `.st-rank-bar`：排名彩色条（top2 绿，bottom2 红）

**淘汰赛 (`.br-` 组件):**
- `.br-wrap`：flex 列布局，4轮（1/8 → 1/4 → 半决 → 决赛）
- `.br-card`：球队卡片，tbd 占位

---
## 四、所有 API 接口

### 4.1 页面路由

| 路由 | 函数 | 说明 |
|------|------|------|
| `/` | index() | 主页面，注入 __DATA (5个JSON合并) |
| `/test` | test_page | test.html |
| `/debug` | debug_page | debug.html |
| `/full_test` | full_test | full_test.html |
| `/v1` ~ `/v5` | v1~v5 | 版本迭代对照页 |
| `/v1_old` ~ `/v3_old` | v1~v3_old | versions_backup 历史版 |
| `/plan/<level>` | plan_page | 2.0/3.0方案页 |
| `/bak` | index_bak | index.html.bak |
| `/v4_backup` / `/v4_clean` | backup | 备份版 |

### 4.2 JSON API

| 路由 | 方法 | 说明 | 关键返回字段 |
|------|------|------|-------------|
| `/api/latest` | GET | 今日比赛完整数据 | 5个JSON合并，match_id/time/home/away/event/direction/fit_score/rating/lambda_diff/ddi_home_win/top2_* |
| `/api/parse` | POST | 解析原始文本 | 返回 match_info 格式 |
| `/api/analyze` | POST | 提交 factor_params 运行全分析 | factor_params写入→run_all.py→返回 rating/mc/info/ddi/ai |
| `/api/review` | POST | 提交复盘评分 | 写入 review.json→run review.py→返回 reviews+stats |
| `/api/reviews` | GET | 获取复盘记录（最近50条） | 包含历史预测数据（lambda_diff/ddi/fit_score/top3_scores等） |
| `/api/live/info` | GET | 临场信息 | 每场的SP/方向/贴合度，含 initial_sp_* |
| `/api/live/recalibrate` | POST | 临场SP重校 | 输入 mid/sp_home/sp_draw/sp_away，返回新ddi/fit_score/rating |
| `/api/history/runs` | GET | 历史运行统计 | prediction_date/total_matches/hit_count |
| `/api/history/matches` | GET | 按日期查历史比赛 | ?date=2026-06-05，返回该日所有比赛详情 |
| `/api/v2/data` | GET | V2兼容数据 | prediction_date/today_scan/rating/mc/info/ddi/ai |
| `/api/backtest/runs` | GET | 回测数据（demo） | 硬编码样例数据 |
| `/api/doc/sections` | GET | 文档章节（demo） | 硬编码参数说明+架构说明 |
| `/api/plan/<level>` | GET | 方案推荐 | level=2.0 或 3.0，返回 singles/combos_2/combos_3 |
| `/api/wc/schedule` | GET | 世界杯赛程+赔率 | 从 wc_schedule.json 加载 |

### 4.3 JS 服务路由

| 路由 | 文件 | 说明 |
|------|------|------|
| `/charts.js` | templates/charts.js | 扫盘渲染引擎 |
| `/live.js` | templates/live.js | 临场面板交互脚本 |

### 4.4 API 响应示例

**`GET /api/latest` 返回格式:**
```json
[{
  "match_id": "206",
  "time": "2026-06-06 18:00",
  "home": "川崎前锋",
  "away": "广岛三箭",
  "event": "日本职业联赛",
  "direction": "让胜",
  "fit_score": 6.84,
  "rating": "B",
  "lambda_diff": 0.394,
  "ddi_home_win": 0.039,
  "top2_total_goals": ["3球","4球"],
  "top2_half_full": ["胜胜","平胜"],
  "top3_scores": ["1-0","1-1","0-1"]
}]
```

**`GET /api/history/matches?date=2026-06-05`:**
```json
{"matches": [
  {"match_id": "206", "home": "川崎前锋", "away": "广岛三箭",
   "direction": "让胜", "fit_score": 6.84, "rating": "B",
   "actual_score": "2-1", "hit": true, "lambda_diff": 0.394,
   "ddi_home_win": 0.039, "scenario_type": "低返还率赛事",
   "top2_total_goals": "[\"3球\",\"4球\"]"}
]}
```

### 4.5 关键注意点
- 首页 `/` 通过注入 `<script>var __DATA=...</script>` 传递数据，不依赖 AJAX 加载
- `/api/analyze` 会调用 subprocess 运行 run_all.py，超时120秒
- 所有 JSON API 返回已通过 `@app.after_request` 设置 no-cache 头
- `/api/live/recalibrate` 是临场核心接口，实时重新计算 DDI/贴合度/评级

---
## 五、数据库结构 (framework.db)

表名: **runs**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| date | TEXT NOT NULL | 运行日期 |
| created_at | TEXT | 创建时间 |
| factor_params | TEXT | JSON字符串 |
| run_type | TEXT | 'live' 或 'backtest' |
| total_matches | INTEGER | 比赛总数 |
| hit_count | INTEGER | 命中数 |
| avg_fit_score | REAL | 平均贴合度 |

表名: **matches**（50+字段）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| run_id | INTEGER FK→runs | 所属运行批次 |
| match_id | TEXT | 比赛编号（如"206"） |
| home / away | TEXT | 主客队 |
| event / match_time | TEXT | 赛事名/时间 |
| match_type / league | TEXT | 类型/联赛 |
| asian_handicap / jc_handicap | REAL/INT | 盘口 |
| lambda_h_final / lambda_a_final / lambda_diff | REAL | λ值 |
| physical_home_win / draw / away_win | REAL | 物理概率 |
| market_home_win / draw / away_win | REAL | 市场概率 |
| ddi_home_win / draw / away_win | REAL | DDI偏差 |
| calibrated_home_win / draw / away_win | REAL | 校准后概率 |
| fit_score / rating / direction | REAL/TEXT/TEXT | 评分/评级/方向 |
| downgrade_count / meltdown | INT | 降级计数/熔断 |
| scenario_type | TEXT | 场景类型 |
| top2_total_goals / top2_half_full / top3_scores | TEXT | JSON数组 |
| s7_score / s7_reason | REAL/TEXT | 环境扰动 |
| trap_analysis / key_risk | TEXT | 诱盘分析/风险 |
| actual_score / half_time_score | TEXT | 实际比分 |
| half_full | TEXT | 半全场 |
| hit | INT | 是否命中 |
| diagnosis | TEXT | 复盘诊断 |

索引: idx_matches_run_id, idx_matches_match_id

**数据库初始化:**
```python
from database import init_db
init_db()  # 自动创建表
```

**数据库操作函数:**
```python
database.insert_run(date, factor_params, run_type, prediction_date) → run_id
database.insert_match(run_id, match_dict) → match_id
database.update_result(match_id, run_id, actual_score, half_time_score, half_full, hit, diagnosis)
database.get_reviews(limit=50) → list of dicts
database.get_latest_run() → (run_dict, matches_list)
```

---
## 六、数据采集流程

### 6.1 数据源

| 来源 | 文件 | 方式 | 数据 |
|------|------|------|------|
| 中国竞彩网 | fetch_jczq.py | HTTP API | 比赛列表+SP赔率+让球盘 |
| SofaScore | fetch_form.py | Playwright | 近期战绩+阵容+伤停 |
| HKJC | fetch_jczq（间接） | API | 亚洲盘口参考 |

### 6.2 数据采集入口

**步骤1：获取竞彩网数据**
```bash
python fetch_jczq.py
# → data/raw_jczq.json（原始API数据）
```

**步骤2：解析生成 locked_data**
```bash
python parser.py  # 或通过 POST /api/parse
# → data/locked_data.json（标准化比赛数据）
```

**步骤3：一键全流程**
```bash
python auto_pipeline.py
# 内部流程：
#   [1/5] 读取 locked_data.json
#   [2/5] 生成 match_info.json
#   [3/5] 检查/生成 factor_params.json（可--factor-json指定）
#   [4/5] 检查/生成 ai_judgment.json
#   [5/5] 运行 run_all.py 全流程分析
#   [6/7] 获取竞彩网实时赔率 → raw_jczq.json
#   [7/7] 同步赔率到 match_info/locked_data
```

**新增：智能因子生成**
```bash
python smart_factors.py
# 从 locked_data 自动生成 factor_params.json + ai_judgment.json
# 含球队档次知识库、伤停推理、战意判断
```

### 6.3 世界杯数据

```bash
python build_wc_data.py
# → data/wc_schedule.json（包含48场小组赛+赔率）
```

数据已内置所有48场小组赛（6月12日-6月25日，12组每组4队），结构：
```json
{"matches": [
  {"home": "墨西哥", "away": "南非", "group": "A",
   "round": 1, "date": "6月12日", "time": "03:00",
   "venue": "墨西哥城", "odds": {...}}
]}
```

---
## 七、分析引擎核心函数

### 7.1 管道顺序 (run_all.py)

```
locked_data.json
    ↓ lambda_calc.calc_initial_lambda()  → λ原始值
    ↓ run_all.apply_factors()            → λ最终值（含伤停/战意/海拔修正）
    ↓ monte_carlo.MonteCarloEngine.run() → 物理概率+竞彩盘口概率+TOP3比分
    ↓ ddi.py 计算链                     → DDI偏差+校准概率
    ↓ fit_score.py 评分                  → 贴合度（7维度，满分11→归一化10）
    ↓ rating.py 评级                     → 方向+评级S/A/B/C
    ↓ 输出至 data/*.json
```

### 7.2 λ计算 (lambda_calc.py)

```python
calc_initial_lambda(home_xg, home_xga, away_xg, away_xga, home_league, away_league)
# λ_h = home_xg * away_xga / league_avg_xga
# λ_a = away_xg * home_xga / league_avg_xga
# 跨联赛时使用 LEAGUE_EXCHANGE_RATE 修正

calc_initial_lambda_alt(home_goals, home_goals_conceded, away_goals, ...)
# 无xG时的替代计算（使用实际进球）

validate_temporal_integrity(match)  # 未来函数检测
```

config.py 中 LEAGUE_AVG_XGA 定义了所有联赛的参考失球值（英超1.40，巴甲1.30等）。

### 7.3 因子修正 (run_all.apply_factors)

```python
apply_factors(lambda_h, lambda_a, factor_params)
# 依次应用：
#   1. 伤停修正 (injury_home * lambda)
#   2. 伤停Boost (injury_home_boost)
#   3. 战意修正 (motivation_home/away)，含反转检测
#   4. 压力修正 (pressure)，战意值减半
#   5. 松懈惩罚 (slack → SLACK_PENALTY=0.08)
#   6. 海拔加成 (altitude > 2500m → ALTITUDE_BONUS=0.15)
```

factor_params.json 每场比赛格式:
```json
{
  "id": "206",
  "home": "川崎前锋",
  "injury_home": 0, "injury_away": 0,
  "injury_home_boost": 0, "injury_away_boost": 0,
  "motivation_home": 0, "motivation_away": 0,
  "pressure_home": false, "pressure_away": false,
  "slack_home": false, "slack_away": false,
  "altitude_home": 0, "altitude_away": 0
}
```

### 7.4 蒙特卡洛模拟 (monte_carlo.py)

```python
engine = MonteCarloEngine(lambda_h, lambda_a, jc_handicap, runs=2000)
result = engine.run()
# 返回:
#   physical: {home_win, draw, away_win}
#   jc_handicap: {rang_sheng, rang_ping, rang_fu}
#   convergence: {runs, std_home}
#   ci_home/ci_draw/ci_away：95%置信区间
#   top2_total_goals: ["3球","4球"]
#   top2_half_full: ["胜胜","平胜"]
#   top3_scores: ["1-0", "2-0", "1-1"]
#   top3_scores_prob: [0.12, 0.08, 0.07]
```

收敛验证：Bootstrap 抽样100次，std < 0.01 即收敛，否则逐步增加至最多10000次。

### 7.5 DDI校准 (ddi.py)

```python
calc_market_prob(sp_home, sp_draw, sp_away)
# → {home_win, draw, away_win}（反SP归一化）

calc_ddi(p_physical, p_market)
# DDI = P_physical - P_market（纯偏差，已修复原始公式中的乘数压死bug）

apply_calibration(p_physical, ddi)
# |DDI| > 0.08 触发，校正幅度 = |DDI| * 0.3，上限 0.05

apply_away_cold_treatment(calibrated, ...)
# 附加赛/解放者杯末轮的客胜冷处理（减少8%概率权重）

apply_odds_momentum_correction(p_physical, match_data)
# 赔率动态修正：基于初始SP→当前SP的变化方向
```

### 7.6 贴合度评分 (fit_score.py)

7维度评分（满分11→归一化到10分）：
1. 数据置信度 (1.5) - API/calc/infer 三级
2. 样本量惩罚 (P1)
3. 跨赛事惩罚 (P2)
4. 伤病可靠性 (1.0)
5. 动机清晰度 (1.5)
6. 盘口偏差 (2.5)
7. 赛事适应性 (0.5)

否决规则（apply_veto_rules）：
- 熔断阈值: FIT_SCORE_THRESHOLD_MELTDOWN = 4.0
- BACKUP阈值: FIT_SCORE_THRESHOLD_BACKUP = 6.0

### 7.7 评级系统 (rating.py)

```python
determine_direction(match) → "胜"/"平"/"负"/"让胜"/"让平"/"让负"
classify_scenario(fit_score, ...) → "低返还率赛事" / "中等置信度" / "高风险低置信"
determine_rating(fit_score, downgrade_count, meltdown, direction_warning)
  # S: fit >= 8.0 + 稳定信号 + 无警告
  # A: fit >= 6.0 + 无降级
  # B: fit >= 4.0 或存在风险降级
  # C: fit < 4.0 或熔断
get_rating_label(rating, fit_score) → "S"/"A"/"B"/"C"
```

降级逻辑（check_wind_control）：
- S7 ≥ 0.5 降1级
- lambda_diff > 0.5 且让球＞2 deep_discount
- 数据置信度中位降1级
- 盘口中线偏差降1-2级
- 缺少xG/伤停源头不可靠各降1级
- 积分排名因素（保级vs争冠）

### 7.8 临场重校 (live_ddi.py)

```python
load_current() → dict of all 6 data files
recalibrate(mid, new_sp_home, new_sp_draw, new_sp_away,
            starting_lineup_confirmed=None, data=None)
# 输入新的SP→重新计算market_prob→calc_ddi→apply_calibration
# → calc_fit_score→determine_rating
# 返回 {before, after, changes}
```

### 7.9 方案推荐 (plan_engine.py)

```python
load_today_data() → info_map, mc_map, rating_map
generate_all_options(info_map, mc_map, rating_map)
  # 生成所有可选投注项（胜平负/让球/总进球/比分/半全场）
  # fit_score < 6.0 或 meltdown 跳过
recommend_plan(options, min_odds, max_odds)
  # 单关：仅总进球/比分/半全场
  # 2串1：跨比赛任意搭配
  # 3串1：同上
```

---
## 八、前端渲染引擎

### 8.1 数据流

```
Flask 首页注入 → var __DATA = {rating, mc, info, ddi, ai}
                                      ↓
                            charts.js: rs(__DATA)
                                      ↓
                        buildSummary → 统计条 + 评级条形图
                        rs() 主渲染  → 比赛卡片表格
                        buildCharts  → SVG λ对比柱状图 + 概率对比图
                        renderReview → 复盘表
```

### 8.2 charts.js 核心函数

| 函数 | 行号 | 功能 |
|------|------|------|
| rs(d) | 196 | 主渲染入口：排序/过滤→构建卡片HTML |
| buildSummary(d) | 54 | 顶部统计条（场次/平均分/评级分布/条形图）|
| buildCharts(card, mid) | 71 | SVG图表：λ柱状图 + 物理vs市场概率对比 |
| renderReview() | 262 | 复盘渲染（昨日扫盘统计+命中率）|
| toggleFilter() | 27 | 筛选面板开关 |
| setFilter(type, val) | 32 | 评级/赛事筛选 |
| dirTag(d) | 14 | 方向标签（主胜/客胜）|
| badge(r, f) | 6 | 评级徽章（S/A/B/C）|
| loadReviews() | 2 | 加载复盘数据 |

全局变量:
- `_DATA`: 当前数据（__DATA的替代，rs()设置后统一使用）
- `RV`: 复盘历史数据
- `SORT_BY`: 排序方式 ("id" 或 "fit")
- `FILTER`: 筛选状态（评级+赛事）
- `FILTER_ALL_EVENTS`: 全部赛事标志

### 8.3 live.js

临场面板交互（鼠标悬停显示实时SP编辑和重校）：
- `loadLiveInfo()`：加载 `/api/live/info` 渲染SP编辑面板
- `doLiveRecalibrate(mid)`：调用 `/api/live/recalibrate` 单场重校
- `doBatchRecalibrate()`：批量重校所有比赛
- `setLineup(mid, confirmed)`：确认首发/核心缺阵

### 8.4 index.html 内联关键函数

| 函数 | 行号 | 功能 |
|------|------|------|
| renderHomePage() | 1279 | 首页渲染：倒计时/当日赛事/Canvas粒子 |
| updateCountdownHQ() | ≈1390 | 倒计时更新（每秒）|
| initParticles() | ≈1400 | Canvas粒子系统（80个上升发光粒子）|
| renderStandings() | 1426 | 12组积分榜 |
| renderBracket() | 1476 | 淘汰赛树状图 |
| switchNav(nav) | 1520 | 导航切换+视图显示管理 |

---
## 九、当前状态 & 待处理事项

### 已完成
- ✅ 世界杯首页倒计时（2026-06-12 00:00）
- ✅ Canvas粒子动画系统
- ✅ 6个视图框架（首页/赛程/积分/淘汰赛/赔率/Top）
- ✅ 侧边栏+世界杯专属导航
- ✅ 赛程数据（48场小组赛，含场地/时间/组别）
- ✅ 积分榜demo数据（12组硬编码）
- ✅ 淘汰赛demo数据（硬编码）
- ✅ 竞彩网赔率已同步到 wc_schedule.json
- ✅ 一键全流程 auto_pipeline.py
- ✅ 临场重校 live_ddi.py
- ✅ 方案推荐 plan_engine.py

### 待完成
1. ⬜ 积分榜从 demo 数据改为真实数据（目前硬编码）
2. ⬜ 淘汰赛从 demo 改为真实晋级队伍
3. ⬜ 世界杯赔率页面（oddsContent）尚未实现实质性内容
4. ⬜ Top球员页面（topContent）尚未实现
5. ⬜ app.py 第364行有重复的 v4_edit 定义需要清理
6. ⬜ 根目录大量一次性调试脚本需要归档
7. ⬜ 国旗图片在 static/flags/ 下，部分国家队可能缺图

### 已知问题
1. wc_schedule.json 的赔率数据部分 SP 为字符串（如 "1.31"），需 parseFloat 使用
2. 部分中文编码可能显示为乱码（UTF-8 vs GBK）
3. index.html 有大量备份/测试HTML版本，当前主入口是该文件

---
## 十、快速参考命令

```bash
# 启动
python app.py

# 拉最新竞彩数据 → 全流程分析
python fetch_jczq.py && python auto_pipeline.py

# 带自定义因子运行
python auto_pipeline.py --factor-json path/to/factor_params.json

# 智能生成因子 + AI判断
python smart_factors.py

# 临场重校（单场比赛用 POST /api/live/recalibrate）
# 批量通过浏览器 live.js 面板操作

# 回测
python backtest.py

# 查看数据库
python -c "import database; database.init_db()"
python -c "
import sqlite3
conn = sqlite3.connect('D:/V3.3.3-Core/framework.db')
cur = conn.cursor()
cur.execute('SELECT * FROM runs ORDER BY id DESC LIMIT 5')
for r in cur.fetchall(): print(r)
conn.close()
"
```

---
## 文档结束
> 新窗口启动后执行: 读 D:\V3.3.3-Core\WORLD_CUP_HANDOFF.md
> 然后根据需求继续开发/维护
