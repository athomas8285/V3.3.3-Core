c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

# Find all </script> occurrences
pos = -1
count = 0
while True:
    pos = c.find('</script>', pos + 1)
    if pos < 0:
        break
    count += 1
    if count <= 5:
        print(f'[{count}] at {pos}: context={repr(c[max(0,pos-5):pos+15])}')

print(f'Total: {count}')