p = "D:/V3.3.3-Core/monte_carlo.py"
with open(p, "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("from config import MONTE_CARLO_RUNS, HALF_TIME_RATIO", "from config import MONTE_CARLO_RUNS, HALF_TIME_RATIO, DISPERSION_ALPHA")
c = c.replace("def __init__(self, lambda_h, lambda_a, jc_handicap, runs=None, random_seed=42):", "def __init__(self, lambda_h, lambda_a, jc_handicap, runs=None, random_seed=42, dispersion_alpha=None):")

idx = c.find("self.convergence_std")
eol = c.find("\n", idx)
c = c[:eol+1] + "        self.dispersion_alpha = DISPERSION_ALPHA if dispersion_alpha is None else dispersion_alpha\n" + c[eol+1:]

c = c.replace("home_goals = np.random.poisson(self.lh, runs)", "n_r = 1.0 / self.dispersion_alpha\n        p_h = n_r / (n_r + self.lh)\n        p_a = n_r / (n_r + self.la)\n        home_goals = np.random.negative_binomial(n_r, p_h, runs)")
c = c.replace("away_goals = np.random.poisson(self.la, runs)", "away_goals = np.random.negative_binomial(n_r, p_a, runs)")
c = c.replace("half_h = np.random.poisson(self.lh * HALF_TIME_RATIO, runs)", "n_r_ht = 1.0 / self.dispersion_alpha\n        p_h_ht = n_r_ht / (n_r_ht + self.lh * HALF_TIME_RATIO)\n        p_a_ht = n_r_ht / (n_r_ht + self.la * HALF_TIME_RATIO)\n        half_h = np.random.negative_binomial(n_r_ht, p_h_ht, runs)")
c = c.replace("half_a = np.random.poisson(self.la * HALF_TIME_RATIO, runs)", "half_a = np.random.negative_binomial(n_r_ht, p_a_ht, runs)")

old_end = '"converged": converged\n            }'
new_end = '"converged": converged,\n                "dispersion_alpha": self.dispersion_alpha\n            }'
c = c.replace(old_end, new_end)

with open(p, "w", encoding="utf-8") as f:
    f.write(c)
print("OK")