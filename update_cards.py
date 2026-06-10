with open("D:/V3.3.3-Core/templates/index.html","r",encoding="utf-8-sig") as f:
    c = f.read()

# Update the loadWCSchedule function to show venue + round
old_card_start = 'html+=\'<div class="wc-card"'
old_card_end = '</div></div>\';'

# Find the card rendering section and replace it
# Instead of complex regex, find the card rendering code and replace it
old_render = """        html+='<div class="wc-card" style="background:rgba(16,22,42,.78);border:1px solid rgba(255,255,255,.06);border-radius:8px;padding:10px 14px;margin-bottom:6px">';
        html+='<div style="display:flex;align-items:center;gap:8px;justify-content:space-between;flex-wrap:wrap">';
        html+='<div style="display:flex;align-items:center;gap:6px"><span style="font-size:11px;color:var(--t3);font-family:var(--mono);min-width:36px">'+timeStr+'</span>'+gb+'</div>';
        html+=oh;
        html+='</div>';
        html+='<div style="display:flex;align-items:center;justify-content:center;gap:10px;margin-top:6px">';
        html+='<div style="display:flex;align-items:center;gap:4px;flex:1;justify-content:flex-end"><span style="font-size:16px">'+(m.home_flag||"")+'</span><span style="font-size:14px;font-weight:700;color:var(--t1)">'+m.home+'</span></div>';
        html+='<span style="font-size:11px;color:var(--t3);font-weight:600">VS</span>';
        html+='<div style="display:flex;align-items:center;gap:4px;flex:1;justify-content:flex-start"><span style="font-size:14px;font-weight:700;color:var(--t1)">'+m.away+'</span><span style="font-size:16px">'+(m.away_flag||"")+'</span></div>';
        html+='</div></div>';"""

new_render = """        var rndText="第"+m.round+"轮";
        var venueText=m.venue||"";
        html+='<div class="wc-card" style="background:rgba(16,22,42,.78);border:1px solid rgba(255,255,255,.06);border-radius:8px;padding:10px 14px;margin-bottom:6px">';
        html+='<div style="display:flex;align-items:center;gap:6px;justify-content:space-between;flex-wrap:wrap">';
        html+='<div style="display:flex;align-items:center;gap:4px"><span style="font-size:10px;color:var(--t3);font-family:var(--mono);background:rgba(255,255,255,.04);padding:1px 5px;border-radius:3px">'+timeStr+'</span>'+gb;
        html+='<span style="font-size:10px;color:var(--t3);background:rgba(0,229,255,.06);padding:1px 5px;border-radius:3px">'+rndText+'</span></div>';
        html+=oh;
        html+='</div>';
        html+='<div style="display:flex;align-items:center;justify-content:center;gap:10px;margin-top:6px">';
        html+='<div style="display:flex;align-items:center;gap:4px;flex:1;justify-content:flex-end"><span style="font-size:16px">'+(m.home_flag||"")+'</span><span style="font-size:14px;font-weight:700;color:var(--t1)">'+m.home+'</span></div>';
        html+='<span style="font-size:11px;color:var(--t3);font-weight:600">VS</span>';
        html+='<div style="display:flex;align-items:center;gap:4px;flex:1;justify-content:flex-start"><span style="font-size:14px;font-weight:700;color:var(--t1)">'+m.away+'</span><span style="font-size:16px">'+(m.away_flag||"")+'</span></div>';
        html+='</div>';
        html+='<div style="font-size:10px;color:var(--t3);text-align:center;margin-top:4px">'+venueText+'</div>';
        html+='</div>';"""

if old_render in c:
    c = c.replace(old_render, new_render)
    with open("D:/V3.3.3-Core/templates/index.html","w",encoding="utf-8") as f:
        f.write(c)
    print("Updated card rendering with venue + round")
else:
    print("FAIL: old render pattern not found!")
    idx = c.find("html+='<div class=\"wc-card\"")
    if idx >= 0:
        print(f"Found at {idx}, context: {c[idx:idx+500]}")
