with open("index.html","r",encoding="utf-8") as f:
    c=f.read()

# 1. Add CSS
css = "\n.sp-g-tl{margin-bottom:22px}.sp-g-tl>.sp-g-h{font-size:16px;padding:10px 12px;background:var(--surface-2);border-bottom:1px solid var(--bd);margin-bottom:0}.sp-g-tl>.sp-g-h::after{right:12px;top:11px}\n.sp-g-tl>.sp-g-c{padding:6px 12px}\n.sp-g-tl>.sp-g-c>.sp-g{margin-bottom:14px}\n.sp-g-tl>.sp-g-c>.meth{margin-bottom:16px;padding-bottom:0;border:none}\n.sp-g-tl>.sp-g-c>.meth .meth-p{font-size:12px}\n"
c = c.replace("</style>", css + "</style>", 1)

# 2. Remove left panel HTML (sp-l-wrap + sp-l + content)
left_start = c.find('<div class="sp-l-wrap"')
left_end = c.find('<div class="sp-wrap"', left_start)
c = c[:left_start] + c[left_end:]
print("Step 2: Removed left panel HTML")

# 3. Change button text and panel header
c = c.replace('<button class="sp-btn">\u53c2\u6570\u8bf4\u660e</button>', '<button class="sp-btn">\u5206\u6790\u6846\u67b6</button>')
c = c.replace('<h2>\u6846\u67b6\u53c2\u6570\u8bf4\u660e</h2>', '<h2>V3.3.3-Core \u5206\u6790\u6846\u67b6</h2>')
print("Step 3: Changed button and header")

# 4. Replace sp-bd content with merged structure
bd_start = c.find('<div class="sp-bd">') + len('<div class="sp-bd">')
bd_end = c.find('<script', bd_start)
bd_content = c[bd_start:bd_end].strip()

