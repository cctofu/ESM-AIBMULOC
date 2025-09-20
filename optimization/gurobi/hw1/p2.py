import gurobipy as gp
from gurobipy import GRB

model = gp.Model("Perfume")

# Decision Variables
x1 = model.addVar(vtype=GRB.INTEGER, name="process_1_runs")
x2 = model.addVar(vtype=GRB.INTEGER, name="process_2_runs")
p = model.addVar(vtype=GRB.INTEGER, name="promoter_hours")

# Objective Function
model.setObjective(8*x1 + 13*x2 - 100*p, GRB.MAXIMIZE)

# Constraints
model.addConstr(x1 + 2*x2 <= 20000, 'c0')
model.addConstr(2*x1 + 3*x2 <= 35000, 'c1')
model.addConstr(3*x1 + 5*x2 <= 1000 + 200*p, 'c2')

# Optimize
model.optimize()
print(model.objVal)
for v in model.getVars():
    print(v.VarName, v.X)
