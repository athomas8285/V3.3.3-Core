import sys
sys.stdout.reconfigure(encoding="utf-8")
f=open("C:/Users/gjj/Desktop/v333/templates/index.html","r",encoding="utf-8",errors="replace")
c=f.read()
f.close()

idx=c.find('sp-bd')
# Find the SECOND occurrence (first is in CSS)
count=0
pos=0
while pos < len(c):
    pos=c.find('sp-bd', pos)
    if pos<0:
        break
    count+=1
    if count==2:
        # This should be the HTML one
        # Go back to find the <div
        div=c.rfind('<div', 0, pos)
        print("HTML sp-bd div at", div)
        # Simple depth counting
        depth=0
        p=div
        while p < len(c):
            if c[p:p+4]=='<div' and c[p+4]!='/' and c[p+4:p+5]!='i':
                depth+=1
                p+=4
            elif c[p:p+6]=='</div>':
                depth-=1
                p+=6
                if depth==0:
                    print("End at", p, "length:", p-div)
                    print(c[div:p][:200])
                    break
            else:
                p+=1
        break
    pos+=1