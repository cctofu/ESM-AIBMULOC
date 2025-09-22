import gurobipy as gp
from gurobipy import GRB

model = gp.Model("Oil")

# Decision variables
x = model.addVar(vtype=GRB.INTEGER, name="crude_oil", lb=0)
a = model.addVar(vtype=GRB.INTEGER, name="aviation_oil", lb=0)
h = model.addVar(vtype=GRB.INTEGER, name="heating_oil", lb=0)

# Objective function
model.setObjective(10*x + 70*a + 50*h, GRB.MAXIMIZE)

# Constraints
model.addConstr(a <= 0.5*x, "c0")
model.addConstr(h <= 0.5*x, "c1")
model.addConstr(a + 0.75*h <= 8, "c2")
model.addConstr(x <= 20, "c3")

# Optimize
model.optimize()
print(model.objVal)
for v in model.getVars():
    print(v.VarName, v.X)
