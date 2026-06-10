import re
with open('templates/charts.js','r',encoding='utf-8') as f:
    c=f.read()
i=0;bal_b=0;bal_p=0;in_sq=False;in_dq=False;n=len(c)
while i<n:
    ch=c[i]
    if ch==chr(39) and not in_dq: in_sq=not in_sq
    elif ch==chr(34) and not in_sq: in_dq=not in_dq
    elif not in_sq and not in_dq:
        if ch==chr(123): bal_b+=1
        elif ch==chr(125): bal_b-=1
        elif ch==chr(40): bal_p+=1
        elif ch==chr(41): bal_p-=1
        elif ch==chr(47) and i+1<n and c[i+1]==chr(47):
            while i<n and c[i]!=chr(10): i+=1
    i+=1
print('Braces:',bal_b)
print('Parens:',bal_p)
