# V3.3.3-Core Web 基础框架模板

## 架构概览

Flask 轻量服务 + 纯前端单页应用，无前端构建工具依赖。

```
项目根目录/
├── app.py                # Flask 服务器入口
├── templates/
│   ├── index.html        # HTML 壳（style + script 引用）
│   └── charts.js         # 全部 JS 逻辑（数据获取、表格、SVG 图表）
├── data/                 # JSON 数据目录
│   ├── rating_result.json      # 评分结果（matches[]）
│   ├── monte_carlo_result.json # MC 模拟结果（matches[]）
│   ├── match_info.json         # 赛事信息（matches[]）
│   ├── ddi_result.json         # DDI 偏差结果（matches[]）
│   └── ai_judgment.json        # AI 判断结果（matches[]）
└── _template/            # 本模板的独立副本
```

## 数据流

```
启动 → index.html → 加载 charts.js
  → window.onload → fetch('/api/latest')
  → rs(d) → 渲染表格 + buildCharts()
  → 用户点击行 → toggle 详情行（含 SVG 图表）
```

## 核心数据结构（/api/latest 返回）

```json
{
  "rating": [ /* 评分 */ ],
  "mc": [ /* Monte Carlo */ ],
  "info": [ /* 赛事信息 */ ],
  "ddi": [ /* DDI 偏差分析 */ ],
  "ai": [ /* AI 判断 */ ]
}
```

5 个数组**按比赛 ID 对齐**，同一索引对应同一场比赛。

### rating[] 关键字段
- `id`, `home`, `away`, `time`, `direction`, `fit_score`, `rating`, `downgrade_count`

### mc[] 关键字段
- `lambda_h_final`, `lambda_a_final`, `lambda_diff`
- `physical`: `{ home_win, draw, away_win }` (物理概率，总和=1)

### info[] 关键字段
- `asian_handicap` (盘口)

### ddi[] 关键字段
- `p_market`: `{ home_win, draw, away_win }` (市场隐含概率)
- `ddi`: `{ home_win, draw, away_win }` (DDI 偏差值)

### ai[] 关键字段
- `s7_score`, `s7_reason`, `trap_analysis`, `key_risk`

## 前端约定

### 配色
- 背景：`#0f0c29` 深色
- 表格头：`#0f3460`
- 表格行：`#16213e`
- 主胜：`#66bb6a`（绿色）
- 平局：`#ffa726`（橙色）
- 客胜：`#ef5350`（红色）
- 物理概率：`#42a5f5`（蓝色）
- 市场概率：`#ef5350`（红色）

### SVG 图表
- 全部用 `document.createElementNS(NS, "svg")` 创建
- 两个图表块：λ 对比柱状图 + 物理 vs 市场概率对比图
- 使用 `viewBox` + 固定 `width/height` 保证渲染一致性
- 图表在 `buildCharts()` 中构建，插入到详情行的 `.detail-box` 内

### 表格交互
- 点击行 → toggle `show` class → 展开/收起详情行
- 详情行包含：λ 差值、S7 说明、诱盘分析、风险提示 + SVG 图表

### 全局数据
- `_DATA` 变量存储完整 API 返回
- `buildCharts()` 通过 `_DATA.mc[idx]` / `_DATA.ddi[idx]` 获取原始数据，不从 DOM 反解析

## 启动

```bash
cd 项目目录
python app.py
# 访问 http://localhost:5000
```

## 复用模板

复制 `_template/` 目录到新项目，然后：
1. 修改 `templates/index.html` 标题和配色
2. 修改 `templates/charts.js` 的表格列和图表类型
3. 替换 `data/` 目录为实际数据
4. 调整 `app.py` 中 `/api/latest` 的数据读取路径
