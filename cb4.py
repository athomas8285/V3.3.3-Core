with open('templates/charts.js','r',encoding='utf-8') as f:
    c=f.read()
lines=c.split(chr(10))
bal_b=0;bal_p=0;in_sq=False;in_dq=False
for li,l in enumerate(lines):
    i=0;n=len(l)
    prev_b=bal_b;prev_p=bal_p
    while i<n:
        ch=l[i]
        if ch==chr(39) and not in_dq: in_sq=not in_sq
        elif ch==chr(34) and not in_sq: in_dq=not in_dq
        elif not in_sq and not in_dq:
            if ch==chr(123): bal_b+=1
            elif ch==chr(125): bal_b-=1
            elif ch==chr(40): bal_p+=1
            elif ch==chr(41): bal_p-=1
            elif ch==chr(47) and i+1<n and l[i+1]==chr(47):
                break
        i+=1
    if bal_b!=0 or bal_p!=0:
        print(f'L{li+1}: b={bal_b:3d} p={bal_p:3d}  {l[:100]}')
print(f'FINAL: b={bal_b} p={bal_p}')
