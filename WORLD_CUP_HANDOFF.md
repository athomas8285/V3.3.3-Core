# V3.3.3-Core Project Complete Handoff (Updated 2026-06-11)
> 新窗口第一句话：读 D:\V3.3.3-Core\WORLD_CUP_HANDOFF.md
> 项目路径: D:\V3.3.3-Core
> Python 3 + Flask + SQLite + Vanilla JS 单页架构
> 最后活跃: 2026-06-11
> 系统定位: 足球赛事量化分析系统（竞彩/亚盘方向预测），含2026世界杯专属模块

---

## 一、启动方式

```bash
cd D:\V3.3.3-Core
python app.py
# 浏览器打开 http://localhost:5020
```

Flask 开发服务器，默认 127.0.0.1:5020，debug=True。

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
├── fit_score.py                   # Step 8: 贴合度评分（8维度）
├── trend_features.py               # 赔率趋势特征提取（第8维度数据源）
├── track_odds.py                   # 竞彩网赔率定时跟踪（30min间隔）
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
│
├── templates/
│   ├── index.html                 # ★ 主页面（单页应用，全部前端逻辑在此，290KB）
│   ├── charts.js                  # ★ 今日扫盘渲染引擎（卡片表格 + SVG图表）
│   ├── live.js                    # ★ 临场面板交互脚本
│   ├── index.html.bak_20260611_183134  # 近期备份
│   ├── index.html.bak2                 # 近期备份
│   ├── plan.html                  # 方案推荐页面
│   ├── v1.html ~ v6.html          # 历史版本页面（迭代对照）
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
│   ├── trend_features.json         # 赔率趋势特征（第8维度 + S7输入）
│   ├── odds_history/               # 赔率跟踪历史（app.py 后台定时采集）
│   ├── wc_schedule.json           # ★ 世界杯赛程+赔率数据
│   ├── raw_jczq.json              # 竞彩网原始API数据
│   └── all_results_detailed.json  # 详细历史结果汇总
│
├── static/
│   ├── bg1.png / bg2.png          # 背景图
│   ├── flags/                     # 国家队国旗图片
│   └── wechat_qr.jpg              # 微信二维码（联系作者弹窗用）
│
├── versions_backup/               # v1/v2/v3 HTML备份
├── work/                          # 调试脚本
└── _template/                     # 可复用Web模板（独立app + data/templates）
```

---

## 三、页面框架（CSS架构 + 组件）

### 3.1 CSS 变量体系

页面深色主题，在 `:root` 中定义，所有组件引用变量（与旧版一致，未改动）：

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
│ .sd-wrap (250px)  │  .main (flex:1, overflow-y) │
│   ┌─────────────┐  │  ┌─── view-content ───────┐ │
│   │ .sd-top      │  │  │ homeContent (默认)    │ │
│   │  logo+status │  │  │ analysisContent       │ │
│   ├─────────────┤  │  │ scheduleContent       │ │
│   │ .sd-body    │  │  │ standingsContent      │ │
│   │  导航列表    │  │  │ bracketContent        │ │
│   │  系统说明书  │  │  │ oddsContent           │ │
│   │  核心参数说明 │  │  │ topContent            │ │
│   │  比赛分析    │  │  │ manualContent         │ │
│   │  历史比赛回测 │  │  │ paramsContent         │ │
│   ├─────────────┤  │  │ backtestContent       │ │
│   │ .sd-footer  │  │  └───────────────────────┘ │
│   └─────────────┘  │                            │
└─────────────────────────────────────────────────┘
```

侧边栏固定 250px，内容区自适应，滚动条极细风格。

### 3.3 核心组件

**侧边栏导航 (`.sd-nav-item` 类):**
- `data-nav` 属性映射视图
- `.active` 高亮（左侧 3px cyan 边框）

**视图切换系统:**
- `switchNav(nav)` 函数：切换 `.view-content` 显示/隐藏
- 每个视图一个 div，id = {nav}Content，class = "view-content"
- 默认加载后调用 switchNav('home')

### 3.4 页面视图

当前有 10 个视图（全部在 index.html 内，JS 渲染）：

| 视图 | 导航名 | 渲染函数 | 说明 |
|------|--------|----------|------|
| 系统首页 | home | renderHomePage() | 世界杯动态倒计时 + 当日比赛卡片 |
| 比赛分析 | analysis | renderAnalysisView() | 24场小组赛卡片（按日期分组，含赔率/分析数据） |
| 小组赛程 | schedule | renderCalendarView() | 按日期分组显示，含球场、组别、时间 |
| 积分榜 | standings | renderStandingsPage() | 12组分2页，每页6组，翻页按钮在标题行 |
| 淘汰赛 | bracket | renderBracket() | 树状淘汰赛图，硬编码 demo 数据 |
| 赔率 | odds | — | 占位页面 |
| TOP | top | — | 占位页面 |
| 分析系统说明 | manual | — | 从后端API加载Markdown渲染 |
| 核心参数说明 | params | — | 从后端API加载Markdown渲染 |
| 历史比赛回测 | backtest | renderBacktest() | 虚拟历史数据展示 |

