# This script generates fetch_sofascore_data.py
import json, os

lines = []
lines.append('import asyncio, json, os, sys')
lines.append("sys.stdout.reconfigure(encoding='utf-8')")
lines.append('from playwright.async_api import async_playwright')
lines.append('from datetime import datetime, timezone, timedelta')
lines.append('')
lines.append('BASE_DIR = os.path.dirname(os.path.abspath(__file__))')

# Team name mapping
team_map = {
    "墨西哥":"Mexico", "南非":"South Africa", "韩国":"Korea Republic",
    "捷克":"Czech Republic", "加拿大":"Canada", "波黑":"Bosnia and Herzegovina",
    "美国":"USA", "巴拉圭":"Paraguay", "卡塔尔":"Qatar",
    "瑞士":"Switzerland", "巴西":"Brazil", "摩洛哥":"Morocco",
    "海地":"Haiti", "苏格兰":"Scotland", "澳大利亚":"Australia",
    "土耳其":"Turkiye", "德国":"Germany", "库拉索":"Curacao",
    "荷兰":"Netherlands", "日本":"Japan", "科特迪瓦":"Ivory Coast",
    "厄瓜多尔":"Ecuador", "瑞典":"Sweden", "突尼斯":"Tunisia",
    "西班牙":"Spain", "佛得角":"Cape Verde", "比利时":"Belgium",
    "埃及":"Egypt", "沙特阿拉伯":"Saudi Arabia", "乌拉圭":"Uruguay",
    "伊朗":"Iran", "新西兰":"New Zealand", "法国":"France",
    "塞内加尔":"Senegal", "伊拉克":"Iraq", "挪威":"Norway",
    "阿根廷":"Argentina", "阿尔及利亚":"Algeria", "奥地利":"Austria",
    "约旦":"Jordan", "葡萄牙":"Portugal", "刚果(金)":"DR Congo",
    "刚果金":"DR Congo", "英格兰":"England", "克罗地亚":"Croatia",
    "加纳":"Ghana", "巴拿马":"Panama", "乌兹别克斯坦":"Uzbekistan",
    "哥伦比亚":"Colombia",
}

lines.append('')
lines.append('TEAM_NAME_MAP = {')
for cn, en in team_map.items():
    encoded_cn = ascii(cn)[1:-1]  # escape unicode
    lines.append(f'    "{cn}": "{en}",')
lines.append('}')

# Helper function stubs
lines.append('')
lines.append('def load_locked_data():')
lines.append("    path = os.path.join(BASE_DIR, 'data', 'locked_data.json')")
lines.append("    if os.path.exists(path):")
lines.append("        with open(path, 'r', encoding='utf-8') as f:")
lines.append("            return json.load(f)")
lines.append("    return {'matches': []}")
lines.append('')
lines.append('')
lines.append("print(f'Team mapping: {len(TEAM_NAME_MAP)} teams')")
lines.append("print('Script generated successfully')")

content = '\n'.join(lines)
output_path = 'D:/V3.3.3-Core/fetch_sofascore_data.py'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'Written: {len(lines)} lines -> {output_path}')