# Build the new merged sp-bd content
system = '<div class="meth"><div class="meth-h">\u5206\u6790\u7cfb\u7edf\u4ecb\u7ecd</div><div class="meth-p">V3.3.3-Core \u662f\u4e00\u5957\u5b8c\u6574\u7684\u8db3\u7403\u6bd4\u8d5b\u9884\u6d4b\u4e0e\u5206\u6790\u6846\u67b6\uff0c\u8986\u76d6\u4ece\u6570\u636e\u91c7\u96c6\u3001\u6a21\u578b\u8fd0\u7b97\u5230\u8d5b\u540e\u590d\u76d8\u7684\u5168\u6d41\u7a0b\u3002\u7cfb\u7edf\u57fa\u4e8e\u6cfd\u677e\u5206\u5e03\u5efa\u6a21\uff0c\u901a\u8fc7\u8499\u7279\u5361\u6d1b\u6a21\u62df\uff082000\u6b21/\u573a\uff09\u8ba1\u7b97\u80dc\u5e73\u8d1f\u6982\u7387\uff0c\u5f15\u5165DDI\uff08\u76d8\u53e3\u504f\u5dee\u6307\u6570\uff09\u6821\u51c6\u5e02\u573a\u70ed\u5ea6\u504f\u5dee\uff0c\u5e76\u53e0\u52a0\u591a\u7ef4\u5ea6\u56e0\u5b50\u4fee\u6b63\uff1a</div><div class="meth-p" style="margin-top:6px">- <b>\u4f24\u505c\u56e0\u5b50</b> \u2014 \u6838\u5fc3\u7403\u5458\u7f3a\u9635\u5bf9\u653b\u9632\u80fd\u529b\u7684\u91cf\u5316\u5f71\u54cd\uff0c\u533a\u5206\u6838\u5fc3\uff08+-20%\uff09\u4e0e\u8f6e\u6362\uff08+-5%\uff09\u4e24\u4e2a\u5c42\u7ea7</div><div class="meth-p">- <b>\u6218\u610f\u56e0\u5b50</b> \u2014 \u4fdd\u7ea7\u3001\u4e89\u51a0\u3001\u5fb7\u6bd4\u7b49\u573a\u666f\u4e0b\u7684\u6218\u610f\u4fee\u6b63\uff0c\u51b3\u8d5b\u671f+-5%\uff0c\u5e38\u89c4\u671f+-15%</div><div class="meth-p">- <b>\u677e\u61c8\u6263\u51cf</b> \u2014 \u5df2\u4fdd\u7ea7/\u5df2\u51fa\u7ebf\u7403\u961f\u7684lambda\u964d8%</div><div class="meth-p">- <b>\u9ad8\u539f\u52a0\u6210</b> \u2014 \u6d77\u62d4>2500m\u4e3b\u573a\u4f18\u52bf\u52a0\u621015%</div><div class="meth-p" style="margin-top:6px">\u6700\u7ec8\u8f93\u51fa\u63a8\u8350\u65b9\u5411\u3001\u9002\u914d\u5ea6\u8bc4\u5206\uff080-10\uff09\u548c\u7f6e\u4fe1\u7b49\u7ea7\uff08S/A/B/C\uff09\uff0c\u517c\u987e\u6570\u636e\u9762\u4e0e\u5e02\u573a\u60c5\u7eea\u7684\u53cc\u91cd\u89c6\u89d2\u3002</div></div>\n      <div class="meth"><div class="meth-h">\u6838\u5fc3\u903b\u8f91</div><div class="meth-p">\u57fa\u4e8e\u6cfd\u677e\u5206\u5e03\u7684\u8fdb\u7403\u671f\u671b\u6a21\u578b\uff08lambda\uff09\uff0c\u901a\u8fc7\u8499\u7279\u5361\u6d1b\u6a21\u62df\uff082000\u6b21/\u573a\uff09\u751f\u6210\u80dc\u5e73\u8d1f\u6982\u7387\u5206\u5e03\u3002\u7ed3\u5408DDI\uff08\u76d8\u53e3\u504f\u5dee\u6307\u6570\uff09\u6821\u51c6\u4e0e\u56e0\u5b50\u4fee\u6b63\u7cfb\u7edf\uff0c\u8f93\u51fa\u63a8\u8350\u65b9\u5411\u4e0e\u9002\u914d\u5ea6\u8bc4\u5206\u3002</div></div>\n      <div class="meth"><div class="meth-h">Lambda \u8ba1\u7b97</div><div class="meth-p">\u4ece\u7ade\u5f69SP\u53cd\u63a8\u5e02\u573a\u9690\u54b8lambda\uff0c\u4e0e\u57fa\u4e8exG/\u5b9e\u9645\u8fdb\u7403\u7684\u7269\u7406lambda\u8fdb\u884c\u4ea4\u53c9\u9a8c\u8bc1\u3002\u6700\u7ec8lambda\u5728\u4e24\u8005\u4e4b\u95f4\u52a0\u6743\u5e73\u8861\uff0c\u517c\u987e\u5e02\u573a\u9884\u671f\u4e0e\u57fa\u672c\u9762\u5b9e\u529b\u3002</div></div>\n      <div class="meth"><div class="meth-h">DDI \u6821\u51c6</div><div class="meth-p">DDI = P(\u7269\u7406) - P(\u5e02\u573a)\uff0c\u8861\u91cf\u6a21\u578b\u4e0e\u5e02\u573a\u4e4b\u95f4\u7684\u504f\u5dee\u3002|DDI| > 0.08 \u65f6\u89e6\u53d1\u6821\u51c6\uff0c\u65b9\u5411\u4e0e\u5e02\u573a\u70ed\u5ea6\u76f8\u53cd\u65f6\u964d\u7ea7\u5904\u7406\u3002\u6821\u51c6\u5e45\u5ea6\u4e0d\u8d85\u8fc70.05\uff0c\u9632\u6b62\u8fc7\u5ea6\u4fee\u6b63\u3002</div></div>\n      <div class="meth"><div class="meth-h">\u56e0\u5b50\u4fee\u6b63</div><div class="meth-p">\u4f24\u75c5\u5f71\u54cd\uff08\u6838\u5fc3+-20%\uff0c\u8f6e\u6362+-5%\uff09\u3001\u6218\u610f\u4fee\u6b63\uff08\u51b3\u8d5b\u671f+-5%\uff0c\u5e38\u89c4\u671f+-15%\uff09\u3001\u677e\u61c8\u6263\u51cf\uff088%\uff09\u3001\u9ad8\u539f\u52a0\u6210\uff0815%\uff09\u3002\u591a\u56e0\u5b50\u53e0\u52a0\u540e\u91cd\u65b0\u5f52\u4e00\u5316lambda\u3002</div></div>\n      <div class="meth"><div class="meth-h">\u98ce\u63a7\u964d\u7ea7</div><div class="meth-p">\u6df1\u76d8\uff08AH>=2.0\uff09\u81ea\u52a8\u964d\u7ea71\u7ea7\uff1b\u4e2d\u76d8\uff081.0<=AH<=1.25\uff09\u4e14lambda\u5dee<0.5\u989d\u5916\u964d\u7ea7\uff1b\u9002\u914d\u5ea6<4.0\u89e6\u53d1\u7194\u65ad\uff0c\u6807\u8bb0\u4e3aC\u7ea7\u3002</div></div>\n      <div style="margin-top:20px;padding-top:16px;border-top:2px solid var(--bd)"><div class="meth-h">\u7248\u672c\u66f4\u65b0</div>\n        <div class="v-item"><span class="v-ver">Rev1.13</span><span class="v-date">2026-05-31</span><div class="v-msg">DDI\u632f\u5e45\u6bd4\u4f8b\u53c2\u6570\u5316\uff1b\u5ba2\u9635\u51b7\u5904\u7406\u673a\u5236\uff1bLambda\u5f52\u4e00\u5316\u91cd\u7b97\u903b\u8f91\u4f18\u5316\uff1b\u81ea\u9002\u5e94\u8bc4\u5206\u533a\u95f4\u3002</div></div>\n        <div class="v-item"><span class="v-ver">Rev1.12</span><span class="v-date">2026-05-28</span><div class="v-msg">\u65b0\u589e\u6570\u636e\u7f3a\u5931\u6807\u8bb0\u7cfb\u7edf\uff1b\u8499\u7279\u5361\u6d1b\u6a21\u62df\u6b21\u6570\u4ece1000\u63d0\u5347\u81f32000\uff1b\u534a\u5168\u573a\u9884\u6d4b\u903b\u8f91\u4fee\u6b63\u3002</div></div>\n        <div class="v-item"><span class="v-ver">Rev1.11</span><span class="v-date">2026-05-25</span><div class="v-msg">\u591a\u56e0\u5b50\u53e0\u52a0\u5f52\u4e00\u5316\uff1b\u6218\u610f\u4fee\u6b63\u4e0e\u4f24\u75c5\u56e0\u5b50\u72ec\u7acb\u8bc4\u4f30\uff1b\u98ce\u63a7\u964d\u7ea7\u6a21\u578b\u91cd\u6784\u3002</div></div>\n        <div class="v-item"><span class="v-ver">Rev1.10</span><span class="v-date">2026-05-20</span><div class="v-msg">\u521d\u59cb\u7248\u672c\uff1a\u6cfd\u677elambda\u6a21\u578b + \u8499\u7279\u5361\u6d1b\u6a21\u62df + DDI\u6821\u51c6 + \u57fa\u7840\u56e0\u5b50\u4fee\u6b63\u3002</div></div>\n      </div>'

