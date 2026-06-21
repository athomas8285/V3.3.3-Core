# APP数据 更新指令

## 文件路径

```
C:\Users\gjj\Documents\Codex\2026-06-14\app-app\outputs\data\
```

| 文件 | 路径 |
|------|------|
| 比赛数据 | `C:\Users\gjj\Documents\Codex\2026-06-14\app-app\outputs\data\analysis.json` |
| 配置数据 | `C:\Users\gjj\Documents\Codex\2026-06-14\app-app\outputs\data\config.json` |
| 资讯数据 | `C:\Users\gjj\Documents\Codex\2026-06-14\app-app\outputs\data\news.json` |

---

## 写入逻辑

| 场景 | 操作 |
|------|------|
| 新增比赛预测 | `rating[]` push、`mc[]` push |
| 重新预测同一场 | 按 `id` 找到，覆盖旧字段 |
| 赛后填赛果 | 按 `id` 找到，只改赛后字段 |

**规则：`rating[]` 和 `mc[]` 按 `id` 找，存在就覆盖，不存在就 push。**

---

## 一、写入 analysis.json

### 1.1 rating[] — 赛前预测字段

| 字段 | 类型 | 必填 | 示例 | 说明 |
|------|------|:----:|------|------|
| `id` | string | ✅ | `"周一013"` | 比赛ID，格式`周X+三位数` |
| `date` | string | ✅ | `"06-15"` | MM-DD 格式 |
| `event` | string | ✅ | `"E组"` | 赛事标识 |
| `group` | string | ✅ | `"E"` | 小组 A~L |
| `home` | string | ✅ | `"德国"` | 主队名 |
| `away` | string | ✅ | `"库拉索"` | 客队名 |
| `homeFlag` | string | ✅ | `"🇩🇪"` | **必填！** 从 config.json teamFlags 取 |
| `awayFlag` | string | ✅ | `"🇨🇼"` | **必填！** 从 config.json teamFlags 取 |
| `direction` | string | ✅ | `"胜"` | **取值：`胜`/`负`/`平`/`让胜`/`让负`**（注意不是`主胜`/`客胜`/`平局`） |
| `rating` | string | ✅ | `"A"` | 置信度 `A`/`B`/`C` |

### 1.2 rating[] — 赛后复盘字段（赛果已知时必填）

| 字段 | 类型 | 必填 | 示例 | 说明 |
|------|------|:----:|------|------|
| `actual_score` | string | ✅ | `"2-0"` | 实际比分 |
| `hit` | boolean | ✅ | `true` | 预测是否命中 |
| `result` | string | ✅ | `"hit"` | 取值：`"hit"` / `"miss"` / `"draw"` |
| `score` | string | ✅ | `"2-0"` | 同 actual_score |
| `predClass` | string | ✅ | `"hit"` | 取值：`"hit"` / `"miss"` / `""` |

**赛后只改这 5 个字段，不动 direction/rating 等赛前字段。**

**命中判断规则：**
- direction=`胜` 且 主队进球>客队 → hit=true, result="hit"
- direction=`胜` 且 主队进球<客队 → hit=false, result="miss"
- direction=`平` 且 比分相同 → hit=true, result="hit"
- direction=`负` 且 客队进球>主队 → hit=true, result="hit"
- direction=`负` 且 客队进球<主队 → hit=false, result="miss"
- 让球盘走水 → result="draw"

### 1.3 mc[] — 模型计算数据

| 字段 | 类型 | 必填 | 示例 |
|------|------|:----:|------|
| `id` | string | ✅ | `"周一013"` |
| `home` | string | ✅ | `"德国"` |
| `away` | string | ✅ | `"库拉索"` |
| `lambda_raw_h` | number | ✅ | `2.5439` |
| `lambda_raw_a` | number | ✅ | `0.3000` |
| `lambda_h_final` | number | ✅ | `2.6304` |
| `lambda_a_final` | number | ✅ | `0.2961` |
| `lambda_diff` | number | ✅ | `2.3343` |
| `jc_handicap` | number | ✅ | `-1` |
| `physical` | object | ✅ | `{"home_win":0.872,"draw":0.110,"away_win":0.018}` |
| `jc_handicap_prob` | object | ✅ | `{"rang_sheng":0.668,"rang_ping":0.204,"rang_fu":0.128}` |
| `top2_total_goals` | array | ✅ | `["2球","3球"]` |
| `top2_half_full` | array | ✅ | `["胜胜","平胜"]` |
| `top3_scores` | array | ✅ | `["2-0","3-0","1-0"]` |

