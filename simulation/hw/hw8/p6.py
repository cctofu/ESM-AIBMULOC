import numpy as np
from scipy.stats import norm
from math import comb, sqrt

# ============================================================
# Problem 6: Credit Risk Portfolio Simulation
# ============================================================

N = 100              # number of loans
mu_X = 3             # mean loss given default
sigma_X = 1          # std dev of loss given default
R = 100              # number of replications
threshold = 45       # loss threshold x = 45

# ------------------------------------------------------------
# Sample P ~ Beta(1,19) using inverse transform
# ------------------------------------------------------------
def sample_beta_1_19():
    U = np.random.rand()
    return 1 - (1 - U)**(1/19)


# ------------------------------------------------------------
# (1) Naive Monte Carlo replication
# ------------------------------------------------------------
def one_replication_naive():
    P = sample_beta_1_19()

    # Bernoulli defaults
    D = (np.random.rand(N) < P)

    # Loss given default ~ N(3,1)
    X = np.random.normal(mu_X, sigma_X, size=N)

    # Compute L
    L = np.sum(D * X)

    return 1.0 if L > threshold else 0.0


# ------------------------------------------------------------
# (2) Conditional Monte Carlo replication
# ------------------------------------------------------------
def one_replication_conditional():
    P = sample_beta_1_19()

    total_prob = 0.0

    # Sum over possible number of defaults K = 0,...,N
    for k in range(N + 1):

        # Binomial probability
        binom_prob = comb(N, k) * (P**k) * ((1 - P)**(N - k))

        if k == 0:
            tail = 0.0   # no defaults -> cannot exceed threshold
        else:
            mean = mu_X * k
            sd = sqrt(k)
            z = (threshold - mean) / sd
            tail = 1 - norm.cdf(z)    # Gaussian tail

        total_prob += binom_prob * tail

    return total_prob


# ------------------------------------------------------------
# Run all experiments
# ------------------------------------------------------------
if __name__ == "__main__":
    print("=== Problem 6 ===\n")

    # ------------------------
    # Naive Monte Carlo
    # ------------------------
    Ys = np.array([one_replication_naive() for _ in range(R)])
    est_naive = Ys.mean()
    var_naive = Ys.var(ddof=1)

    print("(1) Naive Monte Carlo")
    print("   Estimate =", est_naive)
    print("   Variance per replication =", var_naive, "\n")

    # ------------------------
    # Conditional Monte Carlo
    # ------------------------
    Zs = np.array([one_replication_conditional() for _ in range(R)])
    est_cond = Zs.mean()
    var_cond = Zs.var(ddof=1)

    print("(2) Conditional Monte Carlo")
    print("   Estimate =", est_cond)
    print("   Variance per replication =", var_cond, "\n")

    print("Variance reduction factor =", var_naive / var_cond)
