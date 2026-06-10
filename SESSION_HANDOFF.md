# V3.3.3-Core Session Handoff
# Generated 2026-06-03 21:20

## 服务器
Flask running on localhost:5000
Start: python app.py  (in v333 directory)

## 改动文件清单
- templates/index.html       — 历史面板修复 + 推荐度对齐 + LIVE面板HTML
- templates/charts.js        — 昨日扫盘推荐度对齐
- templates/live.js          — 左面板LIVE交互脚本
- app.py                     — +/api/live/recalibrate, /api/live/info, /live.js
- live_ddi.py                — 临场重校引擎
- ddi.py / fit_score.py / rating.py — (未改动, live_ddi依赖调用)

## 今晚4场临场分析结果（封盘前最新）
001 丹麦 vs 刚果金   让负 B   DDI-0.65背离巨大
002 荷兰 vs 阿尔及利亚 胜 A    SP1.18市场高度集中
003 波兰 vs 尼日利亚   胜 A    DDI+0.088超阈值需关注
004 卢森堡 vs 意大利   负 A    适配度7.36全场最一致
推荐: 004负 + 002胜 或 单关004负

## 新skill（重启后生效）
agent-browser / firecrawl-scraper / webapp-testing / summarize
├─ firecrawl-scraper   — 自动抓实时赔率代替手动贴
├─ agent-browser       — 首发阵容截图/验证
└─ webapp-testing      — Playwright测试UI
