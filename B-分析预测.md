# Agent B：分析预测

## 一、工作职责
对当天需要预测的比赛运行分析管道（lambda → MC → DDI → fit_score → rating），产出预测方向和评级。对上一天的预测做复盘诊断，统计命中率。

不负责：数据采集、APP 同步、部署。

## 二、工作目录
- 项目根目录：`D:\V3.3.3-Core`
- 数据库：`D:\V3.3.3-Core\framework.db`
- 预测结果：`D:\V3.3.3-Core\data\rating_result.json`
- 历史记录：`D:\V3.3.3-Core\history.csv`
- 复盘输入：`D:\V3.3.3-Core\data\review.json`

## 三、输入输出

### 预测
- 输入：DB 中当天需要预测的比赛数据 + match_info.json + locked_data.json
- 输出：rating_result.json（direction, rating, fit_score 等）+ 写入 DB

### 复盘
- 输入：DB 中前一天的比赛数据 + history.csv + review.json
- 输出：更新 history.csv（hit、diagnosis 字段）+ 写入 DB

### 关键判断逻辑
当天要预测哪些比赛 → 看竞彩网编号前缀表示的销售日期。比如说：
- 2026-06-21（周日）销售 → 周日037-040
- 2026-06-22（周一）销售 → 周一041-044
- 以此类推。
每天固定预测当天销售日期的这一批，一个不多一个不少。

前一天哪些比赛需要复盘 → 前一天预测的那批比赛如果已有赛果（已过开赛时间），就跑 review.py。

## 四、工作流程

### 步骤 1：判断当天需要预测的比赛
先检查 Agent A 是否已完成当天数据采集。查看 `data/match_info.json` 中当天的比赛：
- 通过编号前缀确定销售日期（如"周日"、"周一"）
- 在 DB 中查这些比赛是否已有 direction（已被预测过）
- 已有 direction 的跳过，没有的才是今天要预测的

### 步骤 2：检查数据完整性
确保要预测的比赛在 locked_data.json 和 match_info.json 中有完整的基础数据（赔率、球队等信息）。

如有缺失，先协调 Agent A 补数据。

### 步骤 3：运行预测管道
```powershell
cd D:\V3.3.3-Core
python auto_pipeline.py
```
或者手动分步：
```powershell
python run_all.py
```

### 步骤 4：验证预测结果
检查 `data/rating_result.json`：
- 所有当天预测的比赛都有 direction 和 rating
- 无异常值（fit_score 为 0 或方向为空的需要重跑）

### 步骤 5：运行复盘
对前一天的预测结果做复盘：
```powershell
python review.py
```
查看输出中的命中率统计。如果命中率显著低于历史均值，记录到日志中。

### 步骤 6：同步到 match_info
预测结果也应该同步更新到 `data/match_info.json`（方向、评分等字段），供 APP 同步时使用。

### 步骤 7：日志记录
在本文档"五、工作日志"末尾追加一条记录。

## 五、工作日志

### 2026-06-21
- 首次创建本文档。项目状态：
  - 今天（周日）需预测：037-040（荷兰 vs 瑞典、德国 vs 科特迪瓦、厄瓜多尔 vs 库拉索、突尼斯 vs 日本）
  - 昨天（周六/6/20）预测的 033-036：部分已开赛，review.py 可跑
  - 最新一次完整运行结果：32 已完赛，12 预测中
