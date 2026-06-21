with open("D:\\V3.3.3-Core\\templates\\index.html", "rb") as f:
    t1 = f.read().decode("utf-8")
with open("D:\\V3.3.3-Core\\templates\\index.html.bak", "rb") as fb:
    t2 = fb.read().decode("utf-8")
    
idx1 = t1.find("function renderFromData")
end1 = t1.find("var __todayRawData", idx1)
idx2 = t2.find("function renderFromData")
end2 = t2.find("var __todayRawData", idx2)

fn1 = t1[idx1:end1]
fn2 = t2[idx2:end2]

# Find where they diverge
for i in range(min(len(fn1), len(fn2))):
    if fn1[i] != fn2[i]:
        print(f"First diff at char {i}")
        print(f"Current: {repr(fn1[max(0,i-20):i+50])}")
        print(f"Backup:  {repr(fn2[max(0,i-20):i+50])}")
        break