import gurobipy as gp
from gurobipy import GRB

model = gp.Model("Stocks")

# Decision variables
x = model.addVars(10, lb=0.0, ub=100, vtype=GRB.CONTINUOUS, name="sell_stock")
price_pur = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
price_cur = [30, 34, 43, 47, 49, 53, 60, 62, 64, 66]
price_fut = [36, 39, 42, 45, 51, 55, 63, 64, 66, 70]

# Objective function
model.setObjective(gp.quicksum((100 - x[i]) * price_fut[i] for i in range(10)), GRB.MAXIMIZE)

# Constraints
# Per-share net cash if sold today (after tax on gains and 1% fee)
net_cash = [
    price_cur[i] * (1 - 0.01) - 0.30 * max(price_cur[i] - price_pur[i], 0.0)
    for i in range(len(price_pur))
]
model.addConstr(gp.quicksum(x[i] * net_cash[i] for i in range(len(price_pur))) == 30000,)

# Optimize
model.optimize()
print(model.ObjVal)
for v in model.getVars():
    print(v.VarName, v.X)