new_bd = '<div class="sp-bd">\n'
new_bd += '  <div class="sp-g sp-g-tl">\n'
new_bd += '    <div class="sp-g-h">V3.3.3-Core \u5206\u6790\u6846\u67b6</div>\n'
new_bd += '    <div class="sp-g-c">\n      ' + system + '\n    </div>\n'
new_bd += '  </div>\n'
new_bd += '  <div class="sp-g sp-g-tl">\n'
new_bd += '    <div class="sp-g-h">\u6846\u67b6\u53c2\u6570\u8bf4\u660e</div>\n'
new_bd += '    <div class="sp-g-c">\n' + bd_content + '\n    </div>\n'
new_bd += '  </div>\n'
new_bd += '</div>\n'

c = c[:bd_start] + new_bd + c[bd_end:]
print("Step 4: Replaced sp-bd content")

# 5. Update spWrap JS - find and replace the OLD JS block with NEW one
old_js_marker = "var wrap = document.getElementById('spWrap')"
old_js_start = c.find(old_js_marker)
if old_js_start > 0:
    # Find the start of the IIFE that contains this
    iife_start = c.rfind("(function()", 0, old_js_start)
    # Find the closing })(); 
    iife_end = c.find("})();", old_js_start) + len("})();")
    
    new_js = '''<script>
(function(){
  var w=document.getElementById('spWrap'),p=document.getElementById('spPanel'),t,o=false;
  w.addEventListener('mouseenter',function(){clearTimeout(t);p.classList.add('open');});
  w.addEventListener('mouseleave',function(){t=setTimeout(function(){p.classList.remove('open');},100);});
  p.addEventListener('mouseenter',function(){clearTimeout(t);p.classList.add('open');});
  p.addEventListener('mouseleave',function(){t=setTimeout(function(){p.classList.remove('open');},100);});
  w.querySelector('button').addEventListener('click',function(e){e.stopPropagation();o=!o;p.classList.toggle('open',o);clearTimeout(t);});
  document.addEventListener('click',function(e){if(!p.contains(e.target)&&!w.contains(e.target)&&o){o=false;p.classList.remove('open');}});
})();
</script>'''
    c = c[:iife_start] + new_js + c[iife_end:]
    print("Step 5: Updated spWrap JS (old -> new)")
else:
    print("Step 5: WARNING - old spWrap JS not found!")

# 6. Update panel width
c = c.replace("width:380px", "width:420px")
c = c.replace("right:-380px", "right:-420px")
print("Step 6: Updated panel width")

# 7. Remove spLWrap JS block
lw_marker = "var wrap = document.getElementById('spLWrap')"
lw_start = c.find(lw_marker)
if lw_start > 0:
    iife_start = c.rfind("(function()", 0, lw_start)
    iife_end = c.find("})();", lw_start) + len("})();")
    c = c[:iife_start] + c[iife_end:]
    print("Step 7: Removed spLWrap JS")

with open("index.html","w",encoding="utf-8") as f:
    f.write(c)
print("DONE")