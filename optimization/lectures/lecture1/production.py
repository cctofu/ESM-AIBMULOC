import gurobipy as gp
from gurobipy import GRB

m = gp.Model("production")
# decision variables
x1 = m.addVar(vtype=GRB.INTEGER, name="tables")
x2 = m.addVar(vtype=GRB.INTEGER, name="chairs")
# Objective
m.setObjective(3*x1 + 2*x2, GRB.MAXIMIZE)
# Constraints
m.addConstr(x1 >= 0, "c0")
m.addConstr(x2 >= 0, "c1")
m.addConstr(x1 <= 40, "c2")
m.addConstr(x1 + x2 <= 80, "c3")
m.addConstr(2*x1 + x2 <= 100, "c4")

m.optimize()
for v in m.getVars():
    print(v.VarName, v.X)
