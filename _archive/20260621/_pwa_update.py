content = open("D:/V3.3.3-Core/templates/index.html", "r", encoding="utf-8").read()
content = content.replace(
    "<title>V3.3.3-Core \u5206\u6790\u7cfb\u7edf</title>",
    "<title>V3.3.3-Core \u5206\u6790\u7cfb\u7edf</title>\n<link rel=\"manifest\" href=\"/static/manifest.json\">\n<meta name=\"apple-mobile-web-app-capable\" content=\"yes\">\n<meta name=\"apple-mobile-web-app-status-bar-style\" content=\"black-translucent\">"
)
reg = "<script>if(\"serviceWorker\"in navigator){window.addEventListener(\"load\",()=>{navigator.serviceWorker.register(\"/static/sw.js\")})}</script>\n"
if "</body>" in content:
    content = content.replace("</body>", reg + "</body>")
open("D:/V3.3.3-Core/templates/index.html", "w", encoding="utf-8").write(content)
print("OK")
