import numpy as np

# ---------------------------------------------------
# Simulation parameters
# ---------------------------------------------------
N = 100           # population size
alpha = 0.2       # P(active -> active)
beta = 0.4        # P(inactive -> inactive)
T = 10_000        # total steps
burn_in = 1_000   # burn-in steps
rng = np.random.default_rng(2025)  # reproducible RNG seed


# ===================================================
# (b) Long-run average number of active individuals
# ===================================================
X = 10  # initial number of active individuals
active_sum = 0

for step in range(1, T + 1):
    # survivors among actives
    if X > 0:
        survivors = np.sum(rng.random(X) <= alpha)
    else:
        survivors = 0

    # activations among inactives
    inactive = N - X
    if inactive > 0:
        new_activations = np.sum(rng.random(inactive) <= (1 - beta))
    else:
        new_activations = 0

    # update total actives
    X = survivors + new_activations

    # accumulate after burn-in
    if step > burn_in:
        active_sum += X

# estimated long-run average
avg_active = active_sum / (T - burn_in)
print(f"(b) Estimated long-run mean of X_n ≈ {avg_active:.4f}")


# ===================================================
# (d) Long-run probability that Y_n > Z_n
# ===================================================
K = 10  # size of initially active cohort
Y, Z = 10, 0
indicator_total = 0

for step in range(1, T + 1):
    # --- Initially active cohort ---
    if Y > 0:
        stay_active = np.sum(rng.random(Y) <= alpha)
    else:
        stay_active = 0

    if K - Y > 0:
        reactivated = np.sum(rng.random(K - Y) <= (1 - beta))
    else:
        reactivated = 0

    Y = stay_active + reactivated

    # --- Initially inactive cohort ---
    if Z > 0:
        stay_active2 = np.sum(rng.random(Z) <= alpha)
    else:
        stay_active2 = 0

    if (N - K - Z) > 0:
        reactivated2 = np.sum(rng.random(N - K - Z) <= (1 - beta))
    else:
        reactivated2 = 0

    Z = stay_active2 + reactivated2

    # record indicator after burn-in
    if step > burn_in:
        indicator_total += int(Y > Z)

# estimate probability
p_est = indicator_total / (T - burn_in)
print(f"(d) Estimated P(Y_n > Z_n) ≈ {p_est:.6f}")
