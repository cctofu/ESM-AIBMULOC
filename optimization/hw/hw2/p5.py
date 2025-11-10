import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(42)

def make_feasible_instance(T=50,
                           prod_cap_low=5, prod_cap_high=20,
                           demand_low=0, demand_high=15,
                           hold_cap_scale=3,
                           cost_low=1.0, cost_high=10.0,
                           hold_low=0.0, hold_high=3.0):
    """
    Create a feasible instance by:
      - drawing random demands d_t
      - drawing random production capacities u_t, then scaling the last few to guarantee sum(u)>=sum(d)
      - setting large enough storage caps q_t so feasibility is not blocked
    """
    d = rng.integers(demand_low, demand_high+1, size=T)  # demand >= 0
    u = rng.integers(prod_cap_low, prod_cap_high+1, size=T)

    # Ensure total production capacity >= total demand
    deficit = d.sum() - u.sum()
    if deficit > 0:
        # add capacity to random periods
        idx = rng.choice(T, size=min(T, max(1, (deficit + prod_cap_high - 1)//prod_cap_high)), replace=False)
        u[idx] += (deficit + len(idx) - 1)//len(idx)

    # Holding caps: make them generous enough (still finite)
    # e.g., proportional to average demand times a scale
    avg_d = max(1, int(d.mean()))
    q = rng.integers(avg_d, avg_d*hold_cap_scale + 1, size=T-1)

    # Costs
    c = rng.uniform(cost_low, cost_high, size=T)         # production cost
    h = rng.uniform(hold_low, hold_high, size=T-1)       # holding cost

    return d, u, q, c, h

def solve_lot_sizing(d, u, q, c, h):
    """
    LP:
      min sum c_t x_t + sum h_t s_t
      s_{t-1} + x_t = d_t + s_t, t=1..T   (s_0=0, s_T=0)
      0 <= x_t <= u_t
      0 <= s_t <= q_t for t=1..T-1; s_T=0
    """
    T = len(d)
    n_x = T
    n_s = T             # we'll include s_1..s_T as variables; s_0 is fixed 0
    n = n_x + n_s

    # Objective
    c_vec = np.zeros(n)
    c_vec[:n_x] = c
    c_vec[n_x:n_x+T-1] = h  # s_1..s_{T-1} have holding cost
    # s_T cost is zero by convention

    # Equality constraints: flow balance for t=1..T plus s_T = 0
    Aeq = np.zeros((T+1, n))
    beq = np.zeros(T+1)

    # t = 1..T:  x_t - s_t + s_{t-1} = d_t; with s_0=0 (constant)
    for t in range(1, T+1):
        # x_t
        Aeq[t-1, t-1] = 1.0
        # -s_t  (s_t is at index n_x + (t-1))
        Aeq[t-1, n_x + (t-1)] = -1.0
        # +s_{t-1} if t>1
        if t > 1:
            Aeq[t-1, n_x + (t-2)] = 1.0
        beq[t-1] = d[t-1]

    # s_T = 0
    Aeq[T, n_x + (T-1)] = 1.0
    beq[T] = 0.0

    # Bounds
    bounds = []
    # x_t bounds
    for t in range(T):
        bounds.append((0.0, float(u[t])))
    # s_1..s_{T-1}: [0, q_t]
    for t in range(T-1):
        bounds.append((0.0, float(q[t])))
    # s_T: fixed 0
    bounds.append((0.0, 0.0))

    res = linprog(c_vec, A_eq=Aeq, b_eq=beq, bounds=bounds, method="highs")
    return res

def summary(res, d, u, q):
    T = len(d)
    n_x = T
    if not res.success:
        return {"success": False, "message": res.message}

    x = res.x[:n_x]
    s = res.x[n_x:]

    # Diagnostics
    eps = 1e-7
    at_bound_x = np.mean((np.isclose(x, 0, atol=eps)) | (np.isclose(x, u, atol=1e-7)))
    at_bound_s = np.mean(np.r_[np.isclose(s[:-1], 0, atol=eps) | np.isclose(s[:-1], q, atol=1e-7), [True]])  # s_T fixed
    integrality_x = np.mean(np.isclose(x, np.round(x), atol=1e-6))
    integrality_s = np.mean(np.isclose(s, np.round(s), atol=1e-6))

    return {
        "success": True,
        "obj": res.fun,
        "x_mean": float(x.mean()),
        "s_mean": float(s.mean()),
        "share_x_at_bounds": float(at_bound_x),
        "share_s_at_bounds": float(at_bound_s),
        "share_x_integral": float(integrality_x),
        "share_s_integral": float(integrality_s),
    }

# Generate and solve 10 instances
T = 50
stats = []
for k in range(10):
    d, u, q, c, h = make_feasible_instance(T=T)
    res = solve_lot_sizing(d, u, q, c, h)
    stats.append(summary(res, d, u, q))

for i, st in enumerate(stats, 1):
    print(f"Instance {i}: {st}")
