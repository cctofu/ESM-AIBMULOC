import gurobipy as gp
from gurobipy import GRB
import numpy as np

def solve_assignment_game(V):
    n, m = V.shape
    model = gp.Model("assignment_game")
    model.Params.OutputFlag = 0 

    x = model.addVars(n, m, lb=0.0, vtype=GRB.CONTINUOUS, name="x")

    model.setObjective(gp.quicksum(V[i, j] * x[i, j]
                                   for i in range(n) for j in range(m)),
                       GRB.MAXIMIZE)

    for i in range(n):
        model.addConstr(gp.quicksum(x[i, j] for j in range(m)) <= 1)
    for j in range(m):
        model.addConstr(gp.quicksum(x[i, j] for i in range(n)) <= 1)

    model.optimize()

    X = np.array([[x[i, j].X for j in range(m)] for i in range(n)])
    val = model.ObjVal
    num_matches = int(np.sum(X > 0.5))
    return val, num_matches

if __name__ == "__main__":
    n, m = 10, 20
    num_instances = 50

    for k in range(num_instances):
        V = np.random.randint(1, 11, size=(n, m)).astype(float)
        val, M, = solve_assignment_game(V)
        print(f"Iteration {k+1}: value = {val:6.2f}, M = {M}")
