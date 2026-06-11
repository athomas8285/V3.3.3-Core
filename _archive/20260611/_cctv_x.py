import os, urllib.request

FLAGS_DIR = "D:\\V3.3.3-Core\\static\\flags"
os.makedirs(FLAGS_DIR, exist_ok=True)

# Bing flag URLs by Bing team name
bing_flags = {
    "mexico": ("https://ts3.tc.mm.bing.net/th?id=OSB.%7ch1pa8vGs9kIEqxF2je4Zw--.png", "墨西哥"),
    "south_africa": ("https://ts4.tc.mm.bing.net/th/id/OSB.0rHoxVTldzoIjS7pJ1PdsQ--.png?w=24", "南非"),
    "korea": ("https://ts2.tc.mm.bing.net/th/id/OSB.ZalNIX_B85wZrZrTb5tebA--.png?w=24", "韩国"),
    "czech": ("https://ts3.tc.mm.bing.net/th?id=OSB.x66yZcxCboJe%7cT1fMlpPKQ--.png", "捷克"),
    "canada": ("https://ts1.tc.mm.bing.net/th/id/OSB.C_GWZ4rWtoW2rCVBo2RJGQ--.png?w=24", "加拿大"),
    "bosnia": ("https://ts3.tc.mm.bing.net/th/id/OSB.SQUmOkV2XKJhDGOg0K8otw--.png?w=24", "波黑"),
    "usa": ("https://ts3.tc.mm.bing.net/th?id=OSB.d21n1cS%7cBfaLp3L_cMfLAg--.png", "美国"),
    "paraguay": ("https://ts1.tc.mm.bing.net/th?id=OSB.nVVQfE%7cU_RKHbx3VcNaY7w--.png", "巴拉圭"),
    "qatar": ("https://ts1.tc.mm.bing.net/th/id/OSB.GRSUQMV2UoXCkLdjfcfKsQ--.png?w=24", "卡塔尔"),
    "switzerland": ("https://ts2.tc.mm.bing.net/th/id/OSB.e1rIq5qxwaltge_EWvPYUw--.png?w=24", "瑞士"),
    "brazil": ("https://ts3.tc.mm.bing.net/th?id=OSB.5sVvejNkKv%7cw9yAjdaCTmw--.png", "巴西"),
    "morocco": ("https://ts3.tc.mm.bing.net/th/id/OSB.xB3RXweWTn_1fhPZXKgPzg--.png?w=24", "摩洛哥"),
    "haiti": ("https://ts2.tc.mm.bing.net/th?id=OSB.kU1cnkSZw%7cIFDOTL7%7ceEWQ--.png", "海地"),
    "scotland": ("https://ts1.tc.mm.bing.net/th/id/OSB.sB_adkQAr7Y7PkJY6AnMmQ--.png?w=24", "苏格兰"),
    "australia": ("https://ts1.tc.mm.bing.net/th/id/OSB.lxJo7gGxzH18Hsoo4STb9Q--.png?w=24", "奥大利亚"),
    "turkey": ("https://ts3.tc.mm.bing.net/th/id/OSB.GlMMoa5k0JqZw07r96vNug--.png?w=24", "土耳其"),
    "germany": ("https://ts3.tc.mm.bing.net/th?id=OSB.UBWG4ftM%7cmxTpOuQWWQYxg--.png", "德国"),
    "curacao": ("https://ts4.tc.mm.bing.net/th/id/OSB.KgiCh8mIEkMEtHykKRj8PA--.png?w=24", "库拉索"),
    "netherlands": ("https://ts3.tc.mm.bing.net/th/id/OSB.YUQM52kTjwke2cIVMy1MyA--.png?w=24", "荷兰"),
    "japan": ("https://ts1.tc.mm.bing.net/th?id=OSB.iI1Qa%7cWIQ%7cVTfmFQOxpilw--.png", "日本"),
    "ivory_coast": ("https://ts1.tc.mm.bing.net/th?id=OSB.knUzbhzw%7cjf9SAffhihZyQ--.png", "科特迪瓦"),
    "ecuador": ("https://ts2.tc.mm.bing.net/th/id/OSB.2I7ZpJczX6qQT_PO9zVuLg--.png?w=24", "厄瓜多尔"),
    "sweden": ("https://ts3.tc.mm.bing.net/th?id=OSB.tbWmN9P6aX%7cztWkoPc1wFQ--.png", "瑞典"),
    "tunisia": ("https://ts4.tc.mm.bing.net/th/id/OSB.yuquxTYQqKNML8kspAHjYA--.png?w=24", "突尼斯"),
    "spain": ("https://ts3.tc.mm.bing.net/th/id/OSB.hgUSGNppUx4Tm_rgtMI_yw--.png?w=24", "西班牙"),
    "cape_verde": ("https://ts1.tc.mm.bing.net/th/id/OSB.xMgA8woRhAhgvw33oG8I3g--.png?w=24", "佛得角"),
    "belgium": ("https://ts2.tc.mm.bing.net/th/id/OSB.PYa4fSExdzdU76dO25jORQ--.png?w=24", "比利时"),
    "egypt": ("https://ts2.tc.mm.bing.net/th/id/OSB.RoOU7SV9u4T1YKtsFZd5_g--.png?w=24", "埃及"),
    "saudi": ("https://ts4.tc.mm.bing.net/th?id=OSB.whALab8IBz2SUiuKayr6%7cA--.png", "沙特"),
    "uruguay": ("https://ts3.tc.mm.bing.net/th?id=OSB.I%7cNF_E_xKggTWwzM%7cB3c%7cw--.png", "乌拉圭"),
    "iran": ("https://ts3.tc.mm.bing.net/th/id/OSB.Z8Npo2TGgl8T9xMsWpYB4Q--.png?w=24", "伊朗"),
    "new_zealand": ("https://ts4.tc.mm.bing.net/th/id/OSB.vLzeEQzVTl0R_yEkrii4PA--.png?w=24", "新西兰"),
    "france": ("https://ts1.tc.mm.bing.net/th/id/OSB.uZpnWUovQu5UlpGjW05T1w--.png?w=24", "法国"),
    "senegal": ("https://ts2.tc.mm.bing.net/th/id/OSB.zyAotVjDnyGpNlGa5vf2wA--.png?w=24", "塞内加尔"),
    "iraq": ("https://ts3.tc.mm.bing.net/th/id/OSB.jSlxaTo7VprpGqRtJiatbg--.png?w=24", "伊拉克"),
    "norway": ("https://ts4.tc.mm.bing.net/th?id=OSB.ItXxev_86DE69gQa%7cDqwgw--.png", "挪威"),
    "argentina": ("https://ts1.tc.mm.bing.net/th/id/OSB.FgTVzvAJp_zjIKdIxE02sg--.png?w=24", "阿根廷"),
    "algeria": ("https://ts2.tc.mm.bing.net/th/id/OSB.lubDsejD8EyJxWAy05qaFw--.png?w=24", "阿尔及利亚"),
    "austria": ("https://ts4.tc.mm.bing.net/th/id/OSB.mD7FPVMPoHNxhZ7cksvsvg--.png?w=24", "奥地利"),
    "jordan": ("https://ts2.tc.mm.bing.net/th?id=OSB.n6dsC8is8oT9iaR%7cI4f20g--.png", "约旦"),
    "portugal": ("https://ts4.tc.mm.bing.net/th/id/OSB.oNV73VCix78iUirbUGbRxw--.png?w=24", "葡萄牙"),
    "dr_congo": ("https://ts1.tc.mm.bing.net/th/id/OSB.NNasrLxtwj2yKvbmcNDTew--.png?w=24", "民主刚果"),
    "england": ("https://ts4.tc.mm.bing.net/th?id=OSB.Bb%7cOCh6mDEaOct3bdDponA--.png", "英格兰"),
    "croatia": ("https://ts3.tc.mm.bing.net/th/id/OSB.E0xhYbL_7Pc7LLvO3a5aGg--.png?w=24", "克罗地亚"),
    "ghana": ("https://ts3.tc.mm.bing.net/th/id/OSB.GLELIQRc9lEcfXk9NOsMOw--.png?w=24", "加纳"),
    "panama": ("https://ts3.tc.mm.bing.net/th/id/OSB.NFgd30bXMRW6GMkt66SiaQ--.png?w=24", "巴拿马"),
    "uzbekistan": ("https://ts2.tc.mm.bing.net/th/id/OSB.fNW0Co8cp0ljnJ4Hd4szZg--.png?w=24", "乌兹别克斯坦"),
    "colombia": ("https://ts1.tc.mm.bing.net/th/id/OSB._B7FG5g7Mx5OBKoj8SOG6A--.png?w=24", "哥伦比亚"),
}

headers = {"User-Agent": "Mozilla/5.0"}
success = 0
for key, (url, app_name) in bing_flags.items():
    fpath = os.path.join(FLAGS_DIR, key + ".png")
    if os.path.exists(fpath) and os.path.getsize(fpath) > 100:
        success += 1
        continue
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10)
        data = resp.read()
        with open(fpath, "wb") as f:
            f.write(data)
        print(f"OK: {app_name} ({len(data)} bytes)")
        success += 1
    except Exception as e:
        print(f"FAIL: {app_name} -> {e}")

print(f"\nDone: {success}/{len(bing_flags)} flags in {FLAGS_DIR}")
