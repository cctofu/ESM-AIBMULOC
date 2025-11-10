import numpy as np

# ---------------------------------------------------------------
# 1. Transition matrix setup
# ---------------------------------------------------------------
P = np.array([
    [1/2, 1/3, 1/6],
    [0,   1/3, 2/3],
    [1/2, 0,   1/2]
])

np.random.seed(2025)  # fixed seed for reproducibility


# ---------------------------------------------------------------
# 2. Simulate one Markov chain trajectory of given length
# ---------------------------------------------------------------
def simulate_chain(P, X0, n_steps):
    """Simulate a single Markov chain trajectory starting at X0."""
    X = X0
    for _ in range(n_steps):
        X = np.random.choice([0, 1, 2], p=P[X])
    return X


# ---------------------------------------------------------------
# 3. (c) and (d): Simulate M independent runs
# ---------------------------------------------------------------
M = 100  # number of trajectories
X10 = np.array([simulate_chain(P, 0, 10) for _ in range(M)])

# (c) Estimate P(X10 = 1 | X0 = 0)
p_X10_eq_1 = np.mean(X10 == 1)

# (d) Estimate E[X10 | X0 = 0]
E_X10 = np.mean(X10)

print(f"(c) P(X10 = 1 | X0 = 0) ≈ {p_X10_eq_1:.4f}")
print(f"(d) E[X10 | X0 = 0] ≈ {E_X10:.4f}")


# ---------------------------------------------------------------
# 4. (e) and (f): Hitting time to state 1
# ---------------------------------------------------------------
def hitting_time(P, X0, target, max_steps=None):
    """Return hitting time to target; if not reached by max_steps, return None."""
    X, t = X0, 0
    while True:
        if X == target:
            return t
        if max_steps is not None and t >= max_steps:
            return None  # not hit within limit
        X = np.random.choice([0, 1, 2], p=P[X])
        t += 1


# (e) P(T ≤ 10 | X0 = 0)
T10 = np.array([hitting_time(P, 0, 1, max_steps=10) for _ in range(M)])
p_T_le_10 = np.mean([t is not None for t in T10])

# (f) E[T | X0 = 0]
T = np.array([hitting_time(P, 0, 1) for _ in range(M)])
E_T = np.mean(T)

print(f"(e) P(T ≤ 10 | X0 = 0) ≈ {p_T_le_10:.4f}")
print(f"(f) E[T | X0 = 0] ≈ {E_T:.4f}")


# ---------------------------------------------------------------
# 5. (g) and (h): Long-run proportions and average cost
# ---------------------------------------------------------------
N = 10000
burn_in = 100
X = 0
trajectory = []

for _ in range(N):
    X = np.random.choice([0, 1, 2], p=P[X])
    trajectory.append(X)

trajectory = np.array(trajectory)
steady_states = trajectory[burn_in:]  # discard first 100 as burn-in

# (g) Long-run proportions
pi_hat = np.array([np.mean(steady_states == i) for i in [0, 1, 2]])

# (h) Long-run average cost: costs for states 0,1,2 = 1,3,2
costs = np.array([1, 3, 2])
g_hat = np.mean(costs[steady_states])

print(f"(g) Long-run proportions π̂ = {np.round(pi_hat, 4)}")
print(f"(h) Long-run average cost ĝ ≈ {g_hat:.4f}")
