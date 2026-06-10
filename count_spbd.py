
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/gjj/Desktop/v333/templates/index.html','r',encoding='utf-8') as f:
    c = f.read()
# Find all occurrences of sp-bd
pos = 0
count = 0
while True:
    pos = c.find('sp-bd', pos)
    if pos < 0:
        break
    count += 1
    ctx = c[max(0,pos-20):pos+20]
    print(f'Occurrence {count} at {pos}: ...{ctx}...')
    pos += 1
