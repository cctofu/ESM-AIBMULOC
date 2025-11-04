import numpy as np

def simulate_N(t, R, seed=30):
    np.random.seed(seed)
    results = []
    for _ in range(R):
        s, n = 0.0, 0
        while s <= t:
            s += np.random.rand()
            n += 1
        results.append(n)
    results = np.array(results)
    mean_val = results.mean()
    std_val = results.std(ddof=1)
    half_width = 1.96 * std_val / np.sqrt(R)
    return mean_val, mean_val - half_width, mean_val + half_width

# Run simulations
for t in [1, 2]:
    for R in [100, 1000, 10000]:
        mean_val, ci_low, ci_high = simulate_N(t, R)
        print(f"t={t}, R={R}: mean={mean_val:.4f}, 95% CI=({ci_low:.4f}, {ci_high:.4f})")