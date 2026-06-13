with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find the old completed section in renderFromWC
old_completed = '''      if(isCompleted){
        var hitStr = m.hit ? '✅命中' : '❌未中';
        var hitColor = m.hit ? '#00e676' : '#ef5350';
        h += '<div class=\"ana-card-result\"><span class=\"result-badge\" style=\"background:' + hitColor + '22;border:1px solid ' + hitColor + '44;color:' + hitColor + ';\">' + m.result + '</span><span class=\"hit-badge\" style=\"color:' + hitColor + ';\">' + hitStr + '</span></div>';
        h += '<div class=\"ana-card-odds\"><div class=\"odds-group\"><span class=\"og-item\" style=\"color:var(--t3);font-size:11px;\">已完赛</span></div></div>';
      } else if(isPredictable){'''

new_completed = '''      if(isCompleted){
        var _dirWC = m.dir || '';
        var _dirColorWC = _dirWC.indexOf('胜') >= 0 ? '#4ade80' : (_dirWC.indexOf('负') >= 0 ? '#ef4444' : '#fbbf24');
        var _rhfWC = m.half_full || '--';
        var _rhitWC = m.hit === true;
        var _rhcWC = _rhitWC ? '#22c55e' : '#ef4444';
        var _rhtxtWC = _rhitWC ? '命中' : '偏离';
        h += '<div class=\"ana-card-odds\" style=\"gap:16px;\">';
        if(_dirWC){
          h += '<div class=\"odds-group\" style=\"background:'+_dirColorWC+'22;border:1px solid '+_dirColorWC+'44;\">';
          h += '<span class=\"og-item\" style=\"color:'+_dirColorWC+';font-size:13px;font-weight:700;\">'+_dirWC+'</span></div>';
        }
        h += '<div class=\"odds-group\" style=\"background:rgba(251,191,36,.12);border:1px solid rgba(251,191,36,.25);gap:8px;padding:3px 12px;\">';
        h += '<span class=\"og-item\" style=\"color:#fbbf24;font-size:16px;font-weight:800;\">'+m.result+'</span>';
        h += '<span class=\"og-item\" style=\"color:var(--t2);font-size:12px;font-weight:600;\">'+_rhfWC+'</span></div>';
        h += '<span style=\"display:flex;align-items:center;gap:4px;margin-left:8px;\">';
        h += '<span class=\"og-item\" style=\"color:'+_rhcWC+';font-weight:700;font-size:13px;background:'+_rhcWC+'22;border:1px solid '+_rhcWC+'44;border-radius:4px;padding:0 8px;\">'+_rhtxtWC+'</span>';
        h += '<span style=\"font-size:12px;color:#64748b;\">▼</span></span></div>';
      } else if(isPredictable){'''

count = html.count(old_completed)
print(f"Found {count} occurrences")

if count > 0:
    html = html.replace(old_completed, new_completed)
    with open("D:\\V3.3.3-Core\\templates\\index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Replaced completed card layout in renderFromWC!")
else:
    # Check what we're matching against
    idx = html.find('isCompleted){')
    while idx >= 0:
        ctx = html[idx:idx+500]
        if 'hitStr' in ctx and 'm.hit ?' in ctx:
            with open("_found_completed.txt", "w", encoding="utf-8") as out:
                out.write(ctx)
            print(f"Found at {idx}")
            break
        idx = html.find('isCompleted){', idx+1)
    else:
        print("Not found!")