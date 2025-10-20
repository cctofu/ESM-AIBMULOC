from gurobipy import Model, GRB, quicksum

def optimize():
    A = [
        [ 4,  3, -1, -1, -1],
        [ 1,  4,  3, -1, -1],
        [ 1,  1,  4,  3, -1],
        [ 1,  1,  1,  4,  3],
    ]
    m_rows = len(A)     
    n_cols = len(A[0])  
    m2 = Model("P2_maximin")
    m2.Params.OutputFlag = 0

    p = m2.addVars(n_cols, lb=0.0, name="p")   
    v = m2.addVar(lb=-GRB.INFINITY, name="v") 

    for i in range(m_rows):
        m2.addConstr(quicksum(A[i][j] * p[j] for j in range(n_cols)) >= v, name=f"row_{i}")
    m2.addConstr(quicksum(p[j] for j in range(n_cols)) == 1.0, name="prob_simplex")

    m2.setObjective(v, GRB.MAXIMIZE)
    m2.optimize()

    p_opt = [p[j].X for j in range(n_cols)]
    v_opt = v.X

    row_payoffs = []
    for i in range(m_rows):
        row_payoffs.append(sum(A[i][j] * p_opt[j] for j in range(n_cols)))

    m1 = Model("P1_minimax")
    m1.Params.OutputFlag = 0

    q = m1.addVars(m_rows, lb=0.0, name="q")  
    w = m1.addVar(lb=-GRB.INFINITY, name="w")  

    for j in range(n_cols):
        m1.addConstr(quicksum(q[i] * A[i][j] for i in range(m_rows)) <= w, name=f"col_{j}")
    m1.addConstr(quicksum(q[i] for i in range(m_rows)) == 1.0, name="prob_simplex")

    m1.setObjective(w, GRB.MINIMIZE)
    m1.optimize()

    q_opt = [q[i].X for i in range(m_rows)]
    w_opt = w.X

    col_payoffs = []
    for j in range(n_cols):
        col_payoffs.append(sum(q_opt[i] * A[i][j] for i in range(m_rows)))

    rows = ["(0,3)", "(1,2)", "(2,1)", "(3,0)"]
    cols = ["(0,4)", "(1,3)", "(2,2)", "(3,1)", "(4,0)"]
    print("----Player 1----")
    print(f"Optimal value w* = {w_opt:.2f}")
    for i, name in enumerate(rows):
        print(f"q[{name}] = {q_opt[i]:.2f}")
    print("\n----Player 2----")
    print(f"Optimal value v* = {v_opt:.2f}")
    for j, name in enumerate(cols):
        print(f"p[{name}] = {p_opt[j]:.2f}")


if __name__ == "__main__":
    optimize()
