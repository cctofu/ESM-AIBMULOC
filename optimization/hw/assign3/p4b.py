import gurobipy as gp
from gurobipy import GRB
import numpy as np

def solve_primal(V):
    """Solve the primal LP and return OPT value, primal matrix X, matching M*,
       and the model + constraints (to read duals u*, p*)."""
    n, m = V.shape
    model = gp.Model("primal")

    x = model.addVars(n, m, lb=0.0, vtype=GRB.CONTINUOUS, name="x")

    model.setObjective(gp.quicksum(V[i, j] * x[i, j] for i in range(n) for j in range(m)), GRB.MAXIMIZE)

    buyer_constr  = [model.addConstr(gp.quicksum(x[i, j] for j in range(m)) <= 1.0) for i in range(n)]
    seller_constr = [model.addConstr(gp.quicksum(x[i, j] for i in range(n)) <= 1.0) for j in range(m)]

    model.optimize()
    X = np.array([[x[i, j].X for j in range(m)] for i in range(n)])
    M = [(i, j) for i in range(n) for j in range(m) if X[i, j] > 0.5]
    return model.ObjVal, X, M, model, buyer_constr, seller_constr

def check_other_matching(V, opt_val, M_star):
    """Exclude M* and re-solve. If value is still OPT, another matching exists."""
    n, m = V.shape
    model = gp.Model("primal_exclude")

    x = model.addVars(n, m, lb=0.0, vtype=GRB.CONTINUOUS, name="x")
    model.setObjective(gp.quicksum(V[i, j] * x[i, j] for i in range(n) for j in range(m)), GRB.MAXIMIZE)

    model.addConstrs((gp.quicksum(x[i, j] for j in range(m)) <= 1.0 for i in range(n)))
    model.addConstrs((gp.quicksum(x[i, j] for i in range(n)) <= 1.0 for j in range(m)))

    if M_star:
        model.addConstr(gp.quicksum(x[i, j] for (i, j) in M_star) <= len(M_star) - 1)

    model.optimize()
    same_value = abs(model.ObjVal - opt_val) <= 1e-6
    return same_value, model.ObjVal

def check_other_prices(V, opt_val, u_star, p_star):
    n, m = V.shape
    dual = gp.Model("dual_face")

    u = dual.addVars(n, lb=0.0, name="u")  
    p = dual.addVars(m, lb=0.0, name="p")  

    dual.addConstrs((u[i] + p[j] >= V[i, j] for i in range(n) for j in range(m)))

    dual.addConstr(gp.quicksum(u[i] for i in range(n)) + gp.quicksum(p[j] for j in range(m)) == opt_val)

    r_u = np.random.standard_normal(n)
    r_p = np.random.standard_normal(m)
    dual.setObjective(gp.quicksum(float(r_u[i]) * u[i] for i in range(n)) + gp.quicksum(float(r_p[j]) * p[j] for j in range(m)), GRB.MAXIMIZE)

    dual.optimize()
    u_alt = np.array([u[i].X for i in range(n)])
    p_alt = np.array([p[j].X for j in range(m)])

    dist = np.linalg.norm(u_alt - u_star, 1) + np.linalg.norm(p_alt - p_star, 1)
    return (dist > 1e-7), dist

def check_another_equilibrium(V):
    opt_val, X, M_star, model, buyer_constr, seller_constr = solve_primal(V)
    u_star = np.array([c.Pi for c in buyer_constr], dtype=float)
    p_star = np.array([c.Pi for c in seller_constr], dtype=float)

    has_other_M, _ = check_other_matching(V, opt_val, M_star)
    if has_other_M:
        return True, "different matching"
    has_other_prices, dist = check_other_prices(V, opt_val, u_star, p_star)
    if has_other_prices:
        return True, f"different prices (L1 distance={dist:.3g})"
    return False, "unique equilibrium"

if __name__ == "__main__":
    n, m = 10, 20
    V = np.random.randint(1, 101, size=(n, m)).astype(float)
    flag, info = check_another_equilibrium(V)
    print(f"Another equilibrium exists: {flag}")
    print(f"Type:{info}")
    
