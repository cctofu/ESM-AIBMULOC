import numpy as np

# ============================================================
# Generate one replication: returns Y, S_list, X_list
# ============================================================

def one_replication():
    # Generate interarrival times X_1,...,X_11
    # Exp(2) ⇒ mean = 1/2
    X = np.random.exponential(scale=1/2, size=11)

    # Generate service times S_1,...,S_10
    # Exp(1)
    S = np.random.exponential(scale=1, size=10)

    W = 0.0
    Y = 0.0
    S_prev = 0.0

    for i in range(10):
        # Lindley recursion
        W = max(0.0, W + S_prev - X[i])     # W_(i+1)
        T = W + S[i]                        # T_(i+1)
        Y += T
        S_prev = S[i]

    return Y, S, X


# ============================================================
# (a) Naive Monte Carlo
# ============================================================

def estimate_naive(R=100):
    Ys = []
    for _ in range(R):
        Y, _, _ = one_replication()
        Ys.append(Y)
    Ys = np.array(Ys)
    return Ys.mean(), Ys.var(ddof=1)


# ============================================================
# (b) CV1 = sum S_i,     E[C1] = 10
# ============================================================

def estimate_cv1(R=100):
    pairs = []
    for _ in range(R):
        Y, S, _ = one_replication()
        C1 = S.sum()
        pairs.append((Y, C1))

    Y_vals = np.array([p[0] for p in pairs])
    C_vals = np.array([p[1] for p in pairs])

    # Compute sample means
    Y_bar = Y_vals.mean()
    C_bar = C_vals.mean()

    # Covariance and variance
    cov_YC = np.sum((Y_vals - Y_bar) * (C_vals - C_bar)) / (R - 1)
    var_C = np.sum((C_vals - C_bar)**2) / (R - 1)

    # Control coefficient
    b_hat = cov_YC / var_C

    # Controlled estimator
    Z = Y_vals - b_hat * (C_vals - 10)

    return Z.mean(), Z.var(ddof=1), b_hat


# ============================================================
# (c) CV2 = sum S_i – sum X_{i+1},     E[C2] = 10 – 10*(1/2) = 5
# ============================================================

def estimate_cv2(R=100):
    pairs = []
    for _ in range(R):
        Y, S, X = one_replication()
        C2 = S.sum() - X[1:11].sum()
        pairs.append((Y, C2))

    Y_vals = np.array([p[0] for p in pairs])
    C_vals = np.array([p[1] for p in pairs])

    # Compute sample means
    Y_bar = Y_vals.mean()
    C_bar = C_vals.mean()

    # Covariance and variance
    cov_YC = np.sum((Y_vals - Y_bar) * (C_vals - C_bar)) / (R - 1)
    var_C = np.sum((C_vals - C_bar)**2) / (R - 1)

    # Control coefficient
    b_hat = cov_YC / var_C

    # Controlled estimator
    Z = Y_vals - b_hat * (C_vals - 5)

    return Z.mean(), Z.var(ddof=1), b_hat


# ============================================================
# Run all three parts
# ============================================================

if __name__ == "__main__":
    print("\n===== Problem 5 Results (100 replications each) =====\n")

    # (a) Naive MC
    mu_naive, var_naive = estimate_naive()
    print("(a) Naive estimator:")
    print("   Mean estimate =", mu_naive)
    print("   Variance per replication =", var_naive, "\n")

    # (b) Control variate C1
    mu_cv1, var_cv1, b1 = estimate_cv1()
    print("(b) Control variate C1 = sum S_i:")
    print("   Mean estimate =", mu_cv1)
    print("   Variance per replication =", var_cv1)
    print("   b1 =", b1)
    print("   Variance reduction =", var_naive / var_cv1, "\n")

    # (c) Control variate C2
    mu_cv2, var_cv2, b2 = estimate_cv2()
    print("(c) Control variate C2 = sum S_i – sum X_{i+1}:")
    print("   Mean estimate =", mu_cv2)
    print("   Variance per replication =", var_cv2)
    print("   b2 =", b2)
    print("   Variance reduction =", var_naive / var_cv2)
