# V3.3.3-Core 足球量化分析系统

足球赛事量化分析 Web 应用，采用 Flask + 纯前端单页架构。

## 快速启动

```bash
python app.py
# 浏览器打开 http://localhost:5000
```

## 核心功能

- 赛事评分表格（含评级、λ值、DDI、S7分数）
- 点击展开详情行（λ差值、S7说明、诱盘分析、风险提示）
- SVG 图表：λ 对比柱状图 + 物理概率 vs 市场概率对比图

## 数据流

```
数据文件 (data/*.json) → Flask API (/api/latest) → 前端渲染
```

## 模板

独立可复用的模板位于 `_template/` 目录，详见 `_template/README.md`。

## 目录结构

```
├── app.py              # Flask 服务器
├── templates/          # 前端模板
│   ├── index.html      # HTML 壳
│   └── charts.js       # 所有 JS 逻辑
├── data/               # JSON 数据
├── _template/          # 可复用的 Web 模板
├── *.py                # 数据处理脚本
└── *.html              # 其他测试/调试页面
```
