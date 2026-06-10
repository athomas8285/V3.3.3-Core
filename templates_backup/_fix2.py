import re

BASE = "C:/Users/gjj/Desktop/v333/templates"

with open(BASE + "/index.html.current_fix", "r", encoding="utf-8") as f:
    fix = f.read()

# ─── Clean text content (from backup, verified manually) ───

# 分析系统介绍 intro text
intro_parts = [
    'V3.3.3-Core 是一套完整的足球比赛预测与分析框架，覆盖从数据采集、模型运算到赛后复盘的全流程。系统基于泊松分布建模，通过蒙特卡洛模拟（2000次/场）计算胜平负概率，引入DDI（盘口偏差指数）校准市场热度偏差，并叠加多维度因子修正：',
    '- <b>伤停因子</b> — 核心球员缺阵对攻防能力的量化影响，区分核心（+-20%）与轮换（+-5%）两个层级',
    '- <b>战意因子</b> — 保级、争冠、德比等场景下的战意修正，决赛期+-5%，常规期+-15%',
    '- <b>松懈扣减</b> — 已保级/已出线球队的lambda降8%',
    '- <b>高原加成</b> — 海拔>2500m主场优势加成15%',
    '最终输出推荐方向、适配度评分（0-10）和置信等级（S/A/B/C），兼顾数据面与市场情绪的双重视角。'
]
intro_html = (
    '<div class="meth-p">' + intro_parts[0] + '</div>\n' +
    '<div class="meth-p" style="margin-top:6px">' + intro_parts[1] + '</div>\n' +
    '<div class="meth-p">' + intro_parts[2] + '</div>\n' +
    '<div class="meth-p">' + intro_parts[3] + '</div>\n' +
    '<div class="meth-p">' + intro_parts[4] + '</div>\n' +
    '<div class="meth-p" style="margin-top:6px">' + intro_parts[5] + '</div>'
)

# Other sections
texts = {
    "核心逻辑": "基于泊松分布的进球期望模型（lambda），通过蒙特卡洛模拟（2000次/场）生成胜平负概率分布。结合DDI（盘口偏差指数）校准与因子修正系统，输出推荐方向与适配度评分。",
    "Lambda 计算": "从竞彩SP反推市场隐含lambda，与基于xG/实际进球的物理lambda进行交叉验证。最终lambda在两者之间加权平衡，兼顾市场预期与基本面实力。",
    "DDI 校准": "DDI = P(物理) - P(市场)，衡量模型与市场之间的偏差。|DDI| > 0.08 时触发校准，方向与市场热度相反时降级处理。校准幅度不超过0.05，防止过度修正。",
    "因子修正": "伤病影响（核心+-20%，轮换+-5%）、战意修正（决赛期+-5%，常规期+-15%）、松懈扣减（8%）、高原加成（15%）。多因子叠加后重新归一化lambda。",
    "风控降级": "深盘（AH>=2.0）自动降级1级；中盘（1.0<=AH<=1.25）且lambda差<0.5额外降级；适配度<4.0触发熔断，标记为C级。"
}

# Version history
versions = [
    ('Rev1.13', '2026-05-31', 'DDI振幅比例参数化；客阵冷处理机制；Lambda归一化重算逻辑优化；自适应评分区间。'),
    ('Rev1.12', '2026-05-28', '新增数据缺失标记系统；蒙特卡洛模拟次数从1000提升至2000；半全场预测逻辑修正。'),
    ('Rev1.11', '2026-05-25', '多因子叠加归一化；战意修正与伤病因子独立评估；风控降级模型重构。'),
    ('Rev1.10', '2026-05-20', '初始版本：泊松lambda模型 + 蒙特卡洛模拟 + DDI校准 + 基础因子修正。')
]
ver_items = ''
for vv, vd, vm in versions:
    ver_items += f'      <div class="v-item"><span class="v-ver">{vv}</span><span class="v-date">{vd}</span><div class="v-msg">{vm}</div></div>\n'
ver_html = f'''      <div class="meth-h">版本更新</div>
{ver_items}'''

