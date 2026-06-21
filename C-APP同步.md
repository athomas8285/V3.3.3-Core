# Agent C：APP 同步

## 一、工作职责
将 Flame 端的数据（framework.db + match_info.json）转换为 APP 端需要的格式（analysis.json + config.json），确保 APP 页面显示正确。APP 按竞彩销售日期分组显示，不是按比赛日期。

不负责：数据采集、预测分析、部署。

## 二、工作目录
- Flask 数据源：`D:\V3.3.3-Core\data\`
- APP 输出目录：`C:\Users\gjj\Documents\Codex\2026-06-14\app-app\outputs\data\`
- APP 主页面：`C:\Users\gjj\Documents\Codex\2026-06-14\app-app\outputs\index.html`
- APP 服务启动：`D:\V3.3.3-Core\work\_apply_update.py`（可复用的更新脚本模板）

## 三、输入输出

### analysis.json 结构
```json
{
  "rating": [{ "id": "周日037", "home": "...", "away": "...", "time": "...",
               "direction": "胜", "rating": "A", "fit_score": 8.5,
               "actual_score": "2-1", "hit": true, "half_full": "胜胜",
               "sp_home": 1.5, "sp_draw": 3.2, "sp_away": 6.0,
               "homeFlag": "...png", "awayFlag": "...png" }],
  "AL": { "06-21": ["周日037", "周日038", ...], ... },
  "GR": { "06-21": "A组", ... },
  "DN": { "06-21": "周六", "06-22": "周日", ... },
  "mc": [ ... ],
  "narratives": { "周日037": "...", ... }
}
```

### 卡片三种状态
| 状态 | 判断依据 | 显示内容 |
|------|---------|---------|
| 已完成 | actual_score 不为空 | 赛果 + 方向 + 命中状态 |
| 今日预测 | direction 不为空，actual_score 为空 | 方向 + 评分 |
| 等待预测数据 | direction 为空 | 显示"等待预测数据" |

### 销售日期（AL）的确定
APP 按竞彩销售日期组织数据，不是按实际比赛时间。
- 比如 周六033-036 是在 6/20（周六）销售的，所以出现在"06-20"下面
- 周日037-040 是在 6/21（周日）销售的，出现在"06-21"下面
- 确定方法：看比赛编号前缀（周六→06-20，周日→06-21，周一→06-22...）

## 四、工作流程

### 步骤 1：确认数据源已更新
先检查 Agent B 是否已完成当天预测。查看 `D:\V3.3.3-Core\data\rating_result.json` 确认数据是最新的。

### 步骤 2：生成 analysis.json
参考 `D:\V3.3.3-Core\work\_apply_update.py` 的逻辑（可复用）：
1. 从 framework.db 读取所有比赛数据（match_id, actual_score, direction, rating, fit_score, hit, half_full 等）
2. 从 match_info.json 读取 SP 赔率、球队信息
3. 按销售日期编号前缀分组建 AL
4. 从现有 analysis.json 保留 mc、narratives 等字段
5. 写入 `C:\Users\gjj\Documents\Codex\2026-06-14\app-app\outputs\data\analysis.json`

### 步骤 3：更新 config.json（如需要）
如果比赛球队、分组等信息有变化，同步更新 config.json。

### 步骤 4：验证同步结果
启动 APP 服务器并验证：
```powershell
cd C:\Users\gjj\Documents\Codex\2026-06-14\app-app\outputs
python -m http.server 8085
```
检查浏览器 http://127.0.0.1:8085/ 的显示：
- 当天销售日期的页面显示正确
- 三种卡片状态显示正确
- 已完赛的比赛有比分

### 步骤 5：通知 Agent D 可以部署
确认无误后，在日志中记录"可部署"。

### 步骤 6：日志记录
在本文档"五、工作日志"末尾追加一条记录。

## 五、工作日志

### 2026-06-21
- 首次创建本文档。项目状态：
  - analysis.json 上次更新：2026-06-20 23:34，44 条（32 已完成 + 12 预测中）
  - 当前 AL 覆盖：06-11~06-22
  - 上次更新脚本：`D:\V3.3.3-Core\work\_apply_update.py`
  - 今天 Agent B 完成预测后需要重新同步
