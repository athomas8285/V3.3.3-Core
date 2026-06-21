# V3.3.3-Core 世界杯竞彩预测系统

## 快速启动
```
cd D:\V3.3.3-Core
python app.py          # Flask 网页版（端口 5020）
```

## 系统架构
详见 `技术白皮书.md`

## 完整工作流程

```
竞彩网 11:00 开盘
    ↓
[A-数据采集.md] → 抓取当天数据 → 写入 DB
    ↓
[B-分析预测.md] → 跑预测管道 → 复盘昨天
    ↓
[C-APP同步.md]  → 生成 analysis.json
    ↓
[D-部署上传.md]  → git push 两个仓库
```

## Agent 文档（新 agent 第一件事读这些）
- `A-数据采集.md` — 每天抓取竞彩网数据、补赛果
- `B-分析预测.md` — 跑预测管道、复盘
- `C-APP同步.md` — 同步数据到 APP 版
- `D-部署上传.md` — 推送到 GitHub

## 项目目录
- `app.py` — Flask 服务器入口
- `framework.db` — SQLite 数据库（所有数据的唯一源头）
- `data/` — 数据文件（match_info, rating_result 等）
- `templates/` — 前端模板（index.html, charts.js, live.js）
- `static/` — 静态资源（队旗、背景图等）
- `work/` — 临时脚本
- `_archive/` — 历史归档

## 数据流向
竞彩网 → fetch_jczq.py → framework.db → run_all.py → rating_result.json → [Flask 页面]
                                                                     ↓
                                                              analysis.json → [APP 页面]
