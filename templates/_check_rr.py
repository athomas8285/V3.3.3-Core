with open("charts.js","r",encoding="utf-8") as f:
    t = f.read()
idx = t.index("function renderReview()")
end = t.index("function", idx+5)
print(t[idx:end])