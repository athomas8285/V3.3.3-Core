import re
p = r"D:\V3.3.3-Core\monte_carlo.py"
with open(p, "r", encoding="utf-8", errors="replace") as f:
    c = f.read()
c = c.replace("converged,
                \"dispersion_alpha\"", "converged,\n                \"dispersion_alpha\"")
with open(p, "w", encoding="utf-8") as f:
    f.write(c)
print("Fixed")