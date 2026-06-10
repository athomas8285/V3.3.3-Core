path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ===== 1. 在第1行后添加筛选状态变量 =====
line1_end = content.find("\n") + 1
new_vars = (
    "var FILTER_RV={rating:{S:true,A:true,B:true,C:true},event:{},dir:true,goals:true,ht:true,score:true};"
    "FILTER_RV_ALL_EVENTS=true;FILTER_RV_SHOW=false;\n"
)
content = content[:line1_end] + new_vars + content[line1_end:]
print("1. 添加FILTER_RV变量")

# ===== 2. 在setFilter后添加新的筛选函数 =====
setfilter_end = content.find("function filterLabel")
rv_filter_funcs = """
function toggleFilterRV(){
  FILTER_RV_SHOW=!FILTER_RV_SHOW;
  var d=document.getElementById("filterDropdownRV");
  if(d){d.style.display=FILTER_RV_SHOW?"block":"none";}
}
function setFilterRV(type,val){
  if(type==="rating"){
    FILTER_RV.rating[val]=!FILTER_RV.rating[val];
    var allTrue=true;
    for(var k in FILTER_RV.rating){if(!FILTER_RV.rating[k]){allTrue=false;break;}}
    if(allTrue){FILTER_RV.rating={S:true,A:true,B:true,C:true};}
  }else if(type==="event"){
    FILTER_RV.event[val]=!FILTER_RV.event[val];
    FILTER_RV_ALL_EVENTS=false;
    var allEv=true;
    for(var k in FILTER_RV.event){if(!FILTER_RV.event[k]){allEv=false;break;}}
    if(allEv){FILTER_RV_ALL_EVENTS=true;FILTER_RV.event={};}
  }else if(type==="event_all"){
    FILTER_RV_ALL_EVENTS=!FILTER_RV_ALL_EVENTS;
    if(FILTER_RV_ALL_EVENTS){FILTER_RV.event={};}
  }else if(type==="correct"){
    FILTER_RV[val]=!FILTER_RV[val];
  }
  if(RV.length)renderReview();
}
"""
content = content[:setfilter_end] + rv_filter_funcs + content[setfilter_end:]
print("2. 添加RV筛选函数")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("保存成功!")