# Parameter descriptions
params = {
    "蒙特卡洛模拟": [
        ('运行次数', 'MONTE_CARLO_RUNS = 2000', '每场比赛跑2000次随机模拟，算出最可能的赛果概率分布。'),
        ('半场比例', 'HALF_TIME_RATIO = 0.44', '半场进球占全场的比例系数，用于半全场预测。')
    ],
    "DDI 校准": [
        ('Kelly因子', 'D_KELLY_DEFAULT = 0.05', '凯利系数，控制资金管理模型的风险偏好。'),
        ('资金流偏差', 'VBAL_DEFAULT = 0.15', '市场资金流向偏差的默认估计值。'),
        ('触发阈值', 'DDI_TRIGGER_THRESHOLD = 0.08', 'DDI偏差超过此值触发校准，市场热度异常。'),
        ('振幅封顶', 'DDI_AMPLITUDE_CAP = 0.05', '单次DDI校准最大幅度，防止过度修正。'),
        ('振幅比例', 'DDI_AMPLITUDE_RATIO = 0.30', 'DDA校准占总偏差的比例（0-1）。'),
        ('客阵冷处理', 'AWAY_COLD_TREATMENT = 0.08', '特殊赛事客队冷却处理幅度，防止反向走热。')
    ],
    "因子修正": [
        ('伤病核心上限', 'INJURY_CORE_MAX = 0.20', '核心球员缺阵最大影响：lambda修正不超过+-20%。'),
        ('轮换上限', 'INJURY_ROTATION_MAX = 0.05', '轮换伤病影响上限，不超过+-5%。'),
        ('松懈罚款', 'SLACK_PENALTY = 0.08', '已保级/已出线球队松懈扣减，lambda降8%。'),
        ('高原加成', 'ALTITUDE_BONUS = 0.15', '海拔>2500m主场优势：lambda加成15%。')
    ],
    "战意修正": [
        ('决赛期上限', 'MOTIVATION_CAP_PLAYOFF = 0.05', '附加赛/末轮生死战：战意修正上限+-5%。'),
        ('常规期上限', 'MOTIVATION_CAP_REGULAR = 0.15', '常规联赛：战意修正上限+-15%。')
    ],
    "风控降级": [
        ('深盘阈值', 'DEEP_HANDICAP_THRESHOLD = 2.0', '让球>=2球触发深盘降级，评级+1级风险。'),
        ('中盘区间', '1.0 <= AH <= 1.25', '中盘区间：让球1-1.25且lambda差<0.5额外降级。'),
        ('熔断阈值', 'FIT_SCORE_THRESHOLD_MELTDOWN = 4.0', '')
    ]
}

def make_sp_g(title, items):
    """Build a collapsible sp-g section with parameter items"""
    items_html = ''
    for lk, lv, desc in items:
        desc_html = f'<br>{desc}' if desc else ''
        items_html += f'<div class="sp-g-i"><span class="lk">{lk}</span> <span class="lv">{lv}</span>{desc_html}</div>\n'
    title_esc = title.replace("'", "\\'")
    return f'''<div class="sp-g"><div class="sp-g-h" onclick="var p=this.parentNode;var c=p.querySelector('.sp-g-c');if(c){{c.classList.toggle('open');p.classList.toggle('expanded');}}">{title}</div><div class="sp-g-c">
{items_html}</div></div>
'''

param_bd = ''
for title, items in params.items():
    param_bd += make_sp_g(title, items)

def make_sp_g_section(title, content):
    return f'''  <div class="sp-g sp-g-tl">
    <div class="sp-g-h" onclick="var p=this.parentNode;var c=p.querySelector('.sp-g-c');if(c){{c.classList.toggle('open');p.classList.toggle('expanded');}}">{title}</div>
    <div class="sp-g-c">
{content}
    </div>
  </div>'''

def make_sub_sp_g(title, content):
    title_esc = title.replace("'", "\\'")
    return f'''      <div class="sp-g">
        <div class="sp-g-h" onclick="var p=this.parentNode;var c=p.querySelector('.sp-g-c');if(c){{c.classList.toggle('open');p.classList.toggle('expanded');}}">{title}</div>
        <div class="sp-g-c">{content}</div>
      </div>'''

# Build section 1 - 分析框架
sec1_inner = ''
sec1_inner += make_sub_sp_g("分析系统介绍", intro_html)
for stitle, stext in [
    ("核心逻辑", texts["核心逻辑"]),
    ("Lambda 计算", texts["Lambda 计算"]),
    ("DDI 校准", texts["DDI 校准"]),
    ("因子修正", texts["因子修正"]),
    ("风控降级", texts["风控降级"]),
]:
    sec1_inner += make_sub_sp_g(stitle, f'<div class="meth-p">{stext}</div>')
sec1_inner += make_sub_sp_g("版本更新", ver_html)

section1 = make_sp_g_section("V3.3.3-Core 分析框架", sec1_inner)

# Build section 2 - 框架参数说明
section2 = make_sp_g_section("框架参数说明", param_bd)

# Build complete right panel
new_right_panel = f'''<div class="sp" id="spPanel"><div class="sp-hdr"><h2>V3.3.3-Core 分析框架</h2></div>
<div class="sp-bd">
{section1}
{section2}
</div>
</div>'''

# Verify balance
open_d = new_right_panel.count("<div")
close_d = new_right_panel.count("</div>")
print(f"New panel: {open_d} open, {close_d} close, diff={open_d-close_d}")

# Find region to replace in current_fix
sp_start = fix.index('<div class="sp" id="spPanel">')
script_pos = fix.index('<script src="/charts.js">', sp_start)
before_script = fix[sp_start:script_pos]
last_close = before_script.rstrip().rfind("</div>")
sp_end = sp_start + last_close + 6

print(f"Replacing: {sp_start}-{sp_end} (len={sp_end-sp_start}) with {len(new_right_panel)}")

# Replace
new_fix = fix[:sp_start] + new_right_panel + fix[sp_end:]

# Fix CSS margin
new_fix = new_fix.replace("margin:0 auto", "margin:0 80px 0 40px")

# Verify total
total_open = new_fix.count("<div")
total_close = new_fix.count("</div>")
print(f"Total: {total_open} open, {total_close} close, diff={total_open-total_close}")
print(f"Size: {len(new_fix)} bytes")

with open(BASE + "/index.html", "w", encoding="utf-8") as f:
    f.write(new_fix)
print("DONE")
