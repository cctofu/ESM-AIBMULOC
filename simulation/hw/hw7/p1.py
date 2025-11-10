import numpy as np

# Number of simulation runs
n = 1000

# 1. Generate uniform samples
U = np.random.uniform(0, 1, n)

# 2. Define transformations
Y1 = np.exp(U)               # e^U
Y2 = np.sqrt(1 - U**2)       # sqrt(1 - U^2)

# 3. Compute means
U_bar = np.mean(U)
Y1_bar = np.mean(Y1)
Y2_bar = np.mean(Y2)

# 4. Compute sample covariances
Cov_U_eU = np.mean((U - U_bar) * (Y1 - Y1_bar))
Cov_U_sqrt = np.mean((U - U_bar) * (Y2 - Y2_bar))

# 5. Compute variances
Var_U = np.mean((U - U_bar)**2)
Var_Y2 = np.mean((Y2 - Y2_bar)**2)

# 6. Compute correlation
Corr_U_sqrt = Cov_U_sqrt / np.sqrt(Var_U * Var_Y2)

# 7. Print results
print(f"Estimated Cov(U, e^U): {Cov_U_eU:.4f}")
print(f"Estimated Corr(U, sqrt(1 - U^2)): {Corr_U_sqrt:.4f}")