### 1.4 narratives — 分析文本

```json
{
  "narratives": {
    "周一013": "模型主胜 87.2% / 差+2.33，赔率趋势持续压低主胜..."
  }
}
```

key=比赛ID，value=分析字符串。

### 1.5 AL / GR / DN — 赛程与分组

```json
{
  "AL": { "06-15": ["周一013", "周一014", "周一016"] },
  "GR": { "E": ["德国", "科特迪瓦", "厄瓜多尔", "库拉索"] },
  "DN": { "06-15": "周一" }
}
```

---

## 二、同步更新 config.json

**重要：每次新增比赛或球队时，必须同步更新 config.json，否则前端会缺旗帜或场馆。**

### teamFlags — 新增球队时添加

```json
{
  "新球队名": { "flag": "🇽🇽", "color": "linear-gradient(135deg,#颜色1,#颜色2)" }
}
```

已知场馆城市：墨西哥城、瓜达拉哈拉、多伦多、洛杉矶、旧金山湾区、纽约/新泽西、波士顿、休斯敦、达拉斯、费城、蒙特雷、亚特兰大、西雅图、堪萨斯城、迈阿密、温哥华

### venues — 新增比赛时添加

```json
{
  "比赛ID": { "group": "A", "venue": "城市名" }
}
```

---

## 三、写入 news.json

**不自动追加。** 需要更新文章时，由用户手动指示后再操作。
格式参考：

- `pinned` 不动
- `url` 不可为 `#`

---

## 四、名称一致性（最重要）

**球队名** 在以下位置必须完全一致：

| 位置 | 文件 |
|------|------|
| `rating[].home` / `rating[].away` | analysis.json |
| `mc[].home` / `mc[].away` | analysis.json |
| `GR` 数组 | analysis.json |
| `teamFlags` 的 key | config.json |

**比赛 ID** 在以下位置必须一致：

| 位置 | 文件 |
|------|------|
| `rating[].id` / `mc[].id` | analysis.json |
| `AL` 数组 | analysis.json |
| `narratives` 的 key | analysis.json |
| `venues` 的 key | config.json |

---

## 五、本次更新踩坑记录（下次注意）

以下是 agent 第一次更新时出的问题，已修复，下次避免：

### ❌ 漏填 homeFlag / awayFlag
所有 rating[] 条目都缺这两个字段，前端复盘页显示 `undefined`。
**对策**：每个比赛对象必须显式填入，值从 config.json teamFlags 取。

### ❌ 漏填 result / score / predClass
已完赛比赛只写了 actual_score 和 hit，缺失 result、score、predClass，复盘页无法正常显示命中状态。
**对策**：赛后更新时 5 个字段（actual_score + hit + result + score + predClass）一起填，不要遗漏。

### ❌ 球队名不在 config.json teamFlags 中
用了 `奥大利亚`、`沙特`、`民主刚果`，但 config.json 里没有这些 key。
**对策**：使用新队名时必须先在 config.json teamFlags 中添加对应条目，否则旗帜显示为黑旗。

### ❌ 比赛 ID 不在 config.json venues 中
新增比赛 `周六008`、`周三021`、`周一015` 没有对应的场馆映射。
**对策**：新增比赛 ID 时必须同步在 config.json venues 中添加。

### ⚠️ direction 取值与 spec 不一致
agent 用了 `胜`/`负`/`平`/`让胜`/`让负`，但旧 spec 写的是 `主胜`/`客胜`/`平局`。
**对策**：已更新本指令，统一用 `胜`/`负`/`平`/`让胜`/`让负`。下次按此标准。

---

## 六、文件操作规则

- 所有 JSON 保存为 **UTF-8 无 BOM**，中文和 emoji 保留原字符不转义
- 写入前先读最新版本
- 不要删除已有数据
- 只动 `outputs/data/` 目录，**不改 index.html**

---

## 七、完成检查清单

- [ ] rating[] 中所有新增比赛已填 homeFlag / awayFlag
- [ ] 已完赛比赛的 actual_score / hit / result / score / predClass 都填了
- [ ] 新球队已添加到 config.json teamFlags
- [ ] 新比赛 ID 已添加到 config.json venues
- [ ] 队名在 analysis.json 和 config.json 之间一致
- [ ] 比赛 ID 在所有位置一致
- [ ] JSON 已保存为 UTF-8 无 BOM