---

## 四、所有 API 接口

### 4.1 页面路由

| 路由 | 函数 | 说明 |
|------|------|------|
| `/` | index() | 主页面，注入 __DATA (5个JSON合并) |
| `/test` | test_page | test.html |
| `/debug` | debug_page | debug.html |
| `/full_test` | full_test | full_test.html |
| `/v1` ~ `/v6` | v1~v6 | 版本迭代对照页 |
| `/plan/<level>` | plan_page | 2.0/3.0方案页 |
| `/bak` | index_bak | index.html.bak |

### 4.2 JSON API

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/latest` | GET | 今日比赛完整数据 |
| `/api/parse` | POST | 解析原始文本 |
| `/api/analyze` | POST | 提交 factor_params 运行全分析 |
| `/api/review` | POST | 提交复盘评分 |
| `/api/reviews` | GET | 获取复盘记录（最近50条） |
| `/api/live/info` | GET | 临场信息 |
| `/api/live/recalibrate` | POST | 临场SP重校 |
| `/api/history/runs` | GET | 历史运行统计 |
| `/api/history/matches` | GET | 按日期查历史比赛 |
| `/api/v2/data` | GET | V2兼容数据 |
| `/api/backtest/runs` | GET | 回测数据（demo） |
| `/api/doc/sections` | GET | 文档章节列表 |
| `/api/doc/content/params` | GET | 核心参数说明内容 |
| `/api/doc/content/arch` | GET | 分析框架说明内容 |
| `/api/plan/<level>` | GET | 方案推荐 |
| `/api/wc/schedule` | GET | 世界杯赛程+赔率 |

---

## 五、前端渲染引擎

### 5.1 数据流

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

### 5.2 index.html 内联关键函数

| 函数 | 功能 |
|------|------|
| renderHomePage() | 首页渲染：动态倒计时到最近比赛 / 当日赛事 |
| renderAnalysisView() | 比赛分析视图：24场卡片按日期分组渲染（★改造核心） |
| renderStandingsPage(page) | 积分榜分页渲染 |
| renderCalendarView() | 赛程日历（已优化，删除无效空白） |
| renderBracket() | 淘汰赛树状图 |
| renderBacktest() | 历史回测虚拟数据 |
| switchNav(nav) | 导航切换+视图显示管理 |
| toggleCard(id) | 卡片展开/收起 |
| openContactModal() | 联系作者弹窗 |

### 5.3 比赛分析卡片结构（★最新版）

**折叠状态：**
```
[周四001] [06-12 03:00] [世界杯] [墨西哥  VS  南非]  [0  1.30 4.15 8.40]  [胜]  [6.8A]  [▼]
                                                                 [-1  2.07 3.28 2.93]
