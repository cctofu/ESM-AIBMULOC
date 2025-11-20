import numpy as np

T = 10.0

# Intensity function λ(t) = 2 + cos(2πt)
def lambda_t(t):
    return 2 + np.cos(2 * np.pi * t)

# Problem 2(a).1  Interarrival + Thinning
# ============================================================
def simulate_inhom_poisson_interarrival(T):
    """Simulate inhomogeneous Poisson process using interarrival + thinning."""
    lam_bar = 3.0   # Upper bound of lambda(t)
    t = 0
    arrivals = []

    while True:
        # Generate interarrival time Exp(lam_bar)
        U = np.random.rand()
        s = -np.log(U) / lam_bar
        t += s
        if t > T:
            break

        # Thinning
        V = np.random.rand()
        if V <= lambda_t(t) / lam_bar:
            arrivals.append(t)

    return np.array(arrivals)


# Problem 2(a).2  Conditional + Thinning
# ============================================================
def simulate_inhom_poisson_conditional(T):
    """Simulate inhomogeneous Poisson process via conditional representation + thinning."""
    lam_bar = 3.0

    N = np.random.poisson(lam_bar * T)

    # Generate uniform proposal times
    U = np.sort(np.random.rand(N))
    proposal_times = T * U

    arrivals = []
    for t in proposal_times:
        if np.random.rand() <= lambda_t(t) / lam_bar:
            arrivals.append(t)

    return np.array(arrivals)


# Problem 2(a).3  Modified Conditional (No Rejection)
# ============================================================

# Mean value function m(t)
def m_t(t):
    return 2 * t + (1 / (2 * np.pi)) * np.sin(2 * np.pi * t)

# Numerical inverse of m(t)
def inverse_m(uT):
    """Numerically solve m(t) = u * m(T) using bisection."""
    target = uT
    lo, hi = 0, T

    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if m_t(mid) < target:
            lo = mid
        else:
            hi = mid

    return 0.5 * (lo + hi)

def simulate_inhom_poisson_modified(T):
    """Simulate using modified conditional representation (no acceptance-rejection)."""
    N = np.random.poisson(m_t(T))
    U = np.random.rand(N)
    arrivals = [inverse_m(u * m_t(T)) for u in U]
    return np.sort(arrivals)


# Problem 2(b)  Time-averaged number of customers
# ============================================================

def time_average_from_arrivals(arrivals, T):
    """Compute (1/T) ∫₀ᵀ N(t) dt = (1/T) Σ (T - A_i)."""
    return np.sum(T - arrivals) / T


def estimate_time_average(simulator, R=100):
    """Perform 100 replications and estimate expected time-averaged number."""
    Ys = []

    for _ in range(R):
        arr = simulator(T)
        Ys.append(time_average_from_arrivals(arr, T))

    return np.mean(Ys)


# RUN PROBLEM 2 RESULTS
# ============================================================

print("Problem 2(b) estimates:\n")

print("Method 1 (Interarrival + thinning): ",
      estimate_time_average(simulate_inhom_poisson_interarrival))

print("Method 2 (Conditional + thinning): ",
      estimate_time_average(simulate_inhom_poisson_conditional))

print("Method 3 (Modified conditional): ",
      estimate_time_average(simulate_inhom_poisson_modified))
