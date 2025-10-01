import gurobipy as gp
from gurobipy import GRB

m = gp.Model("production")
# decision variables
x11 = m.addVar(vtype=GRB.INTEGER, name="x11", lb=0)
x12 = m.addVar(vtype=GRB.INTEGER, name="x12", lb=0)
x13 = m.addVar(vtype=GRB.INTEGER, name="x13", lb=0)
x21 = m.addVar(vtype=GRB.INTEGER, name="x12", lb=0)
x22 = m.addVar(vtype=GRB.INTEGER, name="x12", lb=0)
x23 = m.addVar(vtype=GRB.INTEGER, name="x12", lb=0)

# Objective
m.setObjective(10*x11 + 12*x12 + 14*x13 + 11*x21 + 12*x22 + 13*x23, GRB.MINIMIZE)

# Constraints
m.addConstr(x11 + x21 >= 50, "c1")
m.addConstr(x12 + x22 >= 100, "c2")
m.addConstr(x13 + x23 >= 150, "c3")
m.addConstr(x11 + x12 + x13 <= 100, "c4")
m.addConstr(x21 + x22 + x23 <= 200, "c5")

m.optimize()
print(m.objVal)
for v in m.getVars():
    print(v.VarName, v.X)
