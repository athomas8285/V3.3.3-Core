path = r"C:\Users\gjj\Desktop\v333\templates\index.html"

# The original CSS (from the first version of the file before any modifications)
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#f5f4ed;--surface:#faf9f5;--surface-h:#f0efe8;--surface-2:#ebe9e2;--ink:#1B365D;--ink-l:#2D5A8A;--bd:#e8e6dc;--bd-h:#dbd9ce;--t1:#141413;--t2:#504e49;--t3:#6b6a64;--green:#4a7a5a;--amber:#b8943a;--red:#b05a5a;--mono:'SF Mono','Cascadia Code','Consolas','Monaco',monospace;--sans:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Noto Serif SC','Georgia',serif}
body{font-family:var(--sans);background:var(--bg);color:var(--t1);min-height:100vh;-webkit-font-smoothing:antialiased}
.app{max-width:1040px;margin:0 auto;padding:36px 24px 60px;position:relative;z-index:1}
hdr{margin-bottom:24px;padding-bottom:18px;border-bottom:1px solid var(--bd);text-align:center}
.h1{font-size:34px;font-weight:700;color:var(--ink);letter-spacing:3px;line-height:1.3;margin-bottom:6px}
.h1 small{font-size:14px;font-weight:400;color:var(--t3);letter-spacing:1px;margin-left:10px}
.hr1{display:flex;align-items:center;justify-content:center;gap:16px;margin-bottom:6px;flex-wrap:wrap}
.hdate{font-size:12px;color:var(--t2);font-weight:500}
.hdate em{font-style:normal;color:var(--t3);font-weight:400;margin-left:6px}
.stats{display:flex;gap:10px;font-size:10px;color:var(--t3)}
.stats b{font-family:var(--mono);color:var(--t2);font-weight:500;font-size:11px;margin-left:2px}
.rd{display:flex;height:4px;border-radius:2px;overflow:hidden;gap:1px;margin-top:8px;background:var(--bd)}
.rd div{height:100%;border-radius:1px;transition:width 0.3s}
.sec{margin:28px 0 16px;display:flex;align-items:center;gap:10px}
.sec-h{font-size:14px;color:var(--ink);font-weight:700;letter-spacing:1.5px}
.sec-l{flex:1;height:1px;background:var(--bd)}
.sec-dot{width:5px;height:5px;border-radius:50%;background:var(--ink)}
.card{background:var(--surface);border:1px solid var(--bd);border-radius:6px;overflow:hidden;cursor:pointer;transition:border-color 0.2s,box-shadow 0.2s,background 0.2s}
.card::before{content:"";display:block;height:2px;transition:opacity 0.15s}
.card.rt-s::before{background:var(--ink);opacity:0.5}
.card.rt-a::before{background:var(--amber);opacity:0.5}
.card.rt-b::before{background:var(--green);opacity:0.4}
.card.rt-c::before{background:var(--t3);opacity:0.3}
.card:hover{background:var(--surface-h);border-color:var(--bd-h);box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.card.rt-hit{background:#fef0ee}
.card.rt-hit:hover{background:#fce8e5}
.card.rt-hit .cd{background:#fce8e5}
.card.rt-miss{background:#f3f2ee}
.card.rt-miss:hover{background:#ebeae5}
.card.rt-miss .cd{background:#ebeae5}
.card:hover::before{opacity:1}
.card+.card{margin-top:0;border-top:none}
.card.expanded{border-color:var(--ink-l);box-shadow:0 0 0 1px var(--ink-l)}
.thr{display:flex;align-items:center;padding:10px 14px;font-size:15px;color:var(--ink);font-weight:700;letter-spacing:0.3px;border-bottom:2px solid var(--ink);background:var(--surface-2);text-transform:uppercase}
.thr span:first-child{width:75px;text-align:center;white-space:nowrap}.thr span:nth-child(2){width:110px;text-align:center;white-space:nowrap}.thr span:nth-child(3){width:320px;white-space:nowrap}.thr span:nth-child(4){width:65px;text-align:center;white-space:nowrap}.thr span:nth-child(5){width:100px;text-align:center;white-space:nowrap}.thr span:nth-child(6){width:100px;text-align:center;white-space:nowrap}.thr span:nth-child(7){width:100px;text-align:center;white-space:nowrap}.thr span:last-child{width:110px;text-align:right;padding-right:28px;white-space:nowrap}
.cg2{display:flex;align-items:center;padding:10px 14px;gap:0}
.c2-col{white-space:nowrap}.c2-id{width:75px;text-align:center;font-family:var(--mono);font-size:15px;color:var(--t3)}.c2-tm{width:110px;text-align:center;font-family:var(--mono);font-size:15px;color:var(--t3)}.c2-mm{width:320px;min-width:0}.c2-dr{width:65px;text-align:center;font-weight:600;font-size:15px}.c2-dr .dir{font-size:15px;color:var(--t1)}.c2-g{width:100px;text-align:center;font-family:var(--mono);font-size:13px;color:var(--t2)}.c2-ht{width:100px;text-align:center;font-family:var(--mono);font-size:13px;color:var(--t2)}.c2-scr{width:100px;text-align:center;font-family:var(--mono);font-size:13px;color:var(--t2)}.c2-r{width:110px;text-align:right;display:flex;align-items:center;justify-content:flex-end;gap:4px;padding-right:14px}
.cg2b{padding:0 14px 10px;display:flex;flex-wrap:wrap;align-items:center;gap:8px 32px}
.c2-mm{display:flex;align-items:center;gap:6px;white-space:nowrap}
.c2-h,.c2-a{font-weight:600;font-size:15px;color:var(--t1)}.c2-v{color:var(--t3);font-size:11px;margin:0 6px}
.tag2{font-size:10px;color:var(--t3);background:var(--surface-2);padding:1px 6px;border-radius:3px;line-height:1.4;margin-left:4px}
.c2-r{display:flex;align-items:center;gap:6px;margin-left:auto;white-space:nowrap}
.c-sc2{font-family:var(--mono);font-size:15px;font-weight:600;color:var(--ink)}
.c2-s{display:flex;align-items:center;gap:13px;flex-wrap:wrap;font-size:11px}
.c2-s .cs-l{font-size:13px;color:var(--t3);font-weight:700;letter-spacing:0.3px;text-transform:uppercase}
.c2-s .cs-l.cs-l-lg{font-size:15px;font-family:Georgia,'Times New Roman',serif;vertical-align:middle}.c2-s .cs-v{font-family:var(--mono);color:var(--t2);font-size:11px;font-weight:500}
.c2-s .cs-v.hot{color:var(--red)}.c2-s .cs-v.ok{color:var(--green)}.c2-s .cs-v.warn{color:var(--amber)}
.c2-sp{color:var(--bd);margin:0 4px;font-size:10px;opacity:0.5}
.prob2{display:flex;align-items:center;gap:10px;min-width:500px}
.prob2 .prob-b{flex:1;height:6px;border-radius:3px}
.prob2 .prob-n{font-family:var(--mono);font-size:10px;color:var(--t3);white-space:nowrap}
.cg{display:grid;grid-template-columns:1fr auto;gap:10px;padding:12px 16px}
.cl{min-width:0}.cr{text-align:right;display:flex;flex-direction:column;align-items:flex-end;gap:4px;padding-left:14px}
.c-t{display:flex;align-items:center;gap:8px;margin-bottom:3px}
.c-id{font-family:var(--mono);font-size:12px;color:var(--t3)}.c-ti{font-family:var(--mono);font-size:12px;color:var(--t3)}
.c-m{font-size:18px;font-weight:500;margin:3px 0 2px;letter-spacing:0.2px}
.c-m .vs{color:var(--t3);font-size:12px;font-weight:400;margin:0 8px}
.c-dr{display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap}
.dir{display:inline-flex;align-items:center;gap:4px;font-size:12px;font-weight:500;color:var(--t2)}
.dir i{width:4px;height:4px;border-radius:50%;display:inline-block;background:var(--ink)}
.dir-h{color:var(--green)}.dir-h i{background:var(--green)}
.dir-a{color:var(--red)}.dir-a i{background:var(--red)}
.dir-d{color:var(--amber)}.dir-d i{background:var(--amber)}
.tag{font-size:11px;color:var(--t3);background:var(--surface-2);padding:2px 6px;border-radius:3px}
.prob{display:flex;align-items:center;gap:10px;margin-bottom:9px}
.prob-b{flex:1;display:flex;height:4px;border-radius:2px;overflow:hidden;gap:1px;background:var(--bd)}
.prob-b div{height:100%;border-radius:1px;transition:width 0.2s}
.prob-n{font-family:var(--mono);font-size:11px;color:var(--t3);white-space:nowrap}
.cs{display:flex;flex-wrap:wrap;gap:2px;padding-top:8px;border-top:1px solid var(--bd)}
.cs-i{display:flex;align-items:baseline;gap:4px;padding:0 10px;border-right:1px solid var(--bd);font-size:10px}
.cs-i:first-child{padding-left:0}.cs-i:last-child{border:none;padding-right:0}
.cs-l{font-size:11px;color:var(--t3);font-weight:500;letter-spacing:0.3px;text-transform:uppercase}
.cs-v{font-family:var(--mono);color:var(--t1);font-size:13px;font-weight:500}
.cs-v.hot{color:var(--red)}.cs-v.ok{color:var(--green)}.cs-v.warn{color:var(--amber)}
.c-sc{font-family:var(--mono);font-size:24px;font-weight:600;color:var(--ink);line-height:1}
.badge{display:inline-block;padding:2px 8px;border-radius:3px;font-size:11px;font-weight:600;letter-spacing:0.3px}
.badge-s{background:#eef2f7;color:var(--ink)}.c-bdg2{display:inline-flex;vertical-align:middle}
.badge-a{background:#f5ede0;color:#b8943a}.badge-b{background:#eaf0ea;color:#4a7a5a}.badge-c{background:#f0efec;color:var(--t3)}
.cd{display:none;padding:12px 16px;border-top:1px solid var(--bd);background:var(--surface-2)}
.card.expanded .cd{display:block}
.charts-row{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:12px}
@media(max-width:640px){.charts-row{grid-template-columns:1fr}}
.cb{background:var(--surface);border:1px solid var(--bd);border-radius:6px;padding:10px}
.ct{font-size:11px;color:var(--t3);font-weight:600;letter-spacing:0.5px;text-transform:uppercase;margin-bottom:6px}
.ana{display:grid;grid-template-columns:1fr 1fr;gap:10px}@media(max-width:640px){.ana{grid-template-columns:1fr}}
.ana-i{border-radius:4px;font-size:13px;line-height:1.7;color:var(--t2);background:var(--surface);padding:8px 10px}
.ana-i.risk{background:#f5ecec;grid-column:1/-1}
.ana-l{font-size:11px;color:var(--t3);font-weight:600;letter-spacing:0.3px;text-transform:uppercase;display:block;margin-bottom:1px}
.ana-i.risk .ana-l{color:var(--red)}
.rv{border-radius:6px;overflow:hidden;border:1px solid var(--bd)}
.rv+.rv{margin-top:8px}.rv-in{padding:10px 14px;display:flex;align-items:center;gap:10px;background:var(--surface)}
.rv-d{font-family:var(--mono);font-size:10px;color:var(--t3);min-width:70px}
.rv-t{font-weight:500;font-size:13px}.rv-t small{font-weight:400;color:var(--t3);font-size:11px;margin:0 6px}
.rv-sc{font-family:var(--mono);font-size:12px;color:var(--t2);font-weight:500;margin-left:auto}
.rv-b{font-size:9px;padding:2px 6px;border-radius:3px;font-weight:500;white-space:nowrap}
.rv-hit{background:#eaf0ea;color:var(--green)}.rv-miss{background:#f5ecec;color:var(--red)}.rv-na{background:var(--surface-2);color:var(--t3)}
.rv-bf{display:none;padding:10px 14px;border-top:1px solid var(--bd);background:var(--surface-2);font-size:11px;line-height:1.7;color:var(--t2)}
.rv.expanded .rv-bf{display:block}.rv{cursor:pointer;transition:border-color 0.15s}.rv:hover{border-color:var(--bd-h)}
.sp-g-c{overflow:hidden;transition:max-height 0.25s ease}.sp-g-c:not(.open){max-height:0!important;padding-top:0!important}
.sp-g.expanded>.sp-g-h::after{transform:rotate(90deg)}.sp-g-c.open{max-height:800px}
.sp-l-wrap{position:fixed;left:0;top:50%;transform:translateY(-50%);z-index:100}
.sp-l-btn{writing-mode:vertical-lr;padding:32px 14px;font-size:15px;letter-spacing:4px;background:var(--surface);color:var(--ink);border:1px solid var(--bd);border-right:none;cursor:pointer;border-radius:0 6px 6px 0;font-family:var(--sans);font-weight:500;transition:background 0.2s}
.sp-l-btn:hover{background:var(--surface-h)}
.sp-l{position:fixed;left:-420px;top:0;width:420px;height:100vh;overflow-y:auto;background:var(--surface);border-right:1px solid var(--bd);transition:left 0.3s cubic-bezier(0.4,0,0.2,1);z-index:200;box-shadow:4px 0 24px rgba(0,0,0,0.08)}
.sp-l.open{left:0}
.sp-l-hdr{padding:20px 20px 14px;border-bottom:1px solid var(--bd)}.sp-l-hdr h2{font-size:20px;font-weight:700;color:var(--ink);letter-spacing:0.5px}
.sp-l-bd{padding:16px 20px}
.v-item{margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid var(--bd)}.v-item:last-child{border-bottom:none}
.v-ver{font-size:11px;font-weight:700;color:var(--ink);font-family:var(--mono)}.v-date{font-size:10px;color:var(--t3);margin-left:6px}
.v-msg{font-size:12px;color:var(--t2);line-height:1.6;margin-top:4px}
.meth{margin-bottom:14px}.meth-h{font-size:12px;font-weight:600;color:var(--ink);margin-bottom:4px;letter-spacing:0.3px}
.meth-p{font-size:11px;color:var(--t2);line-height:1.7}
.sp-wrap{position:fixed;right:0;top:50%;transform:translateY(-50%);z-index:100}
.sp-btn{writing-mode:vertical-lr;padding:32px 14px;font-size:15px;letter-spacing:4px;background:var(--ink);color:#f5f4ed;border:none;cursor:pointer;border-radius:6px 0 0 6px;font-family:var(--sans);font-weight:500;transition:background 0.2s}
.sp-btn:hover{background:var(--ink-l)}
.sp{position:fixed;right:-380px;top:0;width:380px;height:100vh;overflow-y:auto;background:var(--surface);border-left:1px solid var(--bd);transition:right 0.3s cubic-bezier(0.4,0,0.2,1);z-index:200;box-shadow:-4px 0 24px rgba(0,0,0,0.08)}
.sp.open{right:0}.sp-hdr{padding:20px 20px 14px;border-bottom:1px solid var(--bd)}.sp-hdr h2{font-size:20px;font-weight:700;color:var(--ink);letter-spacing:0.5px}
.sp-bd{padding:16px 20px}.sp-g{margin-bottom:18px}
.sp-g-h{font-size:14px;color:var(--ink);font-weight:600;letter-spacing:0.3px;cursor:pointer;padding:6px 0;border-bottom:1px solid var(--bd);position:relative;transition:color 0.15s;-webkit-user-select:none;user-select:none}
.sp-g-i{margin-bottom:8px;font-size:13px;line-height:1.7;padding-left:4px}
.sp-g-i .lk{color:var(--t2);font-weight:600;display:block;font-size:12px}
.sp-g-i .lv{color:var(--ink);font-family:var(--mono);font-size:12px;background:var(--surface-2);padding:1px 6px;border-radius:3px}
.sp-g-h::after{content:"\25B6";position:absolute;right:4px;top:7px;font-size:10px;color:var(--ink);transition:transform 0.2s ease}
.fl-pill.on{background:var(--ink)!important;color:#f5f4ed!important;border-color:var(--ink)!important}
.fl-pill:hover{border-color:var(--ink-l)!important}
.loading{text-align:center;padding:60px 0;color:var(--t3);font-size:12px}
.loading::after{content:"";display:block;width:16px;height:16px;border:2px solid var(--bd);border-top-color:var(--ink);border-radius:50%;margin:10px auto 0;animation:spin 0.6s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
"""

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>V3.3.3-Core\u5206\u6790\u7cfb\u7edf</title>
<style>
''' + CSS.strip() + '''
</style>
</head>
<body>
<div class="app">
  <hdr>
    <div class="h1">V3.3.3-Core\u5206\u6790\u7cfb\u7edf<small>\u626b\u76d8\u6570\u636e</small></div>
    <div class="hr1">
      <div class="hdate">2026.6.1 <em>\u626b\u76d8</em></div>
      <div class="stats" id="stats"></div>
    </div>
    <div class="rd" id="rd"></div>
  </hdr>
  <div id="r"><div class="loading">Loading</div></div>
  <div id="rv"></div>
</div>

<div class="sp-l-wrap" id="spLWrap">
  <button class="sp-l-btn">\u7cfb\u7edf\u8bf4\u660e</button>
</div>
<div class="sp-l" id="spLPanel">
  <div class="sp-l-hdr"><h2>V3.3.3-Core \u5206\u6790\u6846\u67b6</h2></div>
  <div class="sp-l-bd">
    <div class="meth">
      <div class="meth-h">\u5206\u6790\u7cfb\u7edf\u4ecb\u7ecd</div>
      <div class="meth-p">V3.3.3-Core \u662f\u4e00\u5957\u5b8c\u6574\u7684\u8db3\u7403\u6bd4\u8d5b\u9884\u6d4b\u4e0e\u5206\u6790\u6846\u67b6\uff0c\u8986\u76d6\u4ece\u6570\u636e\u91c7\u96c6\u3001\u6a21\u578b\u8fd0\u7b97\u5230\u8d5b\u540e\u590d\u76d8\u7684\u5168\u6d41\u7a0b\u3002\u7cfb\u7edf\u57fa\u4e8e\u6cca\u677e\u5206\u5e03\u5efa\u6a21\uff0c\u901a\u8fc7\u8499\u7279\u5361\u6d1b\u6a21\u62df\uff082000\u6b21/\u573a\uff09\u8ba1\u7b97\u80dc\u5e73\u8d1f\u6982\u7387\uff0c\u5f15\u5165DDI\uff08\u76d8\u53e3\u504f\u5dee\u6307\u6570\uff09\u6821\u51c6\u5e02\u573a\u70ed\u5ea6\u504f\u5dee\uff0c\u5e76\u53e0\u52a0\u591a\u7ef4\u5ea6\u56e0\u5b50\u4fee\u6b63\uff1a</div>
      <div class="meth-p" style="margin-top:6px">- <b>\u4f24\u505c\u56e0\u5b50</b> \u2014 \u6838\u5fc3\u7403\u5458\u7f3a\u9635\u5bf9\u653b\u9632\u80fd\u529b\u7684\u91cf\u5316\u5f71\u54cd\uff0c\u533a\u5206\u6838\u5fc3\uff08+-20%\uff09\u4e0e\u8f6e\u6362\uff08+-5%\uff09\u4e24\u4e2a\u5c42\u7ea7</div>
      <div class="meth-p">- <b>\u6218\u610f\u56e0\u5b50</b> \u2014 \u4fdd\u7ea7\u3001\u4e89\u51a0\u3001\u5fb7\u6bd4\u7b49\u573a\u666f\u4e0b\u7684\u6218\u610f\u4fee\u6b63\uff0c\u51b3\u8d5b\u671f+-5%\uff0c\u5e38\u89c4\u671f+-15%</div>
      <div class="meth-p">- <b>\u677e\u61c8\u6263\u51cf</b> \u2014 \u5df2\u4fdd\u7ea7/\u5df2\u51fa\u7ebf\u7403\u961f\u7684lambda\u964d8%</div>
      <div class="meth-p">- <b>\u9ad8\u539f\u52a0\u6210</b> \u2014 \u6d77\u62d4>2500m\u4e3b\u573a\u4f18\u52bf\u52a0\u621015%</div>
      <div class="meth-p" style="margin-top:6px">\u6700\u7ec8\u8f93\u51fa\u63a8\u8350\u65b9\u5411\u3001\u9002\u914d\u5ea6\u8bc4\u5206\uff080-10\uff09\u548c\u7f6e\u4fe1\u7b49\u7ea7\uff08S/A/B/C\uff09\uff0c\u517c\u987e\u6570\u636e\u9762\u4e0e\u5e02\u573a\u60c5\u7eea\u7684\u53cc\u91cd\u89c6\u89d2\u3002</div>
    </div>
    <div class="meth">
      <div class="meth-h">\u6838\u5fc3\u903b\u8f91</div>
      <div class="meth-p">\u57fa\u4e8e\u6cca\u677e\u5206\u5e03\u7684\u8fdb\u7403\u671f\u671b\u6a21\u578b\uff08lambda\uff09\uff0c\u901a\u8fc7\u8499\u7279\u5361\u6d1b\u6a21\u62df\uff082000\u6b21/\u573a\uff09\u751f\u6210\u80dc\u5e73\u8d1f\u6982\u7387\u5206\u5e03\u3002\u7ed3\u5408DDI\uff08\u76d8\u53e3\u504f\u5dee\u6307\u6570\uff09\u6821\u51c6\u4e0e\u56e0\u5b50\u4fee\u6b63\u7cfb\u7edf\uff0c\u8f93\u51fa\u63a8\u8350\u65b9\u5411\u4e0e\u9002\u914d\u5ea6\u8bc4\u5206\u3002</div>
    </div>
    <div class="meth">
      <div class="meth-h">Lambda \u8ba1\u7b97</div>
      <div class="meth-p">\u4ece\u7ade\u5f69SP\u53cd\u63a8\u5e02\u573a\u9690\u54b8lambda\uff0c\u4e0e\u57fa\u4e8exG/\u5b9e\u9645\u8fdb\u7403\u7684\u7269\u7406lambda\u8fdb\u884c\u4ea4\u53c9\u9a8c\u8bc1\u3002\u6700\u7ec8lambda\u5728\u4e24\u8005\u4e4b\u95f4\u52a0\u6743\u5e73\u8861\uff0c\u517c\u987e\u5e02\u573a\u9884\u671f\u4e0e\u57fa\u672c\u9762\u5b9e\u529b\u3002</div>
    </div>
    <div class="meth">
      <div class="meth-h">DDI \u6821\u51c6</div>
      <div class="meth-p">DDI = P(\u7269\u7406) - P(\u5e02\u573a)\uff0c\u8861\u91cf\u6a21\u578b\u4e0e\u5e02\u573a\u4e4b\u95f4\u7684\u504f\u5dee\u3002|DDI| > 0.08 \u65f6\u89e6\u53d1\u6821\u51c6\uff0c\u65b9\u5411\u4e0e\u5e02\u573a\u70ed\u5ea6\u76f8\u53cd\u65f6\u964d\u7ea7\u5904\u7406\u3002\u6821\u51c6\u5e45\u5ea6\u4e0d\u8d85\u8fc70.05\uff0c\u9632\u6b62\u8fc7\u5ea6\u4fee\u6b63\u3002</div>
    </div>
    <div class="meth">
      <div class="meth-h">\u56e0\u5b50\u4fee\u6b63</div>
      <div class="meth-p">\u4f24\u75c5\u5f71\u54cd\uff08\u6838\u5fc3+-20%\uff0c\u8f6e\u6362+-5%\uff09\u3001\u6218\u610f\u4fee\u6b63\uff08\u51b3\u8d5b\u671f+-5%\uff0c\u5e38\u89c4\u671f+-15%\uff09\u3001\u677e\u61c8\u6263\u51cf\uff088%\uff09\u3001\u9ad8\u539f\u52a0\u6210\uff0815%\uff09\u3002\u591a\u56e0\u5b50\u53e0\u52a0\u540e\u91cd\u65b0\u5f52\u4e00\u5316lambda\u3002</div>
    </div>
    <div class="meth">
      <div class="meth-h">\u98ce\u63a7\u964d\u7ea7</div>
      <div class="meth-p">\u6df1\u76d8\uff08AH>=2.0\uff09\u81ea\u52a8\u964d\u7ea71\u7ea7\uff1b\u4e2d\u76d8\uff081.0<=AH<=1.25\uff09\u4e14lambda\u5dee<0.5\u989d\u5916\u964d\u7ea7\uff1b\u9002\u914d\u5ea6<4.0\u89e6\u53d1\u7194\u65ad\uff0c\u6807\u8bb0\u4e3aC\u7ea7\u3002</div>
    </div>
    <div style="margin-top:20px;padding-top:16px;border-top:2px solid var(--bd)">
      <div class="meth-h">\u7248\u672c\u66f4\u65b0</div>
      <div class="v-item"><span class="v-ver">Rev1.13</span><span class="v-date">2026-05-31</span><div class="v-msg">DDI\u632f\u5e45\u6bd4\u4f8b\u53c2\u6570\u5316\uff1b\u5ba2\u9635\u51b7\u5904\u7406\u673a\u5236\uff1bLambda\u5f52\u4e00\u5316\u91cd\u7b97\u903b\u8f91\u4f18\u5316\uff1b\u81ea\u9002\u5e94\u8bc4\u5206\u533a\u95f4\u3002</div></div>
      <div class="v-item"><span class="v-ver">Rev1.12</span><span class="v-date">2026-05-28</span><div class="v-msg">\u65b0\u589e\u6570\u636e\u7f3a\u5931\u6807\u8bb0\u7cfb\u7edf\uff1b\u8499\u7279\u5361\u6d1b\u6a21\u62df\u6b21\u6570\u4ece1000\u63d0\u5347\u81f32000\uff1b\u534a\u5168\u573a\u9884\u6d4b\u903b\u8f91\u4fee\u6b63\u3002</div></div>
      <div class="v-item"><span class="v-ver">Rev1.11</span><span class="v-date">2026-05-25</span><div class="v-msg">\u591a\u56e0\u5b50\u53e0\u52a0\u5f52\u4e00\u5316\uff1b\u6218\u610f\u4fee\u6b63\u4e0e\u4f24\u75c5\u56e0\u5b50\u72ec\u7acb\u8bc4\u4f30\uff1b\u98ce\u63a7\u964d\u7ea7\u6a21\u578b\u91cd\u6784\u3002</div></div>
      <div class="v-item"><span class="v-ver">Rev1.10</span><span class="v-date">2026-05-20</span><div class="v-msg">\u521d\u59cb\u7248\u672c\uff1a\u6cca\u677elambda\u6a21\u578b + \u8499\u7279\u5361\u6d1b\u6a21\u62df + DDI\u6821\u51c6 + \u57fa\u7840\u56e0\u5b50\u4fee\u6b63\u3002</div></div>
    </div>
  </div>
</div>

<div class="sp-wrap" id="spWrap">
  <button class="sp-btn">\u53c2\u6570\u8bf4\u660e</button>
</div>
<div class="sp" id="spPanel"><div class="sp-hdr"><h2>\u6846\u67b6\u53c2\u6570\u8bf4\u660e</h2></div>
<div class="sp-bd">
<div class="sp-g"><div class="sp-g-h" onclick="var p=this.parentNode;var c=p.querySelector('.sp-g-c');if(c){c.classList.toggle('open');p.classList.toggle('expanded');}">\u8499\u7279\u5361\u6d1b\u6a21\u62df</div><div class="sp-g-c">
<div class="sp-g-i"><span class="lk">\u8fd0\u884c\u6b21\u6570</span> <span class="lv">MONTE_CARLO_RUNS = 2000</span><br>\u6bcf\u573a\u6bd4\u8d5b\u8dd12000\u6b21\u968f\u673a\u6a21\u62df\uff0c\u7b97\u51fa\u6700\u53ef\u80fd\u7684\u8d5b\u679c\u6982\u7387\u5206\u5e03\u3002</div>
<div class="sp-g-i"><span class="lk">\u534a\u573a\u6bd4\u4f8b</span> <span class="lv">HALF_TIME_RATIO = 0.44</span><br>\u534a\u573a\u8fdb\u7403\u5360\u5168\u573a\u7684\u6bd4\u4f8b\u7cfb\u6570\uff0c\u7528\u4e8e\u534a\u5168\u573a\u9884\u6d4b\u3002</div></div></div>
<div class="sp-g"><div class="sp-g-h" onclick="var p=this.parentNode;var c=p.querySelector('.sp-g-c');if(c){c.classList.toggle('open');p.classList.toggle('expanded');}">DDI \u6821\u51c6</div><div class="sp-g-c">
<div class="sp-g-i"><span class="lk">Kelly\u56e0\u5b50</span> <span class="lv">D_KELLY_DEFAULT = 0.05</span><br>\u51ef\u5229\u7cfb\u6570\uff0c\u63a7\u5236\u8d44\u91d1\u7ba1\u7406\u6a21\u578b\u7684\u98ce\u9669\u504f\u597d\u3002</div>
<div class="sp-g-i"><span class="lk">\u8d44\u91d1\u6d41\u504f\u5dee</span> <span class="lv">VBAL_DEFAULT = 0.15</span><br>\u5e02\u573a\u8d44\u91d1\u6d41\u5411\u504f\u5dee\u7684\u9ed8\u8ba4\u4f30\u8ba1\u503c\u3002</div>
<div class="sp-g-i"><span class="lk">\u89e6\u53d1\u9608\u503c</span> <span class="lv">DDI_TRIGGER_THRESHOLD = 0.08</span><br>DDI\u504f\u5dee\u8d85\u8fc7\u6b64\u503c\u89e6\u53d1\u6821\u51c6\uff0c\u5e02\u573a\u70ed\u5ea6\u5f02\u5e38\u3002</div>
<div class="sp-g-i"><span class="lk">\u632f\u5e45\u5c01\u9876</span> <span class="lv">DDI_AMPLITUDE_CAP = 0.05</span><br>\u5355\u6b21DDI\u6821\u51c6\u6700\u5927\u5e45\u5ea6\uff0c\u9632\u6b62\u8fc7\u5ea6\u4fee\u6b63\u3002</div>
<div class="sp-g-i"><span class="lk">\u632f\u5e45\u6bd4\u4f8b</span> <span class="lv">DDI_AMPLITUDE_RATIO = 0.30</span><br>DDA\u6821\u51c6\u5360\u603b\u504f\u5dee\u7684\u6bd4\u4f8b\uff080-1\uff09\u3002</div>
<div class="sp-g-i"><span class="lk">\u5ba2\u9635\u51b7\u5904\u7406</span> <span class="lv">AWAY_COLD_TREATMENT = 0.08</span><br>\u7279\u6b8a\u8d5b\u4e8b\u5ba2\u961f\u51b7\u5374\u5904\u7406\u5e45\u5ea6\uff0c\u9632\u6b62\u53cd\u5411\u8d70\u70ed\u3002</div></div></div>
<div class="sp-g"><div class="sp-g-h" onclick="var p=this.parentNode;var c=p.querySelector('.sp-g-c');if(c){c.classList.toggle('open');p.classList.toggle('expanded');}">\u56e0\u5b50\u4fee\u6b63</div><div class="sp-g-c">
<div class="sp-g-i"><span class="lk">\u4f24\u75c5\u6838\u5fc3\u4e0a\u9650</span> <span class="lv">INJURY_CORE_MAX = 0.20</span><br>\u6838\u5fc3\u7403\u5458\u7f3a\u9635\u6700\u5927\u5f71\u54cd\uff1alambda\u4fee\u6b63\u4e0d\u8d85\u8fc7+-20%\u3002</div>
<div class="sp-g-i"><span class="lk">\u8f6e\u6362\u4e0a\u9650</span> <span class="lv">INJURY_ROTATION_MAX = 0.05</span><br>\u8f6e\u6362\u4f24\u75c5\u5f71\u54cd\u4e0a\u9650\uff0c\u4e0d\u8d85\u8fc7+-5%\u3002</div>
<div class="sp-g-i"><span class="lk">\u677e\u61c8\u7f5a\u6b3e</span> <span class="lv">SLACK_PENALTY = 0.08</span><br>\u5df2\u4fdd\u7ea7/\u5df2\u51fa\u7ebf\u7403\u961f\u677e\u61c8\u6263\u51cf\uff0clambda\u964d8%\u3002</div>
<div class="sp-g-i"><span class="lk">\u9ad8\u539f\u52a0\u6210</span> <span class="lv">ALTITUDE_BONUS = 0.15</span><br>\u6d77\u62d4>2500m\u4e3b\u573a\u4f18\u52bf\uff1alambda\u52a0\u621015%\u3002</div></div></div>
<div class="sp-g"><div class="sp-g-h" onclick="var p=this.parentNode;var c=p.querySelector('.sp-g-c');if(c){c.classList.toggle('open');p.classList.toggle('expanded');}">\u6218\u610f\u4fee\u6b63</div><div class="sp-g-c">
<div class="sp-g-i"><span class="lk">\u51b3\u8d5b\u671f\u4e0a\u9650</span> <span class="lv">MOTIVATION_CAP_PLAYOFF = 0.05</span><br>\u9644\u52a0\u8d5b/\u672b\u8f6e\u751f\u6b7b\u6218\uff1a\u6218\u610f\u4fee\u6b63\u4e0a\u9650+-5%\u3002</div>
<div class="sp-g-i"><span class="lk">\u5e38\u89c4\u671f\u4e0a\u9650</span> <span class="lv">MOTIVATION_CAP_REGULAR = 0.15</span><br>\u5e38\u89c4\u8054\u8d5b\uff1a\u6218\u610f\u4fee\u6b63\u4e0a\u9650+-15%\u3002</div></div></div>
<div class="sp-g"><div class="sp-g-h" onclick="var p=this.parentNode;var c=p.querySelector('.sp-g-c');if(c){c.classList.toggle('open');p.classList.toggle('expanded');}">\u98ce\u63a7\u964d\u7ea7</div>
<div class="sp-g-c">
<div class="sp-g-i"><span class="lk">\u6df1\u76d8\u9608\u503c</span> <span class="lv">DEEP_HANDICAP_THRESHOLD = 2.0</span><br>\u8ba9\u7403>=2\u7403\u89e6\u53d1\u6df1\u76d8\u964d\u7ea7\uff0c\u8bc4\u7ea7+1\u7ea7\u98ce\u9669\u3002</div>
<div class="sp-g-i"><span class="lk">\u4e2d\u76d8\u533a\u95f4</span> <span class="lv">1.0 <= AH <= 1.25</span><br>\u4e2d\u76d8\u533a\u95f4\uff1a\u8ba9\u74031-1.25\u4e14lambda\u5dee<0.5\u989d\u5916\u964d\u7ea7\u3002</div>
<div class="sp-g-i"><span class="lk">\u7194\u65ad\u9608\u503c</span> <span class="lv">FIT_SCORE_THRESHOLD_MELTDOWN = 4.0</span></div></div></div>

<script src="/charts.js"></script>
<script>
(function() {
  var wrap = document.getElementById('spWrap');
  var panel = document.getElementById('spPanel');
  var timer;
  wrap.addEventListener('mouseenter', function() { clearTimeout(timer); panel.classList.add('open'); });
  wrap.addEventListener('mouseleave', function() { timer = setTimeout(function() { panel.classList.remove('open'); }, 100); });
  panel.addEventListener('mouseenter', function() { clearTimeout(timer); panel.classList.add('open'); });
  panel.addEventListener('mouseleave', function() { timer = setTimeout(function() { panel.classList.remove('open'); }, 100); });
})();
(function() {
  var wrap = document.getElementById('spLWrap');
  var panel = document.getElementById('spLPanel');
  var timer;
  wrap.addEventListener('mouseenter', function() { clearTimeout(timer); panel.classList.add('open'); });
  wrap.addEventListener('mouseleave', function() { timer = setTimeout(function() { panel.classList.remove('open'); }, 100); });
  panel.addEventListener('mouseenter', function() { clearTimeout(timer); panel.classList.add('open'); });
  panel.addEventListener('mouseleave', function() { timer = setTimeout(function() { panel.classList.remove('open'); }, 100); });
})();
</script>
</body>
</html>'''

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Restored: {len(html)} bytes")

# Verify Chinese text
with open(path, "rb") as f:
    raw = f.read()
for name, bs in [("系统说明按钮", b"\xe7\xb3\xbb\xe7\xbb\x9f\xe8\xaf\xb4\xe6\x98\x8e"), 
                 ("参数说明按钮", b"\xe5\x8f\x82\xe6\x95\xb0\xe8\xaf\xb4\xe6\x98\x8e"),
                 ("分析系统介绍", b"\xe5\x88\x86\xe6\x9e\x90\xe7\xb3\xbb\xe7\xbb\x9f\xe4\xbb\x8b\xe7\xbb\x8d"),
                 ("sp-l-btn", b"sp-l-btn"),
                 ("sp-wrap", b"sp-wrap")]:
    print(f"[{'OK' if bs in raw else 'FAIL'}] {name}")