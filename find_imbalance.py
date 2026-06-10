path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Track bracket balance line by line
balance = 0
paren_bal = 0
for i, line in enumerate(lines, 1):
    opens = line.count("{")
    closes = line.count("}")
    balance += opens - closes
    
    po = line.count("(")
    pc = line.count(")")
    paren_bal += po - pc
    
    if balance < 0 or paren_bal < 0:
        print(f"Negative at line {i}: curly={balance} paren={paren_bal}")
        print(f"  {line[:200].rstrip()}")
        break
else:
    print(f"Final: curly={balance} paren={paren_bal}")
    
    # Find the line where it goes wrong
    bal = 0
    pb = 0
    for i, line in enumerate(lines, 1):
        opens = line.count("{")
        closes = line.count("}")
        bal += opens - closes
        
        po = line.count("(")
        pc = line.count(")")
        pb += po - pc
        
        # Check for lines where balance changes
        if opens != closes or po != pc:
            print(f"L{i:4d} (curly: {opens}/{closes} -> {bal}, paren: {po}/{pc} -> {pb}): {line[:150].rstrip()}")