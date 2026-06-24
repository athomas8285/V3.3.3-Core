import re, json

raw = open("D:/V3.3.3-Core/data/match_info.json", "rb").read()

results = {
    "周日037": {"score": "4-0", "hafu": "胜胜"},
    "周日038": {"score": "0-0", "hafu": "平平"},
    "周日039": {"score": "2-2", "hafu": "胜平"},
    "周日040": {"score": "1-3", "hafu": "胜负"},
}
hfmap = {"hh":"SS","hd":"SP","ha":"SF","dh":"PS","dd":"PP","da":"PF","ah":"FS","ad":"FP","aa":"FF"}
hfmap_cn = {"SS":"胜胜","SP":"胜平","SF":"胜负","PS":"平胜","PP":"平平","PF":"平负","FS":"负胜","FP":"负平","FF":"负负"}
smap = {"s01s00":"1-0","s02s00":"2-0","s02s01":"2-1","s03s00":"3-0","s03s01":"3-1","s03s02":"3-2",
        "s00s01":"0-1","s00s02":"0-2","s01s02":"1-2","s00s03":"0-3","s01s03":"1-3","s02s03":"2-3",
        "s00s00":"0-0","s01s01":"1-1","s02s02":"2-2"}

for tid in ["周日037", "周日038", "周日039", "周日040"]:
    pos = raw.find(('"id": "'+tid+'"').encode())
    start = raw.rfind(b'{', 0, pos)
    depth = 1; end = pos
    while depth > 0 and end < len(raw):
        end += 1
        if raw[end:end+1] == b'{': depth += 1
        elif raw[end:end+1] == b'}': depth -= 1
    obj = json.loads(raw[start:end+1].decode("utf-8", errors="replace"))
    
    r = results[tid]
    hg, ag = int(r["score"].split("-")[0]), int(r["score"].split("-")[1])
    hafu_act = r["hafu"]
    hcp = int(obj.get("jc_handicap", 0))
    ds = obj.get("direction", "")
    rt = obj.get("rating", "")
    
    dh = False
    if ds == "胜": dh = hg > ag
    elif ds == "负": dh = hg < ag
    elif ds == "平": dh = hg == ag
    elif ds == "让胜": dh = (hg - ag + (-hcp)) > 0
    elif ds == "让负": dh = (hg - ag + (-hcp)) < 0
    
    hl = "HIT" if dh else "MISS"
    print(f"[{tid}] {r['score']} dir={ds} rat={rt} {hl} (hcp={hcp}, net={hg-ag})")
    
    ttg = obj.get("ttg_odds", {})
    if ttg:
        for g in range(8):
            k = f"s{g}"
            if k in ttg:
                od = float(ttg[k])
                if 2.0 <= od <= 10.0:
                    hit = hg+ag == g
                    print(f"  TT{g} @{od:.1f}{' YES' if hit else ''}")
        for ps in [(2,3),(3,4)]:
            o1 = ttg.get(f"s{ps[0]}"); o2 = ttg.get(f"s{ps[1]}")
            if o1 and o2:
                o1f, o2f = float(o1), float(o2)
                if 2.0 <= o1f <= 10.0 and 2.0 <= o2f <= 10.0:
                    podds = round(1.0/(1.0/o1f+1.0/o2f),2)
                    hit = (hg+ag) in ps
                    print(f"  TTpack{ps[0]}/{ps[1]} @{podds}{' YES' if hit else ''}")
    
    hafu = obj.get("hafu_odds", {})
    if hafu:
        found = []
        for k, lbl in hfmap.items():
            if k in hafu:
                od = float(hafu[k])
                if 2.0 <= od <= 4.0:
                    lbl_cn = hfmap_cn.get(lbl, lbl)
                    found.append((lbl_cn, od, lbl_cn == hafu_act))
        for lbl_cn, od, hit in found[:8]:
            print(f"  HF:{lbl_cn} @{od:.2f}{' YES' if hit else ''}")
        for opts_cn, pname in [(["胜胜","平胜"],"主不败"), (["负负","平负"],"客不败")]:
            opts = [l for l in found if l[0] in opts_cn]
            if len(opts) >= 2:
                podds = round(1.0/sum(1.0/l[1] for l in opts),2)
                hit = hafu_act in opts_cn
                print(f"  HFpack:{pname} @{podds}{' YES' if hit else ''}")
    
    crs = obj.get("crs_odds", {})
    if crs:
        ascore = f"{hg}-{ag}"
        cfound = []
        for k, lbl in smap.items():
            if k in crs:
                od = float(crs[k])
                if 2.0 <= od <= 10.0:
                    cfound.append((lbl, od))
        for lbl, od in cfound[:6]:
            hit = lbl == ascore
            print(f"  CR:{lbl} @{od:.1f}{' YES' if hit else ''}")
        for opts, pname in [(["1-0","2-0"],"主小胜"), (["0-1","0-2"],"客小胜")]:
            opts2 = [(l,o) for l,o in cfound if l in opts]
            if len(opts2) >= 2:
                podds = round(1.0/sum(1.0/o for _,o in opts2),2)
                hit = ascore in opts
                print(f"  CRpack:{pname} @{podds}{' YES' if hit else ''}")
    
    hhw = obj.get("jc_hhad_win"); hhd = obj.get("jc_hhad_draw"); hhl = obj.get("jc_hhad_lose")
    if hhw and hhd and hhl:
        hhw_f, hhd_f, hhl_f = float(hhw), float(hhd), float(hhl)
        for (a, b, pname) in [
            (hhw_f, hhd_f, "让胜/平"), (hhd_f, hhl_f, "让平/负")
        ]:
            items = [(n,v) for n,v in [("a",a),("b",b)] if v>1.0]
            if len(items) >= 2:
                podds = round(1.0/sum(1.0/v for _,v in items),2)
                jc_score = hg - ag + (-hcp)
                hit = jc_score >= 0 if "让胜" in pname else jc_score <= 0
                print(f"  DirPack:{pname} @{podds}{' YES' if hit else ''}")
    
    print()