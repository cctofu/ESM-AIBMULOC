import numpy as np

# ============================================================
# Problem 3 – G/G/1 queue simulation
# ============================================================

def simulate_GG1(N=1000, burn_in=100):

    W = 0.0   # W_0
    S = 0.0   # S_0

    collected_waits = []

    for n in range(N):

        # Generate next interarrival X ~ Exp(0.5)
        X = -2 * np.log(np.random.rand())

        # Compute waiting time
        W_new = max(0.0, W + S - X)

        # Generate Gamma(3,2) as sum of 3 Exp(2)
        S_new = 0.0
        for _ in range(3):
            U = np.random.rand()
            S_new += -0.5 * np.log(U)   # Exp(2)

        # Collect after burn-in
        if n >= burn_in:
            collected_waits.append(W_new)

        # Update
        W = W_new
        S = S_new

    return np.mean(collected_waits)


print("Problem 3 estimated long-run average waiting time:",
      simulate_GG1(N=1000, burn_in=100))