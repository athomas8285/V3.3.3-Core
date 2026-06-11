import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace TEAM_FLAGS block with PNG-based mapping + flagImg helper
old_flags_block = """// 球队国旗映射
var TEAM_FLAGS = {"""

# Find where TEAM_FLAGS starts
idx = content.find("// 球队国旗映射")
if idx < 0:
    print("ERROR: TEAM_FLAGS not found")
    sys.exit(1)

# Find end of TEAM_FLAGS block (the }; line)
end_idx = content.find("};", idx)
# Find the newline after };
end_line = content.find("\n", end_idx)

new_flags = """// 球队国旗映射（本地 PNG）
var TEAM_FLAGS = {
  "墨西哥":"/static/flags/mexico.png","南非":"/static/flags/south_africa.png","韩国":"/static/flags/korea.png","捷克":"/static/flags/czech.png",
  "加拿大":"/static/flags/canada.png","波黑":"/static/flags/bosnia.png","美国":"/static/flags/usa.png","巴拉圭":"/static/flags/paraguay.png",
  "卡塔尔":"/static/flags/qatar.png","瑞士":"/static/flags/switzerland.png","巴西":"/static/flags/brazil.png","摩洛哥":"/static/flags/morocco.png",
  "海地":"/static/flags/haiti.png","苏格兰":"/static/flags/scotland.png","奥大利亚":"/static/flags/australia.png","土耳其":"/static/flags/turkey.png",
  "德国":"/static/flags/germany.png","库拉索":"/static/flags/curacao.png","荷兰":"/static/flags/netherlands.png","日本":"/static/flags/japan.png",
  "科特迪瓦":"/static/flags/ivory_coast.png","厄瓜多尔":"/static/flags/ecuador.png","瑞典":"/static/flags/sweden.png","突尼斯":"/static/flags/tunisia.png",
  "西班牙":"/static/flags/spain.png","佛得角":"/static/flags/cape_verde.png","比利时":"/static/flags/belgium.png","埃及":"/static/flags/egypt.png",
  "沙特":"/static/flags/saudi.png","乌拉圭":"/static/flags/uruguay.png","伊朗":"/static/flags/iran.png","新西兰":"/static/flags/new_zealand.png",
  "法国":"/static/flags/france.png","塞内加尔":"/static/flags/senegal.png","伊拉克":"/static/flags/iraq.png","挪威":"/static/flags/norway.png",
  "阿根廷":"/static/flags/argentina.png","阿尔及利亚":"/static/flags/algeria.png","奥地利":"/static/flags/austria.png","约旦":"/static/flags/jordan.png",
  "葡萄牙":"/static/flags/portugal.png","民主刚果":"/static/flags/dr_congo.png","英格兰":"/static/flags/england.png","克罗地亚":"/static/flags/croatia.png",
  "加纳":"/static/flags/ghana.png","巴拿马":"/static/flags/panama.png","乌兹别克斯坦":"/static/flags/uzbekistan.png","哥伦比亚":"/static/flags/colombia.png"
};
function flagImg(name){
  var p = TEAM_FLAGS[name];
  return p ? '<img class="tf" src="' + p + '"> ' : '';
}"""

# Replace the block
content = content[:idx] + new_flags + content[end_line+1:]

# 2. Update renderTodayMatches - replace hFlag/aFlag usage
# Change from: hFlag + ' ' + m.h  to: flagImg(m.h) + m.h
content = content.replace(
    "h += '<span class=\"htc-team\">' + hFlag + ' ' + m.h + '</span>';",
    "h += '<span class=\"htc-team\">' + flagImg(m.h) + m.h + '</span>';"
)
content = content.replace(
    "h += '<span class=\"htc-team\">' + aFlag + ' ' + m.a + '</span>';",
    "h += '<span class=\"htc-team\">' + flagImg(m.a) + m.a + '</span>';"
)

# Remove the hFlag/aFlag lines (no longer needed since we use flagImg directly)
content = content.replace(
    "    var hFlag = TEAM_FLAGS[m.h] || \"\";\n    var aFlag = TEAM_FLAGS[m.a] || \"\";\n",
    ""
)

# 3. Add flags to calendar day cell (line 935)
old_cday = 'h += \'<div class="cday-match"><span class="cdm-time">\' + mt.t.slice(0,5) + \'</span>\' + mt.h.slice(0,4) + \' vs \' + mt.a.slice(0,4) + \'</div>\';'
new_cday = 'h += \'<div class="cday-match"><span class="cdm-time">\' + mt.t.slice(0,5) + \'</span>\' + flagImg(mt.h) + mt.h.slice(0,4) + \' vs \' + flagImg(mt.a) + mt.a.slice(0,4) + \'</div>\';'
if old_cday in content:
    content = content.replace(old_cday, new_cday)
    print("Calendar day cell flag OK")
else:
    print("WARNING: Calendar day cell pattern not found!")

# 4. Add flags to day modal (lines 1013-1015)
content = content.replace(
    "h += '<span class=\"mm-home\">' + m.h + '</span>';",
    "h += '<span class=\"mm-home\">' + flagImg(m.h) + m.h + '</span>';"
)
content = content.replace(
    "h += '<span class=\"mm-away\">' + m.a + '</span>';",
    "h += '<span class=\"mm-away\">' + flagImg(m.a) + m.a + '</span>';"
)

# 5. Add CSS for flag images
css_insert = '.tf{width:20px;height:20px;border-radius:50%;vertical-align:middle;margin-right:4px;object-fit:cover;flex-shrink:0}\n'
# Insert after the closing } of the media query section, before .wc-date-group
insert_pos = content.find("/* WC group schedule */")
if insert_pos > 0:
    content = content[:insert_pos] + css_insert + content[insert_pos:]
    print("CSS inserted")
else:
    print("WARNING: CSS insertion point not found")

with open("D:\\V3.3.3-Core\\templates\\index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Done! File updated.")
