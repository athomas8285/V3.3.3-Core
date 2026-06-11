import sys

path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 找到 L283 结束和 L284 开始之间的位置
# L283: "var dp=ys.split('-');yd=new Date(parseInt(dp[0]),parseInt(dp[1])-1,parseInt(dp[2]));}"
# L284: "var h=..."

marker = "parseInt(dp[2]));}"
filter_start = content.find(marker)
print(f"L283结束标记在: {filter_start}")

if filter_start >= 0:
    # 在此之后插入筛选逻辑
    filter_code = (
        "\n"
        "  // \u5e94\u7528\u7b5b\u9009\u5668\n"
        "  var FILTER_RV_HT={'003':'\u5e73\u80dc','004':'\u8d1f\u8d1f','005':'\u8d1f\u80dc','006':'\u8d1f\u5e73','007':'\u80dc\u80dc','008':'\u5e73\u80dc','009':'\u80dc\u80dc'};\n"
        "  yr=yr.filter(function(mx){\n"
        "    var g=gr(mx.rating||'',mx.fit_score||0);if(!FILTER_RV.rating[g])return false;\n"
        "    var ev=mx.event||'';if(!FILTER_RV_ALL_EVENTS&&ev&&!FILTER_RV.event[ev])return false;\n"
        "    if(!FILTER_RV.dir||!FILTER_RV.goals||!FILTER_RV.ht||!FILTER_RV.score){\n"
        "      var sc=mx.actual_score||'';\n"
        "      if(FILTER_RV.dir&&mx.hit!=='True')return false;\n"
        "      if(FILTER_RV.goals||FILTER_RV.ht||FILTER_RV.score){\n"
        "        var tg=0;if(sc.indexOf('-')>=0){var sp=sc.split('-');tg=parseInt(sp[0])+parseInt(sp[1]);}\n"
        "        var tgs=tg+'\u7403';\n"
        "        var tgsA=mx.top2_total_goals||[];\n"
        "        var htA=mx.top2_half_full||[];\n"
        "        var s3A=mx.top3_scores||[];\n"
        "        if(FILTER_RV.goals&&tgsA.indexOf(tgs)<0)return false;\n"
        "        if(FILTER_RV.ht){var ah=FILTER_RV_HT[mx.id]||'';if(!ah||htA.indexOf(ah)<0)return false;}\n"
        "        if(FILTER_RV.score&&s3A.indexOf(sc)<0)return false;\n"
        "      }\n"
        "    }\n"
        "    return true;\n"
        "  });\n"
    )
    
    content = content[:filter_start+len(marker)] + filter_code + content[filter_start+len(marker):]
    print("筛选逻辑已插入!")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("保存成功!")
else:
    print("标记未找到!")