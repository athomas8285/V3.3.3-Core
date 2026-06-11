path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 更新筛选逻辑，加入类型保护（处理字符串JSON和数组两种情况）
old_filter = """        var tgsA=mx.top2_total_goals||[];
        var htA=mx.top2_half_full||[];
        var s3A=mx.top3_scores||[];"""

new_filter = """        var tgsA=mx.top2_total_goals||[];if(typeof tgsA==='string'){try{tgsA=JSON.parse(tgsA)}catch(e){tgsA=[]}}
        var htA=mx.top2_half_full||[];if(typeof htA==='string'){try{htA=JSON.parse(htA)}catch(e){htA=[]}}
        var s3A=mx.top3_scores||[];if(typeof s3A==='string'){try{s3A=JSON.parse(s3A)}catch(e){s3A=[]}}"""

if old_filter in content:
    content = content.replace(old_filter, new_filter)
    print("类型保护已添加!")
else:
    print("未找到原内容！")
    idx = content.find("tgsA=mx.top2_total_goals")
    if idx >= 0:
        print(f"  在位置 {idx}: {content[idx-20:idx+50]}")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("完成!")