```

**展开状态：**
```
┌─────────────────────────────────────────────────────────┐
│ 顶部: 三个胶囊（总进球TOP2 / 半全场TOP2 / 比分TOP3）    │
│                                                         │
│ 中间: 两张SVG柱状图（λ对比 / 物理vs市场概率）           │
│                                                         │
│ 指标: 方向 / 贴合度 / DDI / λ差值                       │
│                                                         │
│ 底部: 📋 比赛解读（推理分析文字，按规则生成）            │
└─────────────────────────────────────────────────────────┘
```

**判断依据（比赛解读）规则：**
- λ差值 < 0.05 → "优势不明显，不易支持让胜"
- λ差值 > 0.08 → "模型信心较强"
- 主胜概率 < 35% → "让胜支撑不足"
- 物理vs市场偏差 > 8% → "存在市场分歧"

**非当日卡片：** 折叠状态正常显示，展开后内容显示"等待预测数据"

---

## 六、当前状态 & 待处理事项

### 已完成（原文档10项 + 新增20+项）

**基础设施：**
- ✅ 世界杯首页倒计时（改为动态：查找最近一场未开始比赛，不硬编码）
- ✅ Canvas粒子动画系统
- ✅ 6+个视图框架（首页/分析/赛程/积分/淘汰赛/赔率/Top/说明书/参数/回测）
- ✅ 侧边栏+世界杯专属导航

**页面优化：**
- ✅ 积分榜分页（12组→每页6组，翻页按钮在标题行右侧）
- ✅ 赛程日历优化（删除1-7号、29-30号空白，保留8-28号）
- ✅ 系统说明书改造（从折叠面板改为独立导航项，内容从后端API加载）
- ✅ DOM结构修复（修复stray div、todayMatches缺失）
- ✅ 页脚 sticky 固定在底部
- ✅ 清除浮动死代码（第1914-1936行）

**比赛分析卡片：**
- ✅ 24场世界杯小组赛卡片渲染（按日期分组）
- ✅ 参考普通版卡片样式重构分析页卡片
- ✅ 竞彩网赔率获取（不让球+让球赔率，让球数）
- ✅ 卡片展开详情（三胶囊 + 柱状图 + 指标 + 比赛解读）
- ✅ 非当日卡片显示"等待预测数据"
- ✅ 比赛解读面板（根据λ/概率/偏差实时生成推理文字）
- ✅ 按时按日期分组显示

**交互优化：**
- ✅ 联系作者弹窗（微信二维码模态窗）
- ✅ 首页卡片点击跳转到分析视图并自动展开
- ✅ "历史比赛回测"虚拟数据展示
- ✅ 分析系统+核心参数两篇详细文档（Markdown输出）

**数据增强：**
- ✅ 世界杯24场小组赛竞彩网数据采集
- ✅ WC分析框架优化（轮次动态、FIFA排名、小组赛制等）
- ✅ 数据采集skill增强（涵盖世界杯完整数据模板）

### ⬜ 待完成

_2026-06-11 新增完成：_
- ✅ 赔率趋势特征提取模块（trend_features.py）
- ✅ 贴合度评分第8维度（trend support）
- ✅ S7后期赔率剧烈变动检测（smart_factors）
- ✅ auto_pipeline.py 集成 trend_features 步骤
- ✅ 技术白皮书更新至 Rev1.15


1. ⬜ 积分榜从 demo 数据改为真实数据
2. ⬜ 淘汰赛从 demo 改为真实晋级队伍
3. ⬜ 赔率页面（oddsContent）实质性内容
4. ⬜ Top球员页面（topContent）
5. ⬜ 竞彩SP实时更新（轮询）
6. ⬜ app.py 重复路由清理
7. ⬜ 根目录调试脚本归档
8. ⬜ 世界杯分析框架代码落地（非仅讨论阶段）

### 已知问题

1. wc_schedule.json 的赔率数据部分 SP 为字符串（如 "1.31"），需 parseFloat 使用
2. 部分中文编码可能显示为乱码（UTF-8 vs GBK），注意用 UTF-8 no BOM 写文件
3. index.html 约290KB，有大量内联JS/CSS，重构时注意性能

### 备份状态

历史备份（均为完整可用的index.html版本）：
- `index.html.bak_20260611_183134` — 近期备份
- `index.html.bak2` — 更早期备份
- 曾存在 世界杯1-7号 / 完整版1-1.2 / 初版1-2 等版本，可能已清理

---

## 七、

## 统一数据采集工作流

每次采集数据时，按此顺序执行两个方案，确保数据全面：

### 方案一：自动批量采集（必做）
一键完成竞彩SP + SofaScore深度数据 + 赔率趋势 + 全流程分析：

`ash
# 完整采集+分析（首次自动拉SofaScore，后续加 --refresh-sofa 强制刷新）
python auto_pipeline.py

# 如需强制刷新SofaScore数据
python auto_pipeline.py --refresh-sofa
`

内部执行顺序：
1. [1/5] 读取 locked_data.json
2. [2/5] 生成 match_info.json
3. [2.5/5.5] 获取 SofaScore 数据（xG/伤停/H2H/场地）
4. [2.6/5.6] 融合数据到 locked_data.json
5. [3/5] 检查因子参数
6. [4/5] 检查AI判断
7. [5/6] 提取赔率趋势特征
8. [6/6] 全流程分析（DDI → fit_score → 评级）
9. [7/8] 拉取竞彩网最新SP
10. [8/8] 同步赔率到数据文件

### 方案二：逐场深度分析（按需）
对关注的比赛，用 data-acquisition skill 做8大板块完整分析：
- 说"拉数据"或"分析[比赛名]"触发 skill
- 覆盖：基本信息、竞彩赔率、亚洲盘口、赛季数据、近期战绩、伤停、战意、特殊事项
- 每场独立输出完整分析报告，逐场审阅确认

### 日常流程
1. 跑 auto_pipeline.py（方案一）→ 出24场批量预测
2. 对重点比赛，说"分析[比赛名]"（方案二）→ 获取深度分析
3. 方案二的深度数据会自动写回 locked_data，下次跑 pipeline 时生效

快速参考命令

```bash
# 启动（超端口5020）
python app.py

# 拉最新竞彩数据 → 全流程分析
python fetch_jczq.py && python auto_pipeline.py

# 带自定义因子运行
python auto_pipeline.py --factor-json path/to/factor_params.json

# 智能生成因子 + AI判断
python smart_factors.py

# 提取赔率趋势特征（供 fit_score 第8维 + S7 使用）
python trend_features.py

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

【本次更新 2026-06-11】
- 根据世界杯页面线程历史对话，补充了20+项已完成工作
- 端口从5000改为5020
- 新增比赛分析卡片、比赛解读面板、积分榜分页、赛程优化等模块说明
- 更新视图列表（从6个扩展到10个）
- 更新待办/已知问题
