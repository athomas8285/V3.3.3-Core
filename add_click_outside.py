import sys

path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 找到 toggleFilter 和 toggleFilterRV 函数，在它们后面添加点击外部关掉下拉的逻辑
# 在 toggleFilter 之后添加 document.click handler

# 先找到 toggleFilter 函数的结尾
idx = content.find("function toggleFilter(){")
tf_end = content.find("function setFilter", idx)
# 在这之前插入点击外部关闭逻辑
click_code = """
document.addEventListener('click',function(e){
  var fd=document.getElementById("filterDropdown");
  if(fd&&FILTER_SHOW){
    var btn=e.target.closest('[onclick*=\"toggleFilter\"]');
    var dd=e.target.closest('#filterDropdown');
    if(!btn&&!dd){FILTER_SHOW=false;fd.style.display='none';}
  }
  var fd2=document.getElementById("filterDropdownRV");
  if(fd2&&FILTER_RV_SHOW){
    var btn2=e.target.closest('[onclick*=\"toggleFilterRV\"]');
    var dd2=e.target.closest('#filterDropdownRV');
    if(!btn2&&!dd2){FILTER_RV_SHOW=false;fd2.style.display='none';}
  }
});
"""

# 插入到 toggleFilter 和 setFilter 之间
content = content[:tf_end] + click_code + content[tf_end:]

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("点击外部关闭已添加!")

# 验证括号
def count_braces(code):
    curly = 0; paren = 0; i = 0; s = None; e = False
    while i < len(code):
        c = code[i]
        if e: e = False; i += 1; continue
        if c == "\\": e = True; i += 1; continue
        if s:
            if c == s: s = None
            i += 1; continue
        if c == "'" or c == '"': s = c; i += 1; continue
        if c == "{": curly += 1
        elif c == "}": curly -= 1
        elif c == "(": paren += 1
        elif c == ")": paren -= 1
        i += 1
    return curly, paren

cl, pr = count_braces(content)
print(f"括号: curly={cl} paren={pr}", end="")
if cl == 0 and pr == 0: print(" 正常!")
else: print(f" 不平衡!")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("保存成功!")